from car import *
from map import *


def update_label(data, title, font, x, y, window):
    label = font.render("{} {}".format(title, data), 1, DATA_FONT_COLOR)
    window.blit(label, (x, y))


def update_data_labels(window, dt, game_time, font, lineLeft, lineCenter, lineRight):
    y_pos = 10
    gap = 10
    x_pos = 10
    update_label(round(1000/dt, 2), "FPS", font, x_pos, y_pos, window)
    update_label(round(game_time/1000, 2), "Game time", font, x_pos, y_pos + 2 * gap, window)

    update_label(round(lineLeft, 2), "Line Left", font, x_pos, y_pos + 4 * gap, window)
    update_label(round(lineCenter, 2), "Line Center", font, x_pos, y_pos + 6 * gap, window)
    update_label(round(lineRight, 2), "Line Right", font, x_pos, y_pos + 8 * gap, window)


def run_game():

    pygame.init()
    window = pygame.display.set_mode((WINDOW_SIZE_W, WINDOW_SIZE_H))
    pygame.display.set_caption("Learn to drive")

    running = True

    label_font = pygame.font.SysFont("monospace", DATA_FONT_SIZE)

    clock = pygame.time.Clock()
    game_time = 0

    car = Car()
    map = Map()

    determinantForInitLines = False

    while running:
        window.fill(WINDOW_BG_COLOR)  # Poner color
        dt = clock.tick(FPS)
        game_time += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:  # Izquierda
                    car.left = True
                if event.key == pygame.K_d:  # Derecha
                    car.right = True
                if event.key == pygame.K_w:  # Acelerar
                    car.isAccelerating = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:  # Izquierda
                    car.left = False
                if event.key == pygame.K_d:  # Derecha
                    car.right = False
                if event.key == pygame.K_w:  # Frenar
                    car.isAccelerating = False

        update_data_labels(window, dt, game_time, label_font,
                           car.longitudeLineLeft,
                           car.longitudeLineCenter,
                           car.longitudeLineRight)

        carRect = car.draw(window)
        map.createMap(window, carRect, car)

        if car.isAccelerating or car.right or car.left:  # is moving
            if determinantForInitLines:
                car.initLines()
                determinantForInitLines = False
            else:
                if (not car.isGrowingLineLeft) and (not car.isGrowingLineCenter) and (not car.isGrowingLineRight):
                    determinantForInitLines = True

        pygame.display.update()


if __name__== "__main__":
    run_game()


