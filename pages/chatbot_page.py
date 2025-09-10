"""
Page Object Model for the chatbot interface elements.
"""

from typing import List, Optional
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotVisibleException,
    WebDriverException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver


class ChatbotPage:
    """Page Object Model for the Chatbot interface."""

    # Locators
    CHAT_TOGGLE_BUTTON = (By.ID, "chat-toggle-button")
    CHAT_PANEL = (By.ID, "chat-panel")
    CHAT_HEADER = (By.ID, "chat-header")
    CHAT_DISPLAY = (By.ID, "chat-display")
    CHAT_INPUT = (By.ID, "chat-input")
    SEND_BUTTON = (By.ID, "send-button")
    BOT_MESSAGES = (
        By.XPATH,
        "//div[@id='chat-display']/div[contains(@class, 'bot-message')]",
    )
    USER_MESSAGES = (
        By.XPATH,
        "//div[@id='chat-display']/div[contains(@class, 'user-message')]",
    )
    LAST_BOT_MESSAGE = (
        By.XPATH,
        "//div[@id='chat-display']/div[contains(@class, 'bot-message')][last()]",
    )

    def __init__(self, driver: WebDriver):
        """Initialize the page with the provided WebDriver."""
        self.driver: WebDriver = driver
        self.wait: WebDriverWait = WebDriverWait(driver, 10)

    def open_chat(self) -> "ChatbotPage":
        """Open the chat panel by clicking the toggle button."""
        try:
            self.wait.until(EC.element_to_be_clickable(self.CHAT_TOGGLE_BUTTON))
            toggle_button: WebElement = self.driver.find_element(
                *self.CHAT_TOGGLE_BUTTON
            )

            if not self.is_chat_panel_visible():
                toggle_button.click()
                # Esperar a que el panel sea visible después de hacer clic
                self.wait.until(EC.visibility_of_element_located(self.CHAT_PANEL))

            return self
        except TimeoutException:
            raise TimeoutException(
                "El botón de alternancia del chat ('chat-toggle-button') no se volvió interactivo dentro del tiempo de espera."
            )
        except NoSuchElementException:
            raise NoSuchElementException(
                "No se encontró el botón de alternancia del chat ('chat-toggle-button')."
            )

    def close_chat(self) -> "ChatbotPage":
        """Close the chat panel."""
        try:
            self.wait.until(EC.element_to_be_clickable(self.CHAT_TOGGLE_BUTTON))
            toggle_button: WebElement = self.driver.find_element(
                *self.CHAT_TOGGLE_BUTTON
            )

            if self.is_chat_panel_visible():
                toggle_button.click()
                # Esperar a que el panel no sea visible después de hacer clic
                self.wait.until(EC.invisibility_of_element_located(self.CHAT_PANEL))

            return self
        except TimeoutException:
            raise TimeoutException(
                "El botón de alternancia del chat ('chat-toggle-button') no se volvió interactivo dentro del tiempo de espera."
            )
        except NoSuchElementException:
            raise NoSuchElementException(
                "No se encontró el botón de alternancia del chat ('chat-toggle-button')."
            )

    def send_message(self, message: str) -> "ChatbotPage":
        """Send a message to the chatbot."""
        try:
            self.wait.until(EC.element_to_be_clickable(self.CHAT_INPUT))
            chat_input: WebElement = self.driver.find_element(*self.CHAT_INPUT)

            chat_input.clear()
            chat_input.send_keys(message)

            send_button: WebElement = self.driver.find_element(*self.SEND_BUTTON)
            send_button.click()

            return self
        except TimeoutException:
            raise TimeoutException(
                "El campo de entrada del chat ('chat-input') no se volvió interactivo dentro del tiempo de espera."
            )
        except NoSuchElementException:
            raise NoSuchElementException(
                "No se encontraron los elementos necesarios para enviar un mensaje."
            )

    def send_message_with_enter(self, message: str):
        """Send a message using the Enter key."""
        chat_input = self.driver.find_element(*self.CHAT_INPUT)

        try:
            self.wait.until(EC.element_to_be_clickable(self.CHAT_INPUT))
        except TimeoutException:
            raise TimeoutException(
                "El campo de entrada del chat ('chat-input') no se volvió interactivo dentro del tiempo de espera."
            )

        chat_input.clear()
        chat_input.send_keys(message)
        chat_input.send_keys(Keys.RETURN)
        return self

    def wait_for_bot_response(self):
        """Wait for the bot to respond and return the response text."""
        try:
            bot_msg_cnt = len(self.driver.find_elements(*self.BOT_MESSAGES))
            self.wait.until(
                lambda driver: len(driver.find_elements(*self.BOT_MESSAGES))
                > bot_msg_cnt
            )
            bot_response = self.driver.find_element(*self.LAST_BOT_MESSAGE)
            return bot_response.text

        except TimeoutException:
            raise TimeoutException(
                "No apareció un nuevo mensaje del bot dentro del tiempo de espera."
            )

    def is_chat_panel_visible(self):
        """Check if the chat panel is visible."""
        try:
            chat_panel: WebElement = self.driver.find_element(*self.CHAT_PANEL)
            return chat_panel.is_displayed()
        except Exception:
            return False

    def get_all_bot_messages(self):
        """Get a list of all bot messages."""
        elements = self.driver.find_elements(*self.BOT_MESSAGES)
        return [element.text for element in elements]

    def get_all_user_messages(self):
        """Get a list of all user messages."""
        elements = self.driver.find_elements(*self.USER_MESSAGES)
        return [element.text for element in elements]

    def is_send_button_enabled(self):
        """Check if the send button is enabled."""
        try:
            return self.driver.find_element(*self.SEND_BUTTON).is_enabled()
        except TimeoutException:
            raise TimeoutException(
                "El botón de envío ('send-button') no se volvió interactivo dentro del tiempo de espera."
            )

    def reset_state(self):
        """Reset the chat to its initial state.

        Useful for tests that need a clean chat state.
        """
        try:
            self.driver.refresh()
            self.wait.until(EC.presence_of_element_located(self.CHAT_TOGGLE_BUTTON))
            return self
        except Exception as e:
            print(f"Error al reiniciar el estado del chat: {e}")
            raise TimeoutException(
                "El botón de alternancia del chat ('chat-toggle-button') no se volvió interactivo dentro del tiempo de espera."
            )
            raise
