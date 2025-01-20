const getState = ({ getStore, getActions, setStore }) => {
	return {
		store: {
			message: null,
			authToken: localStorage.getItem("authToken") || null, // Inicializamos con el token del localStorage
			role: null, //user o admin
			user: null, // dato del usuario autenticado

		},
		actions: {
			// Use getActions to call a function within a fuction
			login: async (email, password) => {
				try {
					const resp = await fetch(process.env.BACKEND_URL + "/api/login", {
						method: "POST",
						headers: { "Content-Type": "application/json" },
						body: JSON.stringify({ email, password }),
					});

					if (resp.ok) {
						const token = await resp.text();
						localStorage.setItem("authToken", token);
						setStore({ authToken: token });
						return { success: true, message: "Login exitoso" };
					} else {
						const error = await resp.json(); // Esto seguirá siendo válido para mensajes de error
						return { success: false, message: error.message || "Error en el login" };
					}
				} catch (err) {
					console.error("Error en login:", err);
					return { success: false, message: "Error de conexión" };
				}
			},

			logout: () => {
				localStorage.removeItem("authToken");  // Eliminamos el token del localStorage
				setStore({ authToken: null });  // Actualizamos el store para eliminar el token
				console.log("Usuario deslogueado exitosamente.");
			},

			signup: async (email, password, language) => {
				try {
				  const resp = await fetch(process.env.BACKEND_URL + "/api/signup", {
					method: "POST",
					headers: { "Content-Type": "application/json" },
					body: JSON.stringify({ email, password, language }),  // Verifica que 'language' está siendo enviado correctamente
				  });
			  
				  if (resp.ok) {
					const data = await resp.json();
					return { success: true, message: "Registro exitoso" };
				  } else {
					const error = await resp.json();
					console.error("Error en el registro:", error);  // Agrega un log para ver el error detallado
					return { success: false, message: error.message || "Error en el registro" };
				  }
				} catch (err) {
				  console.error("Error en signup:", err);
				  return { success: false, message: "Error de conexión" };
				}
			  }
		}
	};
};

export default getState;
