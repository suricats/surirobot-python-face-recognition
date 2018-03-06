from management import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    pictures = db.relationship("Picture", back_populates="user")

    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname


class Picture(db.Model):
    __tablename__ = 'picture'

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(250))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="pictures")

    def __init__(self, path, user):
        self.path = path
        self.user = user
