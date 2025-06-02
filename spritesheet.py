import pygame
import os

class SpriteSheet:
    def __init__(self, folder_path):
        self.folder = folder_path

    def load_strip(self, filename, num_frames, frame_width=128, frame_height=128):
        path = os.path.join(self.folder, filename)
        sheet = pygame.image.load(path).convert_alpha()
        frames = []
        for i in range(num_frames):
            rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
            image = pygame.Surface(rect.size, pygame.SRCALPHA)
            image.blit(sheet, (0, 0), rect)
            frames.append(image)
        return frames
