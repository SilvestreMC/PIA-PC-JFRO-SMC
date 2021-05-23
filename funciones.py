# -*- encoding: utf-8 -*-

# Julia Fernanda Ramirez Oviedo
# Silvestre Martinez Cervantes

import hashlib
import os
import logging
import socket
import requests
from bs4 import BeautifulSoup
from hashlib import md5
from virus_total_apis import PublicApi
from prettytable import PrettyTable

def obtener_hash(ruta_archivo):
    try:
        archivo_objeto = open(ruta_archivo, "rb")
        archivo = archivo_objeto.read()
        logging.info('Obteniedo hash de '+ str(ruta_archivo))
        hash = hashlib.sha512(archivo)
        hased = hash.hexdigest()
        archivo_objeto.close()
        return hased
    except Exception as e:
        logging.error("Ha ocurrido un error: " + str(e))
        print("Ha ocurrido un error: " + str(e))

def recorrer_carpeta(path, file_txt, tabla_hash):
    file_txt.close()
    try:
    # Solo un archivo
        if os.path.isfile(path) == True:
            hashed = obtener_hash(path)
            nom_archivo = os.path.basename(path)
            # Agregar a archivo TXT
            file_txt = open("valores_hash.txt", "a")
            file_txt.write(nom_archivo+"\t"+hashed+"\n")
            file_txt.close()
            #Agregar valor a la tabla para imprimir
            tabla_hash.add_row([nom_archivo, hashed])
        # Recorrer carpeta, tomar solo archivos
        elif os.path.isdir(path) == True:
            archivos_carpeta = os.listdir(path)
            for archivo in archivos_carpeta:
                nom_archivo = str(archivo)
                ruta_archivo = os.path.join(path, nom_archivo)
                if os.path.isfile(ruta_archivo) == True:
                    hashed = obtener_hash(ruta_archivo)
                    # Agregar a archivo TXT
                    file_txt = open("valores_hash.txt", "a")
                    file_txt.write(nom_archivo+"\t"+hashed+"\n")
                    file_txt.close()
                    #Agregar valor a la tabla para imprimir
                    tabla_hash.add_row([nom_archivo, hashed])
        logging.info('valores_hash.txt generado')
    except Exception as e:
        logging.error("Ha ocurrido un error: " + str(e))
        print("Ha ocurrido un error: " + str(e))

def escaneo_puertos(target_ips, lista_puertos, reporte_ips):
    try:
        # Ciclo para recorrer IPs ingresadas
        for target in target_ips:
            # Ciclo para recorrer lista puertos
            reporte_ips.write("\nEscaneo de puertos para: " + target + "\n")
            print("\nEscaneo de puertos para: ", target)
            logging.info("Escaneo de puertos para: " + target)
            for puerto in range(int(lista_puertos[0]), int(lista_puertos[-1])+1):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                resultado = sock.connect_ex((target, puerto))
                if resultado == 0:
                    print("Puerto {}: \t Abierto".format(puerto))
                    logging.info("Puerto {}: Abierto".format(puerto))
                    reporte_ips.write("Puerto {}: \t Abierto".format(puerto)+"\n")
                else:
                    print("Puerto {}: \t Cerrado".format(puerto))
                    logging.info("Puerto {}: Cerrado".format(puerto))
                    reporte_ips.write("Puerto {}: \t Cerrado".format(puerto)+"\n")
                sock.close()
        reporte_ips.close()
    except socket.error as e:
        logging.error("Error de conexión. " + str(e))
        print("Error de conexión. " + str(e))
        sys.exit()

def virus_total(path, API_KEY):
    try:
        api = PublicApi(API_KEY)
        with open(path, "rb") as f:
            file_hash = md5(f.read()).hexdigest()
        response = api.get_file_report(file_hash)
        if response["response_code"] == 200:
            # Reporte
            file_exe = open("rep_exe.txt", "w")
            file_exe.write("====ANÁLISIS DE EJECUTABLE====\nRuta: " + path + "\n")
            if response["results"]["positives"] > 0:
                print("Resultado: Archivo malicioso.")
                file_exe.write("Resultado: Archivo malicioso")
                file_exe.close()
                logging.info(path + ' Archivo malicioso')
            else:
                print("Resultado: Archivo seguro.")
                file_exe.write("Resultado: Archivo seguro")
                logging.info(path + ' Archivo seguro')
            logging.info('rep_exe.txt generado')
        else:
            print("No ha podido obtenerse el análisis del archivo.")
            logging.info(path + ' No ha podido obtenerse el análisis del archivo.')
    except Exception as e:
        logging.error("Ha ocurrido un error: " + str(e))
        print("Ha ocurrido un error: " + str(e))

def scrapping(link, numero):
    try:
        #print("Obteniendo imagenes con BeautifulSoup "+ link)
        response = requests.get(link)
        bs = BeautifulSoup(response.text, 'html.parser')
        #create directory for save images
        os.makedirs("Imagenes_PIA", exist_ok=True)
        img_eti = bs.find_all("img")
        #num_img = 0
        if img_eti != []:
            print("Descargando imagenes...")
            logging.info("Descargando imagenes...")
            for i in range(len(img_eti)):
                if img_eti[i]['src'].startswith("http") == False:
                    download = link + img_eti[i]['src']
                else:
                    download = img_eti[i]['src']
                    #print(download)
                    logging.info(download + " descargando...")
                    # Descarga imagenes en dir Imagenes
                    r = requests.get(download)
                    if r.status_code == 200:
                        f = open('Imagenes_PIA/%s' % download.split('/')[-1], 'wb')
                        f.write(r.content)
                        f.close()
                        #num_img = num_img + 1
                if i == int(numero):
                    break
            print("Imagenes descargadas")
            logging.info(link + " Imagenes descargadas")
        else:
            print("No se encontraron imagenes")
            logging.info(link + "No se encontraron imagenes")
    except Exception as e:
        logging.error("Ha ocurrido un error: " + str(e))
        print("Ha ocurrido un error: " + str(e))
