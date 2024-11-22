from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QProgressBar, QScrollArea)
from PyQt5.QtCore import Qt
from assets.utils.clut_card import ClutCard
from datetime import datetime

class ProcessCard(ClutCard):
    def __init__(self, title, repo_url):
        super().__init__(title=title, msg=f"仓库: {repo_url}")
        self.repo_url = repo_url
        self.content_layout = self.layout()
        self.setup_process_ui()
        self.setMinimumHeight(180)
        self.setMaximumHeight(290)
        
    def setup_process_ui(self):
        """设置进程卡片的特殊UI"""
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(20, 10, 20, 20)
        layout.setSpacing(12)
        
        # 状态和速度信息
        info_layout = QHBoxLayout()
        info_layout.setContentsMargins(0, 0, 0, 0)
        
        self.status_label = QLabel("准备中...")
        self.status_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 13px;
                font-weight: 500;
            }
        """)
        self.speed_label = QLabel("速度: 0 KB/s")
        self.speed_label.setStyleSheet("""
            QLabel {
                color: rgba(255,255,255,0.7);
                font-size: 12px;
            }
        """)
        
        # 开始时间
        self.start_time = datetime.now()
        time_label = QLabel(f"开始时间: {self.start_time.strftime('%H:%M:%S')}")
        time_label.setStyleSheet("""
            QLabel {
                color: rgba(255,255,255,0.5);
                font-size: 12px;
            }
        """)
        
        info_layout.addWidget(self.status_label)
        info_layout.addStretch()
        info_layout.addWidget(self.speed_label)
        info_layout.addWidget(time_label)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background: rgba(255, 255, 255, 0.1);
                border: none;
                border-radius: 4px;
                height: 8px;
                text-align: center;
                margin: 8px 0;
            }
            QProgressBar::chunk {
                background: #4A9EFF;
                border-radius: 4px;
            }
        """)
        self.progress_bar.setTextVisible(False)
        
        # URL显示区域
        url_container = QWidget()
        url_container.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 6px;
                padding: 2px;
            }
        """)
        url_layout = QVBoxLayout(url_container)
        url_layout.setContentsMargins(12, 8, 12, 8)
        
        url_label = QLabel(self.repo_url)
        url_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.6);
                font-size: 12px;
                line-height: 1.4;
            }
        """)
        url_label.setWordWrap(True)
        url_label.setMaximumWidth(600)
        
        url_layout.addWidget(url_label)
        
        # 添加所有组件到主布局
        layout.addLayout(info_layout)
        layout.addWidget(self.progress_bar)
        layout.addWidget(url_container)
        layout.addStretch(1)
        
        # 添加到卡片内容区域
        self.content_layout.addWidget(content)
        
    def set_status(self, text):
        """更新状态文本"""
        self.status_label.setText(text)
        
    def update_progress(self, value, total, speed):
        """更新进度和速度"""
        percentage = int(value / total * 100) if total else 0
        self.progress_bar.setValue(value)
        self.progress_bar.setMaximum(total if total else 100)
        
        # 更新速度显示
        if speed < 1024:
            speed_text = f"{speed} B/s"
        elif speed < 1024 * 1024:
            speed_text = f"{speed/1024:.1f} KB/s"
        else:
            speed_text = f"{speed/1024/1024:.1f} MB/s"
            
        self.speed_label.setText(f"速度: {speed_text}")

class ProcessPage(QWidget):
    _instance = None
    
    @classmethod
    def get_instance(cls):
        """获取单例实例"""
        if cls._instance is None:
            cls._instance = ProcessPage()
        return cls._instance
        
    def __init__(self):
        if ProcessPage._instance is not None:
            raise Exception("ProcessPage 是单例类，请使用 get_instance() 方法获取实例")
        super().__init__()
        self.tasks = {}  # 存储所有任务
        self.setup_ui()
        ProcessPage._instance = self
        
    def setup_ui(self):
        # 主布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # 标题区域
        title_widget = QWidget()
        title_layout = QVBoxLayout(title_widget)
        title_layout.setContentsMargins(0, 0, 0, 10)
        title_layout.setSpacing(5)
        
        title = QLabel("| 进程管理")
        title.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: bold;
        """)
        subtitle = QLabel("Process Management")
        subtitle.setStyleSheet("color: rgba(255,255,255,0.5); font-size: 14px;")
        
        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        
        # 创建一个包含滚动区域的容器
        scroll_container = QWidget()
        scroll_container_layout = QVBoxLayout(scroll_container)
        scroll_container_layout.setContentsMargins(0, 0, 0, 0)
        scroll_container_layout.setSpacing(0)
        
        # 任务列表区域
        self.task_container = QWidget()
        self.task_layout = QVBoxLayout(self.task_container)
        self.task_layout.setContentsMargins(0, 0, 0, 0)
        self.task_layout.setSpacing(10)
        self.task_layout.addStretch()  # 添加弹性空间，使卡片从顶部开始
        
        # 滚动区域
        scroll = QScrollArea()
        scroll.setWidget(self.task_container)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 禁用水平滚动条
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)    # 需要时显示垂直滚动条
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: rgba(255, 255, 255, 0.1);
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 0.2);
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        scroll_container_layout.addWidget(scroll)
        
        # 添加所有组件到主布局
        layout.addWidget(title_widget)
        layout.addWidget(scroll_container, 1)  # 添加权重，使滚动区域占据剩余空间
        
        # 设置滚动区域的大小策略
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # 设置任务容器的最小高度
        self.task_container.setMinimumHeight(300)
        
    def add_task(self, repo_url, thread):
        """添加新任务"""
        # 移除之前的弹性空间
        for i in reversed(range(self.task_layout.count())):
            item = self.task_layout.itemAt(i)
            if item.widget() is None:  # 是弹性空间
                self.task_layout.removeItem(item)
        
        # 添加新任务卡片
        task_card = ProcessCard(f"克隆任务 - {repo_url.split('/')[-1]}", repo_url)
        self.task_layout.addWidget(task_card)
        self.tasks[thread] = task_card
        
        # 重新添加弹性空间
        self.task_layout.addStretch()
        
        # 连接信号
        thread.progress.connect(lambda msg: self._update_task(thread, msg))
        thread.finished.connect(lambda success, msg: self._on_task_finished(thread, success, msg))
        
    def _update_task(self, thread, message):
        """更新任务状态"""
        if thread in self.tasks:
            self.tasks[thread].set_status(message)
            
    def _on_task_finished(self, thread, success, message):
        """处理任务完成"""
        if thread in self.tasks:
            card = self.tasks[thread]
            if success:
                card.set_status("完成")
                card.setStyleSheet("""
                    QProgressBar::chunk {
                        background: #4CAF50;
                    }
                """)
            else:
                card.set_status(f"失败: {message}")
                card.setStyleSheet("""
                    QProgressBar::chunk {
                        background: #FF4A4A;
                    }
                """)