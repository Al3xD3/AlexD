def coord_case(i, j, nb_pixels_per_case):
    debut_ligne = i * nb_pixels_per_case
    fin_ligne = debut_ligne + nb_pixels_per_case
    debut_colonne = j * nb_pixels_per_case
    fin_colonne = debut_colonne + nb_pixels_per_case
    return debut_ligne, debut_colonne, fin_ligne, fin_colonne

def dessiner_jeton(self, jeton, i, j, nb_pixels_per_case, tag='lettre'):
    d = nb_pixels_per_case//2
    debut_ligne, debut_colonne, fin_ligne, fin_colonne = coord_case(i, j, nb_pixels_per_case)
    self.create_rectangle(debut_colonne, debut_ligne, fin_colonne, fin_ligne, fill='#b9936c', tags=tag)

    self.create_text((debut_colonne + d, debut_ligne + d),
                     font=('Times', '{}'.format(31)), text=str(jeton), tags='lettre')
