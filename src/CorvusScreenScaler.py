from screeninfo import get_monitors

class CorvusScreenScaler:

    monitor = get_monitors()[0]
    width = monitor.width
    height = monitor.height
    nativeWidth = 1920
    nativeHeight = 1080

    @classmethod
    def scaleX(cls, x):
        if(cls.width > cls.nativeWidth):
            return x * (cls.width / cls.nativeWidth)
        else:
            return x * (cls.nativeWidth / cls.width)

    @classmethod
    def scaleY(cls, y):
        if(cls.height > cls.nativeHeight):
            return y * (cls.height / cls.nativeHeight)
        else:
            return y * (cls.nativeHeight / cls.height)
