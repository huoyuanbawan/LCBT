# yisang.py

from character import Character, load_template
from utils import resource_path  # 导入 resource_path 函数
import os

class Ismael(Character):
    def __init__(self):
        # 使用 resource_path 函数转换路径
        template_folder = resource_path("img/characters/Ismael")
        
        icon_template = load_template(os.path.join(template_folder, "Ismael.png"))
        skill_templates = [
            load_template(os.path.join(template_folder, "Ismael_s1_down.png")),
            load_template(os.path.join(template_folder, "Ismael_s2_down.png")),
            load_template(os.path.join(template_folder, "Ismael_s3_down.png")),
            load_template(os.path.join(template_folder, "Ismael_defend_down.png")),
            load_template(os.path.join(template_folder, "Ismael_snagharpoon_down.png")),
            load_template(os.path.join(template_folder, "Ismael_wingbeat_down.png")),
            load_template(os.path.join(template_folder, "Ismael_blind_down.png")),
            load_template(os.path.join(template_folder, "Ismael_s1_up.png")),
            load_template(os.path.join(template_folder, "Ismael_s2_up.png")),
            load_template(os.path.join(template_folder, "Ismael_s3_up.png"))
        ]
        self.ego_templates = [
            load_template(os.path.join(template_folder, "zayin_ego.png")),
            load_template(os.path.join(template_folder, "he_ego.png")),
            load_template(os.path.join(template_folder, "w_ego.png")),
        ]
        self.ego_names = [
            "Ismael_snagharpoon_down","Ismael_blind_down",
        ]
        self.skill_names = [
            "Ismael\\Ismael_s1_down", "Ismael\\Ismael_s2_down", "Ismael\\Ismael_s3_down",
            "Ismael\\Ismael_defend_down", "Ismael\\Ismael_snagharpoon_down", "Ismael\\Ismael_wingbeat_down", "Ismael\\Ismael_blind_down", 
            "Ismael\\Ismael_s1_up", "Ismael\\Ismael_s2_up", "Ismael\\Ismael_s3_up"
        ]
        super().__init__("Ismael", icon_template, skill_templates)
        
        self.top_skill_templates = [
            load_template(os.path.join(template_folder, "Ismael_s1.png")),
            load_template(os.path.join(template_folder, "Ismael_s2.png")),
            load_template(os.path.join(template_folder, "Ismael_s3.png")),
            load_template(os.path.join(template_folder, "Ismael_defend.png")),
            load_template(os.path.join(template_folder, "Ismael_snagharpoon.png")),
            load_template(os.path.join(template_folder, "Ismael_wingbeat.png")),
            load_template(os.path.join(template_folder, "Ismael_blind.png")),
        ]

    def detect_skills(self, game_window_handle):
        return super().detect_skills(game_window_handle, self.skill_templates, self.skill_names, self.top_skill_templates)

    def detect_dodge(self, game_window_image_gray):
        return super().detect_dodge(game_window_image_gray, self.skill_templates, self.skill_names)
