from constants import *
import pygame
import math

carImage = pygame.image.load(CAR_FILE)
carImageResized = pygame.transform.scale(carImage, (CAR_WIDTH, CAR_HEIGHT))


def rot_center(image, rect, angle):
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    return rot_image,rot_rect


class Car:
    def __init__(self):
        self.posX = 1110
        self.posY = WINDOW_SIZE_H - 100
        self.speed = .5
        self.angle = 90

        self.right = False
        self.left = False

        self.isAccelerating = False
        self.carDrawed = carImageResized

        self.frontDistanceX = self.posX
        self.frontDistanceY = self.posY
        self.frontTotalDistance = 0

        self.coordenatesLineLeft = [self.posX, self.posY]
        self.coordenatesLineCenter = [self.posX, self.posY]
        self.coordenatesLineRight = [self.posX, self.posY]

        self.linesColor = LINES_COLOR
        self.linesThickness = 2

        self.longitudeLineLeft = 0
        self.longitudeLineCenter = 0
        self.longitudeLineRight = 0

        self.isGrowingLineLeft = True
        self.isGrowingLineCenter = True
        self.isGrowingLineRight = True

    @staticmethod
    def getAngleInRadians(angle):
        angleInRadians = angle * math.pi / 180
        return angleInRadians

    @staticmethod
    def getAngle(angle):
        howManyThreeSixtiesAre = angle // 360
        angleBetweeenZeroAndThreeSixty = angle - howManyThreeSixtiesAre * 360

        howManyNinetiesAre = angleBetweeenZeroAndThreeSixty // 90
        conjugatedAngle = 0
        if howManyNinetiesAre == 0:
            conjugatedAngle = angleBetweeenZeroAndThreeSixty - howManyNinetiesAre * 90
        elif howManyNinetiesAre == 1:
            conjugatedAngle = 180 - angleBetweeenZeroAndThreeSixty
        elif howManyNinetiesAre == 2:
            conjugatedAngle = angleBetweeenZeroAndThreeSixty - 180
        elif howManyNinetiesAre == 3:
            conjugatedAngle = 360 - angleBetweeenZeroAndThreeSixty
        section = howManyNinetiesAre + 1

        return [conjugatedAngle, section]

    def draw(self, window):
        self.accelerate()
        if self.left:
            self.angle += .75
        if self.right:
            self.angle -= .75

        oldRect = self.carDrawed.get_rect(center=(self.posX, self.posY))
        shipImg, newRect = rot_center(self.carDrawed, oldRect, self.angle)
        carRect = window.blit(shipImg, newRect)
        return carRect

    def initLines(self):
        self.isGrowingLineLeft = True
        self.isGrowingLineCenter = True
        self.isGrowingLineRight = True

        self.coordenatesLineLeft = [self.posX, self.posY]
        self.coordenatesLineCenter = [self.posX, self.posY]
        self.coordenatesLineRight = [self.posX, self.posY]

        self.longitudeLineLeft = 0
        self.longitudeLineCenter = 0
        self.longitudeLineRight = 0

    def accelerate(self):
        if self.isAccelerating:
            angleInDegrees = self.getAngle(self.angle)
            xComponent = math.cos(self.getAngleInRadians(angleInDegrees[0])) * self.speed
            yComponent = math.sin(self.getAngleInRadians(angleInDegrees[0])) * self.speed

            if angleInDegrees[1] == 1:
                yComponent *= -1
                xComponent *= 1
            elif angleInDegrees[1] == 2:
                yComponent *= -1
                xComponent *= -1
            elif angleInDegrees[1] == 3:
                yComponent *= 1
                xComponent *= -1
            elif angleInDegrees[1] == 4:
                yComponent *= 1
                xComponent *= 1

            self.posY += yComponent
            self.posX += xComponent
