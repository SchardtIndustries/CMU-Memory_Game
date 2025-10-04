"""
add a hint feature
add a high score counter
add a you win screen
calculate final score based on time, hints used, and guesses
"""

from cmu_graphics import *
from types import SimpleNamespace
import random
import time
import json


HIGH_SCORE_FILE = "highscore.json"

def saveHighScore(score):
    data = {"highScore": score}
    with open(HIGH_SCORE_FILE, "w") as f:
        json.dump(data, f)

def loadHighScore():
    try:
        with open(HIGH_SCORE_FILE, "r") as f:
            data = json.load(f)
            return data.get("highScore", 0)
    except FileNotFoundError:
        return 0

def onAppStart(app):
    app.newHighScoreAchieved = False
    app.highScore = loadHighScore()
    app.width = 600
    app.height = 600
    app.r = 20
    app.delayTime = 0.5 # seconds
    app.inDelay = False
    app.timerStarted = False
    app.guessCount = 0
    app.hintCount = 0
    app.score = 0
    restartGame(app, level=1)

def restartGame(app, level):
    app.level = level
    app.dots = []
    app.selectedDots = []
    app.inDelay = False
    app.gameTimer = 0
    app.timerStarted = False
    app.hintCount = 0
    app.guessCount = 0
    app.score = 0
    app.gameWon = False
    for _ in range(5*level):
        number = random.randrange(100)
        for _ in range(2):
            cx, cy = getRandomDotLocation(app)
            color = getRandomColor()
            dot = makeDot(cx, cy, app.r, color, number)
            app.dots.append(dot)

def checkWin(app):
    if len(app.dots) == 0:
        finalScore = max(0, app.score - (app.hintCount * 5) - (app.guessCount * 2) - int(app.gameTimer))
        if finalScore > app.highScore:
            saveHighScore(finalScore)
            app.highScore = finalScore
            app.newHighScoreAchieved = True
        else:
            app.newHighScoreAchieved = False
        app.gameWon = True

def getRandomColor():
    colors = ["purple", "red", "blue", "green", "orange"]
    return random.choice(colors)

def getRandomDotLocation(app):
    for _ in range(100):
        cx = random.randrange(app.r, app.width - app.r)
        cy = random.randrange(100 + app.r, app.height - app.r)
        if locationIsGood(app, cx, cy):
            break
    return cx, cy

def locationIsGood(app, cx, cy):
    for dot in app.dots:
        d = distance(cx, cy, dot.cx, dot.cy)
        if d < 2 * app.r:
            return False
    return True

def distance(x1, y1, x2, y2):
    return ((x1 - x2)**2 + (y1 - y2)**2)**0.5

def makeDot(cx, cy, r, color, number):
    dot = SimpleNamespace()
    dot.cx = cx
    dot.cy = cy
    dot.radius = r
    dot.color = color
    dot.number = number
    return dot

def onMousePress(app, mouseX, mouseY):
    if not hasattr(app, 'timerStarted') or not app.timerStarted:
            # Start the timer here
            app.timerStartTime = time.time()
            app.timerStarted = True
    if app.inDelay:
        return
    dot = findDot(app, mouseX, mouseY)
    if dot is not None:
        if dot in app.selectedDots:
            return
        app.selectedDots.append(dot) 
        if len(app.selectedDots) == 2:
            app.guessCount += 1
            startDelay(app)

def startDelay(app):
    app.inDelay = True
    app.delayStartTime = time.time()


def checkSelectedDots(app):
    assert len(app.selectedDots) == 2
    dot1, dot2 = app.selectedDots
    if dot1.number == dot2.number:
        app.dots.remove(dot1)
        app.dots.remove(dot2)
        app.score += (10*app.level)
    app.selectedDots = []

def findDot(app, x, y):
    for dot in reversed(app.dots):
        if dotContainsPoint(dot, x, y):
            return dot
    return None

def dotContainsPoint(dot, x, y):
    d = distance(x, y, dot.cx, dot.cy)
    return d <= dot.radius

def onStep(app):
    if app.timerStarted:
        app.gameTimer += .028
    if len(app.dots) == 0:
        app.timerStarted = False
    if getattr(app, 'newHighScoreAchieved', False):
                app.highScore = loadHighScore()  # reload from file
                # Reset the flag
                app.newHighScoreAchieved = False
    if app.inDelay:
        elapsedTime = time.time() - app.delayStartTime
        if elapsedTime >= app.delayTime:
            app.inDelay= False
            checkSelectedDots(app)
    if not getattr(app, 'gameWon', False):
                checkWin(app)
    else:
        pass



def onKeyPress(app, key):
    if app.inDelay == True:
        return
    if key == 'h':
        app.hintCount += 1
        hintFeature(app)
    if key in '12345':
        level = int(key)
        restartGame(app, level)

def redrawAll(app):
    drawTitleAndInstructions(app)
    drawDots(app)
    if getattr(app, 'gameWon', False):
        youWinScreen(app)


def drawTitleAndInstructions(app):
    drawLabel('Memory Game', app.width/2, 20, size=16, bold=True)
    drawLabel('Click to match numbers (ignore colors)', app.width/2, 40, size=16)
    drawLabel('Press 1-5 for a new game at that level!', app.width/2, 60, size=16)
    drawLabel(f'Level: {app.level}', 50, 20, size=16)
    drawLabel(f'Time: {app.gameTimer:.1f}', app.width - 50, 20, size=16)
    drawLabel(f'Hints Used: {app.hintCount}', app.width - 50, 40, size=16)
    drawLabel(f'Score: {app.score}', 50, 40, size=16)
    drawLabel(f'High Score: {app.highScore}', 50, 60, size=16)
    drawLabel(f'Guesses: {app.guessCount}', app.width - 50, 60, size=16)
    youWinScreen(app)

def drawDots(app):
    for dot in app.dots:
        drawCircle(dot.cx, dot.cy, dot.radius, fill=dot.color, border='black', borderWidth=2)
        if dot in app.selectedDots:
            drawLabel(str(dot.number), dot.cx, dot.cy, size=12, bold=True, fill='white')

def youWinScreen(app):
    if len(app.dots) == 0:
        drawRect(0, 0, app.width, app.height, fill='lightgreen')
        drawLabel('You Win!', app.width/2, app.height/2 - 20, size=32, bold=True)
        finalScore = max(0, app.score - (app.hintCount * 5) - (app.guessCount * 2) - int(app.gameTimer))
        drawLabel(f'Final Score: {finalScore}', app.width/2, app.height/2 + 20, size=24)



def main():
    runApp()

main()