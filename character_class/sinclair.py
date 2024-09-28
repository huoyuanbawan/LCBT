# sinclair.py

from character import Character, load_template
from utils import resource_path  # 导入 resource_path 函数
import os

class Sinclair(Character):
    def __init__(self):
        # 使用 resource_path 函数转换路径
        template_folder = resource_path("img/characters/Sinclair")
        
        icon_template = load_template(os.path.join(template_folder, "Sinclair.png"))
        skill_templates = [
            load_template(os.path.join(template_folder, "Sinclair_s1_down.png")),
            load_template(os.path.join(template_folder, "Sinclair_s2_down.png")),
            load_template(os.path.join(template_folder, "Sinclair_s3_down.png")),
            load_template(os.path.join(template_folder, "Sinclair_dodge_down.png")),
            load_template(os.path.join(template_folder, "Sinclair_branch_down.png")),
            load_template(os.path.join(template_folder, "Sinclair_s1_up.png")),
            load_template(os.path.join(template_folder, "Sinclair_s2_up.png")),
            load_template(os.path.join(template_folder, "Sinclair_s3_up.png")),
        ]
        self.skill_names = [
            "Sinclair\\Sinclair_s1_down", "Sinclair\\Sinclair_s2_down", "Sinclair\\Sinclair_s3_down",
            "Sinclair\\Sinclair_dodge_down", "Sinclair\\Sinclair_branch_down",
            "Sinclair\\Sinclair_s1_up", "Sinclair\\Sinclair_s2_up", "Sinclair\\Sinclair_s3_up"
        ]
        self.ego_templates = [
            load_template(os.path.join(template_folder, "zayin_ego.png"))
        ]
        self.ego_names = [
            "Sinclair_branch_down",
        ]        
        super().__init__("Sinclair", icon_template, skill_templates)

        self.top_skill_templates = [
            load_template(os.path.join(template_folder, "Sinclair_s1.png")),
            load_template(os.path.join(template_folder, "Sinclair_s2.png")),
            load_template(os.path.join(template_folder, "Sinclair_s3.png")),
            load_template(os.path.join(template_folder, "Sinclair_dodge.png")),
            load_template(os.path.join(template_folder, "Sinclair_branch.png")),
        ]

    def detect_skills(self, game_window_handle):
        return super().detect_skills(game_window_handle, self.skill_templates, self.skill_names, self.top_skill_templates)

    def detect_dodge(self, game_window_image_gray):
        return super().detect_dodge(game_window_image_gray, self.skill_templates, self.skill_names)
