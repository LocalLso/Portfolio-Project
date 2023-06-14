from portfolio import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Teachers.query.get(int(user_id))


class Teachers(db.Model, UserMixin):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"Teachers('{self.username}', '{self.email}', '{self.image_file}')"


class Students(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"Students('{self.username}', '{self.email}', '{self.image_file}')"

class Tests(db.Model):
    __tablename__ = 'tests'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    subject = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return f"Tests('{self.name}', '{self.subject}')"

class Grade(db.Model):
    __tablename__ = 'grade'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"Grade('{self.name}')"


class Subjects(db.Model):
    __tablename__= 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    