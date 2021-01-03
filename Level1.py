import pygame
import sys
import os 
import time
from PyQt5 import QtCore, QtGui, QtWidgets

pygame.init()

#Implémentation des images
mvtDroite = [pygame.image.load('data\\perso\\robotR_1.png'), pygame.image.load('data\\perso\\robotR_2.png'), pygame.image.load('data\\perso\\robotR_3.png'), pygame.image.load('data\\perso\\robotR_4.png'), pygame.image.load('data\\perso\\robotR_5.png'),
            pygame.image.load('data\\perso\\robotR_6.png'), pygame.image.load('data\\perso\\robotR_7.png'), pygame.image.load('data\\perso\\robotR_8.png'), pygame.image.load('data\\perso\\robotR_9.png')]
mvtGauche = [pygame.image.load('data\\perso\\robotL_1.png'), pygame.image.load('data\\perso\\robotL_2.png'), pygame.image.load('data\\perso\\robotL_3.png'), pygame.image.load('data\\perso\\robotL_4.png'), pygame.image.load('data\\perso\\robotL_5.png'),
            pygame.image.load('data\\perso\\robotL_6.png'), pygame.image.load('data\\perso\\robotL_7.png'), pygame.image.load('data\\perso\\robotL_8.png'), pygame.image.load('data\\perso\\robotL_9.png')]
fond = pygame.image.load('data\\interface\\BGferme.png')
fond2 = pygame.image.load('data\\interface\\BGouvert.png')
personnage = pygame.image.load('data\\perso\\standing.png')
personnageBlesse = pygame.image.load('data\\perso\\persoTransparent.png')

GameOver=pygame.image.load('data\\interface\\gameover.png')

police=pygame.font.Font('data\\PressStart2P.ttf', 32) 

scieDessin=pygame.image.load("data\\scie_redim\\Saw.png")

clock = pygame.time.Clock()

run=False

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):      #Initialisation du menu
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 768)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(470, 360, 311, 61))
        font = QtGui.QFont()
        font.setFamily("Press Start 2P")
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setCheckable(False)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setEnabled(True)
        self.pushButton_3.setGeometry(QtCore.QRect(470, 530, 311, 61))
        font = QtGui.QFont()
        font.setFamily("Press Start 2P")
        font.setPointSize(12)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.pushButton_3.setObjectName("pushButton_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 1024, 791))
        self.label.setStyleSheet("background-color: lightgrey;")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(420, -20, 411, 301))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 60, 391, 651))
        self.label_3.setObjectName("label_3")
        self.label.raise_()
        self.pushButton_3.raise_()
        self.pushButton.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

#Signaux qui permettent la fermeture de la fenêtre et le lancement du jeu
        self.pushButton_3.clicked['bool'].connect(MainWindow.close)     
        self.pushButton.clicked['bool'].connect(MainWindow.close)
        self.pushButton.clicked['bool'].connect(Jeu.activer)
        
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "JOUER"))
        self.pushButton_3.setText(_translate("MainWindow", "QUITTER"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><img src=\":/newPrefix/portal2d.png\"/></p></body></html>"))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p><img src=\":/newPrefix/pixelglados2.png\"/></p></body></html>"))
import test_rc




class Joueur(object):
#Initialisation du personnage
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 5
        self.isJumping = False
        self.droite = False
        self.gauche = False
        self.CptPas = 0
        self.jumpCount = 10
        self.standing = True
        self.descente=False
        self.hitbox=pygame.Rect(self.x+7,self.y+11,31,52)
        self.hp=50
        self.blesse=False

#Dessin du personnage
    def dessin(self,win):
        if self.CptPas + 1 >=27:
            self.CptPas = 0

        if self.droite == True and self.blesse==False :
            win.blit(mvtDroite[self.CptPas//3], (self.x,self.y))
            self.CptPas = self.CptPas + 1

        elif self.gauche == True and self.blesse==False:
            win.blit(mvtGauche[self.CptPas//3], (self.x,self.y))
            self.CptPas = self.CptPas +1
    
        elif not self.gauche and not self.droite and not self.blesse : 
            win.blit(personnage, (self.x,self.y))
        self.hitbox=pygame.Rect(self.x+7,self.y+11,31,52)
        #pygame.draw.rect(win, (0,255,0), self.hitbox,2)  Dessin de la hitbox du personnage

#Changement de l'état du personnage s'il est blessé
        if self.blesse :
            win.blit(personnageBlesse,(self.x,self.y))
            son=pygame.mixer.Sound('data\\sons\\damage.wav')
            canal_1=pygame.mixer.Channel(0)
            canal_1.play(son)

#Affichage de la barre de vie du personnage 
    def update_hp_bar(self, win) :
        pygame.draw.rect(win, (0,0,0), [self.x, self.y-10, 50, 10])
        if self.hp>=35:
            pygame.draw.rect(win, (0,210,0), [self.x, self.y-10, self.hp, 10])

        elif self.hp>15:
            pygame.draw.rect(win, (255,165,0), [self.x, self.y-10, self.hp, 10])
        
        elif self.hp<=15:
            pygame.draw.rect(win, (210,0,0), [self.x, self.y-10, self.hp, 10])

#Réduction des points de vie du personnage s'il se blesse
    def damage(self,amount) :
        self.hp -= amount
      
class Boite(object):
#Initialisation de la boite
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox=pygame.Rect(self.x,self.y,self.width,self.height)

    #def dessin(self,win):
    #        pygame.draw.rect(win, (0,0,255), self.hitbox,2) # Dessin de la hitbox de la boite         


class Jeu():
#Fonction qui permet de lancer le jeu depuis les boutons du menu
    def activer():
        global run
        run = True

        #Initialisation de la fenêtre
        global win
        win = pygame.display.set_mode((1024,768))
        pygame.display.set_caption("Projet S2")
        Jeu.loop()   

#Fonction qui permet d'afficher un écran noir progressivement 
    def fade(width, height): 
        fade = pygame.Surface((width, height))
        fade.fill((0,0,0))
        for alpha in range(0, 300):
            fade.set_alpha(alpha)
            win.blit(fade, (0,0))
            pygame.display.update()
            pygame.time.delay(5)

#Boucle principale
    def loop():
#Initialisation des éléments
        pygame.mixer.music.load('data\\sons\\fond.wav')
        pygame.mixer.music.play(10,0.0)
        pygame.mixer.music.set_volume(0.1)
        pygame.mouse.set_visible(False)
        canal_3=pygame.mixer.Channel(2)
        sonScie=pygame.mixer.Sound('data\\sons\\son_hache.wav')
        canal_3.play(sonScie, loops=-1)
        canal_3.set_volume(0.1)
        perso = Joueur(50, 574, 48, 64)
        boite1 = Boite(926, 479, 92, 79)
        boite2 = Boite(834, 558, 92, 79)
        sol1 = pygame.Rect(0,638,1024,141)
        sol2 = pygame.Rect(0,329,895,65)
        pics1 = pygame.Rect(462,608,66,29)
        pics2 = pygame.Rect(315,305,66,29)
        pics3 = pygame.Rect(591,305,66,29)
        scie = pygame.Rect(199,581,50,50)
        interrupteur=pygame.Rect(148,253,21,77)
        porteFin=pygame.Rect(45,226,63,104)
        porteOuverte=False
        finNiveau=False
        gameOver=False

        global run
        while run :
            clock.tick(27)   #fréquence de rafraichissement / nombre de fps

#Boucle qui capte toutes les entrées du clavier
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            keys = pygame.key.get_pressed()

#Partie basse de la carte
            if perso.y+perso.height>=sol2[1]+sol2[3]:                
                if perso.hitbox.colliderect(scie) and perso.x+ perso.width<=220:
                        perso.x-= 10
                        perso.blesse=True
                        perso.damage(1)

                elif perso.hitbox.colliderect(scie) and perso.x+ perso.width>220 and perso.x<230 :
                    perso.y=scie[1]-2-perso.height
                    perso.y-=25
                    perso.descente=True
                    perso.blesse=True
                    perso.damage(1)
                
                elif perso.hitbox.colliderect(scie) and perso.x>=230 :
                    perso.x+=10
                    perso.blesse=True
                    perso.damage(1)


                elif perso.hitbox.colliderect(pics1):
                    perso.y=perso.y-15
                    perso.descente=True
                    perso.blesse=True
                    perso.damage(1)
                
                else :
                    perso.blesse=False

                if (perso.hitbox).colliderect(boite2.hitbox) and not perso.isJumping:
                    perso.x=boite2.x-perso.width+13

                if (perso.hitbox).colliderect(boite1.hitbox) and not perso.isJumping:
                    perso.x=boite1.x-perso.width+17

                if (perso.hitbox).colliderect(sol1) and perso.blesse==False:
                    perso.y=sol1[1]-perso.height

                if perso.x < boite2.x + boite2.width and  perso.x +perso.width > boite2.x:
                        if perso.y < boite2.y+boite2.height:
                            if ((perso.x+perso.width-perso.velocity-2) < boite2.x+7) and (perso.y+perso.height< sol1[1]) :
                                perso.descente=True
                            else: 
                                perso.descente=False

                if not perso.hitbox.colliderect(boite1.hitbox) and perso.x+perso.width>boite2.x and perso.x+perso.width <boite1.x:
                    if perso.y < boite1.y+14:
                        perso.descente=True

                if perso.x < boite1.x + boite1.width and  perso.x +perso.width > boite1.x-10:
                        if perso.y < boite1.y+boite1.height:
                            if ((perso.x+perso.width-perso.velocity) < boite1.x+25) and (perso.y+perso.height< boite2.y) or ((perso.y+perso.height<boite1.y) and perso.isJumping==False):
                                perso.descente=True                            
                            else:
                                perso.descente=False


                if perso.descente and perso.y+perso.width!=sol1[1]:
                    perso.y+=5    

                if (perso.hitbox).colliderect(boite2.hitbox) and (perso.isJumping) and (perso.y < boite2.y) and perso.x < boite2.x+boite2.width and perso.x > boite2.x:
                    perso.y=boite2.y-perso.height

                if (perso.hitbox).colliderect(boite1.hitbox) and (perso.isJumping) and (perso.y < boite1.y) and perso.x < boite1.x+boite1.width and perso.x > boite1.x:
                    perso.y=boite1.y-perso.height

                if perso.y+perso.height-1>=sol2.bottom:
                    if perso.y+perso.width<boite1.y:
                        perso.descente=True

#Partie haute de la carte
            else :
                if perso.x+perso.width+perso.velocity+2 > sol2[2] and perso.x+perso.width<1024:
                    if perso.y+perso.height< boite1.y and perso.y+perso.height>= sol2.y:
                        perso.descente=True
                    else :
                        perso.descente=False

                if (perso.hitbox).colliderect(sol2):
                    perso.y=sol2[1]-perso.height

                if perso.descente and perso.y+perso.height!=sol1[1]:
                    perso.y+=5 

                if perso.hitbox.colliderect(pics2):
                    perso.y-=15
                    perso.descente=True
                    perso.blesse=True
                    perso.damage(1)

                elif perso.hitbox.colliderect(pics3):
                    perso.y-=15
                    perso.descente=True
                    perso.blesse=True
                    perso.damage(1)

                else : 
                    perso.blesse=False

#Ouverture de la porte et lancement du niveau suivant
                if perso.hitbox.colliderect(interrupteur) and porteOuverte==False:
                    if keys[pygame.K_e]:
                        porteOuverte=True
                        porteSon=pygame.mixer.Sound('data\\sons\\porte.wav')
                        switch=pygame.mixer.Sound('data\\sons\\switch.wav')
                        canal_2=pygame.mixer.Channel(1)
                        canal_2.play(switch)
                        canal_3=pygame.mixer.Channel(2)
                        canal_3.play(porteSon)

                if perso.hitbox.colliderect(porteFin) and porteOuverte:
                    if keys[pygame.K_e]:
                        Jeu.fade(1024,768)
                        finNiveau=True
                        os.system('start "Niveau 2" /min ".\Level2.py"')
                        sys.exit()                        

#Déplacement du personnage             
            if keys[pygame.K_a] and perso.x > perso.velocity: #K_a parce que pygame est en QWERTY sur Windows
                perso.x = perso.x - perso.velocity
                perso.gauche = True
                perso.droite = False

            elif keys[pygame.K_d] and perso.x <= 1024 - perso.width - perso.velocity: 
                perso.x = perso.x + perso.velocity
                perso.gauche = False
                perso.droite = True
        
            
            else :
                perso.gauche = False
                perso.droite = False
                perso.CptPas = 0


#Mécanique pour le saut
            if not(perso.isJumping):
                if keys[pygame.K_SPACE]:
                    perso.isJumping = True
                    perso.droite = False
                    perso.gauche = False 
                    perso.CptPas = 0

            else:
                if perso.jumpCount >= -10:
                    perso.y -= int((perso.jumpCount * abs(perso.jumpCount)) * 0.5)
                    perso.jumpCount -= 1
                else: 
                    perso.jumpCount = 10
                    perso.isJumping = False

            if keys[pygame.K_ESCAPE]:
                sys.exit()


#Affichage de l'image du niveau de base
            if porteOuverte==False and gameOver==False:
                win.blit(fond, (0,0))

#Affichage de l'image du niveau quand le joueur a utilisé l'interrupteur
            if porteOuverte and gameOver==False:
                win.blit(fond2,(0,0))


#Outils pour le débuggage
            
            pygame.draw.rect(win, (0,255,0), sol1,2) # To draw the hit box around the player
            pygame.draw.rect(win, (0,255,0), boite1.hitbox,2) # To draw the hit box around the player
            pygame.draw.rect(win, (0,175,175), sol2,2) # To draw the hit box around the player
            pygame.draw.rect(win, (0,175,175), interrupteur,2) # To draw the hit box around the player
            pygame.draw.rect(win, (0,175,175), porteFin,2) # To draw the hit box around the player
            pygame.draw.rect(win, (0,175,175), scie,2) # To draw the hit box around the player
            pygame.draw.rect(win, (0,175,175), pics2,2) # To draw the hit box around the player
            pygame.draw.rect(win, (0,175,175), pics3,2) # To draw the hit box around the player
                       

#Gestion du Game Over et affichage à l'écran           
            if finNiveau==False and gameOver==False:
                perso.dessin(win)

                if perso.hp <=0 and gameOver==False:
                    Jeu.fade(1024,768)
                    gameOver=True

                    
                win.blit(scieDessin, (200,580))
                
                perso.dessin(win)

                perso.update_hp_bar(win)


                pygame.display.update()

#Activation du Game Over
            elif finNiveau==False and gameOver:
                    pygame.mixer.stop()
                    pygame.mixer.music.stop()

                    if keys[pygame.K_RETURN]:
                        gameOver=False
                        Jeu.loop()
                    win.fill((0,0,0))                     
                    win.blit(GameOver,(267.5,0))
                    
                    text = police.render('PRESS ENTER TO PLAY AGAIN', True, (255,255,255)) 
                    textRect = text.get_rect() 
                    win.blit(text, (textRect[0]+135,textRect[1]+450)) 
                    pygame.display.update()  
                
            elif finNiveau==True:
                run=False

            
#Commandes pour lancer et afficher les fenêtres
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec_())

pygame.QUIT