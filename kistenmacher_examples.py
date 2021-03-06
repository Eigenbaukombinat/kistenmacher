#!/usr/bin/python

## import the dxf library
from dxfwrite import DXFEngine as dxf
import sys
import math

# load library for finger joint boxes
from kistenmacher import kistenmacher




#######################################################################
###                                                                 ###
###  Let the real programme begin!                                  ###
###                                                                 ###
#######################################################################


## create an instance of kistenmacher and set the output filename
km              = kistenmacher("test.dxf")


###################
## EXAMPLE BLOCK ##
###################
## uncomment     ##
##  whatever you ##
##   like!       ##
###################


##
## BEISPIEL: Einfache Fingerzinken-Linie
##
##  Start bei (-600mm,0mm), 5 Finger, in x-Richtung, nicht in y-Richtung,
##    100mm lang, Anfang auszen, kein verkuerzter Anfang, kein verkuerztes Ende
##
if (False):

    ## set parameters for bit diameter and material thickness
    km.bit_diameter = 2
    km.thickness    = 4

    ## draw the line
    km.drawOneSide2(-0,0,5,1,0,100,km.thickness,1,0,0)
    km.drawOneSide2(-0,50,5,-1,0,100,km.thickness,1,0,0)

    ## add description text
    #km.drawing.add(dxf.text("Einfache Linie", (-600,-30), height=10, color='1'))
    #km.drawing.add(dxf.text("100mm / 5 Zinken", (-600,-50), height=10, color='1'))

    km.save()
    sys.exit(0)

##
##  example: box with slip lip
##
if (True):

    ## set kistenmacher parameters
    km.thickness    = 4
    km.bit_diameter = 2
    ## set the number of fingers in each direction
    km.fingers_x   = 3
    km.fingers_y   = 3
    km.fingers_z   = 3

    ## define the size of the box
    length      = 60
    width       = 60
    height      = 40

    ## draw the box at given (x,y)-coordinates with given (length/width/height)
    km.drawBoxV1(-400, 0+height+5*km.bit_diameter, length, width, height)

    ## construct cover lid, slightly larger (by half a millimeter: 0.5mm)
    ## watch out: only one finger for box joint in z-direction because of reduced height
    ## remaining parameters stay the same and are not changes
    km.fingers_z = 1
    km.drawBoxV1(-400, height+length+height+height+8*km.bit_diameter,
                 length + (2 * km.thickness) + 0.5,
                 width  + (2 * km.thickness) + 0.5,
                 float(height)/3 + km.thickness)

    ## add comments in the DXF
    km.drawing.add(dxf.text("box with slip lid",       (-450,-30), height=10, color='1'))
    km.drawing.add(dxf.text("(60x60mm / 68.5x68.5mm)", (-450,-50), height=10, color='1'))



##
## BEISPIEL: BOX with open top and compartment divider: 3 by 2 compartments
##
if (True):

    ## set kistenmacher parameters
    km.thickness    = 4
    km.bit_diameter = 2
    km.fingers_x    = 5
    km.fingers_y    = 3
    km.fingers_z    = 3

    ## define the size
    length = 90
    width  = 60
    height = 30

    km.drawGridInlay(-200,0,length-2*km.thickness,width-2*km.thickness,height-2*km.thickness,3,2)
    km.drawBoxV1(-200, 3*height+10*km.bit_diameter, length, width, height)
    km.drawing.add(dxf.text("Kiste 90x60mm", (-200,-30), height=10, color='1'))
    km.drawing.add(dxf.text("Unterteilung 3x2",  (-200,-50), height=10, color='1'))



##
## BEISPIEL: pen container
##
##    60mm x 60mm base size, 80mm height, compartments: 3x3
##
if (True):
    km.thickness    = 4
    km.bit_diameter = 2
    km.fingers_x    = 3
    km.fingers_y    = 3
    km.fingers_z    = 4

    length = 60
    width  = 60
    height = 80

    ## inlay: subtract twice the thickness from width and length
    ##        subtract bottom thickness from height, and once again for inset effect
    km.drawGridInlay(0,0,length-2*km.thickness,width-2*km.thickness,0.9*height-2*km.thickness,3,3)
    ## draw the box
    km.drawBoxV1(0, 3*height+5*km.bit_diameter, length, width, height)
    ## add description
    km.drawing.add(dxf.text("Stiftehalter mit", (0,-30), height=10, color='1'))
    km.drawing.add(dxf.text("3x3 Unterteilung", (0,-50), height=10, color='1'))



##
## BEISPIEL: big box, top stays open
##
if (True):
    km.thickness    = 6
    km.bit_diameter = 3.175
    km.fingers_x    = 5
    km.fingers_y    = 8
    km.fingers_z    = 4

    length  = 200
    width   = 320
    height  = 80

    km.drawBoxV1(300, height+5*km.bit_diameter, length, width, height)
    km.drawing.add(dxf.text("Riesenkiste 300x200x80mm", (300,-30), height=10, color='1'))


###
### example: closed box with lid
###
if (True):

    km.thickness    = 4
    km.bit_diameter = 2
    km.fingers_x    = 3
    km.fingers_y    = 3
    km.fingers_z    = 4

    length = 60
    width  = 60
    height = 100

    km.drawBoxV2(800, height + 5*km.bit_diameter, length, width, height)
    km.drawing.add(dxf.text("Geschlossene Kiste", (800,-30), height=10, color='1'))


##
## save drawing to dxf and exit
##
km.save()
sys.exit(0)

