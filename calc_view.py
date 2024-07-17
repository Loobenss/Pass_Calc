from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.graphics import RoundedRectangle
from kivy.graphics import Color
from kivy.uix.button import Button


class Calc_view(Widget):
    nb = [] # recois le numero presse
    res = [] # list qui recois les valeurs retournees pour faire la somme
    ind = 0 # indexe la case res[] a mettre les valeurs

    mult = []
    div = []
    sous = 0
    err = 0
    opera = ""
    Builder.load_file('view.kv') # charge le fichier.kv

    def __init__(self, **kwargs):
        super(Calc_view, self).__init__(**kwargs)
        self.opera = self.ids.opera.text


    def press_effacer(self):
        self.ids.image.source = 'erase_on_press.png'
        # self.ids.eff.background_color = (1, 1, 1, .2)
        self.ids.eff.background_normal = ''
        # self.ids.image.size = 37, 36
        self.ids.image.size = 60, 60

        newchaine = self.ids.opera.text[:-1]
        if newchaine == '':
            newchaine = '0'
        self.ids.opera.text = self.unite_apost(newchaine)

        if self.ids.opera.text == '':
            self.ids.opera.text = '0'

        self.opera = self.ids.opera.text
        self.clear_all()
        self.ids.opera.text = self.opera
        self.process()
    
    def release_effacer(self):
        self.ids.image.source = 'erase_on_release.png'
        self.ids.image.size = 65, 65
        self.ids.eff.background_color = (0, 0, 0, 0)
        self.ids.eff.background_normal = ''
        ...
    def press_but(self, but):
        # if but != "":
            if self.ids.opera.text != "":
                self.virg = 0
                self.display(but) # Affiche le boutton presse
                self.clear()
                self.nbp = 0
                self.process_parenth(self.ids.opera.text)
                # self.pare = 0
                self.process()
            else:
                if but not in ("+", "-", "x", "/", "%"):
                    self.ids.opera.text = " "
                    self.display(but) # Affiche le boutton presse
                elif but in ("+", "-", "x", "/", "%") and self.ids.result.text != "":
                    self.display(but)

    def display(self, but):
        if self.ids.opera.text == "" and self.ids.result != "" and self.eq == True and but in ("+", "-", "x", "/"):
            self.ids.opera.text = self.ids.result.text + but
            self.ids.result.text = ""
            self.eq = False

        try:
            # Remplace sign presser plusieur fois
            if (self.ids.opera.text[-1] in ("+", "-", "x", "/") and but in ("+", "-", "x", "/")) or (self.ids.opera.text[-2] in ("+", "-", "x", "/") and self.ids.opera.text[-1] == "0"):
                newchaine = self.ids.opera.text[:-1]
                # print("1")
                self.ids.opera.text = newchaine
            # Pour ajouter "0." apres un signe si user presse "." like(6x0.5)
            if self.ids.opera.text[-1] in ("+", "-", "x", "/") and but == ".":
                self.ids.opera.text = self.ids.opera.text + "0" + but
                # print("2")
        except IndexError as e:
            ...
        
        # if self.ids.opera.text == "" and but in ("-"):
        #     self.ids.opera.text = "-" + "(" + but///////////////////////////////////////////////////////////////
        # elif self.ids.opera.text == "" and but in ("+", "-", "x", "/", "."):
        #     self.ids.opera.text = "-"
        if (self.ids.opera.text[-1] == "(" or self.ids.opera.text[-1] == ".") and but in ("+", "-", "x", "/"):
            if but in ("+", "x", "/", "."):
                self.ids.opera.text = self.ids.opera.text + "0" + but
            else:
                self.ids.opera.text = self.ids.opera.text + but
        elif self.ids.opera.text[-1] == ")" and but not in ("+", "-", "x", "/", ".", "") :
            self.ids.opera.text = self.ids.opera.text + but 
        elif self.ids.opera.text[-1] == ")" and but == ".":
            self.ids.opera.text = self.ids.opera.text + "0." + but
        elif self.ids.opera.text != "0" and self.ids.opera.text != "":
            # print("3")
            self.ids.opera.text = self.ids.opera.text + but
        elif self.ids.opera.text == "0" and but in ("+", "-", "x", "/", "."):
            # print("4")
            self.ids.opera.text = "0" + but
        else:
            # print("5")
            self.ids.opera.text = but


        # boucle pour ramenner le nombre de point dans un nombre  
        for inp in self.ids.opera.text:
            if inp == ".":
                self.point += 1
            if inp in ("+", "-", "x", "/", "(", ")"):
                self.point = 0
        # Verifier s'il a deja un point dans un nombre pour supprimme le deuxieme point
        if self.point > 1:
            self.ids.opera.text = self.ids.opera.text[:-1]

        self.ids.opera.text = self.unite_apost(self.ids.opera.text)


    point = 0
    sign = False
    def add_concat(self, inp):
        
        if self.ind == (len(self.res) - 1):
            self.res[self.ind] = self.res[self.ind] + inp
        else:
            self.res.insert(self.ind, inp)

    def process(self):
        self.load_operation(self.opera)
        self.result()

    def percentage(self):
        if self.ids.opera.text in ("0", "") or self.ids.opera.text[-1] in ("+", "-", "/", "x", "(", "%"):
            ...
        else:
            self.ids.opera.text = self.ids.opera.text + "%"
            self.press_but("")

    #Gerer les parentheses
    pare = 0
    nbp = 0
    def parenthOnOff(self, push):
        self.pare += push
        if self.ids.opera.text == "":
            self.ids.opera.text = " "

        if self.ids.opera.text[-1] not in ("+", "-", "/", "x", "(") and self.pare == 1 and self.ids.opera.text != "0":
            # print("HMMMM")
            self.ids.opera.text = self.ids.opera.text + "("
            # self.nbp += 1
        elif self.ids.opera.text == "0" or self.ids.opera.text == "":
            self.ids.opera.text = "("
            # self.nbp += 1
        elif self.ids.opera.text[-1] in ("+", "-", "/", "x", "("):
            # if self.ids.opera.text[-1] == "x":
            #     self.ids.opera.text = self.ids.opera.text[:-1] + "("
            # else:
            self.ids.opera.text = self.ids.opera.text + "("
            # self.nbp += 1
        elif self.ids.opera.text[-1] == ".":
            self.ids.opera.text = self.ids.opera.text + "0("
            # self.nbp += 1
        else:
            if self.nbp > 0:
                self.ids.opera.text = self.ids.opera.text + ")"
                # self.nbp -= 1
                # if self.nbp == 0:
                #     self.pare = 0
        
        self.press_but("")

    
    # def parenthOff(self, push):
    #     if self.pare < 0:
    #         self.pare += push
    #         self.ids.opera.text = self.ids.opera.text + ")"
    
    def percent(self, percent, i):
        percent[i] = ""
        i = i - 1
        p = ""
        per = ""
        while True:
            if percent[i] in ("+", "-", "x", "/") or i < 0:
                pa = 0
                if percent[i-1] == ")" and percent[i] in ("+", "-"):
                    pa += 1
                    a = i - 1
                    while True:
                        
                        per = per + percent[a]
                        
                        
                        if percent[a] == "(":
                            pa -= 1
                        a -= 1
                        if pa <= 0 and a < 0:
                            # print(pa," ", a)
                            break
                            # per = per + "("
                        
                elif percent[i] in ("+", "-"):
                    # print("OKOK")
                    a = i - 1
                    while True:
                        if percent[a] in ("+", "-", "x", "/") or a < 0:                            
                            break
                        per = per + percent[a]
                        a -= 1
                
                p = per[::-1] + "(" + p[::-1] + "/100)"
                break
            p = p + percent[i]
            percent[i] = ""
            i -= 1
        return p

    def process_parenth(self, operation):
        list_op = list()

        for op in operation:
            # print(operation, "nbp1" )
            # # Controle les parenthese pour ne pas se tromper dans la fermeture
            if op == "(":
                self.pare += 1
                self.nbp += 1
            elif op == ")":
                self.pare += 1
                self.nbp -= 1
                if self.nbp == 0:
                    self.pare = 0
            # print(self.pare, "PAre"+ op,  self.nbp)
            list_op.append(op)
        i = 0
        while i < len(list_op):
            # try:
                # print(list_op[4])
            # except IndexError as e:
                # ...
            if list_op[i] == "%":
                a = i
                perc = self.percent(list_op, i)
                # print(perc)
                while True:
                    if list_op[a] in ("+", "-", "x", "/", ")") or a < 0:
                        b = a + 1
                        # print(list_op[a+1])
                        for p in perc:
                            try:
                                list_op.insert(b, p)
                            except IndexError as e:
                                list_op.append(p)
                            b += 1
                            # print(b)
                        break
                    a -= 1
                i = len(list_op)-1
            i += 1
        # print(list_op)
        i = 0
        while i < len(list_op):
            # try:
            #     print(list_op[4])
            # except IndexError as e:
            #     ...
            # if list_op[i] == "%":
            #     a = i
            #     perc = self.percent(list_op, i)
            #     while True:
            #         if list_op[a] in ("+", "-", "x", "/", ")") or a < 0:
            #             b = a + 1
            #             # print(list_op[a+1])
            #             for p in perc:
            #                 try:
            #                     list_op.insert(b, p)
            #                 except IndexError as e:
            #                     list_op.append(p)
            #                 b += 1
            #                 # print(b)
            #             break
            #         a -= 1
            #     i = len(list_op)-1
            
            try:
                if list_op[i+1] == "(" and list_op[i] == "-":
                    list_op.insert(i+1, "1")
            except IndexError as e:
                ...

            if list_op[i] == ")":
                
                # try:
                #     # print(list_op[i])
                #     if list_op[i] == ")" and list_op[i+1] not in ("x","+", "-", "/", "(", ""):
                #         list_op.insert(i+1, "x")
                # except IndexError as e:
                #     ...

                try:
                    if list_op[i+1] == "(" or (list_op[i] == ")" and list_op[i+1] not in ("x","+", "-", "/", ")", "")):
                        list_op.insert(i+1, "x")
                except IndexError as e:
                    ...
                
                
                list_op[i] = ""
                
                inpar = ""
                try:
                    while True:
                        if list_op[i-1] == "(":
                            list_op[i-1] = ""
                            # print(list_op[i-2]+"ooooo")
                            if list_op[i-2] not in ("x","+", "-", "/", "(", "") and i-1 > 0:
                                list_op[i-1] = "x"
                                # print(list_op)
                            break
                        i -= 1
                        inpar += list_op[i]
                        # print(inpar[::-1])
                        list_op[i] = ""
                except IndexError as e:
                    ...
                
                self.load_operation(inpar[::-1])
                
                # print(inpar[::-1])
                #Vient avec le resultat entre parenthese
                for a in self.soma_res():
                    # print(list_op)
                    list_op.insert(i, a)
                    i += 1
                self.clear()
            self.opera = self.list_str(str(list_op))
            i += 1
        
        # print(self.opera + "OP")

    def list_str(self, chaine):
        sup = ["[", "]", "'", ",", " ", '"']
        for s in sup:
            chaine = chaine.replace(s, '')
        return chaine
    
    def plusOuMoins(self):
        if self.ids.opera.text == "0" or self.ids.opera.text == "":
            self.ids.opera.text = "-"
        elif self.ids.opera.text == "-":
            self.ids.opera.text = ""
        else:
            if self.ids.opera.text[-1] == "-" and self.ids.opera.text[-2] == "(":
                ...
            else:
                if self.ids.opera.text[-1] == "(":
                    self.ids.opera.text = self.ids.opera.text + "-"
                else:
                    self.ids.opera.text = self.ids.opera.text + "(-"

    def load_operation(self, chaine_oper):
        for id, inp in enumerate(chaine_oper):
            if inp == "'":
                continue
            if inp == "":
                continue
            if inp == "(":
                continue
            elif inp == ")":
                # self.res = float
                # print(self.ids.result.text)
                continue
            
            if inp not in ("+", "-", "x", "/"):
                self.add_concat(inp)

                if self.sous == -1:
                    # print(self.res)
                    # self.res[self.ind] = str(int(self.res[self.ind]) * self.sous)
                    self.res[self.ind] = "-"+self.res[self.ind]
                    # print(self.res)
                    self.sous = 0
                
                # Pour concatene le deuxieme membre de la multiplication si ce serait un nombre
                # ex: 1x3 qui devient 1X36
                if len(self.mult) == 2:
                    self.mult[1] = self.mult[1] + inp
                    self.multiplier()
                # Pour recuperer l'autre nombre a multiplier
                elif len(self.mult) == 1:
                    self.multiplier()

                if len(self.div) == 2:
                    self.div[1] = self.div[1] + inp
                    self.diviser()
                # Pour recuperer l'autre nombre a diviser
                elif len(self.div) == 1:
                    self.diviser()
    
            match inp:
                
                case "x":
                    self.div = []
                    self.mult = []
                    self.multiplier()
                case "/":
                    self.mult = []
                    self.div = []
                    self.diviser()
                case "-":
                    # self.mult = []
                    # self.div = []

                    if chaine_oper[id-1] not in ("/", "x", "+", "(") and id != 0 :
                        self.mult = []
                        self.div = []
                        self.ind += 1

                    self.sous = -1
                        
                case "+":
                    self.mult = []
                    self.div = []

                    self.ind += 1
                case _:
                    ...
                    # print("Aucune")
        ...
        

    # Nettoie tout apres une operation terminee
    def clear(self):
        self.res = []
        self.ind = 0
        self.mult = []
        self.div = []
        self.sous = 0
        self.point = 0
        self.err = 0
        self.virg = 0
        self.ids.result.font_size = (38)
    
    def clear_all(self):
        self.ids.opera.text = "0"
        self.ids.opera.foreground_color = (1,1,1)
        self.ids.result.text = ""
        self.pare = 0
        self.clear()

    def multiplier(self):
        
        if len(self.mult) == 2:
            self.res.remove(self.res[self.ind])
        else:
            # print(self.res)
            self.mult.append(self.res[self.ind])
            # print(self.res)
            self.res.remove(self.res[self.ind])

        # print(self.mult)
        prod = 1
        if len(self.mult) > 1: 
            for m in self.mult:
                prod *= float(m)
            # print(self.mult)
            self.res.insert(self.ind, str(prod))
            # print(self.res)
    
    def diviser(self):
        if len(self.div) == 2:
            self.res.remove(self.res[self.ind])
        else:
            self.div.append(self.res[self.ind])
            self.res.remove(self.res[self.ind])
        # print(self.div)
        q = 1
        if len(self.div) > 1:
            i = 0
            while i < len(self.div):
                try:
                    if i == 0:
                        q = float(self.div[i]) / q
                    else:
                        q = q / float(self.div[i])
                except ZeroDivisionError as e:
                    self.err = 401
                i += 1
            self.res.insert(self.ind, str(q))
        
    def result(self):
        ver = self.verif()
        # resultat = 0
        # # print(self.res)
        # for r in self.res:
        #     try:
        #         resultat += float(r)
        #     except ValueError as e:
        #         self.ids.result.text = "Erreur"
        if self.err == 401:
            self.ids.result.text = "Erreur"
            self.ids.opera.foreground_color = (1,0,0)
            self.ids.result.foreground_color = (1,0,0)
        else:
            if self.ids.opera.text[-1] in ("+", "-", "x", "/", ".") or ver < 1 or self.nbp != 0:  #or self.res[self.ind][-1] == "."
                self.ids.result.text = ""
            else:
                # print(self.nbp, "nbp" )
                # self.ids.result.text = str(resultat)
                self.ids.result.text = self.unite_apost(self.soma_res())
                self.ids.opera.foreground_color = (1,1,1)
                self.ids.result.foreground_color = (1,1,1, .4)
                self.ids.result.font_size = 50
    
    def soma_res(self):
        resultat = 0
        # print(self.res)
        for r in self.res:
            if r == "":
                continue
            try:
                resultat += float(r)
            except ValueError as e:
                self.ids.result.text = "Erreur"
        resultat = self.clear_zero(resultat)
        return str(resultat)
    
    def clear_zero(self, resul):
        result = ""
        resul = str(resul)
        
        if resul[-1] == "0" and resul[-2] == ".":
            result = resul[:-2]
        else:
            result = resul

        return result

    def verif(self):
        i = 0
        for inp in self.opera:
            if inp in ("+", "-", "x", "/"):
                i += 1

        for inp in self.ids.opera.text:
            if inp in ("+", "-", "x", "/", "%"):
                i += 1

        return i
    
    virg = 0

    def unite_apost(self, resultat):
        newchaine = ""
        resultinv = resultat[::-1]
        unit = True
        point = True
        for inp in resultinv:
            if inp == "'":
                continue
            if inp not in ("+", "-", "x", "/", ".", "(", ")", "%"):
                self.virg += 1
            else:
                self.virg = 0

            if inp != '.' and point is True and '.' in resultinv:
                point = True
                unit = False
            else:
                point = False
                # unit = True

            newchaine = newchaine + inp
            if self.virg > 2 and unit is True:
                # print(self.virg)
                newchaine = newchaine + "'"
                self.virg = 0
            unit = True
        if newchaine[-1] == "'":
            newchaine = newchaine[:-1]
                
        newchaine1 =""
        # Supprimer les apostrophes apres un symbole
        for id, ch in enumerate(newchaine):
            if ch == "'" and newchaine[id+1] in ("+", "-", "x", "/", ".", "(", ")"):
                continue
            else:
                newchaine1 = newchaine1 + ch
        return newchaine1[::-1]
    
    eq = False
    def equal(self):
        if self.ids.result.text != "":
            self.eq = True
            self.ids.opera.text = ""
            self.ids.result.font_size = (100)
            self.ids.result.foreground_color = (1, 1, 1, 1)
        # self.press_but("", 'egal')
    


    def press_color(self, idb):
        bg = Color(rgba=(25/255, 60/255, 130/255, 1))
        self.ids[idb].canvas.before.add(bg)
        po =  RoundedRectangle(pos=self.ids[idb].pos, size=self.ids[idb].size, radius=[15])
        self.ids[idb].canvas.before.add(po)

    def release_color(self, idb):
        bg = Color(rgba=(48/255, 84/255, 150/255, 1))
        # # self.ids.eff.background_color = (0, 0, 0, 0)
        # # self.ids.eff.background_normal = ''
        # self.ids[idb].background_color = (0, 0, 0, 0)
        # self.ids[idb].background_normal = ''
        self.ids[idb].canvas.before.add(bg)
        po =  RoundedRectangle(pos=self.ids[idb].pos, size=self.ids[idb].size, radius=[15])
        self.ids[idb].canvas.before.add(po)

    def release_eq_color(self,idb):
        bg = Color(rgba=(8/255, 44/255, 110/255, 1))
        self.ids[idb].canvas.before.add(bg)
        po =  RoundedRectangle(pos=self.ids[idb].pos, size=self.ids[idb].size, radius=[15])
        self.ids[idb].canvas.before.add(po)
        
