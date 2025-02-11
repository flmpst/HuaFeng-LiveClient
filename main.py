from frontend import MainWindow
from backend import MainProcessor
import asyncio

if __name__ == "__main__":
    app = MainWindow()
    app.root.mainloop()

    # mp = MainProcessor("https://live.dfggmc.top/", "6b893dd8ad3b0fcafdae29654c8f60e92d421d314fd30b9d615af85bfacb503c")
    # asyncio.run(mp.ziSha())