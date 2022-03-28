from os import getenv
from flask import Flask, render_template, json
from flask_migrate import Migrate
from models.database import db
from models import Edge
from views.edges import edges_app

app: Flask = Flask(__name__)

# берём имя конфига из окружения, если не задано, то это DevelopmentConfig
CONFIG_OBJECT_PATH = f"config.{getenv('CONFIG_NAME', 'DevelopmentConfig')}"
app.config.from_object(CONFIG_OBJECT_PATH)

db.init_app(app)

# используем alembic, чтобы создать схему для db
migrate = Migrate(app, db)

app.register_blueprint(edges_app, url_prefix="/edges")


@app.get("/", endpoint="home")
def hello_world():
    return render_template("index.html")

@app.get("/topology/", endpoint="topology")
def draw_topology():
    edges: list[Edge] = Edge.query.all()

    data = {"edges": [{"from": edge.node_a,
                       "to": edge.node_b,
                       "label": edge.cost,
                       "font": {"aligin": "middle"},
                       "title": f'id: {edge.id}, meta: {edge.meta_data}'} for edge in edges],
            "nodes": [{"id": node,
                       "label": node,
                       "title": node} for node in {edge.node_a for edge in edges} | {edge.node_b for edge in edges}]}
    return render_template(
        "topology.html",
        nodes=json.dumps(data['nodes']),
        edges=json.dumps(data['edges'])
    )

if __name__ == '__main__':
    app.run(host="0.0.0.0")
