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
fond = pygame.image.load('data\\interface\\map2.png')
fond2 = pygame.image.load('data\\interface\\map2ouverte.png')
personnage = pygame.image.load('data\\perso\\standing.png')
personnageBlesse = pygame.image.load('data\\perso\\persoTransparent.png')

GameOver=pygame.image.load('data\\interface\\gameover.png')

police=pygame.font.Font('data\\PressStart2P.ttf', 32) 

scieDessin=pygame.image.load("data\\scie_redim\\Saw.png")

clock = pygame.time.Clock()

run=True            #run est à True car il n'a plus besoin d'être lancé de l'extérieur
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
        if not(self.standing):
            if self.droite == True and self.blesse==False :
                win.blit(mvtDroite[self.CptPas//3], (self.x,self.y))
                self.CptPas = self.CptPas + 1
            elif self.gauche == True and self.blesse==False:
                win.blit(mvtGauche[self.CptPas//3], (self.x,self.y))
                self.CptPas = self.CptPas +1
        
            elif not self.gauche and not self.droite and not self.blesse : 
                win.blit(personnage, (self.x,self.y))
        else:
            if self.droite:
                win.blit(mvtDroite[0], (self.x, self.y))
            else:
                win.blit(mvtGauche[0], (self.x, self.y))

        self.hitbox=pygame.Rect(self.x+9,self.y+14,31,50)
        #pygame.draw.rect(win, (0,255,0), self.hitbox,2) # Dessin de la hitbox du personnage

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
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.hitbox=pygame.Rect(self.x,self.y,self.width,self.height)



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
        canal_3=pygame.mixer.Channel(2)
        sonScie=pygame.mixer.Sound('data\\sons\\son_hache.wav')
        canal_3.play(sonScie, loops=-1)
        canal_3.set_volume(0.1)
        canal_4=pygame.mixer.Channel(3)
        sonPortail=pygame.mixer.Sound('data\\sons\\son_portail.wav')
        canal_4.set_volume(0.3)
        perso = Joueur(951, 116, 48, 64)
        barils = Boite(0, 288, 66, 95)
        grosseBoite= pygame.Rect(392,480,132,195)
        sol1 = pygame.Rect(661,181,363,26)
        sol2 = pygame.Rect(0,384,524,27)
        sol3 = pygame.Rect(0,571,393,23)
        sol4 = pygame.Rect(490,650,700,23)
        toit = pygame.Rect(0,0,1024,83)
        pics1 = pygame.Rect(825,168,56,17)
        pics2 = pygame.Rect(301,370,55,18)
        scie1 = pygame.Rect(618,82,87,33)
        scie2 = pygame.Rect(811,620,92,50)
        interrupteur=pygame.Rect(132,524,18,48)
        porteFin=pygame.Rect(45,500,42,75)
        porteOuverte=False
        finNiveau=False
        portailB = pygame.Rect(300,519,50,70)
        portailO = pygame.Rect(600,599,50,70)
        gameOver=False

        global run
        while run == True:
            clock.tick(27)   #fréquence de rafraichissement / nombre de fps

#Boucle qui capte toutes les entrées du clavier
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                
            keys = pygame.key.get_pressed()
        
#Partie la plus haute de la carte   
            if perso.y+perso.height<=sol2[1]:
                if (perso.hitbox).colliderect(sol1):
                    perso.y=sol1[1]-perso.height-3
                if (perso.hitbox).colliderect(toit):
                    perso.y=toit[1]+toit[3]
                    perso.descente=True
                if perso.hitbox.colliderect(pics1):
                    perso.y-=8
                    perso.descente=True
                    perso.blesse=True
                    perso.damage(1)
                    
                elif perso.hitbox.colliderect(scie1) and perso.x >700:
                    perso.x+= 10
                    perso.blesse=True
                    perso.damage(1)
                elif perso.hitbox.colliderect(scie1) and perso.x<700 and perso.x>635 :
                    perso.y+=5
                    perso.descente=True
                    perso.blesse=True 
                    perso.damage(1)
                elif perso.hitbox.colliderect(scie1) and perso.x<635 :
                    perso.y+=5
                    perso.descente=True
                    perso.blesse=True 
                    perso.damage(1)             
                else :
                    perso.blesse=False
                if perso.descente and perso.y+perso.width!=sol1[1]:
                    perso.y+=5  
        
#Partie intermédiaire de la carte   
            elif perso.y+perso.height>=sol1.bottom and perso.y<=sol2.bottom:
                if (perso.hitbox).colliderect(sol2):
                    perso.y=sol2[1]-perso.height-3
                if perso.hitbox.colliderect(pics2):
                    perso.y-=15
                    perso.descente=True
                    perso.blesse=True
                    perso.damage(1)
                else :
                    perso.blesse=False
                if perso.x<=barils.x+barils.width:
                    perso.x=barils.x+barils.width-2  
                else : 
                    perso.descente=True
                if perso.descente and perso.y+perso.width!=sol2[1]:
                    perso.y+=5  

#Partie la plus basse de la carte               
            elif perso.y+perso.height>=sol2.bottom and perso.y<=sol4.bottom and perso.x<sol4[0]+sol4[2] and perso.x >= sol4[0]:
                if (perso.hitbox).colliderect(sol4):
                    perso.y=sol4[1]-perso.height-3
                    
                if perso.hitbox.colliderect(scie2) and perso.x+ perso.width<829:
                        perso.x-= 10
                        perso.blesse=True
                        perso.damage(1)
                elif perso.hitbox.colliderect(scie2) and perso.x+ perso.width>815 and perso.x<868 :
                    perso.y=scie2[1]-2-perso.height
                    perso.y-=25
                    perso.descente=True
                    perso.blesse=True
                    perso.damage(1)
                
                elif perso.hitbox.colliderect(scie2) and perso.x>=868 :
                    perso.x+=10
                    perso.blesse=True
                    perso.damage(1)
                else :
                    perso.blesse=False
                if perso.x<=barils.x+barils.width:
                    perso.x=barils.x+barils.width-2  
                else : 
                    perso.descente=True
                if perso.descente and perso.y+perso.width!=sol2[1]:
                    perso.y+=5  
                if perso.x <= grosseBoite[0]+grosseBoite[2]:
                    perso.x=grosseBoite[0]+grosseBoite[2]
            
#Partie finale de la carte               
            elif perso.y+perso.height>=sol2.bottom and perso.y+perso.height<=sol3.bottom and perso.x<sol3[2]+grosseBoite[2] and perso.x >= sol3[0]:
                    
                if perso.y+perso.height>sol3[1]:
                    perso.y=sol3[1]-perso.height           

                if perso.hitbox.colliderect(grosseBoite):
                        perso.x-= 10

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
                        os.system('start "Jeu3" /min ".\Level3.py"')      
                        sys.exit()   
                
#Déplacement du personnage                     
            if keys[pygame.K_a] and perso.x > perso.velocity:
                perso.x = perso.x - perso.velocity
                perso.gauche = True
                perso.droite = False
                perso.standing = False
            elif keys[pygame.K_d] and perso.x <= 1024 - perso.width - perso.velocity: 
                perso.x = perso.x + perso.velocity
                perso.gauche = False
                perso.droite = True
                perso.standing = False
            
            else :
                perso.standing = True
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
                
#Mécanique de téléportation
                if perso.hitbox[0]>=portailO[0] and perso.hitbox[0]+perso.hitbox[2]<=portailO[0]+portailO[2]:
                    if perso.hitbox[1] >=portailO[1]:
                        perso.x=portailB[0]-20
                        perso.y=portailB[1]+10
                        canal_4.play(sonPortail)

                if perso.hitbox[0]>=portailB[0] and perso.hitbox[0]+perso.hitbox[2]<=portailB[0]+portailB[2]:
                    if perso.hitbox[1] >=portailB[1]:
                        perso.x=portailO[0]+10
                        perso.y=portailO[1]+1
                        canal_4.play(sonPortail)

#Affichage des portails
                win.blit(pygame.image.load('data\\portailO\\redim2\\PNG\\portal1.png'), (portailO[0],portailO[1]))
                win.blit(pygame.image.load('data\\portailB\\redim2\\PNG\\portal1.png'), (portailB[0],portailB[1]))
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
            
            elif finNiveau==True:
                run=False
Jeu.loop()             

pygame.QUIT