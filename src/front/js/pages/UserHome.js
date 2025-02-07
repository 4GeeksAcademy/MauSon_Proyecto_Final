import React, { useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { Context } from "../store/appContext";
import { Container, Row } from "react-bootstrap";
import { FaShare, FaCopy } from "react-icons/fa";  // Usamos los nuevos iconos de react-icons
import NavbarHeader from "../component/NavbarHeader.jsx";
import ContactBanner from "../component/Banner.jsx";
import NavbarFooter from "../component/NavbarFooter.jsx";
import UserQrCard from "../component/UserQrCard.jsx"; // Se asume que este componente se encuentra en la misma carpeta
import pako from 'pako';
import { Html5QrcodeScanner, Html5Qrcode } from 'html5-qrcode';
import "../../styles/userHome.css";


const UserHome = () => {
  const { actions, store } = useContext(Context);
  const navigate = useNavigate();
  const [lastQr, setLastQr] = useState(null);
  useEffect(() => {
    const localToken = localStorage.getItem("authToken");


    if (!localToken || localToken === "null" || localToken === "undefined" || localToken.trim() === "") {
      console.log("Token inválido. Redirigiendo a Login...");
      navigate("/login", { replace: true });
    } else {
      fetchLastQr();
    }
  }, [navigate]);
  const fetchLastQr = async () => {
    try {
      const token = localStorage.getItem("authToken");
      const userId = 1; // Por ahora hardcodeado como antes
      const BACKEND_URL = process.env.BACKEND_URL;
      const response = await fetch(`${BACKEND_URL}api/user/${userId}/qrcodes`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (!response.ok) throw new Error('Error al obtener QRs');
      const data = await response.json();
      if (data.success && data.qr_codes.length > 0) {
        setLastQr(data.qr_codes[0]); // Tomamos el primer QR (el más reciente)
      }
    } catch (error) {
      console.log("Error al obtener el último QR");
    }
  };

  const handleNavigation = (path) => {
    navigate(path); // Navega a la ruta especificada
  };

  const handleLogOut = () => {
    console.log("Cerrando Sesión");
    localStorage.removeItem("authToken");
    actions.logout();
    navigate("/login", { replace: true });
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0'); // Los meses empiezan desde 0
    const year = date.getFullYear().toString().slice(2); // Obtener solo las dos últimas cifras del año
    return `${day}/${month}/${year}`;
  };

  const handleCopy = async () => {
    if (lastQr && lastQr.data) {
      try {
        const scannerDiv = document.createElement('div');
        scannerDiv.id = 'reader';
        scannerDiv.style.display = 'none';
        document.body.appendChild(scannerDiv);
        const html5QrCode = new Html5Qrcode("reader");
        const response = await fetch(lastQr.data);
        const blob = await response.blob();
        const file = new File([blob], "qr.png", { type: "image/png" });
        try {
          const decodedText = await html5QrCode.scanFile(file, true);
          const jsonData = JSON.parse(decodedText);
          await navigator.clipboard.writeText(JSON.stringify(jsonData, null, 2));
          alert("Contenido del QR copiado exitosamente");
        } finally {
          html5QrCode.clear();
          document.body.removeChild(scannerDiv);
        }
      } catch (error) {
        console.log("Error al procesar y copiar el QR:", error);
      }
    }
  };

  return (
    <div className="view-container">
      <Container fluid className="d-flex flex-column p-0 m-0 h-100">

        <Row className="view-header sticky-top g-0">
          <NavbarHeader />
        </Row>

        <Row className="view-body m-0 p-0 g-0">
          <div className="user-home-content">
            {lastQr && (
              <>
                <div className="qr-info-card">
                  <UserQrCard
                    id={lastQr.id}
                    nombre={lastQr.nombre}
                    fecha_inicio={formatDate(lastQr.fecha_inicio)}
                    fecha_fin={formatDate(lastQr.fecha_fin)}
                    data={lastQr.data}
                  />
                </div>
                <div className="qr-info-placeholder">
                  <img src={lastQr.data} alt="QR Code" />
                </div>
                <div className="qr-info-buttons">
                  <button className="share-button" onClick={() => handleNavigation('/share')}>
                    <FaShare />
                  </button>
                  <button className="copy-button" onClick={handleCopy}>
                    <FaCopy />
                  </button>
                </div>
              </>
            )}
          </div>
        </Row>

        <Row className="view-banner m-0 p-0 g-0">
          <ContactBanner />
        </Row>

        <Row className="view-footer m-0 p-0 g-0">
          <NavbarFooter />
        </Row>

      </Container>
    </div>
  );
};
export default UserHome;