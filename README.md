# RQ2025

Sistema de web scraping para extraer información de requisitoriados desde https://recompensas.pe/requisitoriados

## 📖 Descripción

Este proyecto contiene un sistema completo de web scraping desarrollado en Python que permite:

- Buscar personas requisitoriadas por nombre o apellido
- Extraer información detallada (nombre, foto, recompensa, estado, sexo, lugar de RO, delitos)
- Descargar fotos automáticamente
- Exportar resultados a JSON y CSV
- Realizar búsquedas múltiples
- Manejo robusto de errores y reintentos

## 🚀 Inicio Rápido

### Instalación

```bash
cd scraper
pip install -r requirements.txt
playwright install chromium
```

### Uso

**Búsqueda automática (recomendado):**

```bash
cd scraper
python run_search.py
```

Este script ejecuta automáticamente una búsqueda de "william peter loayza mamani" y muestra los resultados con formato visual.

**Modo interactivo:**

```bash
cd scraper
python scraper.py
```

## 📂 Estructura del Proyecto

```
/scraper
  - scraper.py           # Script principal del scraper
  - run_search.py        # Script de búsqueda automática
  - example.py           # Ejemplos de uso
  - requirements.txt     # Dependencias de Python
  - README.md           # Documentación detallada
  /output              # Directorio de salida
    - resultados.json  # Resultados en formato JSON
    - resultados.csv   # Resultados en formato CSV
    /fotos            # Fotos descargadas
```

## 📚 Documentación

Para instrucciones detalladas de uso, configuración y solución de problemas, consulta [scraper/README.md](scraper/README.md)

## 🛠️ Tecnologías

- **Python 3.8+**
- **Playwright**: Para automatización del navegador y manejo de contenido dinámico
- **Pandas**: Para exportación de datos a CSV
- **Requests**: Para descarga de imágenes

## ✨ Características

- ✅ Script de ejecución automática con salida formateada
- ✅ Interfaz interactiva de línea de comandos
- ✅ Búsqueda simple y múltiple
- ✅ Manejo de páginas dinámicas Angular
- ✅ Retry logic para conexiones lentas
- ✅ Logging detallado
- ✅ Descarga automática de fotos
- ✅ Exportación dual (JSON y CSV)
- ✅ Formato visual con emojis para mejor legibilidad

## 📄 Licencia

Código abierto para fines educativos y de investigación.