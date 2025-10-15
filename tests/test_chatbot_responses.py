"""
Response validation tests for the simple-web demo chatbot.
Each test creates its own ChatbotPage for clarity and easy extension.
"""

import pytest
import time
from pages.chatbot_page import ChatbotPage


@pytest.mark.examples
@pytest.mark.parametrize(
    "greeting", ["Hola", "Buenos días", "Buenas tardes", "Buenas noches"]
)
def test_greeting_responses(driver, greeting, test_data):
    page = ChatbotPage(driver)
    page.open_chat()
    t0 = time.time()
    page.send_message(greeting)
    assert (
        greeting in page.get_all_user_messages()
    ), "User message not displayed in chat"
    bot_response = page.wait_for_bot_response()
    rt = time.time() - t0
    test_data(sent_message=greeting, response_text=bot_response, response_time=rt)
    assert any(
        word in bot_response.lower()
        for word in ["hola", "bienvenido", "saludos", "ayudar"]
    ), f"Bot did not respond appropriately to greeting: {greeting}"


@pytest.mark.examples
@pytest.mark.parametrize("query", ["¿Cuánto cuesta?", "Precios", "Valor del servicio"])
def test_price_inquiry_responses(driver, query, test_data):
    page = ChatbotPage(driver)
    page.open_chat()
    t0 = time.time()
    page.send_message(query)
    assert query in page.get_all_user_messages(), "User message not displayed in chat"
    bot_response = page.wait_for_bot_response()
    rt = time.time() - t0
    test_data(sent_message=query, response_text=bot_response, response_time=rt)
    assert any(
        word in bot_response.lower()
        for word in ["precio", "costo", "valor", "plan", "paquete", "ventas"]
    ), f"Bot did not respond appropriately to price query: {query}"


@pytest.mark.examples
@pytest.mark.parametrize(
    "query",
    [
        "¿Qué servicios ofrecen?",
        "Explícame tus productos",
    ],
)
def test_product_service_info_responses(driver, query, test_data):
    page = ChatbotPage(driver)
    page.open_chat()
    t0 = time.time()
    page.send_message(query)
    assert query in page.get_all_user_messages(), "User message not displayed in chat"
    bot_response = page.wait_for_bot_response()
    rt = time.time() - t0
    test_data(sent_message=query, response_text=bot_response, response_time=rt)
    assert any(
        word in bot_response.lower()
        for word in ["servicio", "producto", "ofrecemos", "plataforma", "solución"]
    ), f"Bot did not respond with product/service information to: {query}"


@pytest.mark.examples
@pytest.mark.parametrize(
    "query",
    [
        "¿Cómo puedo contactarlos?",
        "Datos de contacto",
        "¿Tienen un número de teléfono?",
    ],
)
def test_contact_info_responses(driver, query, test_data):
    page = ChatbotPage(driver)
    page.open_chat()
    t0 = time.time()
    page.send_message(query)
    assert query in page.get_all_user_messages(), "User message not displayed in chat"
    bot_response = page.wait_for_bot_response()
    rt = time.time() - t0
    test_data(sent_message=query, response_text=bot_response, response_time=rt)
    assert any(
        word in bot_response.lower()
        for word in ["contacto", "email", "correo", "teléfono", "llamar", "comunicarse"]
    ), f"Bot did not provide contact information in response to: {query}"
