"""
Problema planteado: dada la  imagen de un producto realizar el scrap de datos para obtener los reviews del mismo
Para resolver este problema hemos dividido la albor en las siguientes fases, hay que acotar que usaremos el buscador
 de amazon.com para realizar la búsqueda de productos.

1) Solicitar al usuario el termino a buscar en la base de datos de Amazon.com
2) Obtenemos los enlaces de las imágenes que aparecen en la búsqueda y los enlaces que nos llevan a las pagínas de cada producto
3) Descargamos las imágenes a una carpeta local en donde
4) Realizar la comparación de c/u de las imágenes descargadas con la imagen que tenemos en local
5) Si existe match entre las imágenes utilizamos la direccióm web del producto para hacer el scrap de los reviews
6) Guardamos la dirección web de la imagen, el nombre del producto, 



-------------------------------------------------
"""


from requests_html import HTMLSession
from bs4 import BeautifulSoup
import csv


def continuar():
	V=input("Presione Enter para continuar: ")


buscar=input("Ingrese los términos a buscar, separe cada termino con + ")

s=HTMLSession()

# URL de amazon.com en donde harmos nuestra primera búsqueda, de donde extraeremos las imágenes a comparar con
# la imagen que tenemos en local

url='https://www.amazon.com/s?k='+buscar+'&crid=3ODISDJDCB5RI&sprefix='+buscar+'%2Caps%2C1522&ref=nb_sb_noss_1'
r=s.get(url)
r.html.render(timeout=100)
soup=BeautifulSoup(r.html.html,'html.parser')


#  Dada la sopa buscamos todos los tags <img> de clase 's-image' 
# los cuales contiene enlaces a las imágenes de cada producto en la busqueda
imagenes=soup.find_all('img',{'class':'s-image'})
#print(imagenes)
#continuar()
cont=0
lista_imagenes=[]
lista_descripciones=[]
print("Lista de enlaces a imagenes para deascargar y comparar")
for imagen in imagenes:
	# por cada producto en la pagina de busqueda extraer el enlace que nos lleva a la página del producto
	# que es de donde vamos a extraer los reviews 
	img_link=imagen.get('src') # Enlace de la imágen
	img_desc=imagen.get('alt') # Descripción de la imagen (producto)
	# lista con los enlaces de las imagenes
	lista_imagenes.append(img_link)
	# lista con la descripcion de la imagen
	lista_descripciones.append(img_desc)
	cont +=1
#	print(img_link)
#	print(cont)
	#continuar()




#  Dada la sopa buscamos todos los tags <a> de clase a-link-normal s-no-outline 
# los cuales contiene enlaces a las páginas de cada producto en la busqueda
enlaces=soup.find_all('a',{'class':'a-link-normal s-no-outline'})
#print(enlaces)
cont2=0
print("Lista de enlaces a páginas")
lista_enlaces=[]
for enlace in enlaces:
	# por cada producto en la pagina de busqueda extraer el enlace que nos lleva a la página de detalle del producto
	# que es de donde vamos a extraer los reviews 
	link='https://www.amazon.com'+enlace.get('href')
	lista_enlaces.append(link) # Enlace de la página de detalle del producto
	#s.find('href')
	#print(str(producto))
	cont2 +=1
#	print(link)
#	print(cont)
#	continuar()
print (lista_enlaces)

print('Listas')

c=int(cont2)
for i in range(c):
	#print('Lista de enlaces a imagenes')
	#print (lista_imagenes, cont2)
	#print('Lista de enlaces a páginas de productos de cada imagen')
	#print (lista_enlaces,cont)
	#print (cont,cont2)
	
	print(i,lista_descripciones[i],lista_imagenes[i],lista_enlaces[i])


continuar()

# Empieza la diversíón, a cada una de las url obtenidas en el paso anterior le extraemos los reviews 
# NOTA: Esta extracción debe estar supeditada al resultado de la comparación de  imágenes, la cual
# Dicha comparación debe usar la lista de enlaces de imagenes obtenida para descargar c/u e las imágenes
# Y compararlas con la imagen que tenemos en local, si las imagenes cocuerdan, se debe guardar el url de la página
# de detalle del producto en una lista, junto con la descripción del producto, esta lista de urls será la utilizada 
#~para buscar  los reviews
ss=HTMLSession()
c=int(0)
for n in lista_enlaces:
	url_prod=lista_enlaces[c]
	rr=ss.get(url_prod)
	rr.html.render(timeout=20)
	sopa=BeautifulSoup(rr.html.html,'html.parser')
	c +=1

	products=sopa.find_all('div',{'class':'a-expander-content reviewText review-text-content a-expander-partial-collapse-content'})
	#print  (str(products))
	#continuar()

	lista_reviews=[]
	for product in products:
		review=product.span.text
		#print(str(review))
		#continuar()
		lista_reviews.append(review)
	print (url_prod)
	print(lista_reviews)
	continuar()