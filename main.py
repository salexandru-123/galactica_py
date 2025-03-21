from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.vector import Vector
from random import randint

class Spaceship(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = './sprites/spaceship.png'  # Sostituisci con il percorso corretto
        self.size_hint = (None, None)
        self.size = (20, 20)
        self.pos = (Window.width / 2 - self.width / 2, 50)

    def on_touch_move(self, touch):
        if touch.y < Window.height / 3:  # Limita il movimento alla parte inferiore dello schermo
            self.x = touch.x - self.width / 2
        if touch.y > Window.height / 10:  # Limita il movimento alla parte inferiore dello schermo
            self.x = touch.x - self.width / 2

class Bullet(Image):
    def __init__(self, x, y, **kwargs):
        super().__init__(**kwargs)
        self.source = './sprites/bullet.png'
        self.size_hint = (None, None)
        self.size = (5, 10)
        self.pos = (x, y)

    def move(self):
        self.y += 10

class Enemy(Image):
    def __init__(self, x, y, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (20, 20)
        self.pos = (x, y)

class Game(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.spaceship = Spaceship()
        self.add_widget(self.spaceship)
        self.bullets = []
        self.enemies = []
        self.level = 1
        self.spawn_enemies()
        Clock.schedule_interval(self.update, 1/60.)
        Clock.schedule_interval(self.spawn_bullets, 0.5)

    def spawn_enemies(self):
        self.enemies = []
        enemy_types = ["./sprites/enemy1.png","./sprites/enemy2.png","./sprites/enemy3.png"]
        enemy_count = min(5+(self.level),10)
        half_enemy_count :int = int((enemy_count -1)/2) 
        pattern = self.level % 4
        print(pattern)
        if pattern == 0:  # Piramide
            for i in range(enemy_count-1):
                for j in range(i):
                    #make the enemies spawn in the middle
                    x = (Window.width/2 + int((20 * half_enemy_count)*2)) - (i * 40) + (j * 20)
                    y = Window.height - 30 - (j * 25) 
                    enemy = Enemy(x, y)
                    enemy.source = enemy_types[int(randint(0,2))]
                    self.enemies.append(enemy)
                    self.add_widget(enemy)
        elif pattern == 2:  # Quadrato
            for i in range(half_enemy_count):
                for j in range(half_enemy_count):
                    #center the square in the middle with any number of enemies
                    x = (Window.width/2 - int((25 * half_enemy_count)/2)) + (j * 25)
                    y = Window.height - 50 - (i * 25) 
                    enemy = Enemy(x, y)
                    enemy.source = enemy_types[int(randint(0,2))]
                    self.enemies.append(enemy)
                    self.add_widget(enemy)
        elif pattern == 3:  # Corona
            for i in range(enemy_count):
                
                x = (Window.width/2 - int((25 * half_enemy_count)/2)) + 30 * (i % 3) * (-1 if i <= half_enemy_count else 1)
                y = Window.height - 50 - (i % 3) * 25
                enemy = Enemy(x, y)
                enemy.source = enemy_types[int(randint(0,2))]
                self.enemies.append(enemy)
                self.add_widget(enemy)
        else:
            # Rettangolo
            cols = (enemy_count -1) // 2
            for i in range(4):
                for j in range(cols):
                    x = (Window.width/2 - int((25 * half_enemy_count)/2)) + j * 25
                    y = Window.height - (i * 25) - 50
                    enemy = Enemy(x, y)
                    enemy.source = enemy_types[int(randint(0,2))]
                    self.enemies.append(enemy)
                    self.add_widget(enemy)

    def spawn_bullets(self, dt):
        bullet = Bullet(self.spaceship.center_x - 10, self.spaceship.top)
        self.bullets.append(bullet)
        self.add_widget(bullet)

    def update(self, dt):
        
        for bullet in self.bullets:
            bullet.move()
            if bullet.y > Window.height:
                self.remove_widget(bullet)
                self.bullets.remove(bullet)
                
            for enemy in self.enemies:
                print(len(self.enemies))
                if bullet.collide_widget(enemy):
                    self.remove_widget(enemy)
                    self.remove_widget(bullet)
                    self.enemies.remove(enemy)
                    self.bullets.remove(bullet)
                    
                    if len(self.enemies) == 0:
                        self.level = self.level + 1
                        self.spawn_enemies()
                        
                    break
        

                    

class GalacticaApp(App):
    def build(self):
        return Game()

if __name__ == '__main__':
    GalacticaApp().run()