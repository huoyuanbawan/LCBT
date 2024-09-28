import shutil
import os
from cx_Freeze import setup, Executable
import site

# 删除现有的 build_exe 目录
build_exe_dir = "build_exe"
if os.path.exists(build_exe_dir):
    shutil.rmtree(build_exe_dir)

# 获取当前 Python 环境中的 site-packages 路径
site_packages_paths = site.getsitepackages()

# 查找 pywin32_system32 路径
pywin32_path = None

for path in site_packages_paths:
    potential_path = os.path.join(path, 'pywin32_system32')
    if os.path.exists(potential_path):
        pywin32_path = potential_path
        break

if not pywin32_path:
    raise RuntimeError("未找到 pywin32 的路径，请确保 pywin32 已正确安装。")

# 自动查找 pywin32 相关的 DLL 文件
pythoncom_dll = None
pywintypes_dll = None

for file in os.listdir(pywin32_path):
    if file.startswith('pythoncom') and file.endswith('.dll'):
        pythoncom_dll = os.path.join(pywin32_path, file)
    elif file.startswith('pywintypes') and file.endswith('.dll'):
        pywintypes_dll = os.path.join(pywin32_path, file)

if not pythoncom_dll or not pywintypes_dll:
    raise RuntimeError("未找到 pywin32 的必要 DLL 文件，请检查 pywin32 的安装。")

# 定义 include_files 列表
include_files = [
    'config.py',
    ('img', 'img'),  # 将整个 img 目录包含进来
    (pythoncom_dll, os.path.basename(pythoncom_dll)),  # 添加 pythoncom DLL
    (pywintypes_dll, os.path.basename(pywintypes_dll)),  # 添加 pywintypes DLL
]

# 定义 build_exe_options
build_exe_options = {
    'packages': ['cv2', 'datetime', 'numpy', 'pyautogui', 'win32gui', 'keyboard', 'tkinter', 'threading', 'logging', 'win32con', 'json'],
    'include_files': include_files,
    'includes': ['tkinter'],  # 确保包含 tkinter
    'excludes': []  # 排除的模块
}

# 设置 setup 函数
setup(
    name='LCBT',
    version='1.0',
    description='LCBT application',
    options={'build_exe': build_exe_options},
    executables=[Executable('main.py', base=None)]
)
