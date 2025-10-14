# Guía Rápida de Referencia - Chatbot QA Test

## Comandos Principales

| Comando | Descripción |
|---------|-------------|
| `make setup` | Configura el entorno virtual e instala dependencias |
| `make test` | Ejecuta todas las pruebas de Laraigo |
| `make test-examples` | Ejecuta solo las pruebas de ejemplo |
| `make clean` | Elimina archivos temporales y de caché |
| `python main.py` | Ejecuta todas las pruebas |
| `python main.py --suite laraigo` | Ejecuta solo pruebas de Laraigo |
| `python main.py --parallel 4` | Ejecuta con 4 procesos paralelos |
| `python main.py -v` | Ejecuta con mayor detalle (verbose) |

## Estructura del Proyecto

| Directorio/Archivo | Propósito |
|--------------------|-----------|
| `config/config.py` | Configuración del framework |
| `pages/` | Page Objects para interacción con la interfaz |
| `tests/` | Casos de prueba |
| `reports/` | Reportes HTML generados |
| `logs/` | Archivos de registro de ejecución |
| `screenshots/` | Capturas de pantalla de fallos |
| `main.py` | Script principal de ejecución |
| `conftest.py` | Configuración de pytest y fixtures |

## Marcadores (Markers) de Pytest

| Marcador | Descripción |
|----------|-------------|
| `@pytest.mark.laraigo` | Pruebas específicas para el chatbot Laraigo |
| `@pytest.mark.examples` | Pruebas de ejemplo |
| `@pytest.mark.parametrize` | Permite ejecutar pruebas con múltiples conjuntos de datos |

## Tiempos de Espera

| Configuración | Valor Predeterminado | Descripción |
|---------------|----------------------|-------------|
| `IMPLICIT_WAIT` | 60 segundos | Espera implícita para elementos |
| `EXPLICIT_WAIT` | 60 segundos | Espera explícita máxima |

## Page Objects Principales

### LaraigoPage

```python
# Inicialización
laraigo_page = LaraigoPage(driver)

# Métodos principales
laraigo_page.open_chat()              # Abre la ventana del chat
laraigo_page.close_chat()             # Cierra la ventana del chat
laraigo_page.send_message(mensaje)    # Envía un mensaje y devuelve la respuesta
laraigo_page.get_all_bot_messages_text()  # Obtiene todas las respuestas del bot
laraigo_page.refresh_chat()           # Refresca la ventana de chat
```

## Fixtures Comunes

| Fixture | Descripción |
|---------|-------------|
| `driver` | Instancia de WebDriver configurada |
| `laraigo_page` | Instancia de LaraigoPage inicializada |
| `logger` | Sistema de logging |
| `test_data` | Recopilador de datos para reportes |
| `wait` | WebDriverWait configurado |

## Reporte de Datos

```python
# Dentro de un caso de prueba
test_data(
    sent_message="Mensaje enviado",  # Mensaje enviado al bot
    response_text=["Respuesta del bot"],  # Respuesta recibida
    response_time=1.23  # Tiempo de respuesta en segundos
)
```

## Logging

```python
# Dentro de un caso de prueba
logger.info("Mensaje informativo")
logger.debug("Mensaje de depuración")
logger.error("Mensaje de error")
logger.log_response_time("test_name", "message", time_value)
```

## Creación de Casos de Prueba

Plantilla básica:

```python
@pytest.mark.laraigo
def test_nombre_descriptivo(laraigo_page, logger, test_data):
    """
    Descripción del caso de prueba
    """
    # 1. Preparación
    laraigo_page.open_chat()
    
    # 2. Acción
    mensaje = "Mensaje de prueba"
    start_time = time.time()
    respuesta = laraigo_page.send_message(mensaje)
    response_time = time.time() - start_time
    
    # 3. Verificación
    assert condicion, "Mensaje de error"
    
    # 4. Registro
    test_data(
        sent_message=mensaje,
        response_text=respuesta,
        response_time=response_time
    )
```

## Verificaciones Comunes

```python
# Verificar contenido de respuesta
assert any(texto_esperado in msg for msg in respuesta)

# Verificar visibilidad de elemento
assert laraigo_page.is_chat_window_visible()

# Verificar tiempo de respuesta
assert response_time < 5.0  # Tiempo máximo de 5 segundos
```

## Configuración Personalizada

Editar `config/config.py` para:
- Cambiar el navegador (`BROWSER_TYPE`)
- Modificar URL base (`BASE_URL`)
- Ajustar paralelismo (`PYTEST_WORKERS`)
- Activar/desactivar modo headless (`HEADLESS`)
- Modificar tiempos de espera (`IMPLICIT_WAIT`, `EXPLICIT_WAIT`)