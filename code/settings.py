# GAME SETUP
WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE = 64
HITBOX_OFFSET = {
    "player": -26,
    "object": -40,
    "grass": -10,
    "invisible": 0,
}

# UI
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
MANA_BAR_WIDTH = 140
ITEM_BOX_SIZE = 80
UI_FONT = "../graphics/font/joystix.ttf"
UI_FONT_SIZE = 18

# GENERAL COLORS
WATER_COLOR = "#71ddee"
UI_BACKGROUND_COLOR = "#222222"
UI_BORDER_COLOR = "#111111"
TEXT_COLOR = "#EEEEEE"
MENU_TEXT_COLOR = "#FFFFFF"

# GENERAL UI COLORS
HEALTH_COLOR = "red"
MANA_COLOR = "blue"
UI_BORDER_COLOR_ACTIVE = "gold"

# WEAPONS DATA
weapon_data = {
    "sword": {"cooldown": 100, "damage": 15, "graphic": "../graphics/weapons/sword/full.png"},
    "lance": {"cooldown": 400, "damage": 30, "graphic": "../graphics/weapons/lance/full.png"},
    "axe": {"cooldown": 300, "damage": 20, "graphic": "../graphics/weapons/axe/full.png"},
    "rapier": {"cooldown": 50, "damage": 8, "graphic": "../graphics/weapons/rapier/full.png"},
    "sai": {"cooldown": 80, "damage": 10, "graphic": "../graphics/weapons/sai/full.png"},
}

# MAGIC DATA
magic_data = {
    "flame": {"strength": 5, "cost": 20, "graphic": "../graphics/particles/flame/fire.png"},
    "heal": {"strength": 20, "cost": 10, "graphic": "../graphics/particles/heal/heal.png"}
}

# ENEMY DATA
monster_data = {
    "python_error": {"health": 100, "score": 100, "damage": 20, "attack_type": "slash",
                     "attack_sound": "../audio/attack/slash.wav", "speed": 3, "resistance": 3, "attack_radius": 80,
                     "notice_radius": 360},
    "seg_fault": {"health": 300, "score": 250, "damage": 40, "attack_type": "claw",
                  "attack_sound": "../audio/attack/claw.wav", "speed": 2, "resistance": 3, "attack_radius": 120,
                  "notice_radius": 400},
    "2": {"health": 100, "score": 110, "damage": 8, "attack_type": "thunder",
          "attack_sound": "../audio/attack/fireball.wav", "speed": 4, "resistance": 3, "attack_radius": 60,
          "notice_radius": 350},
    "01": {"health": 70, "score": 120, "damage": 6, "attack_type": "leaf_attack",
           "attack_sound": "../audio/attack/slash.wav", "speed": 3, "resistance": 3, "attack_radius": 50,
           "notice_radius": 300},
}
