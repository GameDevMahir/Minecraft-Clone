from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

grass_texture = load_texture('assets/grass_block.png')
stone_texture = load_texture('assets/stone_block.png')
brick_texture = load_texture('assets/brick_block.png')
dirt_texture = load_texture('assets/dirt_block.png')
sky_texture = load_texture('assets/skybox.png')
arm_texture = load_texture('assets/arm_texture.png')
punch_sound = Audio('assets/punch_sound', loop = False, autoplay = False, volume = 0.1)

block_pick = 1
playerSpeed = 5
crouching = False

def update():
    global block_pick
    global playerSpeed
    global crouching

    if held_keys['left mouse'] or held_keys['right mouse']:
        hand.active()
    else:
        hand.passive()

    if held_keys['left shift']:
        playerSpeed = 10
    else:
        playerSpeed = 5

    player.speed = playerSpeed

    if held_keys['left control']:
        camera.position = Vec2((0,-0.3))
        crouching = True
    else:
        camera.position = Vec2((0,0))
        crouching = False 

    if held_keys['1']: block_pick = 1
    if held_keys['2']: block_pick = 2
    if held_keys['3']: block_pick = 3
    if held_keys['4']: block_pick = 4


class Voxel(Button):
    def __init__(self, position = (0,0,0), texture = grass_texture):
        super().__init__(
        parent = scene,
        position = position,
        model = 'assets/block',
        origin_y = 0.5,
        texture = texture,
        color = color.color(0,0,random.uniform(0.9,1)),
        scale = 0.5
    )

    def input(self, key):
        if self.hovered:
            if key == 'right mouse down':
                punch_sound.play()
                if block_pick == 1: voxel = Voxel(position = self.position + mouse.normal, texture = grass_texture)
                if block_pick == 2: voxel = Voxel(position = self.position + mouse.normal, texture = stone_texture)
                if block_pick == 3: voxel = Voxel(position = self.position + mouse.normal, texture = brick_texture)
                if block_pick == 4: voxel = Voxel(position = self.position + mouse.normal, texture = dirt_texture)

            if key == 'left mouse down':
                punch_sound.play()
                destroy(self)

class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent = scene,
            model = 'sphere',
            texture = sky_texture,
            scale = 150,
            double_sided = True
        )

class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent = camera.ui,
            model = 'assets/arm',
            texture = arm_texture,
            scale = 0.2,
            rotation = Vec3((150, -20, 0)),
            position = Vec2((1,-0.6))
        )

    def active(self):
        self.position = Vec2(0.8,-0.5)

    def passive(self):
        self.position = Vec2(1,-0.6)

class Hotbar(Entity):
    def __init__(self):
        super().__init__(
            parent = camera.ui,
            model = 'quad',
            texture = 'assets/mchotbar.png',
            scale = (1,0.5),
            texture_scale = (1,1),
            position = Vec2((0,-0.4))
        )

for z in range(20):
    for x in range(20):
        voxel = Voxel(position = (x,0,z))

sky = Sky()
hand = Hand()
hotbar = Hotbar()

player = FirstPersonController(jump_height = 1.25, gravity = 0.3, jump_duration = 0.35)

app.run()