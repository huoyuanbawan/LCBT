# character.py

import cv2
import os
import numpy as np
import pyautogui
import config
import win32gui
import time
from utils import moveTo, click, load_template, get_screen

class Character:
    def __init__(self, name, icon_template, skill_templates):
        self.name = name
        self.icon_template = icon_template
        self.skill_templates = skill_templates
        self.position = None
        self.skill_coordinates = {
            'up': [(550,705),(640,705),(720,705),(810,705),(900,705),(970,705)],
            'down': [(530,760),(620,760),(710,760),(810,760),(890,760),(1000,760)]
        }
        self.current_skills = []

    def detect_position(self, game_window_image_gray):
        # 检测角色头像位置
        search_region = game_window_image_gray[800:900, 450:1200]
        #search_region = game_window_image_gray
        result = cv2.matchTemplate(search_region, self.icon_template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val >= 0.73:
            print('name=', self.name, 'max_val=', max_val, 'max_loc=', max_loc)
            self.position = [max_loc[0] + 450, max_loc[1] + 800]
        else:
            print('找不到', self.name, '的头像')
        return self.position

    def detect_skills(self, game_window_handle, skill_templates, template_names, top_skill_templates):
        if self.position is None:
            print(f"{self.name} 的位置尚未检测到。")
            return []

        left, top, right, bottom = win32gui.GetWindowRect(game_window_handle)
        width = right - left
        height = bottom - top
        game_window_screenshot = pyautogui.screenshot(region=(left, top, width, height))
        
        # 使用OpenCV加载游戏窗口截图
        game_window_image = np.array(game_window_screenshot)
        game_window_image_gray = cv2.cvtColor(game_window_image, cv2.COLOR_RGB2GRAY)  # 转换为灰度图像

        x, y = self.position
        offset_x = 75
        offset_y = 120
        minus_y = 300 - offset_y
        skill_region_up = game_window_image_gray[y-300:y-offset_y, x-offset_x:x+offset_x]
        skill_region_down = game_window_image_gray[y-minus_y:y, x-offset_x:x+offset_x]

        self.current_skills = []

        skill_range = 0

        for template_name in template_names:
            if template_name.endswith("down"):
                skill_range += 1
            
        # 下面三个技能
        best_down_skill = None
        best_down_val = 0
        nearest_index = None
        nearest_coordinate = None
        
        for i in range(skill_range):
            # 打印图像和模板尺寸
            print(f"skill_region_down shape: {skill_region_down.shape}")
            print(f"skill_templates[{i}] shape: {skill_templates[i].shape}")

            result = cv2.matchTemplate(skill_region_down, skill_templates[i], cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            if not nearest_index or not nearest_coordinate:
                #global_loc = (max_loc[0] + x - offset_x, 760)
                nearest_index = self.find_nearest_index(self.position, self.skill_coordinates['down'])
                nearest_coordinate = self.skill_coordinates['down'][nearest_index]
            print('skill=', template_names[i], 'max_val=', max_val)
            if max_val >= 0.75 and max_val > best_down_val:
                best_down_val = max_val
                best_down_skill = (nearest_coordinate, skill_templates[i].shape[1], skill_templates[i].shape[0], template_names[i])
                if config.activate_HongLu_dodge is False and template_names[i].startswith('HongLu\\HongLu_s3'):
                    print('Activate_HongLu_dodge')
                    config.activate_HongLu_dodge = True
                    

        if best_down_skill:
            self.current_skills.append(best_down_skill)
        else:
            print('下面的技能需要二次确认')
            best_down_skill = self.detect_skills_again(nearest_coordinate, game_window_handle, top_skill_templates, template_names, 0)
            if best_down_skill:
                self.current_skills.append(best_down_skill)
            else:
                self.current_skills.append((nearest_coordinate, skill_templates[0].shape[1], skill_templates[0].shape[0], self.name + '\\' + 'Unknown_s1_down'))
                

        # 上面三个技能
        best_up_skill = None
        best_up_val = 0
        nearest_coordinate = self.skill_coordinates['up'][nearest_index]

        up_skill_range = 0

        for template_name in template_names:
            if template_name.endswith("up"):
                up_skill_range += 1
                
        for i in range(skill_range, skill_range + up_skill_range):
            result = cv2.matchTemplate(skill_region_up, skill_templates[i], cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            print('skill=', template_names[i], 'max_val=', max_val)
            if max_val >= 0.75 and max_val > best_up_val:
                best_up_val = max_val
                #global_loc = (max_loc[0] + x - offset_x, 705)
                best_up_skill = (nearest_coordinate, skill_templates[i].shape[1], skill_templates[i].shape[0], template_names[i])
                if config.activate_HongLu_dodge is False and template_names[i].startswith('HongLu\\HongLu_s3'):
                    print('Activate_HongLu_dodge')
                    config.activate_HongLu_dodge = True

        if best_up_skill:
            self.current_skills.append(best_up_skill)
        else:
            print('上面的技能需要二次确认')
            best_up_skill = self.detect_skills_again(nearest_coordinate, game_window_handle, top_skill_templates, template_names, skill_range)
            if best_up_skill:
                self.current_skills.append(best_up_skill)
            else:
                self.current_skills.append((nearest_coordinate, skill_templates[0].shape[1], skill_templates[0].shape[0], self.name + '\\' + 'Unknown_s1_up'))
        return self.current_skills

    def detect_skills_again(self, position, game_window_handle, top_skill_templates, template_names, skill_range):
        moveTo(position, game_window_handle)
        left, top, right, bottom = win32gui.GetWindowRect(game_window_handle)
        width = right - left
        height = bottom - top
        game_window_screenshot = pyautogui.screenshot(region=(left, top, width, height))
        
        # 使用OpenCV加载游戏窗口截图
        game_window_image = np.array(game_window_screenshot)
        game_window_image_gray = cv2.cvtColor(game_window_image, cv2.COLOR_RGB2GRAY)  # 转换为灰度图像

        skill_region = game_window_image_gray[80:200, 600:800]

        best_skill = None
        best_val = 0
        
        for i in range(len(top_skill_templates)):
            result = cv2.matchTemplate(skill_region, top_skill_templates[i], cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(result)
            print('top_skill=', template_names[i], 'max_val=', max_val)
            if max_val >= 0.5 and max_val > best_val:
                best_val = max_val
                index = i + skill_range
                if i + skill_range >= len(template_names):
                    index -= 5
                best_skill = (position, top_skill_templates[i].shape[1], top_skill_templates[i].shape[0], template_names[index])
                if config.activate_HongLu_dodge is False and template_names[index].startswith('HongLu\\HongLu_s3'):
                    print('Activate_HongLu_dodge')
                    config.activate_HongLu_dodge = True

        if best_skill:
            print('二次确定技能成功')
        else:
            print('二次确定技能失败')
            return None
        return best_skill
        

    def find_nearest_index(self, point, coordinates):
        nearest_index = min(range(len(coordinates)), key=lambda i: abs(coordinates[i][0] - point[0]))
        return nearest_index
    
    def select_skill(self, skill_position):
        """
        选择技能并点击对应位置
        :param skill_position: (x, y) 坐标，技能在整个屏幕上的位置
        """
        print(f"点击位置: {skill_position}")
        pyautogui.click(skill_position[0], skill_position[1])

    def use_ego_skill(self, game_window_handle, ego_templates, index):
        # 截取游戏窗口的截图
        left, top, right, bottom = win32gui.GetWindowRect(game_window_handle)
        width = right - left
        height = bottom - top
        game_window_screenshot = pyautogui.screenshot(region=(left, top, width, height))

        # 使用OpenCV加载游戏窗口截图
        game_window_image = np.array(game_window_screenshot)
        game_window_image_gray = cv2.cvtColor(game_window_image, cv2.COLOR_RGB2GRAY)  # 转换为灰度图像

        # 检测角色头像位置
        if not self.position:
            self.detect_position(game_window_image_gray)
            
        if self.position:
            screen_x = left + self.position[0]
            screen_y = top + self.position[1]

            # 点击头像
            moveTo(self.position, game_window_handle)
            pyautogui.click(x=screen_x, y=screen_y)
            time.sleep(0.1)  # 确保点击动作完成

            # 模拟长按头像位置三秒
            pyautogui.mouseDown(x=screen_x, y=screen_y, button='left')
            time.sleep(2)
            pyautogui.mouseUp(x=screen_x, y=screen_y, button='left')

            # 截取新的游戏窗口截图并保存
            new_game_window_screenshot = pyautogui.screenshot(region=(left, top, width, height))

            # 使用OpenCV加载新的游戏窗口截图
            new_game_window_image = np.array(new_game_window_screenshot)
            new_game_window_image_gray = cv2.cvtColor(new_game_window_image, cv2.COLOR_RGB2GRAY)  # 转换为灰度图像

            # 在指定范围内检测 ego 技能图标
            ego_template = ego_templates[index]
            result = cv2.matchTemplate(new_game_window_image_gray, ego_template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            print('loc=', max_loc, 'val=', max_val)
            if max_val >= 0.9:  # 设置匹配阈值
                ego_x = left + max_loc[0]
                ego_y = top + max_loc[1] + 100
                pyautogui.click(x=ego_x, y=ego_y)
                pyautogui.click(x=ego_x, y=ego_y)
                click((200, 100), game_window_handle)
                print(f"{self.name} 使用了 ego 技能。")
                return True
            else:
                print("未检测到 ego 技能图标。")
                click((200, 100), game_window_handle)
                moveTo(self.position, game_window_handle)
                click(self.position, game_window_handle)
                moveTo((200, 100), game_window_handle)
                return False
        else:
            print(f"未检测到 {self.name} 的头像。")
            click((200, 100), game_window_handle)
            return False
            
    def click_icon(self, game_window_image_gray):
        # 检测角色头像位置
        if not self.position:
            self.detect_position(game_window_image_gray)
        if self.position:
            screen_x = self.position[0]
            screen_y = self.position[1]
            # 点击头像
            pyautogui.click(x=screen_x, y=screen_y)
        else:
            print(f"未检测到 {self.name} 的头像。")

    def detect_dodge(self, game_window_handle, skill_templates, template_names):
        left, top, right, bottom = win32gui.GetWindowRect(game_window_handle)
        width = right - left
        height = bottom - top

        # 截取新的游戏窗口截图并保存
        game_window_screenshot = pyautogui.screenshot(region=(left, top, width, height))

        # 使用OpenCV加载新的游戏窗口截图
        game_window_image = np.array(game_window_screenshot)
        game_window_image_gray = cv2.cvtColor(game_window_image, cv2.COLOR_RGB2GRAY)  # 转换为灰度图像

        if not self.position:
            x, y = self.detect_position(game_window_image_gray)
        else:
            x, y = self.position
            
        offset_x = 75
        offset_y = 120
        minus_y = 300 - offset_y
        skill_region_down = game_window_image_gray[minus_y:y, x-offset_x:x+offset_x]

        skill_range = 0

        for template_name in template_names:
            if template_name.endswith("down"):
                skill_range += 1
            
        # 下面三个技能
        best_down_val = 0
        best_i = 0
        for i in range(skill_range):
            result = cv2.matchTemplate(skill_region_down, skill_templates[i], cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            print('skill=', template_names[i], 'max_val=', max_val)
            if max_val >= 0.0 and max_val > best_down_val:
                best_down_val = max_val
                best_i = i

        if "dodge" in template_names[best_i] or "defend" in template_names[best_i]:
            print("已经是防备了")
            return True
            
        else:
            print("不是防备")
            return False
