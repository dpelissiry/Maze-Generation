from collections import deque
import random, time
#from anytree import Node, RenderTree, AnyNode, AsciiStyle, search

'''
#--Pseudocode--#
random first choice pushed to stack and added to root of tree
random direction chosen
if square is not on stack:
    push to stack and add to tree
else:
    choose different direction
repeat until cell has no valid directions
pop cell from stack until cell has a choice that is not in stack
push to stack and add to tree
repeat until stack is deleted
'''

scale = 50
width = 1000
height = 1000

def generate_grid():
    stroke(0)
    for col in range(width/scale+1):
        line(col*scale, 0, col*scale, height)
    for row in range(height/scale+1):
        line(0, scale*row, width, scale*row)
        
def draw_rect_backtrack(cell, last_cell):
    stroke(0,0,0,0)
    fill(255,0,0)
    time.sleep(1)
    
    convert_to_pixels(cell)
    #save pixelx and pixely to compare to previous square pixelx and y
    current_cell_pixelx, current_cell_pixely = pixelx, pixely
    rect(pixelx,pixely,scale-2,scale-2)
    convert_to_pixels(last_cell)
    #compares the location of the previous square to current square so it can place rect over line
    if pixelx > current_cell_pixelx:
        left = True
        rect(current_cell_pixelx,current_cell_pixely,scale,scale-2)
    elif pixelx < current_cell_pixelx:
        right = True
        rect(current_cell_pixelx-2,current_cell_pixely,scale-2,scale-2)
    elif pixelx == current_cell_pixelx:
        if pixely > current_cell_pixely:
            rect(current_cell_pixelx, current_cell_pixely+2,scale-2,scale-2)
        if pixely < current_cell_pixely:
            rect(current_cell_pixelx, current_cell_pixely-2,scale-2,scale-2) 
    
    
def draw_rect_maze(cell, last_cell):
    stroke(0,0,0,0)
    fill(255,255,255)
    
    convert_to_pixels(cell)
    #save pixelx and pixely to compare to previous square pixelx and y
    current_cell_pixelx, current_cell_pixely = pixelx, pixely
    rect(pixelx,pixely,scale-2,scale-2)
    convert_to_pixels(last_cell)
    #compares the location of the previous square to current square so it can place rect over line
    if pixelx > current_cell_pixelx:
        left = True
        rect(current_cell_pixelx,current_cell_pixely,scale,scale-2)
    elif pixelx < current_cell_pixelx:
        right = True
        rect(current_cell_pixelx-2,current_cell_pixely,scale-2,scale-2)
    elif pixelx == current_cell_pixelx:
        if pixely > current_cell_pixely:
            rect(current_cell_pixelx, current_cell_pixely+2,scale-2,scale-2)
        if pixely < current_cell_pixely:
            rect(current_cell_pixelx, current_cell_pixely-2,scale-2,scale-2) 
        
         
    
def convert_to_pixels(cell):
    global pixelx
    global pixely
    
    pixelx = ((cell%(width/scale))*scale)+1
    pixely = ((cell//(width/scale))*scale)+1

def backtrack():
    global drawing
    global current_cell
    last_cell = stack[len(stack)-1]
    stack.pop()
    if len(stack) == 1:
        print("finished")
        #print(len(stack))
        drawing = False
        draw()
    else:
        #print(len(stack))
        current_cell = stack[len(stack)-1]
        #draw_rect_backtrack(current_cell, last_cell)
        #print(stack)
        #time.sleep(1)

    
def choose_direction():
    global current_cell
    height_new = height/scale
    width_new = width/scale
    
    
    
    directions = ['N','W','S','E']
    validDirection = False
    
    #create set of chosen directions
    chosen_directions = set()
    while not validDirection:
        
        
        dist_left_wall = (stack[len(stack)-1] % width_new)
        dist_right_wall = ((width_new)-(stack[len(stack)-1] % width_new))-1
        dist_top = stack[len(stack)-1]//width_new
        dist_bottom = (height_new-1)-(stack[len(stack)-1]//width_new)
        
        direction = random.choice(directions)
        #print(direction)
        if direction == 'N' and dist_top > 0:
            current_cell = stack[len(stack)-1]-width/scale 
            chosen_directions.add(direction)
        elif direction == 'W' and dist_right_wall > 0:
            current_cell = stack[len(stack)-1]+1 
            chosen_directions.add(direction)
        elif direction == 'S' and dist_bottom > 0:
            current_cell = stack[len(stack)-1]+width/scale
            chosen_directions.add(direction)
        elif direction == 'E' and dist_left_wall > 0:
            current_cell = stack[len(stack)-1]-1
            chosen_directions.add(direction)
        if current_cell not in all_squares:
            #print current_cell
            #print(all_squares)
            validDirection = True
        elif len(chosen_directions) == 4 or (len(chosen_directions) == 3 and (dist_top == 0 or dist_bottom == 0 or dist_right_wall == 0 or dist_left_wall == 0)) or (len(chosen_directions) == 2 and ((dist_right_wall + dist_bottom == 0) or (dist_left_wall + dist_bottom == 0) or (dist_right_wall + dist_top == 0) or (dist_left_wall + dist_top == 0))):
            chosen_directions = set()
            #print(current_cell)
            #stack.append(current_cell)
            #print(chosen_directions)
            backtrack()

class Button():
    def __init__(self, text,x,y):
        self.x = x
        self.y = y
        self.text = text
    
    def draw_button(self):
        rectMode(CENTER)
        fill(255,255,255)
        rect(self.x,self.y,150,50)
        fill(0,102,0)
        textSize(20)
        textAlign(CENTER)
        text(self.text, self.x,self.y+5)
        rectMode(CORNER)
    def return_x(self):
        return(self.x)
    def return_y(self):
        return(self.y)
    def mouseInButton(self,mousex,mousey):
        x_values = []
        y_values = []
        for i in range(self.x-50,self.x+50):
            x_values.append(i)
        if mousex in x_values:
            for n in range(int(self.y-25),int(self.y+25)):
                y_values.append(n)
            if mousey in y_values:
                return True
            else:
                return False
        else:
            return False
        
def buttons():
    global start_button
    #screen_w = 1200
    start_button = Button("Generate Maze", (1200/24)*22, (1000/15)*2)
    start_button.draw_button()

def setup():
    global all_squares
    global cells
    global stack
    global first_cell
    global current_cell
    global drawing
    drawing = False
    all_squares = []
    background(200)
    size(1200,1000)
    frameRate(60)
    #list of squares
    cells = list()
    for i in range(1, (width/scale)*(height/scale)+1):
        cells.append(i)
    #creation of stack
    stack = deque()
    stack.append(-1)
    current_cell = 0
    #pick first cell
    first_cell = 0#random.choice(cells)
    
    #print(first_cell)
    stack.append(first_cell)
    all_squares.append(first_cell)
    #root = Node(first_cell, parent = None)
    buttons()
    generate_grid()
    
        
        
        
def draw():
    global stack
    global cells
    if drawing:
        #pick direction to travel and ensures that it is valid direction
        choose_direction()
        #add chosen cell to tree
        #child_node = Node(current_cell, parent = stack[len(stack)-1])
        #add chosen cell to stack
        stack.append(current_cell)
        all_squares.append(current_cell)
        draw_rect_maze(current_cell, stack[len(stack)-2])
        #print(stack)

def mouseClicked():
    global drawing
    
    if start_button.mouseInButton(mouseX, mouseY):
        drawing = True
