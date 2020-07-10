from flask_wtf import FlaskForm
import wtforms


class LoginForm(FlaskForm):
    username = wtforms.StringField('Username', validators=[
        wtforms.validators.InputRequired(),
        wtforms.validators.Length(max=100)
    ])
    password = wtforms.PasswordField('Password', validators=[
        wtforms.validators.InputRequired(),
        wtforms.validators.Length(max=100)
    ])
    remember = wtforms.BooleanField('Remember me')

class AccountForm(FlaskForm):
    new_username = wtforms.StringField('New username', validators=[
        wtforms.validators.Optional(),
        wtforms.validators.Length(min=3, max=100),
        wtforms.validators.Regexp(r'[a-zA-Z0-9_]+', message='Can only contain letters, numbers, and underscores.')
    ])
    password = wtforms.PasswordField('Current password', validators=[
        wtforms.validators.InputRequired(),
        wtforms.validators.Length(max=100)
    ])
    new_password = wtforms.PasswordField('New password', validators=[
        wtforms.validators.Optional(),
        wtforms.validators.Length(min=6, max=100),
        wtforms.validators.EqualTo('confirm_password', message='Passwords must match.')
    ])
    confirm_password = wtforms.PasswordField('Confirm password', validators=[
        wtforms.validators.Optional()
    ])

class CreatePageForm(FlaskForm):
    path = wtforms.PasswordField('Confirm password', validators=[
        wtforms.validators.InputRequired()
    ])

class EditPageForm(FlaskForm):
    path = wtforms.PasswordField('Confirm password', validators=[
        wtforms.validators.InputRequired()
    ])
    content = wtforms.TextAreaField('Confirm password', validators=[])

class UploadFileForm(FlaskForm):
    path = wtforms.PasswordField('Confirm password', validators=[
        wtforms.validators.InputRequired()
    ])
    content = wtforms.TextAreaField('Confirm password', validators=[])
