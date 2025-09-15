"""
UI functionality tests for the chatbot interface.
Tests the visibility and interaction with UI elements.
"""

import pytest
import time
from pages.chatbot_page import ChatbotPage


class TestChatbotUI:
    """Test class for chatbot UI functionality."""

    @pytest.mark.examples
    def test_open_chat_panel(self, chatbot_page: ChatbotPage):
        """Test que el panel del chat se abre correctamente."""
        # Verificar que inicialmente está cerrado
        assert (
            not chatbot_page.is_chat_panel_visible()
        ), "El panel de chat debería estar cerrado inicialmente"

        # Abrir el chat
        chatbot_page.open_chat()
        assert (
            chatbot_page.is_chat_panel_visible()
        ), "El panel de chat debería estar visible después de abrirlo"

    @pytest.mark.examples
    def test_close_chat_panel(self, chatbot_page: ChatbotPage):
        """Test que el panel del chat se cierra correctamente."""
        chatbot_page.reset_state()

        # Verificar que inicialmente está cerrado
        assert (
            not chatbot_page.is_chat_panel_visible()
        ), "El panel de chat debería estar cerrado inicialmente"

        # Abrir el chat
        chatbot_page.open_chat()
        assert (
            chatbot_page.is_chat_panel_visible()
        ), "El panel de chat debería estar visible después de abrirlo"

        # Cerrar el chat
        chatbot_page.close_chat()
        assert (
            not chatbot_page.is_chat_panel_visible()
        ), "El panel de chat debería estar cerrado después de cerrarlo"

    @pytest.mark.examples
    def test_send_button_functionality(self, chatbot_page: ChatbotPage):
        """Test que el botón de enviar funciona correctamente."""
        # Abrir el chat
        chatbot_page.open_chat()

        # Verificar que el botón de enviar está habilitado
        assert (
            chatbot_page.is_send_button_enabled()
        ), "El botón de enviar debería estar habilitado"

        # Enviar un mensaje
        test_message = "Hola, esto es un test"
        chatbot_page.send_message(test_message)

        # Verificar que el mensaje se ha enviado (aparece en la lista de mensajes del usuario)
        user_messages = chatbot_page.get_all_user_messages()
        assert (
            test_message in user_messages
        ), "El mensaje del usuario debería aparecer en el chat"

    @pytest.mark.examples
    def test_enter_key_send(self, chatbot_page: ChatbotPage):
        """Test que la tecla Enter funciona para enviar mensajes."""
        # Abrir el chat
        chatbot_page.open_chat()

        # Enviar un mensaje usando Enter
        test_message = "Mensaje enviado con Enter"
        chatbot_page.send_message_with_enter(test_message)

        # Verificar que el mensaje se ha enviado
        user_messages = chatbot_page.get_all_user_messages()
        assert (
            test_message in user_messages
        ), "El mensaje enviado con Enter debería aparecer en el chat"

    @pytest.mark.examples
    def test_bot_response(self, chatbot_page: ChatbotPage, request, test_data):
        """Test que el bot responde a los mensajes."""
        # Abrir el chat
        chatbot_page.open_chat()

        # Enviar un mensaje y esperar respuesta
        test_message = "Hola"
        start_time = time.time()
        chatbot_page.send_message(test_message)

        # Esperar y verificar que hay respuesta del bot
        response = chatbot_page.wait_for_bot_response()
        response_time = time.time() - start_time
        assert response, "Debería haber una respuesta del bot"

        # Save test data for reporting
        test_data(sent_message=test_message, response_text=response, response_time=response_time)

        # Verificar que la respuesta se añadió a la lista de mensajes del bot
        bot_messages = chatbot_page.get_all_bot_messages()
        assert len(bot_messages) > 0, "Debería haber al menos un mensaje del bot"

    @pytest.mark.examples
    def test_reset_chat_for_specific_test(self, chatbot_page: ChatbotPage):
        """Test que demuestra cómo reiniciar la instancia del chatbot para un test específico."""
        # Primero realizamos algunas acciones que podrían afectar el estado
        chatbot_page.open_chat()
        chatbot_page.send_message("Mensaje inicial")

        # Ahora reiniciamos el estado del chat para este test específico
        chatbot_page.reset_state()

        # Verificamos que el chat está cerrado después del reinicio
        assert (
            not chatbot_page.is_chat_panel_visible()
        ), "El panel de chat debería estar cerrado después del reinicio"

        # Realizamos nuevas acciones con un estado limpio
        chatbot_page.open_chat()
        chatbot_page.send_message("Mensaje después del reinicio")

        # Verificamos que solo existe el mensaje enviado después del reinicio
        user_messages = chatbot_page.get_all_user_messages()
        assert (
            len(user_messages) == 1
        ), "Debería haber solo un mensaje después de reiniciar"
        assert (
            "Mensaje después del reinicio" in user_messages
        ), "El mensaje después del reinicio debería estar en el chat"

    @pytest.mark.examples
    def test_multiple_messages_conversation(self, chatbot_page: ChatbotPage, request, test_data):
        """Test que verifica una conversación con múltiples mensajes."""
        # Abrir el chat
        chatbot_page.open_chat()

        # Enviar múltiples mensajes
        messages = ["Hola", "¿Cómo estás?", "Necesito ayuda"]
        
        # Registramos el tiempo para el diálogo completo
        start_time = time.time()
        all_responses = []

        for message in messages:
            chatbot_page.send_message(message)
            # Esperar respuesta después de cada mensaje
            response = chatbot_page.wait_for_bot_response()
            if response:
                all_responses.append(response)

        response_time = time.time() - start_time

        # Save test data for reporting (último mensaje y última respuesta)
        last_message = messages[-1] if messages else ""
        last_response = all_responses[-1] if all_responses else None
        test_data(sent_message=last_message, response_text=last_response, response_time=response_time)

        # Verificar que todos los mensajes del usuario están en el chat
        user_messages = chatbot_page.get_all_user_messages()
        for message in messages:
            assert (
                message in user_messages
            ), f"El mensaje '{message}' debería estar en el chat"

        # Verificar que hay respuestas del bot para cada mensaje
        bot_messages = chatbot_page.get_all_bot_messages()
        assert len(bot_messages) >= len(
            messages
        ), "Debería haber al menos una respuesta del bot por cada mensaje del usuario"
