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
        wtforms.validators.Regexp(r'^[a-zA-Z0-9_]+$', message='Field can only contain letters, numbers, and underscores.')
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
    path = wtforms.StringField('URL path', validators=[
        wtforms.validators.InputRequired()
    ])

class EditPageForm(FlaskForm):
    path = wtforms.StringField('URL path', validators=[
        wtforms.validators.InputRequired(),
        wtforms.validators.Length(min=3, max=30),
        wtforms.validators.Regexp(r'^[a-zA-Z0-9_/]+$', message='Field can only contain letters, numbers, forward slashes, and underscores.')
    ])
    content = wtforms.TextAreaField('File contents (markdown)', validators=[])
    save_file = wtforms.BooleanField('Check to save file; uncheck for view-only', validators=[])
