# ui.py
import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
from enemy_class.enemy import Enemy
from config import enemy_options, enemy_image_paths, internal_enemy_names, stage_characters

class EnemySelectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("游戏设置")

        # 使用 Notebook 小部件创建多个选项卡
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both')

        # 创建敌人选择页面
        self.enemy_frame = ttk.Frame(self.notebook)
        self.create_enemy_page(self.enemy_frame)
        self.notebook.add(self.enemy_frame, text="选择敌人")

        # 创建关卡设置页面
        self.stages_frames = []
        self.stage_order_vars = {}
        for i in range(1, 5):
            frame = ttk.Frame(self.notebook)
            self.create_stage_page(frame, i)
            self.notebook.add(frame, text=f"关卡 {i}")
            self.stages_frames.append(frame)

        # 创建其他设置页面
        self.config_frame = ttk.Frame(self.notebook)
        self.create_config_page(self.config_frame)
        self.notebook.add(self.config_frame, text="其他设置")

        # 加载之前保存的设置
        self.load_settings()

    def create_enemy_page(self, frame):
        self.label = ttk.Label(frame, text="请选择一个敌人:")
        self.label.pack(pady=10)

        self.selected_enemy = tk.StringVar()
        self.combobox = ttk.Combobox(frame, textvariable=self.selected_enemy)
        self.combobox['values'] = enemy_options
        self.combobox.pack(pady=10)

        self.button = ttk.Button(frame, text="确定", command=self.on_select)
        self.button.pack(pady=10)

        self.selected_enemy_obj = None

    def create_stage_page(self, frame, stage_number):
        label = ttk.Label(frame, text=f"设置关卡 {stage_number} 的角色顺序:")
        label.pack(pady=10)

        for i, character in enumerate(stage_characters, start=1):
            key = f'stage_{stage_number}_pos_{i}'
            var = tk.StringVar()
            self.stage_order_vars[key] = var
            ttk.Label(frame, text=f"位置 {i}:").pack(anchor='w')
            combobox = ttk.Combobox(frame, textvariable=var)
            combobox['values'] = stage_characters
            combobox.pack(anchor='w')

    def create_config_page(self, frame):
        self.low_hp_ego = tk.BooleanVar()
        self.clash_disvantage_ego = tk.BooleanVar()

        ttk.Label(frame, text="残血释放ego:").pack(anchor='w')
        low_hp_ego_checkbox = ttk.Checkbutton(frame, text="开启", variable=self.low_hp_ego, command=self.update_low_hp_ego)
        low_hp_ego_checkbox.pack(anchor='w')

        ttk.Label(frame, text="拼点劣势释放ego:").pack(anchor='w')
        clash_disvantage_ego_checkbox = ttk.Checkbutton(frame, text="开启", variable=self.clash_disvantage_ego, command=self.update_clash_disvantage_ego)
        clash_disvantage_ego_checkbox.pack(anchor='w')

    def update_low_hp_ego(self):
        import config
        config.low_hp_ego = self.low_hp_ego.get()

    def update_clash_disvantage_ego(self):
        import config
        config.clash_disvantage_ego = self.clash_disvantage_ego.get()


    def on_select(self):
        selected_enemy_display_name = self.selected_enemy.get()
        if selected_enemy_display_name in enemy_image_paths:
            enemy_image_path = enemy_image_paths[selected_enemy_display_name]
            internal_enemy_name = internal_enemy_names[selected_enemy_display_name]
            self.selected_enemy_obj = Enemy(internal_enemy_name, enemy_image_path)
            print(f"已选择敌人: {self.selected_enemy_obj.name}, 路径: {self.selected_enemy_obj.templates_folder}")
            self.save_settings()  # 保存设置
            self.root.quit()
        else:
            messagebox.showerror("错误", "选择的敌人不在列表中，请重新选择。")

    def get_selected_enemy(self):
        return self.selected_enemy_obj

    def get_stage_position_character(self, stage_number, position):
        key = f'stage_{stage_number}_pos_{position}'
        var = self.stage_order_vars.get(key)
        if var:
            return var.get()
        else:
            return None

    def save_settings(self):
        settings = {
            'selected_enemy': self.selected_enemy.get(),
            'stage_order': {key: var.get() for key, var in self.stage_order_vars.items()},
            'low_hp_ego': self.low_hp_ego.get(),
            'clash_disvantage_ego': self.clash_disvantage_ego.get()
        }
        with open('config.json', 'w') as f:
            json.dump(settings, f, indent=4)

    def load_settings(self):
        if os.path.exists('config.json'):
            with open('config.json', 'r') as f:
                settings = json.load(f)
                self.selected_enemy.set(settings.get('selected_enemy', ''))
                for key, value in settings.get('stage_order', {}).items():
                    if key in self.stage_order_vars:
                        self.stage_order_vars[key].set(value)
                self.low_hp_ego.set(settings.get('low_hp_ego', False))
                self.clash_disvantage_ego.set(settings.get('clash_disvantage_ego', False))
                import config
                config.low_hp_ego = settings.get('low_hp_ego', False)
                config.clash_disvantage_ego = settings.get('clash_disvantage_ego', False)


    def quit(self):
        self.save_settings()
        self.root.quit()
