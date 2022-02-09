from cgitb import text
from re import X
import pygame
from Button import Button
from InputBox import InputBox

class LoginScreen:
    def __init__(self, screenDimensions, socket):
        self.__socket = socket
        self.__screenDimensions = screenDimensions
        dispWidth = screenDimensions[0]
        dispHeight = screenDimensions[1]
        #Need 2 textboxes
        boxColourActive = (35,35,35)
        boxColourDormant = (30,30,30)
        self.__textColour = (255,255,255)

        x = 999
        font = pygame.font.SysFont("Courier New", x)
        while font.size("Username")[1] > 40:
            x -= 1
            font = pygame.font.SysFont("Courier New", x)

        self.__font = font

        #Boxlocations
        rectangleUsernameBox = pygame.rect.Rect((0,int(400 * dispHeight/1080)), (int(1000 * dispWidth / 1920), int(70 * dispHeight / 1080)))
        rectangleUsernameBox.centerx = dispWidth / 2
        self.__usernameBox = InputBox((255,255,255), boxColourActive, boxColourDormant, False, rectangleUsernameBox, dispHeight)

        rectanglePasswordBox = pygame.rect.Rect((0,int(600 * dispHeight/1080)), (int(1000 * dispWidth / 1920), int(70 * dispHeight / 1080)))
        rectanglePasswordBox.centerx = dispWidth / 2
        self.__passwordBox = InputBox((255,255,255), boxColourActive, boxColourDormant, True, rectanglePasswordBox, dispHeight)

        #Need confirm button
        buttonSize = (int(400 * dispWidth / 1920), int(60 * dispHeight / 1080))
        self.__continueButton = Button("Continue", (0,0), buttonSize, boxColourDormant, boxColourActive, self.__textColour, dispHeight)
        newCoords = (dispWidth / 2, 730 * dispHeight / 1080)
        self.__continueButton.SetLocation(newCoords)

    def main(self, window):
        #Variables used for conditions
        backspace = False
        timeSinceLastBackspace = 0
        timeBetweenBackspaces = 50
        usernameBoxSelected = False
        passWordBoxSelected = False
        control = False
        clock = pygame.time.Clock()
        loggedIn = False
        playerQuit = False
        waiting = False

        while not loggedIn and not playerQuit:
            #Deletes all userinput when client is waiting for a response
            if waiting:
                pygame.event.clear()
                control = False
                backspace = False

            #Handles all the input while the player is typing
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    playerQuit = True
                    self.__socket.EndConnection()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    clickLocation = pygame.mouse.get_pos()
                    if self.__usernameBox.CheckIfClicked(clickLocation):
                        self.__usernameBox.SetActive()
                        usernameBoxSelected = True

                    else:
                        self.__usernameBox.SetDormant()
                        usernameBoxSelected = False

                    if self.__passwordBox.CheckIfClicked(clickLocation):
                        self.__passwordBox.SetActive()
                        passWordBoxSelected = True

                    else:
                        self.__passwordBox.SetDormant()
                        passWordBoxSelected = False

                    if self.__continueButton.CheckIfHovering(clickLocation):
                        self.__continueButton.Pressed()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        backspace = True
                        
                        if self.__usernameBox.isActive:
                            self.__usernameBox.RemoveLetter(control)
                        elif self.__passwordBox.isActive:
                            self.__passwordBox.RemoveLetter(control)

                        timeSinceLastBackspace = -200

                    elif event.key == pygame.K_RETURN:
                        self.__continueButton.Pressed()

                    elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                        control = True

                    elif event.key == pygame.K_TAB:
                        if self.__usernameBox.isActive:
                            self.__usernameBox.SetDormant()
                            self.__passwordBox.SetActive()

                        else:
                            self.__passwordBox.SetDormant()
                            self.__usernameBox.SetActive()

                    else:
                        if self.__usernameBox.isActive:
                            self.__usernameBox.AddLetter(event.unicode)
                        elif self.__passwordBox.isActive:
                            self.__passwordBox.AddLetter(event.unicode)

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_BACKSPACE:
                        backspace = False

                    elif event.key == pygame.K_RETURN:
                        pass

                    elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                        control = False

            #Checks if autobackspace needs to delete a letter
            if backspace and timeSinceLastBackspace > timeBetweenBackspaces:
                if usernameBoxSelected:
                    self.__usernameBox.RemoveLetter(control)
                elif passWordBoxSelected:
                    self.__passwordBox.RemoveLetter(control)

                timeSinceLastBackspace = 0

            #Checks if the box should be highlighted
            if self.__continueButton.CheckIfHovering(pygame.mouse.get_pos()):
                self.__continueButton.SetActive()
            
            else:
                self.__continueButton.SetDormant()

            #Checks if the login details need to be sent to the server
            if self.__continueButton.GetPressedState() and not waiting:
                username = self.__usernameBox.text
                password = self.__passwordBox.text
                self.__socket.msgsToSend.append(f"!LOGIN:{username},{password}")
                self.__continueButton.SetText("Loading")
                waiting = True

            #Handles messages from server
            while self.__socket.receivedMsgs != []:
                if self.__socket.receivedMsgs[0] == "!PASSWORDCORRECT":
                    loggedIn = True
                
                elif self.__socket.receivedMsgs[0] == "!PASSWORDINCORRECT":
                    self.__continueButton.DePressed()
                    waiting = False
                    self.__usernameBox.text = ""
                    self.__passwordBox.text = ""
                    self.__continueButton.SetText("Continue")
                
                self.__socket.receivedMsgs.pop(0)

            #Time 
            clock.tick()
            timeSinceLastBackspace += clock.get_time()

            #Rendering screen
            window.fill((10,10,10))
            
            textRender = self.__font.render("Username", True, self.__textColour)
            window.blit(textRender, (self.__usernameBox.rectangle.x + 10 * self.__screenDimensions[0] / 1920, self.__usernameBox.rectangle.y - 90 * self.__screenDimensions[1] / 1080))
            textRender = self.__font.render("Password", True, self.__textColour)
            window.blit(textRender, (self.__passwordBox.rectangle.x + 10 * self.__screenDimensions[0] / 1920, self.__passwordBox.rectangle.y - 90 * self.__screenDimensions[1] / 1080))

            self.__usernameBox.DrawBox(window)
            self.__passwordBox.DrawBox(window)
            self.__continueButton.Render(window)
            pygame.display.update()
        

        #Returns false if the player quit before logging in 
        if playerQuit:
            return False

        else:
            return True