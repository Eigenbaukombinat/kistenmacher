from dxfwrite import DXFEngine as dxf
import math


class kistenmacher(object):

    ## set variables with their default values
    bit_diameter = 2
    thickness    = 4
    fingers_x    = 3
    fingers_y    = 3
    fingers_z    = 3

    ## constructor
    def __init__(self, filename):

        ## open new drawing under given filename
        self.drawing = dxf.drawing(filename)

        #self.drawRectangle(0,0,100,100)

    ## save the drawing dxf file
    def save(self):
        self.drawing.save()

    ## close the file
    def close(self):
        self.drawing.save()


    ##
    ## draw a finger joint line with given parameters
    ##
    def drawOneSide2(self, cx, cy, nf, dirx, diry, size, thickness, starthigh, beginshort, endshort):

        ## copy class parameters
        bit_diameter = self.bit_diameter
        drawing      = self.drawing

        ## for all fingers to generate...
        for i in range(0 , int(nf)):

            ## calculate finger width;
            finger_size =  float(size) / int(nf)

            ## alternate in/out finger with regards to starthigh
            cx +=  diry*thickness*((starthigh+i)%2==0)- thickness*diry*((starthigh+i)%2!=0)
            cy +=  dirx*thickness*((starthigh+i)%2==0)- thickness*dirx*((starthigh+i)%2!=0)

            ## draw the finger-line and upd position
            ##                     start +                 shorten start/end by bit_diameter if we are inside          start + finger size
            drawing.add(dxf.line( (cx                      + dirx*math.sqrt(2)/2*bit_diameter*((starthigh+i)%2==0)   , cy                    ),
                                  (cx + (finger_size*dirx) - dirx*math.sqrt(2)/2*bit_diameter*((starthigh+i)%2==0)   , cy + (finger_size*diry) )  ))
            cx += (finger_size*dirx)
            cy += (finger_size*diry)



            ## circle in ze edge!!                    start + thickness in correct direction if in + push a little to position
            ## only if not the last one and we start with high
            if i<nf-1 and starthigh:
                drawing.add(dxf.arc(float(bit_diameter)/2, (cx + thickness*diry*((starthigh+i)%2!=0) + dirx*math.sqrt(2)/4*(bit_diameter)*((starthigh+i)%2!=0) - dirx*math.sqrt(2)/4*(bit_diameter)*((starthigh+i)%2==0),
                                                            cy + thickness*dirx*((starthigh+i)%2!=0) - dirx*math.sqrt(2)/4*(bit_diameter)),
                                                            45-dirx*90*((starthigh+i)%2==0), 225-dirx*90*((starthigh+i)%2==0)))



            ## skip line in/out on last line
            if i < nf-1:
                ## draw the line in or out
                ##                     start  -  down                               + up                                   - dog-ear shortens line for going from in to out
                drawing.add(dxf.line( (cx, cy                                                                              -  dirx*math.sqrt(2)/2*bit_diameter*((starthigh+i)%2==0) ), #  - dirx*math.sqrt(2)/2*bit_diameter*(starthigh%2==0) ) ,
                                      (cx, cy - thickness*dirx*((starthigh+i)%2==0) + thickness*dirx*((starthigh+i)%2!=0)  -  dirx*math.sqrt(2)/2*bit_diameter*((starthigh+i)%2!=0) ) ))

#            drawing.add(dxf.arc(float(bit_diameter)/2, (cx + math.sqrt(2)/2*float(bit_diameter)/2*dirx + math.sqrt(2)/2*float(bit_diameter)/2*diry,
#                                                        cy + math.sqrt(2)/2*float(bit_diameter)/2*diry - math.sqrt(2)/2*float(bit_diameter)/2*dirx), arc_from, arc_to))



#            if (i > 0 and i < nf - 1) :
#                pass



    ##
    ## draw a finger joint line with given parameters
    ##
    def drawOneSide(self, cx, cy, nf, dirx, diry, size, thickness, starthigh, beginshort, endshort):
        # cx        ... start in x direction
        # cy        ... start in y direction
        # nf        ... number of fingers
        # dirx      ... direction in x, [ -1, 0, 1 ]
        # diry      ... direction in y, [ -1, 0, 1 ]
        # size      ... run-length of the finger joint line

        ## copy class parameters
        bit_diameter = self.bit_diameter
        drawing      = self.drawing

        ## left of direction in x-dimension is INSIDE of the part
        ## left of direction in y-dimension is INSIDE of the part

        # 1 .. normal into workpiece
        # 2 .. normal into fingers
        # 3 .. diagonal
        dog_ears = 1

        ## remember which direction to go for the finger insets
        ##     starthigh --> out    --> -1
        ## not starthigh --> inside -->  1
        if starthigh == True:
            in_or_out = -1
        else:
            in_or_out = 1

        #old dog ears
        if(dog_ears == 1):
            # determine our direction and set the half-circle arc for the dog-ears
            if   dirx == 1:
                 arc_from    = 0
                 arc_to      = 180
            elif dirx == -1:
                 arc_from    = 180
                 arc_to      = 0
            elif diry == -1:
                 arc_from    = 270
                 arc_to      = 90
            elif diry == 1:
                 arc_from    = 90
                 arc_to      = 270
            else:
                 arc_from    = 0
                 arc_to      = 0


        #diagonal dog-ears
        if(dog_ears == 3):
            # determine our direction and set the half-circle arc for the dog-ears
            if   dirx == 1:
                 arc_from    = 45
                 arc_to      = 225
            elif dirx == -1:
                 arc_from    = 225
                 arc_to      = 45
            elif diry == -1:
                 arc_from    = 315
                 arc_to      = 135
            elif diry == 1:
                 arc_from    = 135
                 arc_to      = 315
            else:
                 arc_from    = 0
                 arc_to      = 0


        ## for all fingers to generate...
        for i in range(0 , int(nf)):

            ## calculate finger width; we do it here instead of outside the for-loop,
            ## because sometimes we will have to adjust it, but need the full value
            ## again in the next iteration
            finger_size =  float(size) / int(nf)

            ## if we start (i==0) with a short piece (parameter beginshort):
            if beginshort and i == 0:
                ## adjust current position accordingly
                cx += abs(thickness) * (dirx)
                cy += abs(thickness) * (diry)
                ## shorten the finger_size temporarily by the same amount
                finger_size -= abs(thickness)

            ## are we in the last iteration?
            if endshort and i == nf-1:
                ## shorten the finger_size temporarily by the same amount
                finger_size -= abs(thickness)

            ## starthigh correction:
            ##  if we start low/inset finger correct the x/y position accordingly
            if not starthigh and i == 0:
                cx += abs(thickness) * (-diry) * in_or_out
                cy += abs(thickness) * ( dirx) * in_or_out


            ## bit_diameter defined && we are drawing INside
            if bit_diameter > 0 and in_or_out == 1:
                ## draw this arc only if this is not the first finger...
                if i > 0:
                    ##          dxf.arc( diameter , ( x , y ) , arc_from, arc_to )
                    # dog ear 1
                    if(dog_ears == 1):
                        drawing.add(dxf.arc(float(bit_diameter)/2, (cx + float(bit_diameter)/2*dirx ,
                                                                    cy + float(bit_diameter)/2*diry), arc_from, arc_to))

                    ## dogear diagonal
                    if(dog_ears == 3):
                        drawing.add(dxf.arc(float(bit_diameter)/2, (cx + math.sqrt(2)/2*float(bit_diameter)/2*dirx + math.sqrt(2)/2*float(bit_diameter)/2*diry,
                                                                    cy + math.sqrt(2)/2*float(bit_diameter)/2*diry - math.sqrt(2)/2*float(bit_diameter)/2*dirx), arc_from, arc_to))

                    ## increase the cursor position
                    if(dog_ears == 1):
                        cx += bit_diameter * dirx
                        cy += bit_diameter * diry

                    ## diagonal
                    if(dog_ears == 3):
                        cx += math.sqrt(2)*float(bit_diameter)/2 * dirx
                        cy += math.sqrt(2)*float(bit_diameter)/2 * diry

                    ## shorten the length of the following finger accordingly
                    finger_size -= bit_diameter
                    #finger_size -= math.sqrt(2)*float(bit_diameter) ##bit_diameter##

                ## draw this arc only if this is not the last finger...
                if i < nf - 1:
                # old dog-ears
                    if(dog_ears == 1):
                        drawing.add(dxf.arc(float(bit_diameter)/2, (cx-float(bit_diameter)/2*dirx+finger_size*dirx,cy-float(bit_diameter)/2*diry+finger_size*diry), arc_from, arc_to))
                    if(dog_ears == 3):
                        drawing.add(dxf.arc(float(bit_diameter)/2, (cx - math.sqrt(2)/2*float(bit_diameter)/2*dirx + math.sqrt(2)/2*float(bit_diameter)/2*diry +finger_size*dirx,
                                                                    cy - math.sqrt(2)/2*float(bit_diameter)/2*diry - math.sqrt(2)/2*float(bit_diameter)/2*dirx +finger_size*diry), arc_from-90, arc_to-90))

                    ## shorten length of finger accordingly
                    # old dog-ears
                    finger_size -= bit_diameter#
                    #finger_size -= math.sqrt(2)*float(bit_diameter) ##bit_diameter##

            ## draw the finger line, depending on x or y direction and length
            drawing.add(dxf.line((cx, cy), (cx+finger_size*dirx, cy+finger_size*diry)))

            ## increase the cursor position after drawing the finger
            cx += (finger_size ) * dirx
            cy += (finger_size ) * diry

            ## if we have drawn a second dog-ear, add it to the cursor position
            if bit_diameter > 0 and in_or_out == 1 and i < nf - 1:
                cx += bit_diameter*dirx
                cy += bit_diameter*diry


            ## skip if end already reached
            if not (i == nf-1):
                ## draw one line of material thickness inwards/outwards
                drawing.add(dxf.line( (cx, cy), (cx-abs(thickness)*(-diry)*in_or_out, cy-abs(thickness)*(dirx)*in_or_out)))
                ## adjust current position accordingly
                cx-=abs(thickness)*(-diry)*in_or_out
                cy-=abs(thickness)*( dirx)*in_or_out
                in_or_out *= -1



    ##
    ##
    ##  drawGridPart .. draws a single grid part with defined number of compartments etc.pp.
    ##
    ##      cx                      .. start in x
    ##      cy                      .. start in y
    ##      x                       .. length
    ##      z                       .. height
    ##      number_of_compartments  .. number of compartments
    ##
    def drawGridPart(self,start_x,start_y, x,z, number_of_compartments):

        ## copy class parameters
        thickness    = self.thickness
        bit_diameter = self.bit_diameter
        drawing      = self.drawing


        ## calculate finger lengths
        ##  length of divider - ((number of divisions - 1) * thickness of the material) / number of divisions
        length_of_division = float(x - (number_of_compartments-1) * thickness) / number_of_compartments

        ## draw the lower line with interruptions
        ##   the same has to be applied for the other direction
        for j in range(0, number_of_compartments - 1):

            ## first dog-ears-variant: draw them to the top
            if (False):
               ## draw the finger line, depending on x or y direction and length
                drawing.add(dxf.line((start_x, start_y), (start_x+length_of_division, start_y)));     start_x += length_of_division
                drawing.add(dxf.line((start_x, start_y), (start_x, start_y+float(z)/2)));   start_y += float(z)/2
                ## add the dog-ears here!
                drawing.add(dxf.arc(float(bit_diameter)/2, (start_x+float(bit_diameter)/2,start_y), 0,180))
                drawing.add(dxf.arc(float(bit_diameter)/2, (start_x+thickness-float(bit_diameter)/2,start_y), 0,180))
                ## skip connection line, if thickness not large enough (eliminate dots)
                if thickness > 2*bit_diameter:
                    drawing.add(dxf.line((start_x+bit_diameter, start_y), (start_x+thickness-bit_diameter, start_y)));
                ## but continue anyway
                start_x += thickness
                drawing.add(dxf.line((start_x, start_y), (start_x, start_y-float(z)/2)));   start_y -= float(z)/2

            ## second dog-ears-variant: draw them to the side
            if (False):
               ## draw the finger line, depending on x or y direction and length
                drawing.add(dxf.line((start_x, start_y), (start_x+length_of_division, start_y)));     start_x += length_of_division
                drawing.add(dxf.line((start_x, start_y), (start_x, start_y+float(z)/2-bit_diameter)));   start_y += float(z)/2
                ## add the dog-ears here!
                drawing.add(dxf.arc(float(bit_diameter)/2, (start_x, start_y-float(bit_diameter)/2), 90,270))
                drawing.add(dxf.arc(float(bit_diameter)/2, (start_x+thickness,start_y-float(bit_diameter)/2), 270,90))
                drawing.add(dxf.line((start_x, start_y), (start_x+thickness, start_y)));
                ## but continue anyway
                start_x += thickness
                drawing.add(dxf.line((start_x, start_y-bit_diameter), (start_x, start_y-float(z)/2)));   start_y -= float(z)/2


            ### draw diagonal dog-ears
            if (True):
                ## draw the finger line, depending on x or y direction and length
                drawing.add(dxf.line((start_x, start_y), (start_x+length_of_division, start_y)));     start_x += length_of_division
                # shorten up-line by dog-ear
                drawing.add(dxf.line((start_x, start_y), (start_x, start_y+float(z)/2-math.sqrt(2)/2*bit_diameter)));   start_y += float(z)/2
                # draw diagonal dog ears
                drawing.add(dxf.arc(float(bit_diameter)/2, (start_x+math.sqrt(2)/4*bit_diameter, start_y-math.sqrt(2)/4*bit_diameter), 45,225))
                drawing.add(dxf.arc(float(bit_diameter)/2, (start_x+thickness-math.sqrt(2)/4*bit_diameter, start_y-math.sqrt(2)/4*bit_diameter), 315,135))
                # draw dog-ear-connection line + add thickness to position of cursor_x
                drawing.add(dxf.line((start_x+math.sqrt(2)/2*bit_diameter, start_y), (start_x+thickness-math.sqrt(2)/2*bit_diameter, start_y)));
                start_x += thickness
                # draw a line downwards
                drawing.add(dxf.line((start_x, start_y-math.sqrt(2)/2*bit_diameter), (start_x, start_y-float(z)/2)));   start_y -= float(z)/2

        ## draw last line to the right
        drawing.add(dxf.line((start_x, start_y), (start_x+length_of_division, start_y)));     start_x += length_of_division
        ## draw line up
        drawing.add(dxf.line((start_x, start_y), (start_x, start_y + z)));          start_y += z
    # replace above line with this to create outer edge
    #    drawOneSide(start_x+thickness,start_y,2,0,1,z,thickness,0,0,0);  start_y+=z

        ## draw long line to-the-left
        drawing.add(dxf.line((start_x, start_y), (start_x-x, start_y)));            start_x -= x
        ## draw final down line
        drawing.add(dxf.line((start_x, start_y), (start_x, start_y - z)));          start_y -= z
    # replace above line with this to create outer edge
    #    drawOneSide(start_x-thickness,start_y,2,0,-1,z,thickness,1,0,0)



    ###
    ### drawGrid
    ###
    def drawGridInlay(self, start_x, start_y, x, y, z, number_of_compartments_x, number_of_compartments_y):

        ## copy class parameters
        thickness    = self.thickness
        bit_diameter = self.bit_diameter

        ## set start coordinates
#        cx = start_x
#        cy = start_y

        ## draw (number_of_compartments_y - 1) many x-dividers
        ##   there are (number_of_compartments_y) compartments in y direction
        ##   and therefore (number_of_compartments_y-1) divisions in x-direction
        for i in range(0, number_of_compartments_y - 1 ):
            ## draw a grid part with length=x an height=z for number_of_compartments_x
            self.drawGridPart(start_x + i*(x+5*bit_diameter), start_y, x, z, number_of_compartments_x)
            ## set the new start point for the next element
            #cx += x + 5*bit_diameter

        ## set new (cx, cy) start point for the other elements
#        cx = start_x
#        cy += z + 5* bit_diameter;

        ## draw (number_of_compartments_x - 1) many y-dividers
        for i in range(0, number_of_compartments_x - 1 ):

            ## draw a grid part with length=y an height=z for number_of_compartments_y
            ## on slightly elevated y-position, so there is no collision
            self.drawGridPart(start_x + i*(y+5*bit_diameter), z + 5* bit_diameter, y, z, number_of_compartments_y)
            ## set new start point for next element
            #cx += y + 5*bit_diameter


    ### draw closed box with all six parts
    def drawBoxV2(self, sx, sy, x, y, z):

        fingers_x    = self.fingers_x
        fingers_y    = self.fingers_y
        fingers_z    = self.fingers_z
        bit_diameter = self.bit_diameter

        # bottom -- starts all sides with high
        self.drawCustomRectangle(sx,                         sy,                         x,  y,  fingers_x,                  1,  fingers_y,                  1,  fingers_x,                   1, fingers_y,                  1)
        # right
        self.drawCustomRectangle(sx + x + 5 * bit_diameter,  sy,                         z,  y,  fingers_z, 1-(fingers_z%2==0),  fingers_y,                  0,  fingers_z,                   0, fingers_y,   (fingers_y%2==0))
        # left
        self.drawCustomRectangle(sx - z - 5 * bit_diameter,  sy,                         z,  y,  fingers_z,                  0,  fingers_y,   (fingers_y%2==0),  fingers_z,  1-(fingers_z%2==0), fingers_y,                  0)
        # lower
        self.drawCustomRectangle(sx,                         sy - z - 5 * bit_diameter,  x, z,   fingers_x,                  0,  fingers_z,                  0,  fingers_x,      fingers_x%2==0, fingers_z, 1-(fingers_z%2==0))
        # upper
        self.drawCustomRectangle(sx,                         sy + y + 5 * bit_diameter,  x, z,   fingers_x,     fingers_x%2==0,  fingers_z, 1-(fingers_z%2==0),  fingers_x,                   0, fingers_z,                  0)
        # top -- starts all sides with high, so it fits the tops of the other parts
        self.drawCustomRectangle(sx + x + 5 * bit_diameter,  sy - y - 5*bit_diameter,x, y,   fingers_x,                  1,  fingers_y,                  1,  fingers_x,                   1, fingers_y,                  1)



    ###
    ### draw a box with bottom, 4 sides and open lid
    ###
    ### start-position: define lower left corner (sx,sy)
    ###
    ### sx      ..      start position in x
    ### sy      ..      start position in y
    ###
    ### x       ..      length (size in x-direction)
    ### y       ..      width  (size in y-direction)
    ### z       ..      height (size in z-direction)
    ###
    def drawBoxV1(self, sx, sy, x, y, z):

        ## copy class parameters
        fingers_x    = self.fingers_x
        fingers_y    = self.fingers_y
        fingers_z    = self.fingers_z
        bit_diameter = self.bit_diameter

        # draw the bottom part
        # use the simple rectangle routine
        #drawRectangle(sx, sy, x, y)
        self.drawCustomRectangle(sx,sy,x,y,fingers_x,1,fingers_y,1,fingers_x,1,fingers_y,1)

        # draw right side, choose start positions in cad file
        self.drawCustomRectangle(sx + x + 5 * bit_diameter, sy,  z,  y,  fingers_z, 1-(fingers_z%2==0),  1,  1,  fingers_z,  0,  fingers_y,  (fingers_y%2==0))
        # draw the left part, choose start positions in cad file
        self.drawCustomRectangle(sx - z - 5 * bit_diameter, sy,  z,  y,  fingers_z, 0,  fingers_y, (fingers_y%2==0),  fingers_z,  1-(fingers_z%2==0),  1,1)
        # draw the lower side, choose start positions in cad file
        self.drawCustomRectangle(sx, sy - z - 5 * bit_diameter,  x, z,  1,1,fingers_z, 0, fingers_x, fingers_x%2==0, fingers_z, 1-(fingers_z%2==0))
        # draw the upper side, choose start positions in cad file
        self.drawCustomRectangle(sx, sy + y + 5 * bit_diameter,  x, z,  fingers_x,   (fingers_x%2==0), fingers_z, 1-(fingers_z%2==0), 1, 1, fingers_z, 0)



    ##
    ## generate a plain cutout rectangle, with dog-ears, if desired
    ##
    ##      cx      ...     start x-position, lower left point
    ##      cy      ...     start y-position, lower left point
    ##      width   ...
    ##      length  ...
    ## bit_diameter ...
    ##   cutx, cuty ...     0 == no dog-ears, 1 == along axis
    ##
    def cutOutRectangle(self, cx, cy, width, length, bit_diameter, cutx, cuty):

        ## copy class parameters
        drawing   = self.drawing

        ## draw both x-lines
        ##  shorten lines appropriately, if cutx set to 1 == yes
        drawing.add(dxf.line((cx+cutx*bit_diameter, cy         ), (cx+width-cutx*bit_diameter, cy         )))
        drawing.add(dxf.line((cx+cutx*bit_diameter, cy + length), (cx+width-cutx*bit_diameter, cy+length  )))

        ## draw both y-lines
        ##  shorten lines appropriately, if cutx set to 1 == yes
        drawing.add(dxf.line((cx      , cy+cuty*bit_diameter ), (cx      , cy+length-cuty*bit_diameter)))
        drawing.add(dxf.line((cx+width, cy+cuty*bit_diameter ), (cx+width, cy+length-cuty*bit_diameter)))

        ## draw the dog-ears for both x-lines, if wanted
        if cutx == 1:
            drawing.add(dxf.arc(bit_diameter/2, (cx+bit_diameter/2       , cy       ), 180, 360))
            drawing.add(dxf.arc(bit_diameter/2, (cx+width-bit_diameter/2 , cy       ), 180, 360))
            drawing.add(dxf.arc(bit_diameter/2, (cx+bit_diameter/2       , cy+length), 360, 180))
            drawing.add(dxf.arc(bit_diameter/2, (cx+width-bit_diameter/2 , cy+length), 360, 180))

        ## draw the dog-ears for both y-lines, if wanted
        if cuty == 1:
            drawing.add(dxf.arc(bit_diameter/2, (cx        , cy+bit_diameter/2       ),  90, 270))
            drawing.add(dxf.arc(bit_diameter/2, (cx        , cy+length-bit_diameter/2),  90, 270))
            drawing.add(dxf.arc(bit_diameter/2, (cx+width  , cy+bit_diameter/2       ), 270,  90))
            drawing.add(dxf.arc(bit_diameter/2, (cx+width  , cy+length-bit_diameter/2), 270,  90))



    ###
    ### drawRectangle
    ###   ... draws a rectangular shape with the given box joint parameters
    ###
    ###   D       <--         C
    ###     X---------------X
    ###     |               |
    ###   | |               | ^
    ###   v |               | |
    ###     |               |
    ###     X---------------X
    ###    A       -->        B
    ###
    ###  order of drawing the lines:
    ###     A -- B , B -- C, C -- D, D -- A
    ###
    def drawRectangle(self, cx, cy, size_x, size_y):

        ## copy class parameters
        fingers_x = self.fingers_x
        fingers_y = self.fingers_y
        fingers_z = self.fingers_z
        thickness = self.thickness

        ## we starthigh on every edge
        ## if a direction has an even number of fingers, the following direction
        ## has to beginshort
        if fingers_x % 2 == 0:  beginshort_y = 1
        else:                   beginshort_y = 0
        if fingers_y % 2 == 0:  beginshort_x = 1
        else:                   beginshort_x = 0

        # draw in the following order: bottom line, right line, top line, left line
        self.drawOneSide(cx+0     , cy+0     , fingers_x,    1,    0, size_x,  thickness,         1, beginshort_x,   0)
        self.drawOneSide(cx+size_x, cy+0     , fingers_y,    0,    1, size_y,  thickness,         1, beginshort_y,   0)
        self.drawOneSide(cx+size_x, cy+size_y, fingers_x,   -1,    0, size_x,  thickness,         1, beginshort_x,   0)
        self.drawOneSide(cx+0     , cy+size_y, fingers_y,    0,   -1, size_y,  thickness,         1, beginshort_y,   0)


    ##
    ## draw a custom rectangle with finger joints,
    ## a choosen number of fingers for each side,
    ## and starthigh/startlow option for each side
    ##
    ## start_x      ..      start position in x-direction
    ## start_y      ..      start position in y-direction
    ## length       ..      lenght (x-direction)
    ## width        ..      width (y-direction)
    ## fingers_n    ..      number of fingers for side n
    ## startghigh_n ..      starthigh on side n
    ##
    ##
    ###
    ###                SKETCH
    ###
    ###                side 3
    ###         D       <--         C
    ###           X---------------X
    ###           |               |
    ###         | |               | ^
    ### side 4  v |               | | side 2
    ###           |               |
    ###           X---------------X
    ###         A       -->         B
    ###                side 1
    ###
    ###  order of drawing the lines:
    ###     A -- B , B -- C, C -- D, D -- A
    ###
    def drawCustomRectangle(self, start_x, start_y, length, width, fingers_1, starthigh_1, fingers_2, starthigh_2, fingers_3, starthigh_3, fingers_4, starthigh_4):

        ## copy class parameters
        thickness = self.thickness

        ##
        ## draw the parts
        ##
        ## the next line starts short, if
        ##  - we have an even number of fingers and started high, OR if
        ##  - we have an odd  number of fingers and started low
        ##
        ## the end of the line is short, if the following line starts low
        ##
        self.drawOneSide(start_x+0     , start_y+0     , fingers_1,    1,    0, length,  thickness,      starthigh_1,  ( (fingers_4 % 2 == 0) & starthigh_4 ) | ( (fingers_4 % 2 != 0) & (not(starthigh_4)) ) ,  not(starthigh_2) )
        self.drawOneSide(start_x+length, start_y+0     , fingers_2,    0,    1, width,   thickness,      starthigh_2,  ( (fingers_1 % 2 == 0) & starthigh_1 ) | ( (fingers_1 % 2 != 0) & (not(starthigh_1)) ) ,  not(starthigh_3) )
        self.drawOneSide(start_x+length, start_y+width , fingers_3,   -1,    0, length,  thickness,      starthigh_3,  ( (fingers_2 % 2 == 0) & starthigh_2 ) | ( (fingers_2 % 2 != 0) & (not(starthigh_2)) ) ,  not(starthigh_4) )
        self.drawOneSide(start_x+0     , start_y+width , fingers_4,    0,   -1, width,   thickness,      starthigh_4,  ( (fingers_3 % 2 == 0) & starthigh_3 ) | ( (fingers_3 % 2 != 0) & (not(starthigh_3)) ) ,  not(starthigh_1) )

        return

