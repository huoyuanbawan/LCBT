# donquixote.py

from character import Character, load_template
import os

class DonQuixote(Character):
    def __init__(self):
        template_folder = "img/characters/DonQuixote"
        icon_template = load_template(os.path.join(template_folder, "DonQuixote.png"))
        skill_templates = [
            load_template(os.path.join(template_folder, "DonQuixote_s1_down.png")),
            load_template(os.path.join(template_folder, "DonQuixote_s2_down.png")),
            load_template(os.path.join(template_folder, "DonQuixote_s3_down.png")),
            load_template(os.path.join(template_folder, "DonQuixote_dodge_down.png")),
            load_template(os.path.join(template_folder, "DonQuixote_la_down.png")),
            load_template(os.path.join(template_folder, "DonQuixote_s1_up.png")),
            load_template(os.path.join(template_folder, "DonQuixote_s2_up.png")),
            load_template(os.path.join(template_folder, "DonQuixote_s3_up.png"))
        ]
        self.ego_templates = [
            load_template(os.path.join(template_folder, "zayin_ego.png"))
        ]
        self.ego_names = [
            "DonQuixote_la_down",
            ]
        self.skill_names = [
            "DonQuixote\\DonQuixote_s1_down", "DonQuixote\\DonQuixote_s2_down", "DonQuixote\\DonQuixote_s3_down",
            "DonQuixote\\DonQuixote_dodge_down", "DonQuixote\\DonQuixote_la_down",
            "DonQuixote\\DonQuixote_s1_up", "DonQuixote\\DonQuixote_s2_up", "DonQuixote\\DonQuixote_s3_up"
        ]
        super().__init__("DonQuixote", icon_template, skill_templates)
        self.top_skill_templates = [
            load_template(os.path.join(template_folder, "DonQuixote_s1.png")),
            load_template(os.path.join(template_folder, "DonQuixote_s2.png")),
            load_template(os.path.join(template_folder, "DonQuixote_s3.png")),
            load_template(os.path.join(template_folder, "DonQuixote_dodge.png")),
            load_template(os.path.join(template_folder, "DonQuixote_la.png")),
        ]
        

    def detect_skills(self, game_window_handle):
        return super().detect_skills(game_window_handle, self.skill_templates, self.skill_names, self.top_skill_templates)

    def detect_dodge(self, game_window_image_gray):
        return super().detect_dodge(game_window_image_gray, self.skill_templates, self.skill_names)

    
