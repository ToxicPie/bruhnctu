from flask_wtf import FlaskForm
import wtforms


class LoginForm(FlaskForm):
    # def username_check(form, field):
    #     if len(field.data) > 100 or len(field.data) < 3:
    #         raise wtforms.validators.ValidationError('Username must be between 3 and 100 characters')
    #     if any(ord(c) >= 128 for c in field.data):
    #         raise wtforms.validators.ValidationError('Username cannot have non-ascii characters')
    #
    # def password_check(form, field):
    #     if len(field.data) > 100 or len(field.data) < 6:
    #         raise wtforms.validators.ValidationError('Password must be between 6 and 100 characters')
    #     if any(ord(c) >= 128 for c in field.data):
    #         raise wtforms.validators.ValidationError('Password cannot have non-ascii characters')

    username = wtforms.StringField('Username', validators=[
        wtforms.validators.InputRequired(),
        wtforms.validators.Length(max=100)
    ])
    password = wtforms.PasswordField('Password', validators=[
        wtforms.validators.InputRequired(),
        wtforms.validators.Length(max=100)
    ])
    remember = wtforms.BooleanField('Remember me')
