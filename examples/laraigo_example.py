"""
Script de ejemplo que demuestra el uso de la clase LaraigoPage para interactuar con el chatbot de Laraigo.
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.laraigo_page import LaraigoPage


def main():
    """Función principal para demostrar el uso de LaraigoPage."""

    # Configurar el driver de Chrome
    chrome_options = Options()
    chrome_options.add_argument(
        "--headless"
    )  # Descomentar para ejecutar en modo headless
    chrome_options.add_argument("--window-size=1920,1080")

    # Inicializar el WebDriver
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )

    try:
        # Inicializar la página del chatbot
        laraigo_bot = LaraigoPage(driver)

        # Cargar la página (usando una ruta local o URL remota)
        laraigo_bot.load_page("https://demos.laraigo.com/QAOmar/Automatizacion.html")

        # Esperar a que la página cargue
        laraigo_bot.wait_for_page_load()
        print("Página cargada correctamente")

        # Abrir el chat
        laraigo_bot.open_chat()
        print("Chat abierto")

        # Enviar un mensaje
        mensaje = "Hola, ¿cómo estás?"
        laraigo_bot.send_message(mensaje)
        print(f"Mensaje enviado: '{mensaje}'")

        # Esperar y obtener la respuesta del bot
        respuesta = laraigo_bot.wait_for_bot_response()
        print(f"Respuesta del bot: '{respuesta}'")

        # Enviar otro mensaje con Enter
        segundo_mensaje = "¿Qué servicios ofreces?"
        laraigo_bot.send_message_with_enter(segundo_mensaje)
        print(f"Mensaje enviado con Enter: '{segundo_mensaje}'")

        # Esperar y obtener la respuesta del bot
        segunda_respuesta = laraigo_bot.wait_for_bot_response()
        print(f"Respuesta del bot: '{segunda_respuesta}'")

        # Mostrar todos los mensajes intercambiados
        print("\nMensajes del usuario:")
        for msg in laraigo_bot.get_all_user_messages_text():
            print(f"- {msg}")

        print("\nMensajes del bot:")
        for msg in laraigo_bot.get_all_bot_messages_text():
            print(f"- {msg}")

        # Ejemplo de cómo subir una imagen (comentado porque requiere una ruta real)
        # chatbot.upload_image("/ruta/a/imagen.jpg")

        # Cerrar el chat
        time.sleep(2)  # Esperar un poco para ver los resultados
        laraigo_bot.close_chat()
        print("Chat cerrado")

        # Reiniciar el estado
        laraigo_bot.reset_state()
        print("Estado del chat reiniciado")

    finally:
        # Cerrar el navegador
        time.sleep(2)  # Esperar un poco antes de cerrar
        driver.quit()
        print("Navegador cerrado")


if __name__ == "__main__":
    main()
