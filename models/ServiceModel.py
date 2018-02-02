import psycopg2
from db import db

class ServiceModel(db.Model):
    __tablename__ = 'service'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    url = db.Column(db.String(200))
    type_due = db.Column(db.String(200)) # by_date means there is a due date or by_balance means alert before it ends


    def __init__(self, name):
        self.name = name

    def json(self):
        return { 'id': self.id, 'name': self.name}
        #return {'name': self.name, 'items': [item.json() for item in self.items.all()]}


    @classmethod
    def find_by_name(cls, name):
        print('here name')
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
