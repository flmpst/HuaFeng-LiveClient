import av

def getVideoSize(videoSourceURL: str) -> tuple:
    try:
        container = av.open(videoSourceURL)
        for stream in container.streams.video:
            returnContent = (stream.width, stream.height)
    except:
        returnContent = False

    return returnContent