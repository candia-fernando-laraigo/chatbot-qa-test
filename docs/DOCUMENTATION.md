# Chatbot QA Test Automation Framework Documentation

## Índice
1. [Introducción](#introducción)
2. [Estructura del Proyecto](#estructura-del-proyecto)
3. [Arquitectura de Pruebas](#arquitectura-de-pruebas)
4. [Flujo de Ejecución](#flujo-de-ejecución)
5. [Configuración del Entorno](#configuración-del-entorno)
6. [Page Object Models](#page-object-models)
7. [Casos de Prueba](#casos-de-prueba)
8. [Reportes y Logs](#reportes-y-logs)
9. [Ejecución Paralela](#ejecución-paralela)
10. [Limitaciones Actuales](#limitaciones-actuales)
11. [Mejores Prácticas](#mejores-prácticas)
12. [Guía de Desarrollo](#guía-de-desarrollo)
13. [Glosario](#glosario)

## Introducción

Este framework de automatización de pruebas ha sido desarrollado como una "Prueba de Concepto" para validar la calidad del chatbot Laraigo implementado en aplicaciones web. El sistema permite ejecutar pruebas automatizadas que simulan interacciones de usuarios con el chatbot, evaluando:

- La interfaz de usuario y su funcionalidad
- La precisión de las respuestas del chatbot
- Los tiempos de respuesta del sistema
- La consistencia en diferentes escenarios de uso

La implementación actual utiliza una estrategia de ejecución simplificada que ejecuta múltiples instancias de pytest en secuencia para completar un conjunto de aproximadamente 190 pruebas. Aunque no es la implementación más eficiente desde el punto de vista del diseño de software, esta "Prueba de Concepto" ha demostrado ser efectiva para validar la funcionalidad básica del chatbot.

## Estructura del Proyecto

El proyecto sigue una estructura modular diseñada para facilitar el mantenimiento y la expansión:

```
chatbot-qa-test/
├── config/                 # Configuraciones generales
│   └── config.py           # Parámetros de configuración (navegador, URLs, timeouts)
├── conftest.py             # Configuración de pytest y fixtures comunes
├── pages/                  # Implementación del patrón Page Object Model
│   ├── chatbot_page.py     # Modelo genérico para interfaces de chatbot
│   └── laraigo_page.py     # Modelo específico para el chatbot Laraigo
├── tests/                  # Suites de pruebas
│   ├── test_chatbot_ui.py  # Pruebas de interfaz genéricas
│   ├── test_chatbot_responses.py  # Pruebas de respuestas genéricas
│   ├── test_laraigo_ui.py  # Pruebas de interfaz específicas para Laraigo
│   └── test_laraigo_responses.py  # Pruebas de respuestas específicas para Laraigo
├── utils/                  # Utilidades y herramientas auxiliares
│   └── logger.py           # Sistema de logging personalizado
├── simple-web/             # Sitio web de demostración para pruebas locales
├── reports/                # Almacenamiento de reportes HTML generados
├── screenshots/            # Capturas de pantalla en fallos de pruebas
├── logs/                   # Registros de ejecución
├── main.py                 # Script principal de ejecución
├── Makefile                # Automatización de comandos comunes
├── README.md               # Documentación general
├── TEST_CASES_EXAMPLE.md   # Documentación de casos de prueba de ejemplo
└── TEST_CASES_LARAIGO.md   # Documentación de casos de prueba específicos de Laraigo
```

## Arquitectura de Pruebas

El framework está construido sobre los siguientes componentes principales:

1. **Pytest**: Motor de pruebas principal, proporciona la estructura para definir, organizar y ejecutar pruebas.

2. **Selenium WebDriver**: Biblioteca de automatización que permite controlar navegadores web programáticamente.

3. **Page Object Model (POM)**: Patrón de diseño que encapsula la interacción con páginas web en clases específicas, separando la lógica de prueba de la implementación de la interfaz.

4. **Sistema de configuración**: Centraliza los parámetros configurables como tipo de navegador, timeouts y URLs.

5. **Sistema de logging**: Registra los detalles de la ejecución, mensajes intercambiados y tiempos de respuesta.

6. **Generador de reportes**: Produce reportes HTML detallados con información sobre cada prueba ejecutada.

La arquitectura sigue el principio de separación de responsabilidades, donde:

- Los **casos de prueba** definen el comportamiento esperado
- Los **page objects** encapsulan la interacción con la interfaz web
- Los **fixtures** configuran el entorno de prueba
- Los **sistemas de logging y reportes** documentan los resultados

## Flujo de Ejecución

El proceso completo de ejecución de pruebas sigue estos pasos:

1. **Inicialización**:
   - El script `main.py` procesa los argumentos de línea de comandos
   - Se configuran directorios para logs, screenshots y reportes
   - Se inicializa el sistema de logging

2. **Configuración de Pruebas**:
   - Se determinan los argumentos para pytest (suite de pruebas, nivel de detalle, paralelismo)
   - Se establece la ruta del reporte HTML

3. **Ejecución de Pruebas** (Este paso se repite 10 veces según la configuración actual):
   - Se construye el comando de pytest con los argumentos necesarios
   - Se ejecuta mediante `subprocess.run()`
   - Se registra el resultado de la ejecución (éxito o fallo)

4. **Para cada prueba individual** (dentro de pytest):
   - El `conftest.py` configura el entorno con los fixtures necesarios
   - Se inicializa el navegador según la configuración
   - Se carga la URL base
   - Se ejecuta el caso de prueba específico
   - Se registran los resultados, incluyendo mensajes enviados y recibidos
   - Se capturan screenshots en caso de fallo
   - Se cierra el navegador

5. **Generación de Reportes**:
   - Se genera un reporte HTML después de cada lote de pruebas
   - Los reportes incluyen detalles de cada prueba, tiempo de ejecución, y enlaces a screenshots

## Configuración del Entorno

### Requisitos Previos

- Python 3.7+
- Navegador Chrome, Firefox o Edge
- WebDrivers correspondientes (instalados automáticamente por webdriver-manager)

### Configuración del Proyecto

El archivo `config/config.py` contiene los principales parámetros configurables:

```python
# URL base para pruebas (puede ser web o local)
BASE_URL = "file://{ruta_local}/simple-web/index.html"

# Configuración del navegador
BROWSER_TYPE = "chrome"  # Opciones: chrome, firefox, edge
HEADLESS = True  # Modo sin interfaz gráfica

# Configuración de ejecución
PYTEST_WORKERS = 16  # Número de pruebas paralelas
IMPLICIT_WAIT = 60  # Tiempo de espera implícito (segundos)
EXPLICIT_WAIT = 60  # Tiempo de espera explícito (segundos)

# Directorios
SCREENSHOT_DIR = "../screenshots"
TAKE_SCREENSHOT_ON_FAILURE = True
```

### Instalación y Configuración

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

## Page Object Models

El framework implementa dos modelos principales:

### ChatbotPage (Genérico)

Implementa funcionalidades comunes para cualquier interfaz de chatbot:

```python
class ChatbotPage:
    # Locators comunes
    CHAT_TOGGLE_BUTTON = (By.ID, "chat-toggle-button")
    CHAT_PANEL = (By.ID, "chat-panel")
    CHAT_INPUT = (By.ID, "chat-input")
    
    # Métodos comunes
    def open_chat(self)
    def send_message(self, message)
    def get_bot_messages(self)
    # etc...
```

### LaraigoPage (Específico)

Extiende la funcionalidad para adaptarse a la implementación específica del chatbot Laraigo:

```python
class LaraigoPage:
    # Locators específicos de Laraigo
    CHAT_OPEN_BUTTON = (By.ID, "chat-open-chatweb")
    CHAT_WINDOW = (By.ID, "chat-window")
    
    # Métodos adaptados
    def open_chat(self)
    def send_message(self, message)
    def refresh_chat(self)
    # etc...
```

Los Page Objects encapsulan toda la interacción con la interfaz web, proporcionando:
- Abstracción de los detalles de implementación
- Reutilización de código
- Facilidad de mantenimiento cuando cambia la interfaz

## Casos de Prueba

Los casos de prueba están organizados en suites según su objetivo:

### Tests de UI (test_laraigo_ui.py)

Verifican la correcta funcionalidad de los elementos de la interfaz:
- Visibilidad del botón de chat
- Apertura/cierre del panel de chat
- Funcionamiento del botón de envío
- Visualización de mensajes

### Tests de Respuestas (test_laraigo_responses.py)

Evalúan la calidad y precisión de las respuestas del chatbot:

1. **Test Case 1: Saludos y Frases de Cortesía**
   - Valida que el sistema responde correctamente a diversos saludos
   - Verifica que la respuesta comienza con "Hola Blanquiazul"

2. **Test Case 2: Consultas sobre la Membresía**
   - Comprueba que las preguntas sobre membresía son reconocidas
   - Verifica respuestas que comienzan con "Gracias por contactarte"

3. **Test Case 3: Preguntas Fuera de Alcance**
   - Valida el manejo de preguntas no programadas
   - Verifica respuestas que comienzan con "Lo lamento"

Cada caso de prueba utiliza `parametrize` de pytest para ejecutar múltiples variantes con diferentes entradas, maximizando la cobertura con código mínimo.

## Reportes y Logs

### Sistema de Logging

El framework implementa un sistema de logging personalizado (`TestLogger`) que registra:

- Inicio y fin de cada prueba
- Mensajes enviados al chatbot
- Respuestas recibidas
- Tiempos de respuesta
- Errores y excepciones

Los logs se almacenan en el directorio `logs/` con un archivo por sesión de prueba.

### Reportes HTML

Después de cada ejecución se genera un reporte HTML detallado en el directorio `reports/` con:

- Resumen de ejecución (pruebas exitosas/fallidas)
- Detalles de cada prueba individual
- Mensajes intercambiados
- Tiempos de respuesta
- Enlaces a screenshots de fallos
- Métricas de rendimiento

Los reportes se nombran con timestamps para mantener un historial completo.

## Ejecución Paralela

El framework admite ejecución paralela a través de dos mecanismos:

1. **Paralelismo dentro de pytest** (usando pytest-xdist):
   - Configurable mediante el parámetro `--parallel` en `main.py`
   - Permite ejecutar múltiples pruebas simultáneamente dentro de un proceso pytest

2. **Ejecución secuencial de múltiples instancias**:
   - La implementación actual ejecuta 10 iteraciones secuenciales de pytest
   - Cada iteración ejecuta un conjunto completo de pruebas
   - Este enfoque fue implementado como solución temporal para la "Prueba de Concepto"

El paralelismo permite:
- Reducir el tiempo total de ejecución
- Simular escenarios de carga con múltiples usuarios simultáneos
- Evaluar el rendimiento del chatbot bajo condiciones de uso intensivo

## Limitaciones Actuales

Al ser una "Prueba de Concepto", el framework tiene algunas limitaciones conocidas:

1. **Ejecución secuencial de múltiples instancias**:
   - La ejecución de 10 iteraciones secuenciales no es la solución más elegante
   - Podría refactorizarse para usar un diseño más estructurado

2. **Manejo de sesiones**:
   - El framework reinicia el navegador para cada prueba, lo que puede ser ineficiente
   - No hay persistencia de sesión entre pruebas

3. **Cobertura limitada**:
   - Los casos de prueba actuales cubren solo escenarios básicos
   - Se podrían añadir flujos de conversación más complejos

4. **Dependencia del DOM**:
   - Los selectores dependen de la estructura específica del DOM
   - Cambios en la interfaz pueden requerir actualizaciones en los Page Objects

## Mejores Prácticas

Para trabajar con este framework, se recomiendan las siguientes prácticas:

1. **Mantener los casos de prueba independientes**:
   - Cada prueba debe funcionar de forma aislada
   - Evitar dependencias entre casos de prueba

2. **Utilizar siempre los Page Objects**:
   - No interactuar directamente con el WebDriver desde los tests
   - Mantener la abstracción para facilitar el mantenimiento

3. **Documentar los casos de prueba**:
   - Mantener actualizados los archivos TEST_CASES*.md
   - Incluir descripción, entradas y resultados esperados

4. **Utilizar parametrización**:
   - Aprovechar `@pytest.mark.parametrize` para probar múltiples variantes
   - Reutilizar el código de prueba para diferentes entradas

5. **Capturar información relevante**:
   - Usar el sistema de logging para registrar detalles importantes
   - Guardar screenshots en caso de fallos

## Guía de Desarrollo

### Agregar Nuevos Casos de Prueba

1. **Identificar el tipo de prueba** (UI o respuesta)
2. **Crear un nuevo método de prueba** en el archivo apropiado:

```python
@pytest.mark.laraigo  # Usar el marcador adecuado
def test_nueva_funcionalidad(self, laraigo_page, logger, test_data):
    # Documentación del caso de prueba
    """
    Test Case: Descripción breve
    Objetivo: Objetivo detallado
    Resultado Esperado: Comportamiento esperado
    """
    
    # Preparación
    laraigo_page.open_chat()
    
    # Acción
    mensaje = "Mensaje de prueba"
    start_time = time.time()
    respuesta = laraigo_page.send_message(mensaje)
    response_time = time.time() - start_time
    
    # Verificación
    assert condicion_esperada, "Mensaje descriptivo del fallo"
    
    # Logging y reporte
    logger.info(f"Mensaje enviado: {mensaje}")
    logger.info(f"Respuesta recibida: {respuesta}")
    test_data(sent_message=mensaje, response_text=respuesta, response_time=response_time)
```

3. **Documentar el caso de prueba** en TEST_CASES_LARAIGO.md
4. **Ejecutar la prueba** utilizando el comando apropiado

### Modificar Page Objects

Para añadir nuevas funcionalidades a los Page Objects:

1. **Identificar los selectores** necesarios
2. **Añadir nuevos locators** a la clase:

```python
NUEVO_ELEMENTO = (By.ID, "id-del-elemento")
```

3. **Implementar métodos** para interactuar con los nuevos elementos:

```python
def nueva_accion(self, parametro) -> "TipoDePagina":
    """Documentación de la nueva acción."""
    try:
        elemento = self.wait.until(
            EC.visibility_of_element_located(self.NUEVO_ELEMENTO)
        )
        # Implementar lógica de interacción
        return self  # Para permitir encadenamiento de métodos
    except TimeoutException:
        # Manejar excepciones adecuadamente
        raise
```

4. **Actualizar los tests** para utilizar la nueva funcionalidad

### Ejecutar Pruebas

Para ejecutar todas las pruebas:

```bash
# Usando Makefile
make test

# Directamente con main.py
python main.py --suite laraigo
```

Para ejecutar un conjunto específico de pruebas:

```bash
# Usando pytest directamente
pytest tests/test_laraigo_responses.py::test_greeting_responses -v
```

Para ejecutar pruebas con paralelismo:

```bash
python main.py --suite laraigo --parallel 4
```

## Glosario

- **Page Object Model (POM)**: Patrón de diseño que encapsula la interacción con páginas web en clases específicas.
- **Fixture**: En pytest, funciones que proporcionan datos o configuran el entorno para las pruebas.
- **Locator**: Tupla que define cómo encontrar un elemento web (método de búsqueda y valor).
- **Selector**: Expresión que identifica elementos en el DOM (ID, clase, XPath, etc.).
- **WebDriver**: API para controlar navegadores web programáticamente.
- **Asserción**: Verificación que debe ser verdadera para que una prueba pase.
- **Parametrización**: Técnica para ejecutar la misma prueba con múltiples conjuntos de datos.
- **Marcadores (Markers)**: Etiquetas que se aplican a las pruebas para categorizarlas.