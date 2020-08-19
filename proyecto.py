#Tecnologico de Costa Rica						      #		
#Area academica de Ingenieria en Computadores				      #
#CE 4301 - Arquitectura de Computadores I				      #	
#Proyecto Individual							      #
#"Disenno e Implementacion de una aplicacion para nitidez en imagenes"        #
#Alumno: Edgar Chaves Gonzalez. 2017239281				      #	
###############################################################################
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import cv2
import numpy as np
import threading
#Algunas variables globales.
ubicacion = ""
x = 0
y = 0
###########################

#Esta funcion es llamada por el boton de codificar una imagen en un archivo de texto. Crea un hilo para que openCV pueda abrir la imagen sin que todo el programa se cierre.
def abrirImagenCodificar():
	hiloCod = threading.Thread(target = abriendoImagenCod)
	hiloCod.start()
###########################
#Esta funcion abre una ventana para que el usuario pueda abrir una imagen y esta pueda ser convertida a escala de grises, codificada y guardado estos datos en un archivo de texto.	
def abriendoImagenCod():
	try:
		root.filename = filedialog.askopenfilename(initialdir = "/home", title = "Seleccione la imagen a procesar", filetypes = (("jpeg", "*jpeg"),("png", "*png"),("all files","*.*")))
		print(root.filename)
	except:
		messagebox.showwarning("Alto! No ha elegido un archivo.")
	
	buffer1 = ""
	#imagen = cv2.imread("/home/edgar/Desktop/pythonFiles/1.png")
	
	try:
		imagen = cv2.imread(root.filename)
		imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
		rows,cols = imagen_gris.shape
		for i in range(rows):
			for j in range(cols):
				if (j < cols - 1) or (i < rows - 1):
					buffer1 += str(imagen_gris[i,j]) + ","
				else:
					buffer1 += str(imagen_gris[i,j])

		f = open("/home/edgar/Desktop/Proyecto-Edgar-Chaves/imagenGris1.bin","w")
		f.write(buffer1)
		f.close()
		cv2.imshow(str(cols) + "x" + str(rows), imagen)
		cv2.imshow(str(cols) + "x" + str(rows), imagen_gris)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
	except:
		messagebox.showwarning("Alto!", "No ha elegido un archivo.")
###########################
#Esta funcion crea una ventana auxiliar donde se ingresan las dimensiones de la imagen a decodificar. Esta funcion lee un archivo de texto plano y la convierte a imagen y es mostraada por openCV.	
def ventanaDecodificar():
	ventanDeco = Toplevel(root)
	ventanDeco. title("Decodificar imagen")
	ventanDeco. geometry("400x400")
	etiquetaExplicativa = Label(ventanDeco, text = "Ingrese las dimensiones de la imagen a decodificar:").place(x = 10, y = 10)
	try:
		dimensionX = IntVar()
		
		etiquetaX = Label(ventanDeco, text = "Ingrese la dimension x").place(x = 10, y = 40)
		Xcaja = Entry(ventanDeco, textvariable = dimensionX).place(x = 170, y = 40)
		
		dimensionY = IntVar()
		etiquetaY = Label(ventanDeco, text = "Ingrese la dimension y").place(x = 10, y = 80)
		Ycaja = Entry(ventanDeco, textvariable = dimensionY).place(x = 170, y = 80)
	except ValueError:
		messagebox.showwarning("Cuidado", "No puede haber una imagen sin dimensiones")

		
	botonObtieneRuta = Button(ventanDeco, text = "Abrir archivo", command = lambda: deco(dimensionX.get(), dimensionY.get())). place(x = 10 , y = 120)
	
		
###########################	 
#Esta funcion es llamada por el boton de decodificacion. Ademas esta funcion crea un hilo para que la ventana que usa openCV para mostrar la imagen y no se cierrren todas las ventanas creadas.	
def deco(x,y):
	
	hiloDeco = threading.Thread(target = decodificando, args = (x,y))
	hiloDeco.start()
###########################
#Esta funcion toma un archivo de texto plano y lo convierte en la imagen.	
def decodificando(x,y):
	
		
	if (x == 0 or y == 0 ):
		messagebox.showwarning("Cuidado", "No puede haber una imagen sin dimensiones")
	else:
		root.filename = filedialog.askopenfilename(initialdir = "/home", title = "Seleccione un archivo para decodificar", filetypes = (("txt", "*txt"),("all files","*.*")))
		#archivo = open("/home/edgar/Desktop/Arqui/imagenPrueba1.txt")
		try:
			archivo = open(root.filename)
			#cols = 640
			#rows = 480
			cols = x
			rows = y
			buffer1 = archivo.read()
			largoBuffer = len(buffer1)
			print(largoBuffer)
			i = 0
			j = 0
			numero = 0
			string = ""
			largoBuffer1 = len(buffer1)
			indexLista = 0
			lista = np.zeros((1,largoBuffer1), np.uint8)
			lista.astype(int)
			for i in range(largoBuffer1):
				if (buffer1[i] == ","):
					i += 1
					numero = int(string)
					string = ""
					lista[0, indexLista] = numero
					#print(lista[0,indexLista])
					indexLista += 1
				else:
					string += buffer1[i]
			lista.astype(int)
			#print(lista[0])
			matriz = np.zeros((rows, cols), np.uint8)
			#matriz = np.zeros((cols,rows), np.uint8)
			largoLista = len(lista[0])
			i = 0
			fila = 0
			columna = 0
			listapeq = 0
			for i in range(largoLista):
				if (columna == cols - 1):
					
					matriz[fila,columna] = lista[0,i]
					
					columna = 0
					fila += 1
				elif (fila == rows - 1):
					break
				else:
					
					matriz[fila,columna] = lista[0,i]
					columna += 1

			cv2.imshow("prueba", matriz)
			cv2.waitKey(0)
			cv2.destroyWindow("prueba")
		except:
			messagebox.showwarning("Alto!", "No ha elegido un archivo.")
###########################		
#Configuracion general para la ventana principal.	
root = Tk()
root.title("Codificador y Decodificador de Imagenes")
root.geometry("700x100")
#Boton que llama a la funcion de abrir imagen y decodificar.
botonCodificarImagen = Button(root, text = "Abrir imagen", command = abrirImagenCodificar).place(x = 20, y = 50)
etiquetaCodificarImagen = Label(root, text = "Para abrir una imagen y codificar \n la imagen presione el boton de abajo.").place(x = 10, y = 10)

#Boton que llama a la funcion de decodificar en donde se ingresan los valores de la dimension X y Y de la imagen.
botonDecodificarArchivo = Button (root, text = "Abrir archivo", command = lambda: ventanaDecodificar()).place(x = 400, y = 50)
etiquetaDecodificarImagen = Label (root, text = "Para abrir un archivo de codificacion \n de imagen presione el boton de abajo.").place(x = 400, y = 10)	
root.mainloop()
