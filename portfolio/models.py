from datetime import datetime
from portfolio import db, login_manager
from flask_login import UserMixin



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# create table in database for storing users
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    active = db.Column(db.Boolean(), default=False)
    role = db.Column(db.String(80), nullable=False)
    grade = db.Column(db.String(80), nullable=False)
    uploads8 = db.relationship('FileUploads', backref='user', lazy=True)
    uploads9 = db.relationship('FileUploadsG9', backref='user', lazy=True)
    uploads10 = db.relationship('FileUploadsG10', backref='user', lazy=True)
    uploads11 = db.relationship('FileUploadsG11', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.name}', '{self.surname}', '{self.username}', '{self.email}', '{self.role}', '{self.grade}')"

    def __init__(self, name, surname, username, image_file, email, password, active, role, grade):
        self.name = name
        self.surname = surname
        self.username = username
        self.image_file = image_file
        self.email = email
        self.password = password
        self.active = active
        self.role = role
        self.grade = grade

    def get_role(self):
        return self.role


class FileUploads(db.Model):
    __tablename__ = 'fileuploads'
    id = db.Column(db.Integer, primary_key=True)
    FileName = db.Column(db.String(60), nullable=False)
    SubjectName = db.Column(db.String(60), nullable=False)
    DateCreated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    Data = db.Column(db.LargeBinary)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"FileUploads('{self.FileName}', '{self.DateCreated}', '{self.user}')"

class FileUploadsG9(db.Model):
    __tablename__ = 'fileuploadsg9'
    id = db.Column(db.Integer, primary_key=True)
    FileName = db.Column(db.String(60), nullable=False)
    SubjectName = db.Column(db.String(60), nullable=False)
    DateCreated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    Data = db.Column(db.LargeBinary)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"FileUploadsG9('{self.FileName}', '{self.DateCreated}', '{self.user}')"

class FileUploadsG10(db.Model):
    __tablename__ = 'fileuploadsg10'
    id = db.Column(db.Integer, primary_key=True)
    FileName = db.Column(db.String(60), nullable=False)
    SubjectName = db.Column(db.String(60), nullable=False)
    DateCreated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    Data = db.Column(db.LargeBinary)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"FileUploadsG10('{self.FileName}', '{self.DateCreated}', '{self.user}')"

class FileUploadsG11(db.Model):
    __tablename__ = 'fileuploadsg11'
    id = db.Column(db.Integer, primary_key=True)
    FileName = db.Column(db.String(60), nullable=False)
    SubjectName = db.Column(db.String(60), nullable=False)
    DateCreated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    Data = db.Column(db.LargeBinary)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"FileUploadsG11('{self.FileName}', '{self.DateCreated}', '{self.user}')"

class FileUploadsAS(db.Model):
    __tablename__ = 'fileuploadsas'
    id = db.Column(db.Integer, primary_key=True)
    FileName = db.Column(db.String(60), nullable=False)
    SubjectName = db.Column(db.String(60), nullable=False)
    DateCreated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    Data = db.Column(db.LargeBinary)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"FileUploadsAS('{self.FileName}', '{self.DateCreated}', '{self.user}')"
