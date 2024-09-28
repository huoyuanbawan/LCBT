# heathcliff.py

from character import Character, load_template
from utils import resource_path  # 假设 utils.py 文件中包含 resource_path 函数
import os

class Heathcliff(Character):
    def __init__(self):
        # 使用 resource_path 函数转换路径
        template_folder = resource_path("img/characters/Heathcliff")
        
        icon_template = load_template(os.path.join(template_folder, "Heathcliff.png"))
        skill_templates = [
            load_template(os.path.join(template_folder, "Heathcliff_s1_down.png")),
            load_template(os.path.join(template_folder, "Heathcliff_s2_down.png")),
            load_template(os.path.join(template_folder, "Heathcliff_s3_down.png")),
            load_template(os.path.join(template_folder, "Heathcliff_dodge_down.png")),
            load_template(os.path.join(template_folder, "Heathcliff_bodysack_down.png")),
            load_template(os.path.join(template_folder, "Heathcliff_bodysack_down.png")),
            load_template(os.path.join(template_folder, "Heathcliff_binds_down.png")),
            load_template(os.path.join(template_folder, "Heathcliff_s1_up.png")),
            load_template(os.path.join(template_folder, "Heathcliff_s2_up.png")),
            load_template(os.path.join(template_folder, "Heathcliff_s3_up.png"))
        ]
        self.ego_templates = [
            load_template(os.path.join(template_folder, "zayin_ego.png")),
            load_template(os.path.join(template_folder, "he_ego.png")),
            load_template(os.path.join(template_folder, "w_ego.png")),
        ]
        self.ego_names = [
            "Heathcliff_bodysack_down", "Heathcliff_bodysack_down", "Heathcliff_binds_down",
        ]
        self.skill_names = [
            "Heathcliff\\Heathcliff_s1_down", "Heathcliff\\Heathcliff_s2_down", "Heathcliff\\Heathcliff_s3_down",
            "Heathcliff\\Heathcliff_dodge_down", "Heathcliff\\Heathcliff_bodysack_down", "Heathcliff\\Heathcliff_bodysack_down", "Heathcliff\\Heathcliff_binds_down",
            "Heathcliff\\Heathcliff_s1_up", "Heathcliff\\Heathcliff_s2_up", "Heathcliff\\Heathcliff_s3_up",
        ]
        super().__init__("Heathcliff", icon_template, skill_templates)
        self.top_skill_templates = [
            load_template(os.path.join(template_folder, "Heathcliff_s1.png")),
            load_template(os.path.join(template_folder, "Heathcliff_s2.png")),
            load_template(os.path.join(template_folder, "Heathcliff_s3.png")),
            load_template(os.path.join(template_folder, "Heathcliff_dodge.png")),
            load_template(os.path.join(template_folder, "Heathcliff_bodysack.png")),
            load_template(os.path.join(template_folder, "Heathcliff_bodysack.png")),
            load_template(os.path.join(template_folder, "Heathcliff_binds.png")),
        ]

    def detect_skills(self, game_window_handle):
        return super().detect_skills(game_window_handle, self.skill_templates, self.skill_names, self.top_skill_templates)

    def detect_dodge(self, game_window_image_gray):
        return super().detect_dodge(game_window_image_gray, self.skill_templates, self.skill_names)
