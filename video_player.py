import tkinter as tk
import vlc

class VideoPlayer:
    def __init__(self, root, video_url):
        self.root = root
        self.video_url = video_url
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.media = self.instance.media_new(video_url)
        self.player.set_media(self.media)

        self.create_ui()

    def create_ui(self):
        self.root.title("Video Player")
        self.root.geometry("800x600")
        self.video_panel = tk.Frame(self.root)
        self.video_panel.pack(fill=tk.BOTH, expand=1)
        self.player.set_hwnd(self.video_panel.winfo_id())

        self.play_button = tk.Button(self.root, text="Play", command=self.play_video)
        self.play_button.pack(side=tk.LEFT)

        self.pause_button = tk.Button(self.root, text="Pause", command=self.pause_video)
        self.pause_button.pack(side=tk.LEFT)

        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_video)
        self.stop_button.pack(side=tk.LEFT)

    def play_video(self):
        self.player.play()

    def pause_video(self):
        self.player.pause()

    def stop_video(self):
        self.player.stop()

if __name__ == "__main__":
    root = tk.Tk()
    video_url = "http://example.com/video.m3u8"  # 替换为实际的视频 URL
    player = VideoPlayer(root, video_url)
    root.mainloop()
