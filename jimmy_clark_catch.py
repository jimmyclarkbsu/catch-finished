import pygame, simpleGE, random

"""
Jimmy Clark
A slide and catch game
Slide and Catch Part 1
"""
class Meat(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("meat.png")
        self.setSize(25, 25)
        self.minSpeed = 3
        self.maxSpeed = 8
        self.reset()
        
    def reset(self):
        #move to top of screen
        self.y = 10
        
        #x is random 0 - screen width
        self.x = random.randint(0, self.screenWidth)
        
        #dy is random minSpeed to maxSpeed
        self.dy = random.randint(self.minSpeed, self.maxSpeed)
        
    def checkBounds(self):
        if self.bottom > self.screenHeight:
            self.reset()

class Wolf(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("howl.png")
        self.setSize(90, 90)
        self.position = (320, 400)
        self.moveSpeed = 5
        
    def process(self):
        if self.isKeyPressed(pygame.K_LEFT):
            self.x -= self.moveSpeed
        if self.isKeyPressed(pygame.K_RIGHT):
            self.x += self.moveSpeed
            
class LblScore(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Score: 0"
        self.center = (100, 30)
        
        
class LblTime(simpleGE.Label):
    def __init__(self):
        super().__init__()
        self.text = "Time left: 10"
        self.center = (500, 30)
    

class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setImage("spider.png")
        
        self.sndBite = simpleGE.Sound("bite.mp3")
        self.numMeats = 10
        self.score = 0
        self.lblScore = LblScore()
        
        self.timer = simpleGE.Timer()
        self.timer.totalTime = 10
        self.lblTime = LblTime()
        
        self.wolf = Wolf(self)
        
        self.meats = []
        for i in range (self.numMeats):
            self.meats.append(Meat(self))
        self.sprites = [self.wolf,
                        self.meats,
                        self.lblScore,
                        self.lblTime]
        
    def process(self):
        for meat in self.meats:
            if meat.collidesWith(self.wolf):
                meat.reset()
                self.sndBite.play()
                self.score += 1
                self.lblScore.text = f"Score: {self.score}"
                
        self.lblTime.text = f"Time Left: {self.timer.getTimeLeft():.2f}"
        if self.timer.getTimeLeft() < 0:
            print(f"Score: (self.score)")
            self.stop()
                
class Instructions(simpleGE.Scene):
    def __init__(self, prevScore):
        super().__init__()
        
        self.prevScore = prevScore
        
        
        self.setImage("spider.png")
        self.response = "Quit"
        
        
        self.directions = simpleGE.MultiLabel()
        self.directions.textLines = [
        "You are the Wolf",
        "Move with left and right arrow keys",
        "Catch as much meat as you can",
        "in the time provided"
        "",
        "Good luck!"]
        
        self.directions.center = (320, 240)
        self.directions.size = (500, 250)
        
        
        self.btnPlay = simpleGE.Button()
        self.btnPlay.text = "Play"
        self.btnPlay.center = (100, 400)
        
        self.btnQuit = simpleGE.Button()
        self.btnQuit.text = "Quit"
        self.btnQuit.center = (540, 400)
        
        
        self.lblScore = simpleGE.Label()
        self.lblScore.text = "Last Score: 0"
        self.lblScore.center = (320, 400)
        
        self.lblScore.text = f"Last score: {self.prevScore}"
        
        self.sprites = [self.directions,
                        self.btnPlay,
                        self.btnQuit,
                        self.lblScore]
        
    
       
        
    def process(self):
        if self.btnPlay.clicked:
            self.response = "Play"
            self.stop()
            
        if self.btnQuit.clicked:
            self.response = "Quit"
            self.stop()
        
def main():
    
    keepGoing = True
    lastScore = 0
    
    
    while keepGoing:
        instructions = Instructions(lastScore)
        instructions.start()
        
        if instructions.response == "Play":
            game = Game()
            game.start()
            lastScore = game.score
            
        else:
            keepGoing = False
    
if __name__ == "__main__":
    main()
