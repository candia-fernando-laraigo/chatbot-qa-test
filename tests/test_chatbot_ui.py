"""
UI functionality tests for the chatbot interface (simple-web).
Each test instantiates its own ChatbotPage to keep things simple.
"""

import pytest
import time
from pages.chatbot_page import ChatbotPage


@pytest.mark.examples
def test_open_chat_panel(driver):
    page = ChatbotPage(driver)
    assert not page.is_chat_panel_visible(), "El panel debería iniciar cerrado"
    page.open_chat()
    assert (
        page.is_chat_panel_visible()
    ), "El panel debería estar visible tras abrirlo"

@pytest.mark.examples
def test_close_chat_panel(driver):
    page = ChatbotPage(driver)
    page.reset_state()
    assert not page.is_chat_panel_visible(), "El panel debería iniciar cerrado"
    page.open_chat()
    assert page.is_chat_panel_visible(), "Debe estar visible tras abrir"
    page.close_chat()
    assert not page.is_chat_panel_visible(), "Debe estar cerrado tras cerrar"

@pytest.mark.examples
def test_send_button_functionality(driver):
    page = ChatbotPage(driver)
    page.open_chat()
    assert page.is_send_button_enabled(), "El botón enviar debe estar habilitado"
    msg = "Hola, esto es un test"
    page.send_message(msg)
    assert (
        msg in page.get_all_user_messages()
    ), "El mensaje debería aparecer en el chat"

@pytest.mark.examples
def test_enter_key_send(driver):
    page = ChatbotPage(driver)
    page.open_chat()
    msg = "Mensaje enviado con Enter"
    page.send_message_with_enter(msg)
    assert (
        msg in page.get_all_user_messages()
    ), "El mensaje debería aparecer en el chat"

@pytest.mark.examples
def test_bot_response(driver, test_data):
    page = ChatbotPage(driver)
    page.open_chat()
    msg = "Hola"
    t0 = time.time()
    page.send_message(msg)
    resp = page.wait_for_bot_response()
    rt = time.time() - t0
    assert resp, "Debería haber una respuesta del bot"
    test_data(sent_message=msg, response_text=resp, response_time=rt)
    assert (
        len(page.get_all_bot_messages()) > 0
    ), "Debe haber al menos un mensaje del bot"

@pytest.mark.examples
def test_reset_chat_for_specific_test(driver):
    page = ChatbotPage(driver)
    page.open_chat()
    page.send_message("Mensaje inicial")
    page.reset_state()
    assert not page.is_chat_panel_visible(), "Debe estar cerrado tras reset"
    page.open_chat()
    page.send_message("Mensaje después del reinicio")
    users = page.get_all_user_messages()
    assert len(users) == 1
    assert "Mensaje después del reinicio" in users

@pytest.mark.examples
def test_multiple_messages_conversation(driver, test_data):
    page = ChatbotPage(driver)
    page.open_chat()
    messages = ["Hola", "¿Cómo estás?", "Necesito ayuda"]
    t0 = time.time()
    responses = []
    for m in messages:
        page.send_message(m)
        r = page.wait_for_bot_response()
        if r:
            responses.append(r)
    rt = time.time() - t0
    last_message = messages[-1] if messages else ""
    last_response = responses[-1] if responses else None
    test_data(
        sent_message=last_message, response_text=last_response, response_time=rt
    )
    users = page.get_all_user_messages()
    for m in messages:
        assert m in users
    assert len(page.get_all_bot_messages()) >= len(messages)
