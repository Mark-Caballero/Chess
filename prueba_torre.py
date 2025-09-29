def eliminar_cords_no_validas2(lista_cordenadas):
    lista_final=[]
    nums=["0","1","2","3","4","5","6","7"]
    for cord in lista_cordenadas:
        if len(cord)==3 and cord[0] in nums and cord[2] in nums and cord[1]==":":
            lista_final.append(cord)
    return lista_final



def ordenar_cords_lista(lista_cords_por_angulos,xx,yy):
    x=xx
    y=yy
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
    

def cords_atravesadas_bot(lista_cords_bot,lista_posiciones_rivales,lista_posiciones_bots):
    lista_cords_por_angulos=[[],[],[],[],[],[],[],[]]
    tipo_ficha="torre"
    pos_ficha=f"{1}:{5}"
    

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
    
    lista_cords_por_angulos=ordenar_cords_lista(lista_cords_por_angulos,1,5)
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

    
    return lista_final



lista_opciones=['1:6', '1:4', '2:5', '0:5', '1:7', '1:3', '3:5', '1:8', '1:2', '4:5', '1:9', '1:1', '5:5', '1:10', '1:0', '6:5', '1:11', '7:5', '1:12', '8:5']
lista_posiciones_rivales=['1:0','2:0','3:0','4:0','5:5','6:0','7:0','4:1','2:3','3:3','5:3','7:3','0:5']
lista_posiciones_bots=['1:5','1:6','2:6','3:6','4:6','5:6','6:6','2:7','3:7','4:7','5:7','6:7']



print(cords_atravesadas_bot(lista_opciones,lista_posiciones_rivales,lista_posiciones_bots))
