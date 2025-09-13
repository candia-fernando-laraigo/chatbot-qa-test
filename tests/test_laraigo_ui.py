"""
UI functionality tests for the Laraigo chatbot interface.
Tests the visibility and interaction with UI elements.
"""

import pytest
from pages.laraigo_page import LaraigoPage


@pytest.fixture
def laraigo_page(driver):
    """Fixture para crear una instancia de LaraigoPage que se reutiliza en los tests."""
    return LaraigoPage(driver)


class TestLaraigoUI:
    """Test class for Laraigo chatbot UI functionality."""

    @pytest.mark.laraigo
    def test_open_chat_window(self, laraigo_page: LaraigoPage):
        """Test que la ventana del chat se abre correctamente."""
        # Verificar que inicialmente está cerrada
        assert (
            not laraigo_page.is_chat_window_visible()
        ), "La ventana de chat debería estar cerrada inicialmente"

        # Abrir el chat
        laraigo_page.open_chat()
        assert (
            laraigo_page.is_chat_window_visible()
        ), "La ventana de chat debería estar visible después de abrirla"

    @pytest.mark.laraigo
    def test_enter_key_send(self, laraigo_page: LaraigoPage):
        """Test que la tecla Enter funciona para enviar mensajes."""
        # Abrir el chat
        laraigo_page.open_chat()

        # Enviar un mensaje usando Enter
        test_message = "Mensaje enviado con Enter"
        laraigo_page.send_message(test_message)

        # Verificar que el mensaje se ha enviado
        user_messages = laraigo_page.get_all_user_messages_text()
        assert (
            test_message in user_messages
        ), "El mensaje enviado con Enter debería aparecer en el chat"

    @pytest.mark.laraigo
    def test_bot_response(self, laraigo_page: LaraigoPage):
        """Test que el bot responde a los mensajes."""
        # Abrir el chat
        laraigo_page.open_chat()

        # Enviar un mensaje y esperar respuesta
        response = laraigo_page.send_message("Hola")

        assert response, "Debería haber una respuesta del bot"

        # Verificar que la respuesta se añadió a la lista de mensajes del bot
        bot_messages = laraigo_page.get_all_bot_messages_text()
        assert len(bot_messages) > 0, "Debería haber al menos un mensaje del bot"

    @pytest.mark.laraigo
    def test_refresh_chat(self, laraigo_page: LaraigoPage):
        """Test que verifica que el botón de refrescar el chat funciona correctamente."""
        # Abrir el chat
        laraigo_page.open_chat()

        # Enviar un mensaje para asegurarnos de que hay contenido
        laraigo_page.send_message("Mensaje antes de refrescar")

        user_messages_before = laraigo_page.get_all_user_messages_text()
        bot_messages_before = laraigo_page.get_all_bot_messages_text()

        assert (
            len(user_messages_before) == 1
        ), "Debería haber un mensaje del usuario antes de refrescar"
        assert (
            len(bot_messages_before) > 0
        ), "Debería haber al menos un mensaje del bot antes de refrescar"

        # Refrescar el chat
        laraigo_page.refresh_chat()

        # Comprobar que los mensajes siguen siendo los mismos después de refrescar
        # Nota: Esto supone que refresh_chat() simplemente refresca la interfaz sin borrar mensajes
        user_messages_after = laraigo_page.get_all_user_messages_text()
        bot_messages_after = laraigo_page.get_all_bot_messages_text()

        assert (
            len(user_messages_after) == 0
        ), "El número de mensajes del usuario debería ser cero después de refrescar"
        assert (
            len(bot_messages_after) == 0
        ), "El número de mensajes del bot debería ser cero después de refrescar"

    @pytest.mark.laraigo
    def test_attachments_menu(self, laraigo_page: LaraigoPage):
        """Test que verifica la funcionalidad del menú de adjuntos."""
        # Abrir el chat
        laraigo_page.open_chat()

        # Verificar que el menú de adjuntos inicialmente no está visible
        assert (
            not laraigo_page.is_attachments_menu_visible()
        ), "El menú de adjuntos no debería estar visible inicialmente"

        # Abrir el menú de adjuntos
        laraigo_page.open_attachments_menu()

        # Verificar que el menú de adjuntos ahora está visible
        assert (
            laraigo_page.is_attachments_menu_visible()
        ), "El menú de adjuntos debería estar visible después de abrirlo"

        # Cerrar el menú de adjuntos
        laraigo_page.close_attachments_menu()

        # Verificar que el menú de adjuntos ahora está cerrado
        assert (
            not laraigo_page.is_attachments_menu_visible()
        ), "El menú de adjuntos debería estar cerrado después de cerrarlo"

    @pytest.mark.laraigo
    def test_multiple_messages_conversation(self, laraigo_page: LaraigoPage):
        """Test que verifica una conversación con múltiples mensajes."""
        # Abrir el chat
        laraigo_page.open_chat()

        # Enviar múltiples mensajes
        messages = ["Hola", "¿Cómo estás?", "Necesito ayuda"]

        for message in messages:
            laraigo_page.send_message(message)

        # Verificar que todos los mensajes del usuario están en el chat
        user_messages = laraigo_page.get_all_user_messages_text()
        for message in messages:
            assert (
                message in user_messages
            ), f"El mensaje '{message}' debería estar en el chat"

        # Verificar que hay respuestas del bot para cada mensaje
        bot_messages = laraigo_page.get_all_bot_messages_text()
        assert len(bot_messages) >= len(
            messages
        ), "Debería haber al menos una respuesta del bot por cada mensaje del usuario"

    @pytest.mark.laraigo
    def test_reset_chat_state(self, laraigo_page: LaraigoPage):
        """Test que demuestra cómo reiniciar la instancia del chatbot para un test específico."""
        # Primero realizamos algunas acciones que podrían afectar el estado
        msg_before_reset = "Mensaje antes del reinicio"
        laraigo_page.open_chat()
        laraigo_page.send_message(msg_before_reset)

        # Ahora reiniciamos el estado del chat para este test específico
        laraigo_page.reset_state()

        # Verificamos que el chat está cerrado después del reinicio
        assert (
            not laraigo_page.is_chat_window_visible()
        ), "La ventana de chat debería estar cerrada después del reinicio"

        # Realizamos nuevas acciones con un estado limpio
        laraigo_page.open_chat()
        assert (
            laraigo_page.is_chat_window_visible()
        ), "La ventana de chat debería estar visible después de abrirla tras el reinicio"

        # Verificamos que solo existe el mensaje enviado después del reinicio
        user_messages = laraigo_page.get_all_user_messages_text()
        assert (
            len(user_messages) == 1
        ), f"Debería haber un mensaje después de reiniciar, pero hay {len(user_messages)}: {user_messages}"
        assert (
            msg_before_reset in user_messages
        ), f"El mensaje '{msg_before_reset}' debería estar en el chat. Mensajes actuales: {user_messages}"

    @pytest.mark.laraigo
    def test_idle_message_visibility(self, laraigo_page: LaraigoPage):
        """Test que verifica la visibilidad y el ocultamiento del mensaje de inactividad."""
        # Este test asume que el mensaje de inactividad aparece después de un tiempo
        # Si es necesario, implementar un mecanismo para forzar su aparición

        # Abrir el chat
        laraigo_page.open_chat()

        # Si el mensaje de inactividad está visible, ocultarlo
        if laraigo_page.is_idle_message_visible():
            laraigo_page.hide_idle_message()

            # Verificar que el mensaje de inactividad ya no está visible
            assert (
                not laraigo_page.is_idle_message_visible()
            ), "El mensaje de inactividad debería estar oculto después de ocultarlo"
