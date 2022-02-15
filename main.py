from turtle import position
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from threading import Timer

# App/Window
app = Ursina(borderless = False)

class Player(Entity):
    def __init__(self,**kwargs):
        self.controller = FirstPersonController(speed=5,**kwargs)
        super().__init__(self.controller)

        self.cursor = Entity(parent=camera.ui, model='quad', color=color.black, scale=.009, rotation_z=45)

        self.hand_gun = Entity(
            parent=camera.ui,
            model="gun/ak47.obj",
            visible=True,
            texture="gun/ak47.png",
            scale=(1.5),
            position=(0.3,-0.3),
            rotation=Vec3(-76,20,0)
            )
        
        self.knife = Entity(
            parent=camera.ui,
            model="gun/sword.obj",
            visible=True,
            color=color.pink,
            scale=(0.05),
            position=(0.3,-0.4),
            rotation=Vec3(-70,-30,0)
            )

        self.weapons = [self.hand_gun,self.knife]
        self.current = 0
        self.switch_weapon()


    def switch_weapon(self):
        for i,v in enumerate(self.weapons):
            if i == self.current:
                v.visible = True
            else:
                v.visible = False


    def input(self,key):

        try:
            self.current=int(key) - 1
            self.switch_weapon()

        except ValueError:
            pass

        if key == "scroll up":
            self.current = (self.current+1) % len(self.weapons)
            self.switch_weapon()

        if key == "scroll down":
            self.current = (self.current-1) % len(self.weapons)
            self.switch_weapon()

        if held_keys["left mouse"]:
            if self.weapons[1]:
                hit = self.knife.position = (0.3,-0.5)
                self.knife.rotation=Vec3(-60,-30,0)
                def nothit():
                    self.knife.position=(0.3,-0.4)
                    self.knife.rotation=Vec3(-70,-30,0)
                if hit:
                    t = Timer(0.1, nothit)
                    t.start()
        if key == "left mouse down" and self.current == 0:
            self.bullets=Bullet(
                model="sphere",
                color=color.black,
                scale=0.05,
                position=self.controller.camera_pivot.world_position,
                rotation=self.controller.camera_pivot.world_rotation
            )

        if held_keys["shift"]:
            self.controller.speed = 9
        else:
            self.controller.speed = 5

    def update(self):
        self.controller.camera_pivot.y = 2 - held_keys["left control"]

class Bullet(Entity):
    def __init__(self,speed=200,lifetime=4,**kwargs):
        super().__init__(**kwargs)
        self.speed=speed
        self.lifetime=lifetime
        self.start=time.time()

    def update(self):
        ray = raycast(self.world_position,self.forward,distance=self.speed*time.dt)
        if not ray.hit and time.time() - self.start < self.lifetime:
            self.world_position += self.forward * self.speed * time.dt
        else:
            destroy(self)

ground = Entity(
    model="plane",
    color=color.lightyellow,
    collider="mesh",
    scale=(100*2,1,100*2)
)

wall_1 = Entity(
    model = "cube",
    collider = "box",
    scale=(8,10,1),
    position=(20,0),
    rotation=(0,0,0),
    texture="brick",
    texture_scale=(5,5),
    color=color.rgb(255, 187, 51)
)

wall_2 = Entity(
    model = "cube",
    collider = "box",
    scale=(1,10,20),
    position=(30,0),
    rotation=(0,0,0),
    texture="brick",
    texture_scale=(5,5),
    color=color.rgb(255, 195, 77)
)

enemy = Entity(
    model = "enemy/wendy.obj",
    texture="enemy/tex_wendy.jpg",
    position=(-62,1,-10.2),
    rotation=(0,90,0),
    scale=(5,5,5)
)

house1 = Entity(
    collider="mesh",
    model = "assets/Cottage_FREE.obj",
    texture="assets/colors.png",
    position=(-68,0,-10),
    rotation=(0,270,0),
    scale=(1)
)


road = Entity(
    model = "assets/Tjunction",
    position=(-50,0.1,-55),
    rotation=(0,270,0),
    scale=(10,0.2,10)
)

tree = Entity(
    model = "assets/tree.obj",
    collider="mesh",
    position=(-64,0.1,-25),
    rotation=(0,120,0),
    scale=(1,1,1)
)

city = Entity(
    model = "assets/tower.obj",
    texture="assets/textures/tower.jpg",
    collider="mesh",
    position=(-62,-1,5),
    rotation=(0,100,0),
    scale=(2)
)


roof_pos_up = 5.5
roof_pos = 25
y = 1
x = 100
z = 100

wall_3 = Entity(
    model = "cube",
    collider = "box",
    scale=(x,y,z),
    position=(roof_pos,roof_pos_up),
    rotation=(0,0,0),
    texture="brick",
    texture_scale=(5,5),
    color=color.rgb(255, 195, 77)
)

wall1 = duplicate(wall_1,z=8)
wall2 = duplicate(wall_1,z=16)
wall3 = duplicate(wall_2,z=8)


    
player=Player(position=(0,0,0))
sky = Sky()

app.run()