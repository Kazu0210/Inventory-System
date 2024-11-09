import pygame
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
import threading

def run_pygame():
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill((30, 30, 30))
        pygame.draw.circle(screen, (255, 0, 0), (200, 150), 50)
        pygame.display.flip()
        clock.tick(60)

# PyQt6 Main Window
app = QApplication([])
window = QMainWindow()
label = QLabel("PyQt6 Window with Embedded Pygame", window)
window.setGeometry(100, 100, 600, 400)
window.show()

# Run Pygame in a separate thread
pygame_thread = threading.Thread(target=run_pygame)
pygame_thread.start()

sys.exit(app.exec())
