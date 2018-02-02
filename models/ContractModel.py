from db import db


class ContractModel(db.Model):
    __tablename__ = 'contract'

    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    service = db.relationship('ServiceModel')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('UserModel')
    counterpart = db.Column(db.String(200))
    login = db.Column(db.String(200))
    password = db.Column(db.String(200)) 
    alert_before = db.Column(db.String(200))

    def __init__(self, service, user, counterpart):
        
        self.service = service
        self.user = user
        self.counterpart = counterpart

    def json(self):
        return {'counterpar': self.counterpart,
                'service': self.service.name,
                'type_service': self.service.type_due,
                'user': self.user.username,
                'alert_before': self.alert_before}

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find(cls, serviceid, userid, counterpart):
        return cls.query.filter_by(service_id=serviceid, 
                                user_id=userid,
                                counterpart=counterpart
                                ).first()

    @classmethod
    def find_by_user(cls, user):
        return cls.query.filter_by(user_id=user).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
