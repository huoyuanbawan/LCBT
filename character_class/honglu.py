# honglu.py

from character import Character, load_template
from utils import resource_path  # 假设 utils.py 文件中包含 resource_path 函数
import os

class HongLu(Character):
    def __init__(self):
        # 使用 resource_path 函数转换路径
        template_folder = resource_path("img/characters/HongLu")
        
        icon_template = load_template(os.path.join(template_folder, "HongLu.png"))
        skill_templates = [
            load_template(os.path.join(template_folder, "HongLu_s1_down.png")),
            load_template(os.path.join(template_folder, "HongLu_s2_down.png")),
            load_template(os.path.join(template_folder, "HongLu_s3_down.png")),
            load_template(os.path.join(template_folder, "HongLu_dodge_down.png")),
            load_template(os.path.join(template_folder, "HongLu_land_down.png")),
            load_template(os.path.join(template_folder, "HongLu_s1_up.png")),
            load_template(os.path.join(template_folder, "HongLu_s2_up.png")),
            load_template(os.path.join(template_folder, "HongLu_s3_up.png"))
        ]
        self.ego_templates = [
            load_template(os.path.join(template_folder, "zayin_ego.png"))
        ]
        self.ego_names = [
            "HongLu_land_down", 
        ]
        self.skill_names = [
            "HongLu\\HongLu_s1_down", "HongLu\\HongLu_s2_down", "HongLu\\HongLu_s3_down",
            "HongLu\\HongLu_dodge_down", "HongLu\\HongLu_land_down", 
            "HongLu\\HongLu_s1_up", "HongLu\\HongLu_s2_up", "HongLu\\HongLu_s3_up",
        ]
        super().__init__("HongLu", icon_template, skill_templates)
        self.top_skill_templates = [
            load_template(os.path.join(template_folder, "HongLu_s1.png")),
            load_template(os.path.join(template_folder, "HongLu_s2.png")),
            load_template(os.path.join(template_folder, "HongLu_s3.png")),
            load_template(os.path.join(template_folder, "HongLu_dodge.png")),
            load_template(os.path.join(template_folder, "HongLu_land.png")),
        ]

    def detect_skills(self, game_window_handle):
        return super().detect_skills(game_window_handle, self.skill_templates, self.skill_names, self.top_skill_templates)

    def detect_dodge(self, game_window_image_gray):
        return super().detect_dodge(game_window_image_gray, self.skill_templates, self.skill_names)
