from flask_wtf import FlaskForm, RecaptchaField
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

from wtforms import SelectMultipleField, widgets
from markupsafe import Markup


class BootstrapListWidget(widgets.ListWidget):

    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        html = [f"<{self.html_tag} {widgets.html_params(**kwargs)}>"]
        for subfield in field:
            if self.prefix_label:
                html.append(
                    f"<li class='list-group-item pl-5'>{subfield.label} {subfield(class_='form-check-input ms-1')}</li>")
            else:
                html.append(
                    f"<li class='list-group-item pl-5'>{subfield(class_='form-check-input me-1')} {subfield.label}</li>")
        html.append("</%s>" % self.html_tag)
        return Markup("".join(html))


class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = BootstrapListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class SearchMoviesForm(FlaskForm):
    categories = MultiCheckboxField('Categorías',
                                    choices=[('Action', 'Acción'),
                                             ('Adventure', 'Aventura'),
                                             ('Animation', 'Animación'),
                                             ('Comedy', 'Comedia'),
                                             ('Crime', 'Crimen'),
                                             ('Documentary', 'Documental'),
                                             ('Drama', 'Drama'),
                                             ('Fantasy', 'Fantasía'),
                                             ('Horror', 'Horror'),
                                             ('Musical', 'Musical'),
                                             ('Mystery', 'Misterio'),
                                             ('Romance', 'Romance'),
                                             ('Thriller', 'Thriller'),
                                             ('War', 'Bélico'),
                                             ('Western', 'Western')]
                                    )

    number = IntegerField(
        'Número de películas',
        [
            DataRequired(),
            NumberRange(min=1, max=100)
        ],
        render_kw={"class": "form-control", "id": "floatingInput"}
    )

    recaptcha = RecaptchaField()
    submit = SubmitField('Buscar',
                         render_kw={"class": "btn btn-success mt-2"})
