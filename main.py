import pygame
import sys
from collections import deque


WIDTH, HEIGHT = 700, 700
TILE_SIZE = 20

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Spot:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.start = False
        self.end = False
        self.obstacle = False
        self.children = []
        self.is_visited = False
        self.exploring = False
        self.path_length = 0
        self.parents = []
        self.is_path = False
        self.path_length = float('inf')
        
    
    def draw(self, surf):
        if self.obstacle:
            pygame.draw.rect(surf, 'black', self.rect)
        elif self.end:
            pygame.draw.rect(surf, 'green', self.rect)
        elif self.start:
            pygame.draw.rect(surf, 'blue', self.rect)
        elif self.exploring:
            pygame.draw.rect(surf, 'yellow', self.rect)
        if self.is_visited and not self.start and not self.end and not self.obstacle:
            pygame.draw.rect(surf, 'red', self.rect)
        if self.is_path:
            pygame.draw.rect(surf, 'purple', self.rect)
        pygame.draw.rect(surf, 'grey', self.rect, 1)
        

    def is_empty(self):
        return not (self.start or self.obstacle or self.end)
    
    def get_children(self, grid):
        c = self.rect.x // self.rect.w
        r = self.rect.y // self.rect.h
        lst = []
        for y in (-1, 0, 1):
            for x in (-1, 0, 1):
                if abs(x) == abs(y): continue
                if not (0 <= r + y < len(grid)): continue
                if not (0 <= c + x < len(grid[r])): continue
                lst.append(grid[r + y][c + x])
        return lst


def drawGrid(surf, grid):
    for r, row in enumerate(grid):
        for c, spot in enumerate(row):
            spot.draw(surf)

def create_grid(width, height, block_size):
    grid = [[0 for j in range(width//block_size)] for i in range(height//block_size)]
    for y in range(height//block_size):
        for x in range(width//block_size):
            grid[y][x] = Spot(x*block_size, y*block_size, block_size, block_size)
    return grid

def findPath(grid, startNode, dstNode, surf):
    visited = set()
    queue = deque()
    startNode.path_length = 1
    queue.append(startNode)
    while len(queue) != 0:
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        curr = queue.popleft()
        if curr in visited:
            continue
        if curr == dstNode:
            p = min([p for p in curr.parents], key=lambda x: x.path_length)
            while p.parents != []:
                p.is_path = True
                p = min([p for p in p.parents], key=lambda x: x.path_length)
            return True
        for child in [c for c in curr.get_children(grid) if not c.obstacle]:
            queue.append(child)
            if child != startNode:
                child.parents.append(curr)
            child.path_length = min(1 + curr.path_length, child.path_length)
            child.exploring = True
        visited.add(curr)
        curr.is_visited = True
        curr.exploring = False
        drawGrid(surf, grid)
    return False

def clear(grid):
    for row in grid:
        for spot in row:
            spot.start = False
            spot.end = False
            spot.obstacle = False
            spot.is_visited = False
            spot.exploring = False
            spot.is_path = False
            spot.parents = []
            spot.path_length = float('inf')
    return grid

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    startNode = None
    endNode = None
    algoresult = None
    grid = create_grid(WIDTH, HEIGHT, TILE_SIZE)
    path = []
    while True:
        screen.fill('white')
        drawGrid(screen, grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if pygame.mouse.get_pressed()[0]:
                mx, my = pygame.mouse.get_pos()
                mx //= TILE_SIZE
                my //= TILE_SIZE
                if grid[my][mx].is_empty():
                    grid[my][mx].obstacle = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    mx, my = pygame.mouse.get_pos()
                    mx //= TILE_SIZE
                    my //= TILE_SIZE
                    if grid[my][mx].is_empty():
                        if not startNode:
                            grid[my][mx].start = True
                            startNode = grid[my][mx]
                        elif not endNode:
                            grid[my][mx].end = True
                            endNode =  grid[my][mx]
                    elif grid[my][mx].start:
                        grid[my][mx].start = False
                        startNode = None
                    elif grid[my][mx].end:
                        grid[my][mx].end = False
                        endNode = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f and algoresult == None:
                    algoresult = findPath(grid, startNode, endNode, screen)

                if event.key == pygame.K_c:
                    grid = clear(grid)
                    startNode = None
                    endNode = None
                    algoresult = None

        pygame.display.update()

main()