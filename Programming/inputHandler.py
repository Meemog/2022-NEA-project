import pygame

class InputHandler:
    def __init__(self):
        self.typing = False

    def HandleInput(self, box):
        commands = []
        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                commands.append("QUIT")

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if box.collidepoint(pygame.mouse.get_pos()):
                    self.typing = True
                    clicked = True
                    
                else:
                    self.typing = False
                    clicked = True

            elif event.type == pygame.KEYDOWN and self.typing:
                if event.key == pygame.K_BACKSPACE:
                    commands.append("BACKSPACE DOWN")

                elif event.key == pygame.K_RETURN:
                    pass

                else:
                    commands.append(f"K{event.unicode}")
        
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKSPACE:
                    commands.append("BACKSPACE UP")

        if self.typing and clicked:
            commands.append("CLICKED ON BOX")

        elif not self.typing and clicked:
            commands.append("CLICKED OUT OF BOX")

        return commands