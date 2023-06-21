from datetime import datetime
from portfolio import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Teachers.query.get(int(user_id))


class Teachers(db.Model, UserMixin):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    surname = db.Column(db.String(20), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    tests = db.relationship('Tests', backref='teacher', lazy=True)
    solution = db.relationship('Solutions', backref='teacher', lazy=True)
    notes = db.relationship('Notes', backref='teacher', lazy=True)
    assignments = db.relationship('Assignments', backref='teacher', lazy=True)
    uploads8 = db.relationship('FileUploads', backref='teacher', lazy=True)
    uploads9 = db.relationship('FileUploadsG9', backref='teacher', lazy=True)
    uploads10 = db.relationship('FileUploadsG10', backref='teacher', lazy=True)
    uploads11 = db.relationship('FileUploadsG11', backref='teacher', lazy=True)

    def __repr__(self):
        return f"Teachers('{self.username}', '{self.email}', '{self.image_file}')"


teacher_subjects = db.Table('teacher_subjects',
        db.Column('teachers_id', db.Integer, db.ForeignKey('teachers.id')),
        db.Column('subjects_id', db.Integer, db.ForeignKey('subjects.id'))
    )

class Students(db.Model, UserMixin):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    surname = db.Column(db.String(20), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    grade_id = db.Column(db.Integer(), db.ForeignKey('grade.id'), nullable=False)

    def __repr__(self):
        return f"Students('{self.username}', '{self.email}', '{self.image_file}')"


student_subjects = db.Table('student_subjects',
        db.Column('students_id', db.Integer, db.ForeignKey('students.id')),
        db.Column('subjects_id', db.Integer, db.ForeignKey('subjects.id'))
    )


class Subjects(db.Model):
    __tablename__= 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    SubjectName = db.Column(db.String(20), unique=True, nullable=False)
    tests = db.relationship('Tests', backref='subjects', lazy=True)
    solution = db.relationship('Solutions', backref='subjects', lazy=True)
    notes = db.relationship('Notes', backref='subjects', lazy=True)
    assignments = db.relationship('Assignments', backref='subjects', lazy=True)


    def __repr__(self):
        return f"Subjects('{self.SubjectName}')"


class Grade(db.Model):
    __tablename__= 'grade'
    id = db.Column(db.Integer, primary_key=True)
    GradeName = db.Column(db.String(20), unique=True, nullable=False)
    students = db.relationship('Students', backref='grade', lazy=True)

    def __repr__(self):
        return f"Grade('{self.GradeName}')"



class Tests(db.Model):
    __tablename__ = 'tests'
    id = db.Column(db.Integer, primary_key=True)
    TestName = db.Column(db.String(60), nullable=False)
    DateCreated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    teacher_id = db.Column(db.Integer(), db.ForeignKey('teachers.id'), nullable=False)
    subject_id = db.Column(db.Integer(), db.ForeignKey('subjects.id'), nullable=False)

    def __repr__(self):
        return f"Tests('{self.TestName}', '{self.DateCreated}')"

class Solutions(db.Model):
    __tablename__ = 'solutions'
    id = db.Column(db.Integer, primary_key=True)
    SolutionName = db.Column(db.String(60), nullable=False)
    DateCreated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    teacher_id = db.Column(db.Integer(), db.ForeignKey('teachers.id'), nullable=False)
    subject_id = db.Column(db.Integer(), db.ForeignKey('subjects.id'), nullable=False)

    def __repr__(self):
        return f"Solutions('{self.SolutionName}', '{self.DateCreated}')"


class Assignments(db.Model):
    __tablename__ = 'assignments'
    id = db.Column(db.Integer, primary_key=True)
    AssignmentName = db.Column(db.String(60), nullable=False)
    DateCreated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    teacher_id = db.Column(db.Integer(), db.ForeignKey('teachers.id'), nullable=False)
    subject_id = db.Column(db.Integer(), db.ForeignKey('subjects.id'), nullable=False)

    def __repr__(self):
        return f"Assignments('{self.AssignmentName}', '{self.DateCreated}')"


class Notes(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    NotesName = db.Column(db.String(60), nullable=False)
    DateCreated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    teacher_id = db.Column(db.Integer(), db.ForeignKey('teachers.id'), nullable=False)
    subject_id = db.Column(db.Integer(), db.ForeignKey('subjects.id'), nullable=False)

    def __repr__(self):
        return f"Notes('{self.NotesName}', '{self.DateCreated}')"

class FileUploads(db.Model):
    __tablename__ = 'fileuploads'
    id = db.Column(db.Integer, primary_key=True)
    FileName = db.Column(db.String(60), nullable=False)
    SubjectName = db.Column(db.String(60), nullable=False)
    DateCreated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    Data = db.Column(db.LargeBinary)
    teacher_id = db.Column(db.Integer(), db.ForeignKey('teachers.id'), nullable=False)

    def __repr__(self):
        return f"FileUploads('{self.FileName}', '{self.DateCreated}', '{self.teacher}')"

class FileUploadsG9(db.Model):
    __tablename__ = 'fileuploadsg9'
    id = db.Column(db.Integer, primary_key=True)
    FileName = db.Column(db.String(60), nullable=False)
    SubjectName = db.Column(db.String(60), nullable=False)
    DateCreated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    Data = db.Column(db.LargeBinary)
    teacher_id = db.Column(db.Integer(), db.ForeignKey('teachers.id'), nullable=False)

    def __repr__(self):
        return f"FileUploadsG9('{self.FileName}', '{self.DateCreated}', '{self.teacher}')"

class FileUploadsG10(db.Model):
    __tablename__ = 'fileuploadsg10'
    id = db.Column(db.Integer, primary_key=True)
    FileName = db.Column(db.String(60), nullable=False)
    SubjectName = db.Column(db.String(60), nullable=False)
    DateCreated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    Data = db.Column(db.LargeBinary)
    teacher_id = db.Column(db.Integer(), db.ForeignKey('teachers.id'), nullable=False)

    def __repr__(self):
        return f"FileUploadsG10('{self.FileName}', '{self.DateCreated}', '{self.teacher}')"

class FileUploadsG11(db.Model):
    __tablename__ = 'fileuploadsg11'
    id = db.Column(db.Integer, primary_key=True)
    FileName = db.Column(db.String(60), nullable=False)
    SubjectName = db.Column(db.String(60), nullable=False)
    DateCreated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    Data = db.Column(db.LargeBinary)
    teacher_id = db.Column(db.Integer(), db.ForeignKey('teachers.id'), nullable=False)

    def __repr__(self):
        return f"FileUploadsG11('{self.FileName}', '{self.DateCreated}', '{self.teacher}')"

class FileUploadsAS(db.Model):
    __tablename__ = 'fileuploadsas'
    id = db.Column(db.Integer, primary_key=True)
    FileName = db.Column(db.String(60), nullable=False)
    SubjectName = db.Column(db.String(60), nullable=False)
    DateCreated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    Data = db.Column(db.LargeBinary)
    teacher_id = db.Column(db.Integer(), db.ForeignKey('teachers.id'), nullable=False)

    def __repr__(self):
        return f"FileUploadsAS('{self.FileName}', '{self.DateCreated}', '{self.teacher}')"