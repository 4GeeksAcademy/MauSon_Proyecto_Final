import React from "react";
import { IoHome, IoPerson, IoQrCode, IoTime } from "react-icons/io5";
import { useNavigate } from "react-router-dom";
import '../../styles/navbarFooter.css';

const NavbarFooter = () => {
  const navigate = useNavigate(); // Usamos el hook useNavigate para cambiar de ruta

  // Función para manejar la navegación
  const handleNavigation = (path) => {
    navigate(path); // Navega a la ruta especificada
  };

  return (
    <div className="navbar-footer">
      {/* Botón de inicio */}
      <button className="footer-icon" onClick={() => handleNavigation('/userhome')}>
        <IoHome size={24} />
      </button>

      {/* Botón de perfil */}
      <button className="footer-icon" onClick={() => handleNavigation('/userinfo')}>
        <IoPerson size={24} />
      </button>

      {/* Botón de historial de QR */}
      <button className="footer-icon" onClick={() => handleNavigation('/generate')}>
        <IoQrCode size={24} />
      </button>

      {/* Botón de creador de QR */}
      <button className="footer-icon" onClick={() => handleNavigation('/qrhistory')}>
        <IoTime size={24} />
      </button>
    </div>
  );
};

export default NavbarFooter;