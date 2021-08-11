from flask_wtf import FlaskForm
from wtforms import SubmitField


class UpdateNewsForm(FlaskForm):
    submit = SubmitField('Newsを更新する')