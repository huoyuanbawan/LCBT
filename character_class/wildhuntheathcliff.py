# WildHuntHeathcliff.py

from character import Character, load_template
from utils import resource_path  # 假设 utils.py 文件中包含 resource_path 函数
import os

class WildHuntHeathcliff(Character):
    def __init__(self):
        # 使用 resource_path 函数转换路径
        template_folder = resource_path("img/characters/WildHuntHeathcliff")
        
        icon_template = load_template(os.path.join(template_folder, "WildHuntHeathcliff.png"))
        skill_templates = [
            load_template(os.path.join(template_folder, "WildHuntHeathcliff_s1_down.png")),
            load_template(os.path.join(template_folder, "WildHuntHeathcliff_s2_down.png")),
            load_template(os.path.join(template_folder, "WildHuntHeathcliff_s3_down.png")),
            load_template(os.path.join(template_folder, "WildHuntHeathcliff_s4_down.png")),
            load_template(os.path.join(template_folder, "WildHuntHeathcliff_defend_down.png")),
            load_template(os.path.join(template_folder, "WildHuntHeathcliff_bodysack_down.png")),
            load_template(os.path.join(template_folder, "WildHuntHeathcliff_bodysack_down.png")),
            load_template(os.path.join(template_folder, "WildHuntHeathcliff_binds_down.png")),
            load_template(os.path.join(template_folder, "WildHuntHeathcliff_s1_up.png")),
            load_template(os.path.join(template_folder, "WildHuntHeathcliff_s2_up.png")),
            load_template(os.path.join(template_folder, "WildHuntHeathcliff_s3_up.png")),
            load_template(os.path.join(template_folder, "WildHuntHeathcliff_s4_up.png"))
        ]
        self.ego_templates = [
            load_template(os.path.join(template_folder, "zayin_ego.png")),
            load_template(os.path.join(template_folder, "he_ego.png")),
            load_template(os.path.join(template_folder, "w_ego.png")),
        ]
        self.ego_names = [
            "WildHuntHeathcliff_bodysack_down", "WildHuntHeathcliff_bodysack_down", "WildHuntHeathcliff_binds_down",
        ]
        self.skill_names = [
            "WildHuntHeathcliff\\WildHuntHeathcliff_s1_down", "WildHuntHeathcliff\\WildHuntHeathcliff_s2_down", "WildHuntHeathcliff\\WildHuntHeathcliff_s3_down", "WildHuntHeathcliff\\WildHuntHeathcliff_s4_down",
            "WildHuntHeathcliff\\WildHuntHeathcliff_defend_down", "WildHuntHeathcliff\\WildHuntHeathcliff_bodysack_down", "WildHuntHeathcliff\\WildHuntHeathcliff_bodysack_down", "WildHuntHeathcliff\\WildHuntHeathcliff_binds_down",
            "WildHuntHeathcliff\\WildHuntHeathcliff_s1_up", "WildHuntHeathcliff\\WildHuntHeathcliff_s2_up", "WildHuntHeathcliff\\WildHuntHeathcliff_s3_up", "WildHuntHeathcliff\\WildHuntHeathcliff_s4_up",
        ]
        super().__init__("WildHuntHeathcliff", icon_template, skill_templates)
        self.top_skill_templates = [
            load_template(os.path.join(template_folder, "WildHuntHeathcliff_s1.png")),
            load_template(os.path.join(template_folder, "WildHuntHeathcliff_s2.png")),
            load_template(os.path.join(template_folder, "WildHuntHeathcliff_s3.png")),
            load_template(os.path.join(template_folder, "WildHuntHeathcliff_s4.png")),
            load_template(os.path.join(template_folder, "WildHuntHeathcliff_defend.png")),
            load_template(os.path.join(template_folder, "WildHuntHeathcliff_bodysack.png")),
            load_template(os.path.join(template_folder, "WildHuntHeathcliff_bodysack.png")),
            load_template(os.path.join(template_folder, "WildHuntHeathcliff_binds.png")),
        ]

    def detect_skills(self, game_window_handle):
        return super().detect_skills(game_window_handle, self.skill_templates, self.skill_names, self.top_skill_templates)

    def detect_dodge(self, game_window_image_gray):
        return super().detect_dodge(game_window_image_gray, self.skill_templates, self.skill_names)