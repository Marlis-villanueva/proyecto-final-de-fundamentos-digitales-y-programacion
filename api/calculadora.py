import html
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs


# Catálogo oficial de Accesorios M Y S
productos = {
    "1": {"nombre": "Aretes Dorados", "precio": 50000},
    "2": {"nombre": "Cadena Dorada", "precio": 135000},
    "3": {"nombre": "Pulsera Dorada", "precio": 98000},
    "4": {"nombre": "Anillo Oro Laminado", "precio": 80000},
    "5": {"nombre": "Anillo Rodio Dorado", "precio": 45000},
    "6": {"nombre": "Arete Rodio Dorado", "precio": 48000},
    "7": {"nombre": "Cadena Rodio Dorado", "precio": 55000},
    "8": {"nombre": "Pulsera Rodio Dorado", "precio": 50000}
}


def formatear_moneda(valor):
    return f"$ {valor:,}".replace(",", ".")


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.enviar_respuesta(
            "<h1>Calculadora Accesorios M Y S</h1>"
            "<p>Selecciona un producto desde nuestra página para calcular tu pedido.</p>"
            '<a href="/">Volver a la tienda</a>'
        )

    def do_POST(self):

        try:
            longitud = int(self.headers.get("Content-Length", 0))
            datos = self.rfile.read(longitud).decode("utf-8")
            formulario = parse_qs(datos)

            opcion = formulario.get("producto", [""])[0]
            texto_cantidad = formulario.get("cantidad", [""])[0]

            # Validar el producto
            if opcion not in productos:
                raise ValueError("Selecciona un producto válido.")

            # Validar la cantidad
            if not texto_cantidad:
                raise ValueError("Ingresa la cantidad de productos.")

            cantidad = int(texto_cantidad)

            if cantidad < 1:
                raise ValueError("La cantidad debe ser mínimo 1.")

            # Buscar el producto
            producto_elegido = productos[opcion]

            nombre = producto_elegido["nombre"]
            precio = producto_elegido["precio"]

            # Calcular el total
            subtotal = precio * cantidad

            contenido = f"""
                <h1>¡Pedido calculado!</h1>

                <h2>Accesorios M Y S</h2>

                <p><strong>Producto seleccionado:</strong>
                {html.escape(nombre)}</p>

                <p><strong>Precio unitario:</strong>
                {formatear_moneda(precio)}</p>

                <p><strong>Cantidad:</strong>
                {cantidad}</p>

                <hr>

                <h2>Total a pagar:</h2>

                <h1>{formatear_moneda(subtotal)}</h1>

                <p>Gracias por elegir Accesorios M Y S.</p>

                <a href="/">Volver a la tienda</a>
            """

            self.enviar_respuesta(contenido)

        except (ValueError, TypeError):
            self.enviar_respuesta(
                """
                <h1>No se pudo calcular el pedido</h1>
                <p>Verifica el producto y la cantidad ingresada.</p>
                <a href="/">Volver a la tienda</a>
                """,
                estado=400
            )

    def enviar_respuesta(self, contenido, estado=200):

        pagina = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Resultado | Accesorios M Y S</title>

            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #FDF2E9;
                    color: #5D4037;
                    text-align: center;
                    padding: 30px 15px;
                }}

                .contenedor {{
                    background: white;
                    max-width: 500px;
                    margin: 40px auto;
                    padding: 30px;
                    border-radius: 20px;
                    box-shadow: 0 0 15px #F5CBA7;
                }}

                h1, h2 {{
                    color: #E26D5C;
                }}

                a {{
                    display: inline-block;
                    background: #F1948A;
                    color: white;
                    text-decoration: none;
                    padding: 12px 25px;
                    border-radius: 20px;
                    font-weight: bold;
                    margin-top: 20px;
                }}
            </style>
        </head>

        <body>
            <div class="contenedor">
                {contenido}
            </div>
        </body>
        </html>
        """

        respuesta = pagina.encode("utf-8")

        self.send_response(estado)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(respuesta)))
        self.end_headers()

        self.wfile.write(respuesta)