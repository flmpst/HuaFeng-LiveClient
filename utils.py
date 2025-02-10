import av

def getVideoSize(videoSourceURL: str) -> tuple:
    try:
        container = av.open(videoSourceURL)
        for stream in container.streams.video:
            size = (stream.width, stream.height)
            container.close()
            return size
    except:
        return False