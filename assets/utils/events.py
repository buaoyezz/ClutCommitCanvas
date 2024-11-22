from PyQt5.QtCore import QObject, pyqtSignal

class EventBus(QObject):
    switch_page = pyqtSignal(str)  # 发送页面切换信号
    
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = EventBus()
        return cls._instance 