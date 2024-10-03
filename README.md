Producto Integrador de Aprendizaje

Instrucciones de uso

Creado por:
Julia Fernanda Ramírez Oviedo
Silvestre Martínez Cervantes

Información general
Este proyecto realiza 5 tareas relacionadas con la ciberseguridad. Las tareas que
realiza son las siguientes:
1) Obtención de hash.
2) Escaneo de puertos.
3) Análisis de ejecutables.
4) Web Scraping.
5) Estatus de procesos y servicios.

Requisitos
-Instalar todos los módulos necesarios que están en el archivo requirements.txt para
que los scripts funcionen.
-Tener Python 3 instalado.
-Tener Powershell versión 4.0 en adelante instalado.

Instrucciones
El script que se debe ejecutar es el main_pia.py, para eso necesitamos hacerlo
desde la Shell de Windows ya que funciona con el módulo argparse y necesita
parámetros para poder funcionar correctamente.
-h: Esta opción nos mostrará información de ayuda para ejecutar el script
correctamente.

Para obtener información de cada tarea, escribir lo siguiente:
py main_pia.py ‘tarea’ -h

1) hash - Obtención de hash
Esta tarea nos permite obtener valor hash de archivos.
Para ejecutar la tarea hay que escribir lo siguiente:
py main_pia.py hash -r 'ruta'
-r: Ingresar una ruta en la cual queremos ver el valor hash de su contenido.
Por ejemplo:
py main_pia.py hash -r C:\Users\SilverMC\Desktop\PCPIA
Una vez ejecutado la instrucción, se generará un archivo llamado valores_hash.txt
con los valores hash de los archivos.
También puedes ejecutar la instrucción especificando si solo quieres el valor hash
de un archivo, por ejemplo:
py main_pia.py hash -r C:\Users\SilverMC\Desktop\PCPIA\funciones.py

2) escaneo – Escaneo de puertos
Esta tarea nos permite saber si tenemos puertos abiertos o cerrados de cierta ip.
Para ejecutar la tarea hay que escribir lo siguiente:
py main_pia.py escaneo -t 'ip' -p 'puerto'
-t: Ingresar una ip. Se puede ingresar varias ip’s separadas por comas. Este
argumento es opcional, por lo que, si no se ingresa, por default tendrá el valor de
"127.0.0.1".
-p: Ingresar el puerto a analizar Se puede ingresar un rango de puertos a analizar
separados por una coma. Ej: -p 22,100
Por ejemplo:
py main_pia.py escaneo -t 127.0.0.1 -p 22
Una vez ejecutado la instrucción, se generará un archivo llamado Escaneo_IP.txt
con la información de los puertos de la ip ingresada.

3) exe - Análisis de ejecutables
Esta tarea nos permite saber si archivo .exe es un archivo seguro o malicioso.
Para ejecutar la tarea hay que escribir lo siguiente:
py main_pia.py exe -r 'ruta' -k 'api_key'
-r: Ingresar la ruta donde se encuentre el ejecutable.
-k: Ingresar una api key. Para obtenerla, es necesario tener una cuenta en
www.virustotal.com.
Por ejemplo:
py main_pia.py exe -r C:\Users\SilverMC\Desktop\minecraft\launcher.exe -k
‘api_key’
Una vez ejecutado la instrucción, se generará un archivo llamado rep_exe.txt con el
resultado obtenido del archivo.

4) scr – Web scraping
Esta tarea nos permite descargar imágenes de una página web.
Para ejecutar la tarea hay que escribir lo siguiente:
py main_pia.py scr -l 'link' -n '#imagenes'
-l: Ingresar el link de la página a hacer web scraping.
-n: Ingresar el número de imágenes a descargar.
Por ejemplo:
py main_pia.py scr -l https://www.uanl.mx/ -n 10
Una vez ejecutado la instrucción, se generará una carpeta llamada Imagenes_PIA
con las imágenes descargadas.

5) estatus - Estatus de procesos y servicios
Esta tarea nos permite ver que servicios del sistema se están ejecutando, cuales
están detenidos y también nos permite ver información de los procesos del sistema
que se están ejecutando.
Para ejecutar la tarea hay que escribir lo siguiente:
py main_pia.py estatus
Una vez ejecutado la instrucción, se generará dos archivos llamados Servicios.txt y
Procesos.txt en donde se guardará la información mostrada en pantalla.

pia.log
Este archivo registra todas las acciones que suceden a la hora de ejecutar una tarea
del script, así como los errores que puedan ocurrir.
