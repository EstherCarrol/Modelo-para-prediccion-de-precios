import requests
from bs4 import BeautifulSoup
import numpy as np
from dnn_app_utils_v3 import *
import json


class WebCrawler:

  def get_urls(self, base_url, limit):
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
  
    diccionarioAtributos = {}
    res = requests.get(property_url)
    soup = BeautifulSoup(res.content, 'html.parser')

    #Extracción de atributos habitaciones, baños, area
    ulEspecifications = soup.find("ul", class_="row list-unstyled font-medium mt-4 gutter-5")
    divsText = ulEspecifications.find_all("div", class_="text-muted")
    j=-1
    for i in divsText:
      j+=1
      value = i.find("span").string
      if j==0:
        diccionarioAtributos["habitaciones"]=value
      if j==1:
        diccionarioAtributos["baños"]=value
      if j==2:
        diccionarioAtributos["área"]=value

    #Extracción de precio
    precio = soup.find('span', class_="rs neg_price font-weight-semibold").string
    precio = precio.strip().replace('\n','').replace('$','').replace(',','').replace(' ','')
    
    diccionarioAtributos["precio"]=precio

    #Extracción de tipo de propiedad
    tipo = soup.find("div", class_="bg-secondary text-uppercase d-inline-block font-xsmall font-weight-bold text-white px-1").string
    tipo = tipo.lower()
    diccionarioAtributos["tipo"]=tipo


    section = soup.find('section', id="additional")
    if section is not None:
      divList = section.find_all('div')


      for i in divList:
        nameAtributte = i.find("p").string
        nameAtributte = nameAtributte.lower()
        value = i.find("span").string
        value = value.lower()
        value = value.replace("+","")
        diccionarioAtributos[nameAtributte]=value     
  
    return diccionarioAtributos
    


  def group_members(self):
    
    return {
      "20191000717": "Jennebier Esther Alvarado López",
      "20171001396": "German Said Pineda Martínez",
      "20151004709": "Christian Omar Bustillo Rodriguez"
    }
  
  def get_dataset(self,m):
    #Arreglo de UrlsPropiedades
    urlsPropiedades = self.get_urls("https://www.quierocasa.hn/propiedad-en-venta-en-tegucigalpa/srp", 1200)
    
    #Arreglo cuyos elementos son diccionarios de atributos de cada propiedad
    #Cada diccionario representa una propiedad
    atributosPropiedades = []


    

    #Primero se obtendran todos los atributos para cada propiedad del arreglo urlsPropiedades
    for urlPropiedad in urlsPropiedades:
        atributosPropiedades.append(self.get_attributes(urlPropiedad))

   
    nuevosAtributosPropiedades=[]
    #Se debe ELIMINAR todas aquellas que no sean casas o apartamentos
    #Y se hará obligatorio que posean estos 3 atributos (área, habitaciones, baños)
    for atributosPropiedad in atributosPropiedades:
        if atributosPropiedad["tipo"] == 'casas' or atributosPropiedad["tipo"] == "apartamentos":
          if "área" in atributosPropiedad and "habitaciones" in atributosPropiedad and "baños" in atributosPropiedad:
            if len(nuevosAtributosPropiedades)<350:
               nuevosAtributosPropiedades.append(atributosPropiedad)

    #Actualizar la lista de propiedades con los elementos que cumplen las condiciones
    atributosPropiedades = nuevosAtributosPropiedades
      
    

    #Conjunto que contiene los atributos para las propiedades
    #Me sirve para quitar todos aquellos atributos que no se encuentren aquí
    setKeys = {'área', 'habitaciones', 'baños', 'tipo','balcón','tipo de calle','estacionamiento','amueblado','precio'}
        
    

    #Eliminamos las claves de cada diccionario en atributosPropiedades que no se encuentren en setKeys
    for atributosPropiedad in atributosPropiedades:
        for key, value in atributosPropiedad.copy().items():
            if key not in setKeys:
                atributosPropiedad.pop(key)
            if 'balcón' not in atributosPropiedad:
              atributosPropiedad['balcón'] = 0
            if 'tipo de calle' not in atributosPropiedad:
              atributosPropiedad['tipo de calle'] = 1.0
            if 'estacionamiento' not in atributosPropiedad:
              atributosPropiedad['estacionamiento'] = 0
            if 'amueblado' not in atributosPropiedad:
              atributosPropiedad['amueblado']=0
    
    
    
    """
    Existen atributos cuyos valores son texto, así que debe cambiarse por un número 
    Si el valor de un atributo es sí se reemplazará por un 1, por ejemplo, amueblado:sí, amueblado:1
    
    casas: 1
    apartamentos:2
    calle: 1
    terrenos y oficinas excluidas
    """
    
    for atributosPropiedad in atributosPropiedades:
      for key, value in atributosPropiedad.items():
          if value == "casas" or value == "si" or value == "calle" or value == "amanecer":
              atributosPropiedad[key]=1.0
              value = 1.0
          if value == "apartamentos" or value =="avenida":
              atributosPropiedad[key]=2.0
              value = 2.0
          if value == "no":
              atributosPropiedad[key]=0
              value = 0
          atributosPropiedad[key]=float(value)

    #Arreglo para cada clave
    habitaciones = []
    banos = []
    área = []
    precio = []
    tipo = []
    balcon = []
    tipo_de_calle = []
    estacionamiento = []
    amueblado = []
    etiquetas = []

    for atributosPropiedad in atributosPropiedades:
      habitaciones.append(atributosPropiedad['habitaciones'])
      banos.append(atributosPropiedad['baños'])
      área.append(atributosPropiedad['área'])
      precio.append(atributosPropiedad['precio'])
      tipo.append(atributosPropiedad['tipo'])
      balcon.append(atributosPropiedad['balcón'])
      tipo_de_calle.append(atributosPropiedad['tipo de calle'])
      estacionamiento.append(atributosPropiedad['estacionamiento'])
      amueblado.append(atributosPropiedad['amueblado'])

    matriz_x = [habitaciones, banos, área, tipo, balcon, tipo_de_calle, estacionamiento, amueblado]
    etiquetas = [precio]

    matriz_x = list(map(list, zip(*matriz_x)))

    matriz_x = np.array(matriz_x)
    matriz_x = matriz_x.T

    
    return atributosPropiedades, matriz_x, etiquetas

    


ob = WebCrawler()

print("-----------------------------------")
#arreglo, matriz_x, etiquetas = ob.get_dataset(1)
#np.save("x", matriz_x)  
#np.save("y", etiquetas)

X=np.load("x.npy")
Y=np.load("y.npy")
layers_dims = [8, 10, 8, 7, 1]
print(X.shape)
print(Y.shape)
print("Terminado")

# GRADED FUNCTION: L_layer_model

def L_layer_model(X, Y, layers_dims, learning_rate = 0.0075, num_iterations = 5000, print_cost=False):#lr was 0.009
    """
    Implements a L-layer neural network: [LINEAR->RELU]*(L-1)->LINEAR->SIGMOID.
    
    Arguments:
    X -- data, numpy array of shape (number of examples, num_px * num_px * 3)
    Y -- true "label" vector (containing 0 if cat, 1 if non-cat), of shape (1, number of examples)
    layers_dims -- list containing the input size and each layer size, of length (number of layers + 1).
    learning_rate -- learning rate of the gradient descent update rule
    num_iterations -- number of iterations of the optimization loop
    print_cost -- if True, it prints the cost every 100 steps
    
    Returns:
    parameters -- parameters learnt by the model. They can then be used to predict.
    """

    np.random.seed(1)
    costs = []                         # keep track of cost
    
    # Parameters initialization. (≈ 1 line of code)
    ### START CODE HERE ###
    parameters = initialize_parameters_deep(layers_dims)
    ### END CODE HERE ###
    
    # Loop (gradient descent)
    for i in range(0, num_iterations):

        # Forward propagation: [LINEAR -> RELU]*(L-1) -> LINEAR -> SIGMOID.
        ### START CODE HERE ### (≈ 1 line of code)
        AL, caches = L_model_forward(X,parameters)
        ### END CODE HERE ###
        
        # Compute cost.
        ### START CODE HERE ### (≈ 1 line of code)
        cost = compute_cost(AL,Y)
        ### END CODE HERE ###
    
        # Backward propagation.
        ### START CODE HERE ### (≈ 1 line of code)
        grads = L_model_backward(AL,Y,caches)
        ### END CODE HERE ###
 
        # Update parameters.
        ### START CODE HERE ### (≈ 1 line of code)
        parameters = update_parameters(parameters, grads, learning_rate)
        ### END CODE HERE ###
                
        # Print the cost every 100 training example
        if print_cost and i % 100 == 0:
            print ("Cost after iteration %i: %f" %(i, cost))
        if i % 100 == 0:
            costs.append(cost)
            
  
    
    return parameters
parameters = L_layer_model(X, Y, layers_dims, num_iterations = 2000, print_cost = True)

layers = []
L = len(layers_dims)
claves = parameters.keys()

print(claves)
for l in range(1,L):
  W = parameters['W' + str(l)].tolist()
  b = parameters['b' + str(l)]
  b = b.flatten()
  b = b.tolist()
    
  if l == L-1:
    dict = {"n":layers_dims[l],
            "activation":"linear",
            "w":W,
            "b":b}
    layers.append(dict)
  else:
    dict = {"n":layers_dims[l],
          "activation":"relu",
          "w":W,
          "b":b}
  layers.append(dict)



dict_save = {"dnn_layers":layers}

with open('params.json', 'w') as archivo:
    json.dump(dict_save, archivo)

    
