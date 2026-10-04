# utils.py
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import config

def draw_text(x, y, text):
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, config.SCREEN_WIDTH, 0, config.SCREEN_HEIGHT)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glColor3f(1.0, 1.0, 1.0)
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))
        
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def dist(x1, z1, x2, z2):
    return math.sqrt((x2 - x1)**2 + (z2 - z1)**2)

def draw_crosshair():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, config.SCREEN_WIDTH, 0, config.SCREEN_HEIGHT)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    cx = config.SCREEN_WIDTH / 2
    cy = config.SCREEN_HEIGHT / 2
    size = 10 
    gap = 5   
    
    glColor3f(1.0, 1.0, 1.0)
    glLineWidth(2.0)
    glBegin(GL_LINES)
    glVertex2f(cx - size - gap, cy)
    glVertex2f(cx - gap, cy)
    glVertex2f(cx + gap, cy)
    glVertex2f(cx + size + gap, cy)
    glVertex2f(cx, cy + gap)
    glVertex2f(cx, cy + size + gap)
    glVertex2f(cx, cy - gap)
    glVertex2f(cx, cy - size - gap)
    glEnd()
    glLineWidth(1.0)
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)