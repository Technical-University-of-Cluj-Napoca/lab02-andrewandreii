import sys
from collections import deque

def find_start_end(maze: list[list[str]]) -> tuple[tuple[int, int], tuple[int, int]]:
    start = None
    end = None

    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell == "S":
                start = (i, j)
            elif cell == "T":
                end = (i, j)

    return (start, end)

def get_neighbors(maze: list[list[str]], coord: tuple[int, int]) -> list[tuple[int, int]]:
    neighbors = []
    for i in (-1, 1):
        if maze[coord[0] + i][coord[1]] in (".", "T"):
            neighbors.append((coord[0] + i, coord[1]))

        if maze[coord[0]][coord[1] + i] in (".", "T"):
            neighbors.append((coord[0], coord[1] + i))

    return neighbors

def bfs(maze: list[list[str]]) -> None:
    start, end = find_start_end(maze)

    to_visit = deque([start])
    visited = set()
    parents = dict()

    while len(to_visit) > 0:
        current = to_visit.popleft()
        visited.add(current)

        if current == end:
            current = parents[current]
            while current != start:
                maze[current[0]][current[1]] = "*"
                current = parents[current]
            break

        for neighbor in get_neighbors(maze, current):
            if neighbor not in visited:
                to_visit.append(neighbor)
                parents[neighbor] = current

def dfs(maze: list[list[str]]) -> None:
    start, end = find_start_end(maze)

    to_visit = [start]
    visited = set()
    parents = dict()

    while len(to_visit) > 0:
        current = to_visit.pop()
        visited.add(current)

        if current == end:
            current = parents[current]
            while current != start:
                maze[current[0]][current[1]] = "*"
                current = parents[current]
            break

        for neighbor in get_neighbors(maze, current):
            if neighbor not in visited:
                to_visit.append(neighbor)
                parents[neighbor] = current

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Expected the filename of the maze and the solving algorithm")
        exit(-1)

    maze = None
    with open(sys.argv[1], "r") as f:
        maze = list(map(lambda x: list(x), f.read().split("\n")))

    for row in maze:
        print("".join(row))

    if sys.argv[2] == "dfs":
        dfs(maze)
    elif sys.argv[2] == "bfs":
        bfs(maze)
    else:
        print("Unknown solving algorithm")
        exit(-1)

    for row in maze:
        for cell in row:
            if cell in ("*", "T", "S"):
                print(f"\033[0;31m{cell}\033[0m", end="")
            else:
                print(cell, end="")
        print()
