import pygame
import math
from queue import PriorityQueue

# Load the image
image_path = "path_planning/img/test1.png"  # Spécifiez le chemin de votre image
IMAGE = pygame.image.load(image_path)

# Redimensionnez l'image pour correspondre à la taille de l'écran
WIDTH = IMAGE.get_width()
HEIGHT = IMAGE.get_height()
IMAGE = pygame.transform.scale(IMAGE, (WIDTH, HEIGHT))

# Définir les couleurs
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == RED

    def is_end(self):
        return self.color == BLUE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

# definition de l'heuristique
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)                      #Manhattan
    #return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)       #Euclidienne
    #return max(abs(x1 - x2), abs(y1 - y2))                  #Tchebychev



def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            # Reconstruire le chemin ici
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    # Définir la couleur des lignes avec une opacité réduite (alpha)
    line_color = (GREY[0], GREY[1], GREY[2], 0)  # Ajoutez un quatrième élément pour l'opacité (100 dans cet exemple)

    for i in range(rows):
        pygame.draw.line(win, line_color, (0, i * gap), (width, i * gap),
                         1)  # Utilisez une largeur de ligne de 1 pour éviter de masquer l'image
    for j in range(rows):
        pygame.draw.line(win, line_color, (j * gap, 0), (j * gap, width), 1)  # Utilisez une largeur de ligne de 1 pour éviter de masquer l'image


def draw(win, grid, rows, width):
    win.blit(IMAGE, (0, 0))  # Affichez l'image à chaque redessin
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col
def place_elements_from_image(image, grid, start_color, end_color):
    """
    Analyse l'image et place automatiquement les éléments sur la grille.
    :param image: L'image chargée avec pygame.
    :param grid: La grille de spots.
    :param start_color: La couleur représentant le point de départ.
    :param end_color: La couleur représentant le point d'arrivée.
    """
    rows = len(grid)
    width = grid[0][0].width
    img_width, img_height = image.get_size()
    for i in range(rows):
        for j in range(rows):
            # Convertir la position de la grille en position de l'image
            img_x = int((j / rows) * img_width)
            img_y = int((i / rows) * img_height)
            pixel_color = image.get_at((img_x, img_y))
            if pixel_color == BLACK:  # Barrière
                grid[i][j].make_barrier()
            elif pixel_color == RED:  # Départ
                global start
                start = grid[i][j]
                start.make_start()
            elif pixel_color == BLUE:  # Arrivée
                global end
                end = grid[i][j]
                end.make_end()
def main():
    global start, end

    ROWS = 50
    grid = make_grid(ROWS, WIDTH)

    start = None
    end = None

    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("A* Path Finding Algorithm")

    place_elements_from_image(IMAGE, grid, ORANGE, BLUE)

    run = True
    started = False
    while run:
        draw(WIN, grid, ROWS, WIDTH)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    algorithm(lambda: draw(WIN, grid, ROWS, WIDTH), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, WIDTH)
                    place_elements_from_image(IMAGE, grid, ORANGE, BLUE)

    pygame.quit()

if __name__ == "__main__":
    main()