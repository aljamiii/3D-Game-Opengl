# game_state.py
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import config
import utils
import math 
from maze import Maze
from player import Player
from enemy import Enemy
from particles import Explosion 

class GameState:
    def __init__(self):
        self.menu_active = True
        self.current_level_index = 0
        
        self.maze = None
        self.player = None
        self.enemies = []
        self.explosions = [] 
        self.game_over = False
        self.won = False

    def start_level(self, level_index):
        self.menu_active = False
        self.current_level_index = level_index
        
        self.maze = Maze(level_index)
        self.player = Player(1, 1)
        self.enemies = []
        self.explosions = [] 
        self.game_over = False
        self.won = False
        
        for ex, ez in self.maze.enemies:
            self.enemies.append(Enemy(ex, ez))

    def restart(self):
        self.start_level(self.current_level_index)

    def update(self):
        if self.menu_active: return
        if self.game_over or self.won: return

        self.player.update()
        
        for exp in self.explosions:
            exp.update()
        self.explosions = [exp for exp in self.explosions if exp.active]

        for f in self.maze.fruits:
            if f['active']:
                if utils.dist(self.player.x, self.player.z, f['x'], f['z']) < 0.5:
                    f['active'] = False
                    self.player.fruits += 1
                    self.player.health += 1
        
        for p in self.maze.powerups:
            if p['active']:
                if utils.dist(self.player.x, self.player.z, p['x'], p['z']) < 0.5:
                    p['active'] = False
                    self.player.activate_powerup(p['type'])

        if self.maze.end_point:
            if utils.dist(self.player.x, self.player.z, *self.maze.end_point) < 1.0:
                self.won = True

        if not self.player.is_invincible():
            for e in self.enemies:
                if e.alive and utils.dist(self.player.x, self.player.z, e.x, e.z) < 0.5:
                    self.player.health -= 1
                    e.alive = False 
                    if self.player.health <= 0:
                        self.game_over = True
                    break 

    def update_enemies(self, did_shoot):
        if self.menu_active: return

        px, pz, pang = self.player.x, self.player.z, self.player.angle
        
        shot_succeeded = did_shoot
        
        # --- DAMAGE BOOST LOGIC (Instant Kill) ---
        if shot_succeeded and self.player.has_damage_boost():
            for e in self.enemies:
                if e.alive:
                    dx = e.x - px
                    dz = e.z - pz
                    dist = math.sqrt(dx*dx + dz*dz)
                    
                    if dist < 30.0:  
                        if not self.maze.check_line_of_sight(px, pz, e.x, e.z):
                            continue 
                            
                        angle_to_enemy = math.atan2(dz, dx)
                        angle_norm = pang % (2 * math.pi)
                        if angle_norm > math.pi:
                            angle_norm -= 2 * math.pi
                        
                        angle_diff = angle_to_enemy - angle_norm
                        while angle_diff > math.pi: angle_diff -= 2 * math.pi
                        while angle_diff < -math.pi: angle_diff += 2 * math.pi
                        
                        if abs(angle_diff) < 0.5: 
                            e.take_damage(10) # Instant Kill
                            self.explosions.append(Explosion(e.x, e.z))
        
        # --- NORMAL SHOT LOGIC (1 Damage) ---
        for e in self.enemies:
            if shot_succeeded and e.alive:
                if e.check_hit(px, pz, pang, self.maze):
                    e.take_damage(1) # Needs 2 hits
                    self.explosions.append(Explosion(e.x, e.z))
            
            e.update(self.player, shot_succeeded, self.maze)

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        if self.menu_active:
            utils.draw_text(280, 400, "THE LOST LABYRINTH")
            utils.draw_text(250, 350, "Select Map to Start:")
            utils.draw_text(250, 320, "1. The Snake")
            utils.draw_text(250, 290, "2. The Hallway")
            utils.draw_text(250, 260, "3. The Room")
            utils.draw_text(250, 230, "4. The Maze")
            utils.draw_text(250, 200, "5. The Spiral")
            return

        if self.game_over:
            utils.draw_text(320, 300, "GAME OVER")
            utils.draw_text(280, 270, "Press 'R' to Restart")
            return
        if self.won:
            utils.draw_text(320, 300, "YOU ESCAPED!")
            utils.draw_text(280, 270, "Press 'R' to Play Again")
            return

        self.player.apply_camera()
        self.maze.draw(self.player.x, self.player.z)
        
        for e in self.enemies:
            e.draw()

        for exp in self.explosions:
            exp.draw()

        self.player.draw_gun()
        
        utils.draw_crosshair()
        
        ui_text = f" Map: {self.current_level_index + 1} | Health: {self.player.health}" 
        utils.draw_text(10, 570, ui_text)
        
        if self.player.is_reloading:
            reload_percent = int((1.0 - self.player.reload_timer / self.player.reload_time) * 100)
            ammo_text = f"Ammo: RELOADING... {reload_percent}%"
        else:
            ammo_text = f"Ammo: {self.player.bullet_count}/{self.player.max_bullets}"
        utils.draw_text(10, 545, ammo_text)
        
        y_offset = 520
        if self.player.powerup_speed_timer > 0:
            utils.draw_text(10, y_offset, f"SPEED BOOST: {int(self.player.powerup_speed_timer)}s")
            y_offset -= 20
        if self.player.powerup_invincible_timer > 0:
            utils.draw_text(10, y_offset, f"INVINCIBLE: {int(self.player.powerup_invincible_timer)}s")
            y_offset -= 20
        if self.player.powerup_damage_timer > 0:
            utils.draw_text(10, y_offset, f"DAMAGE BOOST: {int(self.player.powerup_damage_timer)}s")
            y_offset -= 20
        if self.player.powerup_rapid_timer > 0:
            utils.draw_text(10, y_offset, f"RAPID FIRE: {int(self.player.powerup_rapid_timer)}s")
            y_offset -= 20