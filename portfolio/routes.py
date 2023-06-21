from flask import Flask, render_template, flash, redirect, url_for, request, send_file
from io import BytesIO
from portfolio.models import Teachers, Students, Tests, FileUploads, FileUploadsG9, FileUploadsG10, FileUploadsG11, Subjects
from portfolio.forms import RegistrationForm, LoginForm, UpdateAccountForm, UploadForm
from portfolio import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
from werkzeug.utils import secure_filename
from PIL import Image

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if  form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Teachers(name=form.name.data, surname=form.surname.data, username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}', 'success!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if  form.validate_on_submit():
            user = Teachers.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
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
            FileUpload = FileUploads(FileName=file_uploaded,  SubjectName=subject, Data=data.read(), teacher=current_user)
            db.session.add(FileUpload)
            db.session.commit()
            files8 = FileUploads.query.all()
            return render_template('maths8.html', title='G8-Maths', files8=files8, form=form, subject="mathematics")
    elif request.method == 'GET':
        files8 = FileUploads.query.all()
    return render_template('maths8.html', title='mathematics', form=form, files8=files8, subject="mathematics")


@app.route("/grade9/<subject>", methods=['GET','POST'])
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
            FileUpload = FileUploadsG9(FileName=file_uploaded,  SubjectName=subject, Data=data.read(), teacher=current_user)
            db.session.add(FileUpload)
            db.session.commit()
            files9 = FileUploadsG9.query.all()
            return render_template('maths9.html', title='G9-Maths', files9=files9, form=form, subject="mathematics")
    elif request.method == 'GET':
        files9 = FileUploadsG9.query.all()
    return render_template('maths9.html', title='mathematics', form=form, subject="mathematics", files9=files9)


@app.route("/grade10/<subject>", methods=['GET','POST'])
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
            FileUpload = FileUploadsG10(FileName=file_uploaded,  SubjectName=subject, Data=data.read(), teacher=current_user)
            db.session.add(FileUpload)
            db.session.commit()
            files10 = FileUploadsG10.query.all()
            return render_template('maths10.html', title='G10-Maths',files10=files10, form=form, subject="mathematics")
    elif request.method == 'GET':
        files10 = FileUploadsG10.query.all()
    return render_template('maths10.html', title='mathematics', form=form, subject="mathematics", files10=files10)


@app.route("/grade11/<subject>", methods=['GET','POST'])
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
            FileUpload = FileUploadsG11(FileName=file_uploaded,  SubjectName=subject, Data=data.read(), teacher=current_user)
            db.session.add(FileUpload)
            db.session.commit()
            files11 = FileUploadsG11.query.all()
            return render_template('maths11.html', title='G11-Maths',files11=files11, form=form, subject="mathematics")
    elif request.method == 'GET':
        files11 = FileUploadsG11.query.all()
    return render_template('maths11.html', title='mathematics', form=form, subject="mathematics", files11=files11)


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
