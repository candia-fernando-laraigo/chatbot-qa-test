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


@pytest.mark.responses
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
def test_greeting_responses(driver, laraigo_page, greeting):
    """
    Test Case 1: Saludos y Frases de Cortesía
    Objetivo: Verificar que el sistema responde de manera correcta y consistente 
    a diferentes tipos de saludos ingresados por el usuario.
    Resultado Esperado: Para cualquier saludo, el sistema debe responder con: "Hola Blanquiazul,..".
    """
    # Abrir chat
    laraigo_page.open_chat()

    # Enviar saludo
    start_time = time.time()
    laraigo_page.send_message(greeting)
    
    # Verificar que el mensaje del usuario se muestra en el chat
    user_messages = laraigo_page.get_all_user_messages_text()
    assert greeting in user_messages, "El mensaje del usuario no se muestra en el chat"
    
    # Esperar y obtener respuesta del bot
    bot_response = laraigo_page.wait_for_bot_response()
    response_time = time.time() - start_time

    # Los datos se recogerán automáticamente por el hook del informe de prueba

    # Verificar que la respuesta del bot comienza con "Hola Blanquiazul"
    assert bot_response.startswith(
        "Hola Blanquiazul"
    ), f"La respuesta del bot no comienza con 'Hola Blanquiazul' para el saludo: {greeting}. Respuesta: {bot_response}"
    
    # Registrar tiempo de respuesta (límite aceptable: 5 segundos)
    assert response_time < 5, f"El tiempo de respuesta fue demasiado largo: {response_time} segundos"


@pytest.mark.responses
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
def test_membership_inquiry_responses(driver, laraigo_page, query):
    """
    Test Case 2: Consultas sobre la Membresía
    Objetivo: Validar que el sistema identifica preguntas relacionadas con la membresía 
    y proporciona la respuesta predeterminada para dirigir al usuario al canal correcto.
    Resultado Esperado: Ante cualquier pregunta sobre la membresía, el sistema debe responder: 
    "Gracias por contactarte...".
    """
    # Abrir chat
    laraigo_page.open_chat()

    # Enviar consulta sobre membresía
    start_time = time.time()
    laraigo_page.send_message(query)
    
    # Verificar que el mensaje del usuario se muestra en el chat
    user_messages = laraigo_page.get_all_user_messages_text()
    assert query in user_messages, "El mensaje del usuario no se muestra en el chat"
    
    # Esperar y obtener respuesta del bot
    bot_response = laraigo_page.wait_for_bot_response()
    response_time = time.time() - start_time

    # Los datos se recogerán automáticamente por el hook del informe de prueba

    # Verificar que la respuesta del bot comienza con "Gracias por contactarte"
    assert bot_response.startswith(
        "Gracias por contactarte"
    ), f"La respuesta del bot no comienza con 'Gracias por contactarte' para la consulta: {query}. Respuesta: {bot_response}"
    
    # Registrar tiempo de respuesta (límite aceptable: 5 segundos)
    assert response_time < 5, f"El tiempo de respuesta fue demasiado largo: {response_time} segundos"


@pytest.mark.responses
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
def test_out_of_scope_responses(driver, laraigo_page, query):
    """
    Test Case 3: Preguntas Fuera de Alcance (General Knowledge & Personal Info)
    Objetivo: Comprobar que el sistema gestiona adecuadamente las preguntas que no está 
    programado para responder (conocimiento general, predicciones, información personal, etc.).
    Resultado Esperado: Para cualquier pregunta fuera de su alcance, el sistema debe responder: 
    "Lo lamento...".
    """
    # Abrir chat
    laraigo_page.open_chat()

    # Enviar pregunta fuera del alcance
    start_time = time.time()
    laraigo_page.send_message(query)
    
    # Verificar que el mensaje del usuario se muestra en el chat
    user_messages = laraigo_page.get_all_user_messages_text()
    assert query in user_messages, "El mensaje del usuario no se muestra en el chat"
    
    # Esperar y obtener respuesta del bot
    bot_response = laraigo_page.wait_for_bot_response()
    response_time = time.time() - start_time

    # Los datos se recogerán automáticamente por el hook del informe de prueba

    # Verificar que la respuesta del bot comienza con "Lo lamento"
    assert bot_response.startswith(
        "Lo lamento"
    ), f"La respuesta del bot no comienza con 'Lo lamento' para la consulta: {query}. Respuesta: {bot_response}"
    
    # Registrar tiempo de respuesta (límite aceptable: 5 segundos)
    assert response_time < 5, f"El tiempo de respuesta fue demasiado largo: {response_time} segundos"


@pytest.mark.responses
def test_response_time_metrics(driver, laraigo_page):
    """Test para medir específicamente los tiempos de respuesta como métricas."""
    # Abrir chat
    laraigo_page.open_chat()

    # Lista de mensajes para probar
    test_messages = [
        "Hola Buenos dias",  # Caso de prueba 1
        "Que beneficios tiene la membresia",  # Caso de prueba 2
        "Quien ganara la final"  # Caso de prueba 3
    ]

    response_times = {}

    for message in test_messages:
        # Enviar mensaje
        start_time = time.time()
        laraigo_page.send_message(message)
        
        # Esperar respuesta
        bot_response = laraigo_page.wait_for_bot_response()
        
        # Calcular tiempo de respuesta
        end_time = time.time()
        response_time = end_time - start_time
        
        # Guardar tiempo de respuesta
        response_times[message] = response_time
        
        # Pequeña pausa entre mensajes para evitar sobrecarga
        time.sleep(1)

    # Los datos se almacenan localmente para verificación
    
    # Verificar que todos los tiempos de respuesta están dentro de límites aceptables
    for message, time_taken in response_times.items():
        assert time_taken < 5, f"Tiempo de respuesta demasiado largo para '{message}': {time_taken} segundos"
