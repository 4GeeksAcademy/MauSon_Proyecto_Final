import React from "react";
import { Form } from "react-bootstrap";

const SensitiveDataForm = ({ sensitiveData, setSensitiveData }) => {
  const handleChange = (e) => {
    const { name, value } = e.target;
    setSensitiveData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  return (
    <div>
      <h4>Datos Sensibles</h4>
      <Form>
        <Form.Group controlId="nif_tipo">
          <Form.Label>NIF Tipo</Form.Label>
          <Form.Control
            type="text"
            name="nif_tipo"
            value={sensitiveData?.nif_tipo || ""}
            onChange={handleChange}
            placeholder="Introduce el tipo de NIF"
          />
        </Form.Group>

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
      </Form>
    </div>
  );
};

export default SensitiveDataForm;