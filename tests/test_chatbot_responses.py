"""
Response validation tests for the chatbot interface.
Tests the accuracy and relevance of chatbot responses.
"""

import pytest
import time
from pages.chatbot_page import ChatbotPage


@pytest.mark.responses
@pytest.mark.parametrize(
    "greeting", ["Hola", "Buenos días", "Buenas tardes", "Buenas noches"]
)
def test_greeting_responses(driver, chatbot_page, greeting):
    """TC-RESP-001: Verify that the bot responds appropriately to greetings."""

    # Open chat
    chatbot_page.open_chat()

    # Send greeting
    start_time = time.time()
    chatbot_page.send_message(greeting)
    assert (
        greeting in chatbot_page.get_all_user_messages()
    ), "User message not displayed in chat"
    bot_response = chatbot_page.wait_for_bot_response()
    response_time = time.time() - start_time

    # Make the chatbot_page available to the test report hook
    pytest.chatbot_page = chatbot_page
    pytest.sent_message = greeting
    pytest.response_text = bot_response
    pytest.response_time = response_time

    # Verify bot responds with a greeting
    assert any(
        word in bot_response.lower()
        for word in ["hola", "bienvenido", "saludos", "ayudar"]
    ), f"Bot did not respond appropriately to greeting: {greeting}"


@pytest.mark.responses
@pytest.mark.parametrize("query", ["¿Cuánto cuesta?", "Precios", "Valor del servicio"])
def test_price_inquiry_responses(driver, chatbot_page, query):
    """TC-RESP-002: Verify that the bot responds to price inquiries."""

    # Open chat
    chatbot_page.open_chat()

    # Ask about prices
    start_time = time.time()
    chatbot_page.send_message(query)
    assert (
        query in chatbot_page.get_all_user_messages()
    ), "User message not displayed in chat"
    bot_response = chatbot_page.wait_for_bot_response()
    response_time = time.time() - start_time

    # Make the chatbot_page available to the test report hook
    pytest.chatbot_page = chatbot_page
    pytest.sent_message = query
    pytest.response_text = bot_response
    pytest.response_time = response_time

    # Verify bot mentions prices or refers to sales
    assert any(
        word in bot_response.lower()
        for word in ["precio", "costo", "valor", "plan", "paquete", "ventas"]
    ), f"Bot did not respond appropriately to price query: {query}"


@pytest.mark.responses
@pytest.mark.parametrize(
    "query",
    [
        "¿Qué servicios ofrecen?",
        "Explícame tus productos",
        "asdasdasdas",
    ],
)
def test_product_service_info_responses(driver, chatbot_page, query):
    """TC-RESP-003: Verify that the bot provides product/service information."""

    # Open chat
    chatbot_page.open_chat()

    # Ask about products/services
    start_time = time.time()
    chatbot_page.send_message(query)
    assert (
        query in chatbot_page.get_all_user_messages()
    ), "User message not displayed in chat"
    bot_response = chatbot_page.wait_for_bot_response()
    response_time = time.time() - start_time

    # Make the chatbot_page available to the test report hook
    pytest.chatbot_page = chatbot_page
    pytest.sent_message = query
    pytest.response_text = bot_response
    pytest.response_time = response_time

    # Verify bot mentions products or services
    assert any(
        word in bot_response.lower()
        for word in ["servicio", "producto", "ofrecemos", "plataforma", "solución"]
    ), f"Bot did not respond with product/service information to: {query}"


@pytest.mark.responses
@pytest.mark.parametrize(
    "query",
    [
        "¿Cómo puedo contactarlos?",
        "Datos de contacto",
        "¿Tienen un número de teléfono?",
    ],
)
def test_contact_info_responses(driver, chatbot_page, query):
    """TC-RESP-004: Verify that the bot provides contact information when requested."""

    # Open chat
    chatbot_page.open_chat()

    # Ask about contact information
    start_time = time.time()
    chatbot_page.send_message(query)
    assert (
        query in chatbot_page.get_all_user_messages()
    ), "User message not displayed in chat"
    bot_response = chatbot_page.wait_for_bot_response()
    response_time = time.time() - start_time

    # Make the chatbot_page available to the test report hook
    pytest.chatbot_page = chatbot_page
    pytest.sent_message = query
    pytest.response_text = bot_response
    pytest.response_time = response_time

    # Verify bot provides contact information
    assert any(
        word in bot_response.lower()
        for word in ["contacto", "email", "correo", "teléfono", "llamar", "comunicarse"]
    ), f"Bot did not provide contact information in response to: {query}"
