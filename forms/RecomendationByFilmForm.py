from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class RecomendationByFilmForm(FlaskForm):
    title = StringField(
        'Título',
        [
            DataRequired(),
            Length(min=4,
                   message='No se pueden buscar títulos tan cortos.')
        ],
        render_kw={"class": "form-control", "id": "floatingInput"}
    )

    recaptcha = RecaptchaField()
    submit = SubmitField('Buscar',
                         render_kw={"class": "btn btn-success"})
