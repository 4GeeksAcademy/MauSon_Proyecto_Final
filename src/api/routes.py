"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, Blueprint, send_file
from datetime import datetime
import qrcode
import json
import os
import qrcode
from api.models import MedioPagoTipo, db, User, Contact, SensitiveData, Reserva # Importar los modelos de la base de datos
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash #(Libreria que sirve para guardar una constraseña segura)
import qrcode
from io import BytesIO
import io
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

@api.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        print("Datos recibidos:", data)

        email = data.get('email')
        password = data.get('password')
        language = data.get('language')

        if not email or not password or not language:
            print("Datos incompletos")  
            return jsonify({"message": "Todos los campos son requeridos"}), 400

        if User.query.filter_by(email=email).first():
            print("Usuario ya existe")
            return jsonify({"message": "El usuario ya existe"}), 400

        hashed_password = generate_password_hash(password)
        print("Contraseña hasheada correctamente")

        new_user = User(
            email=email,
            password=hashed_password,
            language=language, 
            role=None,
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        print("Intentando guardar el usuario en la base de datos...")

        db.session.add(new_user)
        db.session.commit()
        print("Usuario guardado exitosamente")

        return jsonify({"message": "Usuario registrado exitosamente"}), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error en el endpoint /signup: {str(e)}")
        return jsonify({"message": "Error interno en el servidor", "error": str(e)}), 500

@api.route ('/login', methods=['POST'])
def handle_Login():
    # Verificar si los datos están presentes
    data = request.json
    if not data:
        return jsonify({"message": "Debe enviar datos en el cuerpo de la solicitud"}), 400

    # Obtener email y contraseña del cuerpo de la solicitud
    email = data.get('email')
    password = data.get('password')

    # Validar email y contraseña
    if not email or not password:
        return jsonify({"message": "El email y password son requeridos"}), 400

    # Buscar el usuario por email en la base de datos
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Usuario o contraseña incorrectos"}), 401

    # Crear un token de acceso utilizando el email del usuario
    token = create_access_token(identity=user.email)
    return(token)

@api.route('/user', methods=['GET'])
@api.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id=None):
    try:
        if user_id:
            # Obtener un usuario específico
            user = User.query.get(user_id)
            if not user:
                return jsonify({"message": "Usuario no encontrado"}), 404
            return jsonify(user.serialize()), 200
        else:
            # Obtener todos los usuarios
            users = User.query.all()
            return jsonify([user.serialize() for user in users]), 200
    except Exception as e:
        return jsonify({"message": "Error al obtener los usuarios", "error": str(e)}), 500
    
@api.route('/user', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        language = data.get('language')

        if not email or not password or not language:
            return jsonify({"message": "El email,password e idioma son requeridos"}), 400

        # Verificar si el usuario ya existe
        if User.query.filter_by(email=email).first():
            return jsonify({"message": "El usuario ya existe"}), 400

        # Hashear la contraseña
        hashed_password = generate_password_hash(password)

        # Crear nuevo usuario
        new_user = User(name=name, email=email, password=hashed_password, language=language ,is_active=True)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "Usuario creado exitosamente", "user": new_user.serialize()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error al crear el usuario", "error": str(e)}), 500


@api.route('/user/<int:user_id>', methods=['PUT'])
def modify_user(user_id):  # Nombre único para la función
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "Usuario no encontrado"}), 404

        data = request.get_json()
        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        user.language = data.get('language', user.language)
        user.is_active = data.get('is_active', user.is_active)

        db.session.commit()
        return jsonify({"message": "Usuario actualizado exitosamente", "user": user.serialize()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error al actualizar el usuario", "error": str(e)}), 500
    

@api.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        # Buscar el usuario en la base de datos por su ID
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({"message": "Usuario no encontrado"}), 404

        # Guardar el email del usuario antes de eliminarlo
        user_email = user.email

        # Eliminar el usuario de la base de datos
        db.session.delete(user)
        db.session.commit()

        # Devolver un mensaje con el email del usuario eliminado
        return jsonify({"message": f"Usuario con email '{user_email}' eliminado exitosamente"}), 200

    except Exception as e:
        # Manejar cualquier error inesperado
        db.session.rollback()
        return jsonify({"message": "Error al eliminar el usuario", "error": str(e)}), 500

@api.route('/backoffice')
@jwt_required()  # Asegura que el usuario esté autenticado
def backoffice():
    return jsonify({"message": "Acceso al Backoffice permitido."})

@api.route('/contact', methods=['GET'])
@jwt_required()
def get_contacts():
    try:
        # Obtener el email del usuario autenticado
        email = get_jwt_identity()  # Esto devolverá el email del usuario actual

        # Obtener el user_id basado en el email
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"message": "Usuario no encontrado"}), 404
        
        # Ahora, usa el user_id obtenido del usuario para filtrar los contactos
        user_id = user.id 
        print(f"Usuario autenticado con ID: {user_id}")  # Log para verificar

        # Filtrar contactos usando el user_id
        contacts = Contact.query.filter_by(user_id=user_id).all()
        
        if not contacts:
            print("No se encontraron contactos.")
            return jsonify({"message": "No hay contactos disponibles"}), 404
        
        return jsonify([contact.serialize() for contact in contacts]), 200
    except Exception as e:
        print(f"Error al obtener los contactos: {e}")
        return jsonify({"message": "Error al obtener los contactos", "error": str(e)}), 500

# FUNCION PARA CREAR UN CONTACTO
@api.route('/contact', methods=['POST'])
@jwt_required()
def create_contact():
    try:
        # Obtener usuario actual del token JWT
        email = get_jwt_identity()  # Obtener el email del usuario autenticado
        
        # Buscar el usuario en la base de datos usando el email
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"message": "Usuario no encontrado"}), 404
        
        # Obtener el ID del usuario autenticado
        current_user_id = user.id
        
        # Obtener los datos del nuevo contacto
        data = request.get_json()
        
        # Crear el nuevo contacto
        new_contact = Contact(
            nombre=data['nombre'],
            primer_apellido=data['primer_apellido'],
            segundo_apellido=data['segundo_apellido'],
            sexo=data['sexo'],
            nacionalidad=data['nacionalidad'],
            fecha_nacimiento=datetime.strptime(data['fecha_nacimiento'], '%Y-%m-%d').date(),
            direccion=data['direccion'],
            localidad=data['localidad'],
            pais=data['pais'],
            email=data['email'],
            telefono_movil=data['telefono_movil'],
            telefono_fijo=data['telefono_fijo'],
            user_id=current_user_id  # Aquí asignamos el ID del usuario autenticado
        )
        
        db.session.add(new_contact)
        db.session.commit()
        
        return jsonify({
            "message": "Contacto creado exitosamente",
            "contact": new_contact.serialize()
        }), 201
        
    except KeyError as e:
        return jsonify({
            "message": "Datos incompletos",
            "error": f"Falta el campo {str(e)}"
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "message": "Error al crear el contacto",
            "error": str(e)
        }), 500
    
#FUNCION PARA EDITAR LOS DATOS DE UN CONTACTO
@api.route('/contact/<int:contact_id>', methods=['PUT'])
@jwt_required()
def update_contact(contact_id):
    try:
        # Obtener el email del usuario autenticado
        email = get_jwt_identity()
        
        # Buscar al usuario en la base de datos usando el email
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"message": "Usuario no encontrado"}), 404
        
        # Obtener el contacto a actualizar
        contact = Contact.query.get(contact_id)
        if not contact:
            return jsonify({"message": "Contacto no encontrado"}), 404
        
        # Verificar que el contacto pertenece al usuario autenticado
        if contact.user_id != user.id:
            return jsonify({"message": "No tienes permiso para actualizar este contacto"}), 403
        
        # Obtener los datos a actualizar
        data = request.get_json()

        # Actualizar los campos del contacto
        contact.nombre = data.get('nombre', contact.nombre)
        contact.primer_apellido = data.get('primer_apellido', contact.primer_apellido)
        contact.segundo_apellido = data.get('segundo_apellido', contact.segundo_apellido)
        contact.sexo = data.get('sexo', contact.sexo)
        contact.nacionalidad = data.get('nacionalidad', contact.nacionalidad)
        contact.fecha_nacimiento = datetime.strptime(data['fecha_nacimiento'], '%Y-%m-%d').date() if 'fecha_nacimiento' in data else contact.fecha_nacimiento
        contact.direccion = data.get('direccion', contact.direccion)
        contact.localidad = data.get('localidad', contact.localidad)
        contact.pais = data.get('pais', contact.pais)
        contact.email = data.get('email', contact.email)
        contact.telefono_movil = data.get('telefono_movil', contact.telefono_movil)
        contact.telefono_fijo = data.get('telefono_fijo', contact.telefono_fijo)
        
        db.session.commit()
        
        return jsonify({
            "message": "Contacto actualizado exitosamente",
            "contact": contact.serialize()
        }), 200
        
    except KeyError as e:
        return jsonify({
            "message": "Datos incompletos",
            "error": f"Falta el campo {str(e)}"
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "message": "Error al actualizar el contacto",
            "error": str(e)
        }), 500

#FUNCION PARA ELIMINAR UN CONTACTO
@api.route('/contact/<int:contact_id>', methods=['DELETE'])
@jwt_required()
def delete_contact(contact_id):
    try:
        # Obtener el email del usuario autenticado
        email = get_jwt_identity()
        
        # Buscar al usuario en la base de datos usando el email
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"message": "Usuario no encontrado"}), 404
        
        # Obtener el contacto a eliminar
        contact = Contact.query.get(contact_id)
        if not contact:
            return jsonify({"message": "Contacto no encontrado"}), 404
        
        # Verificar que el contacto pertenece al usuario autenticado
        if contact.user_id != user.id:
            return jsonify({"message": "No tienes permiso para eliminar este contacto"}), 403
        
        # Eliminar el contacto
        db.session.delete(contact)
        db.session.commit()
        
        return jsonify({
            "message": f"Contacto con ID {contact_id} eliminado exitosamente"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "message": "Error al eliminar el contacto",
            "error": str(e)
        }), 500

# FUNCION PARA GUARDAR LOS DATOS SENSIBLES
@api.route('/sensitive-data', methods=['POST'])
@jwt_required()
def create_sensitive_data():
    try:
        data = request.get_json()
        
        # Verificar que el contacto existe y pertenece al usuario actual
        contact = Contact.query.filter_by(
            id=data['contact_id'],
            user_id=get_jwt_identity()
        ).first()
        
        if not contact:
            return jsonify({
                "message": "Contacto no encontrado o no autorizado"
            }), 404
        
        # Validar tipo de NIF
        try:
            nif_tipo = TipoNif[data['nif_tipo']]
        except KeyError:
            return jsonify({
                "message": "Tipo de NIF inválido",
                "valid_types": [tipo.name for tipo in TipoNif]
            }), 400
        
        new_sensitive_data = SensitiveData(
            nif_tipo=nif_tipo,
            nif_numero=data['nif_numero'],
            nif_country=data['nif_country'],
            contact_id=data['contact_id']
        )
        
        db.session.add(new_sensitive_data)
        db.session.commit()
        
        return jsonify({
            "message": "Datos sensibles guardados exitosamente",
            "sensitive_data": new_sensitive_data.serialize()
        }), 201
        
    except KeyError as e:
        return jsonify({
            "message": "Datos incompletos",
            "error": f"Falta el campo {str(e)}"
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "message": "Error al guardar los datos sensibles",
            "error": str(e)
        }), 500

# FUNCION PARA GUARDAR LOS DATOS RESERVA
@api.route('/reserva', methods=['POST'])
@jwt_required()
def create_reserva():
    try:
        data = request.get_json()
        # Verificar que el viajero existe y pertenece al usuario actual
        traveler = Contact.query.filter_by(
            id=data['traveler_id'],
            user_id=get_jwt_identity()
        ).first()

        if not traveler:
            return jsonify({"message": "Viajero no encontrado o no autorizado"}), 404

        # Validar tipo de medio de pago
        try:
            medio_pago = MedioPagoTipo[data['medio_pago_tipo']]
        except KeyError:
            return jsonify({
                "message": "Tipo de medio de pago inválido",
                "valid_types": [tipo.name for tipo in MedioPagoTipo]
            }), 400
        nueva_reserva = Reserva(
            fecha_entrada=datetime.strptime(data['fecha_entrada'], '%Y-%m-%d').date(),
            fecha_salida=datetime.strptime(data['fecha_salida'], '%Y-%m-%d').date(),
            alojamiento=data['alojamiento'],
            nro_rooms=data['nro_rooms'],
            nro_viajeros=data['nro_viajeros'],
            titular_medio_pago=data['titular_medio_pago'],
            medio_pago_tipo=medio_pago,
            medio_pago_nro=data.get('medio_pago_nro'),
            medio_pago_expira=datetime.strptime(data['medio_pago_expira'], '%Y-%m-%d').date() if data.get('medio_pago_expira') else None,
            fecha_pago=datetime.strptime(data['fecha_pago'], '%Y-%m-%d').date() if data.get('fecha_pago') else None,
            traveler_id=data['traveler_id']
        )

        db.session.add(nueva_reserva)
        db.session.commit()
        return jsonify({
            "message": "Reserva creada exitosamente",
            "reserva": nueva_reserva.serialize()
        }), 201
    except KeyError as e:
        return jsonify({
            "message": "Datos incompletos",
            "error": f"Falta el campo {str(e)}"
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "message": "Error al crear la reserva",
            "error": str(e)
        }), 500
    
@api.route('/user/contacts-qr', methods=['GET'])
@jwt_required()
def generate_user_contacts_qr():
    try:
        # Obtiene el user actual
        current_user_id = get_jwt_identity()
        
        # Fetch user's contacts (limit to 3)
        contacts = Contact.query.filter_by(user_id=current_user_id).limit(3).all()
        
        if not contacts:
            return jsonify({"message": "No hay contactos para generar QR"}), 404
        
        # Prepare contacts data
        contacts_data = []
        for contact in contacts:
            contact_info = contact.serialize()
            
            # Añade datos sensibles si los tiene
            sensitive_data = SensitiveData.query.filter_by(contact_id=contact.id).first()
            if sensitive_data:
                contact_info['sensitive_data'] = sensitive_data.serialize()
            
            contacts_data.append(contact_info)
        
        # Convertir a JSON
        qr_data = json.dumps(contacts_data)
        
        # Generar QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        # Crear imagen
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save to buffer
        img_buffer = BytesIO()
        img.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        
        return send_file(
            img_buffer,
            mimetype='image/png',
            as_attachment=True,
            download_name=f'user_{current_user_id}_contacts_qr.png'
        )
        
    except Exception as e:
        return jsonify({
            "message": "Error al generar el código QR de contactos",
            "error": str(e)
        }), 500

@api.route('/send-contact-qr', methods=['POST'])
@jwt_required()
def send_contact_qr():
    try:
        data = request.json
        contact_id = data.get('contact_id')
        recipient_email = data.get('email')

        contact = Contact.query.filter_by(
            id=contact_id, 
            user_id=get_jwt_identity()
        ).first()
        
        if not contact:
            return jsonify({"message": "Contacto no encontrado"}), 404

        # Generar QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        # Preparar datos del contacto
        contact_data = contact.serialize()
        sensitive_data = SensitiveData.query.filter_by(contact_id=contact_id).first()
        if sensitive_data:
            contact_data['sensitive_data'] = sensitive_data.serialize()
        
        qr.add_data(json.dumps(contact_data))
        qr.make(fit=True)

        # Crear imagen QR
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # Preparar correo
        msg = MIMEMultipart()
        msg['From'] = current_app.config['MAIL_DEFAULT_SENDER']
        msg['To'] = recipient_email
        msg['Subject'] = f'Código QR de Contacto {contact.nombre}'
        
        body = f"""
        Estimado/a {contact.nombre},
        
        Adjunto encontrarás el código QR con tu información de contacto.
        
        Saludos cordiales
        """
        msg.attach(MIMEText(body, 'plain'))
        
        # Guardar QR en buffer
        img_buffer = BytesIO()
        qr_img.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        
        # Adjuntar imagen
        image = MIMEImage(img_buffer.getvalue(), name=f'contacto_{contact_id}_qr.png')
        msg.attach(image)
        
        # Enviar correo
        with smtplib.SMTP(
            current_app.config['MAIL_SERVER'], 
            current_app.config['MAIL_PORT']
        ) as server:
            server.starttls()
            server.login(
                current_app.config['MAIL_USERNAME'], 
                current_app.config['MAIL_PASSWORD']
            )
            server.send_message(msg)
        
        return jsonify({"message": "QR enviado correctamente"}), 200

    except Exception as e:
        return jsonify({
            "message": "Error al enviar QR", 
            "error": str(e)
        }), 500