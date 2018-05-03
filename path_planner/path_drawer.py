from graphics import *
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
win = GraphWin("path_planner", SCREEN_WIDTH, SCREEN_HEIGHT)

## This needs work with screen size and scaling to be actually usable, but the basic idea works
class Drawer():
    def __init__(self, planes, path):
        vertices = []
        edges = []
        max_x = 0
        max_y = 0
        for p in planes:
            for x in p.vertices:
                if x[0] > max_x:
                    max_x = x[0]
                if x[1] > max_y:
                    max_y = x[1]
            vertices.append(p.vertices)
            edges.append(p.edges)
        for v in vertices:
            for v2 in v:
                Circle(Point(v2[0]*SCREEN_WIDTH/max_x, SCREEN_HEIGHT - v2[1]*SCREEN_HEIGHT/max_y), 5).draw(win)
        for e in edges:
            for e2 in e:
                Line(Point(e2[0][0]*SCREEN_WIDTH/max_x, SCREEN_HEIGHT - e2[0][1]*SCREEN_HEIGHT/max_y), Point(e2[1][0]*SCREEN_WIDTH/max_x, SCREEN_HEIGHT - e2[1][1]*SCREEN_HEIGHT/max_y)).draw(win)
        p3 = None
        p4 = None
        for p1, p2 in path:
            if ((p3 is not None and p4 is not None) and (p1,p2) is not path[0] and (p3,p4) is not path[-1]):
                Line(Point(p1*SCREEN_WIDTH/max_x, SCREEN_HEIGHT - p2*SCREEN_HEIGHT/max_y), Point(p3*SCREEN_WIDTH/max_x, SCREEN_HEIGHT - p4*SCREEN_HEIGHT/max_y)).draw(win)
            p3, p4 = p1, p2
        try:
            win.getMouse()
            win.close()
        except GraphicsError:
            pass
