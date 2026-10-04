# maze.py
from OpenGL.GL import *
from OpenGL.GLUT import *
import config
import math
import copy

class Maze:
    def __init__(self, level_index=0):
        idx = level_index % len(config.MAPS)
        self.layout = copy.deepcopy(config.MAPS[idx])
        
        self.fruits = []
        self.enemies = []
        self.end_point = None
        self.powerups = []
        self.parse_map()

    def parse_map(self):
        for z in range(config.MAP_SIZE):
            for x in range(config.MAP_SIZE):
                val = self.layout[z][x]
                world_x = x * config.TILE_SIZE
                world_z = z * config.TILE_SIZE
                
                if val == config.FRUIT:
                    self.fruits.append({'x': world_x, 'z': world_z, 'active': True})
                    self.layout[z][x] = config.PATH 
                elif val == config.ENEMY_SPAWN:
                    self.enemies.append((world_x, world_z))
                    self.layout[z][x] = config.PATH 
                elif val == config.END_POINT:
                    self.end_point = (world_x, world_z)
                elif val in [config.POWERUP_SPEED, config.POWERUP_INVINCIBLE, 
                             config.POWERUP_DAMAGE, config.POWERUP_RAPID]:
                    self.powerups.append({
                        'type': val,
                        'x': world_x,
                        'z': world_z,
                        'active': True
                    })
                    self.layout[z][x] = config.PATH

    def is_wall(self, x, z):
        grid_x = int(round(x / config.TILE_SIZE))
        grid_z = int(round(z / config.TILE_SIZE))
        
        if 0 <= grid_x < config.MAP_SIZE and 0 <= grid_z < config.MAP_SIZE:
            return self.layout[grid_z][grid_x] == config.WALL
        return True 

    # --- NEW: Raycasting for Walls ---
    def check_line_of_sight(self, x1, z1, x2, z2):
        dx = x2 - x1
        dz = z2 - z1
        dist = math.sqrt(dx*dx + dz*dz)
        
        if dist == 0: return True
        
        step_size = 0.5
        steps = int(dist / step_size)
        
        vx = dx / dist * step_size
        vz = dz / dist * step_size
        
        cx, cz = x1, z1
        
        for _ in range(steps):
            cx += vx
            cz += vz
            if self.is_wall(cx, cz):
                return False 
                
        return True
    # ---------------------------------

    def draw(self, player_x, player_z):
        ts = config.TILE_SIZE
        
        for z in range(config.MAP_SIZE):
            for x in range(config.MAP_SIZE):
                world_x = x * ts
                world_z = z * ts
                
                d = math.sqrt((player_x - world_x)**2 + (player_z - world_z)**2)
                fog_factor = max(0.2, 1.0 - (d / 15.0)) 

                glPushMatrix()
                glTranslatef(world_x, 0, world_z)
                
                if self.layout[z][x] == config.WALL:
                    r, g, b = config.COLOR_WALL
                    glColor3f(r * fog_factor, g * fog_factor, b * fog_factor)
                    glutSolidCube(ts)
                
                elif self.layout[z][x] == config.PATH or self.layout[z][x] == config.END_POINT:
                    r, g, b = config.COLOR_GROUND
                    glColor3f(r * fog_factor, g * fog_factor, b * fog_factor)
                    glBegin(GL_QUADS)
                    glVertex3f(-ts/2, -ts/2, -ts/2)
                    glVertex3f(ts/2, -ts/2, -ts/2)
                    glVertex3f(ts/2, -ts/2, ts/2)
                    glVertex3f(-ts/2, -ts/2, ts/2)
                    glEnd()
                    
                    if self.layout[z][x] == config.END_POINT:
                        glColor3f(0, 0, 1 * fog_factor)
                        glBegin(GL_QUADS)
                        h = -ts/2 + 0.1
                        glVertex3f(-0.5, h, -0.5)
                        glVertex3f(0.5, h, -0.5)
                        glVertex3f(0.5, h, 0.5)
                        glVertex3f(-0.5, h, 0.5)
                        glEnd()

                glPopMatrix()

        for f in self.fruits:
            if f['active']:
                glPushMatrix()
                glTranslatef(f['x'], 0, f['z'])
                glColor3f(*config.COLOR_FRUIT)
                glutSolidSphere(0.3, 10, 10)
                glPopMatrix()
        
        for p in self.powerups:
            if p['active']:
                glPushMatrix()
                glTranslatef(p['x'], 0, p['z'])
                if p['type'] == config.POWERUP_SPEED:
                    glColor3f(*config.COLOR_POWERUP_SPEED)
                    glutSolidTorus(0.1, 0.3, 10, 10)
                elif p['type'] == config.POWERUP_INVINCIBLE:
                    glColor3f(*config.COLOR_POWERUP_INVINCIBLE)
                    glutSolidCube(0.4)
                elif p['type'] == config.POWERUP_DAMAGE:
                    glColor3f(*config.COLOR_POWERUP_DAMAGE)
                    glRotatef(-90, 1, 0, 0)
                    glutSolidCone(0.3, 0.5, 10, 10)
                elif p['type'] == config.POWERUP_RAPID:
                    glColor3f(*config.COLOR_POWERUP_RAPID)
                    glutSolidTetrahedron()
                glPopMatrix()