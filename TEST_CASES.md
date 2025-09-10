# Plan de Pruebas de Integración - Chatbot

## Información del proyecto

- **Nombre del proyecto**: Auto QA Chatbot
- **Fecha de creación**: 9 de septiembre de 2025
- **Versión**: 1.0

## Objetivo

Este documento describe los casos de prueba de integración para verificar el correcto funcionamiento del chatbot implementado en la aplicación web. Las pruebas se enfocan en validar la interacción del usuario con la interfaz del chatbot y la precisión de las respuestas según el contexto.

## Entorno de pruebas

- **Navegador**: Chrome (última versión)
- **Framework de pruebas**: Selenium WebDriver + Pytest
- **Lenguaje**: Python 3.x
- **Técnica**: Pruebas automatizadas de UI/UX

## Suites de pruebas

### 1. Suite: Funcionalidad básica de la UI

#### TC-UI-001: Visibilidad del botón de chat

**Objetivo**: Verificar que el botón circular del chat está presente en la página.

**Precondiciones**:
- La página web está cargada completamente

**Pasos**:
1. Cargar la página web

**Resultado esperado**:
- El botón circular del chat debe estar visible en la esquina inferior derecha
- El botón debe tener el icono de mensaje 💬
- El panel del chat debe estar oculto

**Prioridad**: Alta

---

#### TC-UI-002: Apertura y cierre del panel de chat

**Objetivo**: Verificar que el panel de chat se abre y cierra correctamente al hacer clic en el botón.

**Precondiciones**:
- La página web está cargada completamente

**Pasos**:
1. Cargar la página web
2. Hacer clic en el botón circular del chat
3. Verificar que el panel de chat se muestra
4. Hacer clic nuevamente en el botón circular del chat

**Resultado esperado**:
- El panel de chat debe mostrarse después del primer clic
- El panel de chat debe contener el mensaje de bienvenida
- El panel de chat debe ocultarse después del segundo clic

**Prioridad**: Alta

---

#### TC-UI-003: Componentes visuales del panel de chat

**Objetivo**: Verificar que todos los componentes del panel de chat están presentes y correctamente ubicados.

**Precondiciones**:
- La página web está cargada completamente
- El panel del chat está visible

**Pasos**:
1. Cargar la página web
2. Hacer clic en el botón circular del chat

**Resultado esperado**:
- El panel debe contener un encabezado con el texto "Asistente Virtual"
- El área de visualización de mensajes debe estar presente
- El campo de entrada de texto debe estar presente con el placeholder "Escribe tu mensaje..."
- El botón "Enviar" debe estar presente

**Prioridad**: Media

---

### 2. Suite: Envío y recepción de mensajes

#### TC-MSG-001: Envío de mensaje con botón "Enviar"

**Objetivo**: Verificar que se puede enviar un mensaje usando el botón "Enviar".

**Precondiciones**:
- La página web está cargada completamente
- El panel del chat está visible

**Pasos**:
1. Cargar la página web
2. Hacer clic en el botón circular del chat
3. Escribir "Hola" en el campo de entrada
4. Hacer clic en el botón "Enviar"

**Resultado esperado**:
- El mensaje "Hola" debe aparecer en el área de mensajes como un mensaje de usuario (alineado a la derecha)
- El campo de entrada debe quedar vacío después de enviar el mensaje
- El chatbot debe responder con un saludo (mensaje alineado a la izquierda)

**Prioridad**: Alta

---

#### TC-MSG-002: Envío de mensaje con tecla Enter

**Objetivo**: Verificar que se puede enviar un mensaje usando la tecla Enter.

**Precondiciones**:
- La página web está cargada completamente
- El panel del chat está visible

**Pasos**:
1. Cargar la página web
2. Hacer clic en el botón circular del chat
3. Escribir "Hola" en el campo de entrada
4. Presionar la tecla Enter

**Resultado esperado**:
- El mensaje "Hola" debe aparecer en el área de mensajes como un mensaje de usuario
- El campo de entrada debe quedar vacío después de enviar el mensaje
- El chatbot debe responder con un saludo

**Prioridad**: Alta

---

#### TC-MSG-003: Envío de mensaje vacío

**Objetivo**: Verificar que no se procesa el envío de un mensaje vacío.

**Precondiciones**:
- La página web está cargada completamente
- El panel del chat está visible

**Pasos**:
1. Cargar la página web
2. Hacer clic en el botón circular del chat
3. Sin escribir nada en el campo de entrada, hacer clic en el botón "Enviar"

**Resultado esperado**:
- No debe aparecer ningún mensaje nuevo en el área de mensajes
- El chatbot no debe enviar ninguna respuesta

**Prioridad**: Baja

---

### 3. Suite: Respuestas contextuales del chatbot

#### TC-RESP-001: Respuesta a saludos

**Objetivo**: Verificar que el chatbot responde correctamente a diferentes formas de saludo.

**Precondiciones**:
- La página web está cargada completamente
- El panel del chat está visible

**Pasos**:
1. Cargar la página web
2. Hacer clic en el botón circular del chat
3. Enviar los siguientes mensajes (uno por uno, verificando respuesta):
   - "Hola"
   - "Buenos días"
   - "Buenas tardes"
   - "Buenas noches"

**Resultado esperado**:
- Para cada saludo, el chatbot debe responder con un mensaje que incluya "¡Hola!" y un emoji de saludo
- La respuesta debe ser consistente con el formato esperado de los mensajes del bot

**Prioridad**: Media

---

#### TC-RESP-002: Respuesta sobre precios

**Objetivo**: Verificar que el chatbot responde correctamente a preguntas sobre precios.

**Precondiciones**:
- La página web está cargada completamente
- El panel del chat está visible

**Pasos**:
1. Cargar la página web
2. Hacer clic en el botón circular del chat
3. Enviar los siguientes mensajes (uno por uno, verificando respuesta):
   - "¿Cuáles son los precios?"
   - "¿Cuánto cuesta el servicio?"
   - "Necesito saber las tarifas"

**Resultado esperado**:
- Para cada pregunta, el chatbot debe responder con información sobre precios
- La respuesta debe mencionar "planes desde $9.99 al mes"
- La respuesta debe incluir un emoji relevante (📊)

**Prioridad**: Alta

---

#### TC-RESP-003: Respuesta sobre productos/servicios

**Objetivo**: Verificar que el chatbot responde correctamente a preguntas sobre productos y servicios.

**Precondiciones**:
- La página web está cargada completamente
- El panel del chat está visible

**Pasos**:
1. Cargar la página web
2. Hacer clic en el botón circular del chat
3. Enviar los siguientes mensajes (uno por uno, verificando respuesta):
   - "¿Qué productos tienen?"
   - "Cuéntame sobre sus servicios"
   - "¿Qué ofrecen?"

**Resultado esperado**:
- Para cada pregunta, el chatbot debe responder con información sobre servicios
- La respuesta debe mencionar "atención al cliente, análisis de datos y automatización de marketing"
- La respuesta debe incluir un emoji relevante (🛍️)

**Prioridad**: Alta

---

#### TC-RESP-004: Respuesta sobre contacto

**Objetivo**: Verificar que el chatbot responde correctamente a preguntas sobre información de contacto.

**Precondiciones**:
- La página web está cargada completamente
- El panel del chat está visible

**Pasos**:
1. Cargar la página web
2. Hacer clic en el botón circular del chat
3. Enviar los siguientes mensajes (uno por uno, verificando respuesta):
   - "¿Cómo puedo contactarlos?"
   - "¿Cuál es su teléfono?"
   - "¿Cuál es su correo electrónico?"

**Resultado esperado**:
- Para cada pregunta, el chatbot debe responder con información de contacto
- La respuesta debe incluir un número de teléfono (555-123-4567)
- La respuesta debe incluir un correo electrónico (contacto@empresa.com)
- La respuesta debe incluir un emoji relevante (📞)

**Prioridad**: Media

---

#### TC-RESP-005: Respuesta sobre soporte técnico

**Objetivo**: Verificar que el chatbot responde correctamente a menciones sobre problemas técnicos.

**Precondiciones**:
- La página web está cargada completamente
- El panel del chat está visible

**Pasos**:
1. Cargar la página web
2. Hacer clic en el botón circular del chat
3. Enviar los siguientes mensajes (uno por uno, verificando respuesta):
   - "Tengo un problema con el servicio"
   - "Me sale un error"
   - "No funciona la aplicación"

**Resultado esperado**:
- Para cada mensaje, el chatbot debe solicitar más detalles sobre el problema
- La respuesta debe mostrar interés en resolver el problema del usuario
- La respuesta debe incluir un emoji relevante (🔧)

**Prioridad**: Media

---

#### TC-RESP-006: Respuesta a agradecimientos

**Objetivo**: Verificar que el chatbot responde correctamente a mensajes de agradecimiento.

**Precondiciones**:
- La página web está cargada completamente
- El panel del chat está visible

**Pasos**:
1. Cargar la página web
2. Hacer clic en el botón circular del chat
3. Enviar los siguientes mensajes (uno por uno, verificando respuesta):
   - "Gracias"
   - "Muchas gracias por la información"
   - "Te agradezco"

**Resultado esperado**:
- Para cada mensaje, el chatbot debe responder con un mensaje de cortesía
- La respuesta debe incluir frases como "De nada" o "Ha sido un placer"
- La respuesta debe incluir un emoji relevante (😊)

**Prioridad**: Baja

---

#### TC-RESP-007: Respuesta a despedidas

**Objetivo**: Verificar que el chatbot responde correctamente a mensajes de despedida.

**Precondiciones**:
- La página web está cargada completamente
- El panel del chat está visible

**Pasos**:
1. Cargar la página web
2. Hacer clic en el botón circular del chat
3. Enviar los siguientes mensajes (uno por uno, verificando respuesta):
   - "Adiós"
   - "Hasta luego"
   - "Nos vemos"

**Resultado esperado**:
- Para cada mensaje, el chatbot debe responder con un mensaje de despedida
- La respuesta debe incluir frases como "Hasta pronto" o "Que tengas un excelente día"
- La respuesta debe incluir un emoji relevante (👋)

**Prioridad**: Baja

---

#### TC-RESP-008: Respuesta por defecto para mensaje no reconocido

**Objetivo**: Verificar que el chatbot responde apropiadamente cuando no entiende el mensaje del usuario.

**Precondiciones**:
- La página web está cargada completamente
- El panel del chat está visible

**Pasos**:
1. Cargar la página web
2. Hacer clic en el botón circular del chat
3. Enviar un mensaje que no coincida con ninguna de las categorías reconocidas:
   - "xyzabc123"

**Resultado esperado**:
- El chatbot debe responder indicando que no entendió el mensaje
- La respuesta debe solicitar al usuario que reformule su pregunta
- La respuesta debe mantener un tono amigable y servicial

**Prioridad**: Media

---

## Criterios de Aceptación

Para que las pruebas se consideren exitosas:

1. Todas las pruebas de **prioridad Alta** deben pasar al 100%
2. Al menos el 90% de las pruebas de **prioridad Media** deben pasar
3. Al menos el 80% de las pruebas de **prioridad Baja** deben pasar
4. No deben existir errores JavaScript en la consola del navegador
5. Todas las respuestas del chatbot deben generarse en menos de 2 segundos

## Notas adicionales

- Las pruebas deben ejecutarse tanto en modo headless (sin interfaz gráfica) para integración continua, como en modo visual para depuración
- Se recomienda implementar capturas de pantalla automáticas en caso de fallo para facilitar la depuración
- El comportamiento del chat debe ser consistente en distintas resoluciones de pantalla
