"""
Response validation tests for the Laraigo chatbot interface.
Tests the accuracy, relevance, and response time of chatbot responses.
"""

import pytest
import time
from pages.laraigo_page import LaraigoPage


@pytest.mark.laraigo
@pytest.mark.parametrize(
    "greeting",
    [
        "Hola Buenos dias",
        "Hola que tal",
        "Buenas noches",
        "Buenas tardes",
        "Hola muy buenos dias",
        "Hola como estas",
        "Hola",
    ],
)
def test_greeting_responses(driver, greeting, test_data):
    """
    Test Case 1: Saludos y Frases de Cortesía
    Objetivo: Verificar que el sistema responde de manera correcta y consistente
    a diferentes tipos de saludos ingresados por el usuario.
    Resultado Esperado: Para cualquier saludo, el sistema debe responder con: "Hola Blanquiazul,..".
    """
    # Crear página y abrir chat
    page = LaraigoPage(driver)
    page.open_chat()

    # Enviar saludo
    start_time = time.time()
    bot_response = page.send_message(greeting)
    response_time = time.time() - start_time

    # Verificar que el mensaje del usuario se muestra en el chat
    user_messages = page.get_all_user_messages_text()
    assert greeting in user_messages, "El mensaje del usuario no se muestra en el chat"
    
    # Guardar datos para el reporte
    test_data(sent_message=greeting, response_text=bot_response, response_time=response_time)

    # Verificar que la respuesta del bot comienza con "Hola Blanquiazul"
    assert any(
        msg_text.startswith("Hola Blanquiazul") for msg_text in bot_response
    ), f"Ninguna de las respuesta del bot comienza con 'Hola Blanquiazul' para el mensaje: {greeting}. Respuestas: {bot_response}"


@pytest.mark.laraigo
@pytest.mark.parametrize(
    "query",
    [
        "Cuanto tiempo dura la membresia",
        "Que beneficios tiene la membresia",
        "Que descuentos tengo con la membresia",
        "Tengo descuentos en las entradas con la membresia?",
        "Cuanto cuesta la membresia",
        "Como adquiero la membresia",
        "Como cancelo la membresia?",
    ],
)
def test_membership_inquiry_responses(driver, query, test_data):
    """
    Test Case 2: Consultas sobre la Membresía
    Objetivo: Validar que el sistema identifica preguntas relacionadas con la membresía
    y proporciona la respuesta predeterminada para dirigir al usuario al canal correcto.
    Resultado Esperado: Ante cualquier pregunta sobre la membresía, el sistema debe responder:
    "Gracias por contactarte...".
    """
    # Crear página y abrir chat
    page = LaraigoPage(driver)
    page.open_chat()

    # Enviar consulta sobre membresía y obtener respuesta automáticamente
    start_time = time.time()
    bot_response = page.send_message(query)
    response_time = time.time() - start_time

    # Verificar que el mensaje del usuario se muestra en el chat
    user_messages = page.get_all_user_messages_text()
    assert query in user_messages, "El mensaje del usuario no se muestra en el chat"
    
    # Guardar datos para el reporte
    test_data(sent_message=query, response_text=bot_response, response_time=response_time)
    
    # Verificar que la respuesta del bot comienza con "Gracias por contactarte"
    assert any(
        msg_text.startswith("Gracias por contactarte") for msg_text in bot_response
    ), f"Ninguna de las respuesta del bot comienza con 'Gracias por contactarte' para la consulta: {query}. Respuesta: {bot_response}"


@pytest.mark.laraigo
@pytest.mark.parametrize(
    "query",
    [
        "Quien ganara la final",
        "Como me llamo",
        "Cuando se fundo lima",
        "Cual es el precio de la entrada",
        "Cuantos años tengo",
        "Quien ganara el mundial",
    ],
)
def test_out_of_scope_responses(driver, query, test_data):
    """
    Test Case 3: Preguntas Fuera de Alcance (General Knowledge & Personal Info)
    Objetivo: Comprobar que el sistema gestiona adecuadamente las preguntas que no está
    programado para responder (conocimiento general, predicciones, información personal, etc.).
    Resultado Esperado: Para cualquier pregunta fuera de su alcance, el sistema debe responder:
    "Lo lamento...".
    """
    # Crear página y abrir chat
    page = LaraigoPage(driver)
    page.open_chat()

    # Enviar pregunta fuera del alcance y obtener respuesta automáticamente
    start_time = time.time()
    bot_response = page.send_message(query)
    response_time = time.time() - start_time

    # Verificar que el mensaje del usuario se muestra en el chat
    user_messages = page.get_all_user_messages_text()
    assert query in user_messages, "El mensaje del usuario no se muestra en el chat"
    
    # Guardar datos para el reporte
    test_data(sent_message=query, response_text=bot_response, response_time=response_time)
    
    assert any(
        msg_text.startswith("Lo lamento") for msg_text in bot_response
    ), f"Ninguna de las respuesta del bot comienza con 'Lo lamento' para la consulta: {query}. Respuesta: {bot_response}"
