import pygame
import math 
import time
from Engine import Engine
engine = Engine()
global screen
playing = True
engine.update_dt()

#setup pygame window
def draw():
    screen = pygame.display.set_mode((1540,820))
    screen.fill((255,255,255))
    return screen

class Projectile:
    def __init__ (self,velocity,angle,gravity,height,size):
        self.radAngle = (angle*2*math.pi/360)
        self.velocity = velocity
        self.horiVelocity = (velocity * math.cos(self.radAngle))
        self.vertVelocity = (velocity * math.sin(self.radAngle))
        self.acceleration = gravity
        self.size = size
        self.xPos = 0
        self.yPos = self.size + 0.0000000001 + height
        self.initialHeight = height
        self.maxHoriDistance = 0
        self.maxVertDistance = 0

class trailCircle:
    def __init__ (self,xPos,yPos):
        self.xPos = xPos
        self.yPos = yPos

#calculate the max height and distance of projectile
def calculateDistances(projectile,finalVerticalVelocity):
    flightTime = (finalVerticalVelocity-projectile.vertVelocity)/projectile.acceleration
    horiDistance = projectile.horiVelocity * flightTime
    timeOfVertDistance = (projectile.velocity*-1)/projectile.acceleration
    vertDistance = (projectile.vertVelocity * timeOfVertDistance + 0.5*projectile.acceleration*timeOfVertDistance**2)+projectile.initialHeight
    return (horiDistance,vertDistance)

#calculate new positions of circle subroutine
def calculateCircle(projectile,xAcceleration,multi):
    NradianAngle = (math.atan(projectile.vertVelocity/projectile.horiVelocity))
    NcircleX = projectile.xPos +(projectile.horiVelocity * engine.dt * multi)
    NcircleY = projectile.yPos +(projectile.vertVelocity * engine.dt * multi)
    NcircleXVelocity = projectile.horiVelocity+(xAcceleration * engine.dt * multi)
    NcircleYVelocity = projectile.vertVelocity+(projectile.acceleration * engine.dt * multi)
    return (NcircleX,NcircleY,NcircleXVelocity,NcircleYVelocity,NradianAngle)

#calculates the scaled value of circle size
def calculateCircleSize(projectile,multi):
    scaledCircleSize = projectile.size/multi
    projectile.yPos = scaledCircleSize + 0.00000001 + projectile.initialHeight
    return(scaledCircleSize)


#final adjustments subroutine
#figures out the final movements to make to the projectile
def finalAdjustments(projectile,multi):
    remainingY = projectile.size-projectile.yPos
    remainingX = projectile.maxHoriDistance - projectile.xPos*multi
    return (remainingX,remainingY)


#use distances to calculate required scale
#this calculates the scales for the values and the scale in order to keep the projectile from going off screen
def calculateScale(projectile):
    multi = max((math.ceil((projectile.maxVertDistance+projectile.size*2)/800)),(math.ceil((projectile.initialHeight+projectile.size*2)/800)),(math.ceil((projectile.maxHoriDistance+projectile.size)/1500)))
    print(multi)
    tempXScales = [300,600,900,1200,1500]
    tempYScales = [200,400,600,800]
    xScales = [item * multi for item in tempXScales]
    xScales = [str(scale) for scale in xScales]
    yScales = [item * multi for item in tempYScales]
    yScales = [str(scale) for scale in yScales]
    return (xScales,yScales,multi)

#scales the values
def scaleValues(projectile,multi):
    scaledHoriVelocity = projectile.horiVelocity/multi
    scaledVertVelocity = projectile.vertVelocity/multi
    scaledAcceleration = projectile.acceleration/multi
    scaledHeight =projectile.initialHeight/multi
    return(scaledHoriVelocity,scaledVertVelocity,scaledAcceleration,scaledHeight)

#check whether their guess is equal to the answer
#display whether they are right on screen
def checkGuess(screen,finalYVelocity,projectile,guess,v,multi):
    finalVelocity = round(math.sqrt(finalYVelocity**2+projectile.horiVelocity**2),1)
    finalDisplacement = round((math.sqrt(projectile.initialHeight**2+projectile.maxHoriDistance**2)),1)
    finalHoriDisplacement = round((projectile.maxHoriDistance),1)
    finalYVelocity = round(finalYVelocity,1)
    answers = [finalHoriDisplacement,finalDisplacement,finalYVelocity,finalVelocity]
    if v != 1:
        pygame.font.init()
        font = pygame.font.SysFont("Roboto",40)
        if guess == answers[v-2]:
            text = font.render("Correct Answer!!",True,(0,0,0),(255,255,255))
        else:
            answerText = str(answers[v-2])
            incorrectText = ("Incorrect, correct answer was: ")
            totalText = (incorrectText + answerText)
            text = font.render(totalText,True,(0,0,0),(255,255,255))
        textBox = text.get_rect()
        textBox.center = (750,400)
        screen.blit(text,textBox)


#draqs the background grid
def drawBg(screen):
    bgImage = pygame.image.load('Grid.png')
    screen.blit(bgImage,(0,20))

#draw the Y scales
def drawYText(screen,scales):
    pygame.font.init()
    font = pygame.font.SysFont("Arial",20)
    count = 1
    for scale in scales:
        text = font.render(scale,True,(0,0,0),(255,255,255))
        textBox = text.get_rect()
        textBox.center = (30,820-200*count)
        screen.blit(text,textBox)
        count += 1

#draw the X scales
def drawXText(screen,scales):
    pygame.font.init()
    font = pygame.font.SysFont("Arial",20)
    count = 1
    for scale in scales:
        text = font.render(scale,True,(0,0,0),(255,255,255))
        textBox = text.get_rect()
        textBox.center = (300*count,800)
        screen.blit(text,textBox)
        count+=1

#draw the projectile property values at the top right of the screen
def drawValues(screen,multi,projectile):
    tempFloatValues = [projectile.xPos,projectile.yPos - projectile.size-projectile.initialHeight,projectile.horiVelocity,projectile.vertVelocity]
    floatValues = [(value * multi)for value in tempFloatValues]
    valueNames = ["Horizontal displacement  =  ","Vertical displacement  =  ","Horizontal velocity  =  ","Vertical velocity  =  "]
    roundedValues = [round(value,3)for value in floatValues]
    values = [str(value) for value in roundedValues]
    pygame.font.init()
    font=pygame.font.SysFont("Arial",20)
    for i in range(0,len(values)):
        text = font.render(valueNames[i],True,(0,0,0),(255,255,255))
        textBox = text.get_rect()
        textBox.center = (1300,(i+2)*20)
        screen.blit(text,textBox)
        text = font.render(values[i],True,(0,0,0),(255,255,255))
        textBox = text.get_rect()
        textBox.center = (1450,(i+2)*20)
        screen.blit(text,textBox)


def drawCenterText(screen,text):
    pygame.font.init()
    font = pygame.font.SysFont("Roboto",50)
    text = font.render(text,True,(0,0,0),(255,255,255))
    textBox = text.get_rect()
    textBox.center = (750,100)
    screen.blit(text,textBox)

def drawFinalVelocity(screen,circleYVelocity):
    pygame.font.init()
    font = pygame.font.SysFont("Arial",20)
    text = font.render(str(round(circleYVelocity,3)),True,(0,0,0),(255,255,255))
    textBox = text.get_rect()
    textBox.center = (1450,100)
    screen.blit(text,textBox)

#draw repositioned circle subroutine
def updateCircle(projectile,xScales,yScales,finalYVelocity,multi,guess,v,screen,trailCounter,trails,currentTrailCounter):
    drawBg(screen)
    if (projectile.xPos) > currentTrailCounter:
        trail = trailCircle(projectile.xPos,projectile.yPos)
        trails.append(trail) 
        currentTrailCounter += trailCounter
    for trail in trails:
        pygame.draw.circle(screen,(42,56,14),(trail.xPos,820-trail.yPos),2)
    pygame.draw.rect(screen,(0,10,10),(0,820-projectile.initialHeight,20,projectile.initialHeight))
    pygame.draw.circle(screen,(17,59,121),(projectile.xPos,820-projectile.yPos),(projectile.size))
    pygame.draw.line(screen,(0,255,0),(projectile.xPos,820-projectile.yPos),(projectile.xPos + projectile.horiVelocity,820-projectile.yPos),width = 2)
    pygame.draw.line(screen,(0,0,255),(projectile.xPos,820-projectile.yPos),(projectile.xPos,820-(projectile.yPos + projectile.vertVelocity)),width = 2)
    pygame.draw.line(screen,(255,0,255),(projectile.xPos,820-projectile.yPos),(projectile.xPos+projectile.horiVelocity,820-(projectile.yPos + projectile.vertVelocity)),width = 2)
    pygame.draw.polygon(screen,(0,255,00),points = [(projectile.xPos + projectile.horiVelocity,820-projectile.yPos-5),(projectile.xPos + projectile.horiVelocity,820-projectile.yPos+5),(projectile.xPos+projectile.horiVelocity+7,820-projectile.yPos)])
    pygame.draw.polygon(screen,(255,0,255),points=[(projectile.xPos +projectile.horiVelocity - (5*math.cos((180*math.pi/360)-projectile.radAngle)),820-(projectile.yPos + projectile.vertVelocity + (5*math.sin((180*math.pi/360)-projectile.radAngle)))),(projectile.xPos +projectile.horiVelocity + (5*math.cos((180*math.pi/360)-projectile.radAngle)),820-(projectile.yPos + projectile.vertVelocity - (5*math.sin((180*math.pi/360)-projectile.radAngle)))),(projectile.xPos + projectile.horiVelocity + 7*math.cos(projectile.radAngle),(820-(projectile.yPos + projectile.vertVelocity + 7*math.sin(projectile.radAngle))))])
    if projectile.vertVelocity > 0:
        pygame.draw.polygon(screen,(0,0,255),points=[(projectile.xPos-5,820-(projectile.yPos+projectile.vertVelocity)),(projectile.xPos+5,820-(projectile.yPos+projectile.vertVelocity)),(projectile.xPos,820-(projectile.yPos+projectile.vertVelocity+7))])
    else:
        pygame.draw.polygon(screen,(0,0,255),points=[(projectile.xPos-5,820-(projectile.yPos+projectile.vertVelocity)),(projectile.xPos+5,820-(projectile.yPos+projectile.vertVelocity)),(projectile.xPos,820-(projectile.yPos+projectile.vertVelocity-7))])
    drawValues(screen,multi,projectile)
    drawXText(screen,xScales)
    drawYText(screen,yScales)
    if  projectile.yPos - projectile.size == 0:
        drawFinalVelocity(screen,finalYVelocity)
        checkGuess(screen,finalYVelocity,projectile,guess,v,multi)
    else:
        if len(trails) > 0:
            drawCenterText(screen,"Space to pause[Q to quit]")
    pygame.display.update()
    try:
        return(trails,currentTrailCounter)
    except:
        pass


def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()

                    


def runItAll(guess,velocity,angle,whichGuess,circleSize,gravity,height):
        screen = draw()
        projectile = Projectile(velocity,angle,gravity,height,circleSize)
        print(projectile.acceleration)
        finalYVelocity = -1*(math.sqrt(projectile.vertVelocity**2 - 2 * projectile.acceleration * projectile.initialHeight))
        (projectile.maxHoriDistance,projectile.maxVertDistance)=calculateDistances(projectile,finalYVelocity)
        (xScales,yScales,multi) = calculateScale(projectile)
        (projectile.horiVelocity,projectile.vertVelocity,projectile.acceleration,projectile.initialHeight) = scaleValues(projectile,multi)        
        projectile.size = calculateCircleSize(projectile,multi)
        first = True
        trailCounter = ((projectile.maxHoriDistance / multi)/100)
        currentTrailCounter = trailCounter
        trails = []
        print (trailCounter)
        while projectile.yPos > projectile.size:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pause()
                    if event.key == pygame.K_q:
                        pygame.quit()
            (trails,currentTrailCounter) = (updateCircle(projectile,xScales,yScales,finalYVelocity,multi,guess,whichGuess,screen,trailCounter,trails,currentTrailCounter))
            if first:
                drawCenterText(screen,"[Space to start][Q to quit]")
                pygame.display.update()
                pause()
            first = False 
            (projectile.xPos,projectile.yPos,projectile.horiVelocity,projectile.vertVelocity,projectile.radAngle)= calculateCircle(projectile,0,0.25)
        (addX,addY) = finalAdjustments(projectile,multi)
        projectile.xPos += addX/multi
        projectile.yPos += addY
        (trails,currentTrailCounter) = (updateCircle(projectile,xScales,yScales,finalYVelocity,multi,guess,whichGuess,screen,trailCounter,trails,currentTrailCounter))
        drawCenterText(screen,"[Space to finish][Q to quit]")
        pygame.display.update()
        pause()
        pygame.quit()




