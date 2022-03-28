from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField
from wtforms.validators import DataRequired


class EdgeForm(FlaskForm):
    node_a = StringField("Node A:", name="node_a", validators=[DataRequired()])
    node_b = StringField("Node B:", name="node_b", validators=[DataRequired()])
    cost = IntegerField("Cost:", name="cost", validators=[DataRequired()])
    meta_data = StringField("Meta:", name="meta", validators=[DataRequired()])


class ImportForm(FlaskForm):
    raw_data = TextAreaField("LSDB", name="raw_data", validators=[DataRequired()])
