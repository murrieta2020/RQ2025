# Web Scraper - Requisitoriados Recompensas.pe

Sistema de web scraping para extraer información de requisitoriados desde https://recompensas.pe/requisitoriados

## 📋 Características

- ✅ Búsqueda por nombre o apellido
- ✅ Extracción de datos completos (nombre, foto, recompensa, estado, sexo, lugar de RO, delitos)
- ✅ Descarga automática de fotos
- ✅ Exportación a JSON y CSV
- ✅ Soporte para búsquedas múltiples
- ✅ Manejo de errores y reintentos
- ✅ Logs detallados del progreso
- ✅ Esperas explícitas para contenido dinámico

## 🚀 Instalación

### Requisitos previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de instalación

1. **Clonar o descargar el repositorio**

```bash
cd scraper
```

2. **Crear un entorno virtual (recomendado)**

```bash
python -m venv venv

# En Windows:
venv\Scripts\activate

# En Linux/Mac:
source venv/bin/activate
```

3. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

4. **Instalar navegadores de Playwright**

```bash
playwright install chromium
```

## 📖 Uso

### Script de Ejecución Automática

Para realizar una búsqueda automática de "william peter loayza mamani" con resultados formateados:

```bash
python run_search.py
```

Este script:
- ✅ Ejecuta automáticamente la búsqueda sin interacción del usuario
- ✅ Muestra los resultados con formato visual y emojis
- ✅ Exporta automáticamente a JSON y CSV
- ✅ Descarga las fotos de los requisitoriados
- ✅ Muestra un resumen completo al finalizar

### Modo Interactivo

Ejecuta el script principal:

```bash
python scraper.py
```

El script te presentará dos opciones:

1. **Búsqueda simple**: Buscar un solo nombre o apellido
2. **Búsquedas múltiples**: Buscar varios nombres separados por comas

### Uso como Módulo

También puedes importar y usar el scraper en tus propios scripts:

```python
from scraper import RequisitoriadosScraper

# Crear instancia
scraper = RequisitoriadosScraper()

# Búsqueda simple
resultados = scraper.buscar_requisitoriado("LOAYZA")

# Búsquedas múltiples
nombres = ["LOAYZA", "MAMANI", "GONZALES"]
todos_resultados = scraper.buscar_multiples(nombres)

# Exportar resultados
scraper.exportar_json("mis_resultados.json")
scraper.exportar_csv("mis_resultados.csv")
```

## 📂 Estructura de Salida

```
/scraper
  /output
    - resultados.json       # Resultados en formato JSON
    - resultados.csv        # Resultados en formato CSV
    /fotos                  # Fotos descargadas de los requisitoriados
      - William_Peter_Loayza_Mamani.jpg
      - ...
```

## 📊 Formato de Datos

### JSON

```json
[
  {
    "nombre_completo": "William Peter Loayza Mamani",
    "foto_url": "https://recompensas.pe/assets/images/...",
    "foto_local": "scraper/output/fotos/William_Peter_Loayza_Mamani.jpg",
    "recompensa": "S/ 20,000",
    "estado": "Requisitoriado",
    "sexo": "Masculino",
    "lugar_ro": "CUSCO - CUSCO",
    "delitos": "VIOLACIÓN SEXUAL DE MENOR DE EDAD"
  }
]
```

### CSV

El archivo CSV contiene las mismas columnas que el JSON, separadas por comas.

## 🔧 Configuración Avanzada

### Cambiar tiempo de espera

En el código, puedes ajustar los timeouts:

```python
# En scraper.py, método buscar_requisitoriado
page.goto(self.BASE_URL, wait_until='networkidle', timeout=60000)  # 60 segundos
```

### Cambiar número de reintentos

```python
resultados = scraper.buscar_requisitoriado("NOMBRE", max_retries=5)
```

### Modo headless

Por defecto, el navegador se ejecuta en modo headless (sin ventana visible). Para ver el navegador:

```python
# En scraper.py, línea ~202
browser = p.chromium.launch(headless=False)  # Cambiar a False
```

## 🐛 Solución de Problemas

### Error: "Playwright no encontrado"

```bash
pip install playwright
playwright install chromium
```

### Error: "No se encontraron resultados"

- Verifica que la página esté accesible: https://recompensas.pe/requisitoriados
- Intenta con otro nombre o apellido más común
- Revisa los logs para ver detalles del error

### Error: "Timeout"

- La página puede estar lenta, aumenta el timeout
- Verifica tu conexión a internet
- El sitio podría estar caído temporalmente

### Las fotos no se descargan

- Verifica que tengas acceso a internet
- Algunas URLs de imágenes pueden estar rotas
- Revisa los logs para ver errores específicos

## 📝 Notas Importantes

- La página usa Angular, por lo que requiere esperas explícitas
- El scraper implementa retry logic para manejar páginas lentas
- Los resultados se guardan automáticamente en la carpeta `output`
- Las fotos se descargan con nombres seguros (sin caracteres especiales)
- El scraper respeta la estructura de la página y no realiza acciones invasivas

## ⚖️ Consideraciones Legales

- Este scraper es solo para fines educativos y de investigación
- Respeta los términos de servicio del sitio web
- No hagas scraping masivo que pueda afectar el rendimiento del sitio
- La información extraída es de dominio público

## 🤝 Contribuciones

Si encuentras bugs o quieres mejorar el scraper:

1. Reporta el issue
2. Sugiere mejoras
3. Envía un pull request

## 📄 Licencia

Este proyecto es de código abierto y está disponible para uso educativo.

## 📞 Soporte

Si tienes problemas:

1. Revisa la sección de "Solución de Problemas"
2. Verifica los logs del scraper
3. Abre un issue en el repositorio

---

**Versión**: 1.0.0  
**Última actualización**: 2025-10-14
