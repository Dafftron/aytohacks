#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de inicio rapido - Menu interactivo para Aytohacks
"""

import os
import sys

def clear_screen():
    """Limpia la pantalla"""
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu():
    """Muestra el menu principal"""
    clear_screen()
    print("=" * 70)
    print("                    AYTOHACKS - MENU PRINCIPAL")
    print("=" * 70)
    print("")
    print("  [1] Verificar instalacion")
    print("  [2] Buscar informacion de ayuntamientos (Toledo completo)")
    print("  [3] Buscar primeros 20 ayuntamientos (prueba)")
    print("  [4] Fusionar archivos Excel")
    print("  [5] Enviar correos automatizados")
    print("  [6] Prueba de envio de correo")
    print("")
    print("  [7] Ver instrucciones completas")
    print("  [8] Ver resumen de configuracion")
    print("")
    print("  [0] Salir")
    print("")
    print("=" * 70)

def ejecutar_script(script_name):
    """Ejecuta un script de Python"""
    print(f"\nEjecutando {script_name}...\n")
    print("=" * 70)
    os.system(f'python {script_name}')
    print("\n" + "=" * 70)
    input("\nPresiona ENTER para volver al menu...")

def ver_archivo(archivo):
    """Muestra el contenido de un archivo"""
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            print(f.read())
    except:
        with open(archivo, 'r', encoding='latin-1') as f:
            print(f.read())
    input("\nPresiona ENTER para volver al menu...")

def main():
    """Funcion principal del menu"""
    while True:
        mostrar_menu()

        opcion = input("  Selecciona una opcion: ").strip()

        if opcion == '1':
            ejecutar_script('test_instalacion.py')

        elif opcion == '2':
            print("\n" + "=" * 70)
            print("ATENCION: Este proceso puede tardar 10-15 minutos")
            print("Se scrapean 204 ayuntamientos de Toledo")
            print("=" * 70)
            confirmar = input("\nDeseas continuar? (s/n): ").strip().lower()
            if confirmar == 's':
                ejecutar_script('completar_todos.py')

        elif opcion == '3':
            ejecutar_script('buscar_primeros_20.py')

        elif opcion == '4':
            print("\n" + "=" * 70)
            print("NOTA: Necesitas los archivos Excel fuente en datos/")
            print("  - Direcciones_Toledo_completo.xlsx")
            print("  - comparativa_emails_toledo.xlsx")
            print("=" * 70)
            confirmar = input("\nDeseas continuar? (s/n): ").strip().lower()
            if confirmar == 's':
                ejecutar_script('fusionar_excels.py')

        elif opcion == '5':
            print("\n" + "=" * 70)
            print("NOTA: Necesitas tener Thunderbird instalado y configurado")
            print("Cada email requerira confirmacion manual")
            print("=" * 70)
            confirmar = input("\nDeseas continuar? (s/n): ").strip().lower()
            if confirmar == 's':
                ejecutar_script('enviar_correos_thunderbird.py')

        elif opcion == '6':
            ejecutar_script('prueba_envio.py')

        elif opcion == '7':
            clear_screen()
            ver_archivo('INSTRUCCIONES.md')

        elif opcion == '8':
            clear_screen()
            ver_archivo('RESUMEN_CONFIGURACION.txt')

        elif opcion == '0':
            print("\nGracias por usar Aytohacks!")
            print("TecnoHita Instrumentacion - david@tecnohita.com\n")
            sys.exit(0)

        else:
            input("\nOpcion no valida. Presiona ENTER para continuar...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido por el usuario.")
        print("Gracias por usar Aytohacks!\n")
        sys.exit(0)
