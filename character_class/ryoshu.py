# ryoshu.py

from character import Character, load_template
from utils import resource_path  # 导入 resource_path 函数
import os

class RyoShu(Character):
    def __init__(self):
        # 使用 resource_path 函数转换路径
        template_folder = resource_path("img/characters/RyoShu")
        
        icon_template = load_template(os.path.join(template_folder, "RyoShu.png"))
        skill_templates = [
            load_template(os.path.join(template_folder, "RyoShu_s1_down.png")),
            load_template(os.path.join(template_folder, "RyoShu_s2_down.png")),
            load_template(os.path.join(template_folder, "RyoShu_s3_down.png")),
            load_template(os.path.join(template_folder, "RyoShu_dodge_down.png")),
            load_template(os.path.join(template_folder, "RyoShu_forest_down.png")),
            load_template(os.path.join(template_folder, "RyoShu_s1_up.png")),
            load_template(os.path.join(template_folder, "RyoShu_s2_up.png")),
            load_template(os.path.join(template_folder, "RyoShu_s3_up.png"))
        ]
        self.ego_templates = [
            load_template(os.path.join(template_folder, "zayin_ego.png"))
        ]
        self.ego_names = [
            "RyoShu_forest_down",
        ]
        self.skill_names = [
            "RyoShu\\RyoShu_s1_down", "RyoShu\\RyoShu_s2_down", "RyoShu\\RyoShu_s3_down",
            "RyoShu\\RyoShu_dodge_down", "RyoShu\\RyoShu_forest_down",
            "RyoShu\\RyoShu_s1_up", "RyoShu\\RyoShu_s2_up", "RyoShu\\RyoShu_s3_up"
        ]
        super().__init__("RyoShu", icon_template, skill_templates)
        self.top_skill_templates = [
            load_template(os.path.join(template_folder, "RyoShu_s1.png")),
            load_template(os.path.join(template_folder, "RyoShu_s2.png")),
            load_template(os.path.join(template_folder, "RyoShu_s3.png")),
            load_template(os.path.join(template_folder, "RyoShu_dodge.png")),
            load_template(os.path.join(template_folder, "RyoShu_forest.png")),
        ]

    def detect_skills(self, game_window_handle):
        return super().detect_skills(game_window_handle, self.skill_templates, self.skill_names, self.top_skill_templates)

    def detect_dodge(self, game_window_image_gray):
        return super().detect_dodge(game_window_image_gray, self.skill_templates, self.skill_names)
