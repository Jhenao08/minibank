import json

class Movimiento:
    def __init__(self, tipo, monto, destinatario):
        self.tipo = tipo  # Tipo de movimiento: "Débito" o "Crédito"
        self.monto = monto  # Monto de la transacción
        self.destinatario = destinatario  # Identificación del cliente destinatario (si aplica)


class Cliente:
    clientes = {}
    sesion_iniciada = False  # Bandera para indicar si el cliente ha iniciado sesión

    def __init__(self, identificacion, nombre, telefono, correo, direccion, contrasena):
        self.identificacion = identificacion
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo
        self.direccion = direccion
        self.cuentas = []
        self.movimientos = []  # Lista para almacenar los movimientos del cliente
        self.contrasena = contrasena
        Cliente.clientes[identificacion] = self

    def iniciar_sesion(self, contrasena):
        if self.contrasena == contrasena:
            self.sesion_iniciada = True
            print("Inicio de sesión exitoso.")
        else:
            print("Contraseña incorrecta.")

    def cerrar_sesion(self):
        self.sesion_iniciada = False
        print("Sesión cerrada.")

    def crear_cuenta(self, tipo_cuenta, saldo_inicial=0):
        cuenta = Cuenta(tipo_cuenta)
        cuenta.saldo = saldo_inicial  # Establecer el saldo inicial proporcionado
        self.cuentas.append(cuenta)
        print(f"Cuenta {tipo_cuenta} creada para {self.nombre} con un saldo inicial de {saldo_inicial}")

    def consultar_saldo(self, tipo_cuenta):
        if self.sesion_iniciada:
            for cuenta in self.cuentas:
                if cuenta.tipo == tipo_cuenta:
                    print(f"Saldo en cuenta {tipo_cuenta} de {self.nombre}: {cuenta.saldo}")
                    return cuenta.saldo
            print(f"No se encontró una cuenta {tipo_cuenta} para {self.nombre}.")
            crear_cuenta = input("¿Desea crear una cuenta? (s/n): ")
            if crear_cuenta.lower() == 's':
                saldo_inicial = float(input("Ingrese el saldo inicial de la cuenta: "))
                self.crear_cuenta(tipo_cuenta, saldo_inicial)
                return saldo_inicial  # Retorna el saldo inicial si se crea una nueva cuenta
            else:
                return None  # Si no se desea crear una nueva cuenta, retorna None
        else:
            print("Debe iniciar sesión para consultar saldo.")
            return None

    def realizar_transaccion(self, tipo_cuenta, monto, destinatario):
        if self.sesion_iniciada:
            saldo_disponible = self.consultar_saldo(tipo_cuenta)
            if saldo_disponible is None:
                print("No se puede realizar la transacción.")
                return
            if saldo_disponible >= monto:
                for cuenta in self.cuentas:
                    if cuenta.tipo == tipo_cuenta:
                        cuenta.saldo -= monto
                        self.movimientos.append(Movimiento("Débito", monto, destinatario))
                        print(f"Transacción exitosa. Nuevo saldo en cuenta {tipo_cuenta}: {cuenta.saldo}")
                        break
                else:
                    print(f"No se encontró una cuenta {tipo_cuenta} para {self.nombre}.")
            else:
                print("Saldo insuficiente para realizar la transacción.")
        else:
            print("Debe iniciar sesión para realizar una transacción.")

    @classmethod
    def guardar_datos(cls):
        with open('clientes.json', 'w') as archivo:
            datos = {
                'clientes': {
                    identificacion: {
                        'nombre': cliente.nombre,
                        'telefono': cliente.telefono,
                        'correo': cliente.correo,
                        'direccion': cliente.direccion,
                        'contrasena': cliente.contrasena,
                        'cuentas': [cuenta.__dict__ for cuenta in cliente.cuentas]
                    } for identificacion, cliente in cls.clientes.items()
                }
            }
            json.dump(datos, archivo)

    @classmethod
    def cargar_datos(cls):
        try:
            with open('clientes.json', 'r') as archivo:
                datos = json.load(archivo)
                for identificacion, info_cliente in datos['clientes'].items():
                    nuevo_cliente = cls(identificacion, info_cliente['nombre'], info_cliente['telefono'],
                                         info_cliente['correo'], info_cliente['direccion'], info_cliente['contrasena'])
                    for cuenta in info_cliente['cuentas']:
                        nueva_cuenta = Cuenta(cuenta['tipo'])
                        nueva_cuenta.saldo = cuenta['saldo']
                        nuevo_cliente.cuentas.append(nueva_cuenta)
        except FileNotFoundError:
            # Si el archivo no existe, no hay datos que cargar
            pass


class Cuenta:
    def __init__(self, tipo):
        self.tipo = tipo
        self.saldo = 0

    def consignar(self, monto):
        self.saldo += monto


def mostrar_menu():
    print("\nMenú:")
    print("1. Iniciar sesión")
    print("2. Cerrar sesión")
    print("3. Crear nuevo cliente")
    print("4. Modificar cliente existente")
    print("5. Consultar información de cliente")
    print("6. Consultar saldo de cuenta")
    print("7. Realizar transacción")
    print("8. Crear nueva cuenta")
    print("9. Salir")


# Mensaje de bienvenida al Banco JulianH
print("¡Bienvenido al Banco JulianH!")
print("-------------------------------")

# Cargar datos si existen
Cliente.cargar_datos()

# Ejemplo de uso
while True:
    mostrar_menu()
    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        identificacion = input("Ingrese la identificación del cliente: ")
        contrasena = input("Ingrese la contraseña: ")
        if identificacion in Cliente.clientes:
            Cliente.clientes[identificacion].iniciar_sesion(contrasena)
        else:
            print("El cliente no existe.")
    elif opcion == "2":
        identificacion = input("Ingrese la identificación del cliente: ")
        if identificacion in Cliente.clientes:
            Cliente.clientes[identificacion].cerrar_sesion()
        else:
            print("El cliente no existe.")
    elif opcion == "3":
        identificacion = input("Ingrese la identificación del nuevo cliente: ")
        nombre = input("Ingrese el nombre del nuevo cliente: ")
        telefono = input("Ingrese el teléfono del nuevo cliente: ")
        correo = input("Ingrese el correo del nuevo cliente: ")
        direccion = input("Ingrese la dirección del nuevo cliente: ")
        contrasena = input("Ingrese la contraseña del nuevo cliente: ")
        nuevo_cliente = Cliente(identificacion, nombre, telefono, correo, direccion, contrasena)
        saldo_inicial = float(input("Ingrese el saldo inicial de la cuenta: "))
        tipo_cuenta = input("Ingrese el tipo de cuenta a crear: ")
        nuevo_cliente.crear_cuenta(tipo_cuenta, saldo_inicial)
    elif opcion == "4":
        identificacion = input("Ingrese la identificación del cliente a modificar: ")
        nombre = input("Ingrese el nuevo nombre del cliente: ")
        telefono = input("Ingrese el nuevo teléfono del cliente: ")
        correo = input("Ingrese el nuevo correo del cliente: ")
        direccion = input("Ingrese la nueva dirección del cliente: ")
        contrasena = input("Ingrese la nueva contraseña del cliente: ")
        Cliente.clientes[identificacion].nombre = nombre
        Cliente.clientes[identificacion].telefono = telefono
        Cliente.clientes[identificacion].correo = correo
        Cliente.clientes[identificacion].direccion = direccion
        Cliente.clientes[identificacion].contrasena = contrasena
        print("Cliente modificado exitosamente.")
    elif opcion == "5":
        identificacion = input("Ingrese la identificación del cliente a consultar: ")
        if identificacion in Cliente.clientes:
            cliente = Cliente.clientes[identificacion]
            print(f"Información del cliente {cliente.nombre}:")
            print(f"Identificación: {cliente.identificacion}")
            print(f"Nombre: {cliente.nombre}")
            print(f"Teléfono: {cliente.telefono}")
            print(f"Correo: {cliente.correo}")
            print(f"Dirección: {cliente.direccion}")
        else:
            print("El cliente no existe.")
    elif opcion == "6":
        identificacion = input("Ingrese la identificación del cliente: ")
        tipo_cuenta = input("Ingrese el tipo de cuenta a consultar: ")
        if identificacion in Cliente.clientes:
            Cliente.clientes[identificacion].consultar_saldo(tipo_cuenta)
        else:
            print("El cliente no existe.")
    elif opcion == "7":
        identificacion = input("Ingrese la identificación del cliente emisor: ")
        tipo_cuenta = input("Ingrese el tipo de cuenta emisora para la transacción: ")
        monto = float(input("Ingrese el monto de la transacción: "))
        destinatario = input("Ingrese la identificación del cliente destinatario: ")
        if identificacion in Cliente.clientes and destinatario in Cliente.clientes:
            Cliente.clientes[identificacion].realizar_transaccion(tipo_cuenta, monto, destinatario)
        else:
            print("El cliente emisor o el destinatario no existen.")
    elif opcion == "8":
        identificacion = input("Ingrese la identificación del cliente: ")
        tipo_cuenta = input("Ingrese el tipo de cuenta a crear: ")
        saldo_inicial = float(input("Ingrese el saldo inicial de la cuenta: "))
        if identificacion in Cliente.clientes:
            Cliente.clientes[identificacion].crear_cuenta(tipo_cuenta, saldo_inicial)
        else:
            print("El cliente no existe.")
    elif opcion == "9":
        print("¡Gracias por utilizar el Banco JulianH!")
        break
    else:
        print("Opción no válida. Por favor, seleccione una opción válida.")
