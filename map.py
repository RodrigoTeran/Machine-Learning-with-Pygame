from constants import *
import pygame
import math

hexagonImage = pygame.image.load(HEXAGON_FILE)
hexagonImageResized = pygame.transform.scale(hexagonImage, (HEXAGON_WIDTH, HEXAGON_HEIGHT))

hexagonsPositions = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1],
    [1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1],
    [1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
    [1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1],
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

weightsOfCars = []

def measureDistanceBetweenTwoPoints(p1X, p1Y, p2X, p2Y):
    xDelta = p1X - p2X
    yDelta = p1Y - p2Y
    distance = math.sqrt(xDelta ** 2 + yDelta ** 2)
    return distance


def getSecondPointForReferenceCar(car, typePoint):
    hypothenuse = 50

    if typePoint == 45:
        if car.isGrowingLineLeft:
            hypothenuse = car.longitudeLineLeft + .1
        else:
            hypothenuse = car.longitudeLineLeft

    if typePoint == 0:
        if car.isGrowingLineCenter:
            hypothenuse = car.longitudeLineCenter + .1
        else:
            hypothenuse = car.longitudeLineCenter

    if typePoint == -45:
        if car.isGrowingLineRight:
            hypothenuse = car.longitudeLineRight + .1
        else:
            hypothenuse = car.longitudeLineRight

    centerP1X = car.posX
    centerP1Y = car.posY
    angleAndSection = car.getAngle(car.angle + typePoint)

    xComponent = math.cos(car.getAngleInRadians(angleAndSection[0])) * hypothenuse
    yComponent = math.sin(car.getAngleInRadians(angleAndSection[0])) * hypothenuse

    if angleAndSection[1] == 1:
        centerP1X += xComponent
        centerP1Y -= yComponent
    elif angleAndSection[1] == 2:
        centerP1X -= xComponent
        centerP1Y -= yComponent
    elif angleAndSection[1] == 3:
        centerP1X -= xComponent
        centerP1Y += yComponent
    elif angleAndSection[1] == 4:
        centerP1X += xComponent
        centerP1Y += yComponent

    if typePoint == 45:
        car.coordenatesLineLeft = [centerP1X, centerP1Y]
        car.longitudeLineLeft = hypothenuse

    if typePoint == 0:
        car.coordenatesLineCenter = [centerP1X, centerP1Y]
        car.longitudeLineCenter = hypothenuse

    if typePoint == -45:
        car.coordenatesLineRight = [centerP1X, centerP1Y]
        car.longitudeLineRight = hypothenuse


class Map:
    def __init__(self):
        self.generation = 1
        self.numberOfCar = 1
    @staticmethod
    def sortWeights():
        weightsOfCars.sort(key=lambda x: x[2], reverse=False)
        cutOff = int(len(weightsOfCars) * MUTATION_CUT_OFF)
        goodCars = weightsOfCars[0: cutOff]
        badCars = weightsOfCars[cutOff:]
        numBadToTake = int(len(weightsOfCars) * MUTATION_BAD_TO_KEEP)

        # TODO implementar learning

    def createMap(self, window, carsRect, cars):
        numberOfRow = 0

        for car in cars:
            car.lineLeftRect = pygame.draw.line(window, car.linesColor, (car.posX, car.posY),
                             (car.coordenatesLineLeft), car.linesThickness)
            car.lineCenterRect = pygame.draw.line(window, car.linesColor, (car.posX, car.posY),
                             (car.coordenatesLineCenter), car.linesThickness)
            car.lineRightRect = pygame.draw.line(window, car.linesColor, (car.posX, car.posY),
                             (car.coordenatesLineRight), car.linesThickness)

        dead = False
        for row in hexagonsPositions:
            numberOfColumn = 0
            for column in row:
                counter = 0
                for car in cars:
                    isDead = self.draw(window, column, numberOfColumn, numberOfRow, carsRect[counter], car,
                                       car.lineLeftRect,
                                       car.lineCenterRect,
                                       car.lineRightRect)
                    if isDead:
                        if len(weightsOfCars) == GENERATION_SIZE:
                            weightsOfCars[self.numberOfCar - 1] = [
                                [car.nnet.weightsInputHidden],
                                [car.nnet.weightsHiddenOutput],
                                [car.fitness]
                            ]
                        else:
                            weightsOfCars.append([
                                [car.nnet.weightsInputHidden],
                                [car.nnet.weightsHiddenOutput],
                                [car.fitness]
                            ])
                        if self.numberOfCar == GENERATION_SIZE:
                            self.generation += 1
                            self.numberOfCar = 1
                            Map.sortWeights()
                        else:
                            self.numberOfCar += 1
                        car.reset()
                        car.initLines()
                        dead = True
                        break
                    counter += 1
                    if dead: break
                if dead: break
                numberOfColumn += 1
            if dead: break
            numberOfRow += 1

    def checkCollision(self, hexagonRect, carRect):
        if hexagonRect.colliderect(carRect):
            return True
        else:
            return False

    def draw(self, window, column, numberOfColumn, numberOfRow, carRect, car,
             lineLeft,
             lineCenter,
             lineRight
        ):
        leftGap = 250
        upperGap = 22.5
        if column == 1:
            x = HEXAGON_WIDTH * numberOfColumn + leftGap
            if numberOfColumn % 2 == 0:
                y = HEXAGON_HEIGHT * numberOfRow + upperGap
            else:
                y = HEXAGON_HEIGHT * numberOfRow + upperGap

            hexagonRect = window.blit(hexagonImageResized, (x, y))
            isDead = self.checkCollision(hexagonRect, carRect)

            isContactLineLeft = self.checkCollision(hexagonRect, lineLeft)
            isContactLineCenter = self.checkCollision(hexagonRect, lineCenter)
            isContactLineRight = self.checkCollision(hexagonRect, lineRight)

            if isContactLineLeft:
                car.isGrowingLineLeft = False
            if isContactLineCenter:
                car.isGrowingLineCenter = False
            if isContactLineRight:
                car.isGrowingLineRight = False

            getSecondPointForReferenceCar(car, 45)
            getSecondPointForReferenceCar(car, 0)
            getSecondPointForReferenceCar(car, -45)

            return isDead

