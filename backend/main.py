from flask import Flask, jsonify, request, json

app = Flask(__name__)

# Datos de ejemplo (pueden ser datos de una base de datos)
productos = [
    {"id": 1, "nombre": "Producto 1", "precio": 10.99},
    {"id": 2, "nombre": "Producto 2", "precio": 20.49},
    {"id": 3, "nombre": "Producto 3", "precio": 5.99}
]

# Ruta al archivo JSON local
ruta_archivo_json = 'data_ECG.json'

# Función para cargar el contenido del archivo JSON en una variable
def cargar_datos_json(ruta_archivo):
    with open(ruta_archivo, 'r') as archivo:
        datos = json.load(archivo)
    return datos

# Llama a la función para cargar los datos JSON
datos_json = cargar_datos_json(ruta_archivo_json)

# Ruta para obtener todos los productos
@app.route('/productos', methods=['GET'])
def obtener_productos():
    return jsonify(datos_json)

# Ruta para obtener un producto por su ID
@app.route('/producto/<int:producto_id>', methods=['GET'])
def obtener_producto(producto_id):
    producto = next((p for p in productos if p['id'] == producto_id), None)
    if producto:
        return jsonify(producto)
    return jsonify({"mensaje": "Producto no encontrado"}), 404

# Ruta para agregar un nuevo producto
@app.route('/producto', methods=['POST'])
def agregar_producto():
    nuevo_producto = request.json
    productos.append(nuevo_producto)
    return jsonify({"mensaje": "Producto agregado correctamente"}), 201

# Ruta para actualizar un producto existente
@app.route('/producto/<int:producto_id>', methods=['PUT'])
def actualizar_producto(producto_id):
    producto = next((p for p in productos if p['id'] == producto_id), None)
    if not producto:
        return jsonify({"mensaje": "Producto no encontrado"}), 404
    datos_actualizados = request.json
    producto.update(datos_actualizados)
    return jsonify({"mensaje": "Producto actualizado correctamente"})

# Ruta para eliminar un producto existente
@app.route('/producto/<int:producto_id>', methods=['DELETE'])
def eliminar_producto(producto_id):
    global productos
    productos = [p for p in productos if p['id'] != producto_id]
    return jsonify({"mensaje": "Producto eliminado correctamente"})

if __name__ == '__main__':
    app.run(debug=True)
