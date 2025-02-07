import React, { useState, useEffect, useContext } from "react";
import { Tab, Nav, Row, Button, Container } from "react-bootstrap";
import { useNavigate, useLocation } from "react-router-dom";
import { Context } from "../store/appContext";
import NavbarHeader from "../component/NavbarHeader.jsx";
import UserContactForm from "../component/FormPersonal.jsx";
import SensitiveDataForm from "../component/FormSensitive.jsx";
import ContactBanner from "../component/Banner.jsx";
import NavbarFooter from "../component/NavbarFooter.jsx";
import "../../styles/userForm.css";

const UserForm = () => {
  const { store, actions } = useContext(Context);
  const navigate = useNavigate();
  const location = useLocation();
  const [key, setKey] = useState("contact");

  const [formData, setFormData] = useState({
    nombre: "",
    primer_apellido: "",
    segundo_apellido: "",
    telefono_movil: "",
    telefono_fijo: "",
    email: "",
    sexo: "",
    fecha_nacimiento: "",
    nacionalidad: "",
    direccion: "",
    localidad: "",
    pais: ""
  });

  const [sensitiveFormData, setSensitiveFormData] = useState({
    nif_tipo: "",
    nif_numero: "",
    nif_country: ""
  });

  const [isEditing, setIsEditing] = useState(false);

  useEffect(() => {
    if (location.state?.contactToEdit) {
      setFormData(location.state.contactToEdit);
      setSensitiveFormData(location.state.sensitiveDataToEdit || {});
      setIsEditing(true);
    } else {
      setFormData({
        nombre: "",
        primer_apellido: "",
        segundo_apellido: "",
        telefono_movil: "",
        telefono_fijo: "",
        email: "",
        sexo: "",
        fecha_nacimiento: "",
        nacionalidad: "",
        direccion: "",
        localidad: "",
        pais: ""
      });
      setSensitiveFormData({
        nif_tipo: "",
        nif_numero: "",
        nif_country: ""
      });
      setIsEditing(false);
    }
  }, [location.state]);

  const handleSave = async () => {
    if (!store.user) {
      console.error("El usuario no está cargado correctamente.");
      return;
    }

    try {
      if (isEditing) {
        await actions.updateContact(formData.id, formData);
        if (sensitiveFormData) {
          await actions.updateSensitiveData(formData.id, sensitiveFormData);
        }
      } else {
        const newContact = await actions.createContact(formData);
        if (newContact && sensitiveFormData) {
          await actions.createSensitiveData(newContact.id, sensitiveFormData);
        }
      }
      navigate("/userinfo");
    } catch (error) {
      console.error("Error al guardar:", error);
    }
  };

  return (
    <div className="view-container">
      <Container fluid className="d-flex flex-column p-0 m-0 h-100">
        <Row className="view-header sticky-top g-0">
          <NavbarHeader prevLocation={location.state?.from} />
        </Row>

        <Row className="view-body m-0 p-0 
        g-0">
          <Row className="view-body-content m-0 p-0 g-0">
            <div className="user-form-tabs">
              <Tab.Container activeKey={key} onSelect={(k) => setKey(k)}>
                <Nav className="tabs-row">
                  <Nav.Item>
                    <Nav.Link eventKey="contact" className={key === 'contact' ? 'active-tab' : ''}>
                      Datos Personales
                    </Nav.Link>
                  </Nav.Item>
                  <Nav.Item>
                    <Nav.Link eventKey="sensitive" className={key === 'sensitive' ? 'active-tab' : ''}>
                      Datos Sensibles
                    </Nav.Link>
                  </Nav.Item>
                </Nav>

                <Tab.Content>
                  <Tab.Pane eventKey="contact">
                    <UserContactForm
                      contactData={formData}
                      setContactForm={setFormData}
                      isEditing={isEditing}
                    />
                    <div className="d-flex justify-content-center mt-3">
                      <Button onClick={() => setKey('sensitive')}>Siguiente</Button>
                    </div>
                  </Tab.Pane>
                  <Tab.Pane eventKey="sensitive">
                    <SensitiveDataForm
                      sensitiveData={sensitiveFormData}
                      setSensitiveData={setSensitiveFormData}
                    />
                    <div className="d-flex justify-content-center mt-3">
                      <Button
                        className={isEditing ? "update-button" : "create-button"}
                        onClick={handleSave}
                      >
                        {isEditing ? "Actualizar" : "Guardar"}
                      </Button>
                    </div>
                  </Tab.Pane>
                </Tab.Content>
              </Tab.Container>
            </div>
          </Row>

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

export default UserForm;