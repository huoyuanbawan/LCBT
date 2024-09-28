# yisang.py

from character import Character, load_template
from utils import resource_path  # 导入 resource_path 函数
import os

class SevenFaust(Character):
    def __init__(self):
        # 使用 resource_path 函数转换路径
        template_folder = resource_path("img/characters/SevenFaust")
        
        icon_template = load_template(os.path.join(template_folder, "SevenFaust.png"))
        skill_templates = [
            load_template(os.path.join(template_folder, "SevenFaust_s1_down.png")),
            load_template(os.path.join(template_folder, "SevenFaust_s2_down.png")),
            load_template(os.path.join(template_folder, "SevenFaust_s3_down.png")),
            load_template(os.path.join(template_folder, "SevenFaust_defend_down.png")),
            load_template(os.path.join(template_folder, "SevenFaust_emitter_down.png")),
            load_template(os.path.join(template_folder, "SevenFaust_fluid_down.png")),
            load_template(os.path.join(template_folder, "SevenFaust_s1_up.png")),
            load_template(os.path.join(template_folder, "SevenFaust_s2_up.png")),
            load_template(os.path.join(template_folder, "SevenFaust_s3_up.png"))
        ]
        self.ego_templates = [
            load_template(os.path.join(template_folder, "zayin_ego.png")),
            load_template(os.path.join(template_folder, "he_ego.png")),
        ]
        self.ego_names = [
            "SevenFaust_emitter_down","SevenFaust_fluid_down",
        ]
        self.skill_names = [
            "SevenFaust\\SevenFaust_s1_down", "SevenFaust\\SevenFaust_s2_down", "SevenFaust\\SevenFaust_s3_down",
            "SevenFaust\\SevenFaust_defend_down", "SevenFaust\\SevenFaust_emitter_down", "SevenFaust\\SevenFaust_fluid_down",
            "SevenFaust\\SevenFaust_s1_up", "SevenFaust\\SevenFaust_s2_up", "SevenFaust\\SevenFaust_s3_up"
        ]
        super().__init__("SevenFaust", icon_template, skill_templates)
        
        self.top_skill_templates = [
            load_template(os.path.join(template_folder, "SevenFaust_s1.png")),
            load_template(os.path.join(template_folder, "SevenFaust_s2.png")),
            load_template(os.path.join(template_folder, "SevenFaust_s3.png")),
            load_template(os.path.join(template_folder, "SevenFaust_defend.png")),
            load_template(os.path.join(template_folder, "SevenFaust_emitter.png")),
            load_template(os.path.join(template_folder, "SevenFaust_fluid.png")),
        ]

    def detect_skills(self, game_window_handle):
        return super().detect_skills(game_window_handle, self.skill_templates, self.skill_names, self.top_skill_templates)

    def detect_dodge(self, game_window_image_gray):
        return super().detect_dodge(game_window_image_gray, self.skill_templates, self.skill_names)
