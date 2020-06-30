from __future__ import print_function
import pandas as pd
import math
import time
from collections import defaultdict
import datetime
import sys
###Preprocessing split the simple files into various files
# making posible to manipulate them
def preprocessing(path,prepath):
    a = pd.read_csv(path)
    a = a.fillna("nan")
    ###user id created
    itercols = iter(a.columns)
    my_user_id = range(1,len(a.columns))
    next(itercols)
    names = [[number_user,name_user] for (number_user,name_user) in zip(my_user_id,itercols)]
    names_id = pd.DataFrame(names,columns=['userId','name'])
    names_id.to_csv(prepath+"user.csv",index=False)
    #print(names_id)
    ###move id created
    iterows = iter(a.iloc[:,0])
    my_movie_id = range(1,len(a.iloc[:,0])+1)
    movies = [[number_movie,name_movie] for (number_movie,name_movie) in zip(my_movie_id,iterows)]
    movies_id = pd.DataFrame(movies,columns=['movieId','title'])
    movies_id.to_csv(prepath+"movie.csv",index=False)
    #print(movies_id)
    ###making ratings
    my_ratings_id = []
    for i in range(1,len(a.columns)):
        for j in range(len(a.iloc[:,0])):
            if(a.iloc[:,i][j]!="nan"):
                #print(a.iloc[:,i][j],i,j+1)
                my_ratings_id.append([i,j+1,a.iloc[:,i][j]])
    ratings_id = pd.DataFrame(my_ratings_id,columns=['userId','movieId','rating'])
    ratings_id.to_csv(prepath+"ratings.csv",index=False)
    #print(ratings_id)
def manhattan(x,y):
    suma = 0
    for i in range(len(x)):
        #print(x[i],"elemento en x",y[i],"elemento en y")
        suma += abs(float(x[i][0])-float(y[i][0]))
        #print("suma:",suma)
    return suma
def euclidian(x,y):
    suma = 0
    for i in range(len(x)):
        suma += math.pow(float(x[i][0])-float(y[i][0]),2)
    return math.pow(suma,0.5)
def minkowski(x,y,n):
    suma = 0
    for i in range(len(x)):
        suma += math.pow(abs(float(x[i][0])-float(y[i][0])),n)
    return(math.pow(suma,1/n))    
def pearson(x,y):
    my_x = []
    my_y = []
    for i in range(len(x)):
        my_x.append(float(x[i][0]))
        my_y.append(float(y[i][0]))
    tam = len(my_x)
    sum_x = sum(my_x)

    sum_y = sum(my_y)
    prod_xy = sum_x*sum_y
    x_pow = math.pow(sum_x,2)
    y_pow = math.pow(sum_y,2)
    
    list_powx = [math.pow(num,2) for num in my_x]
    list_powy = [math.pow(num,2) for num in my_y]
    list_powx = sum(list_powx)
    list_powy = sum(list_powy)

    mult_xy = []
    for i in range(tam):
        mult_xy.append(my_x[i]*my_y[i])
    mult_xy = sum(mult_xy)
    #b = math.pow(list_powx-(x_pow/tam),0.5)
    #c = list_powx-(x_pow/tam)
    #d = list_powx
    #d = x_pow
    #e = tam
    #print(d,e,"soy el error HOLA!!!!")
    if(tam==0):
        return 0.0
    denominador = math.pow(list_powx-(x_pow/tam),0.5) * math.pow(list_powy-(y_pow/tam),0.5)
    if(denominador==0):
        return 0.0
    resultado = (mult_xy - ((prod_xy)/tam))/ (math.pow(list_powx-(x_pow/tam),0.5) * math.pow(list_powy-(y_pow/tam),0.5))
    return resultado
def sim_cos(x,y):
    my_x = []
    my_y = []
    for i in range(len(x)):
        my_x.append(float(x[i][0]))
        my_y.append(float(y[i][0]))
    mult_xy = []
    for i in range(len(my_x)):
        mult_xy.append(my_x[i]*my_y[i])
    mult_xy = sum(mult_xy)
    long_x = [math.pow(numero,2) for numero in my_x]
    long_x = math.pow(sum(long_x),0.5)
    long_y = [math.pow(numero,2) for numero in my_y]
    long_y = math.pow(sum(long_y),0.5)
    if(len(my_x)==0):
        return 0.0
    calculo = mult_xy/(long_x*long_y)
    return calculo
def jaccard(x,y,n):
    if(n!=0):
        return float(n-len(x)) / n
    else:
        print("No existe ningun elemento similar")
def knn():
    pass
###Simple Distance
# Takes the data rating for the users and keeps the intersected keys, that intersected keys is used to calculate the distances 
def simple_distance(idusuario1,idusuario2,id_type_distance,all_rating_dictionary):
    aux_dict1=dict( ( movie[0],movie[1:]) for movie in all_rating_dictionary[idusuario1] )
    aux_dict2=dict( ( movie[0],movie[1:]) for movie in all_rating_dictionary[idusuario2] )
    keys_a = set( aux_dict1.keys() )
    keys_b = set( aux_dict2.keys() )
    intersection = keys_a & keys_b
    values1 = [aux_dict1.get(movie_id) for movie_id in intersection]
    values2 = [aux_dict2.get(movie_id) for movie_id in intersection]
    if(len(intersection)==0):
        print("There is no same movies between user ",idusuario1,"and ",idusuario2)
        return 
    if(id_type_distance==1):
        print("The value of the manhattan distance between the user ",idusuario1,"and the user ",idusuario2,"is: ",manhattan(values1,values2))
    if(id_type_distance==2):
        print("The value of the euclidian distance between the user ",idusuario1,"and the user ",idusuario2,"is: ",euclidian(values1,values2))
    if(id_type_distance==3):
        n_value = int(input("Value for n, 1 or 2: "))
        print("The value of the minkowski distance between the user ",idusuario1,"and the user ",idusuario2,"is: ",minkowski(values1,values2,n_value))
    if(id_type_distance==4):
        print("The value of the pearson distance between the user ",idusuario1,"and the user ",idusuario2,"is: ",pearson(values1,values2))
    if(id_type_distance==5):
        print("The value of the cosine similarity distance between the user ",idusuario1,"and the user ",idusuario2,"is: ",sim_cos(values1,values2))
    if(id_type_distance==6):
            union = (len(aux_dict1)+len(aux_dict2))-len(intersection)
            print("The value of the jaccard distance between the user ",idusuario1,"and the user ",idusuario2,"is: ",jaccard(values1,values2,union))
###Loading the data using chunks
# the time is relatively  high, that because it search for every user thats save in all the chunks, but its more scalable because
# load the data in chunks, and its not going to overburden the memory 
def load_bd_method1(path):   
    iter_rating = pd.read_csv(path, iterator=True, chunksize=1000000)
    for chunk in iter_rating:
        id_user=list(chunk.iloc[:,0])
        id_movie=list(chunk.iloc[:,1])
        rating_m=list(chunk.iloc[:,2])

        z = zip( id_movie , rating_m)
        l = list(z)
    #LISTAS AUXILIARES
    aux = []
    lista = []

    temp = id_user[0]
    aux.append(temp)
    for nro in range(len(id_user)):
        if id_user[nro] != temp:
            temp = id_user[nro]
            aux.append(temp)
    ##id_user = aux

    tam_user = 0
    for x in range(len(aux)):
        y = tam_user
        tam_user = tam_user + id_user.count(aux[x])
        l_aux = []
        for indice in range(y,tam_user):
            l_aux.append(l[indice])
            #print(indice,l[indice])
        
        lista.append(l_aux)
        del l_aux
    #print(lista)    
    rating = dict(zip(aux,lista))
    return rating
###Loading the data without chunks
# The time is relatively low, that's because it converts the data directly to dictionary, but the problema its that overburden the
# memory because open all the data on memory
def load_bd_method2(path):
    my_dict_rating = pd.read_csv(path)
    #dictionary =  my_dict_rating.set_index('userId').T.to_dict('list')
    rating = my_dict_rating.groupby('userId')[['movieId','rating']].apply(lambda g: g.values.tolist()).to_dict()
    return rating


print("Welcome to the recomendator artubasuyaras")
print("Select the database to be used")
print("1.-Practice Database")
print("2.-Large Practice Database")
print("3.-Books Database,not implemented")
print("4.-Movie Lens 100k database") 
database_id = int(input())
if(database_id==1):
    preprocessing_path = "little_bd/laboratorio1.csv"
    prepath = "little_bd/"
    preprocessing(preprocessing_path,prepath)
    path = "little_bd/ratings.csv"
if(database_id==2):
    preprocessing_path = "large_bd/laboratorio1_large.csv"
    prepath = "large_bd/"
    preprocessing(preprocessing_path,prepath)
    path = "large_bd/ratings.csv"
if(database_id==3):
    sys.exit("Not implemented yet")
if(database_id==4):
    path = "100k/ratings.csv"
print("Select the method to load the bd")
print("1.-Using Chunks")
print("2.-Without Chunks") 
bd_method_id = int(input())
if(bd_method_id==1):
    a = datetime.datetime.now()
    rating = load_bd_method1(path)
    b = datetime.datetime.now()
    print("my time to load the bd with the method 1: ",b-a)
elif(bd_method_id==2):
    a = datetime.datetime.now()
    rating = load_bd_method2(path)
    b = datetime.datetime.now()
    print("my time to load the bd with the method 2: ",b-a)
print("What do you want to do: ")
print("1.-Calculate a distance")
print("2.-Make a recomendation")
id_action = int(input())
if(id_action==1):
    print("What distance you want to calculate")
    print("1.-Calculate Manhattan")
    print("2.-Calculate Euclidian")
    print("3.-Calculate Minkowski")
    print("4.-Calculate Pearson")
    print("5.-Calculate Cosine similarity")
    print("6.-Calculate Jaccard")
    id_distance = int(input())
    id_user1= int(input("user 1: "))
    id_user2= int(input("user 2: "))
    a = datetime.datetime.now()
    simple_distance(id_user1,id_user2,id_distance,rating)
    b = datetime.datetime.now()
    print("my time to find intersection and to calculate a simple distance: ",b-a)
elif(id_action==2):
    sys.exit("Not implemented yet")
    knn()

