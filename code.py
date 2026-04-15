import pygame, math
pygame.init()

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("character customization panel whatever")

clock = pygame.time.Clock()
small_font = pygame.font.SysFont(None, 22)

pygame.key.start_text_input()

bg = pygame.image.load("background.jpg")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

hat_icon = pygame.image.load("hat.png")
color_icon = pygame.image.load("color.png")
pet_icon = pygame.image.load("pets.png")

hat_icon = pygame.transform.scale(hat_icon, (50, 50))
color_icon = pygame.transform.scale(color_icon, (50, 50))
pet_icon = pygame.transform.scale(pet_icon, (50, 50))

hat_imgs = [
    None,
    pygame.transform.scale(pygame.image.load("hat1.png"), (80, 60)),
    pygame.transform.scale(pygame.image.load("piratehat.png"), (130, 100)),
    pygame.transform.scale(pygame.image.load("party_hat.png"), (65, 55)),
    pygame.transform.scale(pygame.image.load("crown.png"), (80, 60)),
    pygame.transform.scale(pygame.image.load("duck.png"), (40, 40)),
]

pet_imgs = [
    None,
    pygame.transform.smoothscale(pygame.image.load("capy.png"), (110, 85)),
    pygame.transform.smoothscale(pygame.image.load("dino.png"), (110, 85)),
]

BASE_COLORS = [
    (255,0,0),(0,255,0),(0,0,255),(255,255,0),
    (255,165,0),(255,105,180),(138,43,226),(0,255,255),
    (255,255,255),(0,0,0),(128,0,0),(0,128,0),
    (0,0,128),(128,128,0),(128,0,128),(0,128,128),
    (192,192,192),(255,215,0),(255,20,147),(75,0,130)
]

GROUND_Y = 470

player1 = {
    "x": 250, "y": GROUND_Y,
    "color": 0, "hat": 0,
    "pet": 0,
    "category": None,
    "shade": 1.0,
    "panel_x": 120,
    "name": "",
    "active": False,
    "saved_flash": 0
}

player2 = {
    "x": 750, "y": GROUND_Y,
    "color": 1, "hat": 0,
    "pet": 0,
    "category": None,
    "shade": 1.0,
    "panel_x": 880,
    "name": "",
    "active": False,
    "saved_flash": 0
}

name_boxes = {
    "p1": pygame.Rect(player1["x"]-80, 50, 160, 40),
    "p2": pygame.Rect(player2["x"]-80, 50, 160, 40)
}

save_buttons = {
    "p1": pygame.Rect(player1["x"]+90, 50, 70, 40),
    "p2": pygame.Rect(player2["x"]+90, 50, 70, 40)
}

class ImageButton:
    def __init__(self, img, x, y):
        self.img = img
        self.rect = self.img.get_rect(topleft=(x, y))

    def draw(self, mouse):
        if self.rect.collidepoint(mouse):
            pygame.draw.rect(screen, (255,255,255),
                             self.rect.inflate(6,6), 2, border_radius=8)
        screen.blit(self.img, self.rect)

    def clicked(self, pos):
        return self.rect.collidepoint(pos)

p1_buttons = {
    "color": ImageButton(color_icon, 50, 200),
    "hat": ImageButton(hat_icon, 50, 270),
    "pet": ImageButton(pet_icon, 50, 340),
}

p2_buttons = {
    "color": ImageButton(color_icon, 900, 200),
    "hat": ImageButton(hat_icon, 900, 270),
    "pet": ImageButton(pet_icon, 900, 340),
}

def apply_shade(color, shade):
    return tuple(min(255, max(0, int(c * shade))) for c in color)

def draw_gradient(bar, base_color):
    width = int(bar.width)

    if width <= 0:
        return

    for i in range(width):
        shade = i / width
        col = apply_shade(base_color, shade)
        pygame.draw.line(
            screen,
            col,
            (bar.x + i, bar.y),
            (bar.x + i, bar.y + bar.height)
        )

def draw_options(player, side, mouse):
    options = []

    if not player["category"]:
        return options

    target_x = 120 if side == "left" else 780
    player["panel_x"] += (target_x - player["panel_x"]) * 0.2
    base_x = int(player["panel_x"])

    cols, size, spacing = 4, 22, 10
    rows = (len(BASE_COLORS) + cols - 1) // cols

    panel_w = cols*(size+spacing)+15
    panel = pygame.Rect(base_x-15, 320, panel_w, 200)
    pygame.draw.rect(screen, (40,40,70), panel, border_radius=15)

    if player["category"] == "color":

        for i, c in enumerate(BASE_COLORS):
            r, c2 = divmod(i, cols)

            rect = pygame.Rect(
                base_x + c2*(size+spacing),
                340 + r*(size+spacing),
                size, size
            )

            pygame.draw.rect(screen, c, rect, border_radius=5)

            if i == player["color"]:
                pygame.draw.rect(screen, (255,255,255), rect, 2, border_radius=5)

            options.append(("color", i, rect))

        slider_y = 340 + rows*(size+spacing) + 10
        bar = pygame.Rect(base_x, slider_y, panel_w-20, 10)

        draw_gradient(bar, BASE_COLORS[player["color"]])

        shade = player["shade"]
        shade = max(0.0, min(1.0, float(shade)))

        width = max(1, int(bar.width))
        knob_x = bar.x + int(shade * width)

        pygame.draw.circle(screen, (255,255,255), (knob_x, bar.y + 5), 6)

        options.append(("shade", bar, bar))

    elif player["category"] == "hat":

        for i in range(min(3, len(hat_imgs))):
            rect = pygame.Rect(base_x, 340 + i*60, 50, 50)
            pygame.draw.rect(screen, (60,60,90), rect, border_radius=8)

            if hat_imgs[i]:
                screen.blit(pygame.transform.scale(hat_imgs[i], (35,30)),
                            (rect.x+7, rect.y+10))

            options.append(("hat", i, rect))

        for j in range(3, len(hat_imgs)):
            rect = pygame.Rect(base_x + 70, 340 + (j-3)*60, 50, 50)
            pygame.draw.rect(screen, (60,60,90), rect, border_radius=8)

            if hat_imgs[j]:
                screen.blit(pygame.transform.scale(hat_imgs[j], (35,30)),
                            (rect.x+7, rect.y+10))

            options.append(("hat", j, rect))

    elif player["category"] == "pet":

        for i in range(len(pet_imgs)):
            rect = pygame.Rect(base_x, 340 + i*60, 50, 50)
            pygame.draw.rect(screen, (60,60,90), rect, border_radius=8)

            if pet_imgs[i]:
                screen.blit(pygame.transform.scale(pet_imgs[i], (35,30)),
                            (rect.x+7, rect.y+10))

            options.append(("pet", i, rect))

    return options

def draw_player(p, t):
    x = p["x"]
    base_y = p["y"]

    sway = math.sin(t*2) * 8
    leg_sway = math.sin(t*2 + 1) * 6
    bob = math.sin(t*2) * 4

    col = apply_shade(BASE_COLORS[p["color"]], p["shade"])

    foot_y = base_y + 120
    head_y = foot_y - 240 + bob
    head_r = 32

    body_top = head_y + head_r
    body_bottom = foot_y - 60

    pygame.draw.circle(screen, (0,0,0), (x, int(head_y)), head_r + 4)
    pygame.draw.circle(screen, col, (x, int(head_y)), head_r)

    pygame.draw.line(screen, (0,0,0),(x, body_top),(x, body_bottom),16)
    pygame.draw.line(screen, col,(x, body_top),(x, body_bottom),12)

    arm_y = body_top + 40

    pygame.draw.line(screen, (0,0,0),(x, arm_y),(x-75+sway, arm_y+30),16)
    pygame.draw.line(screen, col,(x, arm_y),(x-75+sway, arm_y+30),12)

    pygame.draw.line(screen, (0,0,0),(x, arm_y),(x+75+sway, arm_y+30),16)
    pygame.draw.line(screen, col,(x, arm_y),(x+75+sway, arm_y+30),12)

    left_foot = (x - 40 + leg_sway, foot_y)
    right_foot = (x + 40 - leg_sway, foot_y)

    pygame.draw.line(screen, (0,0,0),(x, body_bottom),left_foot,16)
    pygame.draw.line(screen, col,(x, body_bottom),left_foot,12)

    pygame.draw.line(screen, (0,0,0),(x, body_bottom),right_foot,16)
    pygame.draw.line(screen, col,(x, body_bottom),right_foot,12)

    hat = hat_imgs[p["hat"]]
    if hat:
        offset_y = -40
        if p["hat"] == 4:
            offset_y = -28
        screen.blit(hat, hat.get_rect(center=(x, head_y + offset_y)))

    if p["pet"] != 0:
        pet = pet_imgs[p["pet"]]

        # size ni pets
        pet = pygame.transform.smoothscale(pet, (230, 170))

        offset_x = 110
        pet_x = x - offset_x if x > WIDTH // 2 else x + offset_x

        bounce = math.sin(t * 3) * 3

        vertical_offset = 188  # baba - increase; taas - decrease

        ground_y = base_y + 120

        pet_rect = pet.get_rect()
        pet_y = ground_y - pet_rect.height + vertical_offset + bounce

        screen.blit(pet, pet.get_rect(midbottom=(pet_x, pet_y)))

def draw_name_ui(p, rect, save_rect):
    pygame.draw.rect(screen, (30,120,255), rect, border_radius=8)
    pygame.draw.rect(screen, (255,255,255), rect, 2, border_radius=8)

    text = p["name"] if p["name"] else "type your name..."
    color = (255,255,255) if p["name"] else (200,200,200)

    screen.blit(small_font.render(text, True, color),
                (rect.x+10, rect.y+10))

    pygame.draw.rect(screen, (40,40,40), save_rect, border_radius=8)
    pygame.draw.rect(screen, (255,255,255), save_rect, 2, border_radius=8)

    save_text = small_font.render("SAVE", True, (255,255,255))
    screen.blit(save_text, save_text.get_rect(center=save_rect.center))

    if p["saved_flash"] > 0:
        screen.blit(small_font.render("Saved!", True, (0,255,0)),
                    (rect.x, rect.y-20))
        p["saved_flash"] -= 1


running = True
dragging = None

while running:
    t = pygame.time.get_ticks()/1000
    screen.blit(bg, (0,0))
    mouse = pygame.mouse.get_pos()

    draw_player(player1, t)
    draw_player(player2, t)

    p1_opts = draw_options(player1, "left", mouse)
    p2_opts = draw_options(player2, "right", mouse)

    draw_name_ui(player1, name_boxes["p1"], save_buttons["p1"])
    draw_name_ui(player2, name_boxes["p2"], save_buttons["p2"])

    for b in p1_buttons.values(): b.draw(mouse)
    for b in p2_buttons.values(): b.draw(mouse)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            player1["active"] = name_boxes["p1"].collidepoint(mouse)
            player2["active"] = name_boxes["p2"].collidepoint(mouse)

            if save_buttons["p1"].collidepoint(mouse):
                player1["saved_flash"] = 120
                player1["active"] = False

            if save_buttons["p2"].collidepoint(mouse):
                player2["saved_flash"] = 120
                player2["active"] = False

            for key, b in p1_buttons.items():
                if b.clicked(mouse):
                    player1["category"] = key if player1["category"] != key else None

            for key, b in p2_buttons.items():
                if b.clicked(mouse):
                    player2["category"] = key if player2["category"] != key else None

            for opt in p1_opts:
                if opt[2].collidepoint(mouse):
                    if opt[0] == "shade":
                        dragging = ("p1", opt[1])
                    else:
                        player1[opt[0]] = opt[1]

            for opt in p2_opts:
                if opt[2].collidepoint(mouse):
                    if opt[0] == "shade":
                        dragging = ("p2", opt[1])
                    else:
                        player2[opt[0]] = opt[1]

        if event.type == pygame.KEYDOWN:
            for p in (player1, player2):
                if p["active"]:
                    if event.key == pygame.K_BACKSPACE:
                        p["name"] = p["name"][:-1]
                    else:
                        p["name"] += event.unicode

        if event.type == pygame.MOUSEBUTTONUP:
            dragging = None

    if dragging:
        pl, bar = dragging
        v = max(0, min(1, (mouse[0]-bar.x)/bar.width))
        if pl == "p1":
            player1["shade"] = v
        else:
            player2["shade"] = v

    pygame.display.update()
    clock.tick(60)

pygame.quit()
