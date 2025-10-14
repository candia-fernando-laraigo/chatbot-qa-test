# Resumen de Casos de Prueba

#### **Test Case 1: Saludos y Frases de Cortesía**

* **Objetivo:** Verificar que el sistema responde de manera correcta y consistente a diferentes tipos de saludos ingresados por el usuario.
* **Resultado Esperado:** Para cualquier saludo, el sistema debe responder con: "Hola Blanquiazul,..".
* **Inputs de Prueba:**
    * `Hola Buenos dias`
    * `Hola que tal`
    * `Buenas noches`
    * `Buenas tardes`
    * `Hola muy buenos dias`
    * `Hola como estas`

---

#### **Test Case 2: Consultas sobre la Membresía**

* **Objetivo:** Validar que el sistema identifica preguntas relacionadas con la membresía y proporciona la respuesta predeterminada para dirigir al usuario al canal correcto.
* **Resultado Esperado:** Ante cualquier pregunta sobre la membresía, el sistema debe responder: "Gracias por contactarte...".
* **Inputs de Prueba:**
    * `Cuanto tiempo dura la membresia`
    * `Que beneficios tiene la membresia`
    * `Que descuentos tengo con la membresia`
    * `Tengo descuentos en las entradas con la membresia?`
    * `Cuanto cuesta la membresia`
    * `Como adquiero la membresia`
    * `Como cancelo la membresia?`

---

#### **Test Case 3: Preguntas Fuera de Alcance (General Knowledge & Personal Info)**

* **Objetivo:** Comprobar que el sistema gestiona adecuadamente las preguntas que no está programado para responder (conocimiento general, predicciones, información personal, etc.).
* **Resultado Esperado:** Para cualquier pregunta fuera de su alcance, el sistema debe responder: "Lo lamento...".
* **Inputs de Prueba:**
    * `Quien ganara la final`
    * `Como me llamo`
    * `Cuando se fundo lima`
    * `Cual es el precio de la entrada`
    * `Cuantos años tengo`
    * `Quien ganara el mundial`