import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
import threading
import time
from tiktokapi import TikTokApi, exceptions

# 全局变量，存储监测结果
monitor_result = []


class TikTokMonitorApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("TikTok 监控器")
        self.geometry("600x400")
        self.resizable(width=False, height=False)

        # 初始化控件
        self.usernames_label = tk.Label(self, text="输入用户名（多个用户名用英文逗号分隔）：")
        self.usernames_entry = tk.Entry(self)
        self.check_btn = tk.Button(self, text="开始监控", command=self.start_monitor)
        self.stop_btn = tk.Button(self, text="停止监控", command=self.stop_monitor, state="disabled")
        self.interval_label = tk.Label(self, text="监测间隔（秒）：")
        self.interval_entry = tk.Entry(self)
        self.filter_label = tk.Label(self, text="监测结果过滤：")
        self.filter_entry = tk.Entry(self)
        self.result_label = tk.Label(self, text="监测结果：")
        self.result_text = tk.Text(self, state="disabled")
        self.export_btn = tk.Button(self, text="导出结果", command=self.export_result, state="disabled")

        # 设置控件位置和大小
        self.usernames_label.place(x=10, y=10)
        self.usernames_entry.place(x=10, y=30, width=200)
        self.check_btn.place(x=220, y=30)
        self.stop_btn.place(x=300, y=30)
        self.interval_label.place(x=10, y=70)
        self.interval_entry.place(x=10, y=90, width=50)
        self.filter_label.place(x=80, y=70)
        self.filter_entry.place(x=80, y=90, width=200)
        self.result_label.place(x=10, y=130)
        self.result_text.place(x=10, y=150, width=580, height=200)
        self.export_btn.place(x=10, y=360)

        # 初始化定时器
        self.timer = None

        # 绑定关闭事件
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        # 如果正在监测，则停止监测并提示用户
        if self.timer:
            messagebox.showwarning("警告", "正在监测，请先停止监测再退出程序。")
        else:
            self.destroy()

    def start_monitor(self):
        # 检查用户是否输入了有效的用户名和监测间隔
        usernames = self.usernames_entry.get().split(",")
        if not usernames:
            messagebox.showerror("错误", "请输入至少一个用户名。")
            return
        try:
            interval = int(self.interval_entry.get())
        except ValueError:
            messagebox.showerror("错误", "监测间隔必须是一个整数。")
            return
        if interval <= 0:
            messagebox.showerror("错误", "监测间隔必须大于零。")
            return

        # 开始监测
        self.check_btn.config(state="disabled")

        try:
            # 执行监测操作的代码
            ...
        except TikTokApi.exceptions.TikTokNotFoundError:
            # 当用户不存在时
            messagebox.showerror("错误", "该用户不存在！")
            logging.error("用户不存在")
        except TikTokApi.exceptions.TikTokApiError as e:
            # 当出现其他错误时
            messagebox.showerror("错误", f"出现错误：{str(e)}")
            logging.error(str(e))

        def check_username(username):
            """
            检查用户名是否有效
            """
            # 根据需要进行用户名格式验证
            if not username:
                return False
            return True

def set_interval(seconds):
    """
    设置监测的时间间隔
    """
    global interval_timer
    interval_timer = threading.Timer(seconds, check_tiktok)
    interval_timer.start()

def save_result(username, video_url):
    """
    将监测结果存储到文件或数据库中
    """
    # 根据需要选择存储方式
    with open('result.txt', 'a') as f:
        f.write(f"{username}: {video_url}\n")

        def filter_result(results, filter_usernames=None, latest_only=False):
            """
            过滤监测结果
            """
            if filter_usernames:
                results = [r for r in results if r[0] in filter_usernames]
            if latest_only:
                # 过滤出最新的视频
                latest_results = []
                for username, video_url in results:
                    if not latest_results:
                        latest_results.append((username, video_url))
                    else:
                        for i, (u, v) in enumerate(latest_results):
                            if username == u:
                                if i == len(latest_results) - 1:
                                    latest_results.append((username, video_url))
                                else:
                                    latest_results[i] = (username, video_url)
                            else:
                                latest_results.append((username, video_url))
                results = latest_results
            return results

        # 创建菜单
        menu_bar = tk.Menu(root)
        root.config(menu=menu_bar)

        # 创建“设置”菜单
        settings_menu = tk.Menu(menu_bar, tearoff=0)
        settings_menu.add_command(label="设置时间间隔", command=set_interval_popup)
        settings_menu.add_command(label="过滤监测结果", command=filter_popup)
        menu_bar.add_cascade(label="设置", menu=settings_menu)

        # 创建“监测”菜单
        monitor_menu = tk.Menu(menu_bar, tearoff=0)
        monitor_menu.add_command(label="启动监测", command=start_monitoring)
        monitor_menu.add_command(label="停止监测", command=stop_monitoring)
        menu_bar.add_cascade(label="监测", menu=monitor_menu)
