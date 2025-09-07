#bot que ataca a las fichas mas valiosas y defiendes sus fichas, la mas valiosas en caso de tener un posible ataque por parte del rival

def bot(lista_fichas,lista_casillas_ocupadas,color,medida_casilla):
    lista_blancas=[]
    lista_negras=[]
    lista_preferencias=["rey","reina","torre","alfil","caballo","peon"]
    for ficha in lista_fichas:
        if ficha.color=="blanco":
            lista_blancas.append(ficha)
        else:
            lista_negras.append(ficha)

    if color=="blanco":
        lista_bot=lista_blancas
        lista_rival=lista_negras
    else:
        lista_bot=lista_negras
        lista_rival=lista_blancas
    
    lista_opciones=[]

    for ficha in lista_bot:
        lista_opciones=[]
        ficha.restricciones(True)
        
        for cord in lista_casillas_ocupadas:
            if cord in lista_opciones:
                lista_opciones.append({"tipo":ficha.tipo,"posicion":cord})

    num=0
    for opcion in lista_opciones:
        if opcion["tipo"]==lista_preferencias[num]:
            ficha_obhetivo=opcion["posicion"]



                    