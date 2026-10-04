# main.py
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
import time
import config
from game_state import GameState

game = None
last_frame_time = 0
target_fps = 60
frame_delay = 1.0 / target_fps

def display():
    if game: game.draw()
    glutSwapBuffers()

def idle():
    global last_frame_time
    current_time = time.time()
    elapsed = current_time - last_frame_time
    
    if elapsed < frame_delay:
        return
    
    last_frame_time = current_time
    
    if game:
        game.update()
        game.update_enemies(False) 
    glutPostRedisplay()

def mouse_click(button, state, x, y):
    if not game: return
    if game.menu_active: return

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        px, pz, ang = game.player.shoot()
        if px is not None:
            game.update_enemies(True)

def keyboard(key, x, y):
    if not game: return
    
    # --- MENU CONTROLS ---
    if game.menu_active:
        if key == b'1': game.start_level(0)
        elif key == b'2': game.start_level(1)
        elif key == b'3': game.start_level(2)
        elif key == b'4': game.start_level(3)
        elif key == b'5': game.start_level(4)
        elif key == b'\x1b': sys.exit()
        return
    # ---------------------

    # --- GAME CONTROLS ---
    if key == b'r':
        game.restart()
    elif key == b'w':
        game.player.move(1, game.maze)
    elif key == b's':
        game.player.move(-1, game.maze)
    elif key == b'a':
        game.player.rotate(1)
    elif key == b'd':
        game.player.rotate(-1)
    elif key == b' ': 
        px, pz, ang = game.player.shoot()
        if px is not None:
            game.update_enemies(True)
    elif key == b'\x1b':
        game.menu_active = True
    # ---------------------

def init_gl():
    glClearColor(*config.COLOR_SKY, 1.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(config.FOV, config.SCREEN_WIDTH/config.SCREEN_HEIGHT, config.NEAR_CLIP, config.FAR_CLIP)
    glMatrixMode(GL_MODELVIEW)

def main():
    global game
    global last_frame_time
    last_frame_time = time.time()
    
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
    glutCreateWindow(config.WINDOW_TITLE)
    
    init_gl()
    game = GameState()
    
    glutDisplayFunc(display)
    glutIdleFunc(idle)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse_click)
    
    glutMainLoop()

if __name__ == "__main__":
    main()