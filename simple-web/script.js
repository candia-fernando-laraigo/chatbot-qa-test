// Espera a que todo el contenido del HTML esté cargado antes de ejecutar el script
document.addEventListener("DOMContentLoaded", () => {
  // Obtenemos las referencias a los elementos del HTML por su ID
  const chatToggleButton = document.getElementById("chat-toggle-button");
  const chatPanel = document.getElementById("chat-panel");
  const chatInput = document.getElementById("chat-input");
  const sendButton = document.getElementById("send-button");
  const chatDisplay = document.getElementById("chat-display");

  // --- MOSTRAR Y OCULTAR EL CHAT ---
  chatToggleButton.addEventListener("click", () => {
    chatPanel.classList.toggle("hidden"); // Alterna la clase 'hidden'
  });

  // --- ENVIAR MENSAJE ---
  sendButton.addEventListener("click", sendMessage);
  chatInput.addEventListener("keydown", (event) => {
    // Permite enviar mensaje también con la tecla "Enter"
    if (event.key === "Enter") {
      sendMessage();
    }
  });

  function sendMessage() {
    const userMessage = chatInput.value.trim(); // Obtiene el texto y quita espacios
    if (userMessage === "") return; // Si no hay texto, no hace nada

    // Muestra el mensaje del usuario en el panel
    appendMessage(userMessage, "user-message");
    
    chatInput.value = "";
    let timeResponse = Math.floor(Math.random() * 500) + 500;
    setTimeout(() => {
      const botResponse = getBotResponse(userMessage);
      appendMessage(botResponse, "bot-message");
    }, timeResponse);
  }

  // --- RESPUESTA DEL BOT ---
  function getBotResponse(userMessage) {
    const lowerCaseMessage = userMessage.toLowerCase(); // Convertimos a minúsculas para facilitar la comparación

    // Saludos
    if (
      lowerCaseMessage.includes("hola") ||
      lowerCaseMessage.includes("buenos días") ||
      lowerCaseMessage.includes("buenas tardes") ||
      lowerCaseMessage.includes("buenas noches")
    ) {
      return "¡Hola! 👋 ¿En qué puedo ayudarte hoy?";
    }
    // Precios y costos
    else if (
      lowerCaseMessage.includes("valor") ||
      lowerCaseMessage.includes("precio") ||
      lowerCaseMessage.includes("costo") ||
      lowerCaseMessage.includes("tarifa") ||
      lowerCaseMessage.includes("cuánto cuesta")
    ) {
      return "📊 Nuestros precios son muy competitivos. Contamos con planes desde $9.99 al mes. ¿Te gustaría conocer más detalles sobre algún plan específico?";
    }
    // Información del producto/servicio
    else if (
      lowerCaseMessage.includes("producto") ||
      lowerCaseMessage.includes("servicio") ||
      lowerCaseMessage.includes("que ofrecen") ||
      lowerCaseMessage.includes("cómo funciona")
    ) {
      return "🛍️ Ofrecemos una amplia gama de servicios, incluyendo atención al cliente, análisis de datos y automatización de marketing. ¿Hay algún servicio específico que te interese?";
    }
    // Atención al cliente
    else if (
      lowerCaseMessage.includes("contacto") ||
      lowerCaseMessage.includes("contactar") ||
      lowerCaseMessage.includes("teléfono") ||
      lowerCaseMessage.includes("correo") ||
      lowerCaseMessage.includes("email") ||
      lowerCaseMessage.includes("datos") ||
      lowerCaseMessage.includes("llamar")
    ) {
      return "📞 Puedes contactarnos al teléfono 555-123-4567 o enviarnos un correo a contacto@empresa.com. Nuestro horario de atención es de 9:00 a 18:00 de lunes a viernes.";
    }
    // Soporte técnico
    else if (
      lowerCaseMessage.includes("problema") ||
      lowerCaseMessage.includes("error") ||
      lowerCaseMessage.includes("falla") ||
      lowerCaseMessage.includes("no funciona") ||
      lowerCaseMessage.includes("problema")
    ) {
      return "🔧 Lamento escuchar eso. Para brindarte un mejor soporte técnico, ¿podrías describir el problema con más detalle?";
    }
    // Horarios
    else if (
      lowerCaseMessage.includes("horario") ||
      lowerCaseMessage.includes("abierto") ||
      lowerCaseMessage.includes("cerrado") ||
      lowerCaseMessage.includes("horario") ||
      lowerCaseMessage.includes("horas")
    ) {
      return "🕒 Nuestro horario de atención es de lunes a viernes de 9:00 a 18:00 y sábados de 10:00 a 14:00. Domingos cerrado.";
    }
    // Ubicación
    else if (
      lowerCaseMessage.includes("donde") ||
      lowerCaseMessage.includes("ubicación") ||
      lowerCaseMessage.includes("dirección") ||
      lowerCaseMessage.includes("como llegar") ||
      lowerCaseMessage.includes("ubicación") ||
      lowerCaseMessage.includes("dónde")
    ) {
      return '📍 Nos encontramos ubicados en Av. Principal #123, Col. Centro. Puedes encontrarnos fácilmente en Google Maps buscando "Empresa".';
    }
    // Promociones
    else if (
      lowerCaseMessage.includes("descuento") ||
      lowerCaseMessage.includes("promoción") ||
      lowerCaseMessage.includes("oferta") ||
      lowerCaseMessage.includes("descuento")
    ) {
      return "🎉 ¡Tenemos grandes promociones este mes! 30% de descuento en todos nuestros servicios para nuevos clientes y 15% para clientes actuales que renueven su suscripción.";
    }
    // Agradecimientos
    else if (
      lowerCaseMessage.includes("gracias") ||
      lowerCaseMessage.includes("thank") ||
      lowerCaseMessage.includes("te agradezco") ||
      lowerCaseMessage.includes("gracias")
    ) {
      return "😊 ¡De nada! Ha sido un placer ayudarte. Si tienes más preguntas, no dudes en consultar.";
    }
    // Despedida
    else if (
      lowerCaseMessage.includes("adiós") ||
      lowerCaseMessage.includes("hasta luego") ||
      lowerCaseMessage.includes("bye") ||
      lowerCaseMessage.includes("adiós")
    ) {
      return "👋 ¡Hasta pronto! Que tengas un excelente día.";
    }
    // Respuesta por defecto
    else {
      return "Lo siento, no entendí completamente tu pregunta. ¿Podrías reformularla o ser más específico? Estoy aquí para ayudarte.";
    }
  }

  // --- AÑADIR MENSAJES AL PANEL VISUALMENTE ---
  function appendMessage(text, className) {
    const messageElement = document.createElement("div");
    messageElement.className = className;
    messageElement.textContent = text;
    chatDisplay.appendChild(messageElement);

    // Hace scroll automático para que el último mensaje siempre sea visible
    chatDisplay.scrollTop = chatDisplay.scrollHeight;
  }
});
