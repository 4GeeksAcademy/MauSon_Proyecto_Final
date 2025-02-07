import React, { useEffect, useContext } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Context } from "../store/appContext";
import { Container, Row, Col } from "react-bootstrap"; // Usamos react-bootstrap para el layout
import NavbarHeader from "../component/NavbarHeader.jsx";
import UserQrCard from "../component/UserQrCard.jsx";
import ContactBanner from "../component/Banner.jsx";
import NavbarFooter from "../component/NavbarFooter.jsx";
import "../../styles/qrView/qrhistory.css";

const QrHistory = () => {
  const { store, actions } = useContext(Context);
  const navigate = useNavigate();
  const location = useLocation();

  // Cargar los códigos QR si están vacíos
  useEffect(() => {
    console.log("Ejecutando useEffect para cargar QR codes...");
    console.log("user.id:", store.user?.id); 

    if (store.qr_codes.length === 0) {
      actions.loadQrCodes();
    }
  }, [store.qr_codes, actions]);

  // Función para ver más detalles del código QR
  const handleVerContacto = (id) => {
    navigate(`/qr-details/${id}`);
  };

  const handleDeleteQR = (id) => {
    console.log(`Borrar QR con ID: ${id}`);
    actions.deleteQrCode(id);
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const day = String(date.getDate()).padStart(2, "0");
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const year = String(date.getFullYear()).slice(2, 4); // Solo los dos últimos dígitos del año
    return `${day}/${month}/${year}`;
  };

  return (
    <div className="view-container">
      <Container fluid className="d-flex flex-column p-0 m-0 H-100">

        <Row className="view-header sticky-top g-0">
          <NavbarHeader prevLocation={location.state?.from} />
        </Row>

        <Row className="view-body g-0">
          {store.qr_codes && store.qr_codes.length > 0 ? (
            store.qr_codes.map((qrCode) => (
              <UserQrCard
                key={qrCode.id}
                id={qrCode.id}
                nombre={qrCode.nombre}
                fecha_inicio={qrCode.fecha_inicio}
                fecha_fin={qrCode.fecha_fin}
                verContacto={handleVerContacto}
                borrarQR={handleDeleteQR}
              />
            ))
          ) : (
            <p>No se encontraron códigos QR.</p>
          )}
        </Row>

        <Row className="view-banner m-0 g-0">
          <ContactBanner />
        </Row>

        <Row className="view-footer m-0 g-0">
          <NavbarFooter />
        </Row>
      </Container>
    </div>
  );
};

export default QrHistory;