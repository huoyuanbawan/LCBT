# enemy_class/enemy.py
import cv2
import os
import numpy as np
import time
from utils import resource_path, get_screen  # 导入 resource_path 函数

class Enemy:
    def __init__(self, name, templates_folder):
        self.name = name
        self.templates_folder = templates_folder

    def detect_enemy(self, game_window_handle):
        game_window_image_gray = get_screen(game_window_handle)
        enemy_templates = self.load_enemy_templates()
        detected_enemies = []

        for template_name, template_path in enemy_templates.items():
            template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
            if template is None:
                print(f"未能读取模板图像：{template_path}")
                continue

            result = cv2.matchTemplate(game_window_image_gray, template, cv2.TM_CCOEFF_NORMED)
            locations = np.where(result >= 0.65)
            for loc in zip(*locations[::-1]):
                detected_enemies.append((loc, template.shape[1], template.shape[0], template_name, result[loc[1], loc[0]]))



        # 合并位置相近的敌人
        merged_enemies = self.merge_close_enemies(detected_enemies)

        return merged_enemies

    def merge_close_enemies(self, detected_enemies, threshold=50):
        if not detected_enemies:
            return []

        merged_enemies = []
        used = [False] * len(detected_enemies)

        for i, (loc1, w1, h1, template_name1, score1) in enumerate(detected_enemies):
            if used[i]:
                continue

            merged_enemy = (loc1, w1, h1, template_name1, score1)
            for j, (loc2, w2, h2, template_name2, score2) in enumerate(detected_enemies):
                if i != j and not used[j]:
                    if abs(loc1[0] - loc2[0]) <= threshold and abs(loc1[1] - loc2[1]) <= threshold:
                        if score2 > score1:
                            merged_enemy = ((loc1[0] + loc2[0]) // 2, (loc1[1] + loc2[1]) // 2), w2, h2, template_name2, score2
                        used[j] = True
            used[i] = True
            merged_enemies.append(merged_enemy)

        # 去掉分数，只保留位置和模板信息
        merged_enemies = [(loc, w, h, template_name) for loc, w, h, template_name, score in merged_enemies]

        return merged_enemies



    def load_enemy_templates(self):
        enemy_templates = {}
        for root, dirs, files in os.walk(self.templates_folder):
            for file in files:
                if file.endswith(".png"):
                    template_name = os.path.splitext(file)[0]
                    template_path = os.path.join(root, file)
                    # 使用 resource_path 函数来获取正确的路径
                    enemy_templates[template_name] = resource_path(template_path)
        return enemy_templates
