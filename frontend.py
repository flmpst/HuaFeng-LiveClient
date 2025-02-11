import tkinter as tk
from PIL import Image, ImageTk
from ffpyplayer.player import MediaPlayer
import asyncio
import threading
from backend import MainProcessor

# Define video player class
class VideoPlay:
    # Initialization function
    def __init__(self, videoSource: str, anchor: str) -> None:
        self.root: tk.Tk = tk.Tk()
        self.root.title(f'{anchor}的直播')  # Set window title

        # Create a canvas for displaying video frames
        self.canvas: tk.Canvas = tk.Canvas(self.root, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Create pause/play button
        self.pause_button: tk.Button = tk.Button(self.root, text='开始/暂停', command=self.toggle_pause)
        self.pause_button.pack(side=tk.LEFT)

        # Initialize player and playback state flags
        self.player: MediaPlayer = None
        self.is_paused: bool = False
        self.is_stopped: bool = False

        # Start playing video
        self.start_video(videoSource)

    # Function to start playing video
    def start_video(self, file_path: str) -> None:
        self.player = MediaPlayer(file_path)  # Create a MediaPlayer object
        self.loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
        threading.Thread(target=self.loop.run_forever).start()
        asyncio.run_coroutine_threadsafe(self.play_video(), self.loop)

    # Asynchronous function to play video
    async def play_video(self) -> None:
        while not self.is_stopped:
            if self.is_paused:
                await asyncio.sleep(0.1)
                continue

            frame, val = self.player.get_frame()  # Get next frame and frame interval
            if val == 'eof':
                self.player = None  # Release player resources if end of video
                break
            elif frame is None:
                await asyncio.sleep(0.01)  # Retry if no frame
                continue

            # Convert frame image to Tkinter PhotoImage and display on canvas
            image, pts = frame
            image = Image.frombytes("RGB", image.get_size(), bytes(image.to_bytearray()[0]))

            # Get window size and scale image proportionally
            window_width: int = self.canvas.winfo_width()
            window_height: int = self.canvas.winfo_height()
            image.thumbnail((window_width, window_height))

            photo: ImageTk.PhotoImage = ImageTk.PhotoImage(image=image)
            self.canvas.create_image(0, 0, image=photo, anchor=tk.NW)
            self.canvas.image = photo  # Keep reference to PhotoImage to prevent garbage collection

            await asyncio.sleep(val)  # Wait for next frame interval

    # Function to toggle pause state
    def toggle_pause(self) -> None:
        if self.player:
            self.is_paused = not self.is_paused  # Toggle pause state
            self.player.set_pause(self.is_paused)  # Set player pause state

class MainWindow(object):
    def __init__(self, baseURL: str) -> None:
        self.root = tk.Tk()
        self.root.title("直播列表")

        # Initialize MainProcessor
        self.processor = MainProcessor(baseURL)

        # Create frames for layout
        self.left_frame = tk.Frame(self.root)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.right_frame = tk.Frame(self.root)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Create listbox for live list
        self.live_listbox = tk.Listbox(self.left_frame)
        self.live_listbox.pack(fill=tk.Y, expand=True)
        self.live_listbox.bind('<<ListboxSelect>>', self.show_live_details)

        # Create text widget for live details
        self.live_details = tk.Text(self.right_frame)
        self.live_details.pack(fill=tk.BOTH, expand=True)

        # Load live list
        self.load_live_list()

    def load_live_list(self) -> None:
        live_list = self.processor.getLiveList()
        if live_list:
            for live in live_list:
                self.live_listbox.insert(tk.END, live["name"])

    def show_live_details(self, event) -> None:
        selected_index = self.live_listbox.curselection()
        if selected_index:
            live_name = self.live_listbox.get(selected_index)
            live_list = self.processor.getLiveList()
            for live in live_list:
                if live["name"] == live_name:
                    details = f"名称: {live['name']}\n"
                    details += f"状态: {live['status']}\n"
                    details += f"作者: {live['authr']}\n"
                    details += f"描述: {live['description']}\n"
                    self.live_details.delete(1.0, tk.END)
                    self.live_details.insert(tk.END, details)
                    break

if __name__ == "__main__":
    baseURL = "https://live.dfggmc.top/api/v1/"  # Replace with your actual base URL
    app = MainWindow(baseURL)
    app.root.mainloop()