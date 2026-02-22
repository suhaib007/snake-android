from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import NumericProperty, ListProperty
from kivy.clock import Clock
from kivy.core.window import Window
from random import randint
import sys


class SnakePart(Widget):
    pass


class SnakeGame(Widget):
    snake = ListProperty([])
    food = ListProperty([0, 0])
    direction = ListProperty([1, 0])  # [x, y] direction
    score = NumericProperty(0)
    game_over = NumericProperty(0)
    grid_size = NumericProperty(40)
    
    def __init__(self, **kwargs):
        super(SnakeGame, self).__init__(**kwargs)
        self.snake = [[5, 5], [4, 5], [3, 5]]  # Initial snake
        self.spawn_food()
        self.bind(size=self.on_size)
        Clock.schedule_interval(self.update, 0.15)  # 150ms = game speed
    
    def on_size(self, *args):
        pass
    
    def spawn_food(self):
        max_x = int(Window.width / self.grid_size) - 1
        max_y = int(Window.height / self.grid_size) - 1
        self.food = [randint(1, max_x), randint(1, max_y)]
    
    def update(self, dt):
        if self.game_over:
            return
        
        # Move snake
        head = self.snake[0]
        new_head = [head[0] + self.direction[0], head[1] + self.direction[1]]
        
        # Check boundaries
        max_x = int(Window.width / self.grid_size) - 1
        max_y = int(Window.height / self.grid_size) - 1
        
        if (new_head[0] < 0 or new_head[0] > max_x or
            new_head[1] < 0 or new_head[1] > max_y):
            self.game_over = 1
            return
        
        # Check self-collision
        if new_head in self.snake:
            self.game_over = 1
            return
        
        # Add new head
        self.snake.insert(0, new_head)
        
        # Check food collision
        if new_head == self.food:
            self.score += 10
            self.spawn_food()
        else:
            # Remove tail
            self.snake.pop()
    
    def on_touch_down(self, touch):
        if self.game_over:
            self.reset()
            return
        
        # Swipe controls
        dx = touch.x - Window.width / 2
        dy = touch.y - Window.height / 2
        
        if abs(dx) > abs(dy):
            # Horizontal swipe
            if dx > 0 and self.direction != [-1, 0]:
                self.direction = [1, 0]
            elif dx < 0 and self.direction != [1, 0]:
                self.direction = [-1, 0]
        else:
            # Vertical swipe
            if dy > 0 and self.direction != [0, -1]:
                self.direction = [0, 1]
            elif dy < 0 and self.direction != [0, 1]:
                self.direction = [0, -1]
    
    def reset(self):
        self.snake = [[5, 5], [4, 5], [3, 5]]
        self.direction = [1, 0]
        self.score = 0
        self.game_over = 0
        self.spawn_food()


class SnakeApp(App):
    def build(self):
        Window.fullscreen = False
        game = SnakeGame()
        return game


if __name__ == '__main__':
    SnakeApp().run()
