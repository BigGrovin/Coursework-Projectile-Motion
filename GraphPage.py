import matplotlib.pyplot as plt
import numpy as np
import math

def drawVelocityGraph(velocity,angle,gravity,height):
    print("it got here")
    initialVerticalVelocity = (velocity * math.sin(angle * 2 * math.pi/360))
    finalVerticalVelocity = -1*(math.sqrt(initialVerticalVelocity**2 + 2 * gravity * height * -1))
    flightTime = (finalVerticalVelocity-initialVerticalVelocity)/gravity
    timeAxis = np.arange(0,flightTime,0.01)
    vertiVelocity = initialVerticalVelocity + gravity*timeAxis
    vertiSpeed = abs(initialVerticalVelocity+gravity*timeAxis)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    plt.plot(timeAxis,vertiVelocity,"b",label = "Vertical Velocity")
    plt.plot(timeAxis,vertiSpeed,"g",label = "Vertical Speed" )
    plt.xlabel("Time (s)")
    plt.ylabel("ms^-1")
    plt.legend()
    plt.show()

def drawDisplacementGraph(velocity,angle,gravity,height):
    initialVerticalVelocity = (velocity * math.sin(angle * 2 * math.pi/360))
    initialHorizontalVelocity = (velocity * math.cos(angle * 2 * math.pi/360))
    finalVerticalVelocity = -1*(math.sqrt(initialVerticalVelocity**2 + 2 * gravity * height * -1))
    flightTime = (finalVerticalVelocity-initialVerticalVelocity)/gravity
    timeAxis = np.arange(0,flightTime,0.01)
    horiDisplacement = initialHorizontalVelocity * timeAxis
    vertiDisplacement = initialVerticalVelocity * timeAxis + 0.5*gravity*timeAxis**2
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    plt.plot(timeAxis,horiDisplacement,color ="g", label = "Horizontal Displacement")
    plt.plot(timeAxis,vertiDisplacement,color= "b",label = "Vertical Displacement")
    plt.xlabel("Time (s)")
    plt.ylabel("(m)")
    plt.legend()
    plt.show()