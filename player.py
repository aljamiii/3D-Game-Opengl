# player.py
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import random
import config

class Player:
    def __init__(self, start_x, start_z):
        self.x = start_x * config.TILE_SIZE
        self.z = start_z * config.TILE_SIZE
        self.angle = 0.0
        self.hydration = 100.0
        self.fruits = 0
        self.health = 2
        
        # Camera Shake
        self.shake_intensity = 0.0
        self.shake_offset_x = 0.0
        self.shake_offset_y = 0.0
        
        # Gun Animation
        self.recoil_offset = 0.0
        self.quadric = gluNewQuadric()
        
        # Ammo and Reload System
        self.bullet_count = 6
        self.max_bullets = 6
        self.is_reloading = False
        self.reload_timer = 0.0
        self.reload_time = 1.0  
        
        # Powerup Effects
        self.powerup_speed_timer = 0.0
        self.powerup_invincible_timer = 0.0
        self.powerup_damage_timer = 0.0
        self.powerup_rapid_timer = 0.0

    def update(self):
        if self.shake_intensity > 0:
            self.shake_offset_x = (random.random() - 0.5) * self.shake_intensity
            self.shake_offset_y = (random.random() - 0.5) * self.shake_intensity
            self.shake_intensity *= config.SHAKE_DECAY
            if self.shake_intensity < 0.05:
                self.shake_intensity = 0
                self.shake_offset_x = 0
                self.shake_offset_y = 0

        if self.recoil_offset > 0:
            self.recoil_offset -= 0.05
            if self.recoil_offset < 0:
                self.recoil_offset = 0
        
        # Handle Reload Timer
        if self.is_reloading:
            self.reload_timer -= 0.016 
            if self.reload_timer <= 0:
                self.is_reloading = False
                self.bullet_count = self.max_bullets
        
        # Update Powerup Timers
        if self.powerup_speed_timer > 0:
            self.powerup_speed_timer -= 0.016
        if self.powerup_invincible_timer > 0:
            self.powerup_invincible_timer -= 0.016
        if self.powerup_damage_timer > 0:
            self.powerup_damage_timer -= 0.016
        if self.powerup_rapid_timer > 0:
            self.powerup_rapid_timer -= 0.016

    def apply_camera(self):
        lx = math.cos(self.angle)
        lz = math.sin(self.angle)
        gluLookAt(
            self.x, 0.5, self.z,
            self.x + lx + self.shake_offset_x, 0.5 + self.shake_offset_y, self.z + lz,
            0.0, 1.0, 0.0
        )

    def draw_gun(self):
        glPushMatrix()
        glLoadIdentity()
        glClear(GL_DEPTH_BUFFER_BIT)
        gun_z = -0.5 + self.recoil_offset 
        glTranslatef(0.15, -0.15, gun_z) 
        
        # Stock
        glColor3f(0.55, 0.27, 0.07)
        glPushMatrix()
        glScalef(0.08, 0.1, 0.4)
        glutSolidCube(1.0)
        glPopMatrix()

        # Barrels
        glColor3f(0.3, 0.3, 0.3)
        glPushMatrix()
        glTranslatef(-0.02, 0.03, -0.2)
        gluCylinder(self.quadric, 0.02, 0.02, 0.6, 8, 1)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(0.02, 0.03, -0.2)
        gluCylinder(self.quadric, 0.02, 0.02, 0.6, 8, 1)
        glPopMatrix()
        
        # Flash
        if self.recoil_offset > 0.1:
            glColor3f(1.0, 1.0, 0.0)
            glPushMatrix()
            glTranslatef(0.0, 0.03, -0.8)
            glutSolidSphere(0.04, 8, 8)
            glPopMatrix()
        glPopMatrix()

    def move(self, direction, maze):
        move_speed = config.MOVE_SPEED
        if self.powerup_speed_timer > 0:
            move_speed *= 2.0 
        
        dx = math.cos(self.angle) * move_speed * direction
        dz = math.sin(self.angle) * move_speed * direction
        if not maze.is_wall(self.x + dx, self.z): self.x += dx
        if not maze.is_wall(self.x, self.z + dz): self.z += dz

    def rotate(self, direction):
        self.angle -= config.ROT_SPEED * direction

    def shoot(self):
        if self.powerup_rapid_timer > 0:
            self.shake_intensity = 0.8  
            self.recoil_offset = 0.2    
            return self.x, self.z, self.angle
        
        if self.is_reloading or self.bullet_count <= 0:
            return None, None, None 
        
        self.bullet_count -= 1
        
        if self.bullet_count == 0:
            self.is_reloading = True
            self.reload_timer = self.reload_time
        
        self.shake_intensity = 0.8  
        self.recoil_offset = 0.2    
        return self.x, self.z, self.angle

    def activate_powerup(self, powerup_type):
        if powerup_type == config.POWERUP_SPEED:
            self.powerup_speed_timer = config.POWERUP_DURATION
        elif powerup_type == config.POWERUP_INVINCIBLE:
            self.powerup_invincible_timer = config.POWERUP_DURATION
        elif powerup_type == config.POWERUP_DAMAGE:
            self.powerup_damage_timer = config.POWERUP_DURATION
        elif powerup_type == config.POWERUP_RAPID:
            self.powerup_rapid_timer = config.POWERUP_DURATION
    
    def is_invincible(self):
        return self.powerup_invincible_timer > 0
    
    def has_damage_boost(self):
        return self.powerup_damage_timer > 0