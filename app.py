# Piotr Stachowicz
import pygame
import sys
import random
from Bezier import *
import easygui


def HelpMenu():
    easygui.msgbox("Q - QUIT \nP - SAVE IMAGE \nR - HARD RESET \nC - CLEAR \nS - SAVE \nH - HELP \nF - CHANGE COLOUR \nT - SNAPPING MODE ON/OFF (YOUR SAMPLE POINTS MAY SNAP TO THE GREY AXIS) \nM - EVENLY DISTRIBUTED NODES/CHEBYSHEV NODES \nG - GRID ON/OFF \nL - CLEAR GRID",
                   "Key Binds")


HelpMenu()


class PlanePoint:
    def __init__(self, p_x, p_y, colour=(0, 0, 0)):
        self.x = p_x
        self.y = p_y
        self.radius = 3
        self.colour = colour
        self.weight = 1

    def draw(self):
        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.radius)


class WeightHandle:
    def __init__(self, OwnerPoint):
        self.x = OwnerPoint.x
        self.y = OwnerPoint.y
        self.OwnerPoint = OwnerPoint
        self.length = 0
        self.dragging = False
        self.original_length = 0
        self.weight = 1

    def draw(self):
        pygame.draw.line(screen, handle_color, (self.OwnerPoint.x, self.OwnerPoint.y), (self.x, self.y), 2)


def MapCurve(set, w):
    global last_curve
    last_curve = [PlanePoint(p[0], p[1], current_colour) for p in BezierCurve(set, w, mode)]
    for last_point in last_curve:
        last_point.draw()


#  Pygame Setting
pygame.init()
screen_info = pygame.display.Info()
width, height = 1000, 1000
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("Bezier Curve")
clock = pygame.time.Clock()
fps = 120
font = pygame.font.Font(None, 18)


#  Global Variables
mode = True
white = (255, 255, 255)
handle_color = (0, 255, 0)
saved_curves = []
sample_points = []
handles = []
last_curve = []
snapping_x = []
snapping_y = []
snapping = True
current_colour = (0, 0, 0)
changes = False
current_handle = None
ID = 0
tape = False
pos_x = 0
pos_y = 0
grid = False


def DrawGrid():
    global snapping_x
    global snapping_y
    snapping_x = []
    snapping_y = []
    for li in range(0, 1000, 20):
        pygame.draw.line(screen, (200, 200, 200), (0, li), (1000, li), 1)
        pygame.draw.line(screen, (200, 200, 200), (li, 0), (li, 1000), 1)
        snapping_x.append(li)
        snapping_y.append(li)


#  Main loop
while True:
    x, y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                tape = True
                pos_x = x
                pos_y = y
                if 0 <= x <= 1000 and 0 <= y <= 1000:
                    xs, ys = False, False
                    if snapping:
                        for snap_x in snapping_x:
                            if abs(snap_x - x) <= 10:
                                x = snap_x
                                xs = True
                                break
                        for snap_y in snapping_y:
                            if abs(snap_y - y) <= 10:
                                y = snap_y
                                ys = True
                                break
                    changes = True
                    if not xs and not grid:
                        snapping_x.append(x)
                    if not ys and not grid:
                        snapping_y.append(y)
                    new_point = PlanePoint(x, y, current_colour)
                    sample_points.append(new_point)
                    handle = WeightHandle(new_point)
                    handles.append(handle)
            elif event.button == 3:
                for handle in handles:
                    if Distance(handle, pygame.mouse.get_pos()) <= 10:
                        current_handle = handle
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                handles = []
                sample_points = []
                last_curve = []
                tape = False
            elif event.key == pygame.K_r:
                handles = []
                sample_points = []
                saved_curves = []
                last_curve = []
                snapping_x = []
                snapping_y = []
                grid = False
                pos_x = 0
                pos_y = 0
                snapping = True
                current_colour = (0, 0, 0)
                changes = False
                current_handle = None
                tape = False
            elif event.key == pygame.K_p:
                pygame.image.save(screen, f"screenshot{ID}.png")
                ID += 1
            elif event.key == pygame.K_f:
                current_colour = "#{:06x}".format(random.randint(0, 0xFFFFFF))
            elif event.key == pygame.K_h:
                HelpMenu()
            elif event.key == pygame.K_m:
                mode = not mode
            elif event.key == pygame.K_s:
                saved_curves.append(last_curve)
                sample_points = []
                handles = []
            elif event.key == pygame.K_t:
                snapping = not snapping
            elif event.key == pygame.K_g:
                if not grid:
                    interv = 20
                    snapping_x = []
                    snapping_y = []
                    for i in range(0, 1000, interv):
                        snapping_x.append(i)
                        snapping_y.append(i)
                    grid = True
                else:
                    grid = False
                    snapping_x = []
                    snapping_y = []
            elif event.key == pygame.K_l:
                snapping_y = []
                snapping_x = []
                grid = False
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
        elif event.type == pygame.MOUSEMOTION:
            if current_handle is not None:
                handle = current_handle
                handle.length = handle.original_length + DistanceX(handle, (x, y))
                handle.weight = 1 + (handle.length / 50.0)
                handle.x = x
        elif event.type == pygame.MOUSEBUTTONUP:
            current_handle = None

    screen.fill(white)
    weight = []

    if tape:
        dist = DistanceXY((pos_x, pos_y), (x, y))
        text = font.render(f'Length: {dist:.2f}px', True, (0, 0, 0))
        screen.blit(text, (10, 10))

    for handle in handles:
        handle.draw()
        weight.append(handle.weight)

    for point in sample_points:
        point.draw()

    for s_y in snapping_y:
        pygame.draw.line(screen, (200, 200, 200), (0, s_y), (1000, s_y), 1)

    for s_x in snapping_x:
        pygame.draw.line(screen, (200, 200, 200), (s_x, 0), (s_x, 1000), 1)

    if changes and len(sample_points) > 1:
        MapCurve([(point.x, point.y) for point in sample_points], weight)
    else:
        for point in last_curve:
            point.draw()

    for curve in saved_curves:
        for point in curve:
            point.draw()

    pygame.display.flip()
    clock.tick(fps)
