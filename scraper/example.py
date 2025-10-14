#!/usr/bin/env python3
"""
Ejemplo de uso del scraper de requisitoriados

Este script muestra diferentes formas de usar el scraper:
1. Búsqueda simple
2. Búsquedas múltiples
3. Uso como módulo
"""

from scraper import RequisitoriadosScraper
import json


def ejemplo_busqueda_simple():
    """Ejemplo de búsqueda simple"""
    print("\n" + "=" * 60)
    print("EJEMPLO 1: Búsqueda Simple")
    print("=" * 60)
    
    # Crear instancia del scraper
    scraper = RequisitoriadosScraper()
    
    # Buscar un nombre o apellido
    nombre = "LOAYZA"  # Cambia esto por el nombre que quieras buscar
    print(f"\nBuscando: {nombre}")
    
    resultados = scraper.buscar_requisitoriado(nombre)
    
    if resultados:
        print(f"\n✓ Se encontraron {len(resultados)} resultados:")
        for i, persona in enumerate(resultados, 1):
            print(f"\n{i}. {persona['nombre_completo']}")
            print(f"   Recompensa: {persona['recompensa']}")
            print(f"   Estado: {persona['estado']}")
            print(f"   Sexo: {persona['sexo']}")
            print(f"   Lugar de RO: {persona['lugar_ro']}")
            print(f"   Delito(s): {persona['delitos']}")
        
        # Guardar resultados
        scraper.resultados = resultados
        scraper.exportar_json(f"busqueda_{nombre.lower()}.json")
        scraper.exportar_csv(f"busqueda_{nombre.lower()}.csv")
        print(f"\n✓ Resultados guardados en scraper/output/")
    else:
        print("\n✗ No se encontraron resultados")


def ejemplo_busquedas_multiples():
    """Ejemplo de búsquedas múltiples"""
    print("\n" + "=" * 60)
    print("EJEMPLO 2: Búsquedas Múltiples")
    print("=" * 60)
    
    # Crear instancia del scraper
    scraper = RequisitoriadosScraper()
    
    # Lista de nombres a buscar
    nombres = ["LOAYZA", "MAMANI", "GONZALES"]
    print(f"\nBuscando {len(nombres)} nombres: {', '.join(nombres)}")
    
    todos_resultados = scraper.buscar_multiples(nombres)
    
    if todos_resultados:
        print(f"\n✓ Se encontraron {len(todos_resultados)} resultados en total")
        
        # Mostrar resumen
        print("\nResumen de resultados:")
        for i, persona in enumerate(todos_resultados, 1):
            print(f"{i}. {persona['nombre_completo']} - {persona['recompensa']}")
        
        # Exportar todo junto
        scraper.exportar_json("busqueda_multiple.json")
        scraper.exportar_csv("busqueda_multiple.csv")
        print(f"\n✓ Todos los resultados guardados en scraper/output/")
    else:
        print("\n✗ No se encontraron resultados")


def ejemplo_uso_programatico():
    """Ejemplo de uso programático del scraper"""
    print("\n" + "=" * 60)
    print("EJEMPLO 3: Uso Programático")
    print("=" * 60)
    
    # Crear instancia
    scraper = RequisitoriadosScraper()
    
    # Buscar
    nombre = "LOAYZA"
    print(f"\nBuscando: {nombre}")
    resultados = scraper.buscar_requisitoriado(nombre, max_retries=2)
    
    # Procesar resultados
    if resultados:
        print(f"\n✓ Se encontraron {len(resultados)} resultados")
        
        # Analizar datos
        total_recompensa = 0
        for persona in resultados:
            # Extraer monto de recompensa (ej: "S/ 20,000" -> 20000)
            if persona['recompensa'] != "N/A":
                try:
                    monto_str = persona['recompensa'].replace('S/', '').replace(',', '').strip()
                    monto = float(monto_str)
                    total_recompensa += monto
                except:
                    pass
        
        print(f"\nEstadísticas:")
        print(f"- Total de personas: {len(resultados)}")
        print(f"- Recompensa total: S/ {total_recompensa:,.0f}")
        
        # Filtrar por delito específico
        delito_buscar = "VIOLACIÓN"
        personas_delito = [p for p in resultados if delito_buscar.upper() in p['delitos'].upper()]
        print(f"- Personas con delito '{delito_buscar}': {len(personas_delito)}")
        
        # Guardar solo los filtrados
        scraper.resultados = personas_delito
        scraper.exportar_json(f"filtrado_{delito_buscar.lower()}.json")
        
        print(f"\n✓ Resultados filtrados guardados")
    else:
        print("\n✗ No se encontraron resultados")


def main():
    """Ejecutar todos los ejemplos"""
    print("\n" + "=" * 60)
    print("EJEMPLOS DE USO DEL SCRAPER")
    print("=" * 60)
    
    print("\n⚠️  NOTA: Estos ejemplos requieren conexión al sitio web")
    print("   https://recompensas.pe/requisitoriados")
    print("   y que Playwright esté correctamente instalado.")
    
    print("\n¿Qué ejemplo deseas ejecutar?")
    print("1. Búsqueda simple")
    print("2. Búsquedas múltiples")
    print("3. Uso programático")
    print("4. Todos los ejemplos")
    print("0. Salir")
    
    opcion = input("\nSelecciona una opción (0-4): ").strip()
    
    if opcion == "1":
        ejemplo_busqueda_simple()
    elif opcion == "2":
        ejemplo_busquedas_multiples()
    elif opcion == "3":
        ejemplo_uso_programatico()
    elif opcion == "4":
        ejemplo_busqueda_simple()
        ejemplo_busquedas_multiples()
        ejemplo_uso_programatico()
    elif opcion == "0":
        print("\n👋 Adiós!")
        return
    else:
        print("\n✗ Opción no válida")
        return
    
    print("\n" + "=" * 60)
    print("EJEMPLOS COMPLETADOS")
    print("=" * 60)


if __name__ == "__main__":
    main()
