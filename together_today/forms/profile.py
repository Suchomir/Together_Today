from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, FileField
from wtforms.validators import Email, Length, EqualTo, Optional


class EditForm(FlaskForm):
    first_name = StringField("First Name", validators=[Optional()])
    last_name = StringField("Last Name", validators=[Optional()])
    username = StringField("Username", validators=[Optional()])
    picture = FileField("Picture", validators=[Optional()])

    new_password = PasswordField(
        "New Password", validators=[Optional(), Length(min=8, max=64)]
    )
    confirm_password = PasswordField(
        "Confirm New Password",
        validators=[Optional(), Length(min=8, max=64), EqualTo("new_password")],
    )

    submit = SubmitField("Save")
