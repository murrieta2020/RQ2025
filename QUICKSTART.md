# 🚀 Guía de Inicio Rápido

Esta guía te ayudará a empezar a usar el scraper de requisitoriados en menos de 5 minutos.

## ⚡ Instalación Rápida

```bash
# 1. Navegar al directorio del scraper
cd scraper

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Instalar navegador Playwright
playwright install chromium
```

## 💻 Uso Básico

### Opción 1: Modo Interactivo (Recomendado para principiantes)

```bash
python scraper.py
```

El script te preguntará:
1. Si quieres hacer una búsqueda simple o múltiple
2. El nombre o apellido a buscar
3. Automáticamente descargará fotos y exportará resultados

### Opción 2: Ejemplos Predefinidos

```bash
python example.py
```

Este script incluye varios ejemplos que puedes usar como plantilla.

### Opción 3: Uso como Módulo de Python

```python
from scraper import RequisitoriadosScraper

# Crear scraper
scraper = RequisitoriadosScraper()

# Buscar
resultados = scraper.buscar_requisitoriado("LOAYZA")

# Guardar
scraper.resultados = resultados
scraper.exportar_json()
scraper.exportar_csv()
```

## 📂 ¿Dónde encuentro los resultados?

Después de ejecutar el scraper, encontrarás:

```
/scraper/output
  ├── resultados.json    # Datos en formato JSON
  ├── resultados.csv     # Datos en formato CSV
  └── /fotos            # Fotos descargadas
      ├── persona1.jpg
      ├── persona2.jpg
      └── ...
```

## 🔍 Ejemplo de Salida

### JSON
```json
{
  "nombre_completo": "William Peter Loayza Mamani",
  "recompensa": "S/ 20,000",
  "estado": "Requisitoriado",
  "sexo": "Masculino",
  "lugar_ro": "CUSCO - CUSCO",
  "delitos": "VIOLACIÓN SEXUAL DE MENOR DE EDAD"
}
```

### CSV
```
nombre_completo,recompensa,estado,sexo,lugar_ro,delitos
William Peter Loayza Mamani,"S/ 20,000",Requisitoriado,Masculino,CUSCO - CUSCO,VIOLACIÓN SEXUAL DE MENOR DE EDAD
```

## ⚠️ Solución de Problemas Comunes

### Error: "playwright not found"
```bash
pip install playwright
playwright install chromium
```

### Error: "No se encontraron resultados"
- Verifica tu conexión a internet
- Intenta con un nombre más común (ej: "GARCIA", "LOPEZ")
- Revisa que el sitio https://recompensas.pe/requisitoriados esté accesible

### El navegador se abre pero no hace nada
- Aumenta el timeout en el código (ver documentación completa)
- Verifica tu conexión a internet

## 📚 Siguiente Paso

Para información más detallada, consulta:
- [README completo del scraper](scraper/README.md)
- [Código de ejemplo](scraper/example.py)
- [README principal](README.md)

## 💡 Consejos

1. **Primera vez**: Usa el modo interactivo (`python scraper.py`)
2. **Búsquedas múltiples**: Usa nombres comunes separados por comas
3. **Debugging**: Los logs te ayudarán a entender qué está pasando
4. **Personalización**: Revisa el código y adapta según tus necesidades

## 🤝 ¿Necesitas ayuda?

Si tienes problemas:
1. Revisa los logs del scraper (se muestran en consola)
2. Consulta la [documentación completa](scraper/README.md)
3. Verifica que el sitio web esté accesible
4. Abre un issue en el repositorio

---

¡Listo! Ya puedes empezar a usar el scraper. 🎉
