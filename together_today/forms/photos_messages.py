from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import Length, Optional, DataRequired


class AddForm(FlaskForm):
    photo = FileField("Photo", validators=[DataRequired()])
    message = StringField("Text Mssage", validators=[DataRequired(), Length(min=1, max=256)], render_kw={"placeholder": "Love Text <33"})

    submit = SubmitField("Save")

class EditForm(FlaskForm):
    photo = FileField("Photo", validators=[Optional()])
    message = StringField("Text Mssage", validators=[Optional(), Length(min=1, max=256)], render_kw={"placeholder": "Love Text <33"})

    submit = SubmitField("Save")