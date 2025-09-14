import pygame,random
pygame.init()
clock=pygame.time.Clock()
import math


medida_casilla=120
casillas_por_fila=8

ancho_tablero=medida_casilla*10
alto_tablero=ancho_tablero-medida_casilla*2
medida_casilla=ancho_tablero/10

pantalla=pygame.display.set_mode((ancho_tablero,alto_tablero),pygame.RESIZABLE)

x=0
y=0


lista_opciones=[]#coordenada que se pueden utilizar para la ficha seleccionada



def movimiento_valido(lista_casillas_ocupadas,lista_coordenadas, tipo_ficha):
    if tipo_ficha=="caballo":
        return lista_coordenadas
    
    if tipo_ficha=="reina":
        for cord in lista_coordenadas:
            if cord in lista_casillas_ocupadas:
                lista_coordenadas.remove(cord)

def casillas_recorridas(cordenada_inicial,cordenada_final):

    x_inicial,y_inicial=cordenada_inicial.split(":")
    x_inicial=int(x_inicial)
    y_inicial=int(y_inicial)

    
    x_final,y_final=cordenada_final.split(":")
    x_final=int(x_final)
    y_final=int(y_final)


    x0=False
    y0=False 
    lista_x=[]
    if (x_final-x_inicial)>0:
        while x_inicial!=x_final:
            x_inicial+=1
            lista_x.append(x_inicial)

    if (x_final-x_inicial)<0:
        while x_inicial!=x_final:
            x_inicial-=1
            lista_x.append(x_inicial)
    
    if (x_final-x_inicial)==0:
        x0=True
    #________________________
    lista_y=[]
    if (y_final-y_inicial)>0:
        while y_inicial!=y_final:
            y_inicial+=1
            lista_y.append(y_inicial)

    if (y_final-y_inicial)<0:
        while y_inicial!=y_final:
            y_inicial-=1
            lista_y.append(y_inicial)
    
    if (y_final-y_inicial)==0:
        y0=True


    if len(lista_x)!=0:
        lista_x=lista_x[:-1]

    else:
        for c in range(len(lista_y)-1):
            lista_x.append(x_inicial)

    if len(lista_y)!=0:
        lista_y=lista_y[:-1]

    else:
        for c in range(len(lista_x)-1):
            lista_y.append(y_inicial)
    
    #print(lista_x,"·······",lista_y)
    lista_final=[]
    
    longitud = min(len(lista_x), len(lista_y))
    lista_final = []
    for c in range(longitud):
        lista_final.append(f"{lista_x[c]}:{lista_y[c]}")
    

    #print(lista_final)
    return lista_final

def convertir2(cordenada):
    x=cordenada[0]
    y=cordenada[4]
    return x,y

def movimiento_peon(peon,lista_posiciones_equipo_rival,lista_posiciones_equipo_peon,lista_opciones_peon):######################################
    lista_final=[]
    for cord in lista_opciones_peon:
        if cord not in lista_posiciones_equipo_rival and cord not in lista_posiciones_equipo_peon:
            lista_final.append(cord)
    

    if peon.color=="blanco":   
        lista_opciones_comprobar=[f"{peon.columna-1}:{peon.fila-1}",f"{peon.columna+1}:{peon.fila-1}"] 
    elif peon.color=="negro":
        lista_opciones_comprobar=[f"{peon.columna-1}:{peon.fila+1}",f"{peon.columna+1}:{peon.fila+1}"] 

    for opcion in lista_opciones_comprobar:
        if opcion in lista_posiciones_equipo_rival:
            lista_final.append(opcion)

    pos_peon=f"{peon.columna}:{peon.fila}"
    
    if peon.color=="negro" and pos_peon in ["0:1","1:1","2:1","3:1","4:1","5:1","6:1","7:1"]:
        lista_final.append(f"{peon.columna}:{peon.fila+2}")
    elif peon.color=="blanco" and pos_peon in ["0:6","1:6","2:6","3:6","4:6","5:6","6:6","7:6"]:
        lista_final.append(f"{peon.columna}:{peon.fila-2}")



    return lista_final





def ordenar_cords_lista(lista_cords_por_angulos,ficha_bot):
    x=ficha_bot.columna
    y=ficha_bot.fila
    dic={}
    lista_final=[]
    #opcion 1= de menor a mayor
    #opcion 2= de mayor a menor
    for lista_cords in lista_cords_por_angulos:
        if len(lista_cords)>1:
            if int(lista_cords[0][0])>x and int(lista_cords[0][2])<y:
                opcion=1
                operacion="-"
            elif int(lista_cords[0][0])<x and int(lista_cords[0][2])>y:
                opcion=2
                operacion="-"
            
            elif (int(lista_cords[0][0])<x and int(lista_cords[0][2])<y) or (int(lista_cords[0][0])==x and int(lista_cords[0][2])<y) or (int(lista_cords[0][0])<x and int(lista_cords[0][2])==y):
                opcion=2
                operacion="+"
            
            else:
                opcion=1
                operacion="+"

            dic={}
            for cord in lista_cords:
                if operacion=="-":
                    dic.update({int(cord[0])-int(cord[2]):cord})
                elif operacion=="+":
                    dic.update({int(cord[0])+int(cord[2]):cord})

            lista_keys=list(dic.keys())
            if opcion==1:
                lista_keys.sort()
            elif opcion==2:
                lista_keys.sort(reverse=True)

            lista=[]
            for num in lista_keys:
                lista.append(dic[num])
            lista_final.append(lista)
            #print(lista,"                            LISTA")
    return lista_final
    
                


def cords_atravesadas_bot(lista_cords_bot,lista_posiciones_rivales,lista_posiciones_bots,ficha_bot):
    lista_cords_por_angulos=[[],[],[],[],[],[],[],[]]
    tipo_ficha=ficha_bot.tipo
    pos_ficha=f"{ficha_bot.columna}:{ficha_bot.fila}"
    

    lista_cords_bot=eliminar_cords_no_validas2(lista_cords_bot)
    #print("‖‖‖‖‖‖‖‖‖‖‖‖‖‖‖‖‖‖‖‖‖‖‖‖‖‖‖‖")
    #print(tipo_ficha, f"{ficha_bot.columna}:{ficha_bot.fila}")
    #print(lista_cords_bot, "lista del principio")
    for cord in lista_cords_bot:
        if int(cord[0])==int(pos_ficha[0]) and int(cord[2])>int(pos_ficha[2]):
            lista_cords_por_angulos[0].append(cord)
        
        elif int(cord[0])>int(pos_ficha[0]) and int(cord[2])>int(pos_ficha[2]):
            lista_cords_por_angulos[1].append(cord)

        elif int(cord[0])>int(pos_ficha[0]) and int(cord[2])==int(pos_ficha[2]):
            lista_cords_por_angulos[2].append(cord)
        
        elif int(cord[0])>int(pos_ficha[0]) and int(cord[2])<int(pos_ficha[2]):
            lista_cords_por_angulos[3].append(cord)

        #---------------------------------------------------------------------------
        if int(cord[0])==int(pos_ficha[0]) and int(cord[2])<int(pos_ficha[2]):
            lista_cords_por_angulos[4].append(cord)
        
        elif int(cord[0])<int(pos_ficha[0]) and int(cord[2])<int(pos_ficha[2]):
            lista_cords_por_angulos[5].append(cord)

        elif int(cord[0])<int(pos_ficha[0]) and int(cord[2])==int(pos_ficha[2]):
            lista_cords_por_angulos[6].append(cord)
        
        elif int(cord[0])<int(pos_ficha[0]) and int(cord[2])>int(pos_ficha[2]):
            lista_cords_por_angulos[7].append(cord)

    #print(lista_cords_por_angulos,"               lista_cords_por_angulos")
    for i in range(len(lista_cords_por_angulos)):
        lista_cords_por_angulos[i] = eliminar_cords_no_validas2(lista_cords_por_angulos[i])
    #for lista_cords in lista_cords_por_angulos:
    #   lista_cords=eliminar_cords_no_validas2(lista_cords)
    
    lista_cords_por_angulos=ordenar_cords_lista(lista_cords_por_angulos,ficha_bot)
    #[['7:1', '7:2', '7:3', '7:4', '7:5', '7:6', '7:7'], [], [], [], [], [], ['0:0', '1:0', '2:0', '3:0', '4:0', '5:0', '6:0'], []]
    #print(lista_cords_por_angulos,"               lista_cords_por_angulos")

    lista_final=[]
    
    for lista_angulos in lista_cords_por_angulos:
        lista_append=[]
        parar=False
        for cordenada in lista_angulos:
            if cordenada in lista_posiciones_rivales and parar==False:
                lista_append.append(cordenada)
                parar=True
                #print(f"{cordenada} 🟧")

            elif cordenada not in lista_posiciones_rivales and cordenada not in lista_posiciones_bots and parar==False:
                lista_append.append(cordenada)
                #print(f"{cordenada} 🟩")
            elif cordenada in lista_posiciones_bots:
                parar=True
                #print(f"{cordenada} 🟨")

            if parar==True:
                #print(f"🟥")
                break


        for elemento in lista_append:
            lista_final.append(elemento)
        #lista_final.append(lista_append)

    #print(lista_final,"                lista_final")
    
    
    #print("‖‖‖‖‖‖‖‖‖‖‖‖‖‖‖‖‖‖‖‖‖‖‖‖‖‖‖‖")
    return lista_final
    









def eliminar_cords_no_validas(lista_opciones_ficha_bot_actual,ficha_bot,lista_rival,lista_fichas_equipo_actual):
    cords_eliminar=[]
    for cordenada in lista_opciones_ficha_bot_actual:
        lista_casillas_recorridas=[]
        lista_casillas_recorridas=casillas_recorridas(f"{ficha_bot.columna}:{ficha_bot.fila}",cordenada)

        for cord_atravesada in lista_casillas_recorridas:
            for ficha_rival in lista_rival:
                if f"{ficha_rival.columna}:{ficha_rival.fila}"==cord_atravesada:
                    cords_eliminar.append(cordenada)
                    break
    cords_validas1=[]
    for cord in lista_opciones_ficha_bot_actual:
        if cord not in cords_eliminar:
            cords_validas1.append(cord)

    cords_evitar=[]
    for ficha in lista_fichas_equipo_actual:
        cords_evitar.append(f"{ficha.columna}:{ficha.fila}")

    cords_validas=[]
    for cord in cords_validas1:
        if cord not in cords_evitar:
            cords_validas.append(cord)

    cords_validas=eliminar_cords_no_validas2(cords_validas)
    
    return cords_validas


def movimiento_rey(lista_posiciones_equipo_rey,lista_opciones_rey):
    lista_final=[]
    for opcion in lista_opciones_rey:
        if opcion not in lista_posiciones_equipo_rey:
            lista_final.append(opcion)
    return lista_final

def eliminar_cords_no_validas2(lista_cordenadas):
    lista_final=[]
    nums=["0","1","2","3","4","5","6","7"]
    for cord in lista_cordenadas:
        if len(cord)==3 and cord[0] in nums and cord[2] in nums and cord[1]==":":
            lista_final.append(cord)
    return lista_final

def eliminar_cords_ocupadas_caballo(lista_cords_caballo,lista_cords_equipo_caballo):
    lista_final=[]
    for cord in lista_cords_caballo:
        if cord not in lista_cords_equipo_caballo:
            lista_final.append(cord)

    return lista_final
#____________________________________________________________________________

def bot(lista_fichas,lista_casillas_ocupadas,color,medida_casilla):
    lista_blancas=[]#lista de fichas blancas
    lista_negras=[]#lista de fichas negras
    
    dic_peones=diccionario_peones
    valores_fichas={"rey":9999,"reina":9,"torre":5,"alfil":3,"caballo":3,"peon":1}
    
    for ficha in lista_fichas:#cada ficha de la lista de TODAS las fichas
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

    lista_posiciones_bots=[]
    lista_posiciones_rivales=[]
    for bot in lista_bot:
        lista_posiciones_bots.append(f"{bot.columna}:{bot.fila}")
    
    for rival in lista_rival:
        lista_posiciones_rivales.append(f"{rival.columna}:{rival.fila}")
#_____________________________________________________________________________________________________________________
    lista_opciones_finales=[]
    
            #________________________________________________________________
        #ficha_bot ataca a ficha rival
    for ficha_bot_actual in lista_bot:
        lista_opciones_ficha_bot_actual=[]
        lista_opciones_ficha_bot_actual=ficha_bot_actual.restricciones(True)
        

        if ficha_bot_actual.tipo!="caballo" and ficha_bot_actual.tipo!="peon" and ficha_bot_actual.tipo!="rey":
            lista_opciones_ficha_bot_actual=cords_atravesadas_bot(lista_opciones_ficha_bot_actual,lista_posiciones_rivales,lista_posiciones_bots,ficha_bot_actual)
        
        elif ficha_bot_actual.tipo=="caballo":
            lista_opciones_ficha_bot_actual=eliminar_cords_no_validas2(lista_opciones_ficha_bot_actual)

            #print(lista_opciones_ficha_bot_actual,"         lista opciones antes de eliminar fichas no validas")
            lista_opciones_ficha_bot_actual=eliminar_cords_ocupadas_caballo(lista_opciones_ficha_bot_actual,lista_posiciones_bots)
            #print(lista_opciones_ficha_bot_actual, "          caballo lista opciones")
        
        elif ficha_bot_actual.tipo=="rey":
            lista_opciones_ficha_bot_actual=movimiento_rey(lista_posiciones_bots,lista_opciones_ficha_bot_actual)
            print("restriccion hecha a rey")
            print(lista_opciones_ficha_bot_actual)

        else:
            lista_opciones_ficha_bot_actual=eliminar_cords_no_validas2(lista_opciones_ficha_bot_actual)
            lista_opciones_ficha_bot_actual=movimiento_peon(ficha_bot_actual,lista_posiciones_rivales,lista_posiciones_bots,lista_opciones_ficha_bot_actual)
            print(f"{ficha_bot_actual.columna}:{ficha_bot_actual.fila}  ---",lista_opciones_ficha_bot_actual)
        
        
        for cordenada in lista_opciones_ficha_bot_actual:
            cordenada_peligrosa = False 
            for ficha_rival_cordenada in lista_rival:
                if f"{ficha_rival_cordenada.columna}:{ficha_rival_cordenada.fila}"==cordenada:
                #si la cordenada de opciones de la ficha bot es igual a la posicion de la ficha rival que se esta revisando:
        #________________________________________________________________       

        #ficha rival2 ataca a ficha bot

                    for ficha_rival in lista_rival:
                        ataque_con_consecuencias=False
                        lista_opciones_ficha_rival_actual=[]
                        lista_opciones_ficha_rival_actual=ficha_rival.restricciones(True)

                        if ficha_rival.tipo!="caballo" and ficha_rival.tipo!="peon" and ficha_rival.tipo!="rey":
                            lista_opciones_ficha_rival_actual=cords_atravesadas_bot(lista_opciones_ficha_rival_actual,lista_posiciones_bots,lista_posiciones_rivales,ficha_rival)
                        #lista_opciones_ficha_rival_actual=eliminar_cords_no_validas(lista_opciones_ficha_rival_actual,ficha_rival,lista_bot,lista_rival)
                        elif ficha_rival.tipo=="caballo":
                            lista_opciones_ficha_rival_actual=eliminar_cords_no_validas2(lista_opciones_ficha_rival_actual)
                            lista_opciones_ficha_rival_actual=eliminar_cords_ocupadas_caballo(lista_opciones_ficha_rival_actual,lista_posiciones_rivales)

                        elif ficha_rival.tipo=="rey":
                            lista_opciones_ficha_rival_actual=movimiento_rey(lista_posiciones_rivales,lista_opciones_ficha_rival_actual)

                        else:
                            lista_opciones_ficha_rival_actual=eliminar_cords_no_validas2(lista_opciones_ficha_rival_actual)
                            lista_opciones_ficha_rival_actual=movimiento_peon(ficha_rival,lista_posiciones_bots,lista_posiciones_rivales,lista_opciones_ficha_rival_actual)


                        for opcion_rival in lista_opciones_ficha_rival_actual:
                            if opcion_rival==cordenada:
                                valor_jugada=(valores_fichas[ficha_rival.tipo]-valores_fichas[ficha_bot_actual.tipo])
                                #valor jugada= la ficha que ha matado menos a la que han matado
                                victima_cord=f"{ficha_rival_cordenada.columna}:{ficha_rival_cordenada.fila}"
                                lista_opciones_finales.append({"atacante":ficha_bot_actual,"victima":victima_cord,"valor jugada":valor_jugada,"lista rival":lista_rival})
                                cordenada_peligrosa=True
                            
                            
                            
                    if cordenada_peligrosa==False:
                        valor_jugada=valores_fichas[ficha_rival_cordenada.tipo]
                        victima_cord=f"{ficha_rival_cordenada.columna}:{ficha_rival_cordenada.fila}"
                        lista_opciones_finales.append({"atacante":ficha_bot_actual,"victima":victima_cord,"valor jugada":valor_jugada,"lista rival":lista_rival})


                elif ficha_rival_cordenada!=cordenada:
                    cordenada_peligrosa = False 
                    for ficha_rival_ in lista_rival:
                        cordenada_peligrosa=False
                        lista_opciones_ficha_rival_=[]
                        lista_opciones_ficha_rival_=ficha_rival_.restricciones(True)
                        if ficha_rival_.tipo!="caballo" and ficha_rival_.tipo!="peon" and ficha_rival_.tipo!="rey":
                            lista_opciones_ficha_rival_=cords_atravesadas_bot(lista_opciones_ficha_rival_,lista_posiciones_bots,lista_posiciones_rivales,ficha_rival_)
                        elif ficha_rival_.tipo=="caballo":
                            lista_opciones_ficha_rival_=eliminar_cords_no_validas2(lista_opciones_ficha_rival_)
                            lista_opciones_ficha_rival_=eliminar_cords_ocupadas_caballo(lista_opciones_ficha_rival_,lista_posiciones_rivales)

                        elif ficha_rival_.tipo=="rey":
                            lista_opciones_ficha_rival_=movimiento_rey(lista_posiciones_rivales,lista_opciones_ficha_rival_)
                        else:
                            lista_opciones_ficha_rival_=eliminar_cords_no_validas2(lista_opciones_ficha_rival_)
                            lista_opciones_ficha_rival_=movimiento_peon(ficha_rival_,lista_posiciones_bots,lista_posiciones_rivales,lista_opciones_ficha_rival_)


                        #lista_opciones_ficha_rival_=eliminar_cords_no_validas(lista_opciones_ficha_rival_,ficha_rival_,lista_bot,lista_rival)

                        for opcion in lista_opciones_ficha_rival_:
                            if opcion==cordenada:
                                valor_jugada=(valores_fichas[ficha_bot_actual.tipo]*-1)-valores_fichas[ficha_rival_.tipo]
                                lista_opciones_finales.append({"atacante":ficha_bot_actual,"victima":cordenada,"valor jugada":valor_jugada,"lista rival":lista_rival})
                                cordenada_peligrosa=True
                        
                        if cordenada_peligrosa==False:
                            valor_jugada=valores_fichas[ficha_bot_actual.tipo]*-1
                            lista_opciones_finales.append({"atacante":ficha_bot_actual,"victima":cordenada,"valor jugada":valor_jugada,"lista rival":lista_rival})

#---------------------------------------------------------------------------------------------------------------------
        pos_ficha_bot_actual=f"{ficha_bot_actual.columna}:{ficha_bot_actual.fila}"
        #RIVAL
        for posible_ficha_atacante in lista_rival:
            lista_opciones_posible_ficha_atacante=posible_ficha_atacante.restricciones(True)

            if posible_ficha_atacante.tipo!="caballo" and posible_ficha_atacante.tipo!="peon" and posible_ficha_atacante.tipo!="rey":
                lista_opciones_posible_ficha_atacante=cords_atravesadas_bot(lista_opciones_posible_ficha_atacante,lista_posiciones_bots,lista_posiciones_rivales,posible_ficha_atacante)

            elif posible_ficha_atacante.tipo=="caballo":
                lista_opciones_posible_ficha_atacante=eliminar_cords_no_validas2(lista_opciones_posible_ficha_atacante)
                lista_opciones_posible_ficha_atacante=eliminar_cords_ocupadas_caballo(lista_opciones_posible_ficha_atacante,lista_posiciones_rivales)

            elif posible_ficha_atacante.tipo=="rey":
                lista_opciones_posible_ficha_atacante=movimiento_rey(lista_posiciones_rivales,lista_opciones_posible_ficha_atacante)

            else:
                lista_opciones_posible_ficha_atacante=eliminar_cords_no_validas2(lista_opciones_posible_ficha_atacante)
                lista_opciones_posible_ficha_atacante=movimiento_peon(posible_ficha_atacante,lista_posiciones_bots,lista_posiciones_rivales,lista_opciones_posible_ficha_atacante)
                
            
            for cordenada_posible in lista_opciones_posible_ficha_atacante:
                if pos_ficha_bot_actual==cordenada_posible:
                    lista_opciones_escapar_ficha_bot=ficha_bot_actual.restricciones(True)
                    
                    if ficha_bot_actual.tipo!="caballo" and ficha_bot_actual.tipo!="peon" and ficha_bot_actual.tipo!="rey":
                        lista_opciones_escapar_ficha_bot=cords_atravesadas_bot(lista_opciones_escapar_ficha_bot,lista_posiciones_rivales,lista_posiciones_bots,ficha_bot_actual)
                    
                    elif ficha_bot_actual.tipo=="caballo":
                        lista_opciones_escapar_ficha_bot=eliminar_cords_no_validas2(lista_opciones_escapar_ficha_bot)
                        lista_opciones_escapar_ficha_bot=eliminar_cords_ocupadas_caballo(lista_opciones_escapar_ficha_bot,lista_posiciones_bots)
                    
                    elif ficha_bot_actual.tipo=="rey":
                        lista_opciones_escapar_ficha_bot=movimiento_rey(lista_posiciones_bots,lista_opciones_escapar_ficha_bot)
                
                    else:
                        lista_opciones_escapar_ficha_bot=eliminar_cords_no_validas2(lista_opciones_escapar_ficha_bot)
                        lista_opciones_escapar_ficha_bot=movimiento_peon(ficha_bot_actual,lista_posiciones_rivales,lista_posiciones_bots,lista_opciones_escapar_ficha_bot)
                    
                    ######################
                    lista_cordenadas_amenazadas=[]

                    for ficha_rival3 in lista_rival:
                        lista_opciones_ficha_rival3=ficha_rival3.restricciones(True)
                    
                        if ficha_rival3.tipo!="caballo" and ficha_rival3.tipo!="peon" and ficha_rival3.tipo!="rey":
                            lista_opciones_ficha_rival3=cords_atravesadas_bot(lista_opciones_ficha_rival3,lista_posiciones_bots,lista_posiciones_rivales,ficha_rival3)
                        
                        elif ficha_rival3.tipo=="caballo":
                            lista_opciones_ficha_rival3=eliminar_cords_no_validas2(lista_opciones_ficha_rival3)
                            lista_opciones_ficha_rival3=eliminar_cords_ocupadas_caballo(lista_opciones_ficha_rival3,lista_posiciones_rivales)
                        
                        elif ficha_rival3.tipo=="rey":
                            lista_opciones_ficha_rival3=movimiento_rey(lista_posiciones_rivales,lista_opciones_ficha_rival3)
                        
                        else:  
                            lista_opciones_ficha_rival3=eliminar_cords_no_validas2(lista_opciones_ficha_rival3)
                            lista_opciones_ficha_rival3=movimiento_peon(ficha_rival3,lista_posiciones_bots,lista_posiciones_rivales,lista_opciones_ficha_rival3)
                        
                        for elemento in lista_opciones_ficha_rival3:
                            lista_cordenadas_amenazadas.append(elemento)


                    for cordenada_posible_ficha_bot_escapar in lista_opciones_escapar_ficha_bot:
                        if cordenada_posible_ficha_bot_escapar not in lista_cordenadas_amenazadas:
                            if ficha_bot_actual.tipo!="rey":
                                valor_jugada=(valores_fichas[ficha_bot_actual.tipo])
                            else:
                                valor_jugada=(valores_fichas[ficha_bot_actual.tipo])-1
                            
                            lista_opciones_finales.append({"atacante":ficha_bot_actual,"victima":cordenada_posible_ficha_bot_escapar,"valor jugada":valor_jugada,"lista rival":lista_rival})
                
                


##----------------------------------------------------------------------------------------------------------------------
    if len(lista_opciones_finales)==0:
        for ficha_bot in lista_bot:

        
            lista_opciones_ficha_bot=ficha_bot.restricciones(True)
            if ficha_bot.tipo!="caballo" and ficha_bot.tipo!="peon" and ficha_bot.tipo!="rey":
                lista_opciones_ficha_bot=cords_atravesadas_bot(lista_opciones_ficha_bot,lista_posiciones_rivales,lista_posiciones_bots,ficha_bot)
            elif ficha_bot.tipo=="caballo":
                lista_opciones_ficha_bot=eliminar_cords_no_validas2(lista_opciones_ficha_bot)
                lista_opciones_ficha_bot=eliminar_cords_ocupadas_caballo(lista_opciones_ficha_bot,lista_posiciones_bots)

            elif ficha_bot.tipo=="rey":
                lista_opciones_ficha_bot=movimiento_rey(lista_posiciones_bots,lista_opciones_ficha_bot)
            
            else:
                lista_opciones_ficha_bot=eliminar_cords_no_validas2(lista_opciones_ficha_bot)
                lista_opciones_ficha_bot=movimiento_peon(ficha_bot,lista_posiciones_rivales,lista_posiciones_bots,lista_opciones_ficha_bot)
            
            if len(lista_opciones_ficha_bot)>0:
                for cord in lista_opciones_ficha_bot:
                    lista_escoger=[]
                    for ficha_rival3 in lista_rival:
                        ficha_rival3_opciones=ficha_rival3.restricciones(True)
                        if ficha_rival3.tipo!="caballo" and ficha_rival3.tipo!="peon" and ficha_rival3.tipo!="rey":
                            ficha_rival3_opciones=cords_atravesadas_bot(ficha_rival3_opciones,lista_posiciones_bots,lista_posiciones_rivales,ficha_rival3)
                        elif ficha_rival3.tipo=="caballo":
                            ficha_rival3_opciones=eliminar_cords_no_validas2(ficha_rival3_opciones)
                            ficha_rival3_opciones=eliminar_cords_ocupadas_caballo(ficha_rival3_opciones,lista_posiciones_rivales)
                        
                        elif ficha_rival3.tipo=="rey":
                            ficha_rival3_opciones=movimiento_rey(lista_posiciones_rivales,ficha_rival3_opciones)
                        else:
                            ficha_rival3_opciones=eliminar_cords_no_validas2(ficha_rival3_opciones)
                            ficha_rival3_opciones=movimiento_peon(ficha_rival3,lista_posiciones_bots,lista_posiciones_rivales,ficha_rival3_opciones)

                        for cordenada in ficha_rival3_opciones:
                            lista_escoger.append(cordenada)
                    
                    if cord not in lista_escoger:
                        lista_opciones_finales.append({"atacante":ficha_bot,"victima":cord,"valor jugada":0,"lista rival":lista_rival})


        if len(lista_opciones_finales)==0:
            
            for ficha_bot_ in lista_bot:
                lista_opciones_ficha_bot_=ficha_bot_.restricciones(True)

                if ficha_bot_.tipo!="caballo" and ficha_bot_.tipo!="peon" and ficha_bot_.tipo!="rey":
                    lista_opciones_ficha_bot_=cords_atravesadas_bot(lista_opciones_ficha_bot_,lista_posiciones_rivales,lista_posiciones_bots,ficha_bot_)
                elif ficha_bot_.tipo=="caballo":
                    lista_opciones_ficha_bot_=eliminar_cords_no_validas2(lista_opciones_ficha_bot_)
                    lista_opciones_ficha_bot_=eliminar_cords_ocupadas_caballo(lista_opciones_ficha_bot_,lista_posiciones_bots)

                elif ficha_bot_.tipo=="rey":
                    lista_opciones_ficha_bot_=movimiento_rey(lista_posiciones_bots,lista_opciones_ficha_bot_)

                else:
                    lista_opciones_ficha_bot_=eliminar_cords_no_validas2(lista_opciones_ficha_bot_)
                    lista_opciones_ficha_bot_=movimiento_peon(ficha_bot_,lista_posiciones_rivales,lista_posiciones_bots,lista_opciones_ficha_bot_)
                
                if len(lista_opciones_ficha_bot_)>0:
                    lista_opciones_finales.append({"atacante":ficha_bot_,"victima":lista_opciones_ficha_bot_[0],"valor jugada":0,"lista rival":lista_rival})
                    break



    
    lista_opciones_finales_limpia=[]
    for opcion_repetida in lista_opciones_finales:
        if opcion_repetida not in lista_opciones_finales_limpia:
            lista_opciones_finales_limpia.append(opcion_repetida)
    
    opcion_final=lista_opciones_finales_limpia[0]
    for opcion in lista_opciones_finales_limpia:
#-----------------------------------------------------------------        
        #if opcion["atacante"].tipo!="rey":
        #    print(opcion["atacante"].tipo,"  : ",opcion)
        #else:
        #    print("------------------------------------")
        #    print(opcion["atacante"].tipo,"  : ",opcion)
        #    print("------------------------------------")
#-----------------------------------------------------------------
        #print(len(lista_opciones_finales_limpia))
        if opcion["valor jugada"]>opcion_final["valor jugada"]:
            opcion_final=opcion

    numero_maximo=opcion_final["valor jugada"]
    lista_final_final=[]

    for opcionn in lista_opciones_finales:
        if opcionn["valor jugada"]==numero_maximo:
            lista_final_final.append(opcionn)

    opcion_final_=random.choice(lista_final_final)


    return opcion_final_






#___________________________________________________________________________
def comprobador_coordenadas(cord1,cord2):
    cord1=str(cord1)
    cord2=str(cord2)
    i=0
    x1=0
    y1=0
    x2=0
    y2=0
    for c in cord1:
        if c in("01234567"):
            x1=c
            break
    for c in cord1:
        if c in("01234567"):
            y1=c
            break
    for c in cord2:
        if c in("01234567"):
            x2=c
            break
    for c in cord2:
        if c in("01234567"):
            y2=c
            break
    if x1==x2 and y1==y2:
        return True
    else:return False

def convertir(coordenada):
    x,y=coordenada.split(":")
    return int(x),int(y)
#para convertir las coordenadas devueltas por "restricciones" en tuplas de enteros   


def matar_peon(ficha_selec,lista_fichas):
    lista_opciones_ficha_selec=[]
    for ficha in lista_fichas:
        if ficha_selec.color=="negro" and ficha.color=="blanco":
            if ficha.columna==ficha_selec.columna+1 and ficha.fila==ficha_selec.fila+1:
                lista_opciones_ficha_selec.append(f"{ficha.columna}:{ficha.fila }")
            
            if ficha.columna==ficha_selec.columna-1 and ficha.fila==ficha_selec.fila+1:
                lista_opciones_ficha_selec.append(f"{ficha.columna}:{ficha.fila }")

        if ficha_selec.color=="blanco" and ficha.color=="negro":
            if ficha.columna==ficha_selec.columna+1 and ficha.fila==ficha_selec.fila-1:
                lista_opciones_ficha_selec.append(f"{ficha.columna}:{ficha.fila }")
            
            if ficha.columna==ficha_selec.columna-1 and ficha.fila==ficha_selec.fila-1:
                lista_opciones_ficha_selec.append(f"{ficha.columna}:{ficha.fila }")
    return lista_opciones_ficha_selec



class ficha(pygame.sprite.Sprite):
    def __init__(self,color,altura,tipo,columna,fila):
        super().__init__()

        if color=="blanco":
            if tipo=="peon":
                self.original=pygame.image.load("peon_blanco.png").convert_alpha()
            elif tipo=="alfil":
                self.original=pygame.image.load("alfil_blanco.png").convert_alpha()
            elif tipo=="caballo":
                self.original=pygame.image.load("caballo_blanco.png").convert_alpha()
            elif tipo=="reina": 
                self.original=pygame.image.load("reina_blanca.png").convert_alpha()
            elif tipo=="rey":
                self.original=pygame.image.load("rey_blanco.png").convert_alpha()
            elif tipo=="torre":
                self.original=pygame.image.load("torre_blanca.png").convert_alpha()


        elif color=="negro":
            if tipo=="peon":
                self.original=pygame.image.load("peon_negro.png").convert_alpha()
            elif tipo=="alfil":
                self.original=pygame.image.load("alfil_negro.png").convert_alpha()
            elif tipo=="caballo":
                self.original=pygame.image.load("caballo_negro.png").convert_alpha()
            elif tipo=="reina":
                self.original=pygame.image.load("reina_negra.png").convert_alpha()
            elif tipo=="rey":
                self.original=pygame.image.load("rey_negro.png").convert_alpha()
            elif tipo=="torre":
                self.original=pygame.image.load("torre_negra.png").convert_alpha()

        self.fila=fila#y
        self.columna=columna#x
        self.tipo=tipo
        self.color=color
        self.actualizar(altura)
    
    def actualizar(self,altura):
        self.image=self.original
        self.image=pygame.transform.scale(self.image,(54*altura//100,altura))
        self.rect=self.image.get_rect()
        self.rect.y=self.fila*medida_casilla
        self.rect.x=self.columna*medida_casilla+altura/4

    def actualizar_posicion_logica(self):
        self.fila = int((self.rect.y) // medida_casilla)
        self.columna = int((self.rect.x - medida_casilla / 4) // medida_casilla)
    def mover(self):
        mouse=pygame.mouse.get_pos()
        self.rect.center=(mouse[0],mouse[1])
        self.actualizar_posicion_logica()
#::::::::::::::4/8/25:::::primer intento para hacer las normas de colocacion de las fichas
#para hacer las diferentes situaciones segun el turno o diferenias de movimiento a la hora de matar a otra ficha, pon los requisitos al lado del self
    def restricciones(self,primer_movimento):
        lista_opciones=[]
        if self.tipo == "peon":
            if self.color == "negro":
                if primer_movimento:
                    lista_opciones.append(f"{self.columna}:{self.fila + 1}")
                    lista_opciones.append(f"{self.columna}:{self.fila+2}")
                    
                else:
                    lista_opciones.append(f"{self.columna}:{self.fila + 1}")
                    
            elif self.color == "blanco":
                if primer_movimento:
                    lista_opciones.append(f"{self.columna}:{self.fila - 1}")
                    lista_opciones.append(f"{self.columna}:{self.fila - 2}")
                    
                else:
                    lista_opciones.append(f"{self.columna}:{self.fila - 1}")
                    
                
        
        if self.tipo=="torre":
            for i in range(1,8):
                lista_opciones.append(f"{self.columna}:{self.fila+1*i}")#horizontal
                lista_opciones.append(f"{self.columna}:{self.fila-1*i}")#horizontal
                lista_opciones.append(f"{self.columna+1*i}:{self.fila}")#vertical
                lista_opciones.append(f"{self.columna-1*i}:{self.fila}")#vertical
        
        if self.tipo == "caballo":
            lista_opciones.append(f"{self.columna + 1 * 2}:{self.fila + 1}")  # ↱
            lista_opciones.append(f"{self.columna + 1 * 2}:{self.fila - 1}")  # ↰
            lista_opciones.append(f"{self.columna - 1 * 2}:{self.fila + 1}")  # ↳
            lista_opciones.append(f"{self.columna - 1 * 2}:{self.fila - 1}")  # ↲
            lista_opciones.append(f"{self.columna + 1}:{self.fila + 1 * 2}")  # ⇗ ___|
            lista_opciones.append(f"{self.columna - 1}:{self.fila + 1 * 2}")  # ⇘ ---↓
            lista_opciones.append(f"{self.columna + 1}:{self.fila - 1 * 2}")  # ⇖ |___
            lista_opciones.append(f"{self.columna - 1}:{self.fila - 1 * 2}")  # ⇙ ↓---

        if self.tipo == "alfil":

            for i in range(1,8):
                lista_opciones.append(f"{self.columna + 1 * i}:{self.fila + 1 * i}")  # abajo derecha
                lista_opciones.append(f"{self.columna + 1 * i}:{self.fila - 1 * i}")  # abajo izquierda
                lista_opciones.append(f"{self.columna - 1 * i}:{self.fila + 1 * i}")  # arriba derecha
                lista_opciones.append(f"{self.columna - 1 * i}:{self.fila - 1 * i}") # arriba izquierda
        
        if self.tipo == "reina":
            for i in range(1,8):
                lista_opciones.append(f"{self.columna}:{self.fila+1*i}")#horizontal
                lista_opciones.append(f"{self.columna}:{self.fila-1*i}")#horizontal
                lista_opciones.append(f"{self.columna+1*i}:{self.fila}")#vertical
                lista_opciones.append(f"{self.columna-1*i}:{self.fila}")#vertical
                lista_opciones.append(f"{self.columna + 1 * i}:{self.fila + 1 * i}")  # abajo derecha
                lista_opciones.append(f"{self.columna + 1 * i}:{self.fila - 1 * i}")  # abajo izquierda
                lista_opciones.append(f"{self.columna - 1 * i}:{self.fila + 1 * i}")  # arriba derecha
                lista_opciones.append(f"{self.columna - 1 * i}:{self.fila - 1 * i}") # arriba izquierda

            

        if self.tipo == "rey":
            lista_opciones.append(f"{self.columna + 1}:{self.fila + 1}")
            lista_opciones.append(f"{self.columna + 1}:{self.fila - 1}")
            lista_opciones.append(f"{self.columna - 1}:{self.fila + 1}")
            lista_opciones.append(f"{self.columna - 1}:{self.fila - 1}")
            lista_opciones.append(f"{self.columna}:{self.fila + 1}")
            lista_opciones.append(f"{self.columna }:{self.fila - 1}")
            lista_opciones.append(f"{self.columna + 1}:{self.fila}")
            lista_opciones.append(f"{self.columna - 1}:{self.fila}")  

        for cord in lista_opciones:
            if "-" in cord:
                lista_opciones.remove(cord)

        return lista_opciones
        
    def agrandar(self):
        ancho,alto=self.image.get_size()
        resta=medida_casilla/10
        self.image=pygame.transform.scale(self.original,(ancho+resta,alto+resta))
    def reducir(self):
        ancho,alto=self.image.get_size()
        resta=medida_casilla/10
        self.image=pygame.transform.scale(self.original,(ancho-resta,alto-resta))

#····················································································


class comprobador(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y):
        super().__init__()
        self.image=pygame.Surface((2,2))
        self.image.fill((255,0,0))
        self.rect=self.image.get_rect()
        self.rect.x=pos_x
        self.rect.y=pos_y

#::::::::::::::::::::::↑SPRITE FICHAS↑::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::    

#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

lista_fichas=pygame.sprite.Group()#lista sprites
for i in range(1):
    for c in range(8):
            peon_negro=ficha("negro",medida_casilla,"peon",x+c,y+1)#peon negro 
            lista_fichas.add(peon_negro)
        
    for c in range(8):
            peon_blanco=ficha("blanco",medida_casilla,"peon",x+c,y+6)#peon blanco 
            lista_fichas.add(peon_blanco)

    #torres negras
    torre_negra=ficha("negro",medida_casilla,"torre",x,y)
    lista_fichas.add(torre_negra)
    torre_negra=ficha("negro",medida_casilla,"torre",x+7,y)
    lista_fichas.add(torre_negra)

    #torres blancas
    torre_blanca=ficha("blanco",medida_casilla,"torre",x,y+7)
    lista_fichas.add(torre_blanca)
    torre_blanca=ficha("blanco",medida_casilla,"torre",x+7,y+7)
    lista_fichas.add(torre_blanca)

    #caballos negros
    caballo_negro=ficha("negro",medida_casilla,"caballo",x+1,y)
    lista_fichas.add(caballo_negro)
    caballo_negro=ficha("negro",medida_casilla,"caballo",x+6,y)
    lista_fichas.add(caballo_negro)

    #caballos blancos
    caballo_blanco=ficha("blanco",medida_casilla,"caballo",x+1,y+7)
    lista_fichas.add(caballo_blanco)
    caballo_blanco=ficha("blanco",medida_casilla,"caballo",x+6,y+7)
    lista_fichas.add(caballo_blanco)

    #alfiles negros
    alfil_negro=ficha("negro",medida_casilla,"alfil",x+2,y)
    lista_fichas.add(alfil_negro)
    alfil_negro=ficha("negro",medida_casilla,"alfil",x+5,y)
    lista_fichas.add(alfil_negro)

    #alfiles blancos
    alfil_blanco=ficha("blanco",medida_casilla,"alfil",x+2,y+7)
    lista_fichas.add(alfil_blanco)
    alfil_blanco=ficha("blanco",medida_casilla,"alfil",x+5,y+7)
    lista_fichas.add(alfil_blanco)

    #rey negro
    rey_negro=ficha("negro",medida_casilla,"rey",x+4,y)
    lista_fichas.add(rey_negro)

    #rey blanco
    rey_blanco=ficha("blanco",medida_casilla,"rey",x+4,y+7)
    lista_fichas.add(rey_blanco)

    #reina negra
    reina_negra=ficha("negro",medida_casilla,"reina",x+3,y)
    lista_fichas.add(reina_negra)

    #reina blanca
    reina_blanca=ficha("blanco",medida_casilla,"reina",x+3,y+7)
    lista_fichas.add(reina_blanca)

lista_fichas_muertas=pygame.sprite.Group()

diccionario_peones={}

diccionario_posiciones_muertas=[{"peon":"8:7","caballo":"9:7","alfil":"8:6","torre":"9:6","reina":"8:5","rey":"9:5"},{"peon":"8:0","caballo":"9:0","alfil":"8:1","torre":"9:1","reina":"8:2","rey":"9:2"}]#blanco,negro



alfombra=pygame.image.load("alfombra.png").convert_alpha()
alfombra=pygame.transform.scale(alfombra,(ancho_tablero/5,alto_tablero))
ficha_seleccionada = None
arrastrando=False
pos_original_fila=0#fila actual
pos_original_columna=0#columna actual
turno=0
#print(lista_fichas)
bot_=True

color_bot="negro"
color_humano="blanco"
tocando=False
ficha_tocada=None




#::::::::::::::::::::::↓INICIO WHILE↓::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
jugando=True
while jugando:
    for evento in pygame.event.get():
        if evento.type==pygame.QUIT:
            jugando=False
        
        #REDIMENSIO PANTALLA
        if evento.type==pygame.VIDEORESIZE:
            
            ancho_tablero=evento.w
            alto_tablero=evento.w-evento.w/5
            pantalla=pygame.display.set_mode((ancho_tablero,alto_tablero),pygame.RESIZABLE)
            medida_casilla=ancho_tablero/10

            alfombra=pygame.transform.scale(alfombra,(ancho_tablero/5,alto_tablero))
    

    if len(lista_fichas_muertas)>0:
        if ficha_tocada==None:
            for ficha_eliminada in lista_fichas_muertas:
                if ficha_eliminada.rect.collidepoint(pygame.mouse.get_pos()):
                    ficha_tocada=ficha_eliminada
                    ficha_tocada.agrandar()
                    break
    
    if ficha_tocada!=None and ficha_tocada.rect.collidepoint(pygame.mouse.get_pos())==False:
        ficha_tocada.reducir()
        ficha_tocada=None



    
    #DIBUJAR TABLERO
    y=0
    x=0
    for fila in range(8):
        for casilla in range(8):
            if (fila+casilla)%2==0:
                pygame.draw.rect(pantalla,(245, 245, 220),(x,y,medida_casilla,medida_casilla))
                x+=medida_casilla
            elif (fila+casilla)%2==1:
                pygame.draw.rect(pantalla,(139, 69, 19),(x,y,medida_casilla,medida_casilla))
                x+=medida_casilla
        
        x=0
        y+=medida_casilla


    lista_casillas_ocupadas=[]
    for pieza in lista_fichas:
        lista_casillas_ocupadas.append(f"{pieza.columna}:{pieza.fila}")

#:::::::::::::MOVER FICHA::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    if ((turno%2==0 and color_humano=="blanco")or(turno%2==1 and color_humano=="negro")) or bot_==False:
        mouse=pygame.mouse.get_pos()
        mouse_cord=f"{int(mouse[0]//medida_casilla)}:{int(mouse[1]//medida_casilla)}"
        boton=pygame.mouse.get_pressed()
        
        if boton[0]==True and ficha_seleccionada==None:#primer click

            for pieza in lista_fichas:#para cada ficha de la lista de fichas
                if pieza.rect.collidepoint(mouse):#si ese click colisiona con una ficha
                    ficha_seleccionada=pieza#la ficha seleccionada es la colisionada
                    
                    if ficha_seleccionada.tipo=="peon" and f"{ficha_seleccionada.columna}:{ficha_seleccionada.fila}" in ["0:1","1:1","2:1","3:1","4:1","5:1","6:1","7:1","0:6","1:6","2:6","3:6","4:6","5:6","6:6","7:6",]:
                        lista_opciones=ficha_seleccionada.restricciones(True)#metemos las coordenadas enla lisya de reestricciones
                    else:
                        lista_opciones=ficha_seleccionada.restricciones(False)

                    pos_ox=ficha_seleccionada.rect.x+medida_casilla/4
                    pos_oy=ficha_seleccionada.rect.y+medida_casilla/2
                    pos_original_fila=ficha_seleccionada.fila#fila original
                    pos_original_columna=ficha_seleccionada.columna#columna original

                    if ficha_seleccionada.tipo=="peon":
                        lista_comparar=lista_opciones.copy()
                        nueva=matar_peon(ficha_seleccionada,lista_fichas)
                        lista_opciones+=nueva
    #ficha_selec,lista_opciones_ficha_selec,lista_fichas
                        #print(lista_opciones,"::::::::segunda version lista opciones::::::lista_opciones::::::::::::::::::::")
                        #print(lista_comparar,"········primera version lista opciones············lista_coparar·························")
                    #print(lista_opciones,"lista opciones")


                    break#salimos del for
        if boton[0]==True and ficha_seleccionada!=None:
            
            base=mouse[0]-pos_ox
            medida_linea=int(math.sqrt((mouse[0]-pos_ox)**2+(mouse[1]-pos_oy)**2))
            #print(f"medida linea={medida_linea}")
            

            #pygame.draw.line(pantalla,(255,0,0),(pos_ox,pos_oy),(mouse),3)
            arrastrando=True
            ficha_seleccionada.mover()
            ##guardamos todas sus coordenadas posibles de movimiento
            
            #si es peon creamos la lista nueva
            
        if boton[0]==False and ficha_seleccionada!=None:#soltamos el boton
            colocado=False
            cords_atravesadas=[]
            x_recorridas=[]
            y_recorridas=[]
            ultima_cord_mouse=(int(mouse[0]//medida_casilla),int(mouse[1]//medida_casilla))
            pos_ox=int(pos_ox//medida_casilla)#posicion orginal X
            pos_oy=int(pos_oy//medida_casilla)#posicion original Y
            cordenada_inicial=f"{pos_ox}:{pos_oy}"#cordenada inicial
            cordenada_final=f"{ultima_cord_mouse[0]}:{ultima_cord_mouse[1]}"#cordenada final
            cords_atravesadas=casillas_recorridas(cordenada_inicial,cordenada_final)#uso la funcion casillas_recorridas para obtener las coordenadas atravesadas

            #print(cords_atravesadas,"cords atravesadas")
            
            if turno%2==0:
                color="blanco"
            else:
                color="negro"


    #__________________________________________________________________________________
            cord_columna=int(mouse[0]//medida_casilla)
            cord_fila=int(mouse[1]//medida_casilla)
            coordenada_destino = f"{cord_columna}:{cord_fila}"
            if 0<=cord_columna<=7 and 0<=cord_fila<=7 and ficha_seleccionada.color==color:
                casilla_ocupada=False
                
                if ficha_seleccionada.tipo!="caballo":
                    for cord in cords_atravesadas:
                        for pieza in lista_fichas:
                            if f"{pieza.columna}:{pieza.fila}"==cord:
                                ficha_seleccionada.columna=pos_original_columna
                                ficha_seleccionada.fila=pos_original_fila
                                ficha_seleccionada.actualizar(medida_casilla)
                                casilla_ocupada=True
                                break

                
                
                for pieza in lista_fichas:
                    if pieza.columna==cord_columna and pieza.fila==cord_fila and ficha_seleccionada.color==pieza.color:
                        ficha_seleccionada.columna=pos_original_columna
                        ficha_seleccionada.fila=pos_original_fila
                        ficha_seleccionada.actualizar(medida_casilla)
                        casilla_ocupada=True
                        #print("rechazado 1")
                        break
                        
                    if pieza.columna==cord_columna and pieza.fila==cord_fila and ficha_seleccionada.color!=pieza.color and ficha_seleccionada.tipo!="peon":
                        
                        ficha_seleccionada.columna=pieza.columna
                        ficha_seleccionada.fila=pieza.fila
    
                        pieza.columna=int(diccionario_posiciones_muertas[turno%2][pieza.tipo][0])
                        pieza.fila=int(diccionario_posiciones_muertas[turno%2][pieza.tipo][2])
                        lista_fichas_muertas.add(pieza)     
                        lista_fichas.remove(pieza)
                        
                        ficha_seleccionada.actualizar(medida_casilla)
                        colocado=True
                        break

                    #peones   v
                    if pieza.columna==cord_columna and pieza.fila==cord_fila and ficha_seleccionada.color!=pieza.color and ficha_seleccionada.tipo=="peon" and coordenada_destino in lista_opciones and coordenada_destino not in lista_comparar:
                        ficha_seleccionada.columna=pieza.columna
                        ficha_seleccionada.fila=pieza.fila
                        
                        pieza.columna=int(diccionario_posiciones_muertas[turno%2][pieza.tipo][0])
                        pieza.fila=int(diccionario_posiciones_muertas[turno%2][pieza.tipo][2])
                        lista_fichas_muertas.add(pieza)
                        lista_fichas.remove(pieza)
                                                
                        ficha_seleccionada.actualizar(medida_casilla)
                        colocado=True
                        break


                    if pieza.columna==cord_columna and pieza.fila==cord_fila and ficha_seleccionada.color!=pieza.color and ficha_seleccionada.tipo=="peon" and coordenada_destino in lista_comparar and coordenada_destino in lista_opciones:

                        ficha_seleccionada.columna=pos_original_columna
                        ficha_seleccionada.fila=pos_original_fila
                        ficha_seleccionada.actualizar(medida_casilla)
                        casilla_ocupada=True
                        #print("rechazado 2")
                        break



                if casilla_ocupada==False and coordenada_destino in lista_opciones :
                    ficha_seleccionada.columna=cord_columna
                    ficha_seleccionada.fila=cord_fila
                    ficha_seleccionada.actualizar(medida_casilla)
                    colocado=True
                    #print("ha entrado ")

                else:
                    ficha_seleccionada.columna=pos_original_columna
                    ficha_seleccionada.fila=pos_original_fila
                    ficha_seleccionada.actualizar(medida_casilla)
                    #print("rechazado 3")

            else:
                ficha_seleccionada.columna=pos_original_columna
                ficha_seleccionada.fila=pos_original_fila
                ficha_seleccionada.actualizar(medida_casilla)
                #print("rechazado 4")
            ficha_seleccionada=None
            arrastrando=False


            if colocado==True:
                turno+=1

    elif bot_==True and (turno%2==1 and color_bot=="negro" or turno%2==0 and color_bot=="blanco"):

#lista_opciones_finales.append({"atacante":ficha_bot_actual,"victima":victima_cord,"valor jugada":valor_jugada,"lista rival":lista_rival})

        objetivo=bot(lista_fichas,lista_casillas_ocupadas,color_bot,medida_casilla)
        cordenada_objetivo=objetivo["victima"]
        #print(cordenada_objetivo,"  cordenada mandada por la funcion bot para colocar la ficha")
        eliminar_ficha_rival=False
        ficha_bot=objetivo["atacante"]
        #print(ficha_bot.tipo," tipo ficha bot")
        ficha_objetivo=None
        #print(ficha_objetivo, "    despues del None")
        for ficha_rival in objetivo["lista rival"]:
            if f"{ficha_rival.columna}:{ficha_rival.fila}"==cordenada_objetivo:
                eliminar_ficha_rival=True
                ficha_objetivo=ficha_rival
        
        if eliminar_ficha_rival==True:#matar
            ficha_bot.columna=ficha_objetivo.columna
            ficha_bot.fila=ficha_objetivo.fila
            
            ficha_objetivo.columna=int(diccionario_posiciones_muertas[turno%2][ficha_objetivo.tipo][0])
            ficha_objetivo.fila=int(diccionario_posiciones_muertas[turno%2][ficha_objetivo.tipo][2])
            lista_fichas_muertas.add(ficha_objetivo)
            lista_fichas.remove(ficha_objetivo)
            ficha_bot.actualizar(medida_casilla)
            turno+=1

        else:#no matar
            ficha_bot.columna=int(objetivo["victima"][0])
            ficha_bot.fila=int(objetivo["victima"][2])
            ficha_bot.actualizar(medida_casilla)
            turno+=1






    
    #dibujar tablero
    y=0
    x=0
#_____________________________________________________________________________________________
    

    
    if arrastrando==False:
        for pieza in lista_fichas:
            pieza.actualizar(medida_casilla)
        peon_negro.actualizar(medida_casilla)
        
        

    pantalla.blit(alfombra,(ancho_tablero-(ancho_tablero/5),0))

    lista_fichas_muertas.draw(pantalla)
    lista_fichas.draw(pantalla)
    

    #for sprite in lista_fichas:
        #pygame.draw.rect(pantalla, (57, 255, 20), sprite.rect, 2)
    if turno%2==0:
        pygame.draw.rect(pantalla, (240,240,240), (0,0,medida_casilla/4,medida_casilla/4))

        pygame.draw.rect(pantalla, (0,0,0), (0,0,medida_casilla/4,medida_casilla/4),4)

    if turno%2==1:
        pygame.draw.rect(pantalla, (50, 50, 50), (0,0,medida_casilla/4,medida_casilla/4))

        pygame.draw.rect(pantalla, (0,0,0), (0,0,medida_casilla/4,medida_casilla/4),4)





    if len(lista_fichas_muertas)>0:
        for ficha_muerta in lista_fichas_muertas:
            if ficha_muerta!=ficha_tocada:
                ficha_muerta.actualizar(medida_casilla)

    clock.tick(60)

    pygame.display.flip()

def menu():
    fondo=pygame.image.load("fondo.png")
    
