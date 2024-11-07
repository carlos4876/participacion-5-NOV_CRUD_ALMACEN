from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Función para inicializar la base de datos
def init_database():
    conn = sqlite3.connect("almacen.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS producto (
            id INTEGER PRIMARY KEY ,
            descripcion TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Inicializa la base de datos al inicio
init_database()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/producto")
def producto_index():
    conn = sqlite3.connect("almacen.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM producto")
    productos = cursor.fetchall()
    conn.close()
    return render_template("producto/index.html", productos=productos)

@app.route("/producto/create")
def producto_create():
    return render_template("producto/create.html")

@app.route("/producto/save", methods=["POST"])
def producto_save():
    descripcion = request.form["descripcion"]
    cantidad = request.form["cantidad"]
    precio = request.form["precio"]

    conn = sqlite3.connect("almacen.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO producto (descripcion, cantidad, precio) VALUES (?, ?, ?)", (descripcion, cantidad, precio))
    conn.commit()
    conn.close()
    return redirect(url_for("producto_index"))

@app.route("/producto/edit/<int:id>")
def producto_edit(id):
    conn = sqlite3.connect("almacen.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM producto WHERE id = ?", (id,))
    producto = cursor.fetchone()
    conn.close()
    return render_template("producto/edit.html", producto=producto)

@app.route("/producto/update", methods=["POST"])
def producto_update():
    id = request.form["id"]
    descripcion = request.form["descripcion"]
    cantidad = request.form["cantidad"]
    precio = request.form["precio"]

    conn = sqlite3.connect("almacen.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE producto SET descripcion = ?, cantidad = ?, precio = ? WHERE id = ?", (descripcion, cantidad, precio, id))
    conn.commit()
    conn.close()
    return redirect(url_for("producto_index"))

@app.route("/producto/delete/<int:id>")
def producto_delete(id):
    conn = sqlite3.connect("almacen.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM producto WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("producto_index"))

if __name__ == "__main__":
    app.run(debug=True)
