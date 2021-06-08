from flask_wtf import FlaskForm
from wtforms import DateField, StringField, SelectField, SubmitField, FloatField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError
from datetime import date

def fecha_por_debajo_de_hoy(formulario, campo):
    hoy = date.today()
    if campo.data > hoy:
        raise ValidationError('La fecha {} no puede ser mayor que {}'.format(campo.data, hoy))

class MovimientosForm(FlaskForm):
    id = HiddenField()
    fecha = DateField("Fecha", validators = [DataRequired(message="Debe informar una fecha válida"), fecha_por_debajo_de_hoy])
    concepto = StringField("Concepto", validators = [DataRequired(), Length(min=10)])
    categoria = SelectField("Categoria", choices=[('00', ''),('SU', 'Supervivencia'), ('OV', 'Ocio/Vicio'), 
                            ('CU', 'Cultura'), ('EX', 'Extras')])
    cantidad = FloatField("Cantidad", validators = [DataRequired(message="Campo requerido")])
    esGasto = BooleanField("Es gasto")
    submit = SubmitField('Aceptar')

class FiltraMovimientosForm(FlaskForm):
    fechaDesde = DateField("Desde", validators=[fecha_por_debajo_de_hoy], default=date(date.today().year, 1, 1))
    fechaHasta = DateField("Hasta", validators=[fecha_por_debajo_de_hoy], default=date.today())
    texto = StringField("Concepto")
    submit = SubmitField("Filtrar")

