import runpy
from pathlib import Path
from tkinter import *
from tkinter import filedialog
import configparser
import sys
import logging
import os
import config
import subprocess
path = config.get_config_directory()
# 更改工作目录为脚本所在目录
os.chdir(path)

# 打印当前工作目录
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets/frame0")

config_file_path = "config.txt"
config = configparser.ConfigParser()
config.read(config_file_path)

window = Tk()
window.title(f"早柚原神自动化 V0.1.2                           Github主页：https://github.com/PengZhangSDF/GIAA   欢迎提交issue           ")
window.geometry("1032x795")
window.configure(bg="#FFFFFF")
button_images = {}

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=795,
    width=1032,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
middle_frame = Frame(window, bg="#FFFFFF")
middle_frame.place(x=319, y=116, width=324, height=622)
canvas.place(x=0, y=0)


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


# 初始化全局变量
checked_image_path = relative_to_assets("True.png")
unchecked_image_paths = [
    relative_to_assets("button_1.png"),
    relative_to_assets("button_2.png"),
    relative_to_assets("button_3.png"),
    relative_to_assets("button_4.png"),
    relative_to_assets("button_5.png"),
    relative_to_assets("button_6.png"),
]


def toggle_button(button, variable_name, current_state, unchecked_image_path, section='Run'):
    global button_images
    # 切换按钮图片
    if current_state:
        new_image = PhotoImage(file=unchecked_image_path)
        button.config(image=new_image)
        config.set(section, variable_name, "False")
    else:
        new_image = PhotoImage(file=checked_image_path)
        button.config(image=new_image)
        config.set(section, variable_name, "True")

    # 更新按钮图片对象
    button_images[variable_name] = new_image

    # 更新config.txt文件
    with open(config_file_path, "w") as configfile:
        config.write(configfile)
def main_run():
    try:
        runpy.run_path('main.py')
    except:
        subprocess.run(['../Main.exe'])
    append_to_console("启动原神！！")



# 高级设置都在这里定义 #####################################################################################################
# ######################################################################################################################

def clear_middle_section():
    for widget in middle_frame.winfo_children():
        widget.destroy()


def start_genshin_settings():
    clear_middle_section()
    Label(middle_frame, font=("", 12), text="原神路径:").grid(row=0, column=0, sticky='w')
    path_entry = Entry(middle_frame, width=40)
    path_entry.grid(row=2, column=0)
    path_entry.insert(0, config.get("Start", "yuanshen_path"))

    button_4A_image = PhotoImage(
        file=checked_image_path if config.getboolean("Run", "update") else relative_to_assets(
            "button_1.png"))
    button_4A = Button(
        middle_frame,  # 确保按钮添加到 middle_frame 中
        image=button_4A_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: toggle_button(button_4A, "update",
                                      config.getboolean("Run", "update"),
                                      relative_to_assets("button_1.png"), section="Run"),
        relief="flat"
    )
    button_4A.grid(row=9, column=0, padx=10, pady=10)  # 使用 grid 布局
    button_images["update"] = button_4A_image
    Label(middle_frame, text="检查原神更新:").grid(row=9, column=0, sticky='w')

    def choose_path():
        chosen_path = filedialog.askopenfilename()
        if chosen_path:
            path_entry.delete(0, END)
            path_entry.insert(0, chosen_path)

    def select_path(entry):
        path = filedialog.askopenfilename()
        if path:
            entry.delete(0, END)
            entry.insert(0, path)
            config.set("Start", "launcher_path", path)
            with open(config_file_path, "w") as configfile:
                config.write(configfile)
                append_to_console("路径已自动保存")

    def check_run_gia():
        if config.getboolean("Run", "update"):
            if not hasattr(check_run_gia, "gia_widgets_added"):
                # 添加 GIA 路径选择控件
                gia_path_label = Label(middle_frame, text="米哈游启动器路径:")
                gia_path_label.grid(row=12, column=0, sticky='w')
                gia_path_entry = Entry(middle_frame, width=40)
                gia_path_entry.grid(row=13, column=0)
                gia_path_entry.insert(0, config.get("Start", "launcher_path", fallback=""))
                gia_path_button = Button(middle_frame, text="选择路径", command=lambda: select_path(gia_path_entry))
                gia_path_button.grid(row=14, column=0, padx=5)
                check_run_gia.gia_widgets_added = (gia_path_label, gia_path_entry, gia_path_button)
        else:
            if hasattr(check_run_gia, "gia_widgets_added"):
                # 删除 GIA 路径选择控件
                for widget in check_run_gia.gia_widgets_added:
                    widget.destroy()
                del check_run_gia.gia_widgets_added
        middle_frame.after(10, check_run_gia)

    Button(middle_frame, text="选择路径", command=choose_path).grid(row=0, column=0)
    # Label(middle_frame, text="", bg='white').grid(row=3, column=100, sticky='w')
    Label(middle_frame,
          text="    如果要自动启动原神，请将你的原神路径 \n 选择/填写在此处，不是启动器路径", bg='white').grid(row=4,
                                                                                                             column=0,
                                                                                                             sticky='w')
    Label(middle_frame, text="", bg='white').grid(row=5, column=100, sticky='w')

    Label(middle_frame, text="账号:").grid(row=6, column=0, sticky='w')
    account_entry = Entry(middle_frame, width=20)
    account_entry.grid(row=6, column=0)
    account_entry.insert(0, config.get("Start", "account"))

    Label(middle_frame, text="密码:").grid(row=7, column=0, sticky='w')
    password_entry = Entry(middle_frame, width=20)  # show="*"
    password_entry.grid(row=7, column=0)
    password_entry.insert(0, config.get("Start", "password"))

    def save_settings(event=None):
        config.set("Start", "yuanshen_path", path_entry.get())
        config.set("Start", "account", account_entry.get())
        config.set("Start", "password", password_entry.get())
        with open(config_file_path, "w") as configfile:
            config.write(configfile)

    Label(middle_frame, text="", bg='white').grid(row=8, column=100, sticky='w')
    Label(middle_frame, text="", bg='white').grid(row=49, column=100, sticky='w')
    Label(middle_frame, text="我们无法把您的密码加密储存，因此您的密码\n将以字符串的形式储存在config.txt里，请您\n在信任的设备上使"
                             "用这个功能,在账号密码为\n空时，程序会在登录界面弹出时输入空格", bg='white',
          font=("", 12)).grid(row=50, column=0, sticky='w')

    path_entry.bind("<KeyRelease>", save_settings)
    account_entry.bind("<KeyRelease>", save_settings)
    password_entry.bind("<KeyRelease>", save_settings)
    window.after(500, save_settings)
    middle_frame.after(10, check_run_gia)


def check_schedule_settings():
    clear_middle_section()
    Label(middle_frame,
          text="  此功能供在完整运行情况下进行进度检查\n注意：没有勾选的选项即使进行进度检查也不会运行,\n"
               "      强制运行秘境除外\n",
          bg='white').grid(row=9, column=0, sticky='w')


def enigma_settings():
    clear_middle_section()

    def update_combat_file(selection):
        config.set("AutoFight", "using_combat_file", selection if selection != '自动选择' else '')
        current_combat_file.set(f"当前战斗配置文件: {selection}")
        with open(config_file_path, "w") as configfile:
            config.write(configfile)

    # Get list of .txt files from ./AutoFight/AutoFightconfig
    config_dir = './AutoFight/AutoFightconfig'
    txt_files = [f for f in os.listdir(config_dir) if f.endswith('.txt')]
    file_options = ['自动选择'] + txt_files

    # Display current combat configuration file
    current_combat_file = StringVar()
    current_combat_file.set(f"当前战斗配置文件: {config.get('AutoFight', 'using_combat_file', fallback='自动选择')}")
    Label(middle_frame, textvariable=current_combat_file).grid(row=90, column=0, sticky='w')

    # Create OptionMenu for file selection
    selected_file = StringVar()
    selected_file.set('选择战斗配置文件')
    file_menu = OptionMenu(middle_frame, selected_file, *file_options, command=update_combat_file)
    file_menu.grid(row=91, column=0, pady=10)



    Label(middle_frame, text="灵敏度:").grid(row=0, column=0, sticky='w')
    sensitivity_entry = Entry(middle_frame, width=20)
    sensitivity_entry.grid(row=0, column=0)
    sensitivity_entry.insert(0, config.get("Enigma", "offset_per_degree"))
    Label(middle_frame, text="强制运行秘境:").grid(row=10, column=0, sticky='w')
    button_2A_image = PhotoImage(
        file=checked_image_path if config.getboolean("Run", "q_run_enigma") else relative_to_assets(
            "button_1.png")
    )
    button_2A = Button(
        middle_frame,  # 确保按钮添加到 middle_frame 中
        image=button_2A_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: toggle_button(button_2A, "q_run_enigma",
                                      config.getboolean("Run", "q_run_enigma"),
                                      relative_to_assets("button_1.png"), section="Run"),
        relief="flat"
    )
    button_2A.grid(row=10, column=0, padx=10, pady=10)  # 使用 grid 布局
    button_images["q_run_enigma"] = button_2A_image

    button_3A_image = PhotoImage(
        file=checked_image_path if config.getboolean("Enigma", "decompose_relics") else relative_to_assets(
            "button_1.png")
    )

    Label(middle_frame, text="自动分解4星以下圣遗物:").grid(row=15, column=0, sticky='w')
    button_3A = Button(
        middle_frame,  # 确保按钮添加到 middle_frame 中
        image=button_3A_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: toggle_button(button_3A, "decompose_relics",
                                      config.getboolean("Enigma", "decompose_relics"),
                                      relative_to_assets("button_1.png"), section="Enigma"),
        relief="flat"
    )
    button_3A.grid(row=15, column=0, padx=10, pady=10)  # 使用 grid 布局
    button_images["decompose_relics"] = button_3A_image

    enigma_config_path = './config/Enigma.txt'

    def read_enigma_config():
        enigma_dict = {
            "Enigma_now": "",
            "Enigma_first": [],
            "Enigma_second": [],
            "Enigma_third": []
        }
        current_section = None
        with open(enigma_config_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line.startswith('#') or line.startswith(';'):
                    continue  # Skip comment lines
                if line.startswith('[') and line.endswith(']'):
                    current_section = line[1:-1]
                elif current_section:
                    if current_section == "Enigma_now":
                        enigma_dict[current_section] = line
                    else:
                        enigma_dict[current_section].append(line)
        return enigma_dict

    enigma_config = read_enigma_config()

    # Debugging output
    print("Enigma Config Loaded:")
    for key, value in enigma_config.items():
        print(f"{key}: {value}")

    # Display current Enigma selection
    current_enigma = StringVar()
    current_enigma.set(f"当前选择秘境: {enigma_config['Enigma_now']}")
    Label(middle_frame, textvariable=current_enigma).grid(row=80, column=0, sticky='w')

    def update_enigma_selection(selection):
        enigma_config["Enigma_now"] = selection
        current_enigma.set(f"当前选择秘境: {selection}")
        with open(enigma_config_path, "w", encoding='utf-8') as file:
            for section, values in enigma_config.items():
                file.write(f"[{section}]\n")
                if isinstance(values, list):
                    for value in values:
                        file.write(f"{value}\n")
                else:
                    file.write(f"{values}\n")

    def load_enigma_list():
        enigma_menu = Toplevel()
        enigma_menu.title('选择秘境')

        Label(enigma_menu, text="==========圣遗物秘境==========",font=("", 14)).grid(row=0, column=0, columnspan=len(enigma_config["Enigma_first"]))
        row = 0
        for i, option in enumerate(enigma_config["Enigma_first"]):
            if i == 6 or i == 12 or i ==18 or i == 24:
                row = row + 1
            Button(enigma_menu, text=option,font=("", 14), command=lambda opt=option: update_enigma_selection(opt)).grid(row=row+1,
                                                                                                           column=i-row*6)

        Label(enigma_menu, text="==========武器素材秘境==========",font=("", 14)).grid(row=20, column=0, columnspan=len(enigma_config["Enigma_second"]))
        for i, option in enumerate(enigma_config["Enigma_second"]):
            Button(enigma_menu, text=option,font=("", 14), command=lambda opt=option: update_enigma_selection(opt)).grid(row=21,
                                                                                                           column=i)

        Label(enigma_menu, text="==========天赋素材秘境==========",font=("", 14)).grid(row=40, column=0, columnspan=len(enigma_config["Enigma_third"]))
        for i, option in enumerate(enigma_config["Enigma_third"]):
            Button(enigma_menu, text=option,font=("", 14), command=lambda opt=option: update_enigma_selection(opt)).grid(row=41,
                                                                                                           column=i)
        Label(enigma_menu, text="注释:花染之庭 原名 椛染之庭", font=("", 10)).grid(row=60, column=0)
    Button(middle_frame, text="选择秘境", command=load_enigma_list).grid(row=81, column=0, pady=10)

    Label(middle_frame,
          text="\n",bg='white').grid(row=82, column=0, sticky='w')
    def save_settings(event=None):
        sensitivity = sensitivity_entry.get()
        try:
            float(sensitivity)
        except ValueError:
            config.set("Enigma", "offset_per_degree", '')
            append_to_console("已清空该值")
            with open(config_file_path, "w") as configfile:
                config.write(configfile)
        else:
            config.set("Enigma", "offset_per_degree", sensitivity)
            with open(config_file_path, "w") as configfile:
                config.write(configfile)
            append_to_console("已自动保存")

    Label(middle_frame, text="", bg='white').grid(row=1, column=100, sticky='w')
    Label(middle_frame, text="每单位Pydirectinput xOffset/视角转动角度 的值"
                             "\n每个电脑这个值不一样，修改灵敏度之后请删除这个值"
                             "\n程序会在下一次进行秘境战斗时重新计算", bg='white').grid(row=2, column=0, sticky='w')

    sensitivity_entry.bind("<KeyRelease>", save_settings)


def daily_mission_settings():
    clear_middle_section()

    Label(middle_frame, text="寻找次数:").grid(row=0, column=0, sticky='w')
    found_times_entry = Entry(middle_frame, width=20)
    found_times_entry.grid(row=0, column=0)
    found_times_entry.insert(0, config.get("AutoDaily", "found_times"))
    Label(middle_frame, text="程序搜索委托可能'手滑'定位不到委托\n"
                             "增大委托搜索次数可以增加容错率，\n但也会增加大量时间", bg='white', font=("", 12)).grid(
        row=9, column=0, sticky='w')
    Label(middle_frame, text="使用GIA补足委托:").grid(row=10, column=0, sticky='w')
    button_3A_image = PhotoImage(
        file=checked_image_path if config.getboolean("Run", "run_gia") else relative_to_assets(
            "button_1.png")
    )
    button_3A = Button(
        middle_frame,  # 确保按钮添加到 middle_frame 中
        image=button_3A_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: toggle_button(button_3A, "run_gia",
                                      config.getboolean("Run", "run_gia"),
                                      relative_to_assets("button_1.png"), section="Run"),
        relief="flat"
    )
    button_3A.grid(row=10, column=0, padx=10, pady=10)  # 使用 grid 布局
    button_images["run_gia"] = button_3A_image

    Label(middle_frame, text="不使用本程序自动委托系统:").grid(row=15, column=0, sticky='w')
    button_4A_image = PhotoImage(
        file=checked_image_path if config.getboolean("AutoDaily", "skip_auto_daily_program") else relative_to_assets(
            "button_1.png")
    )
    button_4A = Button(
        middle_frame,  # 确保按钮添加到 middle_frame 中
        image=button_4A_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: toggle_button(button_4A, "skip_auto_daily_program",
                                      config.getboolean("AutoDaily", "skip_auto_daily_program"),
                                      relative_to_assets("button_1.png"), section="AutoDaily"),
        relief="flat"
    )
    button_4A.grid(row=16, column=0, padx=10, pady=10)  # 使用 grid 布局
    button_images["skip_auto_daily_program"] = button_4A_image

    def select_path(entry):
        path = filedialog.askopenfilename()
        if path:
            entry.delete(0, END)
            entry.insert(0, path)
            config.set("Start", "gia_path", path)
            with open(config_file_path, "w") as configfile:
                config.write(configfile)
                append_to_console("路径已自动保存")

    window.after(500, lambda: select_path)

    def check_run_gia():
        if config.getboolean("Run", "run_gia"):
            if not hasattr(check_run_gia, "gia_widgets_added"):
                # 添加 GIA 路径选择控件
                gia_path_label = Label(middle_frame, text="GIA路径:")
                gia_path_label.grid(row=20, column=0, sticky='w')
                gia_path_entry = Entry(middle_frame, width=40)
                gia_path_entry.grid(row=21, column=0)
                gia_path_entry.insert(0, config.get("Start", "gia_path", fallback=""))
                gia_path_button = Button(middle_frame, text="选择路径", command=lambda: select_path(gia_path_entry))
                gia_path_button.grid(row=22, column=0, padx=5)
                check_run_gia.gia_widgets_added = (gia_path_label, gia_path_entry, gia_path_button)
        else:
            if hasattr(check_run_gia, "gia_widgets_added"):
                # 删除 GIA 路径选择控件
                for widget in check_run_gia.gia_widgets_added:
                    widget.destroy()
                del check_run_gia.gia_widgets_added
        middle_frame.after(10, check_run_gia)

    def save_settings(event=None):
        found_times = found_times_entry.get()
        if found_times.isdigit():
            config.set("AutoDaily", "found_times", found_times)
            with open(config_file_path, "w") as configfile:
                config.write(configfile)


    found_times_entry.bind("<KeyRelease>", save_settings)
    found_times_entry.bind("<FocusOut>", save_settings)
    found_times_entry.bind("<FocusIn>", save_settings)
    middle_frame.after(10, check_run_gia)


def get_reward_settings():
    clear_middle_section()
    Label(middle_frame, text="使用长效历练点:").grid(row=1, column=0, sticky='w')
    # 添加按钮并设置初始图片
    button_1A_image = PhotoImage(
        file=checked_image_path if config.getboolean("AutoDaily", "use_experience_point") else relative_to_assets(
            "button_1.png")
    )
    button_1A = Button(
        middle_frame,  # 确保按钮添加到 middle_frame 中
        image=button_1A_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: toggle_button(button_1A, "use_experience_point",
                                      config.getboolean("AutoDaily", "use_experience_point"),
                                      relative_to_assets("button_1.png"), section="AutoDaily"),
        relief="flat"
    )
    button_1A.grid(row=1, column=20, padx=10, pady=10)  # 使用 grid 布局

    button_images["use_experience_point"] = button_1A_image


def quit_genshin_settings():
    clear_middle_section()

    Label(middle_frame, text="Key").grid(row=0, column=0, sticky='w')
    key_entry = Entry(middle_frame, width=40)
    key_entry.grid(row=1, column=0)
    key_entry.insert(0, config.get("Quit", "key"))

    def save_settings(event=None):
        config.set("Quit", "key", key_entry.get())
        with open(config_file_path, "w") as configfile:
            config.write(configfile)
        append_to_console("已自动保存")  # 添加调试信息

    Label(middle_frame, text="     可以输入SeverchanKey的值", bg='white', font=("", 12)).grid(row=9, column=0,
                                                                                              sticky='w')

    key_entry.bind("<KeyRelease>", save_settings)

def taskkill():
    result = subprocess.run(['taskkill', '-f', '-im', 'PaddleOCR-json.exe'], capture_output=True, text=True)
    output = result.stdout
    error = result.stderr

    # 打印输出和错误
    append_to_console(output)
    append_to_console(error)
# ######################################################################################################################
# ######################################################################################################################


# 绘制带30%黑色边框的矩形
def create_rectangle_with_border(x0, y0, x1, y1, fill, outline, border_ratio=0.004):
    border_color = '#D3D3D3'
    border_width = int((x1 - x0) * border_ratio)
    canvas.create_rectangle(x0, y0, x1, y1, fill=border_color, outline="")
    canvas.create_rectangle(x0 + border_width, y0 + border_width, x1 - border_width, y1 - border_width, fill=fill,
                            outline="")


create_rectangle_with_border(656.0, 116.0, 985.0, 738.0, fill="#FFFFFF", outline="#000000")
create_rectangle_with_border(12.0, 116.0, 300.0, 738.0, fill="#FFFFFF", outline="#000000")
create_rectangle_with_border(319.0, 116.0, 643.0, 738.0, fill="#FFFFFF", outline="#000000")

# 调整上方线的粗细
canvas.create_line(84.0, 38.58296270991468, 1015.5, 38.58296270991468, fill="#D3D3D3", width=1)

canvas.create_text(
    70.0,
    164.0,
    anchor="nw",
    text="启动原神",
    fill="#000000",
    font=("Impact", 16 * -1)
)

canvas.create_text(
    69.0,
    207.0,
    anchor="nw",
    text="检查进度",
    fill="#000000",
    font=("IndieFlower Regular", 16 * -1)
)

canvas.create_text(
    69.0,
    250.0,
    anchor="nw",
    text="自动秘境",
    fill="#000000",
    font=("IndieFlower Regular", 16 * -1)
)

canvas.create_text(
    69.0,
    298.0,
    anchor="nw",
    text="每日委托",
    fill="#000000",
    font=("IndieFlower Regular", 16 * -1)
)

canvas.create_text(
    70.0,
    338.0,
    anchor="nw",
    text="领取奖励",
    fill="#000000",
    font=("IndieFlower Regular", 16 * -1)
)

canvas.create_text(
    70.0,
    382.0,
    anchor="nw",
    text="退出原神",
    fill="#000000",
    font=("IndieFlower Regular", 16 * -1)
)

canvas.create_text(
    100.0,
    120.0,
    anchor="nw",
    text="任    务",
    fill="#000000",
    font=("IndieFlower Regular", 20 * -1)
)

# 创建按钮并设置初始图片

button_1_image = PhotoImage(
    file=checked_image_path if config.getboolean("Run", "startgenshin") else relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_1_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: toggle_button(button_1, "startgenshin", config.getboolean("Run", "startgenshin"),
                                  relative_to_assets("button_1.png")),
    relief="flat"
)
button_1.place(x=155.0, y=165.0, width=15.0, height=15.0)
button_images["startgenshin"] = button_1_image

button_2_image = PhotoImage(
    file=checked_image_path if config.getboolean("Run", "check_schedule") else relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_2_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: toggle_button(button_2, "check_schedule", config.getboolean("Run", "check_schedule"),
                                  relative_to_assets("button_2.png")),
    relief="flat"
)
button_2.place(x=155.0, y=207.0, width=15.0, height=15.0)
button_images["check_schedule"] = button_2_image

button_3_image = PhotoImage(
    file=checked_image_path if config.getboolean("Run", "run_enigma") else relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_3_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: toggle_button(button_3, "run_enigma", config.getboolean("Run", "run_enigma"),
                                  relative_to_assets("button_3.png")),
    relief="flat"
)
button_3.place(x=155.0, y=251.0, width=15.0, height=15.0)
button_images["run_enigma"] = button_3_image

button_4_image = PhotoImage(
    file=checked_image_path if config.getboolean("Run", "run_daily_mission") else relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_4_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: toggle_button(button_4, "run_daily_mission", config.getboolean("Run", "run_daily_mission"),
                                  relative_to_assets("button_4.png")),
    relief="flat"
)
button_4.place(x=155.0, y=301.0, width=15.0, height=15.0)
button_images["run_daily_mission"] = button_4_image

button_5_image = PhotoImage(
    file=checked_image_path if config.getboolean("Run", "get_reward") else relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_5_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: toggle_button(button_5, "get_reward", config.getboolean("Run", "get_reward"),
                                  relative_to_assets("button_5.png")),
    relief="flat"
)
button_5.place(x=155.0, y=341.0, width=15.0, height=15.0)
button_images["get_reward"] = button_5_image

button_6_image = PhotoImage(
    file=checked_image_path if config.getboolean("Run", "quit_genshin") else relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_6_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: toggle_button(button_6, "quit_genshin", config.getboolean("Run", "quit_genshin"),
                                  relative_to_assets("button_6.png")),
    relief="flat"
)
button_6.place(x=155.0, y=385.0, width=15.0, height=15.0)
button_images["quit_genshin"] = button_6_image

button_image_7 = PhotoImage(file=relative_to_assets("button_7.png"))
button_7 = Button(
    image=button_image_7,
    borderwidth=0,
    highlightthickness=0,
    command=lambda:main_run(),
    relief="flat"
)
button_7.place(x=91.0, y=672.0, width=133.0, height=46.0)

button_image_8 = PhotoImage(file=relative_to_assets("button_8.png"))
button_8 = Button(
    image=button_image_8,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: start_genshin_settings(),
    relief="flat"
)
button_8.place(x=224.0, y=162.0, width=25.0, height=25.0)

button_image_9 = PhotoImage(file=relative_to_assets("button_9.png"))
button_9 = Button(
    image=button_image_9,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: check_schedule_settings(),
    relief="flat"
)
button_9.place(x=224.0, y=205.0, width=25.0, height=25.0)

button_image_10 = PhotoImage(file=relative_to_assets("button_10.png"))
button_10 = Button(
    image=button_image_10,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: enigma_settings(),
    relief="flat"
)
button_10.place(x=224.0, y=246.0, width=25.0, height=25.0)

image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(42.0, 216.0, image=image_image_1)

canvas.create_text(
    764.0,
    130.0,
    anchor="nw",
    text="控制台输出",
    fill="#1158E4",
    font=("IndieFlower Regular", 16 * -1)
)

canvas.create_text(
    79.0,
    20.0,
    anchor="nw",
    text="SGIA:早柚原神自动化   V0.1.2  GUI V0.1.2                                                 我的GUI学的MAA",
    fill="#000000",
    font=("Inter", 16 * -1)
)

button_image_11 = PhotoImage(file=relative_to_assets("button_11.png"))
button_11 = Button(
    image=button_image_11,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: daily_mission_settings(),
    relief="flat"
)
button_11.place(x=224.0, y=296.0, width=25.0, height=25.0)

button_image_12 = PhotoImage(file=relative_to_assets("button_12.png"))
button_12 = Button(
    image=button_image_12,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: get_reward_settings(),
    relief="flat"
)
button_12.place(x=224.0, y=335.0, width=25.0, height=25.0)

button_image_13 = PhotoImage(file=relative_to_assets("button_13.png"))
button_13 = Button(
    image=button_image_13,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: quit_genshin_settings(),
    relief="flat"
)
button_13.place(x=224.0, y=380.0, width=25.0, height=25.0)

button_image_14 = PhotoImage(file=relative_to_assets("button_14.png"))
button_14 = Button(
    image=button_image_14,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: taskkill(),
    relief="flat"
)
button_14.place(x=84.0, y=500.0, width=110.0, height=25.0)

canvas.create_text(
    10.0,
    540.0,
    anchor="nw",
    text="如果你尝试使用alt+F4或者使用关\n闭按钮退出主程序，请按下这个按钮\n释放OCR进程\n这东西可很占CPU的...",
    fill="#000000",
    font=("IndieFlower Regular", 18 * -1)
)
# 创建一个 Text 小部件用于显示控制台输出
console_output = Text(window, bg="#FFFFFF", fg="#000000", font=("IndieFlower Regular", 14 * -1))
console_output.place(x=656, y=164, width=329, height=574)


def append_to_console(text):
    console_output.insert(END, text + "\n")
    console_output.see(END)


class ConsoleRedirect:
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.insert(END, text)
        self.widget.see(END)

    def flush(self):
        pass

class ConsoleHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        append_to_console(log_entry)

# 重定向 stdout 到 Text 小部件
sys.stdout = ConsoleRedirect(console_output)

# 设置日志记录器
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
console_handler = ConsoleHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

window.resizable(False, False)

window.mainloop()
