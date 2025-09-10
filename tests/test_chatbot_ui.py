"""
UI functionality tests for the chatbot interface.
Tests the visibility and interaction with UI elements.
"""

import pytest
from pages.chatbot_page import ChatbotPage


@pytest.fixture
def chatbot_page(driver):
    """Fixture para crear una instancia de ChatbotPage que se reutiliza en los tests."""
    return ChatbotPage(driver)


class TestChatbotUI:
    """Test class for chatbot UI functionality."""

    @pytest.mark.ui
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

    @pytest.mark.ui
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

    @pytest.mark.ui
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

    @pytest.mark.ui
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

    @pytest.mark.ui
    def test_bot_response(self, chatbot_page: ChatbotPage):
        """Test que el bot responde a los mensajes."""
        # Abrir el chat
        chatbot_page.open_chat()

        # Enviar un mensaje y esperar respuesta
        chatbot_page.send_message("Hola")

        # Esperar y verificar que hay respuesta del bot
        response = chatbot_page.wait_for_bot_response()
        assert response, "Debería haber una respuesta del bot"

        # Verificar que la respuesta se añadió a la lista de mensajes del bot
        bot_messages = chatbot_page.get_all_bot_messages()
        assert len(bot_messages) > 0, "Debería haber al menos un mensaje del bot"

    @pytest.mark.ui
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

    @pytest.mark.ui
    def test_multiple_messages_conversation(self, chatbot_page: ChatbotPage):
        """Test que verifica una conversación con múltiples mensajes."""
        # Abrir el chat
        chatbot_page.open_chat()

        # Enviar múltiples mensajes
        messages = ["Hola", "¿Cómo estás?", "Necesito ayuda"]

        for message in messages:
            chatbot_page.send_message(message)
            # Esperar respuesta después de cada mensaje
            chatbot_page.wait_for_bot_response()

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
