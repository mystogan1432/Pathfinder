import math
import sys
import pygame
from collections import deque

colours = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255), (255, 255, 0), (255, 255, 255)]
height = 700
width = 700
box_size = 700//50


def base_grid(grid, window):
    for row in range(50):
        for col in range(50):
            x = col * box_size
            y = row * box_size
            value = grid[row][col]
            # colour = colours[0] if value == 1 else colours[4]
            colour = colours[0]
            if value == 0:
                colour = colours[1]
            if value == 1:
                colour = colours[2]
            if value == 2:
                colour = colours[4]
            if value == 4:
                colour = colours[5]
            rect = pygame.Rect(x, y, 50, 50)
            pygame.draw.rect(window, colour, rect)
            pygame.draw.rect(window, colours[0], rect, 2)

def current_location(pos):
    x, y = pos
    row = y // box_size
    col = x // box_size
    return row, col

def heuristic(point_a, point_b):
    return math.sqrt((point_a[0] - point_b[0]) ** 2 + (point_a[1] - point_b[1]) ** 2)

def find_distance(curr, points):
    start = float("inf")
    idx = 0
    for i in range(len(points)):
        dist = heuristic(curr, points[i])
        if dist < start:
            start = dist
            idx = i
    return idx

def find_path_order(points):
    order = [points.pop(0)]
    while len(points) > 0:
        temp = find_distance(order[len(order) - 1], points)
        print(order)
        order.append(points.pop(temp))
    return order

def bfs(start, end, barriers):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    grid_size = 50
    queue = deque()
    queue.append(start)
    came_from = {}
    visited = set()
    visited.add(start)

    while queue:
        current = queue.popleft()
        if current == end:
            break

        for adj_x, adj_y in directions:
            neighbor = (current[0] + adj_x, current[1] + adj_y)
            if (0 <= neighbor[0] < grid_size and 0 <= neighbor[1] < grid_size and
                    neighbor not in barriers and neighbor not in visited):
                queue.append(neighbor)
                visited.add(neighbor)
                came_from[neighbor] = current

    if end not in came_from:
        return []
    curr = end
    local_path = []
    while curr != start:
        local_path.append(curr)
        curr = came_from[curr]
    local_path.reverse()
    return local_path

def find_path(points, barriers):
    path = []
    for i in range(1, len(points)):
        found_path = bfs(points[i-1], points[i], barriers)
        if found_path:
            path.extend(found_path)
        else:
            return "invalid path"
    return path


def solve_app(points):
    window = pygame.display.set_mode((height, width))
    pygame.init()
    pygame.display.set_caption('Pathfinder')
    running = True
    window.fill(colours[0])
    grid = [[0 for _ in range(50)] for _ in range(50)]
    barriers = []
    for pos in points:
        print(pos[0], pos[1])
        grid[int(pos[0])][int(pos[1])] = 2

    while running:
        base_grid(grid, window)
        if pygame.mouse.get_pressed()[0]:
            row, col = current_location(pygame.mouse.get_pos())
            print(row, col)
            if 0 <= row < 50 and 0 <= col < 50:
                barriers.append((row, col))
                grid[row][col] = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    grid = [[False for _ in range(50)] for _ in range(50)]
                    for pos in points:
                        grid[pos[0]][pos[1]] = 2
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    print(f"points: {points}")
                    point_order = find_path_order(points)
                    path = find_path(point_order, barriers)
                    if path == "invalid path":
                        print("path not valid")
                    else:
                        print(path)
                        for fin in path:
                            grid[int(fin[0])][int(fin[1])] = 4


        pygame.display.update()
    pygame.quit()
    sys.exit()