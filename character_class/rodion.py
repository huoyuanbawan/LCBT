# yisang.py

from character import Character, load_template
from utils import resource_path  # 导入 resource_path 函数
import os

class Rodion(Character):
    def __init__(self):
        # 使用 resource_path 函数转换路径
        template_folder = resource_path("img/characters/Rodion")
        
        icon_template = load_template(os.path.join(template_folder, "Rodion.png"))
        skill_templates = [
            load_template(os.path.join(template_folder, "Rodion_s1_down.png")),
            load_template(os.path.join(template_folder, "Rodion_s2_down.png")),
            load_template(os.path.join(template_folder, "Rodion_s3_down.png")),
            load_template(os.path.join(template_folder, "Rodion_defend_down.png")),
            load_template(os.path.join(template_folder, "Rodion_what_down.png")),
            load_template(os.path.join(template_folder, "Rodion_rime_down.png")),
            load_template(os.path.join(template_folder, "Rodion_s1_up.png")),
            load_template(os.path.join(template_folder, "Rodion_s2_up.png")),
            load_template(os.path.join(template_folder, "Rodion_s3_up.png"))
        ]
        self.ego_templates = [
            load_template(os.path.join(template_folder, "zayin_ego.png")),
            load_template(os.path.join(template_folder, "teth_ego.png")),
        ]
        self.ego_names = [
            "Rodion_what_down", "Rodion_rime_down",
        ]
        self.skill_names = [
            "Rodion\\Rodion_s1_down", "Rodion\\Rodion_s2_down", "Rodion\\Rodion_s3_down",
            "Rodion\\Rodion_defend_down", "Rodion\\Rodion_what_down", "Rodion\\Rodion_rime_down", 
            "Rodion\\Rodion_s1_up", "Rodion\\Rodion_s2_up", "Rodion\\Rodion_s3_up"
        ]
        super().__init__("Rodion", icon_template, skill_templates)
        
        self.top_skill_templates = [
            load_template(os.path.join(template_folder, "Rodion_s1.png")),
            load_template(os.path.join(template_folder, "Rodion_s2.png")),
            load_template(os.path.join(template_folder, "Rodion_s3.png")),
            load_template(os.path.join(template_folder, "Rodion_defend.png")),
            load_template(os.path.join(template_folder, "Rodion_what.png")),
            load_template(os.path.join(template_folder, "Rodion_rime.png")),
            #load_template(os.path.join(template_folder, "YiSang_dimension.png")),
        ]

    def detect_skills(self, game_window_handle):
        return super().detect_skills(game_window_handle, self.skill_templates, self.skill_names, self.top_skill_templates)

    def detect_dodge(self, game_window_image_gray):
        return super().detect_dodge(game_window_image_gray, self.skill_templates, self.skill_names)
