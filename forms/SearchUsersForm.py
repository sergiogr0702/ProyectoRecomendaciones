from flask_wtf import FlaskForm, RecaptchaField
from wtforms import IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, NumberRange


class SearchUsersForm(FlaskForm):
    ocupation = SelectField('Ocupación',
                            choices=[('other', 'Otro'),
                                     ('academic/educator', 'Educador/académico'),
                                     ('artist', 'Artista'),
                                     ('clerical/admin', 'Clero'),
                                     ('college/grad student', 'Estudiante universitario'),
                                     ('customer service', 'Atencion al cliente'),
                                     ('doctor/health care', 'Doctor/enfermero'),
                                     ('executive/managerial', 'Ejecutivo'),
                                     ('farmer', 'Agricultor/ganadero'),
                                     ('homemaker', 'Ama de casa'),
                                     ('K-12 student', 'Estudiante K-12'),
                                     ('lawyer', 'Abogado'),
                                     ('programmer', 'Programador'),
                                     ('retired', 'Jubilado'),
                                     ('sales/marketing', 'Ventas/marketing'),
                                     ('scientist', 'Científico'),
                                     ('self-employed', 'Autónomo'),
                                     ('technician/engineer', 'Técnico/ingeniero'),
                                     ('tradesman/craftsman', 'Artesano/vendedor'),
                                     ('unemployed', 'Desempleado'),
                                     ('writer', 'Escritor')
                                     ],
                            render_kw={"class": "form-control"})

    gender = SelectField('Género',
                         choices=[('M', 'M'),
                                  ('F', 'F')],
                         render_kw={"class": "form-control"})

    age = IntegerField(
        'Edad',
        [
            DataRequired(),
            NumberRange(min=1, max=110)
        ],
        render_kw={"class": "form-control", "id": "floatingInput"}
    )

    number = IntegerField(
        'Número de usuarios',
        [
            DataRequired(),
            NumberRange(min=1, max=100)
        ],
        render_kw={"class": "form-control", "id": "floatingInput"}
    )

    recaptcha = RecaptchaField()
    submit = SubmitField('Buscar',
                         render_kw={"class": "btn btn-success mt-2"})
