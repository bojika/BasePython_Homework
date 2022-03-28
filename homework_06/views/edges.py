from http import HTTPStatus

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)

from sqlalchemy.exc import IntegrityError, DatabaseError
from werkzeug.exceptions import NotFound, BadRequest, InternalServerError

from forms import EdgeForm, ImportForm
from models import Edge
from models.database import db
import textfsm

edges_app = Blueprint("edges_app", __name__)


@edges_app.get("/", endpoint="edges_list")
def list_edges():
    print(f'request.args: {request.args}')
    edges: list[Edge] = Edge.query.all()
    return render_template("edges/list.html", edges=edges)


@edges_app.route("/delete/", endpoint="edge_delete", methods=["GET", "POST"])
def delete_edge():
    print(f'request.args: {request.args}')
    edge_id = request.args['edge_id']
    edge_to_delete = Edge.query.get_or_404(edge_id)
    print(edge_to_delete)
    try:
        db.session.delete(edge_to_delete)
        db.session.commit()
        flash("Ребро успешно удалено.")
    except:
        flash('Что-то пошло не так при удалении ребра')

    edges_list_url = url_for("edges_app.edges_list")
    return redirect(edges_list_url)


@edges_app.route("/update/<int:edge_id>/", methods=["GET", "POST"], endpoint="update")
def update_edge(edge_id: int):
    form = EdgeForm()
    edge_to_update = Edge.query.get_or_404(edge_id)
    if request.method == "GET":
        return render_template("edges/update.html", edge=edge_to_update, form=form)

    if not form.validate_on_submit():
        return render_template("edges/add.html", form=form), HTTPStatus.BAD_REQUEST

    if edge_to_update is None:
        raise NotFound(f"Ребро #{edge_to_update} не найдено!")

    edge_to_update.node_a = form.data["node_a"]
    edge_to_update.node_b = form.data["node_b"]
    edge_to_update.cost = form.data["cost"]
    edge_to_update.meta_data = form.data["meta_data"]
    db.session.add(edge_to_update)

    try:
        db.session.commit()
    except DatabaseError:
        db.session.rollback()
        raise InternalServerError(f"could not save data, unexpected error")

    edges_list_url = url_for("edges_app.edges_list")
    return redirect(edges_list_url)

@edges_app.route("/add/", methods=["GET", "POST"], endpoint="add")
def add_edge():
    form = EdgeForm()
    if request.method == "GET":
        return render_template("edges/add.html", form=form)

    if not form.validate_on_submit():
        return render_template("edges/add.html", form=form), HTTPStatus.BAD_REQUEST

    node_a = form.data["node_a"]
    node_b = form.data["node_b"]
    cost = form.data["cost"]
    meta_data = form.data["meta_data"]
    edge = Edge(node_a=node_a, node_b=node_b, cost=cost, meta_data=meta_data)
    db.session.add(edge)

    try:
        db.session.commit()
    except DatabaseError:
        db.session.rollback()
        raise InternalServerError(f"could not save data, unexpected error")

    edges_list_url = url_for("edges_app.edges_list")
    return redirect(edges_list_url)


@edges_app.route("/import/", methods=["GET", "POST"], endpoint="import")
def import_lsdb():
    form = ImportForm()
    if request.method == "GET":
        return render_template("edges/import.html", form=form, data="raw_lsdb")

    if not form.validate_on_submit():
        return render_template("edges/add.html", form=form), HTTPStatus.BAD_REQUEST

    raw_lsdb = form.data["raw_data"]

    def get_lsdb(raw_lsdb):
        # let's check what we have. IS-IS or OSPF
        if "ATT/P/OL" in raw_lsdb:
            # IS-IS
            template = open('./templates/tfsm/sh_isis_database_iosxr_1.template')
            fsm = textfsm.TextFSM(template)
            result_1 = fsm.ParseText(raw_lsdb)

            lsdb = [[str(i), x[0][:-3] if x[0][-3:] == '.00' else x[0], x[1][:-3] if x[1][-3:] == '.00' else x[1], x[2],
                     x[0] + "->" + x[1]] for i, x in enumerate(result_1, 1)]

            template = open('./templates/tfsm/sh_isis_database_iosxr_2.template')
            fsm = textfsm.TextFSM(template)
            result_2 = fsm.ParseText(raw_lsdb)

        else:
            # OSPF
            template = "./templates/tfsm/sh_ip_ospf_database_router.tfsm"

            f = open(template)
            re_table = textfsm.TextFSM(f)
            header = re_table.header
            result = re_table.ParseText(raw_lsdb)

            # T - transit, P - p2p, S - stub
            for i, s in enumerate(result):
                result[i][3] = str(result[i][3][0:1]).upper()

            # remove stub links
            result = [a for a in result if a[3] != "S"]

            # process "R" router LSA
            lsdb = list(
                [str(a), result[a][0], "DR_" + result[a][5] if result[a][3] == "T" else result[a][4], result[a][8],
                 result[a][6]] for a in range(len(result)) if result[a][9] == "R")
            # process "N" network LSA
            lsdb += list([str(a), "DR_" + result[a][0], result[a][10], "0", result[a][0]] for a in range(len(result)) if
                         result[a][9] == "N")

        return (lsdb)

    edges = [Edge(node_a=edge[1], node_b=edge[2], cost=edge[3], meta_data=edge[4]) for edge in get_lsdb(raw_lsdb)]
    for edge in edges:
        db.session.add(edge)

    try:
         db.session.commit()
    except DatabaseError:
         db.session.rollback()
         raise InternalServerError(f"could not save data, unexpected error")

    edges_list_url = url_for("edges_app.edges_list")
    return redirect(edges_list_url)