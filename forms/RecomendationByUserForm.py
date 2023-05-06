from flask_wtf import FlaskForm, RecaptchaField
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class RecomendationByUserForm(FlaskForm):
    userId = IntegerField(
        'ID del usuario',
        [
            DataRequired(),
            NumberRange(min=0)
        ],
        render_kw={"class": "form-control", "id": "floatingInput"}
    )

    number = IntegerField(
        'Número de recomendaciones',
        [
            DataRequired(),
            NumberRange(min=1, max=100)
        ],
        render_kw={"class": "form-control", "id": "floatingInput"}
    )

    recaptcha = RecaptchaField()
    submit = SubmitField('Buscar',
                         render_kw={"class": "btn btn-success"})
