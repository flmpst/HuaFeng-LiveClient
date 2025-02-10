import tkinter
import vlc
import utils

class VideoPlayer(object):
    def __init__(self,anchor: str,sourceURL: str):

        self.sourceURL = sourceURL

        # Initialize player window
        self.playerWindow = tkinter.Tk()
        self.playerWindowCanvas = tkinter.Canvas(self.playerWindowCanvas)

        # Initialize vlc instance
        self.instance: vlc.Instance = vlc.Instance('--no-drop-late-frames --no-skip-frames --rtsp-tcp')
        self.player: vlc.Instance = self.instance.media_player_new()

        # Configure player window
        self.playerWindow.title = f"{anchor}的直播"
        width, height = utils.getVideoSize(sourceURL)
        self.playerWindowCanvas.config(width=int(width), height=int(height))
        self.playerWindow.geometry(f"{int(width)+10}x{int(height)+10}")

        # Place elements
        self.playerWindowCanvas.pack()

        # Output video stream to canvas
        if hasattr(self.player, 'video_output'):
            self.player.set_hwnd(self.canvas.winfo_id())
        else:
            self.player.set_xwindow(self.canvas.winfo_id())