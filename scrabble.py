import pickle
from random import randint, shuffle, seed, choice
from tp3.joueur import Joueur
from tp3.plateau import Plateau, Jeton


class Scrabble:
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
    def __init__(self, nb_joueurs, langue='fr'):
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
        assert langue.upper() in ['FR', 'EN'], 'Langue non supportée.'
        assert 2 <= nb_joueurs <= 4, "Il faut entre 2 et 4 personnes pour jouer."
        self.plateau = Plateau()
        self.joueur_actif = None
        self.joueurs = [Joueur("Joueur {}".format(i+1)) for i in range(nb_joueurs)]
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
        gagnant = None
        point_gagnant = -1
        for joueur in self.joueurs:
            if joueur.points < point_gagnant: # Saute le reste de la loop si point inferieur
                continue
            if joueur.points == point_gagnant:
                if choice([True, False]): #Si egalite, 50% de chance de conserver un ou l'autre
                    continue
            gagnant = joueur #conserve le joueur gagnant
            point_gagnant = joueur.points #conserve le pointage gagnant
        return gagnant

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
            self.joueur_actif = self.joueurs[randint(0, len(self.joueurs) - 1)] # joueur au hasard, sera incr de 1 avant return
        for i in range( 0,len(self.joueurs)):
            if self.joueurs[i].nom == self.joueur_actif.nom: #trouve le bon joueur en comparant son nom
                if i == len(self.joueurs) - 1:  #dernier atteint retourne au depart
                    self.joueur_actif = self.joueurs[0]
                    break
                else:
                    self.joueur_actif = self.joueurs[i + 1] #set le prochain joueur comme etant actif
                    break
        return







    def tirer_jetons(self, n):
        """
        Simule le tirage de n jetons du sac à jetons et renvoie ceux-ci. Il s'agit de prendre au hasard des jetons dans self.jetons_libres et de les retourner.
        Pensez à utiliser la fonction shuffle du module random.
        :param n: le nombre de jetons à tirer.
        :return: Jeton list, la liste des jetons tirés.
        :exception: Levez une exception avec assert si n ne respecte pas la condition 0 <= n <= 7.
        """
        assert 0 <= n <= 7, "Impossible de tirer les jetons, le nombre entrée est invalide"
        #TODO double check if the amount of jeton left is sufficient could add:
        # if n > len(self.jetons_libres) - 1:
        #     n = len(self.jetons_libres) - 1
        pige = []
        shuffle(self.jetons_libres)
        for i in range(0,n):
            pige.append(self.jetons_libres[-1])
            del self.jetons_libres[-1]
            #retire premier item de la liste et l'ajoute a la pige
        return pige


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
            input_pos_chevalet = input("Entrez les positions du chevalet à jouer séparées par un espace: ").upper().strip()
            pos_chevalet = [int(x) - 1 for x in input_pos_chevalet.split(' ')]
            valide = all([Joueur.position_est_valide(pos) for pos in pos_chevalet])

        valide = False
        while not valide:
            input_pos_plateau = input("Entrez les positions de chacune de ces lettres séparées par un espace: ").upper().strip()
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
        print(self.plateau)
        print(self.joueur_actif)
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
        while True: # boucle d'input
            swap_jeton = str(input('Saisir la position des jetons a changer séparés par un espace: ')).split(' ')
            for pos in swap_jeton:
                if not Joueur.position_est_valide(int(pos) - 1):
                    print('Erreur de saisie, essayez a nouveau')
                    valide = False
                    break
                else:
                    valide = True
            if valide: # fin de l'iteration avec un valide donc tous ok
                break
        for pos in swap_jeton:
            self.jetons_libres.append(self.joueur_actif.retirer_jeton(int(pos) - 1)) #retire jeton et lajoute a la liste des disponibles
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
        changer_joueur = True
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

    def sauvegarder_partie(self, nom_fichier):
        """ *** Vous n'avez pas à coder cette méthode ***
        Permet de sauvegarder l'objet courant dans le fichier portant le nom spécifié.
        La sauvegarde se fera grâce à la fonction dump du module pickle.
        :param nom_fichier: Nom du fichier qui contient un objet scrabble.
        :return: True si la sauvegarde s'est bien passé, False si une erreur s'est passé durant la sauvegarde.
        """
        try:
            with open(nom_fichier, "wb") as f:
                pickle.dump(self, f)
        except:
            return False
        return True

    @staticmethod
    def charger_partie(nom_fichier):
        """ *** Vous n'avez pas à coder cette méthode ***
        Méthode statique permettant de créer un objet scrabble en lisant le fichier dans
        lequel l'objet avait été sauvegardé précédemment. Pensez à utiliser la fonction load du module pickle.
        :param nom_fichier: Nom du fichier qui contient un objet scrabble.
        :return: Scrabble, l'objet chargé en mémoire.
        """
        with open(nom_fichier, "rb") as f:
            objet = pickle.load(f)
        return objet

if __name__ == '__main__':
    ##############################################################################################
    # Programme principal. Vous n'avez pas à coder cela. Vous pouvez le changer selon vos besoins,
    # mais remettez votre TP avec la version originale fournie.
    ##############################################################################################
    seed(42) # Pour vous aider à avoir quelque chose de prévisible histoire de faciliter vos tests.
    print("*"*80)
    print("{:^80}".format("Bienvenue dans IFT-1004 Scrabble"))
    print("*"*80)

    choix = ''
    while choix not in ['n', 'o']:
        choix = input("Entrez (n) pour commencer une nouvelle partie \n"
                      "ou (o) pour ouvrir une partie déja existante: ").strip().lower()
    if choix == 'n':
        valide = False
        while not valide:
            try:
                nb_joueurs = int(input("Veuillez entrer le nombre de joueurs (min=2, max=4): "))
                if 2 <= nb_joueurs <= 4:
                    valide = True
            except:
                print("Vous devez entrer un entier.")

        valide = False
        while not valide:
            langue= input("Veuillez sélectionner la langue(français=fr, anglais=en): ")
            if langue in ['en', 'fr']:
                valide = True
            else:
                print("Nous n'avons pas pu détecter la langue.")

        scrabble = Scrabble(nb_joueurs, langue)
        scrabble.jouer()
    else:
        valide = False
        while not valide:
            try:
                fichier = input("Entrez le nom du fichier à ouvrir: ")
                scrabble = Scrabble.charger_partie(fichier)
                valide = True
            except:
                valide = False
        scrabble.jouer()