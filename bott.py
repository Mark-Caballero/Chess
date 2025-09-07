import pygame,random
pygame.init()
clock=pygame.time.Clock()
import math


medida_casilla=120
casillas_por_fila=8

ancho_tablero=medida_casilla*casillas_por_fila
alto_tablero=ancho_tablero
y=0#fondo
x=0#fondo

pantalla=pygame.display.set_mode((ancho_tablero,alto_tablero),pygame.RESIZABLE)
lista_opciones=[]#coordenada que se pueden utilizar para la ficha seleccionada


def movimiento_valido(lista_casillas_ocupadas,lista_coordenadas, tipo_ficha):
    if tipo_ficha=="caballo":
        return lista_coordenadas
    
    if tipo_ficha=="reina":
        for cord in lista_coordenadas:
            if cord in lista_casillas_ocupadas:
                lista_coordenadas.remove(cord)

def casillas_recorridas(cordenada_inicial,cordenada_final):

    x_inicial=int(cordenada_inicial[0])
    y_inicial=int(cordenada_inicial[2])
    x_final=int(cordenada_final[0])
    y_final=int(cordenada_final[2])
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

#____________________________________________________________________________
def bot(lista_fichas,lista_casillas_ocupadas,color,medida_casilla):#objetivo:que el bot sepa donde tiene que mover la ficha
    lista_blancas=[]#lista de fichas blancas
    lista_negras=[]#lista de fichas negras
    lista_preferencias=["rey","reina","torre","alfil","caballo","peon"]#orden fichas por valor
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
    #______________________________


    lista_opciones_posibles=[]#lista donde guardaremos las opciones de cada ficha del bot

    for ficha in lista_bot:#para cada ficha del bot
        lista_opciones=[]
        lista_opciones=ficha.restricciones(True)#metemos las coordenadas en la lista_opciones_posibles
        #ya tenemos todas las coordenadas de la ficha seleccionada del equipo de BOT
        print(lista_opciones,"lista opciones de la ficha que se esta revisando actualmente(",ficha.tipo,")")
        #print("______________________________________________")
        #for fich in lista_rival:
        
        #   print(f"{int(fich.rect.x//medida_casilla)}:{int(fich.rect.y//medida_casilla)}||||||{fich.tipo}")
        #print("_____________________________________________________________")
        for ficha_rival in lista_rival:
            if f"{int(ficha_rival.rect.x//medida_casilla)}:{int(ficha_rival.rect.y//medida_casilla)}" in lista_opciones:
                print("encontrado!!!")
                lista_opciones_posibles.append({"ficha_atacante_bot":ficha,"posicion_ficha_rival":f"{ficha_rival.rect.x//medida_casilla}:{ficha_rival.rect.y//medida_casilla}","tipo_ficha_rival":ficha_rival.tipo,"ficha_rival":ficha_rival})
    
    print(lista_opciones_posibles,"lista opciones posibles")
    ficha_objetivo=None#lista de fichas rivales que podemos atacar
    numero=0
    if len(lista_opciones_posibles)>0:
        for opcion in lista_opciones_posibles:
            if opcion["tipo_ficha_rival"]==lista_preferencias[numero]:
                ficha_objetivo=[opcion]
                return ficha_objetivo
            numero+=1  


    else:
        objetivo=None
        while(objetivo==None):
            ficha_para_mover=random.choice(lista_bot)
            opciones=[]
            opciones.append(ficha_para_mover.restricciones(True))
            if ficha_para_mover.tipo!="peon":
                objetivo=None
            else:
                posicion_escogida=random.choice(opciones)
                objetivo=[{"ficha_atacante_bot":ficha_para_mover,"posicion_de_movimiento":posicion_escogida}]
                return objetivo



        




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



ficha_seleccionada = None
arrastrando=False
pos_original_fila=0#fila actual
pos_original_columna=0#columna actual
turno=0
#print(lista_fichas)

#::::::::::::::::::::::↓INICIO WHILE↓::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
jugando=True
while jugando:
    for evento in pygame.event.get():
        if evento.type==pygame.QUIT:
            jugando=False
        
        #REDIMENSION PANTALLA
        if evento.type==pygame.VIDEORESIZE:
            ancho_tablero=evento.w
            alto_tablero=evento.w
            pantalla=pygame.display.set_mode((ancho_tablero,alto_tablero),pygame.RESIZABLE)
    
#········dibujar·tabla··························
    x=0
    y=0
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
    if turno%2==0:
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
                        print("rechazado 1")
                        break
                        
                    if pieza.columna==cord_columna and pieza.fila==cord_fila and ficha_seleccionada.color!=pieza.color and ficha_seleccionada.tipo!="peon":
                        
                        ficha_seleccionada.columna=pieza.columna
                        ficha_seleccionada.fila=pieza.fila
                        pieza.kill()
                        ficha_seleccionada.actualizar(medida_casilla)
                        colocado=True
                        break

                    #peones   v
                    if pieza.columna==cord_columna and pieza.fila==cord_fila and ficha_seleccionada.color!=pieza.color and ficha_seleccionada.tipo=="peon" and coordenada_destino in lista_opciones and coordenada_destino not in lista_comparar:
                        ficha_seleccionada.columna=pieza.columna
                        ficha_seleccionada.fila=pieza.fila
                        pieza.kill()
                        ficha_seleccionada.actualizar(medida_casilla)
                        colocado=True
                        break


                    if pieza.columna==cord_columna and pieza.fila==cord_fila and ficha_seleccionada.color!=pieza.color and ficha_seleccionada.tipo=="peon" and coordenada_destino in lista_comparar and coordenada_destino in lista_opciones:

                        ficha_seleccionada.columna=pos_original_columna
                        ficha_seleccionada.fila=pos_original_fila
                        ficha_seleccionada.actualizar(medida_casilla)
                        casilla_ocupada=True
                        print("rechazado 2")
                        break



                if casilla_ocupada==False and coordenada_destino in lista_opciones :
                    ficha_seleccionada.columna=cord_columna
                    ficha_seleccionada.fila=cord_fila
                    ficha_seleccionada.actualizar(medida_casilla)
                    colocado=True
                    print("ha entrado ")

                else:
                    ficha_seleccionada.columna=pos_original_columna
                    ficha_seleccionada.fila=pos_original_fila
                    ficha_seleccionada.actualizar(medida_casilla)
                    print("rechazado 3")

            else:
                ficha_seleccionada.columna=pos_original_columna
                ficha_seleccionada.fila=pos_original_fila
                ficha_seleccionada.actualizar(medida_casilla)
                print("rechazado 4")
            ficha_seleccionada=None
            arrastrando=False


            if colocado==True:
                turno+=1

    else:
        #parte bot
        ficha_objetivo=bot(lista_fichas,lista_casillas_ocupadas,"negro",medida_casilla)
        cordd=ficha_objetivo[0]["posicion_ficha_rival"]
        tipo=ficha_objetivo[0]["tipo_ficha_rival"]
        print("||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
        print(tipo,cordd,ficha_objetivo,"ficha objetivo")
        #[{"tipo_ficha_atacante_bot":ficha_para_mover.tipo,"posicion_de_movimiento":random.choice(opciones)}]
        #lista_opciones_posibles.append({"tipo_ficha_atacante_bot":ficha.tipo,"posicion_ficha_rival":f"{ficha_rival.rect.x//medida_casilla}:{ficha_rival.rect.y//medida_casilla}","tipo_ficha_rival":ficha_rival.tipo,"ficha_rival":ficha_rival})

        if len(ficha_objetivo[0])==4:
            print("🟩")
            print(ficha_objetivo[0]["posicion_ficha_rival"],"posicion_ficha_rival")
            x_str, y_str = convertir2(ficha_objetivo[0]["posicion_ficha_rival"])

            ficha_bot=ficha_objetivo[0]["ficha_atacante_bot"]
            ficha_rival=ficha_objetivo[0]["ficha_rival"]

            ficha_bot.columna=int(x_str)
            ficha_bot.fila=int(y_str)
            ficha_bot.actualizar(medida_casilla)
            ficha_rival.kill()
            turno+=1


        else:
            print("🟥")
#{"ficha_atacante_bot":ficha_para_mover,"posicion_de_movimiento":posicion_escogida}
            
            x_str, y_str = ficha_objetivo[0]["posicion_de_movimiento"].split(":")
            ficha_bot=ficha_objetivo[0]["ficha_atacante_bot"]
            ficha_rival=ficha_objetivo[0]["ficha_rival"]
            print(x_str,y_str,"coordenadas de la ficha bot")
            ficha_bot.columna = int(x_str)
            ficha_bot.fila = int(y_str)

            ficha_bot.actualizar(medida_casilla)
            

            
        
            #ficha_bot.columna=int(x_str)//medida_casilla
            #ficha_bot.fila=int(y_str)//medida_casilla





    
    medida_casilla=ancho_tablero/casillas_por_fila #medidas de la casilla segun el tamao de la pantalla
    #dibujar tablero
    y=0
    x=0
#_____________________________________________________________________________________________
    

    
    if arrastrando==False:
        for pieza in lista_fichas:
            pieza.actualizar(medida_casilla)
        peon_negro.actualizar(medida_casilla)
    
    lista_fichas.draw(pantalla)
    

    #for sprite in lista_fichas:
        #pygame.draw.rect(pantalla, (57, 255, 20), sprite.rect, 2)
    if turno%2==0:
        pygame.draw.rect(pantalla, (240,240,240), (0,0,medida_casilla/4,medida_casilla/4))

        pygame.draw.rect(pantalla, (0,0,0), (0,0,medida_casilla/4,medida_casilla/4),4)

    if turno%2==1:
        pygame.draw.rect(pantalla, (50, 50, 50), (0,0,medida_casilla/4,medida_casilla/4))

        pygame.draw.rect(pantalla, (0,0,0), (0,0,medida_casilla/4,medida_casilla/4),4)


    


    clock.tick(60)
    pygame.display.flip()