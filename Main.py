from cmu_graphics import *
from types import SimpleNamespace
import random
import time

def onAppStart(app):
    app.r = 20
    restartGame(app, level=1)

def restartGame(app, level):
    assert 1 <= level <= 3
    app.level = level
    app.dots = []
    app.selectedDots = []
    for _ in range(5*level):
        number = random.randrange(100)
        for _ in range(2):
            cx, cy = getRandomDotLocation(app)
            color = getRandomColor()
            dot = makeDot(cx, cy, app.r, color, number)
            app.dots.append(dot)

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
    dot = findDot(app, mouseX, mouseY)
    if dot is not None:
        app.selectedDots.append(dot)    
        
def findDot(app, x, y):
    for dot in reversed(app.dots):
        if dotContainsPoint(dot, x, y):
            return dot
    return None

def dotContainsPoint(dot, x, y):
    d = distance(x, y, dot.cx, dot.cy)
    return d <= dot.radius

def onStep(app):
    pass

def onKeyPress(app, key):
    if key in '123':
        level = int(key)
        restartGame(app, level)

def redrawAll(app):
    drawTitleAndInstructions(app)
    drawDots(app)


def drawTitleAndInstructions(app):
    drawLabel('Memory Game', app.width/2, 20, size=16, bold=True)
    drawLabel('Click to match numbers (ignore colors)', app.width/2, 40, size=16)
    drawLabel('Press 1-3 for a new game at that level!', app.width/2, 60, size=16)

def drawDots(app):
    for dot in app.dots:
        drawCircle(dot.cx, dot.cy, dot.radius, fill=dot.color, border='black', borderWidth=2)
        if dot in app.selectedDots:
            drawLabel(str(dot.number), dot.cx, dot.cy, size=12, bold=True, fill='white')

def main():
    runApp()

main()