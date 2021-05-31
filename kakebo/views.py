from kakebo import app
import sqlite3
from flask import jsonify, render_template, request, redirect, url_for, flash
from kakebo.forms import MovimientosForm
from datetime import date

def consultaSQL(query, parametros = []):
    #abrimos la conexion
    conexion = sqlite3.connect("movimientos.db")
    cur = conexion.cursor()

    #ejecutamos la consulta
    cur.execute(query, parametros)

    #Obtenemos los datos de la consulta
    claves = cur.description
    filas = cur.fetchall()

    #Procesar los datos para devolver una losta de diccionarios
    resultado=[]

    for fila in filas:
        d={}
        for clave, valor in zip(claves, fila):
            d[clave[0]] = valor
        resultado.append(d)

    conexion.close()
    return resultado

def modificaSQL(query, parametros = []):
    conexion=sqlite3.connect("movimientos.db")
    cur = conexion.cursor()

    cur.execute(query, parametros)

    conexion.commit()
    conexion.close()

@app.route('/')
def index():
    movimientos = consultaSQL("SELECT * FROM movimientos;")
    
    saldo = 0
    for d in movimientos:
        if d["esGasto"] == 0:
            saldo += d["cantidad"]
        else:
            saldo -= d["cantidad"]
        d["saldo"] = saldo

    return render_template("movimientos.html", datos = movimientos)

@app.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    formulario = MovimientosForm()

    if request.method == 'GET':
        return render_template('alta.html', form = formulario)

    else:
        if formulario.validate():
            query = "INSERT INTO movimientos (fecha, concepto, categoria, esGasto, cantidad) VALUES (?, ?, ?, ?, ?)"
            try:
                modificaSQL(query, [formulario.fecha.data, formulario.concepto.data, formulario.categoria.data, formulario.esGasto.data, formulario.cantidad.data])

            except sqlite3.Error as el_error:
                print("Error en SQL INSERT", el_error)
                flash("Se ha producido un error en la base de datos. Pruebe en unos minutos", "error")
                return render_template('alta.html', form=formulario)

            return redirect(url_for("index"))
            #Redirect a la ruta /
        else:
            return render_template('alta.html', form = formulario)

@app.route('/borrar/<int:id>', methods=['GET', 'POST'])
def borrar(id):
    if request.method == 'GET':
        filas = consultaSQL("SELECT * FROM movimientos WHERE id=?", [id])
        if len(filas) == 0:
            flash("El registro no existe", "error")
            return render_template('borrar.html', )
        
        return render_template('borrar.html', movimiento=filas[0])
    else:
        try:
            modificaSQL("DELETE FROM movimientos WHERE id = ?;", [id])
        except sqlite3.error as e:
            flash("Se ha producido un error de base de datos, vuelva a intentarlo", 'error')
            return redirect(url_for('index'))
            
        flash("Borrado realizado con éxito", 'aviso')    
        return redirect(url_for('index'))

@app.route('/modificar/<int:id>', methods=['GET', 'POST'])
def modificar(id):

    if request.method == 'GET':
        filas = consultaSQL("SELECT * FROM movimientos WHERE id=?", [id])
        if len(filas) == 0:
            flash("El registro no existe", "error")
            return render_template('modificar.html')
        registro = filas[0]
        registro["fecha"] = date.fromisoformat(registro["fecha"])
        
        formulario = MovimientosForm(data = registro)

        return render_template('modificar.html', form = formulario)
    else:
        formulario = MovimientosForm()

        if formulario.validate():
            query = "UPDATE movimientos SET(fecha, concepto, categoria, esGasto, cantidad) VALUES (?, ?, ?, ?, ?) WHERE id = ?"
            try:
                modificaSQL(query, [formulario.fecha.data, formulario.concepto.data, formulario.categoria.data, formulario.esGasto.data, formulario.cantidad.data, id])
            except sqlite3.Error as el_error:
                print("Error en SQL UPDATE", el_error)
                flash("Se ha producido un error en la base de datos. Pruebe en unos minutos", "error")
                return render_template('modificar.html', form=formulario)

            return redirect(url_for("index"))