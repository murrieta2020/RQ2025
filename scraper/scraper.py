#!/usr/bin/env python3
"""
Web Scraper para https://recompensas.pe/requisitoriados
Extrae información de personas requisitoriadas
"""

import json
import logging
import os
import time
from pathlib import Path
from typing import List, Dict, Optional
import requests
import pandas as pd
from playwright.sync_api import sync_playwright, Page, TimeoutError as PlaywrightTimeoutError


# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RequisitoriadosScraper:
    """Scraper para extraer información de requisitoriados"""
    
    BASE_URL = "https://recompensas.pe/requisitoriados"
    OUTPUT_DIR = Path(__file__).parent / "output"
    FOTOS_DIR = OUTPUT_DIR / "fotos"
    
    def __init__(self):
        """Inicializa el scraper"""
        self._setup_directories()
        self.resultados = []
        
    def _setup_directories(self):
        """Crea los directorios necesarios"""
        self.OUTPUT_DIR.mkdir(exist_ok=True)
        self.FOTOS_DIR.mkdir(exist_ok=True)
        logger.info(f"Directorios creados: {self.OUTPUT_DIR}, {self.FOTOS_DIR}")
    
    def _wait_for_results(self, page: Page, timeout: int = 10000) -> bool:
        """
        Espera a que los resultados se carguen
        
        Args:
            page: Página de Playwright
            timeout: Tiempo máximo de espera en milisegundos
            
        Returns:
            True si se encontraron resultados, False si no hay resultados
        """
        try:
            # Esperar a que aparezca algún resultado o mensaje de "no resultados"
            page.wait_for_selector(
                'div.card, div.alert, div.no-results',
                timeout=timeout
            )
            time.sleep(2)  # Espera adicional para que se cargue todo el contenido
            return True
        except PlaywrightTimeoutError:
            logger.warning("Timeout esperando resultados")
            return False
    
    def _extract_card_data(self, card) -> Optional[Dict[str, str]]:
        """
        Extrae datos de una tarjeta de requisitoriado
        
        Args:
            card: Elemento de la tarjeta
            
        Returns:
            Diccionario con los datos extraídos o None si hay error
        """
        try:
            data = {}
            
            # Extraer nombre completo
            nombre_elem = card.query_selector('h5.card-title, h4.card-title, div.card-title, p.fw-bold')
            data['nombre_completo'] = nombre_elem.inner_text().strip() if nombre_elem else "N/A"
            
            # Extraer foto URL
            img_elem = card.query_selector('img')
            data['foto_url'] = img_elem.get_attribute('src') if img_elem else "N/A"
            
            # Extraer recompensa
            recompensa_elem = card.query_selector('p.text-danger, span.text-danger, div.text-danger, h3.text-danger, h4.text-danger')
            if not recompensa_elem:
                # Buscar en todo el texto que contenga "S/"
                all_text = card.inner_text()
                for line in all_text.split('\n'):
                    if 'S/' in line or 's/' in line.lower():
                        data['recompensa'] = line.strip()
                        break
                else:
                    data['recompensa'] = "N/A"
            else:
                data['recompensa'] = recompensa_elem.inner_text().strip()
            
            # Extraer estado, sexo, lugar de RO y delitos
            # Estos datos suelen estar en el cuerpo de la tarjeta
            card_body = card.query_selector('div.card-body')
            if card_body:
                body_text = card_body.inner_text()
                lines = body_text.split('\n')
                
                data['estado'] = "N/A"
                data['sexo'] = "N/A"
                data['lugar_ro'] = "N/A"
                data['delitos'] = "N/A"
                
                for i, line in enumerate(lines):
                    line_lower = line.lower().strip()
                    
                    if 'estado' in line_lower and i + 1 < len(lines):
                        # El valor puede estar en la misma línea o en la siguiente
                        if ':' in line:
                            data['estado'] = line.split(':', 1)[1].strip()
                        elif i + 1 < len(lines):
                            data['estado'] = lines[i + 1].strip()
                    
                    elif 'sexo' in line_lower:
                        if ':' in line:
                            data['sexo'] = line.split(':', 1)[1].strip()
                        elif i + 1 < len(lines):
                            data['sexo'] = lines[i + 1].strip()
                    
                    elif 'lugar' in line_lower and 'ro' in line_lower:
                        if ':' in line:
                            data['lugar_ro'] = line.split(':', 1)[1].strip()
                        elif i + 1 < len(lines):
                            data['lugar_ro'] = lines[i + 1].strip()
                    
                    elif 'delito' in line_lower:
                        if ':' in line:
                            data['delitos'] = line.split(':', 1)[1].strip()
                        elif i + 1 < len(lines):
                            # El delito puede ocupar múltiples líneas
                            delito_lines = []
                            for j in range(i + 1, len(lines)):
                                next_line = lines[j].strip()
                                if next_line and not any(k in next_line.lower() for k in ['estado', 'sexo', 'lugar', 'recompensa']):
                                    delito_lines.append(next_line)
                                else:
                                    break
                            if delito_lines:
                                data['delitos'] = ' '.join(delito_lines)
            else:
                # Si no hay card-body, buscar en toda la tarjeta
                data['estado'] = "N/A"
                data['sexo'] = "N/A"
                data['lugar_ro'] = "N/A"
                data['delitos'] = "N/A"
            
            logger.info(f"Datos extraídos para: {data['nombre_completo']}")
            return data
            
        except Exception as e:
            logger.error(f"Error extrayendo datos de tarjeta: {e}")
            return None
    
    def _download_photo(self, foto_url: str, nombre: str) -> str:
        """
        Descarga la foto de un requisitoriado
        
        Args:
            foto_url: URL de la foto
            nombre: Nombre del requisitoriado (para el nombre del archivo)
            
        Returns:
            Ruta donde se guardó la foto o "N/A" si falla
        """
        if foto_url == "N/A" or not foto_url:
            return "N/A"
        
        try:
            # Crear nombre de archivo seguro
            safe_name = "".join(c for c in nombre if c.isalnum() or c in (' ', '_')).rstrip()
            safe_name = safe_name.replace(' ', '_')[:50]  # Limitar longitud
            
            # Determinar extensión
            ext = '.jpg'
            if foto_url.lower().endswith('.png'):
                ext = '.png'
            elif foto_url.lower().endswith('.jpeg'):
                ext = '.jpeg'
            
            filename = f"{safe_name}{ext}"
            filepath = self.FOTOS_DIR / filename
            
            # Descargar imagen
            # Si la URL es relativa, construir URL completa
            if foto_url.startswith('/'):
                foto_url = f"https://recompensas.pe{foto_url}"
            elif not foto_url.startswith('http'):
                foto_url = f"https://recompensas.pe/{foto_url}"
            
            response = requests.get(foto_url, timeout=30)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            logger.info(f"Foto descargada: {filename}")
            return str(filepath.relative_to(self.OUTPUT_DIR.parent))
            
        except Exception as e:
            logger.error(f"Error descargando foto {foto_url}: {e}")
            return "N/A"
    
    def buscar_requisitoriado(self, nombre_busqueda: str, max_retries: int = 3) -> List[Dict[str, str]]:
        """
        Busca requisitoriados por nombre o apellido
        
        Args:
            nombre_busqueda: Nombre o apellido a buscar
            max_retries: Número máximo de reintentos
            
        Returns:
            Lista de diccionarios con los datos encontrados
        """
        logger.info(f"Buscando: {nombre_busqueda}")
        
        for intento in range(max_retries):
            try:
                with sync_playwright() as p:
                    # Lanzar navegador
                    browser = p.chromium.launch(headless=True)
                    context = browser.new_context(
                        viewport={'width': 1920, 'height': 1080}
                    )
                    page = context.new_page()
                    
                    # Navegar a la página
                    logger.info(f"Navegando a {self.BASE_URL}")
                    page.goto(self.BASE_URL, wait_until='networkidle', timeout=60000)
                    
                    # Esperar a que cargue el formulario
                    page.wait_for_selector('input[name="nombreCompleto"]', timeout=30000)
                    
                    # Ingresar nombre en el campo de búsqueda
                    logger.info("Ingresando nombre en el formulario")
                    page.fill('input[name="nombreCompleto"]', nombre_busqueda)
                    
                    # Hacer clic en el botón de buscar
                    logger.info("Haciendo clic en buscar")
                    search_button = page.query_selector('button.btn.btn-danger, button[type="submit"]')
                    if search_button:
                        search_button.click()
                    else:
                        logger.error("No se encontró el botón de búsqueda")
                        browser.close()
                        return []
                    
                    # Esperar a que carguen los resultados
                    if not self._wait_for_results(page):
                        logger.warning("No se cargaron resultados")
                        browser.close()
                        return []
                    
                    # Extraer resultados
                    resultados_busqueda = []
                    
                    # Buscar tarjetas de resultados
                    cards = page.query_selector_all('div.card')
                    logger.info(f"Se encontraron {len(cards)} tarjetas")
                    
                    if len(cards) == 0:
                        # Intentar con otros selectores
                        cards = page.query_selector_all('div.resultado, div.item, article')
                        logger.info(f"Intento alternativo: {len(cards)} elementos encontrados")
                    
                    for card in cards:
                        data = self._extract_card_data(card)
                        if data and data['nombre_completo'] != "N/A":
                            # Descargar foto
                            data['foto_local'] = self._download_photo(
                                data['foto_url'], 
                                data['nombre_completo']
                            )
                            resultados_busqueda.append(data)
                    
                    browser.close()
                    
                    if resultados_busqueda:
                        logger.info(f"Se encontraron {len(resultados_busqueda)} resultados")
                        return resultados_busqueda
                    else:
                        logger.warning("No se encontraron resultados válidos")
                        return []
                        
            except Exception as e:
                logger.error(f"Error en intento {intento + 1}/{max_retries}: {e}")
                if intento < max_retries - 1:
                    logger.info(f"Reintentando en 5 segundos...")
                    time.sleep(5)
                else:
                    logger.error("Se agotaron los reintentos")
                    return []
        
        return []
    
    def buscar_multiples(self, nombres: List[str]) -> List[Dict[str, str]]:
        """
        Realiza búsquedas múltiples
        
        Args:
            nombres: Lista de nombres a buscar
            
        Returns:
            Lista con todos los resultados encontrados
        """
        todos_resultados = []
        
        for nombre in nombres:
            resultados = self.buscar_requisitoriado(nombre)
            todos_resultados.extend(resultados)
            time.sleep(2)  # Pausa entre búsquedas
        
        self.resultados = todos_resultados
        return todos_resultados
    
    def exportar_json(self, filename: str = "resultados.json") -> str:
        """
        Exporta resultados a JSON
        
        Args:
            filename: Nombre del archivo
            
        Returns:
            Ruta del archivo creado
        """
        filepath = self.OUTPUT_DIR / filename
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.resultados, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Resultados exportados a JSON: {filepath}")
            return str(filepath)
        except Exception as e:
            logger.error(f"Error exportando a JSON: {e}")
            return ""
    
    def exportar_csv(self, filename: str = "resultados.csv") -> str:
        """
        Exporta resultados a CSV
        
        Args:
            filename: Nombre del archivo
            
        Returns:
            Ruta del archivo creado
        """
        filepath = self.OUTPUT_DIR / filename
        
        try:
            if not self.resultados:
                logger.warning("No hay resultados para exportar")
                return ""
            
            df = pd.DataFrame(self.resultados)
            df.to_csv(filepath, index=False, encoding='utf-8-sig')
            
            logger.info(f"Resultados exportados a CSV: {filepath}")
            return str(filepath)
        except Exception as e:
            logger.error(f"Error exportando a CSV: {e}")
            return ""


def main():
    """Función principal con ejemplo de uso"""
    print("=" * 60)
    print("Web Scraper - Requisitoriados Recompensas.pe")
    print("=" * 60)
    
    # Crear instancia del scraper
    scraper = RequisitoriadosScraper()
    
    # Modo interactivo
    print("\nModo de búsqueda:")
    print("1. Búsqueda simple")
    print("2. Búsquedas múltiples")
    opcion = input("\nSelecciona una opción (1 o 2): ").strip()
    
    if opcion == "1":
        # Búsqueda simple
        nombre = input("\nIngresa nombre o apellido a buscar: ").strip()
        if nombre:
            resultados = scraper.buscar_requisitoriado(nombre)
            scraper.resultados = resultados
            
            if resultados:
                print(f"\n✓ Se encontraron {len(resultados)} resultados")
                for i, r in enumerate(resultados, 1):
                    print(f"\n{i}. {r['nombre_completo']}")
                    print(f"   Recompensa: {r['recompensa']}")
                    print(f"   Estado: {r['estado']}")
                    print(f"   Delito(s): {r['delitos']}")
            else:
                print("\n✗ No se encontraron resultados")
    
    elif opcion == "2":
        # Búsquedas múltiples
        print("\nIngresa los nombres a buscar (separados por coma):")
        nombres_input = input().strip()
        nombres = [n.strip() for n in nombres_input.split(',') if n.strip()]
        
        if nombres:
            print(f"\nBuscando {len(nombres)} nombres...")
            resultados = scraper.buscar_multiples(nombres)
            
            if resultados:
                print(f"\n✓ Se encontraron {len(resultados)} resultados en total")
            else:
                print("\n✗ No se encontraron resultados")
    else:
        print("Opción no válida")
        return
    
    # Exportar resultados
    if scraper.resultados:
        print("\n" + "=" * 60)
        print("Exportando resultados...")
        json_file = scraper.exportar_json()
        csv_file = scraper.exportar_csv()
        
        print(f"\n✓ Resultados guardados:")
        print(f"  - JSON: {json_file}")
        print(f"  - CSV: {csv_file}")
        print(f"  - Fotos: {scraper.FOTOS_DIR}")
        print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
