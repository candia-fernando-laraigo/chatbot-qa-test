# Manual de Uso - Chatbot QA Test Automation

Este manual proporciona instrucciones paso a paso para utilizar el framework de pruebas automatizadas para chatbots.

## Instalación y Configuración

### Requisitos Previos

- Python 3.7 o superior
- Google Chrome, Firefox o Edge
- Git (opcional)

### Pasos de Instalación

1. **Clonar el repositorio** (o descargar como ZIP):
   ```bash
   git clone https://github.com/candia-fernando-laraigo/chatbot-qa-test
   cd chatbot-qa-test
   ```

2. **Configurar el entorno virtual**:
   ```bash
   # Crear entorno virtual
   python -m venv venv
   
   # Activar entorno virtual
   # En Linux/Mac:
   source venv/bin/activate
   # En Windows:
   venv\Scripts\activate
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Verificar la configuración**: Abrir `config/config.py` y revisar que los parámetros sean adecuados para su entorno:
   - `BASE_URL`: URL del sitio web a probar
   - `BROWSER_TYPE`: Navegador a utilizar (chrome, firefox, edge)
   - `HEADLESS`: Modo sin interfaz gráfica (True/False)
   - `PYTEST_WORKERS`: Número de pruebas paralelas

## Ejecutar Pruebas

### Ejecución Básica

Para ejecutar todas las pruebas con la configuración predeterminada:

```bash
make test
```

O si prefiere no usar Make:

```bash
python main.py
```

### Opciones de Ejecución

Para ejecutar pruebas con opciones personalizadas:

```bash
# Ejecutar solo pruebas de ejemplo
python main.py --suite examples

# Ejecutar pruebas de Laraigo
python main.py --suite laraigo

# Ejecutar con paralelismo personalizado
python main.py --parallel 4

# Ejecutar con mayor nivel de detalle
python main.py -v
```

### Ver Resultados

1. **Reportes HTML**: Los reportes se generan en el directorio `reports/` con nombres basados en timestamps. Puede abrir el más reciente en su navegador:
   ```bash
   # En Linux
   xdg-open reports/$(ls -t reports | head -1)
   
   # En macOS
   open reports/$(ls -t reports | head -1)
   
   # En Windows (usando PowerShell)
   start (Get-ChildItem -Path reports | Sort-Object LastWriteTime -Descending | Select-Object -First 1).FullName
   ```

2. **Logs**: Los registros detallados se encuentran en el directorio `logs/`.

3. **Screenshots**: Las capturas de pantalla de fallos se almacenan en `screenshots/`.

## Personalización

### Configurar el Chatbot a Probar

Si necesita probar un chatbot diferente o en una URL distinta:

1. Modificar `config/config.py`:
   ```python
   # Cambiar la URL base
   BASE_URL = "https://su-sitio-web.com"
   ```

2. Ajustar los tiempos de espera si es necesario:
   ```python
   IMPLICIT_WAIT = 30  # segundos
   EXPLICIT_WAIT = 30  # segundos
   ```

### Ejecutar en Modo Visible

Para ver el navegador durante la ejecución (útil para depuración):

1. Modificar `config/config.py`:
   ```python
   HEADLESS = False
   ```

2. Ejecutar las pruebas normalmente:
   ```bash
   python main.py
   ```

## Solución de Problemas

### Errores Comunes

1. **TimeoutException**:
   - Incrementar los valores de `IMPLICIT_WAIT` y `EXPLICIT_WAIT` en `config.py`
   - Verificar que los selectores en los Page Objects sean correctos

2. **NoSuchElementException**:
   - Verificar que los ID o selectores CSS utilizados son correctos
   - Asegurarse de que la página carga completamente antes de interactuar

3. **WebDriver no encontrado**:
   - El sistema debería descargar automáticamente el WebDriver
   - Si falla, descargue manualmente el WebDriver correspondiente a su navegador

4. **Errores de importación**:
   - Verificar que está ejecutando desde el directorio raíz del proyecto
   - Asegurarse de que todas las dependencias están instaladas

### Obtener Ayuda

Si encuentra problemas no documentados:

1. Revisar los logs en el directorio `logs/`
2. Verificar los screenshots generados en caso de fallos
3. Contactar al equipo de desarrollo con los detalles del error

## Extensión del Framework

### Añadir Nuevos Casos de Prueba

Para agregar nuevos escenarios de prueba:

1. Crear un nuevo archivo de prueba o añadir a uno existente:
   ```python
   @pytest.mark.laraigo
   def test_nuevo_escenario(laraigo_page, logger, test_data):
       # Documentación de la prueba
       """Descripción del nuevo escenario de prueba"""
       
       # Lógica de prueba
       laraigo_page.open_chat()
       respuesta = laraigo_page.send_message("Mi mensaje de prueba")
       
       # Verificación
       assert condicion, "Mensaje de error"
       
       # Guardar datos para el reporte
       test_data(sent_message="Mi mensaje", response_text=respuesta)
   ```

2. Documentar el nuevo caso en `TEST_CASES_LARAIGO.md`

### Pruebas Parametrizadas

Para probar múltiples variantes de un mismo escenario:

```python
@pytest.mark.laraigo
@pytest.mark.parametrize(
    "mensaje,respuesta_esperada",
    [
        ("Hola", "Hola Blanquiazul"),
        ("Buenos días", "Hola Blanquiazul"),
        # Más combinaciones
    ],
)
def test_saludos_parametrizados(laraigo_page, mensaje, respuesta_esperada, test_data):
    laraigo_page.open_chat()
    respuesta = laraigo_page.send_message(mensaje)
    
    assert any(respuesta_esperada in r for r in respuesta)
    test_data(sent_message=mensaje, response_text=respuesta)
```