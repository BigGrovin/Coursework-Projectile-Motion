#imports
from functools import partial
from tkinter import *
import Main as main
import pygame
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math
import GraphPage as graph
from Main import Projectile
import json as jason
import tkinter.ttk as ttk

#globals
global validFloat


#performs a check each time the user tries to enter a value in an entry box
#only allows numbers and decimals to be entered
def entryCheck(entry):
    if entry == "":
        return True
    try:
        float(entry)
    except:
        return False
    else: 
        return True


#create save subroutine
########## GROUP A - File organised for firect access ##########
def createSave(velocityEntryBox,angleEntryBox,gravityEntryBox,heightEntryBox,saveNameEntryBox,circleSizeEntryBox):
    try:
        (velocity,angle,gravity,height,circleSize)=collectValues(velocityEntryBox,angleEntryBox,gravityEntryBox,heightEntryBox,circleSizeEntryBox)
        name = saveNameEntryBox.get()
        if name != "":
            ########### GROUP B - Dictionaries ##########
            savesDict = {       #puts all the paramters the user has entered into a dictionary so that they can be handled more easily
                "name" : name,
                "initial velocity" : velocity,
                "initial angle" : angle,
                "gravity" : gravity,
                "initial height" : height,
                "circle size" : circleSize
            }
            with open("saves.json","r")as saveFile: #opens the save file in read mode
                try:
                    data = jason.load(saveFile) #tries to put the save file in a list
                except:
                    data = [] #if it can't, it means the save file is empty, and so a new, blank list is created
                    pass
                data.append(savesDict) #new save parameters added to the list
            with open("saves.json","w")as saveFile: #opens the save file in write mode
                jason.dump(data, saveFile, indent=2) #rewrites all the data from the list into the json save file
            if len(widgets) > 26:
                widgets.pop(-1).grid_remove() #removes the error messag for there not being a save name, if there was one on screen
        else:
            if len(widgets) < 27: #makes error message appear if no save name entered
                nameErrorTextBox = Text(guiCanvas, height = 1, width = 20,bg = "light grey",borderwidth=0,font="Roboto")
                nameErrorTextBox.tag_configure("center",justify = "center")
                widgets.append(nameErrorTextBox)
                nameErrorTextBox.insert("1.0","ERROR! Invalid Name")
                nameErrorTextBox.tag_add("center","1.0","end")
                nameErrorTextBox.grid(row=8,column=4)
                nameErrorTextBox.config(state=DISABLED)
    except:
        errorMessage(velocityEntryBox,angleEntryBox,gravityEntryBox,heightEntryBox,circleSizeEntryBox) #if there were any invalid values in the entry box then nothing is saved and the values are replaced by default

#list of widgets
#used to store all the widgets currently on the screen, used to delete them so new ones can be drawn
widgets = []

#Create the main frame
frame = Tk()
frame.geometry("1400x800")
frame.resizable(False,False)

validFloat = frame.register(entryCheck) #variable used to check the entry values

#Create the canvas
guiCanvas = Canvas(frame,bg ="light grey",height="800",width="1400")


#Load MainMenu subroutine
def loadMain():
    deleteWids() #deletes all the existing widgets on the screen
    newSimBut = Button(guiCanvas,text="Create New Simulation",activebackground="light green",height=7,width=20, command = loadNewSim) #creates the button which calls loadNewSim
    savedSimsBut = Button(guiCanvas,text="Saved Simulations",activebackground="light green",height=7,width=20, command = loadSavedSim) #creates the button which calls loadSavedSim
    widgets.append(newSimBut) #adds the widgets to the widgets list to be deleted later
    widgets.append(savedSimsBut)
    newSimBut.grid(row=1,column=1,padx=20,pady=20)
    savedSimsBut.grid(row=1,column=3,padx=20,pady=20)
    guiCanvas.pack()


#subroutine to collect all the calues from the  entry boxes
def collectValues(velocityEntryBox,angleEntryBox,gravityEntryBox,heightEntryBox,circleSizeEntryBox):
    velocity = float((velocityEntryBox.get())) #grabs all the values and converts them to floats as they are strings initially
    angle = float((angleEntryBox.get())) 
    gravity = (float(gravityEntryBox.get()))*-1
    height = float((heightEntryBox.get()))
    circleSize = float((circleSizeEntryBox.get()))
    return (velocity,angle,gravity,height,circleSize)



#subroutine to run begin running the simulation
def runSimulation(velocityEntryBox,angleEntryBox,gravityEntryBox,heightEntryBox,circleSizeEntryBox,v,guessEntryBox):
    try:
        whichGuess = v.get() #gets the users guess value
        try:
            guess = round(float(guessEntryBox.get()),1) #rounds their value to 1dp
        except:
            guess = 0 #if the guess is a word or something else then guess is entered as 0
        (velocity,angle,gravity,height,circleSize)=collectValues(velocityEntryBox,angleEntryBox,gravityEntryBox,heightEntryBox,circleSizeEntryBox) #calls the collect values subroutine so that the values can be stored as variables and used
        main.runItAll(guess,velocity,angle,whichGuess,circleSize,gravity,height) #calls the run it all subroutine, this opens a pygame window and uses the parameters collected to run the simulation
    except:
        errorMessage(velocityEntryBox,angleEntryBox,gravityEntryBox,heightEntryBox,circleSizeEntryBox) #calls error message subroutine in case of any values being invalid



#display error in input boxes if invalid entry
#checks each entry individually to ensure that it can be converted to float
#if it can't then whatever invalid data the user has entered is replaced by the default value
def errorMessage(velocityEntryBox,angleEntryBox,gravityEntryBox,heightEntryBox,circleSizeEntryBox):
    try:
        numCheck = float(velocityEntryBox.get())
    except:
        velocityEntryBox.delete(0,last=99999)
        velocityEntryBox.insert(0,"100")
    try:
        numCheck = float(angleEntryBox.get())
    except:
        angleEntryBox.delete(0,last=99999)
        angleEntryBox.insert(0,"45")
    try:
        numCheck = float(gravityEntryBox.get())
    except:
        gravityEntryBox.delete(0,last=99999)
        gravityEntryBox.insert(0,"10")
    try:
        numCheck = float(heightEntryBox.get())
    except:
        heightEntryBox.delete(0,last=99999)
        heightEntryBox.insert(0,"0")
    try:
        numCheck = float(circleSizeEntryBox.get())
    except:
        circleSizeEntryBox.delete(0,last=99999)
        circleSizeEntryBox.insert(0,"20")

#draw graph subroutines
def velocityGraph(velocityEntryBox,angleEntryBox,gravityEntryBox,heightEntryBox,circleSizeEntryBox): #calls subroutines to collect values and draw a graph
    try:
        (velocity,angle,gravity,height,circleSize)=collectValues(velocityEntryBox,angleEntryBox,gravityEntryBox,heightEntryBox,circleSizeEntryBox)
        graph.drawVelocityGraph(velocity,angle,gravity,height) #draws a graph of velocity against time with the paramters collected from the entry boxes
    except:
        errorMessage(velocityEntryBox,angleEntryBox,gravityEntryBox,heightEntryBox)


def displacementGraph(velocityEntryBox,angleEntryBox,gravityEntryBox,heightEntryBox,circleSizeEntryBox): #calls subroutines to collect values and draw a graph
    try:
        (velocity,angle,gravity,height,circleSize)=collectValues(velocityEntryBox,angleEntryBox,gravityEntryBox,heightEntryBox,circleSizeEntryBox)
        graph.drawDisplacementGraph(velocity,angle,gravity,height) #draws a graph of displacement against time with the parameers collected from the entry boxes
    except:
        errorMessage(velocityEntryBox,angleEntryBox,gravityEntryBox,heightEntryBox)


#Load new simulation subroutine
def loadNewSim():
    deleteWids()
#creates all the buttons and entry boxes
#puts each of them in a grid, all with the same font
    angleEntryBox = Entry(guiCanvas,width=20,validate = "key", validatecommand = (validFloat,"%P"))
    angleEntryBox.insert(0,"45")
    angleEntryBox.grid(row=1,column=1)
    widgets.append(angleEntryBox)

    angleTextBox = Text(guiCanvas, height = 2, width = 30,bg = "light grey",borderwidth=0,font="Roboto")
    angleTextBox.tag_configure("center",justify = "center")
    widgets.append(angleTextBox)
    angleTextBox.insert("1.0","Angle of Launch")
    angleTextBox.tag_add("center","1.0","end")
    angleTextBox.grid(row=1,column=0)
    angleTextBox.config(state=DISABLED)


    velocityEntryBox = Entry(guiCanvas,width=20,validate="key", validatecommand = (validFloat,"%P"))
    velocityEntryBox.insert(0,"100")
    velocityEntryBox.grid(row=1,column=3)
    widgets.append(velocityEntryBox)
 
    velocityTextBox = Text(guiCanvas, height = 2, width = 20,bg = "light grey",borderwidth=0,font="Roboto")
    velocityTextBox.tag_configure("center",justify = "center")
    widgets.append(velocityTextBox)
    velocityTextBox.insert("1.0","Initial Velocity (U)(m/s)")
    velocityTextBox.tag_add("center","1.0","end")
    velocityTextBox.grid(row=1,column=4)
    velocityTextBox.config(state=DISABLED)


    gravityEntryBox = Entry(guiCanvas,width=20,validate="key", validatecommand = (validFloat,"%P"))
    gravityEntryBox.insert(0,"10")
    gravityEntryBox.grid(row=3,column=3)
    widgets.append(gravityEntryBox)

    gravityTextBox = Text(guiCanvas, height = 2, width = 30,bg = "light grey",borderwidth=0,font="Roboto")
    gravityTextBox.tag_configure("center",justify = "center")
    widgets.append(gravityTextBox)
    gravityTextBox.insert("1.0","Acceleration due to gravity (m/s^2)")
    gravityTextBox.tag_add("center","1.0","end")
    gravityTextBox.grid(row=3,column=4)
    gravityTextBox.config(state=DISABLED)


    heightEntryBox = Entry(guiCanvas,width = 20,validate="key", validatecommand = (validFloat,"%P"))
    heightEntryBox.insert(0,"0")
    heightEntryBox.grid(row=3,column=1)
    widgets.append(heightEntryBox)

    heightTextBox = Text(guiCanvas,height=2,width=30,bg = "light grey",borderwidth=0,font="Roboto")
    heightTextBox.tag_configure("center",justify= "center")
    widgets.append(heightTextBox)
    heightTextBox.insert("1.0","Initial height (m)")
    heightTextBox.tag_add("center","1.0","end")
    heightTextBox.grid(row=3,column=0)
    heightTextBox.config(state=DISABLED)


    circleSizeEntryBox = Entry(guiCanvas,width=20,validate="key", validatecommand = (validFloat,"%P"))
    circleSizeEntryBox.insert(0,"20")
    circleSizeEntryBox.grid(row=5,column=1)
    widgets.append(circleSizeEntryBox)

    circleSizeTextBox = Text(guiCanvas,height=2,width=30,bg = "light grey",borderwidth=0,font="Roboto")
    circleSizeTextBox.tag_configure("center",justify = "center")
    widgets.append(circleSizeTextBox)
    circleSizeTextBox.insert("1.0","Radius of projectile (m)")
    circleSizeTextBox.tag_add("center","1.0","end")
    circleSizeTextBox.grid(row=5,column=0)
    circleSizeTextBox.config(state=DISABLED)


    massEntryBox = Entry(guiCanvas,width=20)
    massEntryBox.insert(0,"20")
    massEntryBox.grid(row=5,column=3)
    widgets.append(massEntryBox)

    massTextBox = Text(guiCanvas,height=2,width=30,bg = "light grey",borderwidth=0,font="Roboto")
    massTextBox.tag_configure("center",justify = "center")
    widgets.append(massTextBox)
    massTextBox.insert("1.0","Mass of projectile (Kg)")
    massTextBox.tag_add("center","1.0","end")
    massTextBox.grid(row=5,column=4)
    massTextBox.config(state=DISABLED)

    #button to call the drawVelocityGraph function
    velocityGraphBut = Button(guiCanvas,text="Draw Velocity-Time Graph",activebackground="light green",height = 2,width=25,command= lambda: velocityGraph(velocityEntryBox,angleEntryBox,gravityEntryBox,heightEntryBox,circleSizeEntryBox))
    velocityGraphBut.grid(row=6,column=2,padx=10)
    widgets.append(velocityGraphBut)

    #button to call the drawDisplacementGraph function
    displacementGraphBut = Button(guiCanvas,text = "Draw Displacement-Time Graph",activebackground="light green",height = 2,width = 25,command = lambda: displacementGraph(velocityEntryBox,angleEntryBox,gravityEntryBox,heightEntryBox,circleSizeEntryBox))
    displacementGraphBut.grid(row=7,column=2,padx=10)
    widgets.append(displacementGraphBut)

    saveTextBox = Text(guiCanvas,height = 2, width = 25, bg = "light grey", borderwidth = 0, font = "Roboto")
    saveTextBox.tag_configure("center",justify = "center")
    widgets.append(saveTextBox)
    saveTextBox.insert("1.0","Enter a save name to save")
    saveTextBox.tag_add("center","1.0","end")
    saveTextBox.grid(row=9,column=4)
    saveTextBox.config(state=DISABLED)

    saveNameEntryBox = Entry(guiCanvas,width = 20)
    saveNameEntryBox.grid(row=10,column=4)
    widgets.append(saveNameEntryBox)

    #button to call the save function to save the current parameters
    saveBut = Button(guiCanvas,text="Save Parameters",activebackground = "light green", height = 2,width=20,command = lambda: createSave(velocityEntryBox,angleEntryBox,gravityEntryBox,heightEntryBox,saveNameEntryBox,circleSizeEntryBox))
    saveBut.grid(row=11,column=4)
    widgets.append(saveBut)



    #defines the 5 radio buttons
    (but1,but2,but3,but4,but5) = (1,1,1,1,1)
    radioButtons = [but1,but2,but3,but4,but5]
    v = IntVar()
    
    #creates the list of different values the user can guess
    #puts each value in the list as a radio button
    #places them in the grid
    guessOptions = ["None","Horizontal displacement (m)","Total displacement (m)","Final vertical velocity (m/s)","Final total velocity (m/s)"]
    for i in range (0,len(radioButtons)):
        radioButtons[i] = Radiobutton(guiCanvas,text = guessOptions[i],variable =v,value = i+1)
        radioButtons[i].grid(row=7+i,column = 1)
        widgets.append(radioButtons[i])
    v.set(1)
    

    guessEntryBox = Entry(guiCanvas,width = 20) #creates an entry for the user to enter their guess value and places it in the grid
    guessEntryBox.grid(row = 9,column = 0)
    widgets.append(guessEntryBox)

    guessTextBox = Text(guiCanvas,height=2,width=30,bg = "light grey",borderwidth=0,font="Roboto") #creates the corresponding text box to inform the user
    guessTextBox.tag_configure("center",justify = "center")
    widgets.append(guessTextBox)
    guessTextBox.insert("1.0","Which value would you like to guess?")
    guessTextBox.tag_add("center","1.0","end")
    guessTextBox.grid(row=7,column=0)
    guessTextBox.config(state=DISABLED)

    #button to call the runSimulationfunction to run the simulation with the current paramteters that have been entered
    runBut=Button(guiCanvas,text="Run Simulation",activebackground="light green",height=2,width=25,command= lambda: runSimulation(velocityEntryBox,angleEntryBox,gravityEntryBox,heightEntryBox,circleSizeEntryBox,v,guessEntryBox))
    runBut.grid(row=5,column=2,padx=10)
    widgets.append(runBut)

    #button to return the user to the main menu (calls the loadMain function)
    menuBut = Button(guiCanvas,text="Back to menu",activebackground="light green",height=2,width=25,command = loadMain)
    menuBut.grid(row=0,column=2,padx=10)
    widgets.append(menuBut)

    guiCanvas.pack() #updates the canvas


#load a saved simualtion menu
def loadSavedSim():
    deleteWids()
    with open("saves.json","r")as saveFile: #opens the json file "saves"
        try:
            data = jason.load(saveFile) #puts the data from the json file into a list for easier use
        except:
            data = [] #error checks
    saveOptions = [d["name"]for d in data]

    #creates option box so the user can choose a save to run
    saveChoiceValue = StringVar()
    saveChoiceDropDown = ttk.Combobox(guiCanvas,values = saveOptions, state = "readonly", textvariable = saveChoiceValue, font = "Roboto")
    saveChoiceDropDown.grid(row = 1,column = 1)
    widgets.append(saveChoiceDropDown)

    #button that calls the loadMain subroutine
    menuBut = Button(guiCanvas,text="Back to menu",activebackground="light green",height=2,width=33,command = loadMain)
    menuBut.grid(row=0,column=1,padx=10,pady=10)
    widgets.append(menuBut)

    #button that calls the runSimulation subroutine
    runBut = Button(guiCanvas,text = "Run saved simulation",activebackground = "light green",height = 2, width = 33,command = partial(runSavedSim,saveChoiceValue))
    runBut.grid(row = 2,column = 1,padx=10,pady=10)
    widgets.append(runBut)

def runSavedSim(saveName):
    saveName = saveName.get()
    with open("saves.json","r") as saveFile:
        data = jason.load(saveFile)
        saveValues = next((item for item in data if item["name"] == saveName), None)
        (name,velocity,angle,gravity,height,circleSize) = saveValues.values()
        main.runItAll(1,velocity,angle,1,circleSize,gravity,height)
    

#Delete all buttons subroutine
def deleteWids():
    for widget in widgets:
        widget.grid_remove() #removes each widget in te list widgets (all of the ones on screen)
    del widgets[:]

loadMain()
frame.mainloop()
