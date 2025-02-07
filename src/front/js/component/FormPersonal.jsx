import React from "react";
import { Form, Row, Col } from "react-bootstrap";
import "../../styles/userView/formPersonal.css";

const UserContactForm = ({ contactData, setContactForm, isEditing }) => {
  const handleChange = (e) => {
    const { name, value } = e.target;
    setContactForm((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  return (
    <div className="user-contact-form-container">
      <Form>
        {/* Nombre */}
        <Row className="mb-3">
          <Col sm={12}>
            <Form.Group controlId="nombre">
              <Form.Label>Nombre</Form.Label>
              <Form.Control
                type="text"
                name="nombre"
                value={contactData.nombre || ""}
                onChange={handleChange}
                required
              />
            </Form.Group>
          </Col>
        </Row>

        {/* Primer y Segundo Apellido */}
        <Row className="mb-3">
          <Col sm={6}>
            <Form.Group controlId="primer_apellido">
              <Form.Label>Primer Apellido</Form.Label>
              <Form.Control
                type="text"
                name="primer_apellido"
                value={contactData.primer_apellido || ""}
                onChange={handleChange}
                required
              />
            </Form.Group>
          </Col>
          <Col sm={6}>
            <Form.Group controlId="segundo_apellido">
              <Form.Label>Segundo Apellido</Form.Label>
              <Form.Control
                type="text"
                name="segundo_apellido"
                value={contactData.segundo_apellido || ""}
                onChange={handleChange}
              />
            </Form.Group>
          </Col>
        </Row>

        {/* Teléfonos */}
        <Row className="mb-3">
          <Col sm={6}>
            <Form.Group controlId="telefono_movil">
              <Form.Label>Teléfono Móvil</Form.Label>
              <Form.Control
                type="text"
                name="telefono_movil"
                value={contactData.telefono_movil || ""}
                onChange={handleChange}
                required
              />
            </Form.Group>
          </Col>
          <Col sm={6}>
            <Form.Group controlId="telefono_fijo">
              <Form.Label>Teléfono Fijo</Form.Label>
              <Form.Control
                type="text"
                name="telefono_fijo"
                value={contactData.telefono_fijo || ""}
                onChange={handleChange}
              />
            </Form.Group>
          </Col>
        </Row>

        {/* Email y Sexo */}
        <Row className="mb-3">
          <Col sm={6}>
            <Form.Group controlId="email">
              <Form.Label>Email</Form.Label>
              <Form.Control
                type="email"
                name="email"
                value={contactData.email || ""}
                onChange={handleChange}
                required
              />
            </Form.Group>
          </Col>
          <Col sm={6}>
            <Form.Group controlId="sexo">
              <Form.Label>Sexo</Form.Label>
              <Form.Control
                type="text"
                name="sexo"
                value={contactData.sexo || ""}
                onChange={handleChange}
                required
              />
            </Form.Group>
          </Col>
        </Row>

        {/* Fecha de Nacimiento y Nacionalidad */}
        <Row className="mb-3">
          <Col sm={6}>
            <Form.Group controlId="fecha_nacimiento">
              <Form.Label>Fecha de Nacimiento</Form.Label>
              <Form.Control
                type="date"
                name="fecha_nacimiento"
                value={contactData.fecha_nacimiento || ""}
                onChange={handleChange}
                required
              />
            </Form.Group>
          </Col>
          <Col sm={6}>
            <Form.Group controlId="nacionalidad">
              <Form.Label>Nacionalidad</Form.Label>
              <Form.Control
                type="text"
                name="nacionalidad"
                value={contactData.nacionalidad || ""}
                onChange={handleChange}
                required
              />
            </Form.Group>
          </Col>
        </Row>

        {/* Dirección */}
        <Row className="mb-3">
          <Col sm={12}>
            <Form.Group controlId="direccion">
              <Form.Label>Dirección</Form.Label>
              <Form.Control
                type="text"
                name="direccion"
                value={contactData.direccion || ""}
                onChange={handleChange}
                required
              />
            </Form.Group>
          </Col>
        </Row>

        {/* Localidad y País */}
        <Row className="mb-3">
          <Col sm={6}>
            <Form.Group controlId="localidad">
              <Form.Label>Localidad</Form.Label>
              <Form.Control
                type="text"
                name="localidad"
                value={contactData.localidad || ""}
                onChange={handleChange}
                required
              />
            </Form.Group>
          </Col>
          <Col sm={6}>
            <Form.Group controlId="pais">
              <Form.Label>País</Form.Label>
              <Form.Control
                type="text"
                name="pais"
                value={contactData.pais || ""}
                onChange={handleChange}
                required
              />
            </Form.Group>
          </Col>
        </Row>
      </Form>
    </div>
  );
};

export default UserContactForm;