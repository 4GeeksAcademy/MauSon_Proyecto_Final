from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    
    # Relaciones
    # datos_viajero = db.relationship('DatosViajero', backref='user', lazy=True)
    # qr_codes = db.relationship('QRDatabase', backref='user', lazy=True)
    # transacciones = db.relationship('Transaccion', backref='user', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }

class DatosViajero(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    primer_apellido = db.Column(db.String(100), nullable=False)
    segundo_apellido = db.Column(db.String(100), nullable=False)
    sexo = db.Column(db.String(10), nullable=False)
    nif = db.Column(db.String(20), nullable=False, unique=True, index=True)
    numero_soporte_documento = db.Column(db.String(20), nullable=False)
    tipo_documento = db.Column(db.String(20), nullable=False)
    nacionalidad = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    localidad = db.Column(db.String(100), nullable=False)
    pais = db.Column(db.String(100), nullable=False)
    telefono_fijo = db.Column(db.String(20), nullable=True)
    telefono_movil = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    numero_viajeros = db.Column(db.Integer, nullable=False)
    parentesco_viajeros = db.Column(db.String(100), nullable=False)
    
    # Relaciones
    transacciones = db.relationship('Transaccion', backref='viajero', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "nombre": self.nombre,
            "primer_apellido": self.primer_apellido,
            "segundo_apellido": self.segundo_apellido,
            "sexo": self.sexo,
            "nif": self.nif,
            "numero_soporte_documento": self.numero_soporte_documento,
            "tipo_documento": self.tipo_documento,
            "nacionalidad": self.nacionalidad,
            "fecha_nacimiento": self.fecha_nacimiento,
            "direccion": self.direccion,
            "localidad": self.localidad,
            "pais": self.pais,
            "telefono_fijo": self.telefono_fijo,
            "telefono_movil": self.telefono_movil,
            "email": self.email,
            "numero_viajeros": self.numero_viajeros,
            "parentesco_viajeros": self.parentesco_viajeros
        }
    
class Transaccion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    viajero_id = db.Column(db.Integer, db.ForeignKey('datos_viajero.id'), nullable=False)
    referencia = db.Column(db.String(100), nullable=False, index=True)
    fecha_transaccion = db.Column(db.Date, nullable=False)
    firmas = db.Column(db.String(100), nullable=False)
    fecha_hora_entrada = db.Column(db.DateTime, nullable=False)
    fecha_hora_salida = db.Column(db.DateTime, nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    numero_habitaciones = db.Column(db.Integer, nullable=False)
    conexion_internet = db.Column(db.Boolean(), nullable=False)
    tipo = db.Column(db.String(100), nullable=False)
    identificacion_medio_pago = db.Column(db.String(100), nullable=False)
    titular_medio_pago = db.Column(db.String(100), nullable=False)
    fecha_caducidad_tarjeta = db.Column(db.Date, nullable=False)
    fecha_pago = db.Column(db.Date, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "viajero_id": self.viajero_id,
            "referencia": self.referencia,
            "fecha_transaccion": self.fecha_transaccion,
            "firmas": self.firmas,
            "fecha_hora_entrada": self.fecha_hora_entrada,
            "fecha_hora_salida": self.fecha_hora_salida,
            "direccion": self.direccion,
            "numero_habitaciones": self.numero_habitaciones,
            "conexion_internet": self.conexion_internet,
            "tipo": self.tipo,
            "identificacion_medio_pago": self.identificacion_medio_pago,
            "titular_medio_pago": self.titular_medio_pago,
            "fecha_caducidad_tarjeta": self.fecha_caducidad_tarjeta,
            "fecha_pago": self.fecha_pago
        }
    
class QRDatabase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    archivo = db.Column(db.String(200), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "archivo": self.archivo
        }
        
# class Empresa(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     razon_social = db.Column(db.String(60), nullable=False)
#     cif = db.Column(db.String(20), nullable=False, unique=True, index=True)
#     nombre_comercial = db.Column(db.String(60), nullable=False)
#     domicilio = db.Column(db.String(200), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

#     def serialize(self):
#         return {
#             "id": self.id,
#             "razon_social": self.razon_social,
#             "cif": self.cif,
#             "nombre_comercial": self.nombre_comercial,
#             "domicilio": self.domicilio,
#             "user_id": self.user_id,
#         }

# class DatosEmpresa(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     empresa_id = db.Column(db.Integer, db.ForeignKey('empresa.id'), nullable=False)
#     razon_social = db.Column(db.String(200), nullable=False)
#     cif = db.Column(db.String(20), nullable=False)
#     municipio = db.Column(db.String(100), nullable=False)
#     provincia = db.Column(db.String(100), nullable=False)
#     telefono = db.Column(db.String(20), nullable=False)
#     email = db.Column(db.String(120), nullable=False)
#     web = db.Column(db.String(200), nullable=False)
#     url_anuncio = db.Column(db.String(200), nullable=False)

#     def serialize(self):
#         return {
#             "id": self.id,
#             "razon_social": self.razon_social,
#             "cif": self.cif,
#             "municipio": self.municipio,
#             "provincia": self.provincia,
#             "telefono": self.telefono,
#             "email": self.email,
#             "web": self.web,
#             "url_anuncio": self.url_anuncio
#         }

# class DatosEstablecimiento(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     establecimiento_id = db.Column(db.Integer, db.ForeignKey('establecimiento.id'), nullable=False)
#     tipo_establecimiento = db.Column(db.String(20), nullable=False)
#     denominacion = db.Column(db.String(200), nullable=False)
#     direccion = db.Column(db.String(200), nullable=False)
#     cod_postal = db.Column(db.String(200), nullable=False)
#     localidad_y_provincia = db.Column(db.Integer, nullable=False)

#     def serialize(self):
#         return {
#             "id": self.id,
#             "tipo_establecimiento": self.tipo_establecimiento,
#             "denominacion": self.denominacion,
#             "direccion": self.direccion,
#             "cod_postal": self.cod_postal,
#             "localidad_y_provincia": self.localidad_y_provincia
#         }


# class Reservas(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     numero_res = db.Column(db.Integer, nullable=False, index=True)
#     fecha_res = db.Column(db.Date, nullable=False)
#     fecha_ini = db.Column(db.Date, nullable=False)
#     fecha_fin = db.Column(db.Date, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     alojamiento_id = db.Column(db.Integer, db.ForeignKey('alojamientos.id'), nullable=False)
#     medio_pago_id = db.Column(db.Integer, db.ForeignKey('medios_pago.id'), nullable=False)
#     transaccion_id = db.Column(db.Integer, db.ForeignKey('transaccion.id'), nullable=False)  

#     alojamiento = db.relationship('Alojamientos', backref=db.backref('reservas', lazy=True))
#     medio_pago = db.relationship('MediosPago', backref=db.backref('reservas', lazy=True))
#     transaccion = db.relationship('Transaccion', backref=db.backref('reservas', lazy=True))  

#     def serialize(self):
#         return {
#             "id": self.id,
#             "numero_res": self.numero_res,
#             "fecha_res": self.fecha_res,
#             "fecha_ini": self.fecha_ini,
#             "fecha_fin": self.fecha_fin,
#             "user": self.user.serialize() if self.user else None,
#             "alojamiento": self.alojamiento.serialize() if self.alojamiento else None,
#             "medio_pago": self.medio_pago.serialize() if self.medio_pago else None,
#             "transaccion": self.transaccion.serialize() if self.transaccion else None
#         }
