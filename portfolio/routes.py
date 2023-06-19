from flask import Flask, render_template, flash, redirect, url_for, request, send_file
from io import BytesIO
from portfolio.models import Teachers, Students, Tests,FileUploads, Subjects
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
    return render_template('lgcse.html', title='LGCSE')

@app.route("/maths", methods=['GET','POST'])
@login_required
def maths():
    form = UploadForm()
    if form.validate_on_submit():
        file = form.file.data
        subject = form.subject.data
        data = form.file.data
        file_uploaded = secure_filename(file.filename)
        if file_uploaded != '':
            FileUpload = FileUploads(FileName=file_uploaded,  SubjectName=subject, Data=data.read(), teacher=current_user)
            db.session.add(FileUpload)
            db.session.commit()
            return redirect(url_for('maths'))
    files = FileUploads.query.all()
    return render_template('maths.html', title='mathematics', form=form, files=files)

@app.route("/maths/<int:upload_id>/uploads")
def uploads(upload_id):
    file = FileUploads.query.get_or_404(upload_id)
    return send_file(BytesIO(file.Data), download_name=file.FileName, as_attachment=True)

