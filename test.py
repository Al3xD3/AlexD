# replace le layout pour debut parti
self.titre_top.grid(row=0, column=2, columnspan=4, rowspan=1)
self.plateau = Plateau(self, 30)
self.plateau.grid(row=1, column=2, columnspan=4, rowspan=18)
# self.plateau.grid(row=0, column=0, sticky=NSEW)

# init joueur
self.changer_joueur = True
self.joueur_actif = None
# TODO Methode pour nommer nos joueur dynamiquement
self.joueurs = [Joueur("Joueur {}".format(i + 1)) for i in range(nb_joueurs)]

# init score board
self.score_label = Label(self, text="Tableau des Résultats", fg="black", font=("Courier", 12))
self.score_label.grid(row=1, column=0, pady=2, padx=2)
self.text_score_joueur = StringVar()
self.score_joueur = Label(self, textvariable=self.text_score_joueur, fg="black", font=("Courier", 11))
self.score_joueur.grid(row=2, column=0, pady=2, padx=2, rowspan=4)

# Init Liste mot joue
self.liste_label = Label(self, text="Mots Placées", fg="black", font=("Courier", 12))
self.liste_label.grid(row=8, column=0, pady=2, padx=2)
self.text_mot_place = StringVar()
self.text_mot_place.set("")
self.mot_place = Label(self, textvariable=self.text_mot_place, anchor=S, fg="black", font=("Courier", 11))
self.mot_place.grid(row=9, column=0, pady=2, padx=2, rowspan=1)

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
self.sign_label = Label(self, text="Creation Dec 2018", fg="black", font=("Courier", 6))
self.sign_label.grid(row=23, column=6, pady=2, padx=2, columnspan=2)