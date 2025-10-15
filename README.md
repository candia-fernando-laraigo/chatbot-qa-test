# Laraigo Chatbot QA Test

> Automatización de pruebas funcionales, regresión y estrés para chatbots, centrado en Laraigo con un entorno de ejemplo local. Incluye ejecución paralela, reportes HTML auto-contenidos con datos por test, logging y capturas en fallos.

![Visión general de la ejecución y resultados](assets/response_example.png)

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.x-green.svg?logo=selenium&logoColor=white)](https://www.selenium.dev/)
[![Pytest](https://img.shields.io/badge/Pytest-7.x-red.svg?logo=pytest&logoColor=white)](https://docs.pytest.org/)

</div>

## Tabla de Contenidos

- [Introducción y objetivos](#-introducción-y-objetivos)
- [Páginas bajo prueba](#-páginas-bajo-prueba)
- [Arquitectura y cómo funciona](#-arquitectura-y-cómo-funciona)
- [Requisitos](#-requisitos)
- [Instalación y ejecución rápida](#-instalación-y-ejecución-rápida)
- [Ejecución avanzada](#-ejecución-avanzada-suites-y-paralelismo)
- [Configuración](#-configuración)
- [Estructura del proyecto](#-estructura-del-proyecto)
- [Detalles de implementación](#-detalles-de-implementación-resumen-técnico)
- [Reportes, logs y evidencias](#-reportes-logs-y-evidencias)
- [Extender el proyecto](#-extender-el-proyecto)
- [Solución de problemas](#-solución-de-problemas)

## Introducción y objetivos

Probar manualmente un chatbot es lento y poco repetible. Este proyecto aporta:

- Interacciones **end-to-end** con Selenium
- Paralelización con **pytest-xdist** para carga/estrés
- Validación de contenido con aserciones textuales
- Reportes HTML enriquecidos y logs por ejecución

Se incluye un "entorno simple" (`simple-web/`) para validar rápidamente la infraestructura (POM, fixtures, sincronización) sin depender de servicios externos.

<div align="center">
  
![Chat simple en acción](assets/chatbot_page.png)
  
</div>

## Páginas bajo prueba

| Entorno | URL |
|---------|-----|
| **Producción Laraigo** | [https://demos.laraigo.com/QAOmar/Automatizacion.html](https://demos.laraigo.com/QAOmar/Automatizacion.html) |
| **Testing Laraigo** | [https://demos.laraigo.com/QAOmar/AutomatizacionTST.html](https://demos.laraigo.com/QAOmar/AutomatizacionTST.html) |

> El repo también incluye una página local (`simple-web/index.html`) para pruebas rápidas.

## Arquitectura y cómo funciona

### Componentes clave:

#### Page Object Model (POM)
- **`pages/chatbot_page.py`**: POM del chat simple local
  - Métodos: `open_chat()`, `send_message()`, `wait_for_bot_response()`, etc.
- **`pages/laraigo_page.py`**: POM específico para Laraigo
  - Funcionalidades: abrir/cerrar/refresh, envío, adjuntos, ubicación, mensaje de inactividad
  - Usa `WebDriverWait` extensivo y selectores de la UI Laraigo (`chat-open-chatweb`, `chat-history-refresh`, etc.)

#### Fixtures y configuración Pytest
- **`conftest.py`**:
  - Crea `WebDriver` según `config/config.py`
  - Define fixtures: `driver` y `test_data`
  - Enriquecimiento del reporte HTML y screenshot automático en fallos
- **Marcadores**: 
  - `@pytest.mark.examples` (entorno simple)
  - `@pytest.mark.laraigo` (entorno Laraigo)

#### Runner y paralelización
- **`main.py`**:
  - Invoca pytest con `-n <workers>` (xdist)
  - Repeticiones con `--count` (pytest-repeat)
  - Genera un reporte HTML por ejecución
- **`Makefile`**:
  - Prepara venv, instala dependencias
  - Permite correr suites
  - Incluye `make report` para abrir el último reporte

#### Reportes y logs
- **HTML por ejecución** en `reports/<timestamp>_report.html`
  - Datos por test integrados
  - En fallos, screenshot embebido
- **Logs** en `logs/` gestionados por `utils/logger.py`

<div align="center">

![Reporte HTML con resultados y detalle](assets/report_page.png)

</div>

### Flujo de ejecución (alto nivel):

1. `make test` → prepara venv y llama a `python main.py --suite laraigo` (o `examples`)
2. `main.py` arma argumentos de pytest y habilita paralelismo con xdist
3. `conftest.py` levanta el navegador (headless por defecto)
4. Los tests usan el POM para interactuar con el chat y validar
5. Se generan reportes, logs y, si corresponde, screenshots

## Requisitos

| Componente | Detalle |
|------------|---------|
| **Python** | 3.10+ (recomendado 3.13.7) |
| **Navegador** | Google Chrome (recomendado), Firefox, Edge |
| **Sistema Operativo** | Linux, macOS, Windows |
| **Principales Librerías** | `selenium`, `pytest`, `pytest-html`, `pytest-xdist`, `webdriver-manager`, `pytest-repeat` |

> Los drivers de navegadores se gestionan automáticamente con `webdriver-manager`. En Linux, Chrome headless usa flags ya incluidos.

## Instalación y ejecución rápida

### Instalación con un solo comando:

```bash
make
```

<details>
<summary><b>¿Qué hace este comando?</b></summary>

- Crea/actualiza un entorno virtual (`venv/`)
- Instala dependencias de `requirements.txt`
- Ejecuta la suite por defecto (Laraigo)
</details>

### Abrir el reporte HTML más reciente:

```bash
make report
```

## Ejecución avanzada (suites y paralelismo)

### Suite de ejemplos (chat simple local):

```bash
./venv/bin/python main.py --suite examples -v
```

### Suite Laraigo con 8 workers:

```bash
./venv/bin/python main.py --suite laraigo --parallel 8 -vv
```

### Todos los tests del repo (sin marcador):

```bash
./venv/bin/python main.py --suite all -v
```

### Parámetros útiles de `main.py`:

| Parámetro | Descripción | Valores posibles |
|-----------|-------------|-----------------|
| `--suite` | Conjunto de tests a ejecutar | `all` \| `examples` \| `laraigo` |
| `--parallel` | Procesos en paralelo | Número (default: `config.PYTEST_WORKERS`) |
| `--count` | Repeticiones en una ejecución | Número (requiere `pytest-repeat`) |
| `-v/-vv/-vvv` | Nivel de verbosidad | - |

> Ajustar `--parallel` según núcleos disponibles. Para estrés, usa un valor alto; para debugging, 1-2.

## Configuración

Archivo: `config/config.py`

| Parámetro | Descripción | Valores |
|-----------|-------------|---------|
| `PAGE_URL` | Destino bajo prueba | Default: `LARAIGO_CHATBOT_TEST` |
| `PAGE_TIMEOUT` | Timeout general para esperas | Segundos |
| `BROWSER_TYPE` | Navegador a utilizar | `chrome` \| `firefox` \| `edge` |
| `HEADLESS` | Modo sin interfaz gráfica | `True` \| `False` |
| `PYTEST_WORKERS` | Procesos paralelos por defecto | Número |
| `SCREENSHOT_DIR` | Directorio para capturas | Ruta |
| `TAKE_SCREENSHOT_ON_FAILURE` | Captura en fallos | `True` \| `False` |

#### URLs predefinidas:
- Producción: `LARAIGO_CHATBOT_PROD = "https://demos.laraigo.com/QAOmar/Automatizacion.html"`
- Testing: `LARAIGO_CHATBOT_TEST = "https://demos.laraigo.com/QAOmar/AutomatizacionTST.html"`

> Si quieres usar el entorno local simple, ajusta `PAGE_URL` para apuntar al archivo `simple-web/index.html` vía `file://` o crea una opción dedicada.

## Estructura del proyecto

<details open>
<summary><b>Estructura de archivos y directorios</b></summary>

```
chatbot-qa-test/
├─ main.py                       # Runner para pytest (paralelo, repeticiones)
├─ conftest.py                   # Fixtures (driver, test_data), WebDriver, reporte enriquecido
├─ config/
│  └─ config.py                  # Parámetros de ejecución y entorno
├─ pages/
│  ├─ chatbot_page.py            # POM simple-web
│  └─ laraigo_page.py            # POM Laraigo
├─ tests/
│  ├─ test_chatbot_ui.py         # UI básica simple-web
│  ├─ test_chatbot_responses.py  # Respuestas simple-web
│  └─ test_laraigo_responses.py  # Validaciones Laraigo
├─ simple-web/                   # Mini sitio local
├─ utils/
│  └─ logger.py                  # Logging de ejecución
├─ assets/                       # Imágenes y CSS para docs/reportes
├─ reports/                      # Reportes HTML generados
├─ screenshots/                  # Evidencias en fallo
├─ docs/                         # Documentación de casos
├─ requirements.txt              # Dependencias
└─ Makefile                      # Tareas de setup/ejecución
```
</details>

## Detalles de implementación (resumen técnico)

### Page Objects Models (POMs)

<details>
<summary><b>ChatbotPage</b> (chat simple local)</summary>

- **Selectores principales**:
  - `CHAT_TOGGLE_BUTTON`
  - `CHAT_INPUT`
  - `SEND_BUTTON`
- **Funcionalidad**:
  - Envío de mensajes con botón o tecla Enter
  - `wait_for_bot_response()` sincroniza por aparición de nuevo mensaje
</details>

<details>
<summary><b>LaraigoPage</b> (específico para Laraigo)</summary>

- **Funcionalidad**:
  - Abrir/cerrar/refresh chat
  - Envío de adjuntos (imagen/archivo/audio/video)
  - Compartir ubicación
  - Manejo de mensaje de inactividad
  - Utilidades para obtener mensajes: `get_all_*_messages[_text]`
</details>

### Fixtures y configuración

<details>
<summary><b>Fixtures clave</b> (conftest.py)</summary>

- **`driver`**:
  - Instancia navegador según `BROWSER_TYPE` usando `webdriver-manager`
- **`test_data`**:
  - Adjunta al reporte HTML datos del test (mensaje, respuesta, tiempos)
- **Hooks**:
  - `pytest_runtest_makereport`: agrega bloque HTML con datos y screenshot en fallos
  - `pytest_terminal_summary`: inserta resumen JSON al final del HTML
</details>

### Runner y ejecución

<details>
<summary><b>Runner</b> (main.py)</summary>

- Construye argumentos pytest
- Habilita `-n <workers>` para paralelismo
- Configura `--count <N>` para repeticiones
- Genera reporte auto-contenido en `reports/`
</details>

### Validaciones (tests)

<details>
<summary><b>Suite "examples"</b> (chat simple)</summary>

- Validaciones de saludos, precios, productos/servicios, contacto
- Registra tiempos y múltiples mensajes en conversación
</details>

<details>
<summary><b>Suite "laraigo"</b> (chatbot Laraigo)</summary>

- Saludos deben iniciar con "Hola Blanquiazul…"
- Consultas de membresía con "Gracias por contactarte…"
- Mensajes fuera de alcance con "Lo lamento…"
- Guarda tiempos y última respuesta recibida
</details>

## Reportes, logs y evidencias

### Reportes HTML

<details open>
<summary><b>Contenido de reportes</b></summary>

- **Ubicación**: `reports/<timestamp>_report.html`
- **Características**:
  - Resumen de resultados y tiempos de ejecución
  - Bloques "Test Data" con mensaje enviado, respuesta, response time y duración
  - En fallos: screenshot embebido y error detallado
</details>

### Logs

- **Ubicación**: `logs/test_run_<timestamp>.log`

<div align="center">

![Reporte HTML con test expandido y evidencia](assets/report_page.png)

</div>

## Extender el proyecto

### Nuevo caso de prueba

<details open>
<summary><b>Pasos para añadir nuevos tests</b></summary>

1. Crear archivo en `tests/` o sumar funciones a los existentes
2. Usar marcadores `@pytest.mark.examples` o `@pytest.mark.laraigo`
3. Reutilizar fixtures `driver` y `test_data`
4. Guardar datos con `test_data(sent_message=..., response_text=..., response_time=...)` para enriquecer el reporte
</details>

### Validaciones de contenido

- Preferir `startswith`, `in`, normalización `lower()`, o regex
- Añadir esperas explícitas en POM antes de leer el DOM

### Soporte de navegador

- Cambiar `BROWSER_TYPE` en `config/config.py`
- Los drivers se gestionan automáticamente con webdriver-manager

## ⚠️ Solución de problemas

<details>
<summary><b>Error al iniciar el navegador (driver)</b></summary>

- ✅ Verifica conexión a internet (para descarga de `webdriver-manager`)
- ✅ Asegúrate que Chrome/Firefox/Edge estén correctamente instalados
</details>

<details>
<summary><b>Fallos sólo en modo headless</b></summary>

- ✅ Cambia `HEADLESS=False` en config.py para visualizar la ejecución
- ✅ En Linux, los flags `--no-sandbox` y `--disable-dev-shm-usage` ya están activos
</details>

<details>
<summary><b>No se ve el reporte</b></summary>

- ✅ Usa `make report` para abrir automáticamente el último reporte
- ✅ Abre manualmente el último archivo generado en la carpeta `reports/`
</details>

<details>
<summary><b>Timeouts/tardanza</b></summary>

- ✅ Ajusta `PAGE_TIMEOUT` en `config/config.py`
- ✅ Reduce `--parallel` para entornos con recursos limitados
</details>

---

**Autoría:** [Fernando Candia](https://github.com/candia-fernando-laraigo)

