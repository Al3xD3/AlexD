def coord_case(i, j, nb_pixels_per_case):
    debut_ligne = i * nb_pixels_per_case + 2
    fin_ligne = debut_ligne + nb_pixels_per_case + 2
    debut_colonne = j * nb_pixels_per_case + 2
    fin_colonne = debut_colonne + nb_pixels_per_case + 2
    return debut_ligne, debut_colonne, fin_ligne, fin_colonne


def dessiner_jeton(self,jeton, i, j, nb_pixels_per_case, tag='lettre'):
    d = nb_pixels_per_case//2
    debut_ligne, debut_colonne, fin_ligne, fin_colonne = coord_case(i, j, nb_pixels_per_case)
    self.create_rectangle(debut_colonne, debut_ligne, fin_colonne, fin_ligne, fill='#b9936c', tags=tag)

    self.create_text((debut_colonne + d, debut_ligne + d), font=('Times', '{}'.format(31)), text=str(jeton), tags='lettre')

class jeton_chev(object):
    def __init__(self, canvas, jeton, number, size):
        if number == 0:
            canvas.plateau.delete('lettreChevalet')
        self.canvas = canvas.plateau
        poschevalet = self.canvas.coords(self.canvas.chevalet)
        offsetH = (size/2) // 2
        debut_x = poschevalet[0] + (size/2) * (number * 1.5 + 0.5)
        debut_y = poschevalet[1] + offsetH
        fin_x = debut_x + (size/2)
        fin_y = debut_y + (size/2)
        self.border = self.canvas.create_rectangle(debut_x, debut_y, fin_x, fin_y, fill='#b9936c', tags='lettreChevalet')
        self.texte = self.canvas.create_text((debut_x + offsetH, debut_y + offsetH), font=('Times', '{}'.format(int((size/2) - 14))), text=str(jeton), tags='lettreChevalet')
        self.xpos = debut_x
        self.ypos = debut_y
        self.canvas.tag_bind(self.texte, '<Button1-Motion>', self.move)
        self.canvas.tag_bind(self.texte, '<ButtonRelease-1>', self.release)
        self.move_flag = False
        self.position = number
        self.size = size
        #debug
        self.nom = str(jeton)




    def move(self, event):
        if self.move_flag:
            new_xpos, new_ypos = event.x, event.y
            if new_xpos > 5 and new_xpos < self.size//2 * 15 and new_ypos > 5 and new_ypos < self.size//2 * 18: #reste dans canvas
                self.canvas.move(self.border, new_xpos - self.mouse_xpos, new_ypos - self.mouse_ypos)
                self.canvas.move(self.texte, new_xpos - self.mouse_xpos, new_ypos - self.mouse_ypos)
                self.mouse_xpos = new_xpos
                self.mouse_ypos = new_ypos
        else:
            self.move_flag = True
            self.canvas.tag_raise(self.border)
            self.canvas.tag_raise(self.texte)
            self.mouse_xpos = event.x
            self.mouse_ypos = event.y

    def release(self, event):
        self.move_flag = False
        self.xpos = event.x
        self.ypos = event.y





