import pygame
import time
from timeit import default_timer as timer
import random
import threading
import math

pygame.init()

#Declaring Variables
displayWidth = 1280
displayHeight = 800

FPS = 60

gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption('Cubeman')

pygame.display.update()

clock = pygame.time.Clock()
createCubeInterval = 5.0

font = pygame.font.SysFont("jokerman", 50)

floor = 650

def textObjects(text, colour):
    textSurface = font.render(text, True, colour)
    return textSurface, textSurface.get_rect()

def messageToScreen(msg, colour, yPosition = 0):
    textSurf, textRect = textObjects(msg, colour)
    textRect.center = (displayWidth/2), (displayHeight/2) + yPosition
    gameDisplay.blit(textSurf, textRect)
    
def displayScore(msg, colour):
    screen_text = font.render(msg, True, colour)
    gameDisplay.blit(screen_text, [displayWidth-(0.25*displayWidth), (0.005*displayHeight)])
    
def createDownCube(randDownCubePositionX, randDownCubePositionY, cubemanSize, colour):  
    pygame.draw.rect(gameDisplay, pygame.Color(colour), [randDownCubePositionX, randDownCubePositionY, cubemanSize, cubemanSize])        

def createDownCube2(secondDownCubePositionX, secondDownCubePositionY, cubemanSize):
    pygame.draw.rect(gameDisplay, pygame.Color('blue'), [secondDownCubePositionX, secondDownCubePositionY, cubemanSize, cubemanSize])

def createSideCube(randSideCubePositionX, randSideCubePositionY, cubemanSize, colour):
        pygame.draw.rect(gameDisplay, pygame.Color(colour), [randSideCubePositionX, randSideCubePositionY, cubemanSize, cubemanSize])
        
def createSideCube2(secondSideCubePositionX, secondSideCubePositionY, cubemanSize):
    pygame.draw.rect(gameDisplay, pygame.Color('blue'), [secondSideCubePositionX, secondSideCubePositionY, cubemanSize, cubemanSize])        
        
def gameIntro():

    intro = True

    while intro:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                    
        gameDisplay.fill(pygame.Color("White"))
        messageToScreen("Welcome to Cubeman!", pygame.Color("black"), -25)
        messageToScreen("Press C to play, and Q to quit.", pygame.Color("black"), 25)
        pygame.display.update()
        clock.tick(FPS) 

def gameLoop():

    start = timer()
    gotCubed = False
    gameOver = False
    split = False
    
    floorShrink = 0.2
    floorSplit = 0.2

    floorLength = displayWidth/2
    
    firstFloorStart = 0
    firstFloorEnd = firstFloorStart + floorLength
    
    secondFloorStart = displayWidth/2 - 2
    secondFloorEnd = secondFloorStart + floorLength
      
    cubemanSize = 15
    cubeDownCounter = 0
    cubeSideCounter = 0

    secondSideCubeCounter = 0
    secondDownCubeCounter = 0

    firstFloorCounter = 0
    secondFloorCounter = 0
    
    cubemanPositionX = displayWidth/2
    cubemanPositionY = floor-cubemanSize
    cubemanPositionXChange = 0
    cubemanPositionYChange = 0

    randDownCubePositionX = random.randrange(firstFloorStart, secondFloorEnd, cubemanSize)
    randDownCubePositionY = 0
    randDownCubePositionYChange = 5
    randDownCubePositionXChange = 0

    randSideCubePositionX = firstFloorStart
    randSideCubePositionY = floor-cubemanSize
    randSideCubePositionYChange = 0
    randSideCubePositionXChange = 5

    secondSideCubePositionX = secondFloorStart
    secondSideCubePositionXChange = 5
    secondSideCubePositionY = floor-cubemanSize

    secondDownCubePositionX = random.randrange(secondFloorStart, secondFloorEnd, cubemanSize)
    secondDownCubePositionY = 0
    secondDownCubePositionYChange = 5
    
    jumping = False
    score = 0
    fadeTimer = 0
    
    firstFloorTransparency = 255
    secondFloorTransparency = 255
    
    while not gotCubed:
        
        while gameOver:

            gameDisplay.fill(pygame.Color("white"))
            messageToScreen("YOU'VE BEEN CUBED!", pygame.Color("red"), -60)
            messageToScreen("You lasted: " + str(round(score, 1)) + " seconds.",  pygame.Color("red"), 0)
            messageToScreen("Press C to play again or Q to quit", pygame.Color("red"), 60)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gotCubed = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()
                        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gotCubed = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    cubemanPositionXChange = -cubemanSize
                    print("firstfloorcounter: " + str(firstFloorCounter))
                    print("firstfloortransparency: " + str(firstFloorTransparency))
                    print("secondFloortransparency: " + str(secondFloorTransparency))
                    print("cubemanpositionychange: " + str(cubemanPositionYChange))
                if event.key == pygame.K_RIGHT:
                    cubemanPositionXChange = cubemanSize
                if event.key == pygame.K_UP and jumping == False:
                    cubemanPositionY = floor -5*cubemanSize
                    cubemanPositionYChange = 4
                    jumping = True
                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    cubemanPositionXChange = 0        

        if cubemanPositionX < 0:
            cubemanPositionX = cubemanSize
        if cubemanPositionX >= displayWidth-cubemanSize:
            cubemanPositionX = displayWidth-cubemanSize
            
        if cubemanPositionY == floor-cubemanSize and cubemanPositionX < secondFloorEnd-cubemanSize and cubemanPositionX > firstFloorStart and firstFloorTransparency >0 and secondFloorTransparency>0:
            cubemanPositionYChange = 0
            jumping = False
        if cubemanPositionX > secondFloorEnd-cubemanSize or cubemanPositionX < firstFloorStart-cubemanSize:
            cubemanPositionYChange = 4
            jumping = True
            
        if cubemanPositionY > floor:
            if cubemanPositionX < secondFloorEnd and cubemanPositionX > secondFloorEnd-cubemanSize:
                cubemanPositionX = secondFloorEnd+cubemanSize
            if cubemanPositionX > firstFloorStart and cubemanPositionX < firstFloorStart+cubemanSize:
                cubemanPositionX = firstFloorStart-cubemanSize
            
        if randDownCubePositionY >= floor:
            cubeDownCounter += 1
            randDownCubePositionY = 0
            if floorLength > 460:
                randDownCubePositionX = random.randrange(math.ceil(firstFloorStart), math.floor(secondFloorEnd-cubemanSize), cubemanSize)
            if floorLength <= 460:
                randDownCubePositionX = random.randrange(math.ceil(firstFloorStart), math.floor(firstFloorEnd-cubemanSize), cubemanSize)
        if randSideCubePositionX > secondFloorEnd-cubemanSize:
            randSideCubePositionXChange = -randSideCubePositionXChange
            cubeSideCounter += 1
        if randSideCubePositionX < firstFloorStart:
            randSideCubePositionXChange = randSideCubePositionXChange*(-1)
            cubeSideCounter += 1
        if randSideCubePositionX > firstFloorEnd-cubemanSize and floorLength <= 460:
            randSideCubePositionXChange = -randSideCubePositionXChange
            cubeSideCounter += 1
            
        if secondSideCubePositionX > secondFloorEnd-cubemanSize:
            secondSideCubePositionXChange = -secondSideCubePositionXChange
            secondSideCubeCounter += 1
        if secondSideCubePositionX < secondFloorStart:
            secondSideCubePositionXChange = -secondSideCubePositionXChange
            secondSideCubeCounter += 1
            
        if cubemanPositionX >= randDownCubePositionX and cubemanPositionX <= randDownCubePositionX + cubemanSize:
            if cubemanPositionY >= randDownCubePositionY and cubemanPositionY <= randDownCubePositionY + cubemanSize:    
                gameOver = True
        if cubemanPositionX >= randSideCubePositionX and cubemanPositionX <= randSideCubePositionX + cubemanSize:
            if cubemanPositionY >= randSideCubePositionY and cubemanPositionY <= randSideCubePositionY + cubemanSize:
                gameOver = True
        if cubemanPositionX >= secondSideCubePositionX and cubemanPositionX <= secondSideCubePositionX + cubemanSize and floorLength <= 460:
            if cubemanPositionY >= secondSideCubePositionY and cubemanPositionY <= secondSideCubePositionY + cubemanSize:
                gameOver = True
        if cubemanPositionX >= secondDownCubePositionX and cubemanPositionX <= secondDownCubePositionX + cubemanSize:
            if cubemanPositionY >= secondDownCubePositionY and cubemanPositionY <= secondDownCubePositionY + cubemanSize:
                gameOver = True
        
        if cubeDownCounter%5 == 0 and randDownCubePositionYChange <= 20 and cubeDownCounter > 0:
            randDownCubePositionYChange += 0.05
        if cubeSideCounter%5 == 0 and randSideCubePositionXChange <= 20 and cubeSideCounter > 0:
            randSideCubePositionXChange -= 0.05
        if cubeSideCounter%10 == 0 and cubeSideCounter > 0 and randSideCubePositionXChange <= 20:
            randSideCubePositionXChange += 0.05
            
        if secondDownCubeCounter%5 == 0 and secondDownCubePositionYChange <= 20 and secondDownCubeCounter > 0:
            secondDownCubePositionYChange += 0.05
        if secondSideCubeCounter%5 == 0 and secondSideCubePositionXChange <= 20 and secondSideCubeCounter > 0:
            secondSideCubePositionXChange -= 0.05
        if secondSideCubeCounter%10 == 0 and secondSideCubeCounter > 0 and secondSideCubePositionXChange <= 20:
            secondSideCubePositionXChange += 0.05

        if floorLength <= displayWidth/2 and floorLength > 460:
            firstFloorStart += floorShrink
            floorLength -= floorShrink
           
        if firstFloorStart < cubemanSize and floorLength <= 460:
            floorSplit = -floorSplit
            firstFloorCounter += 1
            secondFloorCounter += 1
            
        if firstFloorStart > displayWidth/2 - floorLength:
            floorSplit = - floorSplit
            firstFloorCounter += 1
            secondFloorCounter += 1
        
        if cubemanPositionY >= displayHeight:
            gameOver = True
            
        if floorLength <= 460:    
            if cubemanPositionX < secondFloorStart and cubemanPositionX > firstFloorEnd:
                cubemanPositionYChange = 4
                jumping = True        
            if cubemanPositionY > floor:
                if cubemanPositionX > secondFloorStart and cubemanPositionX < secondFloorStart+cubemanSize:
                    cubemanPositionX = secondFloorStart-cubemanSize
                if cubemanPositionX < firstFloorEnd and cubemanPositionX > firstFloorEnd-cubemanSize:
                    cubemanPositionX = firstFloorEnd+cubemanSize
            
        cubemanPositionX += cubemanPositionXChange
        cubemanPositionY += cubemanPositionYChange
        
        randDownCubePositionY += randDownCubePositionYChange
        randDownCubePositionX += randDownCubePositionXChange

        firstFloorEnd = firstFloorStart + floorLength
        secondFloorEnd = secondFloorStart + floorLength
    
        randSideCubePositionY += randSideCubePositionYChange
        randSideCubePositionX += randSideCubePositionXChange
        
        gameDisplay.fill(pygame.Color('White'))

        if floorLength <= 460:
            firstFloorStart -= floorSplit
            secondFloorStart += floorSplit
            secondSideCubePositionX += secondSideCubePositionXChange
            secondDownCubePositionY += secondDownCubePositionYChange
            createSideCube2(secondSideCubePositionX, secondSideCubePositionY, cubemanSize)
            createDownCube2(secondDownCubePositionX, secondDownCubePositionY, cubemanSize)
            if secondDownCubePositionY >= floor:
                secondDownCubePositionY = 0
                secondDownCubeCounter += 1
                secondDownCubePositionX = random.randrange(math.ceil(secondFloorStart), math.floor(secondFloorEnd-cubemanSize), cubemanSize)

        if randDownCubePositionX <= firstFloorEnd and randDownCubePositionX >= firstFloorStart:
            createDownCube(randDownCubePositionX, randDownCubePositionY, cubemanSize, "red")
        elif randDownCubePositionX <= secondFloorEnd and randDownCubePositionX >= secondFloorStart:
            createDownCube(randDownCubePositionX, randDownCubePositionY, cubemanSize, "blue")

        if randSideCubePositionX <= firstFloorEnd and randSideCubePositionX >= firstFloorStart:    
            createSideCube(randSideCubePositionX, randSideCubePositionY, cubemanSize, "red")
        elif randSideCubePositionX <= secondFloorEnd and randSideCubePositionX >= secondFloorStart:
            createSideCube(randSideCubePositionX, randSideCubePositionY, cubemanSize, "blue")
            
        pygame.draw.rect(gameDisplay, pygame.Color('black'), [cubemanPositionX, cubemanPositionY, cubemanSize, cubemanSize])

        firstFloor = pygame.Surface((floorLength, displayHeight-floor))
        secondFloor = pygame.Surface((floorLength, displayHeight-floor))
        secondFloor.set_alpha(secondFloorTransparency)
        firstFloor.set_alpha(firstFloorTransparency)
        firstFloor.fill(pygame.Color("red"))
        secondFloor.fill(pygame.Color("blue"))
        gameDisplay.blit(firstFloor, (firstFloorStart, floor))
        gameDisplay.blit(secondFloor, (secondFloorStart, floor))
        
        if firstFloorCounter > 0:
            fadeTimer += 1/60
            if fadeTimer>0 and fadeTimer<4:
                messageToScreen("Get off the platform before it dissapears!", pygame.Color("red"), -50)
            if cubemanPositionX >= firstFloorStart and cubemanPositionX <= firstFloorEnd:
                firstFloorTransparency -= 0.5
                secondFloorTransparency = 255
            elif cubemanPositionX >= secondFloorStart and cubemanPositionX <= secondFloorEnd:
                firstFloorTransparency = 255
                secondFloorTransparency -= 0.5
            
        if firstFloorTransparency <= 0:
            firstFloorTransparency = 0
            if cubemanPositionX > firstFloorStart and cubemanPositionX < firstFloorEnd:
                cubemanPositionYChange = 4
                jumping = True
        if secondFloorTransparency <= 0:
            secondFloorTransparency = 0
            if cubemanPositionX > secondFloorStart and cubemanPositionX < secondFloorEnd:
                cubemanPositionYChange = 4
                jumping = True
                
        score += 1/60
        displayScore("Score: " + str(round(score,1)), pygame.Color("black"))
        pygame.display.update()
        clock.tick(FPS)       
   
    pygame.quit()
    quit()
    
gameIntro()
gameLoop()


