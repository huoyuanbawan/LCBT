# LamentYiSang.py

from character import Character, load_template
from utils import resource_path  # 导入 resource_path 函数
import os

class LamentYiSang(Character):
    def __init__(self):
        # 使用 resource_path 函数转换路径
        template_folder = resource_path("img/characters/LamentYiSang")
        
        icon_template = load_template(os.path.join(template_folder, "LamentYiSang.png"))
        skill_templates = [
            load_template(os.path.join(template_folder, "LamentYiSang_s1_down.png")),
            load_template(os.path.join(template_folder, "LamentYiSang_s2_down.png")),
            load_template(os.path.join(template_folder, "LamentYiSang_s3_down.png")),
            load_template(os.path.join(template_folder, "LamentYiSang_defend_down.png")),
            load_template(os.path.join(template_folder, "LamentYiSang_crow_down.png")),
            load_template(os.path.join(template_folder, "LamentYiSang_dimension_down.png")),
            load_template(os.path.join(template_folder, "LamentYiSang_sunshower_down.png")),
            load_template(os.path.join(template_folder, "LamentYiSang_s1_up.png")),
            load_template(os.path.join(template_folder, "LamentYiSang_s2_up.png")),
            load_template(os.path.join(template_folder, "LamentYiSang_s3_up.png"))
        ]
        self.ego_templates = [
            load_template(os.path.join(template_folder, "zayin_ego.png")),
            load_template(os.path.join(template_folder, "he_ego.png")),
            load_template(os.path.join(template_folder, "w_ego.png")),
        ]
        self.ego_names = [
            "LamentYiSang_crow_down","LamentYiSang_dimension_down",
        ]
        self.skill_names = [
            "LamentYiSang\\LamentYiSang_s1_down", "LamentYiSang\\LamentYiSang_s2_down", "LamentYiSang\\LamentYiSang_s3_down",
            "LamentYiSang\\LamentYiSang_defend_down", "LamentYiSang\\LamentYiSang_crow_down", "LamentYiSang\\LamentYiSang_dimension_down", "LamentYiSang\\LamentYiSang_sunshower_down",
            "LamentYiSang\\LamentYiSang_s1_up", "LamentYiSang\\LamentYiSang_s2_up", "LamentYiSang\\LamentYiSang_s3_up"
        ]
        super().__init__("LamentYiSang", icon_template, skill_templates)
        
        self.top_skill_templates = [
            load_template(os.path.join(template_folder, "LamentYiSang_s1.png")),
            load_template(os.path.join(template_folder, "LamentYiSang_s2.png")),
            load_template(os.path.join(template_folder, "LamentYiSang_s3.png")),
            load_template(os.path.join(template_folder, "LamentYiSang_defend.png")),
            load_template(os.path.join(template_folder, "LamentYiSang_crow.png")),
            load_template(os.path.join(template_folder, "LamentYiSang_dimension.png")),
            load_template(os.path.join(template_folder, "LamentYiSang_sunshower.png")),
        ]

    def detect_skills(self, game_window_handle):
        return super().detect_skills(game_window_handle, self.skill_templates, self.skill_names, self.top_skill_templates)

    def detect_dodge(self, game_window_image_gray):
        return super().detect_dodge(game_window_image_gray, self.skill_templates, self.skill_names)
