import tkinter as tk
from PIL import Image, ImageTk
from ffpyplayer.player import MediaPlayer
import asyncio
import threading
from tkinter import *
from tkinter.ttk import *
from backend import MainProcessor

# 定义视频播放器类
class VideoPlay:
    # 初始化函数
    def __init__(self, videoSource: str, anchor: str) -> None:
        self.root: tk.Tk = tk.Tk()
        self.root.title(f'{anchor}的直播')  # 设置窗口标题

        # 创建一个画布用于显示视频帧
        self.canvas: tk.Canvas = tk.Canvas(self.root, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # 创建暂停/播放按钮
        self.pause_button: tk.Button = tk.Button(self.root, text='开始/暂停', command=self.toggle_pause)
        self.pause_button.pack(side=tk.LEFT)

        # 初始化播放器和播放状态标志
        self.player: MediaPlayer = None
        self.is_paused: bool = False
        self.is_stopped: bool = False

        # 开始播放视频
        self.start_video(videoSource)

    # 开始播放视频的函数
    def start_video(self, file_path: str) -> None:
        self.player = MediaPlayer(file_path)  # 创建一个MediaPlayer对象
        self.loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
        threading.Thread(target=self.loop.run_forever).start()
        asyncio.run_coroutine_threadsafe(self.play_video(), self.loop)

    # 异步播放视频的函数
    async def play_video(self) -> None:
        while not self.is_stopped:
            if self.is_paused:
                await asyncio.sleep(0.1)
                continue

            frame, val = self.player.get_frame()  # 获取下一帧和帧间隔
            if val == 'eof':
                self.player = None  # 如果视频结束，释放播放器资源
                break
            elif frame is None:
                await asyncio.sleep(0.01)  # 如果没有帧，重试
                continue

            # 将帧图像转换为Tkinter PhotoImage并显示在画布上
            image, pts = frame
            image = Image.frombytes("RGB", image.get_size(), bytes(image.to_bytearray()[0]))

            # 获取窗口大小并按比例缩放图像
            window_width: int = self.canvas.winfo_width()
            window_height: int = self.canvas.winfo_height()
            image.thumbnail((window_width, window_height))

            photo: ImageTk.PhotoImage = ImageTk.PhotoImage(image=image)
            self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
            self.canvas.image = photo  # 保持对PhotoImage的引用以防止垃圾回收

            await asyncio.sleep(val)  # 等待下一个帧间隔

    # 切换暂停状态的函数
    def toggle_pause(self) -> None:
        if self.player:
            self.is_paused = not self.is_paused  # 切换暂停状态
            self.player.set_pause(self.is_paused)  # 设置播放器暂停状态


class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        self.__win()
        self.tk_label_frame_m70090d2 = self.__tk_label_frame_m70090d2(self)
        self.tk_list_box_m7009mg6 = self.__tk_list_box_m7009mg6(self.tk_label_frame_m70090d2) 
        self.tk_frame_m700adhb = self.__tk_frame_m700adhb(self)
        self.tk_canvas_m700csgf = self.__tk_canvas_m700csgf(self.tk_frame_m700adhb) 
        self.tk_button_m700bxy8 = self.__tk_button_m700bxy8(self)
        self.tk_label_frame_m700yzw9 = self.__tk_label_frame_m700yzw9(self)
        self.tk_list_box_m700arav = self.__tk_list_box_m700arav(self.tk_label_frame_m700yzw9) 

    def __win(self):
        self.title("花枫Live")
        # 设置窗口大小、居中
        width = 550
        height = 320
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)
        
        self.minsize(width=width, height=height)
        
    def scrollbar_autohide(self, vbar, hbar, widget):
        """自动隐藏滚动条"""
        def show():
            if vbar: vbar.lift(widget)
            if hbar: hbar.lift(widget)
        def hide():
            if vbar: vbar.lower(widget)
            if hbar: hbar.lower(widget)
        hide()
        widget.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Leave>", lambda e: hide())
        if hbar: hbar.bind("<Enter>", lambda e: show())
        if hbar: hbar.bind("<Leave>", lambda e: hide())
        widget.bind("<Leave>", lambda e: hide())
    
    def v_scrollbar(self, vbar, widget, x, y, w, h, pw, ph):
        widget.configure(yscrollcommand=vbar.set)
        vbar.config(command=widget.yview)
        vbar.place(relx=(w + x) / pw, rely=y / ph, relheight=h / ph, anchor='ne')
    def h_scrollbar(self, hbar, widget, x, y, w, h, pw, ph):
        widget.configure(xscrollcommand=hbar.set)
        hbar.config(command=widget.xview)
        hbar.place(relx=x / pw, rely=(y + h) / ph, relwidth=w / pw, anchor='sw')
    def create_bar(self, master, widget, is_vbar, is_hbar, x, y, w, h, pw, ph):
        vbar, hbar = None, None
        if is_vbar:
            vbar = Scrollbar(master)
            self.v_scrollbar(vbar, widget, x, y, w, h, pw, ph)
        if is_hbar:
            hbar = Scrollbar(master, orient="horizontal")
            self.h_scrollbar(hbar, widget, x, y, w, h, pw, ph)
        self.scrollbar_autohide(vbar, hbar, widget)
    def __tk_label_frame_m70090d2(self, parent):
        frame = LabelFrame(parent, text="直播列表",)
        frame.place(relx=0.0333, rely=0.0411, relwidth=0.3660, relheight=0.8418)
        return frame
    def __tk_list_box_m7009mg6(self, parent):
        lb = Listbox(parent)
        
        lb.insert(END, "列表框")
        
        lb.insert(END, "Python")
        
        lb.insert(END, "Tkinter Helper")
        
        lb.place(relx=0.0000, rely=0.0000, relwidth=1.0000, relheight=1.0000)
        return lb
    def __tk_frame_m700adhb(self, parent):
        frame = Frame(parent,)
        frame.place(relx=0.4436, rely=0.0633, relwidth=0.3678, relheight=0.5063)
        return frame
    def __tk_canvas_m700csgf(self, parent):
        canvas = Canvas(parent, bg="#aaa")
        canvas.place(relx=0.0000, rely=0.0000, relwidth=1.0000, relheight=1.0000)
        return canvas
    def __tk_button_m700bxy8(self, parent):
        btn = Button(parent, text="进去", takefocus=False,)
        btn.place(relx=0.8503, rely=0.0633, relwidth=0.1054, relheight=0.1139)
        return btn
    def __tk_label_frame_m700yzw9(self, parent):
        frame = LabelFrame(parent, text="直播间信息",)
        frame.place(relx=0.4436, rely=0.5728, relwidth=0.3660, relheight=0.3133)
        return frame
    def __tk_list_box_m700arav(self, parent):
        lb = Listbox(parent)
        
        lb.insert(END, "直播间名")
        
        lb.insert(END, "主播")
        
        lb.insert(END, "直播间人数")
        
        lb.place(relx=0.0000, rely=0.0000, relwidth=1.0000, relheight=1.0000)
        return lb
    
class AskWindow(Tk):
    def __init__(self, screenName = None, baseName = None, className = "Tk", useTk = True, sync = False, use = None):
        super().__init__(screenName, baseName, className, useTk, sync, use)

        self.geometry("400x150")
        self.title(" ")

        self.labelr8fs = Label(self, text="输入直播服务器地址")
        self.label3d3a = Label(self, text="例如: https://live.dfggmc.top/")
        self.textf3d0c = Text(self, width=40, height=1)
        self.label8hsc = Label(self, text="输入用户 Token（未输入将无法发送弹幕、创建直播间等）")
        self.textdje2v = Text(self, width=40, height=1)
        self.buttonf94 = Button(self, text="提交", command=self.getUserInput)

        self.elements = [self.labelr8fs, self.label3d3a, self.textf3d0c, self.label8hsc, self.textdje2v, self.buttonf94]

        for element in self.elements:
            element.pack()

    def getUserInput(self):
        self.base_url = self.textf3d0c.get(1.0, END).rstrip("\n")
        self.token = self.textdje2v.get(1.0, END).rstrip("\n")

        print(self.base_url)
        print(self.token)

aw = AskWindow()
aw.mainloop()