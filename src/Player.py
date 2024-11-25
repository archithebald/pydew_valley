import pygame

from Settings import *
from Timer import Timer

import os
import pathlib

class Player(pygame.sprite.Sprite):
    def __init__(self, position, group) -> None:
        super().__init__(group)
        
        self.import_assets()
        self.status = 'down'
        self.frame_index = 0
        
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=position)
        
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 400
        
        self.timers = {
            'tool_use': Timer(duration=350, func=self.use_tool),
            'tool_switch': Timer(duration=350),
            'seed_use': Timer(duration=350, func=self.use_seed),
            'seed_switch': Timer(duration=350)
        }
        
        self.tools = ["hoe", "axe", "water"]
        self.tool_index = 0
        self.selected_tool = self.tools[self.tool_index]
        
        self.seeds = ['corn', 'tomato']
        self.seed_index = 0
        self.selected_seed = self.seeds[self.seed_index]
        
    def use_tool(self):
        pass
    
    def use_seed(self):
        pass
        
    def input(self):
        pressed_keys = pygame.key.get_pressed()
        
        if not self.timers["tool_use"].active and not self.timers["seed_use"].active:
            if pressed_keys[pygame.K_z]:
                self.status = "up"
                self.direction.y = -1
            elif pressed_keys[pygame.K_s]:
                self.status = "down"
                self.direction.y = 1
            else:
                self.direction.y = 0
                
            if pressed_keys[pygame.K_d]:
                self.status = "right"            
                self.direction.x = 1
            elif pressed_keys[pygame.K_q]:
                self.status = "left"
                self.direction.x = -1
            else:
                self.direction.x = 0
                
            if pressed_keys[pygame.K_SPACE]:
                self.timers["tool_use"].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0
                
            if pressed_keys[pygame.K_a] and not self.timers["tool_switch"].active:                   
                self.timers["tool_switch"].activate()
                self.tool_index += 1
                
                if self.tool_index > (len(self.tools)-1):
                    self.tool_index = 0
                
                self.selected_tool = self.tools[self.tool_index]
                
                print(self.selected_tool)
                
            if pressed_keys[pygame.K_e]:
                self.timers["seed_use"].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0
                    
            if pressed_keys[pygame.K_r] and not self.timers["seed_switch"].active:                   
                self.timers["seed_switch"].activate()
                self.seed_index += 1
                    
                if self.seed_index > (len(self.seeds)-1):
                    self.seed_index = 0
                    
                self.selected_seed = self.seeds[self.seed_index]
                    
                print(self.selected_seed)
    
    def get_status(self):
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + "_idle"
        
        if self.timers["tool_use"].active:
            self.status = self.status.split('_')[0] + "_" + self.selected_tool
        
    def move(self, dt):
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
                                
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x
        
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y
                    
    def update_timers(self):
        for timer in self.timers.values():
            timer.update()
                    
    def update(self, dt):
        self.input()
        self.move(dt=dt)
        self.animate(dt=dt)
        self.get_status()
        self.update_timers()
        
    def directory_structure(self, folder: pathlib.Path):
        items = {}
        
        for item in folder.iterdir():
            if item.is_dir():
                items[item.name] = self.directory_structure(folder=item)
            else:
                items[item.name] = item 

        return items
        
    def import_assets(self):
        self.items = {}
        self.animations = {}
        
        self.graphics_folder_path = "E:\\WatermelonGame\\src\\graphics"
        self.graphics_folder = pathlib.Path(self.graphics_folder_path)
        
        if self.graphics_folder.exists():
            self.items = self.directory_structure(self.graphics_folder)
                    
        for folder in self.items["character"]:
            self.animations[folder] = []
            for animation in self.items["character"][folder]:
                path: pathlib.WindowsPath = str(self.items["character"][folder][animation])
                
                self.animations[folder].append(pygame.image.load(path).convert_alpha())
                
    def animate(self, dt):
        self.frame_index += 4 * dt
        
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
                    
        self.image = self.animations[self.status][int(self.frame_index)]