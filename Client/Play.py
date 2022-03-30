import ctypes, pygame
from NewGame import Game

user32 = ctypes.windll.user32
#Prevents the screen from scaling with windows resolution scale
#System -> Display -> Scale and Layout
user32.SetProcessDPIAware()

window = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.display.set_caption("SpeedTyper")
pygame.font.init()

game = Game(window)
game.main()

if game.socket is not None:
    game.socket.EndConnection()

pygame.font.quit()
pygame.quit()