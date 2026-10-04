# particles.py
from OpenGL.GL import *
from OpenGL.GLUT import *
import random
import config

class Particle:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.vx = (random.random() - 0.5) * 0.3
        self.vy = (random.random() - 0.5) * 0.3
        self.vz = (random.random() - 0.5) * 0.3
        self.life = 1.0  

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz
        self.life -= 0.05 

class Explosion:
    def __init__(self, x, z):
        self.particles = []
        for _ in range(20):
            self.particles.append(Particle(x, 0.5, z))
        self.active = True

    def update(self):
        for p in self.particles:
            p.update()
        
        self.particles = [p for p in self.particles if p.life > 0]
        
        if len(self.particles) == 0:
            self.active = False

    def draw(self):
        for p in self.particles:
            glPushMatrix()
            glTranslatef(p.x, p.y, p.z)
            
            # Solid Color (No Blending)
            glColor3f(config.COLOR_PARTICLE[0], config.COLOR_PARTICLE[1], 0.0)
            
            # Shrink effect
            scale = 0.1 * p.life
            glScalef(scale, scale, scale)
            
            glutSolidCube(1.0)
            
            glPopMatrix()