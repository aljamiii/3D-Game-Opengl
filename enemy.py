# enemy.py
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import config
import utils

STATE_IDLE = 0
STATE_CHASE = 1

class Enemy:
    def __init__(self, x, z):
        self.x = x
        self.z = z
        self.state = STATE_IDLE
        self.speed = config.MOVE_SPEED * 0.25 
        self.quadric = gluNewQuadric()
        self.alive = True
        self.health = 2  # New Health Attribute

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.alive = False

    def check_hit(self, px, pz, p_angle, maze): 
        if not self.alive: return False
        
        dx = self.x - px
        dz = self.z - pz
        dist = math.sqrt(dx*dx + dz*dz)
        
        if dist > 15.0: return False

        # Raycast check for walls
        if not maze.check_line_of_sight(px, pz, self.x, self.z):
            return False 

        angle_to_enemy = math.atan2(dz, dx)
        p_angle = p_angle % (2 * math.pi)
        if p_angle > math.pi: p_angle -= 2 * math.pi
        
        angle_diff = angle_to_enemy - p_angle
        while angle_diff > math.pi: angle_diff -= 2 * math.pi
        while angle_diff < -math.pi: angle_diff += 2 * math.pi
        
        if abs(angle_diff) < 0.2:
            return True
        return False

    def update(self, player, did_shoot, maze):
        if not self.alive: return

        d = utils.dist(self.x, self.z, player.x, player.z)
        
        if d < 5.0:
            self.state = STATE_CHASE
        if did_shoot and d < 15.0:
            self.state = STATE_CHASE

        if self.state == STATE_CHASE:
            if d > 0.5:
                dx = (player.x - self.x) / d * self.speed
                dz = (player.z - self.z) / d * self.speed
                
                next_x = self.x + dx
                if not maze.is_wall(next_x, self.z):
                    self.x = next_x
                    
                next_z = self.z + dz
                if not maze.is_wall(self.x, next_z):
                    self.z = next_z

    def draw(self):
        if not self.alive: return

        glPushMatrix()
        glTranslatef(self.x, -0.5, self.z)
        
        # Visual Health Feedback (Darker red if damaged)
        if self.health == 1:
            glColor3f(0.5, 0.0, 0.0) 
        else:
            glColor3f(*config.COLOR_ENEMY) 
        
        glPushMatrix()
        glRotatef(-90, 1, 0, 0)
        gluCylinder(self.quadric, 0.3, 0.3, 1.5, 10, 10)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(0, 1.5, 0)
        gluSphere(self.quadric, 0.4, 10, 10)
        glPopMatrix()
        
        glPopMatrix()