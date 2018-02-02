from db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    mail = db.Column(db.String(200))
    mobile = db.Column(db.String(80))

    def __init__(self, username, password, mail, mobile):
        self.username = username
        self.password = password
        self.mail = mail
        self.mobile = mobile

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {'id': self.id, 'username': self.username,
                'mail': self.mail,
                'mobile': self.mobile}

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
