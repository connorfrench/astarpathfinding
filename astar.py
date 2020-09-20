import pygame
import math 
from queue import PriorityQueue

#Create and 800 x 800 window
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Pathfinder")

#Color variables for colors used
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

#Node class to store each node of the grid
class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.width = width
        self.total_rows = total_rows
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.is_perma_barrier = False
        self.neighbors = []

    def get_pos(self):
        return self.row, self.col   #position of node

    #functions that determine meaning of node based on what color it currently is
    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN
    
    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    #functions that change the color value of a node to change it's meaning to the program
    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN
    
    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    #function draw the node
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    #function to keep track of the neighbors of each node, making sure that they are not barriers or outside of the scope of the grid
    def update_neighbors(self, grid):
        if self.row < self.total_rows - 1 and not grid[self.row+1][self.col].is_barrier(): #DOWN
            self.neighbors.append(grid[self.row+1][self.col])

        if self.row > 0 and not grid[self.row-1][self.col].is_barrier(): #UP
            self.neighbors.append(grid[self.row-1][self.col])

        if self.col > 0 and not grid[self.row][self.col-1].is_barrier(): #LEFT
            self.neighbors.append(grid[self.row][self.col-1])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col+1].is_barrier(): #RIGHT
            self.neighbors.append(grid[self.row][self.col+1])

#draw the path using the predecessor list
def reconstruct_path(pred, cur, draw):
    while cur in pred:
        cur = pred[cur]
        cur.make_path()
        draw()

#heuristic function using Manhattan Distance
def h(n1, n2):
    x1, y1 = n1
    x2, y2 = n2
    return abs(x1 - x2) + abs (y1 - y2)

#A* pathfinding algorithm that finds the shortest path from one node to another
def astar(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))         #add start node to queue
    pred = {}                               #list of predecessors so that final path can be drawn
    g = {node: float("inf") for row in grid for node in row}    #initialize g value of each node to infinity, and start to 0
    g[start] = 0
    f = {node: float("inf") for row in grid for node in row}       #initialize f value of each node to infinity, and start to it's heuristic value
    f[start] = h(start.get_pos(), end.get_pos())
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2]
        open_set_hash.remove(current)
        if current == end:                  #end node is found
            reconstruct_path(pred, end, draw)   #draw the path, making sure end and start are still visible
            end.make_end()
            start.make_start()
            return True
        for neighbor in current.neighbors:      #add the neighbors of current node to the set of open nodes, and update their g and f values
            temp_g = g[current] + 1
            if temp_g < g[neighbor]:
                pred[neighbor] = current
                g[neighbor] = temp_g
                f[neighbor] = temp_g + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count+= 1
                    open_set.put((f[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()       
        draw()
        if current != start:
            current.make_closed()           #close node after it is removed
    return False

#determine the grid based on the number of rows and width of window, while also making the outer borders of the grid barriers
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            if(i == 0 or j == 0 or i == node.total_rows-1 or j == node.total_rows-1):
                node.make_barrier()
                node.is_perma_barrier = True
            grid[i].append(node)
    return grid

#draw the gridlines of grid
def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GRAY, (0, i * gap), (width, i * gap))
        pygame.draw.line(win, GRAY, (i * gap, 0), (i * gap, width))

#draw the grid
def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()

#determine which node the mouse is currently hovering over when clicked
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col

def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)
    start = None
    end = None
    run = True

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():            #allow user to quit out
            if event.type == pygame.QUIT:
                run = False
            if pygame.mouse.get_pressed()[0]:       #user can place start, end, and barriers with left click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                if not start and node != end and not node.is_barrier():
                    start = node
                    start.make_start()
                elif not end and node != start and not node.is_barrier():
                    end = node
                    end.make_end()
                elif node != end and node != start:
                    node.make_barrier()
            elif pygame.mouse.get_pressed()[2]:     #user can remove start, end, and barriers with right click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                if not node.is_perma_barrier:       #do not allow outer barrier to be removed
                    node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:       #press space to start algorithm
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    astar(lambda: draw(win, grid, ROWS, width), grid, start, end)
                if event.key == pygame.K_c:                             #press c to clear grid
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
    pygame.quit()

main(WIN, WIDTH)