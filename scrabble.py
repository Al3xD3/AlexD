import pickle
from random import randint, shuffle, seed, choice
from Joueur import Joueur
from plateau import Plateau, Jeton
from tkinter import *
from tkinter import messagebox
from utils import jeton_chev


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
        #param du GUI
        #w = 600  # width for the Tk
        #h = 650  # height for the Tk main
        #ws = self.winfo_screenwidth()  # width of the screen
        #hs = self.winfo_screenheight()  # height of the screen
        #x = (ws / 2) - (w / 2)
        #y = (hs / 2) - (h / 2)
        #self.geometry('%dx%d+%d+%d' % (w, h, x, y))

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
        column=7,pady=2, padx=2)
        self.nb_pixels_per_case = 60

        # Bouton explication du jeu
        self.voir_instruction = Button(self, text = "Lire instruction", command=self.lire_instruction, width=20).grid(row=3, column=7, pady=2, padx=2)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.plateau = Plateau(self, self.nb_pixels_per_case)
        canvas1 = self.plateau
        #self.plateau.grid(row=0, column=0, sticky=NSEW)

        self.chevalet = Canvas(self, height=self.nb_pixels_per_case,
                                      width=7*self.nb_pixels_per_case, bg='#645b4b')
        self.chevalet.bind("<Button-1>", self.highlight_case_chevalet)
        #self.chevalet.grid(sticky=S)

    def nouveau_pop(self):
        #fenetre de choix nouvelle partie
        self.new = Toplevel(self)
        self.new.wm_title('Nouvelle partie')
        w = 300  # width for the Tk
        h = 180  # height for the Tk main
        ws = self.winfo_screenwidth()  # width of the screen
        hs = self.winfo_screenheight()  # height of the screen
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.new.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.langue = IntVar()
        Label(self.new, text="Langue de jeux?", justify=CENTER, padx=20).grid(row=0, column=0)
        for i in range(len(self.langue_possible)):
            Radiobutton(self.new, text=self.langue_possible[i][0], padx=20, variable=self.langue, value=i).grid(
                row=1 + i, column=0)
        self.nbre_joueur = IntVar()
        Label(self.new, text="Nombre de joueur?", justify=CENTER, padx=20).grid(row=0, column=1)
        for i in range(2, 5):
            Radiobutton(self.new, text=str(i) + " joueurs", padx=20, variable=self.nbre_joueur, value=i).grid(row=i - 1,
                                                                                                              column=1)
        Button(self.new, text="Commencer", command=self.nouvelle_partie).grid(column=0, columnspan=2, pady=10)


    def lire_instruction(self):
        #fenetre de choix instruction
        self.new = Toplevel(self)
        self.new.wm_title("Instruction", )


    def nouvelle_partie(self):
        """Initie les parametres d'une nouvelle partie
        :param None
        Interface servant a entre le nombre de joueur et la langue utilise
                :return int nbr joueur
        :return str langue FR ou EN
        :exception: Levez une exception avec assert si la langue n'est ni fr, FR, en, ou EN ou si nb_joueur < 2 ou > 4.
        """

        self.initialiser_jeu(self.nbre_joueur.get(), self.langue_possible[self.langue.get()][1])
        self.new.destroy()
        # TODO Que doit ton reseter?

    def close(self):
        self.destroy()

    def score_board_update(self):
        txt = ""
        for joueur in self.joueurs:
            txt += '{} :  {} points\n'.format(joueur.nom, joueur.points)
            self.text_score_joueur.set(txt)

    def joueur_actif_update(self):
        txt = "Au tour de: {}".format(self.joueur_actif.nom)
        self.text_joueur_actif.set(txt)


    def initialiser_jeu(self, nb_joueurs, langue='fr'):
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
        self.start_new = Button(self, text="Sauvegarder Partie", command=self.sauvegarder_partie, width=30).grid(row=2,column=7,pady=2,padx=2)
        # TODO test function sauvegarde

        # replace le layout pour debut parti
        self.titre_top.grid(row=0, column=2, columnspan=4, rowspan=1)
        self.plateau = Plateau(self, 30)
        self.plateau.grid(row=1, column=2, columnspan=4, rowspan=18)
        #self.plateau.grid(row=0, column=0, sticky=NSEW)

        # init joueur
        self.changer_joueur = True
        self.joueur_actif = None
        # TODO Methode pour nommer nos joueur dynamiquement
        self.joueurs = [Joueur("Joueur {}".format(i + 1)) for i in range(nb_joueurs)]

        # init score board
        self.score_label = Label(self, text="Tableau des Résultats", fg="black", font=("Courier", 12)).grid(row=1, column=0, pady=2, padx=2)
        self.text_score_joueur = StringVar()
        self.score_joueur = Label(self, textvariable=self.text_score_joueur, fg="black", font=("Courier", 11)).grid( row=2, column=0, pady=2, padx=2, rowspan=4)

        # portion joueur
        self.text_joueur_actif = StringVar()
        self.joueur_actif_label = Label(self, textvariable=self.text_joueur_actif, fg="black", font=("Courier", 12)).grid(row=20, column=3, columnspan=2, pady=2, padx=2)
        self.annonce = StringVar()
        self.annonce_label = Label(self, textvariable=self.annonce, fg="black", font=("Courier", 12)).grid(row=21, column=3, columnspan=2, pady=2, padx=2)

        self.boutton_pass = Button(self, text="Passer", command=self.choix_passer_tour).grid(row=22, column=2)
        self.boutton_changer = Button(self, text="Changer Jeton", command=self.choix_changer_jeton).grid(row=22,
                                                                                                         column=3)
        self.boutton_placer = Button(self, text="Placer Jeton", command=self.choix_placer_jeton).grid(row=22, column=5)
        self.boutton_abandonner = Button(self, text="Abandonner", command=self.choix_abandonner).grid(row=22, column=4)

        # signature
        self.score_label = Label(self, text="Creation Dec 2018", fg="black", font=("Courier", 6)).grid(row=23, column=6,
                                                                                                       pady=2, padx=2,
                                                                                                       columnspan=2)

        # init langue
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
            self.debut_jeux()

    # -------------------------------------  Fin d<init jeux ----------------------------------------

    def debut_jeux(self):
        if self.joueur_actif == None:
            self.joueur_suivant()
        for jeton in self.tirer_jetons(self.joueur_actif.nb_a_tirer):
            self.joueur_actif.ajouter_jeton(jeton)
        self.update_board()

    def prochain_tour(self):
        #efface jeton du jouer d,avant
        self.plateau.dessiner()
        # Verif si fin de parti
        if self.partie_terminee():
            print("partie terminer... TODO implement display \n gagnant : {}".format(self.determiner_gagnant()))
            self.determiner_gagnant()
        if self.changer_joueur:
            self.joueur_suivant()
        for jeton in self.tirer_jetons(self.joueur_actif.nb_a_tirer):
            self.joueur_actif.ajouter_jeton(jeton)
        self.update_board()

    def update_board(self):
        self.joueur_actif_update()
        self.score_board_update()

    def choix_passer_tour(self):
        print("PASSER TOUR!")
        self.changer_joueur = True
        self.prochain_tour()

    def choix_abandonner(self):
        quitter = self.joueur_actif
        self.joueur_suivant()
        self.joueurs.remove(quitter)
        self.changer_joueur = False
        self.prochain_tour()

    def choix_changer_jeton(self):
        self.changer_joueur = True
        return
        # TODO quoi faire lorsque change jeton

    def choix_placer_jeton(self):
        pos_chevalet = []
        pos_plateau = []
        offset = self.nb_pixels_per_case //2 #pour pointer a partir du centre du jeton
        for jeton in self.plateau.jeton_chevalet:
            if jeton.ypos < self.plateau.coords(self.plateau.chevalet)[1]:   #regarde ceux qui ne sont plus dans le chevalet
                pos_chevalet.append(jeton.position)
                pos_plateau.append((jeton.xpos + offset,jeton.ypos + offset))

        valide = False
        while not valide:
            jetons = [self.joueur_actif.retirer_jeton(p) for p in pos_chevalet]
            mots, score = self.plateau.placer_mots(jetons, pos_plateau)
            if any([not self.mot_permis(m) for m in mots]):
                for pos in pos_plateau:
                    jeton = self.plateau.retirer_jeton(pos)
                    self.joueur_actif.ajouter_jeton(jeton)
                    self.annonce.set('Au moins un des mots est absent du dictionnaire')
                    self.plateau.dessiner()
                    self.dessiner_chevalet()
                    #TODO replacer L,ensemble des jeton dans le chevalet, pas juste le dernier
                    return
                valide = False
            else:
                print("Mots formés:", mots)
                print("Score obtenu:", score)
                self.joueur_actif.ajouter_points(score)
                valide = True
        self.changer_joueur = True
        self.prochain_tour()


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
            return True
        return False

    def joueur_suivant(self):
        """
        Change le joueur actif.
        Le nouveau joueur actif est celui à l'index du (joueur courant + 1)% nb_joueurs.
        Si on n'a aucun joueur actif, on détermine au harsard le suivant.
        """
        if self.joueur_actif is None:
            self.joueur_actif = self.joueurs[randint(0, len(self.joueurs) - 1)]
        else:
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
                self.plateau.jeton_chevalet.append(jeton_chev(self,jeton, j, self.nb_pixels_per_case))


        #TODO Implement un fall back si mot nn accepte


    def tirer_jetons(self, n):
        """
        Simule le tirage de n jetons du sac à jetons et renvoie ceux-ci. Il s'agit de prendre au hasard des jetons dans self.jetons_libres et de les retourner.
        Pensez à utiliser la fonction shuffle du module random.
        :param n: le nombre de jetons à tirer.
        :return: Jeton list, la liste des jetons tirés.
        :exception: Levez une exception avec assert si n ne respecte pas la condition 0 <= n <= 7.
        """
        assert 0 <= n <= 7, "Impossible de tirer les jetons, le nombre entrée est invalide"
        # double check if the amount of jeton left is sufficient
        if n > len(self.jetons_libres):
            n = len(self.jetons_libres)
        pige = []
        shuffle(self.jetons_libres)
        for i in range(0, n):
            pige.append(self.jetons_libres[-1])
            del self.jetons_libres[-1]
            # retire premier item de la liste et l'ajoute a la pige
        return pige

    def highlight_case_chevalet(self, event):
        global drag_id, dragged
        items = self.chevalet.find_withtag(CURRENT)
        if items:
            image = self.itemcget(items[0], 'image')
            dragged = DragToplevel(self, image, event.x_root, event.y_root)
            drag_id = self.bind('<Motion>', lambda e: dragged.move(e.x_root, e.y_root))
        # if self.chevalet.find_withtag(CURRENT):
        #     self.chevalet.itemconfig(CURRENT, fill="blue")

#TODO DELETE unused tp3
    def demander_positions(self):
        """ *** Vous n'avez pas à coder cette méthode ***
        Demande à l'utilisateur d'entrer les positions sur le chevalet et le plateau
        pour jouer son coup.
        Si les positions entrées sont valides, on retourne les listes de ces positions. On doit
        redemander tant que l'utilisateur ne donne pas des positions valides.
        Valide ici veut dire uniquement dans les limites donc pensez à utilisez valider_positions_avant_ajout et Joueur.position_est_valide.
        :return: tuple (int list, str list): Deux listes, la première contient les positions du chevalet (plus précisement il s'agit des indexes de ces positions) et l'autre liste contient les positions codées du plateau.
        """
        valide = False
        while not valide:
            pos_chevalet = []
            for id in range(Joueur.TAILLE_CHEVALET):
                if self.chevalet.itemcget(id, "fill") == "blue":
                    pos_chevalet.append(id)
            print(pos_chevalet)
            #input_pos_chevalet = [int(x) for x in range(7) if self.chevalet[x]["fill"] == "blue"]
            #pos_chevalet = [int(x) for x in input_pos_chevalet.split(' ')]
            valide = all([Joueur.position_est_valide(pos) for pos in pos_chevalet])

        valide = False
        while not valide:
            input_pos_plateau = input(
                "Entrez les positions de chacune de ces lettres séparées par un espace: ").upper().strip()
            pos_plateau = input_pos_plateau.split(' ')

            if len(pos_chevalet) != len(pos_plateau):
                print("Les nombres de jetons et de positions ne sont pas les mêmes.")
                valide = False
            else:
                valide = self.plateau.valider_positions_avant_ajout(pos_plateau)

        return pos_chevalet, pos_plateau

    def jouer_un_tour(self):
        """ *** Vous n'avez pas à coder cette méthode ***
        Faire jouer à un des joueurs son tour entier jusqu'à ce qu'il place un mot valide sur le
        plateau.
        Pour ce faire
        1 - Afficher le plateau puis le joueur;
        2 - Demander les positions à jouer;
        3 - Retirer les jetons du chevalet;
        4 - Valider si les positions sont valides pour un ajout sur le plateau;
        5 - Si oui, placer les jetons sur le plateau, sinon retourner en 1;
        6 - Si tous les mots formés sont dans le dictionnaire, alors ajouter les points au joueur actif;
        7 - Sinon retirer les jetons du plateau et les remettre sur le chevalet du joueur, puis repartir en 1;
        8 - Afficher le plateau.
        :return: Ne retourne rien.
        """
        valide = False
        while not valide:
            pos_chevalet, pos_plateau = self.demander_positions()
            jetons = [self.joueur_actif.retirer_jeton(p) for p in pos_chevalet]

            mots, score = self.plateau.placer_mots(jetons, pos_plateau)
            if any([not self.mot_permis(m) for m in mots]):
                print("Au moins l'un des mots formés est absent du dictionnaire.")
                for pos in pos_plateau:
                    jeton = self.plateau.retirer_jeton(pos)
                    self.joueur_actif.ajouter_jeton(jeton)
                valide = False
            else:
                print("Mots formés:", mots)
                print("Score obtenu:", score)
                self.joueur_actif.ajouter_points(score)
                valide = True

        print(self.plateau)

    def changer_jetons(self):
        """
        Faire changer au joueur actif ses jetons. La méthode doit demander au joueur de saisir les positions à changer les unes après les autres séparés par un espace.
        Si une position est invalide (utilisez Joueur.position_est_valide) alors redemander.
        Dès que toutes les positions valides les retirer du chevalier du joueur et lui en donner de nouveau.
        Enfin, on remet des jetons pris chez le joueur parmi les jetons libres.
        :return: Ne retourne rien.
        """
        while True:  # boucle d'input
            swap_jeton = str(input('Saisir la position des jetons a changer séparés par un espace: ')).split(' ')
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

    def jouer(self):
        """
        Cette fonction permet de jouer la partie.
        Tant que la partie n'est pas terminée, on joue un tour.
        À chaque tour :
            - On change le joueur actif et on lui affiche que c'est son tour. ex: Tour du joueur 2.
            - On lui affiche ses options pour qu'il choisisse quoi faire:
                "Entrez (j) pour jouer, (p) pour passer votre tour, (c) pour changer certains jetons,
                (s) pour sauvegarder ou (q) pour quitter"
            Notez que si le joueur fait juste sauvegarder on ne doit pas passer au joueur suivant mais dans tous les autres cas on doit passer au joueur suivant. S'il quitte la partie on l'enlève de la liste des joueurs.
        Une fois la partie terminée, on félicite le joueur gagnant!

        :return Ne retourne rien.
        """
        abandon = False
        changer_joueur = False
        while not self.partie_terminee() and not abandon:
            debut = self.joueur_actif is None
            if changer_joueur:
                self.joueur_suivant()
            if debut:
                print("Le premier joueur sera: {}.".format(self.joueur_actif.nom))

            for jeton in self.tirer_jetons(self.joueur_actif.nb_a_tirer):
                self.joueur_actif.ajouter_jeton(jeton)

            print("Tour du {}.".format(self.joueur_actif.nom))
            choix = input("Entrez (j) pour jouer, (p) pour passer votre tour,\n"
                          "(c) pour changer certains jetons, (s) pour sauvegarder\n"
                          "ou (q) pour quitter: ").strip().lower()
            if choix == "j":
                self.jouer_un_tour()
                changer_joueur = True
            elif choix == "p":
                changer_joueur = True
            elif choix == "c":
                self.changer_jetons()
                changer_joueur = True
            elif choix == "q":
                quitter = self.joueur_actif
                self.joueur_suivant()
                self.joueurs.remove(quitter)
                changer_joueur = False
            elif choix == "s":
                valide = False
                while not valide:
                    nom_fichier = input("Nom du fichier de sauvegarde: ")
                    valide = self.sauvegarder_partie(nom_fichier)
                changer_joueur = False
            else:
                raise Exception("Choix invalide.")

        if self.partie_terminee():
            print("Partie terminée.")
            print("{} est le gagnant.".format(self.determiner_gagnant().nom))

    def sauvegarder_partie(self):
        """ *** Vous n'avez pas à coder cette méthode ***
        Permet de sauvegarder l'objet courant dans le fichier portant le nom spécifié.
        La sauvegarde se fera grâce à la fonction dump du module pickle.
        :return: True si la sauvegarde s'est bien passé, False si une erreur s'est passé durant la sauvegarde.
        """
        # TODO methode pour avoir un input du fichier
        try:
            with open(nom_fichier, "wb") as f:
                pickle.dump(self, f)
        except:
            return False
        return True

    @staticmethod
    def charger_partie():
        """ *** Vous n'avez pas à coder cette méthode ***
        Méthode statique permettant de créer un objet scrabble en lisant le fichier dans
        lequel l'objet avait été sauvegardé précédemment. Pensez à utiliser la fonction load du module pickle.
        :return: Scrabble, l'objet chargé en mémoire.
        """
        # TODO methode pour avoir un input du fichier
        with open(nom_fichier, "rb") as f:
            objet = pickle.load(f)
        return objet


if __name__ == '__main__':
    Scrabble().mainloop()
