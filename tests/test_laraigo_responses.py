"""
Response validation tests for the Laraigo chatbot interface.
Tests the accuracy, relevance, and response time of chatbot responses.
"""

import pytest
import time
from pages.laraigo_page import LaraigoPage


@pytest.fixture
def laraigo_page(driver):
    """Fixture para crear una instancia de LaraigoPage que se reutiliza en los tests."""
    return LaraigoPage(driver)


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
    ],
)
def test_greeting_responses(driver, laraigo_page, greeting, logger, request, test_data):
    """
    Test Case 1: Saludos y Frases de Cortesía
    Objetivo: Verificar que el sistema responde de manera correcta y consistente
    a diferentes tipos de saludos ingresados por el usuario.
    Resultado Esperado: Para cualquier saludo, el sistema debe responder con: "Hola Blanquiazul,..".
    """
    # Log test information
    logger.info(f"Testing greeting response for: '{greeting}'")

    # Abrir chat
    laraigo_page.open_chat()
    logger.debug("Chat window opened")

    # Enviar saludo
    start_time = time.time()
    bot_response = laraigo_page.send_message(greeting)
    response_time = time.time() - start_time
    logger.debug(f"Sent message: '{greeting}' and received response")

    # Verificar que el mensaje del usuario se muestra en el chat
    user_messages = laraigo_page.get_all_user_messages_text()
    assert greeting in user_messages, "El mensaje del usuario no se muestra en el chat"
    logger.debug("User message verified in chat")

    # Log response time
    logger.log_response_time("test_greeting_responses", greeting, response_time)
    # Log bot response
    if bot_response:
        logger.info(
            f"Bot responses received: {[msg[:100] + '...' if len(msg) > 100 else msg for msg in bot_response]} (truncated)"
        )
    # Log all bot messages
    for idx, msg in enumerate(laraigo_page.get_all_bot_messages_text()):
        logger.debug(f"Bot message {idx + 1}: {msg}")
    # Log all user messages
    for idx, msg in enumerate(laraigo_page.get_all_user_messages_text()):
        logger.debug(f"User message {idx + 1}: {msg}")
    
    # Save test data for reporting
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
def test_membership_inquiry_responses(driver, laraigo_page, query, logger, request, test_data):
    """
    Test Case 2: Consultas sobre la Membresía
    Objetivo: Validar que el sistema identifica preguntas relacionadas con la membresía
    y proporciona la respuesta predeterminada para dirigir al usuario al canal correcto.
    Resultado Esperado: Ante cualquier pregunta sobre la membresía, el sistema debe responder:
    "Gracias por contactarte...".
    """
    # Log test information
    logger.info(f"Testing membership query response for: '{query}'")

    # Abrir chat
    laraigo_page.open_chat()
    logger.debug("Chat window opened")

    # Enviar consulta sobre membresía y obtener respuesta automáticamente
    start_time = time.time()
    bot_response = laraigo_page.send_message(query)
    response_time = time.time() - start_time
    logger.debug(f"Sent message: '{query}' and received response")

    # Verificar que el mensaje del usuario se muestra en el chat
    user_messages = laraigo_page.get_all_user_messages_text()
    assert query in user_messages, "El mensaje del usuario no se muestra en el chat"
    logger.debug("User message verified in chat")

    # Log response time
    logger.log_response_time("test_membership_inquiry_responses", query, response_time)
    # Log bot response
    if bot_response:
        logger.info(
            f"Bot responses received: {[msg[:100] + '...' if len(msg) > 100 else msg for msg in bot_response]} (truncated)"
        )
    # Log all bot messages
    for idx, msg in enumerate(laraigo_page.get_all_bot_messages_text()):
        logger.debug(f"Bot message {idx + 1}: {msg}")
    # Log all user messages
    for idx, msg in enumerate(laraigo_page.get_all_user_messages_text()):
        logger.debug(f"User message {idx + 1}: {msg}")

    # Save test data for reporting
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
def test_out_of_scope_responses(driver, laraigo_page, query, logger, request, test_data):
    """
    Test Case 3: Preguntas Fuera de Alcance (General Knowledge & Personal Info)
    Objetivo: Comprobar que el sistema gestiona adecuadamente las preguntas que no está
    programado para responder (conocimiento general, predicciones, información personal, etc.).
    Resultado Esperado: Para cualquier pregunta fuera de su alcance, el sistema debe responder:
    "Lo lamento...".
    """
    # Log test information
    logger.info(f"Testing out-of-scope query response for: '{query}'")

    # Abrir chat
    laraigo_page.open_chat()
    logger.debug("Chat window opened")

    # Enviar pregunta fuera del alcance y obtener respuesta automáticamente
    start_time = time.time()
    bot_response = laraigo_page.send_message(query)
    response_time = time.time() - start_time
    logger.debug(f"Sent message: '{query}' and received response")

    # Verificar que el mensaje del usuario se muestra en el chat
    user_messages = laraigo_page.get_all_user_messages_text()
    assert query in user_messages, "El mensaje del usuario no se muestra en el chat"
    logger.debug("User message verified in chat")

    # Log response time
    logger.log_response_time("test_out_of_scope_responses", query, response_time)
    # Log bot response
    if bot_response:
        logger.info(
            f"Bot responses received: {[msg[:100] + '...' if len(msg) > 100 else msg for msg in bot_response]} (truncated)"
        )
    # Log all bot messages
    for idx, msg in enumerate(laraigo_page.get_all_bot_messages_text()):
        logger.debug(f"Bot message {idx + 1}: {msg}")
    # Log all user messages
    for idx, msg in enumerate(laraigo_page.get_all_user_messages_text()):
        logger.debug(f"User message {idx + 1}: {msg}")
    
    # Save test data for reporting
    test_data(sent_message=query, response_text=bot_response, response_time=response_time)
    
    assert any(
        msg_text.startswith("Lo lamento") for msg_text in bot_response
    ), f"Ninguna de las respuesta del bot comienza con 'Lo lamento' para la consulta: {query}. Respuesta: {bot_response}"
