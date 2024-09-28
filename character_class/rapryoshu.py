# RAPRyoShu.py

from character import Character, load_template
from utils import resource_path  # 导入 resource_path 函数
import os

class RAPRyoShu(Character):
    def __init__(self):
        # 使用 resource_path 函数转换路径
        template_folder = resource_path("img/characters/RAPRyoShu")
        
        icon_template = load_template(os.path.join(template_folder, "RAPRyoShu.png"))
        skill_templates = [
            load_template(os.path.join(template_folder, "RAPRyoShu_s1_down.png")),
            load_template(os.path.join(template_folder, "RAPRyoShu_s2_down.png")),
            load_template(os.path.join(template_folder, "RAPRyoShu_s3_down.png")),
            load_template(os.path.join(template_folder, "RAPRyoShu_defend_down.png")),
            load_template(os.path.join(template_folder, "RAPRyoShu_forest_down.png")),
            load_template(os.path.join(template_folder, "RAPRyoShu_s1_up.png")),
            load_template(os.path.join(template_folder, "RAPRyoShu_s2_up.png")),
            load_template(os.path.join(template_folder, "RAPRyoShu_s3_up.png"))
        ]
        self.ego_templates = [
            load_template(os.path.join(template_folder, "zayin_ego.png"))
        ]
        self.ego_names = [
            "RAPRyoShu_forest_down",
        ]
        self.skill_names = [
            "RAPRyoShu\\RAPRyoShu_s1_down", "RAPRyoShu\\RAPRyoShu_s2_down", "RAPRyoShu\\RAPRyoShu_s3_down",
            "RAPRyoShu\\RAPRyoShu_dodge_down", "RAPRyoShu\\RAPRyoShu_forest_down",
            "RAPRyoShu\\RAPRyoShu_s1_up", "RAPRyoShu\\RAPRyoShu_s2_up", "RAPRyoShu\\RAPRyoShu_s3_up"
        ]
        super().__init__("RAPRyoShu", icon_template, skill_templates)
        self.top_skill_templates = [
            load_template(os.path.join(template_folder, "RAPRyoShu_s1.png")),
            load_template(os.path.join(template_folder, "RAPRyoShu_s2.png")),
            load_template(os.path.join(template_folder, "RAPRyoShu_s3.png")),
            load_template(os.path.join(template_folder, "RAPRyoShu_defend.png")),
            load_template(os.path.join(template_folder, "RAPRyoShu_forest.png")),
        ]

    def detect_skills(self, game_window_handle):
        return super().detect_skills(game_window_handle, self.skill_templates, self.skill_names, self.top_skill_templates)

    def detect_dodge(self, game_window_image_gray):
        return super().detect_dodge(game_window_image_gray, self.skill_templates, self.skill_names)
