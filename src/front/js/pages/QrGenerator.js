import React, { useContext, useState, useEffect } from "react";
import { Navigate, useNavigate } from "react-router-dom";
import { Context } from "../store/appContext";
import { FaArrowLeft, FaBars, FaHome, FaUser, FaQrcode, FaHistory, FaCheck, FaCalendarAlt } from "react-icons/fa";
import NavbarHeader from "../component/NavbarHeader.jsx";
import ContactBanner from "../component/Banner.jsx";
import NavbarFooter from "../component/NavbarFooter.jsx";
import "../../styles/QrGenerator.css";
const isValidDate = (dateStr) => {
   if (!/^\d{2}\/\d{2}\/\d{2}$/.test(dateStr)) {
      return false;
   }
   const [day, month, year] = dateStr.split('/').map(num => parseInt(num, 10));
   const fullYear = 2000 + year;
   const date = new Date(fullYear, month - 1, day);
   return date &&
      date.getDate() === day &&
      date.getMonth() === month - 1 &&
      date.getFullYear() === fullYear;
};
const getDateFromString = (dateStr) => {
   const [day, month, year] = dateStr.split('/').map(num => parseInt(num, 10));
   return new Date(2000 + year, month - 1, day);
};
const QrCard = ({
   formData,
   setFormData,
   isSubmitted,
   setIsSubmitted,
   localError,
   setLocalError,
   handleSubmit,
   handleIndividualQR,
   handleReset,
   isLoading
}) => {
   const validateDate = (value, field) => {
      if (!value) {
         setLocalError(`La fecha de ${field === 'startDate' ? 'inicio' : 'fin'} es requerida`);
         return false;
      }
      if (!isValidDate(value)) {
         setLocalError(`Formato de fecha inválido para ${field === 'startDate' ? 'inicio' : 'fin'}. Use DD/MM/YY`);
         return false;
      }
      if (field === 'endDate' && formData.startDate) {
         const startDate = getDateFromString(formData.startDate);
         const endDate = getDateFromString(value);
         if (endDate < startDate) {
            setLocalError('La fecha de fin no puede ser anterior a la fecha de inicio');
            return false;
         }
      }
      setLocalError(null);
      return true;
   };
   const handleDateChange = (e, field) => {
      const { value } = e.target;
      setFormData({ ...formData, [field]: value });
      if (value.length === 8) {
         const formattedDate = value.replace(/(\d{2})(\d{2})(\d{2})/, '$1/$2/$3');
         setFormData({ ...formData, [field]: formattedDate });
         validateDate(formattedDate, field);
      } else if (value.length === 0) {
         setLocalError(null);
      }
   };
   return isSubmitted ? (
      <div className="qr-card success">
         <div className="card-content">
            <FaCheck className="success-icon" />
            <p>¡QR generado exitosamente!</p>
            <button className="button primary-button full-width" onClick={handleReset}>
               Generar otro QR
            </button>
         </div>
      </div>
   ) : (
      <div className="qr-card">
         <div className="card-content">
            <form onSubmit={handleSubmit} className="qr-form">
               <div className="form-group">
                  <label htmlFor="qrName">Nombre del QR:</label>
                  <input
                     id="qrName"
                     type="text"
                     name="name"
                     value={formData.name}
                     onChange={(e) => {
                        setFormData({ ...formData, name: e.target.value });
                        setLocalError(null);
                     }}
                     className="form-input"
                     placeholder="Nombre del QR"
                  />
               </div>
               <div className="form-group">
                  <label htmlFor="event">Evento *</label>
                  <div className="select-wrapper">
                     <select
                        id="event"
                        name="event"
                        value={formData.event}
                        onChange={(e) => {
                           setFormData({ ...formData, event: e.target.value });
                           setLocalError(null);
                        }}
                        className="form-select"
                        required
                     >
                        <option value="">Selecciona un evento</option>
                        <option value="event1">Evento 1</option>
                        <option value="event2">Evento 2</option>
                     </select>
                  </div>
               </div>
               <div className="date-container">
                  <div className="form-group">
                     <label htmlFor="startDate">Inicio: *</label>
                     <div className="date-input-wrapper">
                        <input
                           id="startDate"
                           type="text"
                           name="startDate"
                           value={formData.startDate}
                           onChange={(e) => handleDateChange(e, 'startDate')}
                           onBlur={(e) => validateDate(e.target.value, 'startDate')}
                           placeholder="DD/MM/YY"
                           className="form-input"
                           maxLength="8"
                           required
                        />
                        <FaCalendarAlt className="calendar-icon" />
                     </div>
                  </div>
                  <div className="form-group">
                     <label htmlFor="endDate">Fin: *</label>
                     <div className="date-input-wrapper">
                        <input
                           id="endDate"
                           type="text"
                           name="endDate"
                           value={formData.endDate}
                           onChange={(e) => handleDateChange(e, 'endDate')}
                           onBlur={(e) => validateDate(e.target.value, 'endDate')}
                           placeholder="DD/MM/YY"
                           className="form-input"
                           maxLength="8"
                           required
                        />
                        <FaCalendarAlt className="calendar-icon" />
                     </div>
                  </div>
               </div>
               {localError && <div className="error-message">{localError}</div>}
               <div className="button-container">
                  <button
                     type="button"
                     className="button secondary-button"
                     onClick={handleIndividualQR}
                     disabled={isLoading}
                  >
                     {isLoading ? "Generando..." : "Generar QR individual"}
                  </button>
                  <button
                     type="submit"
                     className="button primary-button"
                     disabled={!formData.event || !formData.startDate || !formData.endDate || localError || isLoading}
                  >
                     {isLoading ? "Generando..." : "Generar QR grupal"}
                  </button>
               </div>
            </form>
         </div>
      </div>
   );
};
const QrGenerator = () => {
   const { actions } = useContext(Context);
   const navigate = useNavigate();
   const [validToken, setValidToken] = useState(null);
   const [formData, setFormData] = useState({
      name: '',
      event: '',
      startDate: '',
      endDate: ''
   });
   const [isSubmitted, setIsSubmitted] = useState(false);
   const [localError, setLocalError] = useState(null);
   const [isLoading, setIsLoading] = useState(false);
   useEffect(() => {
      const localToken = localStorage.getItem("authToken");
      setValidToken(!!localToken && localToken.trim() !== "");
   }, []);
   const validateForm = () => {
      if (!formData.event || !formData.startDate || !formData.endDate) {
         setLocalError("Por favor completa todos los campos obligatorios");
         return false;
      }
      if (!isValidDate(formData.startDate)) {
         setLocalError("Fecha de inicio inválida");
         return false;
      }
      if (!isValidDate(formData.endDate)) {
         setLocalError("Fecha de fin inválida");
         return false;
      }
      const startDate = getDateFromString(formData.startDate);
      const endDate = getDateFromString(formData.endDate);
      if (endDate < startDate) {
         setLocalError("La fecha de fin no puede ser anterior a la fecha de inicio");
         return false;
      }
      return true;
   };
   const handleLogout = () => {
      localStorage.removeItem("authToken");
      actions.setAuthToken(null);
      navigate("/login");
   };

   const handleIndividualQR = async () => {
      if (validateForm()) {
         try {
            setIsLoading(true);
            setLocalError(null);
            console.log("Iniciando generación de QR individual...");
            const token = localStorage.getItem("authToken");
            const contactId = 1;
            const BACKEND_URL = process.env.BACKEND_URL;
            // Primera petición - Obtener QR
            const qrResponse = await fetch(`${BACKEND_URL}api/contact/${contactId}/qr`, {
               method: 'GET',
               headers: {
                  'Authorization': `Bearer ${token}`
               }
            });
            if (!qrResponse.ok) {
               throw new Error('Error en la generación del QR');
            }
            const qrData = await qrResponse.json();
            console.log("QR generado correctamente");
            // Segunda petición - Guardar datos
            const saveResponse = await fetch(`${BACKEND_URL}api/contact/${contactId}/qrcode`, {
               method: 'POST',
               headers: {
                  'Content-Type': 'application/json',
                  'Authorization': `Bearer ${token}`
               },
               body: JSON.stringify({
                  nombre: formData.name,
                  fecha_inicio: formData.startDate,
                  fecha_fin: formData.endDate,
                  data: qrData.qr_base64
               })
            });
            if (!saveResponse.ok) {
               throw new Error('Error al guardar los datos del QR');
            }
            console.log("QR guardado exitosamente");
            setIsSubmitted(true);
         } catch (error) {
            console.log("Se produjo un error en el proceso");
            setLocalError("No se pudo completar la operación. Por favor, intente nuevamente.");
         } finally {
            setIsLoading(false);
         }
      }
   };
   const handleSubmit = async (e) => {
      e.preventDefault();
      if (validateForm()) {
         try {
            setIsLoading(true);
            setLocalError(null);
            console.log("Iniciando generación de QR grupal...");
            const token = localStorage.getItem("authToken");
            const groupId = 1;
            const BACKEND_URL = process.env.BACKEND_URL;
            // Primera petición - Obtener QR grupal
            const qrResponse = await fetch(`${BACKEND_URL}api/group/${groupId}/qr`, {
               method: 'GET',
               headers: {
                  'Authorization': `Bearer ${token}`
               }
            });
            if (!qrResponse.ok) {
               throw new Error('Error en la generación del QR grupal');
            }
            const qrData = await qrResponse.json();
            console.log("QR grupal generado correctamente");
            // Segunda petición - Guardar datos del QR grupal
            const saveResponse = await fetch(`${BACKEND_URL}api/contact/${groupId}/qrcode`, {
               method: 'POST',
               headers: {
                  'Content-Type': 'application/json',
                  'Authorization': `Bearer ${token}`
               },
               body: JSON.stringify({
                  nombre: formData.name,
                  fecha_inicio: formData.startDate,
                  fecha_fin: formData.endDate,
                  data: qrData.qr_base64
               })
            });
            if (!saveResponse.ok) {
               throw new Error('Error al guardar los datos del QR grupal');
            }
            console.log("QR grupal guardado exitosamente");
            setIsSubmitted(true);
         } catch (error) {
            console.log("Se produjo un error en el proceso del QR grupal");
            setLocalError("No se pudo completar la operación. Por favor, intente nuevamente.");
         } finally {
            setIsLoading(false); y
         }
      }
   };
   const handleReset = () => {
      setFormData({
         name: '',
         event: '',
         startDate: '',
         endDate: ''
      });
      setIsSubmitted(false);
      setLocalError(null);
   };
   if (validToken === null) return <h1>Cargando...</h1>;
   if (!validToken) return <Navigate to="/login" replace />;
   return (
      <div className="qr-generator-container">
         <NavbarHeader />
         <main className="main-content">
            <QrCard
               formData={formData}
               setFormData={setFormData}
               isSubmitted={isSubmitted}
               setIsSubmitted={setIsSubmitted}
               localError={localError}
               setLocalError={setLocalError}
               handleSubmit={handleSubmit}
               handleIndividualQR={handleIndividualQR}
               handleReset={handleReset}
               isLoading={isLoading}
            />
         </main>
         <ContactBanner />
         <NavbarFooter />
      </div>
   );
};
export default QrGenerator;