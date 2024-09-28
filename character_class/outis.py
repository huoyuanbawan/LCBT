# yisang.py

from character import Character, load_template
from utils import resource_path  # 导入 resource_path 函数
import os

class Outis(Character):
    def __init__(self):
        # 使用 resource_path 函数转换路径
        template_folder = resource_path("img/characters/Outis")
        
        icon_template = load_template(os.path.join(template_folder, "Outis.png"))
        skill_templates = [
            load_template(os.path.join(template_folder, "Outis_s1_down.png")),
            load_template(os.path.join(template_folder, "Outis_s2_down.png")),
            load_template(os.path.join(template_folder, "Outis_s3_down.png")),
            load_template(os.path.join(template_folder, "Outis_defend_down.png")),
            load_template(os.path.join(template_folder, "Outis_to_down.png")),
            load_template(os.path.join(template_folder, "Outis_ebony_down.png")),
            load_template(os.path.join(template_folder, "Outis_binds_down.png")),
            load_template(os.path.join(template_folder, "Outis_s1_up.png")),
            load_template(os.path.join(template_folder, "Outis_s2_up.png")),
            load_template(os.path.join(template_folder, "Outis_s3_up.png"))
        ]
        self.ego_templates = [
            load_template(os.path.join(template_folder, "zayin_ego.png")),
            load_template(os.path.join(template_folder, "he_ego.png")),
            load_template(os.path.join(template_folder, "w_ego.png")),
        ]
        self.ego_names = [
            "Outis_to_down", "Outis_ebony_down", "Outis_binds_down"
        ]
        self.skill_names = [
            "Outis\\Outis_s1_down", "Outis\\Outis_s2_down", "Outis\\Outis_s3_down",
            "Outis\\Outis_defend_down", "Outis\\Outis_to_down", "Outis\\Outis_ebony_down", "Outis\\Outis_binds_down",
            "Outis\\Outis_s1_up", "Outis\\Outis_s2_up", "Outis\\Outis_s3_up"
        ]
        super().__init__("Outis", icon_template, skill_templates)
        
        self.top_skill_templates = [
            load_template(os.path.join(template_folder, "Outis_s1.png")),
            load_template(os.path.join(template_folder, "Outis_s2.png")),
            load_template(os.path.join(template_folder, "Outis_s3.png")),
            load_template(os.path.join(template_folder, "Outis_defend.png")),
            load_template(os.path.join(template_folder, "Outis_to.png")),
            load_template(os.path.join(template_folder, "Outis_ebony.png")),
            load_template(os.path.join(template_folder, "Outis_binds.png")),
            #load_template(os.path.join(template_folder, "YiSang_dimension.png")),
        ]

    def detect_skills(self, game_window_handle):
        return super().detect_skills(game_window_handle, self.skill_templates, self.skill_names, self.top_skill_templates)

    def detect_dodge(self, game_window_image_gray):
        return super().detect_dodge(game_window_image_gray, self.skill_templates, self.skill_names)
