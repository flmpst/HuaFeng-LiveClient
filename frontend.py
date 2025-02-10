import tkinter as tk
from PIL import Image, ImageTk
from ffpyplayer.player import MediaPlayer
import asyncio
import threading

# 定义视频播放器类
class VideoPlayTk:
    # 初始化函数
    def __init__(self, videoSource):
        self.root = tk.Tk()
        self.root.title('视频播放器')  # 设置窗口标题

        # 创建一个画布用于显示视频帧
        self.canvas = tk.Canvas(self.root, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # 创建暂停/播放按钮
        self.pause_button = tk.Button(self.root, text='暂停/继续', command=self.toggle_pause)
        self.pause_button.pack(side=tk.LEFT)

        # 初始化播放器和播放状态标志
        self.player = None
        self.is_paused = False
        self.is_stopped = False

        # 开始播放视频
        self.start_video(videoSource)

    # 开始播放视频的函数
    def start_video(self, file_path):
        self.player = MediaPlayer(file_path)  # 创建一个MediaPlayer对象
        self.loop = asyncio.get_event_loop()
        threading.Thread(target=self.loop.run_forever).start()
        asyncio.run_coroutine_threadsafe(self.play_video(), self.loop)

    # 播放视频的异步函数
    async def play_video(self):
        while not self.is_stopped:
            if self.is_paused:
                await asyncio.sleep(0.1)
                continue

            frame, val = self.player.get_frame()  # 获取下一帧和帧间隔
            if val == 'eof':
                self.player = None  # 如果到达视频末尾，则释放播放器资源
                break
            elif frame is None:
                await asyncio.sleep(0.01)  # 如果没有帧，则稍后再试
                continue

            # 将帧图像转换为Tkinter PhotoImage并显示在画布上
            image, pts = frame
            image = Image.frombytes("RGB", image.get_size(), bytes(image.to_bytearray()[0]))

            # 获取窗口大小并等比例缩放图像
            window_width = self.canvas.winfo_width()
            window_height = self.canvas.winfo_height()
            image.thumbnail((window_width, window_height))

            photo = ImageTk.PhotoImage(image=image)
            self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
            self.canvas.image = photo  # 保持对PhotoImage的引用，防止被垃圾回收

            await asyncio.sleep(val)  # 等待下一帧的时间间隔

    # 切换暂停状态的函数
    def toggle_pause(self):
        if self.player:
            self.is_paused = not self.is_paused  # 切换暂停状态
            self.player.set_pause(self.is_paused)  # 设置播放器的暂停状态

