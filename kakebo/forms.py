from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, BooleanField, FloatField, HiddenField
from wtforms.fields.core import StringField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from datetime import date

def fecha_por_debajo_de_hoy(formulario, campo):
    hoy = date.today()
    if campo.data > hoy:
        raise ValidationError('La fecha {} no puede ser mayor que {}'.format(campo.data, hoy))

class MovimientosForm(FlaskForm):
    id = HiddenField()
    fecha = DateField("Fecha", validators = [DataRequired(message="Debe informar una fecha válida"),
            fecha_por_debajo_de_hoy])
    concepto = StringField("Concepto", validators = [DataRequired(), Length(min=10)])
    categoria = SelectField("Categoria", choices=[('SU', 'Supervivencia'), 
                ('OV', 'Ocio'),('CU', 'Cultura'), ('EX', 'Extras'), ("IN", "Ingreso")]) 
    cantidad = FloatField("Cantidad", validators = [DataRequired()])
    esGasto = BooleanField("Es gasto")

    submit = SubmitField('Aceptar')
