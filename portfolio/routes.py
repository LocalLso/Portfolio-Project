from flask import Flask, render_template, flash, redirect, url_for, request, send_file, current_app
from io import BytesIO
from portfolio.models import User, FileUploads, FileUploadsG9, FileUploadsG10, FileUploadsG11, load_user
from portfolio.forms import RegistrationForm, LoginForm, UpdateAccountForm, UploadForm
from portfolio import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
from werkzeug.utils import secure_filename
from PIL import Image
from functools import wraps



def role_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return current_app.login_manager.unauthorized()
            user_role = current_user.role
            if ( (user_role != role)  and (role != "ANY")):
                return current_app.login_manager.unauthorized()
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/contactUs")
def contactUs():
    return render_template('contact_us.html', title='Contact Us')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if  form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, surname=form.surname.data, username=form.username.data,
                    email=form.email.data, password=hashed_password, role=form.role.data, active=False, image_file='default.png', grade=form.grade.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}', 'success!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    grades = ['Grade8', 'Grade9', 'Grade10', 'Grade11', 'AS']
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if  form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                for grade in grades:
                    if current_user.grade == grade:
                        return redirect(url_for('students', grade_no=current_user.grade))
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash(f'Login unsuccessful', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def  logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + f_ext
    picture_path =  os.path.join(app.root_path, 'static/profile_pics', picture_filename)
    
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_filename



@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been udated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route("/lgcse")
def lgcse():
    return render_template('lgcse.html', title='LGCSE', subject='mathematics')


@app.route("/grade8/<subject>", methods=['GET','POST'])
@role_required(role="TEACHER")
@login_required
def grade8(subject):
    form = UploadForm()
    if form.validate_on_submit():
        file = form.file.data
        subject = form.subject.data
        data = form.file.data
        file_uploaded = secure_filename(file.filename)
        f_ext = os.path.splitext(file.filename)[1]
        if file_uploaded != '':
            if f_ext not in app.config['ALLOWED_EXTENSIONS']:
                return redirect(url_for('grade8', subject="mathematics"))
            FileUpload = FileUploads(FileName=file_uploaded,  SubjectName=subject, Data=data.read(), user=current_user)
            db.session.add(FileUpload)
            db.session.commit()
            files8 = FileUploads.query.all()
            return render_template('maths8.html', title='G8-Maths', files8=files8, form=form, subject="mathematics")
    elif request.method == 'GET':
        files8 = FileUploads.query.all()
    return render_template('maths8.html', title='mathematics', form=form, files8=files8, subject="mathematics")


@app.route("/grade9/<subject>", methods=['GET','POST'])
@role_required(role="TEACHER")
@login_required
def grade9(subject):
    form = UploadForm()
    if form.validate_on_submit():
        file = form.file.data
        subject = form.subject.data
        data = form.file.data
        file_uploaded = secure_filename(file.filename)
        f_ext = os.path.splitext(file.filename)[1]
        if file_uploaded != '':
            if f_ext not in app.config['ALLOWED_EXTENSIONS']:
                return redirect(url_for('grade9', subject="mathematics"))
            FileUpload = FileUploadsG9(FileName=file_uploaded,  SubjectName=subject, Data=data.read(), user=current_user)
            db.session.add(FileUpload)
            db.session.commit()
            files9 = FileUploadsG9.query.all()
            return render_template('maths9.html', title='G9-Maths', files9=files9, form=form, subject="mathematics")
    elif request.method == 'GET':
        files9 = FileUploadsG9.query.all()
    return render_template('maths9.html', title='mathematics', form=form, subject="mathematics", files9=files9)


@app.route("/grade10/<subject>", methods=['GET','POST'])
@role_required(role="TEACHER")
@login_required
def grade10(subject):
    form = UploadForm()
    if form.validate_on_submit():
        file = form.file.data
        subject = form.subject.data
        data = form.file.data
        file_uploaded = secure_filename(file.filename)
        f_ext = os.path.splitext(file.filename)[1]
        if file_uploaded != '':
            if f_ext not in app.config['ALLOWED_EXTENSIONS']:
                return redirect(url_for('grade10', subject="mathematics"))
            FileUpload = FileUploadsG10(FileName=file_uploaded,  SubjectName=subject, Data=data.read(), user=current_user)
            db.session.add(FileUpload)
            db.session.commit()
            files10 = FileUploadsG10.query.all()
            return render_template('maths10.html', title='G10-Maths',files10=files10, form=form, subject="mathematics")
    elif request.method == 'GET':
        files10 = FileUploadsG10.query.all()
    return render_template('maths10.html', title='mathematics', form=form, subject="mathematics", files10=files10)


@app.route("/grade11/<subject>", methods=['GET','POST'])
@role_required(role="TEACHER")
@login_required
def grade11(subject):
    form = UploadForm()
    if form.validate_on_submit():
        file = form.file.data
        subject = form.subject.data
        data = form.file.data
        file_uploaded = secure_filename(file.filename)
        f_ext = os.path.splitext(file.filename)[1]
        if file_uploaded != '':
            if f_ext not in app.config['ALLOWED_EXTENSIONS']:
                return redirect(url_for('grade11', subject="mathematics"))
            FileUpload = FileUploadsG11(FileName=file_uploaded,  SubjectName=subject, Data=data.read(), user=current_user)
            db.session.add(FileUpload)
            db.session.commit()
            files11 = FileUploadsG11.query.all()
            return render_template('maths11.html', title='G11-Maths',files11=files11, form=form, subject="mathematics")
    elif request.method == 'GET':
        files11 = FileUploadsG11.query.all()
    return render_template('maths11.html', title='mathematics', form=form, subject="mathematics", files11=files11)

# for teachers - to be removed later
@app.route("/maths/<int:upload_id>/uploads")
def uploads(upload_id):
    file = FileUploads.query.get_or_404(upload_id)
    return send_file(BytesIO(file.Data), download_name=file.FileName, as_attachment=True)

@app.route("/maths/<int:upload_id>/uploads")
def uploads9(upload_id):
    file = FileUploadsG9.query.get_or_404(upload_id)
    return send_file(BytesIO(file.Data), download_name=file.FileName, as_attachment=True)

@app.route("/maths/<int:upload_id>/uploads")
def uploads10(upload_id):
    file = FileUploadsG10.query.get_or_404(upload_id)
    return send_file(BytesIO(file.Data), download_name=file.FileName, as_attachment=True)

@app.route("/maths/<int:upload_id>/uploads")
def uploads11(upload_id):
    file = FileUploadsG11.query.get_or_404(upload_id)
    return send_file(BytesIO(file.Data), download_name=file.FileName, as_attachment=True)

# For students
@app.route("/maths/<int:content8>/uploadsContent")
def uploadsContent(content8):
    file = FileUploads.query.get_or_404(content8)
    return send_file(BytesIO(file.Data), download_name=file.FileName, as_attachment=True)

@app.route("/maths/<int:content9>/uploadsContent")
def uploadsContent9(content9):
    file = FileUploadsG9.query.get_or_404(content9)
    return send_file(BytesIO(file.Data), download_name=file.FileName, as_attachment=True)

@app.route("/maths/<int:content10>/uploadsContent")
def uploadsContent10(content10):
    file = FileUploadsG10.query.get_or_404(content10)
    return send_file(BytesIO(file.Data), download_name=file.FileName, as_attachment=True)

@app.route("/maths/<int:content11>/uploadsContent")
def uploadsContent11(content11):
    file = FileUploadsG11.query.get_or_404(content11)
    return send_file(BytesIO(file.Data), download_name=file.FileName, as_attachment=True)


@app.route("/maths/<int:contentAS>/uploadsContent")
def uploadsContentAS(contentAS):
    file = FileUploadsG11.query.get_or_404(contentAS)
    return send_file(BytesIO(file.Data), download_name=file.FileName, as_attachment=True)



@app.route("/students/<grade_no>")
@role_required(role="STUDENT")
@login_required
def students(grade_no):
    if current_user.grade == 'Grade8':
        content8 = FileUploads.query.all()
        return render_template('student_content.html', title='G8-Maths', grade_no=current_user.grade, content8=content8, subject="mathematics")
    elif current_user.grade == 'Grade9':
        content9 = FileUploadsG9.query.all()
        return render_template('student_content9.html', title='G9-Maths', grade_no=current_user.grade, content9=content9, subject="mathematics")
    elif current_user.grade == 'Grade10':
        content10 = FileUploadsG10.query.all()
        return render_template('student_content10.html', title='G10-Maths', grade_no=current_user.grade, content10=content10, subject="mathematics")
    elif current_user.grade == 'Grade11':
        content11 = FileUploadsG11.query.all()
        return render_template('student_content11.html', title='G11-Maths', grade_no=current_user.grade, content11=content11, subject="mathematics")
    elif current_user.grade == 'AS':
        contentAS = FileUploadsAS.query.all()
        return render_template('student_contentAS.html', title='AS-Maths', grade_no=current_user.grade, contentAS=contentAS, subject="mathematics")
