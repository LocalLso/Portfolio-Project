from flask_wtf.file import FileField, FileAllowed
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import validators
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from portfolio.models import Teachers, Students, Tests

class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

	def validate_username(self, username):
		user = Teachers.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('Please chose a different username')


	def validate_email(self, email):
		user = Teachers.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Please chose a different email')

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remeber me')
	submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	picture = FileField('Update profile picture', validators=[FileAllowed(['png', 'jpg', 'jpeg'])])
	submit = SubmitField('Update')

	def validate_username(self, username):
		if username.data != current_user.username:
			user = Teachers.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('Please chose a different username')


	def validate_email(self, email):
		if email.data != current_user.email:
			user = Teachers.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('Please chose a different email')
