# yisang.py

from character import Character, load_template
from utils import resource_path  # 导入 resource_path 函数
import os

class Unknown(Character):
    def __init__(self):
        # 使用 resource_path 函数转换路径
        template_folder = resource_path("img/characters/Unknown")
        
        icon_template = load_template(os.path.join(template_folder, "Unknown.png"))
        skill_templates = [
            load_template(os.path.join(template_folder, "Unknown_s1_down.png")),
            load_template(os.path.join(template_folder, "Unknown_s1_up.png")),
        ]
        self.ego_templates = [
            load_template(os.path.join(template_folder, "zayin_ego.png")),
            load_template(os.path.join(template_folder, "he_ego.png")),
        ]
        self.ego_names = [
            "Unknown_down",
        ]
        self.skill_names = [
            "Unknown\\Unknown_s1_down", 
            "Unknown\\Unknown_s1_up", 
        ]
        super().__init__("Unknown", icon_template, skill_templates)
        
        self.top_skill_templates = [
            load_template(os.path.join(template_folder, "Unknown_s1.png")),
        ]

    def detect_skills(self, game_window_handle):
        return super().detect_skills(game_window_handle, self.skill_templates, self.skill_names, self.top_skill_templates)

    def detect_dodge(self, game_window_image_gray):
        return super().detect_dodge(game_window_image_gray, self.skill_templates, self.skill_names)
