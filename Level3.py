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
fond = pygame.image.load('data\\interface\\MAP3.png')
fond2 = pygame.image.load('data\\interface\\MAP3ouverte.png')
personnage = pygame.image.load('data\\perso\\standing.png')
personnageBlesse = pygame.image.load('data\\perso\\persoTransparent.png')

GameOver=pygame.image.load('data\\interface\\gameover.png')

police=pygame.font.Font('data\\PressStart2P.ttf', 32) 

scieDessin=pygame.image.load("data\\scie_redim\\Saw.png")

victoire=pygame.image.load("data\\interface\\victory.png")

clock = pygame.time.Clock()

run=True        #run est à True car il n'a plus besoin d'être lancé de l'extérieur
win=None

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
        self.hitbox=pygame.Rect(self.x+9,self.y+14,31,50)
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

        self.hitbox=pygame.Rect(self.x+9,self.y+14,31,50)
        #pygame.draw.rect(win, (0,255,0), self.hitbox,2) # Dessin de la hitbox du personnage

#Changement de l'état du personnage s'il est blessé  
        if self.blesse :
            win.blit(personnageBlesse,(self.x,self.y))
            son=pygame.mixer.Sound('data\\sons\\damage.wav')
            canal_1=pygame.mixer.Channel(0)
            canal_1.play(son)

#Affichage de la barre de vie du personnage 
    def update_hp_bar(self, win):
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


class Jeu():
#Initialisation de la fenêtre
    global win
    win = pygame.display.set_mode((1024,768))
    pygame.display.set_caption("Projet S2")

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
        perso = Joueur(40, 604, 48, 64)
        boite1 = pygame.Rect(526, 280, 131, 390)
        sol1 = pygame.Rect(0,668,1024,100)
        sol2 = pygame.Rect(0,473,262,26)
        sol3 = pygame.Rect(264,279,262,27)
        sol4 = pygame.Rect(787,168,238,27)
        toit = pygame.Rect(0,0,1024,86)
        pics1 = pygame.Rect(435,265,51,14)
        scie = pygame.Rect(284,646,69,34)
        sonScie=pygame.mixer.Sound('data\\sons\\son_hache.wav')
        canal_3=pygame.mixer.Channel(2)
        canal_3.play(sonScie, loops=-1)
        canal_3.set_volume(0.1)
        acide=pygame.Rect(659,306,369,364)
        interrupteur=pygame.Rect(912,120,19,50)
        porteFin=pygame.Rect(981,92,41,77)
        porteOuverte=False
        finNiveau=False
        portailB1 = pygame.Rect(480,605,50,70)
        portailO1 = pygame.Rect(1,422,50,70)
        portailB2 = pygame.Rect(225,420,50,70)
        portailO2 = pygame.Rect(285,220,50,70)
        portailB3 = pygame.Rect(620,220,70,50)
        portailO3 = pygame.Rect(800,100,50,80)
        canal_4=pygame.mixer.Channel(3)
        sonPortail=pygame.mixer.Sound('data\\sons\\son_portail.wav')
        canal_4.set_volume(0.3)
        gameOver=False

        global run
        while run == True:
            clock.tick(27)   #fréquence de rafraichissement / nombre de fps

#Boucle qui capte toutes les entrées du clavier
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                
            keys = pygame.key.get_pressed()
            
            if perso.y+perso.height>=sol2.bottom + 20:

#Partie la plus basse de la carte  
                if (perso.hitbox).colliderect(sol1):
                    perso.y=sol1[1]-perso.height-3

                if (perso.hitbox).colliderect(boite1):
                    perso.x=boite1[0]-perso.width-3
                
                if perso.hitbox.colliderect(scie) and perso.hitbox[0]+ perso.hitbox[2]<=290:
                        perso.x-= 10
                        perso.blesse=True
                        perso.damage(1)

                elif perso.hitbox.colliderect(scie) and perso.hitbox[0]+perso.hitbox[2]>290 and perso.hitbox[0]+perso.hitbox[2]<350 :
                    perso.y=scie[1]-4-perso.height
                    perso.y-=25
                    perso.descente=True
                    perso.blesse=True
                    perso.damage(1)
                
                elif perso.hitbox.colliderect(scie) and perso.hitbox[0]>=345 :
                    perso.x+=10
                    perso.blesse=True   
                    perso.damage(1)
             
                else :
                    perso.blesse=False

                if perso.hitbox[0]>=portailB1[0] and perso.hitbox[0]+perso.hitbox[2]<=portailB1[0]+portailB1[2]:
                    if perso.hitbox[1] >=portailB1[1]:
                        perso.x=portailO2[0]+10
                        perso.y=portailO2[1]+1
                        canal_4.play(sonPortail)

                
                if perso.descente and perso.y+perso.width!=sol1[1]:
                    perso.y+=5  
                    

#Partie intermédiaire de la carte   
            elif perso.y+perso.height>sol3.bottom+20 and perso.y<=sol2.bottom+20:
                if perso.x > sol2.right:
                    perso.descente=True

                if (perso.hitbox).colliderect(sol2):
                    perso.y=sol2[1]-perso.height-1

                if perso.descente :
                    perso.y+=5

                else : 
                    perso.blesse=False

                if perso.hitbox[0]>=portailO1[0] and perso.hitbox[0]+perso.hitbox[2]<=portailO1[0]+portailO1[2]:
                    if perso.hitbox[1] >=portailO1[1]:
                        perso.x=portailB3[0]-20
                        perso.y=portailB3[1]-7
                        canal_4.play(sonPortail)

                if perso.hitbox[0]>=portailB2[0] and perso.hitbox[0]+perso.hitbox[2]<=portailB2[0]+portailB2[2]:
                    if perso.hitbox[1]+perso.hitbox[3] >=portailB2[1]:
                        perso.x=portailO3[0]+10
                        perso.y=portailO3[1]+5
                        canal_4.play(sonPortail)

#Partie en haut à gauche de la carte   
            elif perso.hitbox[1]+perso.hitbox[3]>sol4.bottom and perso.y<=sol3.bottom+20:    

                if perso.hitbox[0]<sol3[0]:
                    perso.descente=True
                
                if perso.hitbox[0]>boite1[0]+boite1[2]:
                    perso.descente=True
                        
                if (perso.hitbox).colliderect(sol3):
                    perso.y=sol3[1]-perso.height-1

                
                if (perso.hitbox).colliderect(pics1)and perso.hitbox[0]+perso.hitbox[2]<=446:
                    perso.x-=10
                    perso.blesse=True
                    perso.damage(1)


                elif (perso.hitbox).colliderect(pics1)and perso.hitbox[0]>480 :
                    perso.x+=10
                    perso.blesse=True
                    perso.damage(1)

                elif perso.hitbox.colliderect(pics1) and perso.hitbox[0]>425 and perso.hitbox[0]<475 :
                    perso.y=pics1[1]-perso.hitbox[3]
                    perso.y-=15
                    perso.descente=True
                    perso.blesse=True
                    perso.damage(1)

                if not perso.hitbox.colliderect(pics1) :
                    perso.blesse=False  
                    

                if perso.hitbox[0]>=portailO2[0] and perso.hitbox[0]+perso.hitbox[2]<=portailO2[0]+portailO2[2]:
                    if perso.hitbox[1] >=portailO2[1]:
                        perso.x=portailB1[0]-20
                        perso.y=portailB1[1]-1
                        canal_4.play(sonPortail)

                if (perso.hitbox).colliderect(boite1):
                    perso.y=boite1[1]-perso.height
                    perso.descente=False


                if perso.descente and perso.y+perso.height!=sol3[1]:
                    perso.y+=5

                if perso.hitbox[0]>=portailB3[0] and perso.hitbox[0]+perso.hitbox[2]<=portailB3[0]+portailB3[2]:
                    if perso.hitbox[1] >=portailB3[1]:
                        perso.x=portailO1[0]+10
                        perso.y=portailO1[1]+10
                        canal_4.play(sonPortail)

            if (perso.hitbox).colliderect(sol4):
                    perso.y=sol4[1]-perso.height-1
                    perso.descente=False   

            if (perso.hitbox).colliderect(acide):
                perso.blesse=True
                perso.damage(1)
                perso.y-=10
                perso.descente=True
            
#Partie finale de la carte   
            elif perso.hitbox[1]+perso.hitbox[3]<=sol4.bottom-8:
                if (perso.hitbox).colliderect(toit):
                    perso.y=toit[1]+toit[3]
                    perso.descente=True

                if perso.descente and perso.y+perso.height<sol4[1]:
                    perso.y+=5

                if perso.hitbox[0]>=portailO3[0] and perso.hitbox[0]+perso.hitbox[2]<=portailO3[0]+portailO3[2]:
                    if perso.hitbox[1] >=portailO3[1]:
                        perso.x=portailB2[0]-10
                        perso.y=portailB2[1]-1
                        canal_4.play(sonPortail)

#Ouverture de la porte et fin du jeu 
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

#Déplacement du personnage                     
            if keys[pygame.K_a] and perso.x > perso.velocity:
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
                    perso.y -= int((perso.jumpCount * abs(perso.jumpCount)) * 0.3)
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
            
            if finNiveau==False and gameOver==False:
                perso.dessin(win)

                if perso.hp <=0 and gameOver==False:
                    Jeu.fade(1024,768)
                    gameOver=True

#Affichage des portails
                win.blit(pygame.image.load('data\\portailO\\redim2\\PNG\\portal1.png'), (portailO1[0],portailO1[1]))
                win.blit(pygame.image.load('data\\portailB\\redim2\\PNG\\portal1.png'), (portailB1[0],portailB1[1]))
                win.blit(pygame.image.load('data\\portailO\\redim2\\PNG\\portal1.png'), (portailO2[0],portailO2[1]))
                win.blit(pygame.image.load('data\\portailB\\redim2\\PNG\\portal1.png'), (portailB2[0],portailB2[1]))
                win.blit(pygame.image.load('data\\portailO\\redim2\\PNG\\portal1.png'), (portailO3[0],portailO3[1]))
                win.blit(pygame.image.load('data\\portailB\\redim2\\PNG\\portal1.png'), (portailB3[0],portailB3[1]))
                            
                perso.update_hp_bar(win)

                pygame.display.update()

#Gestion du Game Over et affichage à l'écran            
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

#Gestion de la fin du jeu              
            elif finNiveau==True:
                pygame.mixer.stop()
                pygame.mixer.music.stop()
                
                if keys[pygame.K_RETURN]:
                    sys.exit()
                
                win.fill((0,0,0))  
                win.blit(victoire,(350,75))                   
                    
                text = police.render('PRESS ENTER TO QUIT', True, (255,255,255)) 
                textRect = text.get_rect() 
                win.blit(text, (textRect[0]+250,textRect[1]+450)) 
                    
                pygame.display.update()  

#Outils pour le débuggage         
            """
            pygame.draw.rect(win, (0,255,0), sol1,2) # To draw the hit box around the player
            pygame.draw.rect(win, (0,255,0), sol3,2) # To draw the hit box around the player
            pygame.draw.rect(win, (0,255,0), sol4,2) # To draw the hit box around the player
            pygame.draw.rect(win, (0,255,0), boite1,2) # To draw the hit box around the player
            pygame.draw.rect(win, (0,175,175), sol2,2) # To draw the hit box around the player
            pygame.draw.rect(win, (0,175,175), interrupteur,2) # To draw the hit box around the player
            pygame.draw.rect(win, (0,175,175), porteFin,2) # To draw the hit box around the player
            pygame.draw.rect(win, (0,175,175), scie,2) # To draw the hit box around the player
            pygame.draw.rect(win, (0,175,175), portailB2,2) # To draw the hit box around the player
            pygame.draw.rect(win, (0,175,175), toit,2) # To draw the hit box around the player
            pygame.draw.rect(win, (0,175,175), pics1,2) # To draw the hit box around the player
            """
            
            pygame.display.update()
                


Jeu.loop()    

pygame.QUIT
