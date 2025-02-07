import React, { useEffect, useContext } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Context } from "../store/appContext";
import { Container, Row } from "react-bootstrap";
import NavbarHeader from "../component/NavbarHeader.jsx";
import ContactBody from "../component/ContactBody.jsx";
import ContactBanner from "../component/Banner.jsx";
import NavbarFooter from "../component/NavbarFooter.jsx";
import "../../styles/userView/userInfo.css";

const UserInfo = () => {
  const { store, actions } = useContext(Context);
  const navigate = useNavigate();
  const location = useLocation();

  // Cargar usuario, contactos y datos sensibles si aún no están cargados
  useEffect(() => {
    if (!store.user || !store.user.id) {
      actions.loadUser().then(() => {
        actions.loadContacts(); // Cargar los contactos
        actions.loadRandomImgs();  // Cargar imágenes aleatorias
      });
    } else {
      actions.loadContacts();
    }
  }, [store.user]);

  useEffect(() => {
    // Cargar los datos sensibles una vez los contactos estén cargados
    if (store.contact && store.contact.length > 0) {
      store.contact.forEach(contact => {
        actions.loadSensitiveData(contact.id); // Cargar datos sensibles para cada contacto
      });
    }
  }, [store.contact]);

  return (
    <div className="view-container">
      <Container fluid className="d-flex flex-column p-0 m-0 h-100">

        <Row className="view-header g-0">
          <NavbarHeader prevLocation={location.state?.from} />
        </Row>

        <Row className="view-body m-0 g-0">
          <ContactBody
            contactData={store.contact || []}
            sensitiveData={store.sensitive_data || []}
          />
        </Row>

        <Row className="view-banner m-0 g-0">
          <ContactBanner />
        </Row>

        <Row className="view-footer g-0">
          <NavbarFooter />
        </Row>
      </Container>
    </div>
  );
};

export default UserInfo;
