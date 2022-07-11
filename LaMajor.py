import random


class Carta():
    def __init__(self, numero, pal):
        assert (
                    0 <= numero), "Error: Valor del numero de la carta es incorrecte"
        assert (
                    numero <= 11), "Error: Valor del numero de la carta es incorrecte"
        assert (0 <= pal), "Error: Valor del pal de la carta es incorrecte"
        assert (pal <= 3), "Error: Valor del pal de la carta es incorrecte"
        self.numero = numero
        self.pal = pal

    def get_numero(self):
        return self.numero

    def get_pal(self):
        return self.pal

    def set_numero(self, numero):
        assert (
                    0 <= numero), "Error: Valor del numero de la carta es incorrecte"
        assert (
                    numero <= 11), "Error: Valor del numero de la carta es incorrecte"
        self.numero = numero

    def set_pal(self, pal):
        assert (pal <= 3), "Error: Valor del pal de la carta es incorrecte"
        assert (0 <= pal), "Error: Valor del pal de la carta es incorrecte"
        self.pal = pal

    def __str__(self):
        Llnomspal = ["Bastos", "Copes", "Espases", "Oros"]
        LLnumero = ["As", "2", "3", "4", "5", "6", "7", "8", "9", "Sota",
                    "Cavall", "Rei"]
        return (LLnumero[self.numero] + " de " + Llnomspal[self.pal])

    def __gt__(self, altre):
        if (self.numero > altre.numero):
            return True
        elif (self.numero == altre.numero):
            if (self.pal < altre.pal):
                return True
            else:
                return False
        else:
            return False


class Baralla():
    def __init__(self):
        self.pila = []
        for i in range(0, 4):
            for e in range(0, 12):
                carta = Carta(e, i)
                self.pila.append(carta)

    def get_pila(self):
        return self.pila

    def set_pila(self, pila):
        self.pila = pila

    def __str__(self):
        out = ""
        for c in self.pila:
            out = out + str(c) + "\n"
        return out

    def barrejar(self):
        random.shuffle(self.pila)

    def pop_carta(self):
        if (len(self.pila) == 0):
            return None
        else:
            carta = self.pila.pop()
            return carta

    def quantitat_cartes(self):
        return (len(self.pila))


class Jugador():
    def __init__(self, nom):
        self.nom = str(nom)
        self.ma = []
        self.rondes = []

    def get_nom(self):
        return self.nom

    def get_ma(self):
        return self.ma

    def get_rondes(self):
        return self.rondes

    def set_nom(self, nom):
        self.nom = str(nom)

    def set_ma(self, ma):
        self.ma = ma

    def set_rondes(self, rondes):
        self.rondes = rondes

    def str_cartes_ma(self):
        cartesma = ""
        a = 1
        for i in self.ma:
            cartesma += (str(a) + " -> " + str(i) + "\n")
            a += 1
        return cartesma

    def afegir_carta_ma(self, carta):
        if (carta != None):
            self.ma.append(carta)

    def afegir_carta_rondes(self, carta1, carta2):
        if (carta1 != None and carta2 != None):
            self.rondes.append(carta1)
            self.rondes.append(carta2)

    def seleccionar_carta_ma(self, index):
        assert (index >= 0 and index < len(
            self.ma)), "Error: Selecció carta incorrecte"
        return self.ma[index]

    def eliminar_carta_ma(self, carta):
        if carta in self.ma:
            self.ma.remove(carta)

    def quantitat_cartes_ma(self):
        return len(self.ma)

    def punts_cartes_rondes(self):
        valor = 0
        for i in self.rondes:
            valor += i.numero + 1
        return valor


class JugadorMaquina(Jugador):
    def _init_(self, nom):
        Jugador.__init__(self, nom)

    def seleccionar_carta_ma(self):
        if len(self.ma) > 1:
            carta_Alta = max(self.ma)
        elif len(self.ma) == 1:
            carta_Alta = self.ma[0]
        else:
            carta_Alta = None
        return carta_Alta


def Joc(nom1, nom2):
    random.seed(nom1 + nom2)
    jugador = Jugador(nom1)
    maquina = JugadorMaquina(nom2)
    baralla = Baralla()
    baralla.barrejar()

    for i in range(3):
        carta1 = baralla.pop_carta()
        jugador.afegir_carta_ma(carta1)
        carta2 = baralla.pop_carta()
        maquina.afegir_carta_ma(carta2)
    while (jugador.quantitat_cartes_ma() > 0) and (
            maquina.quantitat_cartes_ma() > 0):
        print(jugador.str_cartes_ma())
        err = True
        while err == True:
            try:
                tria = int(input(nom1 + " quina carta tires?"))
                se1 = jugador.seleccionar_carta_ma(tria - 1)
                err = False
            except ValueError:
                print("Error : el valor ha de ser un sencer")
            except AssertionError as error:
                print(error)
        se2 = maquina.seleccionar_carta_ma()
        print(nom1, "ha tirat", se1)
        print(nom2, "ha tirat", se2)
        if se1 > se2:
            jugador.afegir_carta_rondes(se1, se2)
        else:
            maquina.afegir_carta_rondes(se1, se2)

        jugador.eliminar_carta_ma(se1)
        maquina.eliminar_carta_ma(se2)

        if (baralla.quantitat_cartes() > 0):
            jugador.afegir_carta_ma(baralla.pop_carta())
            maquina.afegir_carta_ma(baralla.pop_carta())
    return (jugador, maquina)


if __name__ == "__main__":
    nom1 = input()
    nom2 = input()
    jug1, jug2 = Joc(nom1, nom2)
    valor1 = jug1.punts_cartes_rondes()
    print(nom1, "te", valor1)
    valor2 = jug2.punts_cartes_rondes()
    print(nom2, "te", valor2)
    if (valor1 > valor2):
        print("El guanyador és:", nom1)
    elif (valor2 > valor1):
        print("El guanyador és:", nom2)
    else:
        print("Empat!")