import React from "react";
import { Row, Col } from "react-bootstrap";
import { FaTrashAlt } from "react-icons/fa"; // Icono de borrar
import { BsQrCodeScan } from "react-icons/bs";

import "../../styles/qrView/qrcard.css"; // Usamos los estilos desde el archivo CSS

const UserQrCard = ({ id, nombre, fecha_inicio, fecha_fin, verContacto, borrarQR }) => {
  const formatDate = (date) => {
    // Formateamos la fecha en el formato dd/mm/yyyy
    const options = { day: '2-digit', month: '2-digit', year: '2-digit' };
    return new Date(date).toLocaleDateString('es-ES', options);
  };

  return (
    <div className="qr-card-container">
      <Row noGutters className="qr-card-content m-0">
        {/* Columna 1: Imagen QR */}
        <Col xs="auto" className="qr-img-col">
          <div className="qr-img">
            <BsQrCodeScan />
          </div>
        </Col>

        {/* Columna 2: Información de QR */}
        <Col xs className="qr-data-col">
          <div className="qr-data">
            <p className="nombre">{nombre}</p>
            <p className="fechas">{`Del ${formatDate(fecha_inicio)} al ${formatDate(fecha_fin)}`}</p>
            <a href="#" onClick={() => verContacto(id)} className="show-qr-link">Show QR...</a>
          </div>
        </Col>

        {/* Columna 3: Icono de Borrar */}
        <Col xs="auto" className="qr-dele-col">
          <div className="qr-dele">
            <button className="delete-button" onClick={() => borrarQR(id)}>
              <FaTrashAlt />
            </button>
          </div>
        </Col>
      </Row>
    </div>
  );
};

export default UserQrCard;