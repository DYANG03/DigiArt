#Daniel Yang
#This program allows users to use various tools to create and design art. The user may select the tool they want to use in any order.
#The tools this program has are pencil, eraser, paintbrush, line, spraypaint, paintbucket, colour picker, and filled and unfilled rectangles and ellipses.
#This program comes with an undo redo function in case of mistakes. You can also save your work.
#There are also stamps for the user to enjoy.
#This program is designed with a theme of the anime Your Name
from pygame import *
from random import *
from math import *
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename

root = Tk()
root.withdraw()
pi = 3.14159265358979323846
def getAngle(x,y): #function that gets the angle depending on the quadrant
    if x == 0:
        x = 0.1
    val = atan(abs(y/x))        
    if x>0:
        if y>0:
            angle = val
        elif y<0:
            angle = 2*pi - val
        else:
            angle = 0
    elif x<0:
        if y>0:
            angle = pi - val
        elif y<0:
            angle = pi + val
        else:
            angle = pi
    else:
        if y>0:
            angle = pi/2
        elif y<0:
            angle = 3*pi/2
    return angle

#screen and screen size
ssx = 1280
ssy = 720
screen = display.set_mode((ssx,ssy))
#images tool positions and sizing
x = 20
y = 80
dx = 60
dy = 60
sx = int(0.9*dx)
sy = int(0.9*dy)

#background image
background = transform.scale(image.load("images/wp1892096.png"),(1280,720))
screen.blit(background,(0,0))
#title
movedown = 90
screen.blit(transform.smoothscale(image.load("images/title.png"),(466,263)),(905,60+movedown)) #draws the titles
screen.blit(transform.smoothscale(image.load("images/title 2.png"),(311,81)),(980,230+movedown))
#darken when hovering over tool
cover = Surface((sx,sy)).convert() # make blank Surface
cover.set_alpha(100) #set transparency of surface
cover.fill((255,0,255)) 
cover.set_colorkey((255,0,255))
draw.rect(cover,(1),(2,2,sx-3,sy-3))

allTools = ["pencil","eraser","paintbrush","line","spraypaint","paint bucket","filled rectangle","unfilled rectangle", #stores tool names
            "filled ellipse","unfilled ellipse","eyedropper"]
toolRects = [0 for i in range(len(allTools))] #stores tool rects
toolIcons = [] #stores tool images
    

#tool images and drawing tool images
def toolImages(I): #load and scale tool images
    loadImage = image.load("images/"+I+".jpg") #takes image name and loads it
    scaleImage = transform.smoothscale(loadImage,(sx-3,sy-3)) #scales the loaded image
    return scaleImage
for i in range(len(allTools)): #drawing tool images
    j = i//2 #vertical positioning of tools
    if i%2 != 0:#horizontal positioning of tools
        k = 1
    else:
        k = 0
    screen.blit(toolImages(allTools[i]),(x+k*dx+2,y+j*dy+2)) #draws all tool images in the loop
    toolIcons.append(toolImages(allTools[i])) #stores the tool images in a list
    toolIcons.append((x+k*dx+2,y+j*dy+2)) #stores the tool image positions in the same list
    toolRects[i] = Rect(x+k*dx,y+j*dy,sx,sy) #makes a rect for every tool image
    draw.rect(screen,(255,255,255),toolRects[i],2)
draw.rect(screen,(0),toolRects[0],2)#makes pencil selected automatically

#stamps
stamps = ["Mitsuha1","Mitsuha2","Mitsuha4","TakiMitsuha","TakiMitsuha2","TakiMitsuha3"] #stores the stamp names
stampImages = [] #store the stamp images
stampRects = [] #stores the stamp rects
for i in range(len(stamps)):
    stampImage = transform.smoothscale(image.load("images/"+stamps[i]+".png"),(120,140)) #load all stamps from the list
    stampImages.append(stampImage) #store the images in the stamp image list
for i in range(len(stamps)):
    screen.blit(stampImages[i],(160+140*i,570)) #blit the stamps onto the program
    stampRect = Rect(160+140*i,570,120,140) #make rects that correlate to each one
    stampRects.append(stampRect) #add rects to stamp rect list
    
#canvas rectangle
canvasRect = Rect(160,80,800,480)
draw.rect(screen,(255,255,255),canvasRect)

#load and save, rects, images, and drawing
saveRect = Rect(160,30,40,40) 
openRect = Rect(210,30,40,40)
saveImage = transform.smoothscale(image.load("images/save.png"),(40,40))
screen.blit(saveImage,(160,30))
openImage = transform.smoothscale(image.load("images/open.png"),(40,40))
screen.blit(openImage,(210,30))


#color selection
colorWheel = transform.smoothscale(image.load("images/color selection.jpg"),(270,158)) #import the palette
screen.blit(colorWheel,(1010,562))
colorRect = Rect(1010,562,300,194) #make a rect around it
smallColor = screen.subsurface(1160,522,40,40).copy()
draw.rect(screen,0,(1200,482,80,80)) #shows the initial colour as black

#thickness slider rectangle
dyd = 60
sliderBackground = screen.subsurface(20,386+dyd,119,18).copy() #copy small portion of screen for blitting
sliderRect = Rect(20,390+dyd,115,10) #slider scrolling area
draw.rect(screen,(255,255,255),sliderRect,1)
draw.rect(screen,(255,255,255),(75,386+dyd,4,18))
thickness = 10
draw.circle(screen,0,(24,415+dyd),2)#drawing circles underneath to show increasing thickness
draw.circle(screen,0,(36,415+dyd),3)
draw.circle(screen,0,(50,415+dyd),4)
draw.circle(screen,0,(66,415+dyd),5)
draw.circle(screen,0,(84,415+dyd),6)
draw.circle(screen,0,(104,415+dyd),7)
draw.circle(screen,0,(125,415+dyd),8)


def drawbox(a): #highlights selected tool
    for rect in toolRects:
        draw.rect(screen,(255,255,255),rect,2)
    draw.rect(screen,(0),toolRects[allTools.index(a)],2)
    
posSelected = 0 #remembers which one is already highlighted when selecting tools

tool = "pencil" #stores the current tool

#undo redo, rects, images, and drawing
undoRect = Rect(260,30,40,40)
redoRect = Rect(310,30,40,40)
screen.blit(transform.smoothscale(image.load("images/undo.png"),(40,40)),(260,30))
screen.blit(transform.smoothscale(image.load("images/redo.png"),(40,40)),(310,30))

#clear canvas
clearRect = Rect(360,30,40,40)
screen.blit(transform.scale(image.load("images/clear.png"),(40,40)),(360,30))

undo = [screen.subsurface(canvasRect).copy()] #lists for undo redo
redo = []

pixels = set() #sets for flood fill
pixels2 = set()

colour = 0 #stores the colour chosen

clicking = False
clicked = False
undoClicked = False
redoClicked = False
running =True
while running:
    mb = mouse.get_pressed()
    mx,my = mouse.get_pos()
    for e in event.get():
        if e.type == QUIT:
            running = False
        if e.type == MOUSEBUTTONDOWN:
            linex,liney = mouse.get_pos() #gets mouseposition when pressed down, used for line, rectangle, and ellipse tools
            back = screen.copy()
        if e.type == MOUSEBUTTONDOWN and undoRect.collidepoint(mouse.get_pos()):
            undoClicked = True #runs undo
        if e.type == MOUSEBUTTONDOWN and redoRect.collidepoint(mouse.get_pos()):
            redoClicked = True #runs redo
        if e.type == MOUSEBUTTONDOWN and openRect.collidepoint(mx, my):
            try:
                result = askopenfilename(filetypes = [("Picture files", "*.png;*.jpg")]) #gets filename from user               
                myPic=image.load(result) #loads the image with the same filename
                screen.blit(myPic,(canvasRect.x,canvasRect.y)) #blits the image onto the canvas
                undo.append(myPic) #adds to undo so program doesn't crash
                tool = None
            except:
                pass
        if e.type == MOUSEBUTTONDOWN and saveRect.collidepoint(mx,my):
            try:
                result=asksaveasfilename(defaultextension=".jpg") #gets the filename the user wants to save it as
                image.save(screen.subsurface(canvasRect).copy(),result) #saves the canvas
                tool = None
            except:
                pass
        if e.type == MOUSEBUTTONDOWN and canvasRect.collidepoint(mouse.get_pos()) and tool == "paint bucket":
            fx,fy = mouse.get_pos()
            fillColour = screen.get_at((fx,fy)) #what colour needs to be filled in by flood fill
            pixels.add((fx,fy)) #adds the first pixel to flood fill set
            clicking = True
        if e.type == MOUSEBUTTONUP:
            clicked = False
        if e.type == MOUSEBUTTONUP and canvasRect.collidepoint(mouse.get_pos()):
            canvasShot = screen.subsurface(canvasRect).copy()
            undo.append(canvasShot)
            redo = [] #clear redo whenever something new is added to undo
        if e.type == MOUSEBUTTONUP and not clicking:
            pixels.clear() #clear pixels after done flood filling

    #drawing thickness slider
    if mb[0]==1 and sliderRect.collidepoint(mx,my):
        screen.blit(back,(0,0))
        screen.blit(sliderBackground,(20,386+dyd)) 
        draw.rect(screen,(255,255,255),sliderRect,1)
        draw.rect(screen,(255,255,255),(mx,386+dyd,4,18)) #draws the slider at mouse position
        thickness = (mx-20)//5 #thickness is determined by how far the slider is from its original position
    #clear canvas
    if mb[0]==1 and clearRect.collidepoint(mx,my):
        draw.rect(screen,(255,255,255),canvasRect)

    #getting colour from wheel
    if mb[0]==1 and colorRect.collidepoint(mx,my): #if you click on the colour palette
        colour = screen.get_at((mx,my)) #sets the colour to the colour you clicked on
        draw.rect(screen,colour,(1200,482,80,80)) #shows what colour you currently picked
    screen.blit(smallColor,(1160,522)) #makes it so smaller coloured rectangle disappears after mouse is off of colour palette
    if colorRect.collidepoint(mx,my):
        draw.rect(screen,screen.get_at((mx,my)),(1160,522,40,40)) #draws a smaller rectangle so you can compare the colour you are hovering over with your old one
    
    
    #selecting stamps and stamping
    for i in range(len(stamps)):
        if stampRects[i].collidepoint(mx,my) and mb[0]==1:
            tool = stamps[i]
            tool2 = tool #ensures no other tool is used at the same time and stores which stamp is selected
        if tool == stamps[i]:
            if canvasRect.collidepoint(mx,my) and mb[0]==1:
                screen.set_clip(canvasRect)
                screen.blit(back,(0,0))
                screen.blit(stampImages[stamps.index(tool2)],(mx-50,my-50)) #because the lists are linked, use indexes to blit the right image
                screen.set_clip(None)
    
    
    #drawing and selecting tools
    for i in range(len(allTools)): #loops through all the tools    
        c = toolRects[i] #checks one tool at a time
        j = i//2 #vertical positioning of the tools
        if i%2 != 0: #horizontal positioning of tools
            k = 1
        else:
            k = 0
        screen.blit(toolIcons[i*2],toolIcons[i*2+1]) #blits tool images to their locations 
        if i == posSelected: 
            if posSelected%2 != 0: #positioning of selected tool
                k2 = 1
            else:
                k2 = 0
            screen.blit(cover,(x+k2*dx,y+posSelected//2*dy)) #highlights selected tool
        if c.collidepoint(mx,my):
            for g in range(0,len(toolIcons),2):
                if i != g//2 and g//2 != posSelected:
                    screen.blit(toolIcons[g],toolIcons[g+1])
            if i != posSelected:
                screen.blit(cover,(x+k*dx,y+j*dy)) #highlights tools when you hover over them
            if mb[0] == 1 and not clicked: #when you hold down the mouse you can't change tools, must click
                clicked = True 
                drawbox(allTools[i]) #outlines the selected tool
                posSelected = i
                tool = allTools[i] #saves the tool selected
 
                
    #drawing
    if mb[0]==1 and canvasRect.collidepoint(mx,my):
        screen.set_clip(canvasRect) #length between the disconnected circles
        if tool == "pencil":
            screen.set_clip(canvasRect) #length between the disconnected circles
            draw.line(screen,colour,(omx,omy),(mx,my)) #draw line from old point to new point
            screen.set_clip
        if tool == "eraser":
            screen.set_clip(canvasRect) #length between the disconnected circles
            lengthB = hypot(mx-omx,my-omy) #angle between the disconnected circles
            angleB = getAngle(mx-omx,my-omy)
            for i in range(int(lengthB)):
                draw.circle(screen,(255,255,255),(omx+int(i*cos(angleB)),omy+int(i*sin(angleB))),thickness) #connects the disconnected circles with circles
            screen.set_clip(None)
        if tool == "paintbrush":
            screen.set_clip(canvasRect) #length between the disconnected circles
            lengthB = hypot(mx-omx,my-omy) #length between the disconnected circles
            angleB = getAngle(mx-omx,my-omy) #angle between the disconnected circles
            for i in range(int(lengthB)):
                draw.circle(screen,colour,(omx+int(i*cos(angleB)),omy+int(i*sin(angleB))),thickness) #connects the disconnected circles with circles
            screen.set_clip(None)
        if tool == "spraypaint":
            screen.set_clip(canvasRect)
            numPoints = randint(0, 10)
            pointsList = []
            #fill the list with random points
            while len(pointsList) < numPoints:
                sprayx = randint(mx-thickness*3, mx+thickness*3)
                sprayy = randint(my - thickness*3, my + thickness*3)
                #check if the point is within a circle
                if ((sprayx-mx)**2 + (sprayy-my)**2)**0.5 < thickness*3:
                    pointsList.append((sprayx, sprayy))
            #draw the points
            for point in pointsList:
                draw.circle(screen,colour,(point[0], point[1]), 1)
            screen.set_clip(None)
        if tool == "line":
            screen.set_clip(canvasRect)
            screen.blit(back,(0,0))
            lengthLine = hypot(mx-linex,my-liney) #gets length of the line
            angleLine = getAngle(mx-linex,my-liney) #gets the angle so direction of line is known
            for i in range(int(lengthLine)):
                draw.circle(screen,colour,(linex+int(i*cos(angleLine)),liney+int(i*sin(angleLine))),thickness) #draws line as a bunch of circles
            screen.set_clip(None)
        if tool == "filled rectangle":
            screen.set_clip(canvasRect)
            screen.blit(back,(0,0))
            if mx-linex<=0: #different starting points depending on which way you drag
                startpx = mx
            elif mx-linex>0:
                startpx = linex                
            if my-liney<=0:
                startpy = my
            elif my-liney>0:
                startpy = liney
            draw.rect(screen,colour,(startpx,startpy,abs(mx-linex),abs(my-liney)))
            screen.set_clip(None)
        if tool == "unfilled rectangle":
            screen.set_clip(canvasRect)
            screen.blit(back,(0,0))
            if mx-linex<=0: #different starting points depending on which way you drag
                startpx = mx
            elif mx-linex>0:
                startpx = linex                
            if my-liney<=0:
                startpy = my
            elif my-liney>0:
                startpy = liney
            for i in range(thickness):
                draw.rect(screen,colour,(startpx,startpy,abs(mx-linex)+i,abs(my-liney)+i),1)
                draw.rect(screen,colour,(startpx+i,startpy+i,abs(mx-linex),abs(my-liney)),1)
            screen.set_clip(None)
        if tool == "filled ellipse":
            screen.set_clip(canvasRect)
            screen.blit(back,(0,0))
            if mx-linex<=0: #these are the four cases for drawing the ellipse depending on which way you drag
                startpx = mx
            elif mx-linex>0:
                startpx = linex                
            if my-liney<=0:
                startpy = my
            elif my-liney>0:
                startpy = liney
            draw.ellipse(screen,colour,(startpx,startpy,abs(mx-linex),abs(my-liney)))
            screen.set_clip(None)
        if tool == "unfilled ellipse":
            screen.set_clip(canvasRect)
            screen.blit(back,(0,0))
            if mx-linex<=0: #these are the four cases for drawing the ellipse depending on which way you drag
                startpx = mx
            elif mx-linex>0:
                startpx = linex                
            if my-liney<=0:
                startpy = my
            elif my-liney>0:
                startpy = liney
            try:
                draw.ellipse(screen,colour,(startpx,startpy,abs(omx-linex),abs(omy-liney)),thickness)
            except:
                pass
            screen.set_clip(None)
        screen.set_clip(None)
        screen.blit(smallColor,(1160,522)) #makes it so smaller coloured rectangle disappears after mouse is off of colour palette
    if tool == "eyedropper" and canvasRect.collidepoint(mx,my):
        if mb[0]==1:
            colour = screen.get_at((mx,my))
            draw.rect(screen,colour,(1200,482,80,80))
        draw.rect(screen,screen.get_at((mx,my)),(1160,522,40,40))
    if tool == "paint bucket" and clicking and canvasRect.collidepoint(mx,my):
        for i in range(10000):#speeds the process up
            if len(pixels)>0: #while there are still pixels to check
                pixel = pixels.pop()
                pixels2.add(pixel)#add pixels to be coloured to second set so it can all be coloured at once later
                if pixel[0]==0 or pixel[0]==ssx-1 or pixel[1]==0 or pixel[1]==ssy-1: #if the pixel is at the edge, don't check around it as it will give an error
                    continue
                else:
                    #check every pixel around to see if it is the colour to be filled
                    if screen.get_at((pixel[0]+1,pixel[1])) == fillColour and (pixel[0]+1,pixel[1]) not in pixels2 and canvasRect.collidepoint(pixel[0]+1,pixel[1]):
                        pixels.add((pixel[0]+1,pixel[1]))
                    if screen.get_at((pixel[0]-1,pixel[1])) == fillColour and (pixel[0]-1,pixel[1]) not in pixels2 and canvasRect.collidepoint(pixel[0]-1,pixel[1]):
                        pixels.add((pixel[0]-1,pixel[1]))
                    if screen.get_at((pixel[0],pixel[1]+1)) == fillColour and (pixel[0],pixel[1]+1) not in pixels2 and canvasRect.collidepoint(pixel[0],pixel[1]+1):
                        pixels.add((pixel[0],pixel[1]+1))
                    if screen.get_at((pixel[0],pixel[1]-1)) == fillColour and (pixel[0],pixel[1]-1) not in pixels2 and canvasRect.collidepoint(pixel[0],pixel[1]-1):
                        pixels.add((pixel[0],pixel[1]-1))
            else:
                for j in pixels2:
                    screen.set_at(j,colour) #colour all pixels at the same time
                pixels2.clear()
                clicking = False
                break
    #undo redo
    if undoClicked: #each time you click undo once
        undoClicked = False
        try:
            undoImage = undo.pop()
            redo.append(undoImage) #add image into redo
            screen.blit(undo[-1],(160,80))
        except:
            pass        
    if redoClicked: #each time clicked redo once
        redoClicked = False
        try:
            redoImage = redo.pop()
            undo.append(redoImage) #add image back into undo
            screen.blit(redoImage,(160,80)) #blit image
        except:
            pass
        

            
            
            

            
            
     



    omx,omy = mx,my
    display.flip()


quit()
