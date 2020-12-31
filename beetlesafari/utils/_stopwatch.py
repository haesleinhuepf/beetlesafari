
def stopwatch(text : str = None):
    import time

    if text is not None:
        print("-------------------------> " + text + " took " + str(int((time.time() - stopwatch.timestamp) * 1000)) + "ms")

    stopwatch.timestamp = time.time()

stopwatch.timestamp = 0