import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as widgets
import sys

sys.path.insert(1,"C:\\python")
import y2daq

#code uses term buggy as motor was previously part of buggy experiment

# Create analog daq object with input channel 0, output channel 0
a=y2daq.analog()
a.reset()
a.addInput(0)
a.addOutput(0)
a.Nscans = 2
a.Rate = 1



def move_buggy():
    I = np.array([])
    x = -1
    
    while start_buggy == 'True':
        

        # choose required output depending on status of radio buttons
        if radioHandle.value_selected == 'forward':
            y = np.array([48, 96, 192, 144],dtype=np.uint8)
        elif radioHandle.value_selected == 'backward':
            y = np.array([144, 192, 96, 48,],dtype=np.uint8)
#             move the motor four steps
        #data,timestamps = a.read()
        for i in range(4):
#            data,timestamps = a.read()
            dio.write(np.unpackbits(y[i]))
            # digital output
            plt.pause(0.1) # wait for motor to move
            data,timestamps = a.read()
            plt.pause(0.1)
            newX = x + 1
            I = np.append(I,data[0])
            x = newX
            np.savetxt('I.txt', I)

            
            
def startCallback(event):
    global start_buggy
    start_buggy = 'True'
    move_buggy()
    
def stopCallback(event):
    global start_buggy
    start_buggy = 'False'
    
def closeCallback(event):
    dio.clear()
    dio.__end__()
    plt.close('all') #close all open figure windows
    
# Create digital output object
dio=y2daq.digital()
# Set up the user interface
fig=plt.figure(figsize=(3,3))
# Radio buttons control the direction of the buggy
rax=plt.axes([0.2,0.4,0.6,0.3])
radioHandle=widgets.RadioButtons(rax,('forward','backward'),active=0)
# Button to start the buggy
startax=plt.axes([0.2,0.28,0.25,0.1])
startHandle=widgets.Button(startax,'Start')
startHandle.on_clicked(startCallback)
# Button to stop the buggy
stopax=plt.axes([0.55,0.28,0.25,0.1])
stopHandle=widgets.Button(stopax,'Stop')
stopHandle.on_clicked(stopCallback)
# Button to close the GUI
bax=plt.axes([0.4,0.75,0.2,0.1])
closeHandle=widgets.Button(bax,'Close')
closeHandle.on_clicked(closeCallback)


