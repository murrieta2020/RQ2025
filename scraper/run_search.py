#!/usr/bin/env python3
"""
Script de ejecución automática para buscar requisitoriados en recompensas.pe

Ejecuta una búsqueda automática con el nombre "william peter loayza mamani"
y muestra los resultados de forma clara y formateada.

Uso:
    python run_search.py
"""

import sys
from pathlib import Path
from scraper import RequisitoriadosScraper


def print_separator(char="=", length=60):
    """Imprime un separador visual"""
    print(char * length)


def print_header(title):
    """Imprime un encabezado formateado"""
    print_separator()
    print(title)
    print_separator()


def print_person_details(persona, index):
    """Imprime los detalles de una persona de forma formateada"""
    print(f"\n{index}. Nombre: {persona['nombre_completo']}")
    print(f"   💰 Recompensa: {persona['recompensa']}")
    print(f"   📍 Estado: {persona['estado']}")
    print(f"   👤 Sexo: {persona['sexo']}")
    print(f"   🗺️  Lugar RO: {persona['lugar_ro']}")
    print(f"   ⚖️  Delitos: {persona['delitos']}")
    print(f"   📸 Foto: {persona.get('foto_local', 'N/A')}")


def main():
    """Función principal del script"""
    try:
        # Encabezado principal
        print()
        print_header("🔍 BUSCANDO REQUISITORIADOS - RECOMPENSAS.PE")
        
        # Nombre a buscar
        nombre_busqueda = "william peter loayza mamani"
        print(f"\nBúsqueda: {nombre_busqueda}")
        print()
        
        # Crear instancia del scraper
        print("🚀 Inicializando scraper...")
        scraper = RequisitoriadosScraper()
        
        # Ejecutar búsqueda
        print(f"🔎 Buscando '{nombre_busqueda}'...")
        print()
        resultados = scraper.buscar_requisitoriado(nombre_busqueda)
        
        # Actualizar resultados en el scraper para exportación
        scraper.resultados = resultados
        
        # Mostrar resultados
        print()
        print_header(f"📊 RESULTADOS ENCONTRADOS: {len(resultados)}")
        
        if resultados:
            # Mostrar cada persona encontrada
            for i, persona in enumerate(resultados, 1):
                print_person_details(persona, i)
            
            # Exportar a JSON y CSV
            print()
            print_header("💾 EXPORTANDO RESULTADOS")
            print()
            
            print("📝 Generando archivos...")
            json_path = scraper.exportar_json("william_peter_loayza_mamani.json")
            csv_path = scraper.exportar_csv("william_peter_loayza_mamani.csv")
            
            # Resumen final
            print()
            print_header("💾 ARCHIVOS GENERADOS")
            print()
            
            if json_path:
                print(f"✓ JSON: {json_path}")
            else:
                print("✗ JSON: Error al generar archivo")
            
            if csv_path:
                print(f"✓ CSV: {csv_path}")
            else:
                print("✗ CSV: Error al generar archivo")
            
            print(f"✓ Fotos: {scraper.FOTOS_DIR}")
            
            print()
            print_separator()
            print(f"✅ Proceso completado exitosamente. Total: {len(resultados)} resultado(s)")
            print_separator()
            
        else:
            print("\n⚠️  No se encontraron resultados para la búsqueda.")
            print()
            print_separator()
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Búsqueda cancelada por el usuario.")
        print_separator()
        return 1
        
    except Exception as e:
        print("\n")
        print_header("❌ ERROR")
        print(f"\n⚠️  Ocurrió un error durante la ejecución: {e}")
        print("\n💡 Sugerencias:")
        print("   - Verifica tu conexión a internet")
        print("   - Asegúrate de que Playwright esté correctamente instalado")
        print("   - Intenta ejecutar: playwright install chromium")
        print("\n")
        print_separator()
        
        # Mostrar traceback para debug
        import traceback
        print("\n🔍 Detalles del error:")
        print(traceback.format_exc())
        print_separator()
        
        return 1


if __name__ == "__main__":
    sys.exit(main())
