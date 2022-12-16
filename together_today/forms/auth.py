from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    HiddenField,
    FileField,
)
from wtforms.validators import DataRequired, Length, EqualTo, Optional


class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    picture = FileField("Picture (Optional)", validators=[Optional()])

    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=8, max=64)]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), Length(min=8, max=64), EqualTo("password")],
    )

    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    next = HiddenField("Next", validators=[Optional()])
    submit = SubmitField("Log In")
