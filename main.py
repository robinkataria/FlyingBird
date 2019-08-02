import random
import sys
import pygame
from pygame.locals import *

#Global Variables:

FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/background.png'
PIPE = 'gallery/sprites/pipe.png'

#Shows Welcome img on Screen
def welcomeScreen():

    #Initialise elements coordinates on welcomeScreen
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT * 0.13)
    basex = 0

    while True:
        for event in pygame.event.get():

            #Cross/Esc Button: Close the game
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            #Space/UP Button: Start the game
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                return

            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(GAME_SPRITES['player'],(playerx,playery)) 
                SCREEN.blit(GAME_SPRITES['message'],(messagex,messagey))
                SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
            
            pygame.display.update()
            FPSCLOCK.tick(FPS)


#main game logic            
def mainGame():
    score = 0
    playerx = int(SCREENWIDTH / 5)
    playery = int(SCREENWIDTH / 2)

    #Create 2 pipes for blitting
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    #list of upper pipes & lower pipes
    upperPipes = [
        {'x':SCREENWIDTH + 200 , 'y':newPipe1[0]['y']},
        {'x':SCREENWIDTH + 200 , 'y':newPipe2[0]['y']}
    ]
    lowerPipes = [
        {'x':SCREENWIDTH + 200 , 'y':newPipe1[1]['y']},
        {'x':SCREENWIDTH + 200 + (SCREENWIDTH/2) , 'y':newPipe2[1]['y']}
    ]

    #motion initialisation

    pipeVelX = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8

    playerAccY = 1

    playerFlapAccv = -8  #vel while flapping
    playerFlapped = False   #True, when bird is flapping

    
    while True: 

        for event in pygame.event.get():
            
            #Cross/Esc Button: Close the game
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            #Space/UP Button: Flap
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                if playery > 0 :        #bird inside screen
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play() 

        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)      #True, if player crashed

        if crashTest:
            return
        
        #check for Score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2

        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos +4:
                score += 1
                GAME_SOUNDS['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False

        playerHeight = GAME_SPRITES['player'].get_height() 
        playery = playery + min(playerVelY , GROUNDY - playerHeight - playery)   

        
        #Move Pipes to LEFT
        for upperPipe,lowerPipe in zip(upperPipes,lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        #Add new pipe when 1st pipe is about to cross the leftmost part of screen
        if 0 < upperPipes[0]['x'] < 5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        #If pipe is out of the screen, remove(pop) it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        #Blitting on the screen
        SCREEN.blit(GAME_SPRITES['background'],(0,0))
        for upperPipe,lowerPipe in zip(upperPipes,lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0],(upperPipe['x'],upperPipe['y']))    
            SCREEN.blit(GAME_SPRITES['pipe'][1],(lowerPipe['x'],lowerPipe['y']))
        SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
        SCREEN.blit(GAME_SPRITES['base'],(0,GROUNDY))
        
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width) /2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset,SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


#return True, if player collides
def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery> GROUNDY - 25  or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False        


#returns position of two pipes for Blitting
def getRandomPipe():
    
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT / 3
    pipeX = SCREENWIDTH + 10
    y2 = offset + random.randrange(0,int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2*offset))
    y1 = pipeHeight - y2 + offset

    pipe = [
        {'x':pipeX , 'y': -y1 },  #UpperPipe
        {'x':pipeX , 'y': y2}     #LowerPipe
    ]
    return pipe


#main Function:
if __name__ == "__main__":
    pygame.init()          #initialise all pygame modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Birds By Robin')

    #Game Sprites Load:
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav') 
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    #Game Sprites Load:
    GAME_SPRITES['message'] = pygame.image.load('gallery/sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert_alpha()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()
    
    GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
        pygame.image.load(PIPE).convert_alpha()
    )
    GAME_SPRITES['numbers'] = (
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha()
    )

    while True:
        welcomeScreen()
        mainGame()
