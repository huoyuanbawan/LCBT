# yisang.py

from character import Character, load_template
from utils import resource_path  # 导入 resource_path 函数
import os

class Faust(Character):
    def __init__(self):
        # 使用 resource_path 函数转换路径
        template_folder = resource_path("img/characters/Faust")
        
        icon_template = load_template(os.path.join(template_folder, "Faust.png"))
        skill_templates = [
            load_template(os.path.join(template_folder, "Faust_s1_down.png")),
            load_template(os.path.join(template_folder, "Faust_s2_down.png")),
            load_template(os.path.join(template_folder, "Faust_s3_down.png")),
            load_template(os.path.join(template_folder, "Faust_defend_down.png")),
            load_template(os.path.join(template_folder, "Faust_emitter_down.png")),
            load_template(os.path.join(template_folder, "Faust_fluid_down.png")),
            load_template(os.path.join(template_folder, "Faust_s1_up.png")),
            load_template(os.path.join(template_folder, "Faust_s2_up.png")),
            load_template(os.path.join(template_folder, "Faust_s3_up.png"))
        ]
        self.ego_templates = [
            load_template(os.path.join(template_folder, "zayin_ego.png")),
            load_template(os.path.join(template_folder, "he_ego.png")),
        ]
        self.ego_names = [
            "Faust_emitter_down","Faust_fluid_down",
        ]
        self.skill_names = [
            "Faust\\Faust_s1_down", "Faust\\Faust_s2_down", "Faust\\Faust_s3_down",
            "Faust\\Faust_defend_down", "Faust\\Faust_emitter_down", "Faust\\Faust_fluid_down",
            "Faust\\Faust_s1_up", "Faust\\Faust_s2_up", "Faust\\Faust_s3_up"
        ]
        super().__init__("Faust", icon_template, skill_templates)
        
        self.top_skill_templates = [
            load_template(os.path.join(template_folder, "Faust_s1.png")),
            load_template(os.path.join(template_folder, "Faust_s2.png")),
            load_template(os.path.join(template_folder, "Faust_s3.png")),
            load_template(os.path.join(template_folder, "Faust_defend.png")),
            load_template(os.path.join(template_folder, "Faust_emitter.png")),
            load_template(os.path.join(template_folder, "Faust_fluid.png")),
        ]

    def detect_skills(self, game_window_handle):
        return super().detect_skills(game_window_handle, self.skill_templates, self.skill_names, self.top_skill_templates)

    def detect_dodge(self, game_window_image_gray):
        return super().detect_dodge(game_window_image_gray, self.skill_templates, self.skill_names)
