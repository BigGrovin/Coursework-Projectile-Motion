#imports
from tkinter import *
import time
import Main as main
import pygame
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math
import GraphPage as graph

#yucky yucky globals
global widgets
global guiCanvas

#save files
class save:
    def __init__(self,name,velocity,angle,gravity,height,circleSize):
        self.name = name
        self.velocity=velocity
        self.angle=angle
        self.gravity=gravity
        self.height=height
        self.circleSize=circleSize

savesList = []
    
#create save subroutine
def createSave(velocityEntryBox,angleEntryBox,gravityEntryBox,heightEntryBox,saveNameEntryBox,circleSizeEntryBox):
    (velocity,angle,gravity,height,circleSize)=collectValues(velocityEntryBox,angleEntryBox,gravityEntryBox,heightEntryBox,circleSizeEntryBox)
    name = saveNameEntryBox.get()
    if name != "":
        savesList.append(save(name,velocity,angle,gravity,height,circleSize))
        if len(widgets) > 23:
            widgets.pop(-1).grid_remove()
    else:
        if len(widgets) < 24:
            nameErrorTextBox = Text(guiCanvas, height = 2, width = 20,bg="CYAN",borderwidth=0,font="Roboto")
            nameErrorTextBox.tag_configure("center",justify = "center")
            widgets.append(nameErrorTextBox)
            nameErrorTextBox.insert("1.0","ERROR! Invalid Name")
            nameErrorTextBox.tag_add("center","1.0","end")
            nameErrorTextBox.grid(row=8,column=4)


#list of widgets
widgets = []

#Create the main frame
frame = Tk()
frame.geometry("1400x800")
frame.resizable(False,False)

#Create the canvas
guiCanvas = Canvas(frame,bg = "cyan",height="800",width="1400")


#Load MainMenu subroutine
def loadMain():
    deleteWids()
    newSimBut = Button(guiCanvas,text="Create New Simulation",activebackground="green",height=7,width=20, command = loadNewSim)
    savedSimsBut = Button(guiCanvas,text="Saved Simulations",activebackground="green",height=7,width=20)
    widgets.append(newSimBut)
    widgets.append(savedSimsBut)
    newSimBut.grid(row=1,column=1,padx=20,pady=20)
    savedSimsBut.grid(row=1,column=3,padx=20,pady=20)
    guiCanvas.pack()


#collect values subroutine
def collectValues(velocityEntryBox,angleEntryBox,gravityEntryBox,heightEntryBox,circleSizeEntryBox):
    velocity = float((velocityEntryBox.get()))
    angle = float((angleEntryBox.get()))
    gravity = (float(gravityEntryBox.get()))*-1
    height = float((heightEntryBox.get()))
    circleSize = float((circleSizeEntryBox.get()))
    return (velocity,angle,gravity,height,circleSize)



#run simulation subroutine
def runSimulation(velocityEntryBox,angleEntryBox,gravityEntryBox,heightEntryBox,circleSizeEntryBox,v,guessEntryBox):
    try:
        whichGuess = v.get()
        try:
            guess = round(float(guessEntryBox.get()),1)
        except:
            guess = 0
        (velocity,angle,gravity,height,circleSize)=collectValues(velocityEntryBox,angleEntryBox,gravityEntryBox,heightEntryBox,circleSizeEntryBox)
        (circleXVelocity,circleYVelocity,radianAngle)= main.calculateVelocities(angle,velocity)
        finalYVelocity = -1*(math.sqrt(circleYVelocity**2 + 2*gravity*height*-1))
        (horiDistance,vertDistance)=main.calculateDistances(velocity,angle,gravity,height)
        (xScales,yScales,multi) = main.calculateScale(horiDistance,vertDistance,height,circleSize)
        (circleXVelocity,circleYVelocity,gravity,height) = main.scaleValues(circleXVelocity,circleYVelocity,gravity,multi,height)
        circleSize = main.calculateCircleSize(circleSize,multi)
        circleX = 0
        circleY = circleSize + 0.0000000001 + height
        first = True
        while circleY > circleSize:
            main.updateCircle(circleX,circleY,circleXVelocity,circleYVelocity,radianAngle,height,xScales,yScales,circleSize,finalYVelocity,multi,guess,whichGuess)
            if first:
                time.sleep(1)
            first = False 
            (circleX,circleY,circleXVelocity,circleYVelocity,radianAngle)= main.calculateCircle(circleX,circleY,circleXVelocity,circleYVelocity,0,gravity,0.35)
        (addX,addY) = main.finalAdjustments(circleY,circleX,horiDistance,circleSize,multi)
        circleX += addX/multi
        circleY += addY
        main.updateCircle(circleX,circleY,circleXVelocity,circleYVelocity,radianAngle,height,xScales,yScales,circleSize,finalYVelocity,multi,guess,whichGuess)
        time.sleep(1)
        pygame.quit()
    except:
        errorMessage(velocityEntryBox,angleEntryBox,gravityEntryBox,heightEntryBox)



#display error in input boxes if invalid entry
def errorMessage(velocityEntryBox,angleEntryBox,gravityEntryBox,heightEntryBox):
    try:
        x = float(velocityEntryBox.get())
    except:
        velocityEntryBox.delete(0,last=99999)
        velocityEntryBox.insert(0,"Invalid Input")
    try:
        x = float(angleEntryBox.get())
    except:
        angleEntryBox.delete(0,last=99999)
        angleEntryBox.insert(0,"Invalid Input")
    try:
        x = float(gravityEntryBox.get())
    except:
        gravityEntryBox.delete(0,last=99999)
        gravityEntryBox.insert(0,"Invalid Input")
    try:
        x = float(heightEntryBox.get())
    except:
        heightEntryBox.delete(0,last=99999)
        heightEntryBox.insert(0,"Invalid Input")

#draw graph subroutines
def velocityGraph(velocityEntryBox,angleEntryBox,gravityEntryBox,heightEntryBox,circleSizeEntryBox):
    try:
        (velocity,angle,gravity,height,circleSize)=collectValues(velocityEntryBox,angleEntryBox,gravityEntryBox,heightEntryBox,circleSizeEntryBox)
        graph.drawVelocityGraph(velocity,angle,gravity,height)
    except:
        errorMessage(velocityEntryBox,angleEntryBox,gravityEntryBox,heightEntryBox)


def displacementGraph(velocityEntryBox,angleEntryBox,gravityEntryBox,heightEntryBox,circleSizeEntryBox):
    try:
        (velocity,angle,gravity,height,circleSize)=collectValues(velocityEntryBox,angleEntryBox,gravityEntryBox,heightEntryBox,circleSizeEntryBox)
        graph.drawDisplacementGraph(velocity,angle,gravity,height)
    except:
        errorMessage(velocityEntryBox,angleEntryBox,gravityEntryBox,heightEntryBox)


#Load new simulation subroutine
def loadNewSim():
    deleteWids()

    angleEntryBox = Entry(guiCanvas,width=20,validate = "focusout")
    angleEntryBox.insert(0,"45")
    angleEntryBox.grid(row=1,column=1)
    widgets.append(angleEntryBox)

    angleTextBox = Text(guiCanvas, height = 2, width = 30,bg="CYAN",borderwidth=0,font="Roboto")
    angleTextBox.tag_configure("center",justify = "center")
    widgets.append(angleTextBox)
    angleTextBox.insert("1.0","Angle of Launch")
    angleTextBox.tag_add("center","1.0","end")
    angleTextBox.grid(row=0,column=0)


    velocityEntryBox = Entry(guiCanvas,width=20,validate="focusout")
    velocityEntryBox.insert(0,"50")
    velocityEntryBox.grid(row=1,column=3)
    widgets.append(velocityEntryBox)
 
    velocityTextBox = Text(guiCanvas, height = 2, width = 20,bg="CYAN",borderwidth=0,font="Roboto")
    velocityTextBox.tag_configure("center",justify = "center")
    widgets.append(velocityTextBox)
    velocityTextBox.insert("1.0","Initial Velocity (U)(m/s)")
    velocityTextBox.tag_add("center","1.0","end")
    velocityTextBox.grid(row=0,column=4)


    gravityEntryBox = Entry(guiCanvas,width=20,validate="focusout")
    gravityEntryBox.insert(0,"10")
    gravityEntryBox.grid(row=3,column=3)
    widgets.append(gravityEntryBox)

    gravityTextBox = Text(guiCanvas, height = 2, width = 30,bg="CYAN",borderwidth=0,font="Roboto")
    gravityTextBox.tag_configure("center",justify = "center")
    widgets.append(gravityTextBox)
    gravityTextBox.insert("1.0","Acceleration due to gravity (m/s^2)")
    gravityTextBox.tag_add("center","1.0","end")
    gravityTextBox.grid(row=2,column=4)


    heightEntryBox = Entry(guiCanvas,width = 20,validate="focusout")
    heightEntryBox.insert(0,"0")
    heightEntryBox.grid(row=3,column=1)
    widgets.append(heightEntryBox)

    heightTextBox = Text(guiCanvas,height=2,width=30,bg="CYAN",borderwidth=0,font="Roboto")
    heightTextBox.tag_configure("center",justify= "center")
    widgets.append(heightTextBox)
    heightTextBox.insert("1.0","Initial height (m)")
    heightTextBox.tag_add("center","1.0","end")
    heightTextBox.grid(row=2,column=0)


    circleSizeEntryBox = Entry(guiCanvas,width=20,validate="focusout")
    circleSizeEntryBox.insert(0,"20")
    circleSizeEntryBox.grid(row=5,column=1)
    widgets.append(circleSizeEntryBox)

    circleSizeTextBox = Text(guiCanvas,height=2,width=30,bg="CYAN",borderwidth=0,font="Roboto")
    circleSizeTextBox.tag_configure("center",justify = "center")
    widgets.append(circleSizeTextBox)
    circleSizeTextBox.insert("1.0","Radius of projectile (m)")
    circleSizeTextBox.tag_add("center","1.0","end")
    circleSizeTextBox.grid(row=4,column=0)


    velocityGraphBut = Button(guiCanvas,text="Draw Velocity-Time Graph",activebackground="green",height = 2,width=20,command= lambda: velocityGraph(velocityEntryBox,angleEntryBox,gravityEntryBox,heightEntryBox,circleSizeEntryBox))
    velocityGraphBut.grid(row=6,column=2,padx=10)
    widgets.append(velocityGraphBut)

    displacementGraphBut = Button(guiCanvas,text = "Draw Displacement-Time Graph",activebackground="green",height = 2,width = 20,command = lambda: displacementGraph(velocityEntryBox,angleEntryBox,gravityEntryBox,heightEntryBox,circleSizeEntryBox))
    displacementGraphBut.grid(row=7,column=2,padx=10)
    widgets.append(displacementGraphBut)

    saveNameEntryBox = Entry(guiCanvas,width = 20)
    saveNameEntryBox.grid(row=6,column=4)
    widgets.append(saveNameEntryBox)

    saveBut = Button(guiCanvas,text="Save Parameters",activebackground = "green", height = 2,width=20,command = lambda: createSave(velocityEntryBox,angleEntryBox,gravityEntryBox,heightEntryBox,saveNameEntryBox,circleSizeEntryBox))
    saveBut.grid(row=7,column=4)
    widgets.append(saveBut)




    (but1,but2,but3,but4,but5) = (1,1,1,1,1)
    radioButtons = [but1,but2,but3,but4,but5]
    v = IntVar()
    
    guessOptions = ["None","Horizontal displacement (m)","Total displacement (m)","Final vertical velocity (m/s)","Final total velocity (m/s)"]
    for i in range (0,len(radioButtons)):
        radioButtons[i] = Radiobutton(guiCanvas,text = guessOptions[i],variable =v,value = i+1)
        radioButtons[i].grid(row=7+i,column = 1)
        widgets.append(radioButtons[i])
    v.set(1)
    

    guessEntryBox = Entry(guiCanvas,width = 20)
    guessEntryBox.grid(row = 9,column = 0)
    widgets.append(guessEntryBox)

    guessTextBox = Text(guiCanvas,height=2,width=30,bg="CYAN",borderwidth=0,font="Roboto")
    guessTextBox.tag_configure("center",justify = "center")
    widgets.append(guessTextBox)
    guessTextBox.insert("1.0","Which value would you like to guess?")
    guessTextBox.tag_add("center","1.0","end")
    guessTextBox.grid(row=7,column=0)


    runBut=Button(guiCanvas,text="Run Simulation",activebackground="green",height=2,width=20,command= lambda: runSimulation(velocityEntryBox,angleEntryBox,gravityEntryBox,heightEntryBox,circleSizeEntryBox,v,guessEntryBox))
    runBut.grid(row=5,column=2,padx=10)
    widgets.append(runBut)

    menuBut = Button(guiCanvas,text="Back to menu",activebackground="green",height=2,width=20,command = loadMain)
    menuBut.grid(row=0,column=2,padx=10)
    widgets.append(menuBut)

    guiCanvas.pack()

#Delete all buttons subroutine
def deleteWids():
    for widget in widgets:
        widget.grid_remove()
    del widgets[:]

#test stuff
loadMain()
frame.mainloop()
