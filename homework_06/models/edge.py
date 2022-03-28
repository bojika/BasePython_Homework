from sqlalchemy import Column, Integer, String
from .database import db


class Edge(db.Model):
    id = Column(Integer, primary_key=True)
    node_a = Column(String, nullable=False)
    node_b = Column(String, nullable=False)
    cost = Column(String, nullable=False)
    meta_data = Column(String, nullable=True)

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.node_a!r} {self.node_b!r} {self.cost!r} {self.meta_data!r}>"
