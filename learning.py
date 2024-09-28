import cv2
import numpy as np
import pyautogui
import win32gui
import os
import time
import keyboard
import sys
import config
from enemy_class.enemy import Enemy
from config import enemy_offset_x, enemy_offset_y, reward_params, skill_enemy_params, default_low_reward
from utils import click, moveTo, right_click, adjust_brightness_contrast, save_screenshot_with_timestamp, resource_path 





def calculate_reward(character, skill_enemy_situation, skill, clash_sign, enemy_name, enemy_position):
    skill_list = skill.split('_')
    skill_name = skill_list[0] + '_' + skill_list[1]
    
    clash_reward = reward_params.get(clash_sign, 0)
    
    if enemy_name.startswith('ego'):
        print('处理敌人ego的收益')
        #if enemy_position[0] <= 1050:
            #print('确认己方不是最高速')
        if clash_sign != 'Unopposed':
            print('确认可以进行偷刀')
            if (skill_list[1] == 's1' or skill_list[1] == 's2' or skill_list[1] == 's3') and (skill_list[1] != 'dodge' and skill_list[1] != 'defend'):
                print('确认己方不是ego')
                if character.position[0] <= 550:
                    print('确认己方是最高速')
                    teammate_target_ego = False
                    for the_skill_name, _, the_enemy_name, the_enemy_position, the_clash_sign in skill_enemy_situation:
                        if the_enemy_position == enemy_position and the_clash_sign != 'Unopposed':
                            teammate_target_ego = True
                            break
                    if teammate_target_ego:
                        print('队友正在拼ego，准备偷刀')
                        clash_reward = 3
                        enemy_name = 'ego0'
                    else:
                        print('没有队友拼ego，不准备偷刀')
                else:
                    clash_reward = 3
                    enemy_name = 'ego0'
                    
                    
    print('skill=', skill, ' clash_sign=', clash_sign, ' enemy_name=', enemy_name)                 

    # 判断是否在技能-敌人收益参数中找到匹配
    skill_enemy_reward = skill_enemy_params.get((skill_name, enemy_name[:-1]))
    if skill_enemy_reward is None:
        # 如果找不到匹配，则使用默认的低收益参数
        skill_enemy_reward = default_low_reward.get(skill_name, 0)  # 使用默认低收益参数

    if enemy_name.startswith('grounding_refusal'):
        if skill_list[0] == config.last_hit_refracted_generator:
            print('让击中电箱的', skill_list[0], '进行拼点')
            skill_enemy_reward *= 1000
        else:
            skill_enemy_reward /= 1000

    if skill_list[1] != 's1' and skill_list[1] != 's2' and skill_list[1] != 's3' and skill_list[1] != 's4' and skill_list[1] != 'dodge' and skill_list[1] != 'defend':
        skill_enemy_reward *= 100
        
    # 引入惩罚系数，根据技能分配的均匀性调整收益
    enemy_count = 0
    for the_skill_name, _, the_enemy_name, the_enemy_position, the_clash_sign in skill_enemy_situation:
        if the_enemy_position == enemy_position:
            #print('the_enemy_name=', the_enemy_name, 'the_skill_name=',skill_name)
            if the_enemy_name.startswith('ego'):
                enemy_count += 1
            elif the_clash_sign == 'Unopposed':
                enemy_count += 0.5
            elif the_clash_sign == 'Neutral':
                enemy_count += 0.7
            elif the_clash_sign == 'Favored':
                enemy_count += 0.9
            else:
                enemy_count += 1
            #if the_skill_name.startswith('YiSang_crow'):
                #enemy_count += 3

            if the_enemy_name.startswith('overcharge_release'):
                enemy_count += 1000

        
                
    penalty_factor = 1 / (1 + enemy_count)
    return clash_reward * skill_enemy_reward * penalty_factor


def move_to_enemy_positions_and_select(character, detected_enemies, game_window_handle, skills, skill_enemy_situation):
    best_enemy_position = None
    best_enemy_name = None
    best_skill = None
    best_skill_position = None
    best_clash_sign = None
    least_best_clash_sign = None
    highest_reward = 0
    
    left, top, right, bottom = win32gui.GetWindowRect(game_window_handle)
    width = right - left
    height = bottom - top

    for skill in skills:
        skill_position, w, h, template_name = skill
        skill_name = os.path.basename(template_name).split(".")[0]  # 提取技能名称

        # 点击技能位置
        moveTo(skill_position, game_window_handle)
        click(skill_position, game_window_handle)

        for i, (enemy_loc, w, h, enemy_template_name) in enumerate(detected_enemies):
            '''
            # 检查是否按下了 'q' 键
            if keyboard.is_pressed('q'):
                print("检测到 'q' 键按下，程序结束。")
                sys.exit()  # 终止整个程序
            '''
            enemy_name = os.path.basename(enemy_template_name).split(".")[0]
            x, y = enemy_loc
            moveTo([x + enemy_offset_x, y + enemy_offset_y], game_window_handle)  # 移动鼠标到敌人位置
            if skill_name.startswith('Sinclair') or enemy_name.startswith('echoing_cry'):
                click([x + enemy_offset_x, y + enemy_offset_y], game_window_handle)
                moveTo(skill_position, game_window_handle)

            # 截取整个游戏窗口的截图
            game_window_screenshot = pyautogui.screenshot(region=(left, top, width, height))

            # 将截图转换为灰度图像，并裁剪感兴趣区域
            game_window_image_gray = cv2.cvtColor(np.array(game_window_screenshot), cv2.COLOR_RGB2GRAY)[0:80, 745:870]
            # 调整亮度和对比度
            #game_window_image_gray = adjust_brightness_contrast(game_window_image_gray, alpha=1.5, beta=3)
            # 保存检测区域截图
            #save_screenshot_with_timestamp(game_window_image_gray, prefix='detect_region')
            
            # 检测画面上方区域是否有匹配的标志
            detected_clash_sign = detect_clash_sign(game_window_image_gray, game_window_handle)

            # 计算当前组合的收益
            if detected_clash_sign:
                if not least_best_clash_sign or (reward_params[detected_clash_sign] >= reward_params[least_best_clash_sign] and detected_clash_sign != 'Unopposed'):
                    least_best_clash_sign = detected_clash_sign
                current_reward = calculate_reward(character, skill_enemy_situation, skill_name, detected_clash_sign, enemy_name, enemy_loc)
                print(f"检测到标志: {detected_clash_sign}, 技能: {skill_name}, 敌人: {enemy_name}, 敌人位置: {enemy_loc}, 收益: {current_reward}")
                if current_reward > highest_reward:
                    highest_reward = current_reward
                    best_enemy_position = (x, y)
                    best_enemy_name = enemy_template_name
                    best_skill = skill_name
                    best_skill_position = skill_position
                    best_clash_sign = detected_clash_sign

            if skill_name.startswith('Sinclair') or enemy_name.startswith('echoing_cry'):
                click(skill_position, game_window_handle)
                click(skill_position, game_window_handle)
                   

        # 在遍历技能列表的末尾添加右键点击
        right_click([200, 50], game_window_handle)
        #time.sleep(5)
        
    if config.clash_disvantage_ego and len(detected_enemies) > 3 and not best_enemy_name.startswith('ego') and (least_best_clash_sign == 'Struggling' or least_best_clash_sign == 'Hopeless' or best_clash_sign == 'Struggling' or best_clash_sign == 'Hopeless') and ('s1' in best_skill or 's2' in best_skill or 's3' in best_skill):
        if character.name == 'HongLu':
            if config.activate_HongLu_dodge and not config.already_activate_HongLu_dodge:
                config.activate_HongLu_dodge = False
            elif config.already_activate_HongLu_dodge:
                config.activate_HongLu_dodge = True
            config.already_activate_HongLu_dodge = False

        print('拼点劣势，使用ego')
        print('best_enemy_name=', best_enemy_name)
       
        index = 0
        if not character.use_ego_skill(game_window_handle, character.ego_templates, index):
            moveTo(character.position, game_window_handle)
            click(character.position, game_window_handle)
        skill_position, w, h, _ = skills[0]
        up_skill_position, w, h, _ = skills[1]
        skill_name = character.ego_names[index]  # 提取技能名称

        click(up_skill_position, game_window_handle)
        click((200, 50), game_window_handle)

        # 点击技能位置
        moveTo(skill_position, game_window_handle)
        click(skill_position, game_window_handle)

        for i, (enemy_loc, w, h, enemy_template_name) in enumerate(detected_enemies):
            # 检查是否按下了 'q' 键
            if keyboard.is_pressed('q'):
                print("检测到 'q' 键按下，程序结束。")
                sys.exit()  # 终止整个程序
            enemy_name = os.path.basename(enemy_template_name).split(".")[0]
            x, y = enemy_loc
            moveTo([x + enemy_offset_x, y + enemy_offset_y], game_window_handle)  # 移动鼠标到敌人位置
        
            # 截取整个游戏窗口的截图
            game_window_screenshot = pyautogui.screenshot(region=(left, top, width, height))

            # 将截图转换为灰度图像，并裁剪感兴趣区域
            game_window_image_gray = cv2.cvtColor(np.array(game_window_screenshot), cv2.COLOR_RGB2GRAY)[0:80, 745:870]
            # 调整亮度和对比度
            #game_window_image_gray = adjust_brightness_contrast(game_window_image_gray, alpha=1.5, beta=3)
            # 保存检测区域截图
            #save_screenshot_with_timestamp(game_window_image_gray, prefix='detect_region')
            
            # 检测画面上方区域是否有匹配的标志
            if enemy_template_name.startswith('ego_'):
                
                detected_clash_sign = 'Dominating'
            else:
                detected_clash_sign = detect_clash_sign(game_window_image_gray, game_window_handle)

            # 计算当前组合的收益
            if detected_clash_sign:
                current_reward = calculate_reward(character, skill_enemy_situation, skill_name, detected_clash_sign, enemy_name, enemy_loc)
                print(f"检测到标志: {detected_clash_sign}, 技能: {skill_name}, 敌人: {enemy_name}, 敌人位置: {enemy_loc}, 收益: {current_reward}")
                if current_reward > highest_reward:
                    highest_reward = current_reward
                    best_enemy_position = (x, y)
                    best_enemy_name = enemy_template_name
                    best_skill = skill_name
                    best_skill_position = skill_position
                    best_clash_sign = detected_clash_sign
                   

        # 在遍历技能列表的末尾添加右键点击
        right_click([200, 50], game_window_handle)

    if character.name == 'WildHuntHeathcliff' and len(detected_enemies) > 2 and 'stagger' not in best_enemy_name and ((best_clash_sign != 'Unopposed') or ('s1' in skills[0][3] and 's1' in skills[1][3])) and 's1' in best_skill:
        moveTo(character.position, game_window_handle)
        click(character.position, game_window_handle)
        skill_position, w, h, _ = skills[0]
        skill_name = 'WildHuntHeathcliff_defend'  # 提取技能名称

        highest_reward = 5.0
        best_skill = skill_name
        best_skill_position = skill_position
        best_clash_sign = 'Dominating'
                   
        
    if  best_skill and best_skill_position and best_enemy_name and best_enemy_position and best_clash_sign:
        click(best_skill_position, game_window_handle)  # 点击最佳技能位置
        click([best_enemy_position[0] + enemy_offset_x, best_enemy_position[1] + enemy_offset_y], game_window_handle)
        if best_enemy_name.startswith('overcharge_release'):
            config.now_hit_refracted_generator = character.name
            print(character.name, '击中电箱')
        print(f"选择的最佳敌人位置: {best_enemy_position}, 敌人名字:{best_enemy_name}, 使用技能: {best_skill}, 拼点情况: {best_clash_sign}")
        # 更新被选中敌人的技能计数
        if skill_enemy_situation:
            print('skill_enemy_situation=', skill_enemy_situation)
            for i, (skill_name, skill_position, enemy_name, enemy_position, clash_sign) in enumerate(skill_enemy_situation):
                if clash_sign in reward_params:
                    print('skill_name=', skill_name, ' enemy_name=', enemy_name, 'clash_sign=', clash_sign)
                    if not best_skill.startswith('WildHuntHeathcliff_defend') and enemy_position == best_enemy_position:
                        if skill_name.startswith('WildHuntHeathcliff_defend') or (enemy_name.startswith('ego') and clash_sign != 'Unopposed') or (reward_params[clash_sign] >= reward_params[best_clash_sign] and clash_sign != 'Unopposed' and best_clash_sign != 'Defense') :
                            #and not enemy_name.startswith('track_them_to_the_end')
                            print('clash_sign=', clash_sign)
                            click(skill_position, game_window_handle)  # 点击最佳技能位置
                            
                            click(skill_position, game_window_handle)
                            
                            click([enemy_position[0] + enemy_offset_x, enemy_position[1] + enemy_offset_y], game_window_handle)
                            
                            best_clash_sign = 'Unopposed'
                        else :
                            skill_enemy_situation[i] = (skill_name, skill_position, enemy_name, enemy_position, 'Unopposed')
                else:
                    break
                
        skill_enemy_situation.append((best_skill, best_skill_position, best_enemy_name, best_enemy_position, best_clash_sign))
    else:
        print("没有找到合适的敌人或技能组合。")



def detect_clash_sign(game_window_image_gray, game_window_handle):
    clash_templates = [
        "img/clash/Dominating0.png",
        "img/clash/Favored0.png",
        "img/clash/Neutral0.png",
        "img/clash/Unopposed0.png",
        "img/clash/Struggling0.png",
        "img/clash/Hopeless0.png",
        "img/clash/Defense0.png",
        # "img/clash/OneSidedGuard0.png",
        # "img/clash/Hopeless1.png",
        # "img/clash/Hopeless2.png",
        # "img/clash/Hopeless3.png",
    ]

    # 使用 resource_path 函数转换路径并加载模板图像
    clash_template_images = []
    clash_template_names = []
    for template in clash_templates:
        template_path = resource_path(template)
        template_image = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        if template_image is not None:
            clash_template_images.append(template_image)
            clash_template_names.append(template_path)
        else:
            print(f"未能读取模板图像：{template_path}")

    best_match = 'Unopposed'
    best_match_value = 0.0
    match_values = {}

    for template_image, template_name in zip(clash_template_images, clash_template_names):
        result = cv2.matchTemplate(game_window_image_gray, template_image, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        template_base_name = os.path.basename(template_name).split(".")[0][:-1]  # 去掉文件扩展名和尾随数字
        match_values[template_base_name] = max_val

        # 打印调试信息
        #print('clash_sign=', template_base_name, ' max_val=', max_val)

        if max_val >= 0.4 and max_val > best_match_value:
            best_match_value = max_val
            best_match = template_base_name

    return best_match

def process_character(character,detected_enemies, game_window_handle, skill_enemy_situation):
    # 创建角色对象
    # character = character_class()

    # 检测角色位置
    if character.position:
        character_position = character.position
        print('角色头像坐标已知为', character.position)
    else:
        print('角色头像坐标未知')
    
    # 检测角色的技能
    character_skills = character.detect_skills(game_window_handle)
    
    # 去除重复的技能
    unique_skills = []
    seen_templates = set()
    
    for skill in character_skills:
        loc, w, h, template_name = skill
        if template_name not in seen_templates:
            seen_templates.add(template_name)
            unique_skills.append(skill)
            print(f"检测到的技能: {template_name} 位置: {loc}")

    
    # 将检测到的敌人位置列表传递给移动和选择技能函数
    move_to_enemy_positions_and_select(character, detected_enemies, game_window_handle, unique_skills, skill_enemy_situation)
