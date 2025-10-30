import pygame
import math
import random
import time

pygame.init()

WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🌄 FoForest Scenerest Sunrise & Sunset Loop with Birds")

clock = pygame.time.Clock()

GROUND = (60, 160, 80)
TREE_DARK = (0, 90, 60)
TREE_LIGHT = (0, 120, 80)
TENT_MAIN = (255, 180, 50)
TENT_SIDE = (230, 150, 30)
MOON_COLOR = (255, 255, 230)
SUN_COLOR = (255, 240, 100)
STAR_COLOR = (255, 255, 255)
BIRD_COLOR = (40, 40, 40)

stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT // 2)) for _ in range(100)]

birds = []
for _ in range(10):  
    birds.append({
        "x": random.randint(0, WIDTH),
        "y": random.randint(80, 250),
        "speed": random.uniform(1.5, 3.0),
        "wing_angle": random.uniform(0, math.pi),
        "direction": random.choice(["right", "left"]),
    })

def sky_color(time_of_day):
    """Smooth gradient between night, sunrise, day, sunset"""
    if time_of_day < 0.25:  
        t = time_of_day / 0.25
        return (int(20 + 80*t), int(30 + 120*t), int(60 + 120*t))
    elif time_of_day < 0.5:  
        t = (time_of_day - 0.25) / 0.25
        return (int(100 + 100*t), int(150 + 80*t), int(255 - 80*t))
    elif time_of_day < 0.75:  
        t = (time_of_day - 0.5) / 0.25
        return (int(200 + 30*t), int(230 - 80*t), int(175 - 60*t))
    else:  
        t = (time_of_day - 0.75) / 0.25
        return (int(230 - 200*t), int(150 - 120*t), int(100 + 20*t))

def draw_tree(x, y, scale, sway):
    """Simple pine tree with two layers"""
    points = [
        (x, y - 60*scale + sway),
        (x - 25*scale, y + 20*scale + sway),
        (x + 25*scale, y + 20*scale + sway)
    ]
    pygame.draw.polygon(screen, TREE_DARK, points)
    points2 = [
        (x, y - 40*scale + sway/2),
        (x - 20*scale, y + 40*scale + sway/2),
        (x + 20*scale, y + 40*scale + sway/2)
    ]
    pygame.draw.polygon(screen, TREE_LIGHT, points2)

def draw_tent(x, y):

    base_y = y
    pygame.draw.polygon(screen, TENT_MAIN, [(x, base_y - 60), (x + 100, base_y), (x, base_y)])
    pygame.draw.polygon(screen, TENT_SIDE, [(x, base_y - 60), (x, base_y), (x - 80, base_y)])
    pygame.draw.line(screen, (80, 40, 0), (x, base_y - 60), (x, base_y), 3)

def draw_sunmoon(time_of_day):
    angle = (time_of_day * 2 * math.pi) - math.pi / 2
    cx, cy = WIDTH // 2, HEIGHT // 1.2
    radius = 250
    sx = cx + radius * math.cos(angle)
    sy = cy + radius * math.sin(angle)

    if 0.25 <= time_of_day <= 0.75:  
        pygame.draw.circle(screen, SUN_COLOR, (int(sx), int(sy)), 35)
    else:  
        pygame.draw.circle(screen, MOON_COLOR, (int(sx), int(sy)), 25)
        draw_stars()

def draw_stars():
    for (x, y) in stars:
        brightness = random.randint(150, 255)
        pygame.draw.circle(screen, (brightness, brightness, brightness), (x, y), random.choice([1, 2]))

def draw_birds(time_of_day):
    if 0.25 <= time_of_day <= 0.75: 
        for bird in birds:
            if bird["direction"] == "right":
                bird["x"] += bird["speed"]
                if bird["x"] > WIDTH + 50:
                    bird["x"] = -50
                    bird["y"] = random.randint(80, 250)
            else:
                bird["x"] -= bird["speed"]
                if bird["x"] < -50:
                    bird["x"] = WIDTH + 50
                    bird["y"] = random.randint(80, 250)

            bird["wing_angle"] += 0.2
            flap = math.sin(bird["wing_angle"]) * 5

            if bird["direction"] == "right":
                pygame.draw.polygon(screen, BIRD_COLOR, [
                    (bird["x"], bird["y"]),
                    (bird["x"] - 8, bird["y"] + flap),
                    (bird["x"] - 16, bird["y"])
                ])
                pygame.draw.polygon(screen, BIRD_COLOR, [
                    (bird["x"], bird["y"]),
                    (bird["x"] - 8, bird["y"] - flap),
                    (bird["x"] - 16, bird["y"])
                ])
            else:
                pygame.draw.polygon(screen, BIRD_COLOR, [
                    (bird["x"], bird["y"]),
                    (bird["x"] + 8, bird["y"] + flap),
                    (bird["x"] + 16, bird["y"])
                ])
                pygame.draw.polygon(screen, BIRD_COLOR, [
                    (bird["x"], bird["y"]),
                    (bird["x"] + 8, bird["y"] - flap),
                    (bird["x"] + 16, bird["y"])
                ])

running = True
start_time = time.time()

while running:
    elapsed = (time.time() - start_time) % 20 
    t = elapsed / 20.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(sky_color(t))

    draw_sunmoon(t)

    pygame.draw.rect(screen, GROUND, (0, HEIGHT - 100, WIDTH, 100))

    wind = math.sin(time.time() * 2) * 3

    for i in range(-2, 12):
        draw_tree(70 * i + 40, HEIGHT - 120, 1.5, wind * (0.5 if i % 2 == 0 else 1))
    for i in range(-3, 13):
        draw_tree(70 * i + 20, HEIGHT - 140, 1.2, wind * (0.6 if i % 2 == 0 else 1))
    for i in range(-3, 13):
        draw_tree(70 * i + 60, HEIGHT - 160, 1.0, wind * (0.8 if i % 2 == 0 else 1))

    draw_tent(WIDTH // 2 + 50, HEIGHT - 50)

    draw_birds(t)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
