import cv2
import os
import win32gui
import pyautogui
from datetime import datetime
import signal
import sys
import numpy as np

def load_template(template_path):
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        print(f"未能读取模板图像：{template_path}")
    return template

def load_templates(folder):
    templates = {}
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith(".png"):
                template_path = os.path.join(root, file)
                template = load_template(template_path)
                if template is not None:
                    templates[file] = template
    return templates

def click(position, game_window_handle):
    # 获取游戏窗口的左上角坐标
    left, top, _, _ = win32gui.GetWindowRect(game_window_handle)
    print('click_position=', position)
    # 点击位置，转换为相对于游戏窗口的坐标
    pyautogui.click(left + position[0], top + position[1])

def moveTo(position, game_window_handle):
    print('move_to=', position)
    # 获取游戏窗口的左上角坐标
    left, top, _, _ = win32gui.GetWindowRect(game_window_handle)
    
    # 点击位置，转换为相对于游戏窗口的坐标
    pyautogui.moveTo(left + position[0], top + position[1], duration=0.05)

def get_screen(game_window_handle, selected_region=None):
    """
    截取游戏窗口的截图，并返回灰度图像。
    
    :param game_window_handle: 游戏窗口的句柄。
    :param selected_region: 可选参数，指定需要截取的区域，格式为[(x1, y1), (x2, y2)]。
    :return: 截取后的灰度图像。
    """
    # 获取窗口的左、上、右、下边界
    left, top, right, bottom = win32gui.GetWindowRect(game_window_handle)
    width = right - left
    height = bottom - top

    # 截取整个游戏窗口的截图
    game_window_screenshot = pyautogui.screenshot(region=(left, top, width, height))
    game_window_image_gray = cv2.cvtColor(np.array(game_window_screenshot), cv2.COLOR_BGR2GRAY)

    # 如果指定了截取的区域
    if selected_region:
        (x1, y1), (x2, y2) = selected_region
        # 确保坐标在合理范围内
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(width, x2), min(height, y2)
        game_window_image_gray = game_window_image_gray[y1:y2, x1:x2]

    return game_window_image_gray
    
def right_click(position, game_window_handle):
    # 获取游戏窗口的左上角坐标
    left, top, _, _ = win32gui.GetWindowRect(game_window_handle)
    pyautogui.rightClick(left + position[0], top + position[1])

def dragTo(position, game_window_handle):
    # 获取游戏窗口的左上角坐标
    left, top, _, _ = win32gui.GetWindowRect(game_window_handle)
    pyautogui.dragTo(position[0] + left, position[1] + top, duration=0.5)

def save_screenshot_with_timestamp(image, prefix='screenshot', directory='screenshots'):
    # 创建目录如果它不存在
    if not os.path.exists(directory):
        os.makedirs(directory)
        
    # 生成带有时间戳的文件名
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    filename = f"{prefix}_{timestamp}.png"
    filepath = os.path.join(directory, filename)
    
    # 保存图像
    cv2.imwrite(filepath, image)
    print(f"Saved screenshot: {filepath}")

def detect_img(game_window_handle, icon_path, region=(0,0,1600,900), threshold=0.8, min_distance=50):
    """
    在指定的游戏窗口区域内检测标志图片，并返回所有相似度大于阈值的位置坐标。

    :param game_window_handle: 游戏窗口的句柄
    :param region: 截图的区域 (x1, y1, x2, y2)，相对于窗口左上角的坐标
    :param icon_path: 标志图片的路径
    :param threshold: 相似度阈值
    :param min_distance: 最小距离阈值，确保相邻点不会被检测为多个位置
    :return: 相似度大于阈值的位置坐标列表 [(x, y), ...]
    """
    # 获取游戏窗口的位置
    left, top, right, bottom = win32gui.GetWindowRect(game_window_handle)
    window_width = right - left
    window_height = bottom - top

    # 检查区域范围的有效性
    x1, y1, x2, y2 = region
    if x1 < 0 or y1 < 0 or x2 > window_width or y2 > window_height:
        raise ValueError("检测区域超出了游戏窗口的范围")

    # 截取指定区域的截图
    screenshot = pyautogui.screenshot(region=(left + x1, top + y1, x2 - x1, y2 - y1))
    game_window_image_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY)

    # 读取标志图片
    icon_image = cv2.imread(icon_path, cv2.IMREAD_GRAYSCALE)
    if icon_image is None:
        raise FileNotFoundError(f"无法加载标志图片: {icon_path}")

    # 使用模板匹配来检测标志
    result = cv2.matchTemplate(game_window_image_gray, icon_image, cv2.TM_CCOEFF_NORMED)
    loc = np.where(result >= threshold)

    # 收集匹配的位置
    matches = []
    for pt in zip(*loc[::-1]):
        matches.append((pt[0] + x1, pt[1] + y1))

    # 筛选相近的坐标
    filtered_matches = []
    for match in matches:
        if not filtered_matches:
            filtered_matches.append(match)
        else:
            if all(np.linalg.norm(np.array(match) - np.array(existing_match)) > min_distance for existing_match in filtered_matches):
                filtered_matches.append(match)

    return filtered_matches

def unique_positions(lists, min_distance=50):
    """
    合并多个位置列表并去除相近的位置，只保留一个位置。

    :param lists: 需要合并的多个列表，每个列表包含多个位置坐标 (x, y)
    :param min_distance: 最小距离阈值，确保相邻点不会被检测为多个位置
    :return: 去重后的位置列表
    """
    all_positions = [pos for lst in lists for pos in lst]
    
    unique_positions = []
    for pos in all_positions:
        if not unique_positions:
            unique_positions.append(pos)
        else:
            if all(np.linalg.norm(np.array(pos) - np.array(existing_pos)) > min_distance for existing_pos in unique_positions):
                unique_positions.append(pos)
    
    return unique_positions

def map_positions(detected_enemies, target_positions, max_x_diff=30, max_y_diff=30):
    """
    将 detected_enemies 列表中的 enemy_loc 映射到 target_positions 中相近的位置。

    :param detected_enemies: 列表，每个元素包含 (enemy_loc, w, h, template_name)
    :param target_positions: 目标位置列表
    :param max_x_diff: 最大允许的横坐标差异
    :param max_y_diff: 最大允许的纵坐标差异
    :return: 更新后的 detected_enemies 列表
    """
    mapped_enemies = []
    used_positions = set()

    for enemy in detected_enemies:
        enemy_loc = enemy[0]
        closest_target = None

        for target_pos in target_positions:
            if target_pos in used_positions:
                continue

            x_diff = abs(enemy_loc[0] - target_pos[0])
            y_diff = abs(enemy_loc[1] - target_pos[1])
        
            if x_diff <= max_x_diff and y_diff <= max_y_diff:
                closest_target = target_pos
                break

        if closest_target:
            used_positions.add(closest_target)
            mapped_enemy = (closest_target, *enemy[1:])
        else:
            mapped_enemy = (enemy_loc, *enemy[1:])  # 保留原始坐标

        mapped_enemies.append(mapped_enemy)

    return mapped_enemies

def adjust_brightness_contrast(image, alpha=1.0, beta=0):
    """
    调整图像的亮度和对比度
    alpha: 对比度控制 (1.0-3.0)
    beta: 亮度控制 (0-100)
    """
    adjusted = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return adjusted

def signal_handler(sig, frame):
    print('程序终止')
    sys.exit(0)

def setup_signal_handlers():
    signal.signal(signal.SIGINT, signal_handler)
    if hasattr(signal, 'SIGBREAK'):
        signal.signal(signal.SIGBREAK, signal_handler)

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
