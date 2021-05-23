# -*- encoding: utf-8 -*-

# Julia Fernanda Ramirez Oviedo
# Silvestre Martinez Cervantes

import argparse
import os
import logging
import socket
import sys
import subprocess
from prettytable import PrettyTable
from funciones import recorrer_carpeta
from funciones import virus_total
from funciones import escaneo_puertos
from funciones import scrapping


if __name__ == '__main__':
    # Registro de errores
    logging.basicConfig(filename="pia.log", level=logging.INFO)
    # Establecer argumentos argparse
    description = """Ejemplos de uso:
    El script puede hacer 5 tareas diferentes en total:
    
    py main_pia.py hash -r 'ruta'
    py main_pia.py escaneo -t 'ip' -p 'puerto'
    py main_pia.py exe -r 'ruta' -k 'api_key'
    py main_pia.py scr -l 'link' -n '#imagenes'
    py main_pia.py estatus

    IMPORTANTE:

    Tambien para ejecutar la tarea exe necesita tener una cuenta
    en www.virustotal.com ya que necesita de una key para poder
    realizar la tarea"""

    parser = argparse.ArgumentParser(description='PIA PC',
                                     epilog=description,
                                     formatter_class=argparse.
                                     RawDescriptionHelpFormatter)

    subparser = parser.add_subparsers(dest = "tarea")

    hash_parser = subparser.add_parser("hash", help="""Obtener valor hash de
                                     archivos""")

    hash_parser.add_argument("-r", metavar="RUTA", dest="ruta", help="""Ingresar
                             ruta de carpeta o archivo para obtener hash""",
                             required=True, nargs=1)#Archivo o carpeta

    escaneo_parser = subparser.add_parser("escaneo", help="""Escaneo de
                                          puertos""")

    escaneo_parser.add_argument("-t", metavar="TARGET", dest="target",
                                help="""Ingresar IP separadas por coma.
                                127.0.0.1 por default""", default="127.0.0.1")
                                #Pueden ser varias IP
    escaneo_parser.add_argument("-p", metavar="PUERTOS", dest="puertos")

    exe_parser = subparser.add_parser("exe", help="""Análisis de ejecutables""")

    exe_parser.add_argument("-r", metavar="RUTA", dest="ruta_exe", help="""Ingresar
                            ruta de ejecutable para realizar análisis""",
                            required=True, nargs=1)

    exe_parser.add_argument("-k", metavar="KEY", dest="API_KEY", help="""Ingresar
                            API Key de Virus Total""", required=True, nargs=1)

    scr_parser = subparser.add_parser("scr", help="""Realizar descarga de
                                      imagenes de pagina solicitada""")

    scr_parser.add_argument("-l", metavar="LINK", dest="link", help="""Ingresar
                            URL de pagina""", required=True)

    scr_parser.add_argument("-n", metavar="NUMERO", dest="numero",
                            help="""Ingresar máximo de imagenes a descargar""",
                            required=True)

    scr_parser = subparser.add_parser("estatus", help="""Obtiene estatus de
                                      servicios y procesos""")

    args = parser.parse_args()

    # OBTENCIÓN DE HASH
    # Seleccionar carpeta, validar ruta
    if args.tarea == "hash":
            path = args.ruta[0]
            path_valida = os.path.exists(path)
            while path_valida == False:
                #logging.error(path + " Ruta inexistente")
                path = input("No existe la ruta, ingrese otra ruta: ")
                path_valida = os.path.exists(path)
            file_txt = open("valores_hash.txt", "w")
            file_txt.write("===VALORES HASH DE ARCHIVOS===\n\nRuta: "+path+"\n\n")
            file_txt.write("Nombre de archivo\tValor Hash\n")
            #Manejo de tabla
            tabla_hash = PrettyTable()
            tabla_hash.field_names = ["Archivo", "Valor Hash"]
            recorrer_carpeta(path, file_txt, tabla_hash)
            print("Obtención de valores hash\n", tabla_hash)

    # ESCANEO DE PUERTOS
    if args.tarea == "escaneo":
        try:
            target_ips = args.target.split(",")
            lista_puertos = args.puertos.split(",")
            # Generar txt
            reporte_ips = open("Escaneo_IP.txt", "w")
            # Función con socket para conectar y conocer estado puerto
            escaneo_puertos(target_ips, lista_puertos, reporte_ips)
            logging.info('Escaneo_IP.txt generado')
        except Exception as e:
            logging.error("Ha ocurrido un error: " + str(e))
            print("Ha ocurrido un error: " + str(e))

    # ANÁLISIS DE EJECUTABLE
    if args.tarea == "exe":
        try:
            path = args.ruta_exe[0]
            path_valida = os.path.exists(path)
            while path_valida == False:
                path = input("No existe la ruta, ingrese otra ruta: ")
                path_valida = os.path.exists(path)
                #logging.error(path + " Ruta inexistente")
            if path.endswith(".exe"):
                virus_total(path, args.API_KEY[0])
            else:
                print("El archivo no es un ejecutable, no se puede analizar")
                logging.info(path + ' El archivo no es un ejecutable, no se puede analizar')
        except Exception as e:
            logging.error("Ha ocurrido un error: " + str(e))
            print("Ha ocurrido un error: " + str(e))

    # WEB SCRAPPING IMG
    if args.tarea == "scr":
        link = args.link
        numero = args.numero
        scrapping(link, numero)

    # POWERSHELL ESTATUS DE PROCESOS Y SERVICIOS
    if args.tarea == "estatus":
        # Script POWERSHELL
        try:
            ruta = os.getcwd()
            script_ps = ruta+"\Estatus.ps1"
            lineaPS = "powershell -Executionpolicy ByPass -File "+script_ps
            proceso = subprocess.run(lineaPS)
            logging.info('Ejecutando Estatus.ps1')
            print(proceso)
            logging.info('Procesos.txt generado')
            logging.info('Servicios.txt generado')
        except Exception as e:
            logging.error("Ha ocurrido un error: " + str(e))
            print("Ha ocurrido un error: " + str(e))
