import React from "react";
import { Form, Row, Col } from "react-bootstrap";
import "../../styles/userView/formSensitive.css"; // Asegúrate de importar el archivo CSS

const SensitiveDataForm = ({ sensitiveData, setSensitiveData }) => {
  const handleChange = (e) => {
    const { name, value } = e.target;
    setSensitiveData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  return (
    <div className="sensitive-data-form-container">
      <h4 className="form-title">Datos Sensibles</h4>
      <Form>
        {/* NIF Tipo - Dropdown */}
        <Row className="mb-3">
          <Col sm={12}>
            <Form.Group controlId="nif_tipo">
              <Form.Label>NIF Tipo</Form.Label>
              <Form.Control
                as="select"
                name="nif_tipo"
                value={sensitiveData?.nif_tipo || ""}
                onChange={handleChange}
              >
                <option value="">Selecciona un tipo de NIF</option>
                <option value="DNI">DNI</option>
                <option value="TIE">TIE</option>
                <option value="PASAPORTE">Pasaporte</option>
              </Form.Control>
            </Form.Group>
          </Col>
        </Row>

        {/* NIF Número */}
        <Row className="mb-3">
          <Col sm={12}>
            <Form.Group controlId="nif_numero">
              <Form.Label>NIF Número</Form.Label>
              <Form.Control
                type="text"
                name="nif_numero"
                value={sensitiveData?.nif_numero || ""}
                onChange={handleChange}
                placeholder="Introduce el número de NIF"
              />
            </Form.Group>
          </Col>
        </Row>

        {/* NIF País */}
        <Row className="mb-3">
          <Col sm={12}>
            <Form.Group controlId="nif_country">
              <Form.Label>NIF País</Form.Label>
              <Form.Control
                type="text"
                name="nif_country"
                value={sensitiveData?.nif_country || ""}
                onChange={handleChange}
                placeholder="Introduce el país del NIF"
              />
            </Form.Group>
          </Col>
        </Row>
      </Form>
    </div>
  );
};

export default SensitiveDataForm;