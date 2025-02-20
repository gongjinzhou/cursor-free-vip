import warnings
import os
import subprocess
import shutil
from pathlib import Path
import sys

# 忽略特定警告
warnings.filterwarnings("ignore", category=SyntaxWarning)

def clean_build_dirs():
    """清理构建目录"""
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"已清理 {dir_name} 目录")

def build_app():
    """根据操作系统构建应用"""
    is_windows = sys.platform.startswith('win')
    is_mac = sys.platform.startswith('darwin')
    
    # 清理旧的构建文件
    clean_build_dirs()
    
    if is_windows:
        spec_file = 'build_windows.spec'
        print("正在为Windows构建...")
    elif is_mac:
        spec_file = 'build_mac.spec'
        print("正在为macOS构建...")
    else:
        print("不支持的操作系统")
        return False
    
    try:
        # 运行PyInstaller
        subprocess.run(['pyinstaller', spec_file], check=True)
        
        # 构建成功
        dist_dir = Path('dist')
        if is_windows:
            exe_path = dist_dir / 'CursorVIP.exe'
            if exe_path.exists():
                print(f"\n构建成功！可执行文件位置：{exe_path}")
                return True
        elif is_mac:
            app_path = dist_dir / 'CursorVIP.app'
            if app_path.exists():
                print(f"\n构建成功！应用程序位置：{app_path}")
                return True
        
        print("\n构建似乎成功了，但找不到输出文件")
        return False
        
    except subprocess.CalledProcessError as e:
        print(f"\n构建失败：{e}")
        return False
    except Exception as e:
        print(f"\n发生未知错误：{e}")
        return False

if __name__ == '__main__':
    if build_app():
        print("\n✨ 构建完成！")
    else:
        print("\n❌ 构建失败") 