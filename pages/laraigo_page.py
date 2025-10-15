"""
Page Object Model para la interfaz del chatbot Laraigo.
Proporciona métodos para interactuar con los elementos específicos del chatbot de Laraigo.
"""

from typing import List
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    WebDriverException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
import time

from config.config import PAGE_URL, PAGE_TIMEOUT

class LaraigoPage:
    """Page Object Model para la interfaz del chatbot Laraigo."""

    # Locators específicos para el chatbot de Laraigo
    CHAT_OPEN_BUTTON = (By.ID, "chat-open-chatweb")
    CHAT_WINDOW = (By.ID, "chat-window")
    CHAT_CLOSE_BUTTON = (By.CLASS_NAME, "header-close-button-chatweb")
    CHAT_REFRESH_BUTTON = (By.ID, "chat-history-refresh")
    CHAT_INPUT = (By.ID, "chat-input-chatweb")
    CHAT_HISTORY = (By.ID, "chat-history-chatweb")
    BOT_MESSAGES = (By.CSS_SELECTOR, ".chat-message-chatweb-bot p")
    USER_MESSAGES = (By.CSS_SELECTOR, ".chat-message-chatweb-user p")
    LAST_BOT_MESSAGE = (By.CSS_SELECTOR, ".lastbot .chat-message-chatweb-bot p")
    LAST_USER_MESSAGE = (By.CSS_SELECTOR, ".lastuser .chat-message-chatweb-user p")
    ATTACHMENTS_BUTTON = (By.ID, "input-attach-button-show")
    ATTACHMENTS_MENU = (By.ID, "attachmentmenu")
    ATTACHMENT_IMAGE = (By.ID, "input-image-button")
    ATTACHMENT_FILE = (By.ID, "input-file-button")
    ATTACHMENT_AUDIO = (By.ID, "input-audio-button")
    ATTACHMENT_VIDEO = (By.ID, "input-video-button")
    ATTACHMENT_LOCATION = (By.ID, "input-location-button")
    CHAT_IDLE_MESSAGE = (By.ID, "chat-idle-message")

    def __init__(self, driver: WebDriver, timeout: int = PAGE_TIMEOUT):
        """Inicializar la página con el WebDriver proporcionado y un timeout personalizable."""
        self.driver: WebDriver = driver
        self.wait: WebDriverWait = WebDriverWait(driver, timeout)
        self.timeout = timeout

        try:
            self.driver.get(PAGE_URL)
        except WebDriverException as e:
            raise WebDriverException(f"No se pudo cargar la página: {e}")
        except Exception as e:
            raise Exception(f"Error inesperado al cargar la página: {e}")

    def wait_for_page_load(self) -> "LaraigoPage":
        """Esperar a que la página cargue completamente."""
        try:
            self.wait.until(EC.presence_of_element_located(self.CHAT_OPEN_BUTTON))
            return self
        except TimeoutException:
            raise TimeoutException(
                f"La página no cargó completamente dentro de {self.timeout} segundos."
            )

    def open_chat(self) -> "LaraigoPage":
        """Abrir la ventana del chat haciendo clic en el botón de chat."""
        try:
            # Esperar a que el botón de chat esté disponible
            self.wait.until(EC.element_to_be_clickable(self.CHAT_OPEN_BUTTON))
            open_button: WebElement = self.driver.find_element(*self.CHAT_OPEN_BUTTON)

            # Verificar si el chat ya está abierto
            if not self.is_chat_window_visible():
                open_button.click()
                # Esperar a que la ventana del chat sea visible
                self.wait.until(EC.visibility_of_element_located(self.CHAT_WINDOW))

            return self
        except TimeoutException:
            raise TimeoutException(
                f"El botón del chat ('chat-open-chatweb') no se volvió interactivo dentro de {self.timeout} segundos."
            )
        except NoSuchElementException:
            raise NoSuchElementException(
                "No se encontró el botón del chat ('chat-open-chatweb')."
            )

    def close_chat(self) -> "LaraigoPage":
        """Cerrar la ventana del chat."""
        try:
            if self.is_chat_window_visible():
                close_button: WebElement = self.driver.find_element(
                    *self.CHAT_CLOSE_BUTTON
                )
                close_button.click()
                # Esperar a que la ventana del chat no sea visible
                self.wait.until(EC.invisibility_of_element_located(self.CHAT_WINDOW))

            return self
        except TimeoutException:
            raise TimeoutException(
                f"La ventana del chat no se cerró dentro de {self.timeout} segundos."
            )
        except NoSuchElementException:
            raise NoSuchElementException("No se encontró el botón de cierre del chat.")

    def refresh_chat(self) -> "LaraigoPage":
        """Refrescar el historial del chat."""
        try:
            if self.is_chat_window_visible():
                refresh_button: WebElement = self.driver.find_element(
                    *self.CHAT_REFRESH_BUTTON
                )
                refresh_button.click()
                # Esperar un momento para que se refresque
                time.sleep(1)
            return self
        except NoSuchElementException:
            raise NoSuchElementException(
                "No se encontró el botón de actualización del chat."
            )

    def send_message(self, message: str) -> List[str]:
        """
        Enviar un mensaje al chatbot y esperar su respuesta.

        Esta función es atómica: maneja tanto el envío del mensaje como la captura
        de la respuesta del bot en una sola operación.

        Args:
            message: El mensaje a enviar

        Returns:
            Lista con los textos de las respuestas nuevas del bot
        """
        try:
            if not self.is_chat_window_visible():
                self.open_chat()

            # Esperar a que el campo de entrada esté disponible
            self.wait.until(EC.element_to_be_clickable(self.CHAT_INPUT))
            chat_input: WebElement = self.driver.find_element(*self.CHAT_INPUT)

            msg_bot_count = len(self.get_all_bot_messages())
            # Limpiar el campo y escribir el mensaje
            chat_input.clear()
            chat_input.send_keys(message)
            chat_input.send_keys(Keys.RETURN)

            # Esperar a que el mensaje del usuario aparezca en el historial
            self.wait.until(lambda _: message in self.get_all_user_messages_text())
        except TimeoutException:
            raise TimeoutException(
                f"No se pudo enviar el mensaje dentro de {self.timeout} segundos."
            )
        except NoSuchElementException:
            raise NoSuchElementException(
                "No se encontraron los elementos necesarios para enviar un mensaje."
            )

        try:
            self.wait.until(lambda _: len(self.get_all_bot_messages()) > msg_bot_count)
            new_bot_messages = self.get_all_bot_messages()[msg_bot_count:]
            return [msg.text for msg in new_bot_messages]
        except TimeoutException:
            raise TimeoutException(
                f"No se recibió una respuesta del bot dentro de {self.timeout} segundos."
            )
        except NoSuchElementException:
            raise NoSuchElementException(
                "No se encontraron los mensajes del bot después de enviar el mensaje."
            )

    def is_chat_window_visible(self) -> bool:
        """Verificar si la ventana del chat está visible."""
        try:
            chat_window: WebElement = self.driver.find_element(*self.CHAT_WINDOW)
            return chat_window.is_displayed()
        except NoSuchElementException:
            return False

    def is_chat_button_visible(self) -> bool:
        """Verificar si el botón del chat está visible."""
        try:
            chat_button: WebElement = self.driver.find_element(*self.CHAT_OPEN_BUTTON)
            return chat_button.is_displayed()
        except NoSuchElementException:
            return False

    def get_all_bot_messages(self) -> List[WebElement]:
        """Obtener una lista de todos los elementos de mensajes del bot."""
        return self.driver.find_elements(*self.BOT_MESSAGES)

    def get_all_bot_messages_text(self) -> List[str]:
        """Obtener una lista con el texto de todos los mensajes del bot."""
        elements = self.get_all_bot_messages()
        return [element.text for element in elements]

    def get_all_user_messages(self) -> List[WebElement]:
        """Obtener una lista de todos los elementos de mensajes del usuario."""
        return self.driver.find_elements(*self.USER_MESSAGES)

    def get_all_user_messages_text(self) -> List[str]:
        """Obtener una lista con el texto de todos los mensajes del usuario."""
        elements = self.get_all_user_messages()
        return [element.text for element in elements]

    def get_chat_history(self) -> WebElement:
        """Obtener el elemento que contiene el historial del chat."""
        try:
            return self.driver.find_element(*self.CHAT_HISTORY)
        except NoSuchElementException:
            raise NoSuchElementException("No se encontró el historial del chat.")

    def open_attachments_menu(self) -> "LaraigoPage":
        """Abrir el menú de adjuntos."""
        try:
            if self.is_chat_window_visible():
                attach_button: WebElement = self.driver.find_element(
                    *self.ATTACHMENTS_BUTTON
                )
                attach_button.click()
                # Esperar a que el menú de adjuntos sea visible
                self.wait.until(EC.visibility_of_element_located(self.ATTACHMENTS_MENU))
            return self
        except TimeoutException:
            raise TimeoutException(
                f"El menú de adjuntos no se volvió visible dentro de {self.timeout} segundos."
            )
        except NoSuchElementException:
            raise NoSuchElementException("No se encontró el botón de adjuntos.")

    def close_attachments_menu(self) -> "LaraigoPage":
        """Cerrar el menú de adjuntos haciendo clic fuera de él."""
        try:
            if self.is_attachments_menu_visible():
                # Hacer clic en el campo de entrada para cerrar el menú
                chat_input: WebElement = self.driver.find_element(*self.CHAT_INPUT)
                chat_input.click()
                # Esperar a que el menú de adjuntos no sea visible
                self.wait.until(
                    EC.invisibility_of_element_located(self.ATTACHMENTS_MENU)
                )
            return self
        except TimeoutException:
            raise TimeoutException(
                f"El menú de adjuntos no se cerró dentro de {self.timeout} segundos."
            )

    def is_attachments_menu_visible(self) -> bool:
        """Verificar si el menú de adjuntos está visible."""
        try:
            attachments_menu: WebElement = self.driver.find_element(
                *self.ATTACHMENTS_MENU
            )
            return attachments_menu.is_displayed()
        except NoSuchElementException:
            return False

    def upload_image(self, file_path: str) -> "LaraigoPage":
        """Subir una imagen como adjunto."""
        try:
            if not self.is_attachments_menu_visible():
                self.open_attachments_menu()

            image_input: WebElement = self.driver.find_element(*self.ATTACHMENT_IMAGE)
            image_input.send_keys(file_path)

            # Cerrar el menú de adjuntos después de subir
            self.close_attachments_menu()
            return self
        except NoSuchElementException:
            raise NoSuchElementException("No se encontró el campo para subir imágenes.")

    def upload_file(self, file_path: str) -> "LaraigoPage":
        """Subir un archivo como adjunto."""
        try:
            if not self.is_attachments_menu_visible():
                self.open_attachments_menu()

            file_input: WebElement = self.driver.find_element(*self.ATTACHMENT_FILE)
            file_input.send_keys(file_path)

            # Cerrar el menú de adjuntos después de subir
            self.close_attachments_menu()
            return self
        except NoSuchElementException:
            raise NoSuchElementException("No se encontró el campo para subir archivos.")

    def upload_audio(self, file_path: str) -> "LaraigoPage":
        """Subir un audio como adjunto."""
        try:
            if not self.is_attachments_menu_visible():
                self.open_attachments_menu()

            audio_input: WebElement = self.driver.find_element(*self.ATTACHMENT_AUDIO)
            audio_input.send_keys(file_path)

            # Cerrar el menú de adjuntos después de subir
            self.close_attachments_menu()
            return self
        except NoSuchElementException:
            raise NoSuchElementException("No se encontró el campo para subir audios.")

    def upload_video(self, file_path: str) -> "LaraigoPage":
        """Subir un video como adjunto."""
        try:
            if not self.is_attachments_menu_visible():
                self.open_attachments_menu()

            video_input: WebElement = self.driver.find_element(*self.ATTACHMENT_VIDEO)
            video_input.send_keys(file_path)

            # Cerrar el menú de adjuntos después de subir
            self.close_attachments_menu()
            return self
        except NoSuchElementException:
            raise NoSuchElementException("No se encontró el campo para subir videos.")

    def share_location(self) -> "LaraigoPage":
        """Compartir la ubicación."""
        try:
            if not self.is_attachments_menu_visible():
                self.open_attachments_menu()

            location_button: WebElement = self.driver.find_element(
                *self.ATTACHMENT_LOCATION
            )
            location_button.click()

            # No cerramos el menú porque el propio botón ya lo cierra
            return self
        except NoSuchElementException:
            raise NoSuchElementException(
                "No se encontró el botón para compartir ubicación."
            )

    def is_idle_message_visible(self) -> bool:
        """Verificar si el mensaje de inactividad está visible."""
        try:
            idle_message: WebElement = self.driver.find_element(*self.CHAT_IDLE_MESSAGE)
            return idle_message.is_displayed()
        except NoSuchElementException:
            return False

    def hide_idle_message(self) -> "LaraigoPage":
        """Ocultar el mensaje de inactividad."""
        try:
            if self.is_idle_message_visible():
                idle_message: WebElement = self.driver.find_element(
                    *self.CHAT_IDLE_MESSAGE
                )
                close_button = idle_message.find_element(
                    By.CLASS_NAME, "speech-bubble-times"
                )
                close_button.click()
                # Esperar a que el mensaje de inactividad no sea visible
                self.wait.until(
                    EC.invisibility_of_element_located(self.CHAT_IDLE_MESSAGE)
                )
            return self
        except NoSuchElementException:
            return self  # Si no hay mensaje de inactividad, no hay problema

    def reset_state(self) -> "LaraigoPage":
        """
        Reiniciar el estado del chat a su estado inicial.

        Útil para pruebas que necesitan un estado limpio del chat.
        """
        try:
            self.driver.refresh()
            # Esperar a que la página se cargue completamente después de refrescar
            self.wait.until(EC.presence_of_element_located(self.CHAT_OPEN_BUTTON))
            return self
        except TimeoutException:
            raise TimeoutException(
                f"La página no se recargó correctamente dentro de {self.timeout} segundos."
            )
        except Exception as e:
            print(f"Error al reiniciar el estado del chat: {e}")
            raise
