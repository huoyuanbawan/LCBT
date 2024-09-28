# main.py

import cv2
import numpy as np
import pyautogui
import win32gui
import win32con
import os
import time
import keyboard
import sys
import config
import tkinter as tk
import threading
import logging
from datetime import datetime
from learning import process_character
from utils import click, moveTo, dragTo, load_template, load_templates, setup_signal_handlers, resource_path, get_screen, detect_img, unique_positions, map_positions  
from character_class.sinclair import Sinclair
from character_class.honglu import HongLu
from character_class.heathcliff import Heathcliff
from character_class.wildhuntheathcliff import WildHuntHeathcliff
from character_class.ismael import Ismael
from character_class.donquixote import DonQuixote
from character_class.ryoshu import RyoShu
from character_class.rapryoshu import RAPRyoShu
from character_class.yisang import YiSang
from character_class.lamentyisang import LamentYiSang
from character_class.rodion import Rodion
from character_class.outis import Outis
from character_class.faust import Faust
from character_class.sevenfaust import SevenFaust
from character_class.crackfaust import CrackFaust
from character_class.unknown import Unknown
from enemy_class.enemy import Enemy
from ui import EnemySelectorApp



def on_exit_key_event(event):
    if event.name == 'r' and event.event_type == 'down' and keyboard.is_pressed('ctrl'):
        print("Ctrl+R detected. Terminating the program...")
        os._exit(0)  # 立即终止程序

def find_character_positions(game_window_handle, characters):
    game_window_image_gray = get_screen(game_window_handle)
    # 检测到的角色及其横坐标
    detected_characters = []

    for character in characters:
        character.position = None
        character_position = character.detect_position(game_window_image_gray)
        if character_position:
            detected_characters.append((character, character_position[0]))

    # 按横坐标递减顺序排序
    detected_characters.sort(key=lambda x: x[1], reverse=True)

    # 固定的位置列表，横坐标和纵坐标
    new_positions = [(500, 850), (600, 850), (700, 850), (800, 850), (910, 850), (1010, 850)]

    print('当前检测到的人数为', len(detected_characters))

    if detect_img(game_window_handle, 'img/restart/lcb_sinner.png', (450, 800, 1200, 900)):
        perform_restart(game_window_handle)
        return []

    # 确保新位置列表的长度不超过检测到的角色数量
    if len(detected_characters) > len(new_positions):
        raise ValueError("Detected more characters than the provided new positions can accommodate.")

    for i, (character, _) in enumerate(detected_characters):
        print('character=', character.name, ' position=', character.position)

    if len(detected_characters) < 6:
        # 结果列表
        final_characters = []

        # 遍历 new_positions 和 detected_characters 进行匹配
        detected_index = 0
        for new_pos in reversed(new_positions):
            if detected_index < len(detected_characters):
                detected_char = detected_characters[detected_index]
                detected_x = detected_char[1]
                new_x = new_pos[0]
                
                # 如果 detected_char 和 new_pos 横坐标差距在30以内
                if abs(detected_x - new_x) <= 30:
                    final_characters.append(detected_char)
                    detected_index += 1
                else:
                    # 插入 unknown_character
                    unknown_char = Unknown()
                    unknown_char.position = new_pos
                    #final_characters.append((unknown_char, unknown_char.position))
                    detected_characters.insert(detected_index, (unknown_char, unknown_char.position[0]))
                    print('中间插入', new_pos)
                    detected_index += 1
            else:
                # 如果没有更多的 detected_characters，插入 unknown_character
                unknown_char = Unknown()
                unknown_char.position = new_pos
                #final_characters.append((unknown_char, unknown_char.position))
                detected_characters.insert(detected_index, (unknown_char, unknown_char.position[0]))
                print('末尾插入', new_pos)

        #detected_characters = final_characters

    # 检测标志图片的位置
    detected_staggers0 = detect_img(game_window_handle, 'img/restart/stagger0.png', (450, 800, 1200, 900), 0.9)
    detected_staggers1 = detect_img(game_window_handle, 'img/restart/stagger1.png', (450, 800, 1200, 900), 0.9)
    detected_staggers2 = detect_img(game_window_handle, 'img/restart/stagger2.png', (450, 800, 1200, 900), 0.9)
    detected_staggers3 = detect_img(game_window_handle, 'img/restart/stagger3.png', (450, 800, 1200, 900), 0.9)
    detected_staggers4 = detect_img(game_window_handle, 'img/restart/stagger4.png', (450, 800, 1200, 900), 0.9)
    detected_staggers5 = detect_img(game_window_handle, 'img/restart/stagger5.png', (450, 800, 1200, 900), 0.9)

    detected_panic = detect_img(game_window_handle, 'img/restart/panic.png', (450, 800, 1200, 900), 0.9)

    print('检测到的混乱数分别为', len(detected_staggers0), len(detected_staggers1), len(detected_staggers2), len(detected_staggers3), len(detected_staggers4), len(detected_staggers5), len(detected_panic))

    # 合并列表并去除相近位置
    all_detected_staggers = [detected_staggers0, detected_staggers1, detected_staggers2, detected_staggers3, detected_staggers4, detected_staggers5, detected_panic]
    unique_detected_staggers = unique_positions(all_detected_staggers, min_distance=50)
    
    for i in range(len(unique_detected_staggers)):
        detected_characters.pop(0)   

    # 逆序遍历排序后的角色实例
    for i, (character, _) in enumerate(reversed(detected_characters)):
        if i >= len(new_positions):
            break
        new_position = new_positions[i]
        character.position = new_position  # 更新角色的位置
        detected_characters[-(i+1)] = (character, new_position[0])  # 更新character_position[0]
        print('character=', character.name, ' position=', character.position)

    print('当前检测到的人数为', len(detected_characters))

    if len(detected_characters) <= 3:
        perform_restart(game_window_handle)
        return []

    # 返回排序后的角色实例列表
    return [char[0] for char in detected_characters]

def detect_and_handle_reconnect(game_window_handle):
    reconnect_template_path = resource_path('img/reconnect.png')
    reconnect_template = cv2.imread(reconnect_template_path, cv2.IMREAD_GRAYSCALE)
    
    threshold = 0.8  # 匹配阈值，可以根据需要调整


    # 检查是否按下了 'q' 键
    if keyboard.is_pressed('q'):
        print("检测到 'q' 键按下，程序结束。")
        sys.exit()  # 终止整个程序

    # 使用OpenCV加载游戏窗口截图
    game_window_image_gray = get_screen(game_window_handle)  

    if reconnect_template is not None:
        result = cv2.matchTemplate(game_window_image_gray, reconnect_template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= threshold:
            click(max_loc, game_window_handle)
            time.sleep(1)

def detect_and_handle_try_again(game_window_handle):
    detected_retry_stage = detect_img(game_window_handle, 'img/restart/retry_stage.png')
    if detected_retry_stage:
        moveTo(detected_retry_stage[0], game_window_handle)
        click(detected_retry_stage[0], game_window_handle)
        time.sleep(1)
        detected_confirm = detect_img(game_window_handle, 'img/restart/confirm.png')
        if detected_confirm:
            moveTo(detected_confirm[0], game_window_handle)
            click(detected_confirm[0], game_window_handle)
            set_default()
            return True
    return False
    '''
    tryagain_template_path = resource_path('img/tryagain.png')
    tryagain_template = cv2.imread(tryagain_template_path, cv2.IMREAD_GRAYSCALE)
    
    threshold = 0.8  # 匹配阈值，可以根据需要调整

    # 检查是否按下了 'q' 键
    if keyboard.is_pressed('q'):
        print("检测到 'q' 键按下，程序结束。")
        sys.exit()  # 终止整个程序

    game_window_image_gray = get_screen(game_window_handle)

    if tryagain_template is not None:
        result = cv2.matchTemplate(game_window_image_gray, tryagain_template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= threshold:
            set_default()
            click(max_loc, game_window_handle)
            time.sleep(1)
    '''
                
def detect_and_handle_skip(game_window_handle):
    skip_template_path = resource_path('img/event/skip.png')
    skip_template = cv2.imread(skip_template_path, cv2.IMREAD_GRAYSCALE)

    additional_templates = [
        resource_path("img/event/king/wear_the_mask_of_wrath.png"),
    ]

    event_templates = {
        "verylow": resource_path("img/event/verylow.png"),
        "low": resource_path("img/event/low.png"),
        "normal": resource_path("img/event/normal.png"),
        "high": resource_path("img/event/high.png"),
        "veryhigh": resource_path("img/event/veryhigh.png"),
    }
    
    threshold = 0.8  # 匹配阈值，可以根据需要调整


    while True:
        # 检查是否按下了 'q' 键
        if keyboard.is_pressed('q'):
            print("检测到 'q' 键按下，程序结束。")
            sys.exit()  # 终止整个程序

        game_window_image_gray = get_screen(game_window_handle)
        detect_region = game_window_image_gray[350:450, 650:850]

        if skip_template is not None:
            result = cv2.matchTemplate(detect_region, skip_template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            if max_val >= threshold:
                skip_x, skip_y = max_loc[0] + skip_template.shape[1] // 2, max_loc[1] + skip_template.shape[0] // 2
                click([skip_x + 650, skip_y + 350], game_window_handle)
                click([skip_x + 650, skip_y + 350], game_window_handle)
                click([skip_x + 650, skip_y + 350], game_window_handle)
                click([skip_x + 650, skip_y + 350], game_window_handle)
                click([skip_x + 650, skip_y + 350], game_window_handle)
                click([skip_x + 650, skip_y + 350], game_window_handle)
                click([skip_x + 650, skip_y + 350], game_window_handle)
                click([skip_x + 650, skip_y + 350], game_window_handle)
                click([skip_x + 650, skip_y + 350], game_window_handle)
                click([skip_x + 650, skip_y + 350], game_window_handle)
                time.sleep(1)

                '''
                detect_region = get_screen(game_window_handle)

                # 检测并点击additional_templates中的图片
                for template_path in additional_templates:
                    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
                    if template is not None:
                        result = cv2.matchTemplate(detect_region, template, cv2.TM_CCOEFF_NORMED)
                        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                        print('max_val=', max_val, 'template_path=', template_path)
                        if max_val >= 0.9:
                            if 'cleaves.png' in template_path or 'envy.png' in template_path:
                                click((max_loc[0] + template.shape[1] // 2, max_loc[1] + template.shape[0] // 2), game_window_handle)
                            elif 'burns.png' in template_path:
                                moveTo((1512, 256), game_window_handle)
                                dragTo((1512, 650), game_window_handle)
                            time.sleep(0.5)
                            break  # 点击后跳出循环
                '''

                detected_choices = detect_img(game_window_handle, 'img/event/king/wear_the_mask_of_wrath.png', (875,550,1250,670))
                if detected_choices:
                    moveTo(detected_choices[0], game_window_handle)
                    click(detected_choices[0], game_window_handle)
                

                detect_region = get_screen(game_window_handle, [(0, 750), (700, 850)])
                
                # 检测并点击event_templates中的图片
                for event_name, template_path in event_templates.items():
                    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
                    if template is not None:
                        result = cv2.matchTemplate(detect_region, template, cv2.TM_CCOEFF_NORMED)
                        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                        if max_val >= threshold:
                            event_x, event_y = max_loc[0] + template.shape[1] // 2, max_loc[1] + template.shape[0] // 2
                            click([event_x, event_y + 750 + 30], game_window_handle)
                            
                time.sleep(1)              
                click([1420, 820], game_window_handle)
            else:
                return game_window_image_gray
        else:
            return game_window_image_gray

def detect_and_handle_summary(game_window_handle):
    # 检测战斗结束的标志图片
    summary_image_path = resource_path("img/summary.png")
    # 读取标志图片
    summary_img = cv2.imread(summary_image_path, cv2.IMREAD_GRAYSCALE)
    
    # 截取游戏窗口的截图  
    game_window_image_gray = get_screen(game_window_handle)


    # 使用模板匹配来检测标志
    result = cv2.matchTemplate(game_window_image_gray, summary_img, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(result)

    if max_val >= 0.8:
        print('检测到了summary')
        click((1550, 900), game_window_handle)
        time.sleep(1)  

def battling(game_window_handle, battling_image):

    if battling_image is None:
        raise FileNotFoundError("无法加载战斗图像")

    game_window_image_gray = get_screen(game_window_handle)

    # 定义搜索区域
    search_region = game_window_image_gray[50:140, 15:80]

    # 匹配 default_magnifier_image
    result = cv2.matchTemplate(search_region, battling_image, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc= cv2.minMaxLoc(result)

    if max_val >= 0.5:
        print('已经找到了战斗图像！')
        print('max_val=', max_val)
        
        return True
    else:
        print('找不到战斗图像！请检查电脑显示缩放比例是否是100%')
        return False

def set_shot(game_window_handle):
    click((530, 760), game_window_handle)
     
    click((200, 50), game_window_handle)
 
    click((360, 784), game_window_handle)
    click((360, 784), game_window_handle)
        
    # 模拟长按 'q' 键 3 秒钟
    print("模拟长按 'q' 键 3 秒钟...")
    pyautogui.keyDown('q')
    click((200, 50), game_window_handle)
    time.sleep(0.1)
    pyautogui.press('p')
    time.sleep(0.1)
    pyautogui.press('p')
    time.sleep(0.1)
    pyautogui.press('p')
    time.sleep(2.7)  # 持续按下 3 秒
    pyautogui.keyUp('q')
    print("长按 'q' 键结束。")
    click((200, 50), game_window_handle)
    time.sleep(0.2)

def handle_enemies(detected_enemies, game_window_handle, sorted_characters):
    left, top, right, bottom = win32gui.GetWindowRect(game_window_handle)
    width = right - left
    height = bottom - top
    detected_enemy_ego = False

    detected_enemies = sorted(detected_enemies, key=lambda x: x[0][0], reverse=True)

    # 初始检测到的敌人
    for enemy_loc, w, h, template_name in detected_enemies:
        print(f"检测到敌人0: {template_name} 位置: {enemy_loc}") 

    if config.enemy.name == 'Section4.1':
        # 目标位置列表
        target_positions = [(512, 153), (618, 347), (733, 153), (865, 347), (969, 153), (1102, 347)]

        # 将 detected_enemies 中的 enemy_loc 映射到 target_positions
        detected_enemies = map_positions(detected_enemies, target_positions, 35, 35)


        # 处理后检测到的敌人
        for enemy_loc, w, h, template_name in detected_enemies:
            print(f"检测到敌人1: {template_name} 位置: {enemy_loc}")    
                                    
    i = 0
    while i < len(detected_enemies):
        enemy_loc, w, h, template_name = detected_enemies[i]
        if template_name.startswith('dodge'):
            if config.enemy.name == 'Section1.3':
                for character in sorted_characters:   
                    if character.name.endswith('Faust') and character.position :
                        moveTo(character.position, game_window_handle)
                        click(character.position, game_window_handle)
                        break

        '''
        if template_name.startswith('leave_interloper') or template_name.startswith('sky_clearing_cut') or template_name.startswith('purple_electric_screaming'):
            for character in sorted_characters:
                if character.name.endswith('Rodion') and character.position:
                    if character.use_ego_skill(game_window_handle, character.ego_templates, 0):
                        break
        '''

        if template_name.startswith('self_destructive_purge') or template_name.startswith('quick_suppression'):
            detected_enemies = []
            perform_restart(game_window_handle)
            break

        '''
        if template_name.startswith('overcharge_release'):
            detected_enemies.insert(0, detected_enemies.pop(i))
            i += 1  
            continue
        '''

        if template_name.startswith('ego_d_fluid') and (enemy_loc[1] <= 100 or enemy_loc[1] >= 530):
            detected_enemies.pop(i)
            continue

        if template_name.startswith('ego_f_fluid') and (enemy_loc[0] <= 350 or enemy_loc[0] >= 1350 or enemy_loc[1] <= 100):
            detected_enemies.pop(i)
            continue

        if template_name.startswith('ego_hex_nail') and (enemy_loc[0] <= 250):
            detected_enemies.pop(i)
            continue
        
        if template_name.startswith('ego_impending_days') and (enemy_loc[1] <= 100 or (enemy_loc[1] >= 250 and enemy_loc[1] <= 300) or enemy_loc[0] <= 350 or (enemy_loc[1] >= 370 and enemy_loc[1] <= 440)):
            detected_enemies.pop(i)
            continue

        if template_name.startswith('grounding_refusal') and enemy_loc[0] <= 450:
            detected_enemies.pop(i)
            continue

        if template_name.startswith('ego_h_binds') and (enemy_loc[0] >= 1450 or enemy_loc[0] <= 300 or (enemy_loc[1] >= 250 and enemy_loc[1] <= 290) or enemy_loc[1] <= 100 or enemy_loc[1] >= 550):
            detected_enemies.pop(i)
            continue

        if template_name.startswith('ego_chains') and (enemy_loc[0] <= 360 or enemy_loc[1] >= 520):
            detected_enemies.pop(i)
            continue

        if template_name.startswith('soda') and (enemy_loc[1] <= 450 and enemy_loc[1] >= 390):
            detected_enemies.pop(i)
            continue


        if template_name.startswith('purple_electric_screaming'):
            ego_count = 0
            ego_threshold = 1
            
            for character in reversed(sorted_characters):
                if ego_count >= ego_threshold:
                    break
                
                if character.name.endswith('Sinclair') and character.position:
                    if character.use_ego_skill(game_window_handle, character.ego_templates, 0):
                        ego_count += 1
                        continue

                if character.name.endswith('Rodion') and character.position:
                    if character.use_ego_skill(game_window_handle, character.ego_templates, 0):
                        ego_count += 1
                        continue
                    
                if character.name.endswith('Outis') and character.position:
                    if character.use_ego_skill(game_window_handle, character.ego_templates, 1):
                        ego_count += 1
                        continue
                    elif character.use_ego_skill(game_window_handle, character.ego_templates, 2):
                        ego_count += 1
                        continue

                if character.name.endswith('YiSang') and character.position:
                    if character.use_ego_skill(game_window_handle, character.ego_templates, 2):
                        ego_count += 1
                        continue

                if character.name.endswith('Ismael') and character.position:
                    if character.use_ego_skill(game_window_handle, character.ego_templates, 2):
                        ego_count += 1
                        continue

                if character.name.endswith('Heathcliff') and character.position:
                    if character.use_ego_skill(game_window_handle, character.ego_templates, 2):
                        ego_count += 1
                        continue

        if template_name.startswith('ego'):
            detected_enemy_ego = True
            
        i += 1

    if config.enemy.name == 'Section2.1' and len(detected_enemies) > 3:
        ego_threshold = 2
        ego_count = 0

        for character in reversed(sorted_characters):
            if ego_count >= ego_threshold:
                break
            
            if character.name.endswith('Faust') and character.position:
                if character.use_ego_skill(game_window_handle, character.ego_templates, 1):
                    ego_count += 1
                    continue
                
            if character.name.endswith('Outis') and character.position:
                if character.use_ego_skill(game_window_handle, character.ego_templates, 2):
                    ego_count += 1
                    continue

            if character.name.endswith('YiSang') and character.position:
                if character.use_ego_skill(game_window_handle, character.ego_templates, 2):
                    ego_count += 1
                    continue

            if character.name.endswith('Ismael') and character.position:
                if character.use_ego_skill(game_window_handle, character.ego_templates, 2):
                    ego_count += 1
                    continue

            if character.name.endswith('Heathcliff') and character.position:
                if character.use_ego_skill(game_window_handle, character.ego_templates, 2):
                    ego_count += 1
                    continue


    if config.enemy.name == 'Section2.3' and len(detected_enemies) > 3:
        if not config.already_use_ego:
            config.already_use_ego = True
            ego_threshold = 1
            ego_count = 0

            for character in reversed(sorted_characters):
                if character.name.endswith('Faust') and character.position:
                    if character.use_ego_skill(game_window_handle, character.ego_templates, 1):
                        break
                    
            for character in reversed(sorted_characters):
                if ego_count >= ego_threshold:
                    break                

                if character.name.endswith('Ismael') and character.position:
                    if character.use_ego_skill(game_window_handle, character.ego_templates, 2):
                        ego_count += 1
                        continue

                if character.name.endswith('Outis') and character.position:
                    if character.use_ego_skill(game_window_handle, character.ego_templates, 1):
                        ego_count += 1
                        continue
                    elif character.use_ego_skill(game_window_handle, character.ego_templates, 2):
                        ego_count += 1
                        continue
                    
                if character.name.endswith('YiSang') and character.position:
                    if character.use_ego_skill(game_window_handle, character.ego_templates, 2):
                        ego_count += 1
                        continue

                if character.name.endswith('Heathcliff') and character.position:
                    if character.use_ego_skill(game_window_handle, character.ego_templates, 2):
                        ego_count += 1
                        continue
                
        if detected_enemy_ego:

            ego_threshold = 1
            ego_count = 0
                    
            for character in reversed(sorted_characters):
                if ego_count >= ego_threshold:
                    break
                    

                if character.name.endswith('Ismael') and character.position:
                    if character.use_ego_skill(game_window_handle, character.ego_templates, 2):
                        ego_count += 1
                        continue

                if character.name.endswith('Outis') and character.position:
                    if character.use_ego_skill(game_window_handle, character.ego_templates, 1):
                        ego_count += 1
                        continue
                    elif character.use_ego_skill(game_window_handle, character.ego_templates, 2):
                        ego_count += 1
                        continue
                        
                if character.name.endswith('YiSang') and character.position:
                    if character.use_ego_skill(game_window_handle, character.ego_templates, 2):
                        ego_count += 1
                        continue

                if character.name.endswith('Heathcliff') and character.position:
                    if character.use_ego_skill(game_window_handle, character.ego_templates, 2):
                        ego_count += 1
                        continue

    if config.enemy.name == 'Section3.1' and len(detected_enemies) > 3:
        #if not config.already_use_ego:
        if detect_img(game_window_handle, 'img/battle/turn1.png', (60, 100, 130, 140)):
            config.already_use_ego = True
            ego_threshold = 1
            ego_count = 0

            for character in reversed(sorted_characters):
                if character.name.endswith('Faust') and character.position:
                    if character.use_ego_skill(game_window_handle, character.ego_templates, 1):
                        break
                    
            for character in reversed(sorted_characters):
                if ego_count >= ego_threshold:
                    break                

                if character.name.endswith('Ismael') and character.position:
                    if character.use_ego_skill(game_window_handle, character.ego_templates, 2):
                        ego_count += 1
                        continue

                if character.name.endswith('Outis') and character.position:
                    if character.use_ego_skill(game_window_handle, character.ego_templates, 2):
                        ego_count += 1
                        continue
                    elif character.use_ego_skill(game_window_handle, character.ego_templates, 1):
                        ego_count += 1
                        continue
                    
                if character.name.endswith('YiSang') and character.position:
                    if character.use_ego_skill(game_window_handle, character.ego_templates, 2):
                        ego_count += 1
                        continue

                if character.name.endswith('Heathcliff') and character.position:
                    if character.use_ego_skill(game_window_handle, character.ego_templates, 2):
                        ego_count += 1
                        continue
                
        if detected_enemy_ego:
            for character in reversed(sorted_characters):
                if character.name.endswith('Faust') and character.position:
                    if character.use_ego_skill(game_window_handle, character.ego_templates, 1):
                        break

            ego_threshold = 1
            ego_count = 0
                    
            for character in reversed(sorted_characters):
                if ego_count >= ego_threshold:
                    break
                    

                if character.name.endswith('Ismael') and character.position:
                    if character.use_ego_skill(game_window_handle, character.ego_templates, 2):
                        ego_count += 1
                        continue

                if character.name.endswith('Outis') and character.position:
                    if character.use_ego_skill(game_window_handle, character.ego_templates, 2):
                        ego_count += 1
                        continue
                    elif character.use_ego_skill(game_window_handle, character.ego_templates, 1):
                        ego_count += 1
                        continue
                        
                if character.name.endswith('YiSang') and character.position:
                    if character.use_ego_skill(game_window_handle, character.ego_templates, 2):
                        ego_count += 1
                        continue

                if character.name.endswith('Heathcliff') and character.position:
                    if character.use_ego_skill(game_window_handle, character.ego_templates, 2):
                        ego_count += 1
                        continue

    if config.enemy.name == 'Section4.1' and len(detected_enemies) > 3:
        for character in reversed(sorted_characters):
            if character.name.endswith('Faust') and character.position:
                if character.use_ego_skill(game_window_handle, character.ego_templates, 1):
                    break
                
        if detect_img(game_window_handle, 'img/battle/turn1.png', (60, 100, 130, 140)):
            ego_threshold = 2
            ego_count = 0
                    
            for character in reversed(sorted_characters):
                if ego_count >= ego_threshold:
                    break                

                if character.name.endswith('Ismael') and character.position:
                    if character.use_ego_skill(game_window_handle, character.ego_templates, 2):
                        ego_count += 1
                        continue

                if character.name.endswith('Outis') and character.position:
                    if character.use_ego_skill(game_window_handle, character.ego_templates, 1):
                        ego_count += 1
                        continue
                    elif character.use_ego_skill(game_window_handle, character.ego_templates, 2):
                        ego_count += 1
                        continue
                    
                if character.name.endswith('YiSang') and character.position:
                    if character.use_ego_skill(game_window_handle, character.ego_templates, 2):
                        ego_count += 1
                        continue

                if character.name.endswith('Heathcliff') and character.position:
                    if character.use_ego_skill(game_window_handle, character.ego_templates, 2):
                        ego_count += 1
                        continue
                
        if detected_enemy_ego or True:

            ego_threshold = 2
            ego_count = 0
                    
            for character in reversed(sorted_characters):
                if ego_count >= ego_threshold:
                    break
                    

                if character.name.endswith('Ismael') and character.position:
                    if character.use_ego_skill(game_window_handle, character.ego_templates, 2):
                        ego_count += 1
                        continue

                if character.name.endswith('Outis') and character.position:
                    if character.use_ego_skill(game_window_handle, character.ego_templates, 1):
                        ego_count += 1
                        continue
                    elif character.use_ego_skill(game_window_handle, character.ego_templates, 2):
                        ego_count += 1
                        continue
                        
                if character.name.endswith('YiSang') and character.position:
                    if character.use_ego_skill(game_window_handle, character.ego_templates, 2):
                        ego_count += 1
                        continue

                if character.name.endswith('Heathcliff') and character.position:
                    if character.use_ego_skill(game_window_handle, character.ego_templates, 2):
                        ego_count += 1
                        continue

            

    if config.enemy.name == 'Section4.2' and len(detected_enemies) > 3:
        ego_threshold = 1
        ego_count = 0

        for character in reversed(sorted_characters):
            if ego_count >= ego_threshold:
                break
            
            if character.name.endswith('Faust') and character.position:
                if character.use_ego_skill(game_window_handle, character.ego_templates, 1):
                    ego_count += 1
                    break
    '''
            if character.name.endswith('Rodion') and character.position:
                if character.use_ego_skill(game_window_handle, character.ego_templates, 1):
                    ego_count += 1
                    continue
    '''

                    
    if config.low_hp_ego and detect_img(game_window_handle, 'img/battle/low_hp.png', (460,800,1100,850), 0.9) and len(detected_enemies) >= 3:
        print('检测到残血')
        for character in sorted_characters:
            if character.name.endswith('Faust') and character.position:
                if character.use_ego_skill(game_window_handle, character.ego_templates, 1):
                    break  

    for enemy_loc, w, h, template_name in detected_enemies:
        print(f"检测到敌人2: {template_name} 位置: {enemy_loc}")

    return detected_enemies

def detect_and_restart(game_window_handle):
    # 创建一个空字典来存储模板
    restart_templates = {}

    # 定义模板文件夹和文件名列表
    restart_folder = 'img/restart'
    template_files = ['dead0.png', 'stagger0.png', 'stagger1.png', 'stagger2.png', 'stagger3.png', 'stagger4.png', 'stagger5.png', 'panic.png']

    # 循环遍历模板文件列表
    for file in template_files:
        # 使用 resource_path 转换路径
        template_path = resource_path(f'{restart_folder}/{file}')
        # 加载模板图像
        template = load_template(template_path)
        if template is not None:
            # 将模板添加到字典中
            restart_templates[file] = template

    # 截取游戏窗口的截图
    game_window_image_gray = get_screen(game_window_handle)
    
    # 存储检测到的stagger位置
    stagger_positions = []

    for template_name, template in restart_templates.items():
        result = cv2.matchTemplate(game_window_image_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8  # 设定匹配阈值，根据需要调整
        locations = np.where(result >= threshold)

        if template_name.startswith('dead') and len(locations[0]) > 0:
            print(f"找到匹配的重开图片: {template_name}")
            perform_restart(game_window_handle)
            return True

        if template_name.startswith('stagger'):
            for loc in zip(*locations[::-1]):
                stagger_positions.append(loc)

    # 合并位置差不多的stagger位置
    def is_close(pos1, pos2, max_distance = 30):
        return abs(pos1[0] - pos2[0]) <= max_distance and abs(pos1[1] - pos2[1]) <= max_distance

    merged_stagger_positions = []
    for pos in stagger_positions:
        if not any(is_close(pos, merged_pos) for merged_pos in merged_stagger_positions):
            merged_stagger_positions.append(pos)

    if len(merged_stagger_positions) >= 3:
        print("检测到3个或以上的stagger图片，重开游戏")
        perform_restart(game_window_handle)
        return True

    return False

def set_default():
    config.activate_HongLu_dodge = False
    config.already_activate_HongLu_dodge = False
    config.already_use_ego = False
    
    if config.enemy.name.endswith('.2'):
        config.current_enemy_index -= 1            
        config.enemy = create_enemy(config.current_enemy_index)
        print(f"当前敌人已为：{config.enemy.name}")
    elif config.enemy.name.endswith('.3'):
        config.current_enemy_index -= 2            
        config.enemy = create_enemy(config.current_enemy_index)
        print(f"当前敌人已为：{config.enemy.name}")    

def perform_restart(game_window_handle):
    pyautogui.press('esc')
    time.sleep(1)
    click((820, 500), game_window_handle)
    set_default()
    print('HongLu激活防备已经关闭')
    time.sleep(5)

def shift_window(game_window_handle):
    if config.enemy.name == 'Section1.1':
        # 按下 'w' 键 0.2 秒
        pyautogui.keyDown('w')
        time.sleep(0.2)
        pyautogui.keyUp('w')
        print("pressed 'w' key for 0.2 seconds.")



    if config.enemy.name == 'Section1.2':
        pyautogui.keyDown('w')
        time.sleep(0.2)
        pyautogui.keyUp('w')
        pyautogui.keyDown('a')
        time.sleep(0.1)
        pyautogui.keyUp('a')

    
    if config.enemy.name.startswith('Section2.3'):
        # 按下 'w' 键 0.2 秒
        pyautogui.keyDown('w')
        time.sleep(0.2)
        pyautogui.keyUp('w')
        print("pressed 'w' key for 0.2 seconds.")
    

    if config.enemy.name.startswith('Section3.'):
        # 按下 'w' 键 0.2 秒
        pyautogui.keyDown('w')
        time.sleep(0.2)
        pyautogui.keyUp('w')
        print("pressed 'w' key for 0.2 seconds.")

    '''
    if enemy.name.startswith('Section4.1'):
        # 按下 'w' 键 0.2 秒
        pyautogui.keyDown('w')
        time.sleep(0.4)
        pyautogui.keyUp('w')
        print("pressed 'w' key for 0.2 seconds.")
    '''

def detect_battle_end(game_window_handle, should_click = False):


    detected_clockhead0 = detect_img(game_window_handle, "img/window/clocktrain0.png")
    detected_clockhead1 = detect_img(game_window_handle, "img/window/clocktrain1.png")
    detected_clockhead2 = detect_img(game_window_handle, "img/window/clocktrain2.png")

    for obj in detected_clockhead0:
        print('找到时钟头0')
        click(obj, game_window_handle)
        time.sleep(1)
        break

    for obj in detected_clockhead1:
        print('找到时钟头1')
        click(obj, game_window_handle)
        time.sleep(1)
        break

    for obj in detected_clockhead2:
        print('找到时钟头2')
        click(obj, game_window_handle)
        time.sleep(1)
        break
        
    return detected_clockhead0 or detected_clockhead1 or detected_clockhead2  # 返回匹配结果是否超过阈值

def detect_enter(game_window_handle):
    # 检测战斗结束的标志图片
    enter_image_path = resource_path("img/window/enter.png")
    # 读取标志图片
    enter_img = cv2.imread(enter_image_path, cv2.IMREAD_GRAYSCALE)
        
    # 截取游戏窗口的截图  
    game_window_image_gray = get_screen(game_window_handle)


    # 使用模板匹配来检测标志
    enter_result = cv2.matchTemplate(game_window_image_gray, enter_img, cv2.TM_CCOEFF_NORMED)
    _, enter_max_val, _, _ = cv2.minMaxLoc(enter_result)

    if enter_max_val >= 0.65:
        pyautogui.press('enter')
        moveTo((200, 100), game_window_handle)
        time.sleep(1)
        print('找到enter了')
        return True
    else:
        print('找不到enter')
    
    return False


def select_characters(game_window_handle, app):


    moveTo((200, 100), game_window_handle)
    # game_window_image_gray = get_screen(game_window_handle)

    '''
    if True:
        config.first_select = False
        selected_image_path = resource_path("img/window/backup.png")
        selected_img = cv2.imread(selected_image_path, cv2.IMREAD_GRAYSCALE)

        result = cv2.matchTemplate(game_window_image_gray, selected_img, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(result >= threshold)
        points = list(zip(*loc[::-1]))

        if points:
            merged_points = merge_close_points(points, distance_threshold=30)


            for center in merged_points:
                click_x = int(center[0]) + selected_img.shape[1] // 2
                click_y = int(center[1]) + selected_img.shape[0] // 2
                click((click_x, click_y), game_window_handle)
                print(f"Clicked at: ({click_x}, {click_y})")
        
        selected_image_path = resource_path("img/window/selected.png")
        selected_img = cv2.imread(selected_image_path, cv2.IMREAD_GRAYSCALE)

        result = cv2.matchTemplate(game_window_image_gray, selected_img, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(result >= threshold)
        points = list(zip(*loc[::-1]))

        if points:
            merged_points = merge_close_points(points, distance_threshold=30)


            for center in merged_points:
                click_x = int(center[0]) + selected_img.shape[1] // 2
                click_y = int(center[1]) + selected_img.shape[0] // 2
                click((click_x, click_y), game_window_handle)
                print(f"Clicked at: ({click_x}, {click_y})")
        '''
    if detect_img(game_window_handle, 'img/window/selected.png'):
        if detect_img(game_window_handle, 'img/window/clear_selection.png', (1300, 600, 1550, 670)):
            detected_clear_selection = detect_img(game_window_handle, 'img/window/clear_selection.png', (1300, 600, 1550, 670))
            moveTo(detected_clear_selection[0], game_window_handle)
            click(detected_clear_selection[0], game_window_handle)
            time.sleep(2)
            pyautogui.press('enter')
            time.sleep(2)
   
    if config.enemy.name == "Section1.1":
        for i in range(12):
            name = app.get_stage_position_character(1, i + 1)
            pos = config.characters_positions[name]
            click(pos, game_window_handle)
            
    elif config.enemy.name == "Section2.1":
        for i in range(12):
            name = app.get_stage_position_character(2, i + 1)
            pos = config.characters_positions[name]
            click(pos, game_window_handle)

    elif config.enemy.name == "Section3.1":
        for i in range(12):
            name = app.get_stage_position_character(3, i + 1)
            pos = config.characters_positions[name]
            click(pos, game_window_handle)
            
    elif config.enemy.name == "Section4.1":
        for i in range(12):
            name = app.get_stage_position_character(4, i + 1)
            pos = config.characters_positions[name]
            click(pos, game_window_handle)
        
    click((1430, 760), game_window_handle)
    print('按下enter')
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('enter')
    
def merge_close_points(points, distance_threshold=30):
    if not points:
        return []

    merged_points = []
    used = [False] * len(points)

    for i, point1 in enumerate(points):
        if used[i]:
            continue

        merged_point = point1
        for j, point2 in enumerate(points):
            if i != j and not used[j]:
                if abs(point1[0] - point2[0]) <= distance_threshold and abs(point1[1] - point2[1]) <= distance_threshold:
                    # 合并两个点，取平均值
                    merged_point = ((point1[0] + point2[0]) // 2, (point1[1] + point2[1]) // 2)
                    used[j] = True

        used[i] = True
        merged_points.append(merged_point)

    return merged_points

def get_current_enemy_index():
    # 构建反向查找字典
    internal_to_external_names = {v: k for k, v in config.internal_enemy_names.items()}
    # 获取内部名称对应的外部名称
    external_enemy_name = internal_to_external_names.get(config.enemy.name)
    if external_enemy_name:
        # 查找外部名称的索引
        current_enemy_index = config.enemy_names.index(external_enemy_name)
        return current_enemy_index
    else:
        print(f"无法找到 {config.enemy.name} 对应的外部敌人名称")
        return None

def create_enemy(index):
    """
    创建并返回新的 Enemy 对象
    """
    print('enemy_index =', index)
    enemy_name = config.enemy_names[index]
    enemy_image_path = config.enemy_image_paths[enemy_name]
    internal_enemy_name = config.internal_enemy_names[enemy_name]
    return Enemy(internal_enemy_name, enemy_image_path)

def update_enemy(game_window_handle):
    
    if detect_enter(game_window_handle):
        set_default()
        time.sleep(1)
        if detect_img(game_window_handle, "img/window/save_team.png", (1330,700,1550,810)):
            #if config.enemy.name.endswith('.1'):
            while not config.enemy.name.startswith('CheckPoint'):
                # 更新敌人对象为下一个
                config.current_enemy_index += 1
                config.enemy = create_enemy(config.current_enemy_index)
                print('检查点更新，更新敌人为序号', config.current_enemy_index)                     

            pyautogui.press('enter')
            time.sleep(1)

            if detect_img(game_window_handle, 'img/window/confirm.png'):
                print('确认confirm')
                pyautogui.press('enter')
                time.sleep(1)                
                     

        if config.current_enemy_index >= len(config.enemy_names):
            print("所有关卡已完成！")
            config.current_enemy_index = 0  # 重置为第一个敌人，或者根据需求修改                    
                    
        if config.enemy.name.startswith('CheckPoint') or config.enemy.name.endswith('.3') or config.enemy.name.endswith('3.2'):
            # 更新敌人对象为下一个
            config.current_enemy_index += 1
            print('节点更新，更新敌人为序号', config.current_enemy_index)
                               
        config.enemy = create_enemy(config.current_enemy_index)
        print(f"当前敌人已为：{config.enemy.name}")
                


                

    if (config.enemy.name.endswith('.1') and detect_img(game_window_handle, 'img/battle/wave2.3.png', (50, 50, 130, 100), 0.9)) or (config.enemy.name.endswith('.2') and detect_img(game_window_handle, 'img/battle/wave3.3.png', (50, 50, 130, 100), 0.9)):
        # 更新敌人对象为下一个
        config.current_enemy_index += 1
        print('波次更新，更新敌人为序号', config.current_enemy_index)

        if config.current_enemy_index >= len(config.enemy_names):
            print("所有关卡已完成！")
            config.current_enemy_index = 0  # 重置为第一个敌人，或者根据需求修改
                    
        config.enemy = create_enemy(config.current_enemy_index)
        print(f"当前敌人已为：{config.enemy.name}")

    if config.enemy.name.endswith('.1') and detect_img(game_window_handle, 'img/battle/wave3.3.png', (50, 50, 130, 100), 0.9):
        # 更新敌人对象为下一个
        config.current_enemy_index += 2
        print('波次更新2，更新敌人为序号', config.current_enemy_index)

        if config.current_enemy_index >= len(config.enemy_names):
            print("所有关卡已完成！")
            config.current_enemy_index = 0  # 重置为第一个敌人，或者根据需求修改
                    
        config.enemy = create_enemy(config.current_enemy_index)
        print(f"当前敌人已为：{config.enemy.name}")

    return config.enemy

def main():
    # 设置信号处理
    setup_signal_handlers()

    # 使用 resource_path 函数获取图片文件的路径
    battling_path = resource_path("img/battle/battling.png")

    # 使用构造好的路径读取图片
    battling_image = cv2.imread(battling_path, cv2.IMREAD_GRAYSCALE)
    if battling_image is None:
        print(f"未能读取模板图像：{battling_path}")
        exit()
    
    # 获取游戏窗口句柄
    game_window_handle = win32gui.FindWindow(None, "LimbusCompany")  # 替换成游戏窗口的标题
    if game_window_handle == 0:
        print("找不到游戏窗口！")
        exit()

    left, top, right, bottom = win32gui.GetWindowRect(game_window_handle)
    width = right - left
    height = bottom - top

    print('height=', height, 'width=', width)
    print("请确保游戏语言为英文，并且电脑显示缩放比例为100%。")  
    # 获取当前时间
    start_time = datetime.now()

    # 格式化当前时间为字符串
    formatted_time = start_time.strftime('%Y-%m-%d %H:%M:%S')

    # 打印当前时间
    print("当前时间:", formatted_time)
    
    # 设置窗口新的位置和大小
    win32gui.SetWindowPos(game_window_handle, win32con.HWND_TOP, 0, 0, 1616, 939, win32con.SWP_NOOWNERZORDER | win32con.SWP_NOZORDER)

    

    # 将游戏窗口置于前台
    win32gui.SetForegroundWindow(game_window_handle)

    donquixote = DonQuixote()
    honglu = HongLu()
    heathcliff = Heathcliff()
    wildhuntheathcliff = WildHuntHeathcliff()
    ismael = Ismael()
    ryoshu = RyoShu()
    rapryoshu = RAPRyoShu()
    sinclair = Sinclair()
    yisang = YiSang()
    lamentyisang = LamentYiSang()
    rodion = Rodion()
    outis = Outis()
    faust = Faust()
    sevenfaust = SevenFaust()
    crackfaust = CrackFaust()
    characters = [rodion, honglu, outis, ryoshu, rapryoshu, sinclair, donquixote, heathcliff,wildhuntheathcliff, ismael, yisang, lamentyisang, faust, crackfaust, sevenfaust]

    root = tk.Tk()
    app = EnemySelectorApp(root)
    def on_closing():
        app.save_settings()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
    
    # 获取选择的敌人对象
    config.enemy = app.get_selected_enemy()
    # 获取敌人的索引
    config.current_enemy_index = get_current_enemy_index()

    if config.enemy:
        print(f"选择的敌人是: {config.enemy.name}")
    else:
        print("未选择敌人")
        return False


    count_of_battling = 0
    
    try:
        while True:
            detected_enemies = []
            
            click((200, 50), game_window_handle)

            # 检测战斗结束并自动进入下一关
            if detect_battle_end(game_window_handle, True):
                print("战斗结束，进入下一关...")
                time.sleep(2)
                    
                
            config.enemy = update_enemy(game_window_handle)

            if detect_img(game_window_handle, 'img/window/clear_selection.png', (1300, 600, 1550, 670)):
                select_characters(game_window_handle, app)
                    
            if battling(game_window_handle, battling_image):
                count_of_battling += 1
                #config.already_seen_battling = True
                
                if detect_and_restart(game_window_handle):
                    sorted_characters = []
                    set_default()
                    honglu.position = None                      
                    detected_enemies = []
                    print("检测到重开条件，已执行重开操作。")
                else:
                    print("未检测到重开条件。")
                    
                set_shot(game_window_handle)
                shift_window(game_window_handle)



                # 使用OpenCV加载游戏窗口截图

                game_window_image_gray = get_screen(game_window_handle)  # 转换为灰度图像

                sorted_characters = find_character_positions(game_window_handle, characters)


                # 检测敌人
                detected_enemies = config.enemy.detect_enemy(game_window_handle)

                detected_enemies = handle_enemies(detected_enemies, game_window_handle, sorted_characters)

            else:
                print('count_of_battling清零')
                count_of_battling = 0

            if not detected_enemies:
                print("未检测到敌人。")
            else:   
                skill_enemy_situation = []
                print('activate_HongLu_dodge=',config.activate_HongLu_dodge, ' already_activate_HongLu_dodge=',config.already_activate_HongLu_dodge)
                for character in sorted_characters:
                    print('character1=', character.name, ' position=', character.position)
                    if character.name == 'HongLu' and config.activate_HongLu_dodge and not config.already_activate_HongLu_dodge and character.position and not character.detect_dodge(game_window_handle):
                        use_dodge_or_not = True
                        character.detect_skills(game_window_handle)
                        for _, _, _, template_name in character.current_skills:
                            if template_name.startswith('HongLu\\HongLu_s3'):
                                use_dodge_or_not = False
                                break

                        print('use_dodge_or_not=', use_dodge_or_not)
                        if use_dodge_or_not:                          
                            moveTo(honglu.position, game_window_handle)
                            click(honglu.position, game_window_handle)
                            config.activate_HongLu_dodge = False
                            config.already_activate_HongLu_dodge = True
                        break

                       

                for character in sorted_characters:
                    print(f"{character.name} 头像位置: {character.position}")
                    process_character(character, detected_enemies, game_window_handle, skill_enemy_situation)
                #break

            

            moveTo((200, 100), game_window_handle)
            time.sleep(1)
            if battling(game_window_handle, battling_image):
                print('count_of_battling=', count_of_battling)
                if count_of_battling >= 10:
                    
                    pyautogui.press('p')
                    time.sleep(1)
                    
                if detect_img(game_window_handle, 'img/battle/start.png', (1050, 635, 1150, 680)):
                    config.last_hit_refracted_generator = config.now_hit_refracted_generator

                    print("模拟按下 'enter' 键...")
                    #exit()
                    pyautogui.press('enter')
            
            times = 500
            while times >= 0 :
                click((200, 50), game_window_handle)
                times -= 1

                '''
                if keyboard.is_pressed('q'):
                    print("检测到 'q' 键按下，程序结束。")
                    sys.exit()
                '''

                if keyboard.is_pressed('enter'):
                    print("检测到 'enter' 键按下，程序继续。")
                    break

                # 截取游戏窗口的截图  
                game_window_image_gray = get_screen(game_window_handle)

                detect_and_handle_reconnect(game_window_handle)
                if detect_and_handle_try_again(game_window_handle):
                    detected_enemies = []
                detect_and_handle_summary(game_window_handle)

                if detect_img(game_window_handle, 'img/window/terminal.png', (1250, 670, 1530, 800)):

                    # 记录程序结束时间
                    end_time = datetime.now()
                    # 格式化当前时间为字符串
                    formatted_time = end_time.strftime('%Y-%m-%d %H:%M:%S')

                    # 计算程序运行时长
                    elapsed_time = end_time - start_time

                    # 格式化输出
                    days = elapsed_time.days
                    seconds = elapsed_time.seconds
                    hours, remainder = divmod(seconds, 3600)
                    minutes, seconds = divmod(remainder, 60)

                    print(f"程序运行时长: {days} 天, {hours} 小时, {minutes} 分钟, {seconds} 秒")
                    # 打印当前时间
                    print("当前时间:", formatted_time)
                    print('已经成功挑战完四号线')
                    try:
                        win32gui.PostMessage(game_window_handle, win32con.WM_CLOSE, 0, 0)
                        print("游戏窗口已关闭")
                    except Exception as e:
                        print(f"关闭游戏窗口时出错: {e}")
                    sys.exit()
                    
                
                game_window_image_gray = detect_and_handle_skip(game_window_handle)
                # detected_enemies = config.enemy.detect_enemy(game_window_handle)

                if battling(game_window_handle, battling_image) or detect_battle_end(game_window_handle) or detect_img(game_window_handle, 'img/window/clear_selection.png', (1300, 600, 1550, 670)) or detect_img(game_window_handle, "img/window/save_team.png", (1330,700,1550,810)):
                    break
                else:
                    print('count_of_battling清零')
                    count_of_battling = 0
                
                if not detected_enemies:
                    time.sleep(0.1)
                else:
                    break
    except KeyboardInterrupt:
        print('检测到 Ctrl+C 或 q 键，程序终止')
        sys.exit(0)

# 配置日志记录
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("app.log", mode='w'),
                        logging.StreamHandler(sys.stdout)
                    ])

if __name__ == "__main__":
    try:
# 设置键盘监听事件
        keyboard.hook(on_exit_key_event)
        main()
    except Exception as e:
        logging.error("An error occurred", exc_info=True)
    finally:
        # 取消键盘监听
        keyboard.unhook_all()
        input("Press Enter to close...")  # 等待用户输入
