import requests
from bs4 import BeautifulSoup

class WebCrawler:

  def get_urls(self, base_url, limit):
    '''
    Este método utiliza <base_url> para encontrar las primeras <limit> urls de propiedades disponibles para una ubicación específica en el sitio "quierocasa.hn". Para realizar correctamente esta descarga se debe hacer repetidas solicitudes cambiando el valor de <nro_pagina>, como en el siguiente ejemplo:

    get_urls("https://www.quierocasa.hn/propiedad-en-venta-en-tegucigalpa/srp", 40)

    Al recibir <base_url> esta se modificará para hacer repetidas solicitudes a urls como:

    "https://www.quierocasa.hn/propiedad-en-venta-en-tegucigalpa/srp/page/<nro_pagina>"

    Este método retorna una lista de <limit> urls de propiedades encontradas (las primeras que aparezcan, sin repeticiones).Ej.:
    [
     "https://www.quierocasa.hn/se-vende-casa-en-el-hatillo-tegucigalpa/lldui3x/prd", 
     "https://www.quierocasa.hn/casa-en-venta-jardines-de-loarque-tegucigalpa/xhkvssb/prd", 
     ...
    ]
    '''

    """
     urlsPropiedades =[] #lista a retornar que contiene todas las url de las propiedades
    
    if limit>0 and limit<10:
      res = requests.get(base_url) #res guarda la respuesta de la petición hecha a la url especificada
      soup = BeautifulSoup(res.content, 'html.parser') #creación del objeto de la clase BeautifulSoup
        
      for a in soup.find_all('a'):
        if a.get('title')=="Ver detalles":
          linkPropiedad = "https://www.quierocasa.hn"+a.get('href')
          urlsPropiedades.append(linkPropiedad) 
    print(urlsPropiedades)
    """

    #Declaracion de variables 
    urlsPropiedades =[] #lista a retornar que contiene todas las url de las propiedades
    contadorCasas=0

    #Cuando el número de casas está entre 1 y 9
    if limit>0 and limit<10:
      print("Entre a la primera condición")
      res = requests.get(base_url) #res guarda la respuesta de la petición hecha a la url especificada
      soup = BeautifulSoup(res.content, 'html.parser') #creación del objeto de la clase BeautifulSoup
       
      for a in soup.find_all('a'):
        if contadorCasas==limit:
          return urlsPropiedades
        if a.get('title')=="Ver detalles":
          contadorCasas +=1
          linkPropiedad = "https://www.quierocasa.hn"+a.get('href')
          urlsPropiedades.append(linkPropiedad)
    

    #Cuando el número de casas es mayor a 9
    elif limit>9:
      res = requests.get(base_url) #res guarda la respuesta de la petición hecha a la url especificada
      soup = BeautifulSoup(res.content, 'html.parser') #creación del objeto de la clase BeautifulSoup
  
      for a in soup.find_all('a'):#este ciclo agrega los 9 enlaces de la página actual
        if a.get('title')=="Ver detalles":
          linkPropiedad = "https://www.quierocasa.hn"+a.get('href')
          urlsPropiedades.append(linkPropiedad)
          contadorCasas+=1 


      contadorPagina = 2
      contadorCasasTemporal=0

      while contadorCasas<=limit:
        if contadorCasasTemporal==9:
          contadorPagina+=1
          contadorCasasTemporal=0
        base_url = base_url+"/page/"+str(contadorPagina)
        res = requests.get(base_url) #res guarda la respuesta de la petición hecha a la url especificada
        soup = BeautifulSoup(res.content, 'html.parser') #creación del objeto de la clase BeautifulSoup
        for a in soup.find_all('a'):#este ciclo agrega los 9 enlaces de la página actual
          if contadorCasas==limit:
            return urlsPropiedades
          if a.get('title')=="Ver detalles":
            linkPropiedad = "https://www.quierocasa.hn"+a.get('href')
            urlsPropiedades.append(linkPropiedad)
            contadorCasas+=1
            contadorCasasTemporal+=1 
    
    return urlsPropiedades
        
       
      







  def get_attributes(self, property_url):
    '''
    Este método recibe una url de las que retorna el método get_urls, y la utiliza para revisar el código HTML que se obtiene al descargar dicha URL (puede usar la librería beatiful soup). A partir de dicho código se debe obtener un diccionario de atributos como el del ejemplo.

    Ejemplo de uso:
    get_attributes("https://www.quierocasa.hn/se-vende-casa-en-el-hatillo-tegucigalpa/lldui3x/prd")

    Retorna: 
    {
      'habitaciones': '3'
      'baños': '2.5'
      'área': '290'
      'precio': '275154'
      'tipo': 'casas'
      'amueblado': 'no'
      'cocina': '1'
      'salas de recepción': 'si'
      'balcón': '2'
      'tipo de calle': 'calle'
      'orientación': 'amanecer'
      'suelo': '1'
      'estacionamiento': '+5'
    }
    '''
    pass


  def group_members(self):
    '''Este método retorna un diccionario con los miembros del equipo que trabajaron en el desarrollo de las asignación. Este diccinario tiene como claves los números de cuenta y como valores los nombres completos de los miembros. Ejemplo:

    {
      "20201001678": "María Dolores de Barriga",
      "20195678901": "Elon Reeve Musk",
      "20148004423": "Zacarias Flores Del Campo"
    }
    '''
    pass


objeto = WebCrawler()
listaCasas=objeto.get_urls("https://www.quierocasa.hn/propiedad-en-venta-en-tegucigalpa/srp",11)
print(listaCasas)
print(len(listaCasas))