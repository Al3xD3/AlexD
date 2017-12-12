import pickle
from random import randint, shuffle, seed, choice
from Joueur import Joueur
from plateau import Plateau, Jeton
from tkinter import *
from utils import jeton_chev
from time import *
from tkinter.filedialog import *

class PositionInvalideException(Exception):
    pass

class MotNonPermisException(Exception):
    pass

class CaseOccupeeException(Exception):
    pass

class CaseVideException(Exception):
    pass
class NombreDeJetonsInvalide(Exception):
    pass



class Scrabble(Tk):
    """
    Classe Scrabble qui implémente aussi une partie de la logique de jeu.
    Les attributs d'un scrabble sont:
    - dictionnaire: set, contient tous les mots qui peuvent être joués sur dans cette partie.
    En gros pour savoir si un mot est permis on va regarder dans le dictionnaire.
    - plateau: Plateau, un objet de la classe Plateau on y place des jetons et il nous dit le nombre de points gagnés.
    - jetons_libres: Jeton list, la liste de tous les jetons dans le sac, c'est là que chaque joueur
                    peut prendre des jetons quand il en a besoin.
    - joueurs: Joueur list,  L'ensemble des joueurs de la partie.
    - joueur_actif: Joueur, le joueur qui est entrain de jouer le tour en cours. Si aucun joueur alors None.
    """

    def __init__(self):
        super().__init__()
        self.title('Scrabble')
        self.fresh_load = False

        # Param des functions de classe
        self.langue_possible = [('Français', 'FR'), ('English', 'EN'), ('Dansk', 'DA')]

        # Debut du dessin de GUI
        self.titre_top = Label(self, text="Mon Super Scrabble", fg="purple", font=("Courier", 30))
        self.titre_top.grid(row=0, column=2, columnspan=4, rowspan=3)

        # Bouton New game
        self.start_new = Button(self, text="Nouvelle Partie", command=self.nouveau_pop, width=30).grid(row=0, column=7,
                                                                                                       pady=2, padx=2)
        # Bouton Charger
        self.start_new = Button(self, text="Charger Partie", command=self.charger_partie, width=30).grid(row=1,
                                                                                                         column=7,
                                                                                                         pady=2, padx=2)
        self.nb_pixels_per_case = 60

        # Bouton explication du jeu
        self.voir_instruction = Button(self, text="Lire instruction", command=self.lire_instruction, width=20).grid(
            row=3, column=7, pady=2, padx=2)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.chevalet = Canvas(self, height=self.nb_pixels_per_case,
                               width=7 * self.nb_pixels_per_case, bg='#645b4b')
        self.chevalet.bind("<Button-1>", self.highlight_case_chevalet)



    def nouveau_pop(self):
        # fenetre de choix nouvelle partie
        self.new = Toplevel(self)
        self.new.wm_title('Nouvelle partie')
        self.new.focus_set()
        self.new.grab_set()
        w = 300  # width for the Tk
        h = 180  # height for the Tk main
        ws = self.winfo_screenwidth()  # width of the screen
        hs = self.winfo_screenheight()  # height of the screen
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.new.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.langue = IntVar()
        self.langue.set(0) #valeur par défaut de la langue à francais
        Label(self.new, text="Langue de jeux?", justify=CENTER, padx=20).grid(row=0, column=0)
        for i in range(len(self.langue_possible)):
            Radiobutton(self.new, text=self.langue_possible[i][0], padx=20, variable=self.langue, value=i).grid(
                row=1 + i, column=0)
        self.nbre_joueur = IntVar()
        self.nbre_joueur.set(2) #valeur par défaut du nombre de joueur à 2
        Label(self.new, text="Nombre de joueur?", justify=CENTER, padx=20).grid(row=0, column=1)
        for i in range(2, 5):
            Radiobutton(self.new, text=str(i) + " joueurs", padx=20, variable=self.nbre_joueur, value=i).grid(row=i - 1,
                                                                                                              column=1)
        Button(self.new, text="Commencer", command=self.nouvelle_partie).grid(column=0, columnspan=2, pady=10)

    def lire_instruction(self):
        # fenetre de choix instruction
        self.new = Toplevel(self)
        self.new.focus_set()
        self.new.grab_set()
        self.new.wm_title("Instruction")
        txt = """
        Bienvenue sur le jeu de Super Scrabble

        Afin de jouer à cette version de Scrabble il vous faudra déplacer les jetons à l'aide 
        de votre souris puis appuyez sur le bouton terminer tour pour valider.

        Plusieurs options s'offre à vous:

        - Vous devez disposer les jetons sur le plateau pour placer un mot.

        - Pour changer vos jetons, il vous faudra les déposer dans le rectangle intitulé 'Changer jetons'.

        - Pour sauter votre tour, conserver les jetons sur votre chevalet
                                                                                       Bonne partie!



                                                                                        """
        Label(self.new, text=txt).grid(row=0, column=0)

    def nouvelle_partie(self):
        """Initie les parametres d'une nouvelle partie
        :param None
        Interface servant a entre le nombre de joueur et la langue utilise
                :return int nbr joueur
        :return str langue FR ou EN
        :exception: Levez une exception avec assert si la langue n'est ni fr, FR, en, ou EN ou si nb_joueur < 2 ou > 4.
        """
        # init plateau
        self.plateau = Plateau(self, 30)
        # init joueur
        self.changer_joueur = True
        self.joueur_actif = None
        # TODO Methode pour nommer nos joueur dynamiquement
        self.joueurs = [Joueur("Joueur {}".format(i + 1)) for i in range(self.nbre_joueur.get())]
        # init langue
        langue = self.langue_possible[self.langue.get()][1]
        if langue.upper() == 'FR':
            # Infos disponibles sur https://fr.wikipedia.org/wiki/Lettres_du_Scrabble
            data = [('E', 15, 1), ('A', 9, 1), ('I', 8, 1), ('N', 6, 1), ('O', 6, 1),
                    ('R', 6, 1), ('S', 6, 1), ('T', 6, 1), ('U', 6, 1), ('L', 5, 1),
                    ('D', 3, 2), ('M', 3, 2), ('G', 2, 2), ('B', 2, 3), ('C', 2, 3),
                    ('P', 2, 3), ('F', 2, 4), ('H', 2, 4), ('V', 2, 4), ('J', 1, 8),
                    ('Q', 1, 8), ('K', 1, 10), ('W', 1, 10), ('X', 1, 10), ('Y', 1, 10),
                    ('Z', 1, 10)]
            nom_fichier_dictionnaire = 'dictionnaire_francais.txt'
        elif langue.upper() == 'EN':
            # Infos disponibles sur https://fr.wikipedia.org/wiki/Lettres_du_Scrabble
            data = [('E', 12, 1), ('A', 9, 1), ('I', 9, 1), ('N', 6, 1), ('O', 8, 1),
                    ('R', 6, 1), ('S', 4, 1), ('T', 6, 1), ('U', 4, 1), ('L', 4, 1),
                    ('D', 4, 2), ('M', 2, 3), ('G', 3, 2), ('B', 2, 3), ('C', 2, 3),
                    ('P', 2, 3), ('F', 2, 4), ('H', 2, 4), ('V', 2, 4), ('J', 1, 8),
                    ('Q', 1, 10), ('K', 1, 5), ('W', 2, 4), ('X', 1, 8), ('Y', 2, 4),
                    ('Z', 1, 10)]
            nom_fichier_dictionnaire = 'dictionnaire_anglais.txt'

        self.jetons_libres = [Jeton(lettre, valeur) for lettre, occurences, valeur in data for i in range(occurences)]
        with open(nom_fichier_dictionnaire, 'r') as f:
            self.dictionnaire = set([x[:-1].upper() for x in f.readlines() if len(x[:-1]) > 1])
            # fin de l'init part a debut jeux

        self.initialiser_jeu()
        self.new.destroy()
        # TODO Que doit ton reseter?

    def close(self):
        self.destroy() #utile pour fermer une fenêtre

    def score_board_update(self):
        txt = "" #text initial nul
        for joueur in self.joueurs:
            txt += '{} :  {} points\n'.format(joueur.nom, joueur.points) #donne un text egal au nom et à l'attribut point de chaque joueur
            self.text_score_joueur.set(txt)

    def compteur_update(self):
        txt = ""
        for joueur in self.joueurs:
            txt += "{} : {} minutes(s)\n".format(joueur.nom, round(float(joueur.temps_de_jeu / 60), 1))
            self.text_temps_joueur.set(txt)

    def joueur_actif_update(self):
        txt = "Au tour de: {}".format(self.joueur_actif.nom)
        self.text_joueur_actif.set(txt)

    def text_mot_update(self, mot):
        self.text_mot_place.set('{}\n{}'.format(self.text_mot_place.get(), mot))

    def initialiser_jeu(self):
        """ *** Vous n'avez pas à coder cette méthode ***
        Étant donnés un nombre de joueurs et une langue. Le constructeur crée une partie de scrabble.
        Pour une nouvelle partie de scrabble,
        - un nouvel objet Plateau est créé;
        - La liste des joueurs est créée et chaque joueur porte automatiquement le nom Joueur 1, Joueur 2, ... Joueur n où n est le nombre de joueurs;
        - Le joueur_actif est None.
        :param nb_joueurs: int, nombre de joueurs de la partie au minimun 2 au maximum 4.
        :param langue: str, FR pour la langue française, et EN pour la langue anglaise. Dépendamment de la langue, vous devez ouvrir, lire, charger en mémoire le fichier "dictionnaire_francais.txt" ou "dictionnaire_anglais.txt" ensuite il faudra ensuite extraire les mots contenus pour construire un set avec le mot clé set.
        Aussi, grâce à la langue vous devez être capable de créer tous les jetons de départ et les mettre dans jetons_libres.
        Pour savoir combien de jetons créés pour chaque langue vous pouvez regarder à l'adresse:
        https://fr.wikipedia.org/wiki/Lettres_du_Scrabble
        *** Dans notre scrabble, nous n'utiliserons pas les jetons jokers qui ne contienent aucune lettre donc ne les incluez pas dans les jetons libres ***
        :exception: Levez une exception avec assert si la langue n'est ni fr, FR, en, ou EN ou si nb_joueur < 2 ou > 4.
        """
        # Bouton Sauvegarder
        self.start_new = Button(self, text="Sauvegarder Partie", command=self.sauvegarder_partie, width=30)
        self.start_new.grid(row=2, column=7, pady=2, padx=2)
        # TODO test function sauvegarde

        # replace le layout pour debut parti
        self.titre_top['text'] = "Mon Super Scrabble"
        self.titre_top.grid(row=0, column=2, columnspan=4, rowspan=1)
        self.plateau.grid(row=1, column=2, columnspan=4, rowspan=18)
        # self.plateau.grid(row=0, column=0, sticky=NSEW)


        # init score board
        self.score_label = Label(self, text="Tableau des Résultats", fg="black", font=("Courier", 12))
        self.score_label.grid(row=1, column=0, pady=2, padx=2)
        self.text_score_joueur = StringVar()
        self.score_joueur = Label(self, textvariable=self.text_score_joueur, fg="black", font=("Courier", 11))
        self.score_joueur.grid(row=2, column=0, pady=2, padx=2, rowspan=4)

        # Init Liste mot joue
        self.liste_label = Label(self, text="Mots Placés", fg="black", font=("Courier", 12))
        self.liste_label.grid(row=8, column=0, pady=2, padx=2)
        self.text_mot_place = StringVar()
        self.text_mot_place.set("")
        self.mot_place = Label(self, textvariable=self.text_mot_place, fg="black", font=("Courier", 11))
        self.mot_place.grid(row=9, column=0, pady=2, padx=2, rowspan=1, sticky=N)

        # init le compteur de temps
        self.compteur_label = Label(self, text="Temps de jeu", fg="black", font=("Courrier", 12))
        self.compteur_label.grid(row=5, column=7, pady=2, padx=2)
        self.text_temps_joueur = StringVar()
        self.temps_joueur = Label(self, textvariable=self.text_temps_joueur, fg="black", font=("Courier", 11))
        # self.text_score_joueur = StringVar()
        # self.score_joueur = Label(self, textvariable=self.text_score_joueur, fg="black", font=("Courier", 11))
        self.temps_joueur.grid(row=6, column=7, pady=2, padx=2, rowspan=4)

        # portion joueur
        self.text_joueur_actif = StringVar()
        self.joueur_actif_label = Label(self, textvariable=self.text_joueur_actif, fg="black", font=("Courier", 12))
        self.joueur_actif_label.grid(row=20, column=3, columnspan=2, pady=2, padx=2)
        self.annonce = StringVar()
        self.annonce_label = Label(self, textvariable=self.annonce, fg="black", font=("Courier", 12))
        self.annonce_label.grid(row=21, column=2, columnspan=4, pady=2, padx=2)
        self.annonce.set('')

        # portion bouton
        self.boutton_placer = Button(self, text="Terminer Tour", command=self.choix_terminer_tour)
        self.boutton_placer.grid(row=22, column=5)
        self.boutton_abandonner = Button(self, text="Abandonner", command=self.choix_abandonner)
        self.boutton_abandonner.grid(row=22, column=3)
        # signature
        self.score_label = Label(self, text="Creation Dec 2017", fg="black", font=("Courier", 6))
        self.score_label.grid(row=23, column=6, pady=2, padx=2, columnspan=2)

        # c'est parti : début du jeu
        if self.fresh_load == True:
            self.fresh_load = False
            self.plateau.dessiner()
            self.dessiner_chevalet()
        self.debut_jeux()

    # -------------------------------------  Fin d<init jeux ----------------------------------------

    def debut_jeux(self):
        global start_time #de manière à implémenter le compteur
        start_time = time() #un temps de début pour le premier joueur pour faire time - start_time = elapsed_time
        if self.joueur_actif == None:
            self.joueur_suivant() #au début de la partie aucun joueur actif, sélectionner le premier joueur
        for jeton in self.tirer_jetons(self.joueur_actif.nb_a_tirer):
            self.joueur_actif.ajouter_jeton(jeton)
        self.update_board() #mettre à jour le pointage ,le nombre de minutes et le nombre de joueur

    def prochain_tour(self):
        # efface jeton du joueur d'avant
        self.plateau.dessiner()
        # Verif si fin de parti
        self.partie_terminee()
        if self.changer_joueur:
            self.joueur_suivant()
        for jeton in self.tirer_jetons(self.joueur_actif.nb_a_tirer):
            self.joueur_actif.ajouter_jeton(jeton)
        self.update_board()

    def update_board(self): #fonction utilisée entre chaque tour pour MÀJ l'ensemble des canvas dynamique
        self.joueur_actif_update()
        self.score_board_update()
        self.compteur_update()

    def choix_passer_tour(self): #pour passer son tour
        self.changer_joueur = True
        self.prochain_tour()

    def choix_abandonner(self): #permet au joueur actif de quitter la partie
        quitter = self.joueur_actif
        self.joueur_suivant()
        self.joueurs.remove(quitter)
        self.changer_joueur = False
        self.prochain_tour()

    def choix_changer_jeton(self, swap_jeton):
        for pos in swap_jeton:
            self.jetons_libres.append(
                self.joueur_actif.retirer_jeton(int(pos)))  # retire jeton et l'ajoute à la liste des disponibles
        jeton_pigee = self.tirer_jetons(len(swap_jeton))
        for i in range(0, len(jeton_pigee)):
            self.joueur_actif.ajouter_jeton(jeton_pigee[i])
        self.changer_joueur = True
        self.prochain_tour()

    def choix_terminer_tour(self):
        # fonction qui decide quel type de tour a ete jouer
        pos_chevalet = []
        pos_plateau = []
        pos_chev_changer = []
        offset = self.nb_pixels_per_case // 2  # pour pointer a partir du centre du jeton
        for jeton in self.plateau.jeton_chevalet:
            if jeton.ypos < self.plateau.coords(self.plateau.chevalet)[
                1] - self.nb_pixels_per_case:  # regarde ceux qui ne sont dans le plateau
                pos_chevalet.append(jeton.position)
                pos_plateau.append((jeton.xpos + offset, jeton.ypos + offset))
            if jeton.ypos > self.plateau.coords(self.plateau.chevalet)[1] and jeton.xpos > \
                    self.plateau.coords(self.plateau.rectanlge_lac)[0]:  # regarde ceux qui sont dans le changer
                pos_chev_changer.append(jeton.position)
        if len(pos_chevalet) > 0 and len(pos_chev_changer) > 0:
            self.annonce.set(
                'Vous avez des jetons sur le plateau et\nen position dechangement de jeton, une '
                'seul de\nses actions peut etre effectue a la fois.')
            self.plateau.dessiner()
            self.dessiner_chevalet()
        elif len(pos_chevalet) > 0 and len(pos_chev_changer) == 0:
            self.choix_placer_jeton(pos_chevalet, pos_plateau)
        elif len(pos_chevalet) == 0 and len(pos_chev_changer) > 0:
            self.choix_changer_jeton(pos_chev_changer)
        elif len(pos_chevalet) == 0 and len(pos_chev_changer) == 0:
            self.choix_passer_tour()

    def choix_placer_jeton(self, pos_chevalet, pos_plateau):
        # prend liste index chevalet et pos plateau
        if self.plateau.valider_positions_avant_ajout(pos_plateau): # si les position sont valides alors retourne true
            jetons = [self.joueur_actif.retirer_jeton(p) for p in pos_chevalet] #enleve les jetons du chevalet du joueur
            mots, score = self.plateau.placer_mots(jetons, pos_plateau) #place les jetons sur la plateau
            if any([not self.mot_permis(m) for m in mots]):
                for pos in pos_plateau:
                    jeton = self.plateau.retirer_jeton(pos)
                    self.joueur_actif.ajouter_jeton(jeton)
                self.annonce.set('Au moins un des mots est\nabsent du dictionnaire')
                self.plateau.dessiner() #MÀJ plateau
                self.dessiner_chevalet() #MÀJ chevalet
                return
        else:
            self.annonce.set('Au moins un des jetons est\nmal positione')
            return
        self.joueur_actif.ajouter_points(score)
        self.annonce.set('')
        self.changer_joueur = True
        self.prochain_tour()
        for i in range(len(mots)):
            self.text_mot_update(mots[i])

    def mot_permis(self, mot):
        """
        Permet de savoir si un mot est permis dans la partie ou pas en regardant dans le dictionnaire.
        :param mot: str, mot à vérifier.
        :return: bool, True si le mot est dans le dictionnaire, False sinon.
        """
        if mot.upper() in self.dictionnaire:
            return True
        return False

    def determiner_gagnant(self):
        """
        Détermine le joueur gagnant, s'il y en a un. Pour déterminer si un joueur est le gagnant,
        il doit avoir le pointage le plus élevé de tous.
        :return: Joueur, un des joueurs gagnants, i.e si plusieurs sont à égalité on prend un au hasard.
        """

        point_gagnant = -1  # Valeur arbitraire negative initiale pour comparaison
        for joueur in self.joueurs:
            if joueur.points > point_gagnant:  # Si on a un nouveau gagnant
                gagnant = []  # reinitialise la liste
                gagnant.append(joueur)  # stock le joueur gagnant
                point_gagnant = joueur.points  # stock le pointage gagnant
            if joueur.points == point_gagnant:  # gere l'egalite
                gagnant.append(joueur)  # ajoute a la liste des gagant potentiel
        return choice(gagnant)  # retourne un objet aleatoire de la liste des gagnants

    def partie_terminee(self):
        """
        Vérifie si la partie est terminée. Une partie est terminée si il
        n'existe plus de jetons libres ou il reste moins de deux (2) joueurs. C'est la règle que nous avons choisi d'utiliser pour ce travail, donc essayez de
        négliger les autres que vous connaissez ou avez lu sur Internet.
        Returns:
            bool: True si la partie est terminée, et False autrement.
        """
        if len(self.jetons_libres) < 1 or len(self.joueurs) < 2:
            self.titre_top['text'] = "Félicitation à {} qui a remporté la victoire".format(self.determiner_gagnant())
            self.boutton_placer.destroy()
            self.boutton_abandonner.destroy()
            self.plateau.destroy()
            self.liste_label.destroy()
            self.mot_place.destroy()
            self.joueur_actif_label.destroy()
            self.annonce_label.destroy()
            return True
        return False



    def joueur_suivant(self):
        """
        Change le joueur actif.
        Le nouveau joueur actif est celui à l'index du (joueur courant + 1)% nb_joueurs.
        Si on n'a aucun joueur actif, on détermine au harsard le suivant.
        """
        global start_time
        elapsed_time = time() - start_time #calcule le temps écoulé du premier joueur
        if self.joueur_actif is None:
            self.joueur_actif = self.joueurs[randint(0, len(self.joueurs) - 1)]
        else:
            self.joueur_actif.temps_de_jeu += elapsed_time #ajoute le temps écoulé à l'Attribut temps de jeu du joueur
            start_time = time()
            self.joueur_actif = self.joueurs[(self.joueurs.index(self.joueur_actif) + 1) % len(self.joueurs)]

        if self.joueur_actif.nb_a_tirer > 0:
            for jeton in self.tirer_jetons(self.joueur_actif.nb_a_tirer):
                self.joueur_actif.ajouter_jeton(jeton)

        self.dessiner_chevalet()

    def dessiner_chevalet(self):
        self.plateau.delete('lettreChevalet')
        self.plateau.jeton_chevalet = []
        for j, jeton in enumerate(self.joueur_actif.jetons):
            if jeton:
                self.plateau.jeton_chevalet.append(jeton_chev(self, jeton, j, self.nb_pixels_per_case))

    def tirer_jetons(self, n):
        """
        Simule le tirage de n jetons du sac à jetons et renvoie ceux-ci. Il s'agit de prendre au hasard des jetons dans self.jetons_libres et de les retourner.
        Pensez à utiliser la fonction shuffle du module random.
        :param n: le nombre de jetons à tirer.
        :return: Jeton list, la liste des jetons tirés.
        :exception: Levez une exception avec assert si n ne respecte pas la condition 0 <= n <= 7.
        """
        try:
            if n > len(self.jetons_libres):
                n = len(self.jetons_libres)
            pige = []
            shuffle(self.jetons_libres)
            for i in range(0, n):
                pige.append(self.jetons_libres[-1])
                del self.jetons_libres[-1]
                # retire premier item de la liste et l'ajoute a la pige
            return pige
        except:
            raise NombreDeJetonsInvalide ("Impossible de tirer les jetons, le nombre entrée est invalide")

    def highlight_case_chevalet(self, event):
        global drag_id, dragged
        items = self.chevalet.find_withtag(CURRENT)
        if items:
            image = self.itemcget(items[0], 'image')
            dragged = DragToplevel(self, image, event.x_root, event.y_root)
            drag_id = self.bind('<Motion>', lambda e: dragged.move(e.x_root, e.y_root))


    def changer_jetons(self):
        """
        Faire changer au joueur actif ses jetons. La méthode doit demander au joueur de saisir les positions à changer les unes après les autres séparés par un espace.
        Si une position est invalide (utilisez Joueur.position_est_valide) alors redemander.
        Dès que toutes les positions valides les retirer du chevalier du joueur et lui en donner de nouveau.
        Enfin, on remet des jetons pris chez le joueur parmi les jetons libres.
        :return: Ne retourne rien.
        """
        while True:  # boucle d'input
            swap_jeton = str(input('Saisir la position des jetons à changer séparés par un espace: ')).split(' ')
            for pos in swap_jeton:
                if not Joueur.position_est_valide(int(pos) - 1):
                    print('Erreur de saisie, essayez a nouveau')
                    valide = False
                    break
                else:
                    valide = True
            if valide:  # fin de l'iteration avec un valide donc tous ok
                break
        for pos in swap_jeton:
            self.jetons_libres.append(
                self.joueur_actif.retirer_jeton(int(pos) - 1))  # retire jeton et lajoute a la liste des disponibles
        jeton_pigee = self.tirer_jetons(len(swap_jeton))
        for i in range(0, len(jeton_pigee)):
            self.joueur_actif.ajouter_jeton(jeton_pigee[i])
        return


    def sauvegarder_partie(self):
        """ *** Vous n'avez pas à coder cette méthode ***
        Permet de sauvegarder l'objet courant dans le fichier portant le nom spécifié.
        La sauvegarde se fera grâce à la fonction dump du module pickle.
        :return: True si la sauvegarde s'est bien passé, False si une erreur s'est passé durant la sauvegarde.
        """
        filepath = asksaveasfilename(title="Sauvegarder une partie de Supper Scrabble", #permet d'ouvrir une fenetre pour enregistrer la partie
                                     filetypes=[('Super Scrabble Save', '.sss'), ('all files', '.*')])
        filepath += '.sss'
        # if filepath != ".sss":
        try:
            with open(filepath, "wb") as f:
                pickle.dump(
                    [self.joueurs, self.joueur_actif, self.jetons_libres, self.plateau.cases, self.dictionnaire,
                     self.text_mot_place.get()], f) #utilise pickle pour enregistrer les infos nécéssaires dans un fichier texte
                label = Tk()
                label.title("Toutes nos félicitations")
                label.config(padx=20, pady=20)
                b = Button(label, text="OK", command=label.destroy)
                b.grid(row=2, column=0)
                c = Label(label, text="Votre fichier a été sauvegardé avec succès", padx=20, pady=20)
                c.grid(row=0, column=0)

        except:
            label = Tk()
            label.title("Erreur!")
            label.config(padx=20, pady=20)
            b = Button(label, text="OK", command=label.destroy)
            b.grid(row=2, column=0)
            c = Label(label, text="Votre fichier n'a pas pu être sauvegardé", padx=20, pady=20)
            c.grid(row=0, column=0)
    #     return True
    # return False

    # @staticmethod
    def charger_partie(self):
        """ *** Vous n'avez pas à coder cette méthode ***
        Méthode statique permettant de créer un objet scrabble en lisant le fichier dans
        lequel l'objet avait été sauvegardé précédemment. Pensez à utiliser la fonction load du module pickle.
        :return: .
        """
        try:
            filepath = askopenfilename(title="Charger une partie de Supper Scrabble", #ouvre le finder pour sélectionner fichier
                                       filetypes=[('Super Scrabble Save', '.sss'), ('all files', '.*')])
            if filepath != "":
                label = Tk()
                label.title("Toutes nos félicitations")
                label.config(padx=20, pady=20)
                b = Button(label, text="OK", command=label.destroy)
                b.grid(row=2, column=0)
                c = Label(label, text="Votre fichier a été chargé!", padx=20, pady=20)
                c.grid(row=0, column=0)
                with open(filepath, "rb") as f:
                    self.joueurs, self.joueur_actif, self.jetons_libres, cases, self.dictionnaire, text_mot_place = pickle.load(
                        f) #charges les informations pertinentes qui caractérise la partie qui a été enregistrée
                self.changer_joueur = False
                self.fresh_load = True
                self.plateau = Plateau(self, 30, self.fresh_load, cases)
                self.initialiser_jeu()
                self.text_mot_place.set(text_mot_place)
        except:
            master = Tk()
            master.title("Intervention requise!")
            master.config(padx=20, pady=20)
            b = Button(master, text="OK", command=master.destroy)
            b.grid(row=2, column=0)
            c = Label(master, text="Veuillez selectionner un fichier valide", padx=20, pady=20)
            c.grid(row=0, column=0)



if __name__ == '__main__':
    Scrabble().mainloop()