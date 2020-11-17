import math

def measureDistanceBetweenTwoPoints(p1X, p1Y, p2X, p2Y):
    xDelta = p1X - p2X
    yDelta = p1Y - p2Y
    distance = math.sqrt(xDelta ** 2 + yDelta ** 2)
    return distance

def getFunctionFromTwoPointsFrontDistance(centerP1X, centerP1Y, p2X, p2Y, xValue):
    xDelta = centerP1X - p2X
    yDelta = centerP1Y - p2Y

    if xDelta == 0:
        if centerP1Y > p2Y:  # Mirando arriba
            finalYValue = p2Y - xValue
        else:   # Mirando abajo
            finalYValue = p2Y + xValue
        return [xValue, finalYValue]
    m = yDelta / xDelta
    b = centerP1Y - (m * centerP1X)

    finalYValue = m * xValue + b
    return [xValue, finalYValue]


print(getFunctionFromTwoPointsFrontDistance(1, 1, 1, 2, 3))
