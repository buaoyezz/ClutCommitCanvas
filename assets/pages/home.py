# -*- coding: utf-8 -*-
#=========================
# Home Page 
# ClutCommitCanvas Page 1
# B1
#=========================

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QHBoxLayout, 
                            QFrame, QSpacerItem, QSizePolicy)
from assets.utils.clut_button import ClutLineEdit, ClutButton
from assets.utils.message_box import ClutMessageBox
from assets.utils.clut_card import ClutCard
from assets.utils.clut_image_card import ClutImageCard
from assets.utils.overlay_notification import OverlayNotification
from assets.utils.notification_manager import NotificationManager
import webbrowser

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.notification = NotificationManager()
        self.init_ui()
        
    def init_ui(self):
        # 主布局
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)  # 增加页面边距
        layout.setSpacing(24)  # 增加组件间距
        
        # 欢迎区域
        welcome_container = QFrame()
        welcome_container.setObjectName("welcomeContainer")
        welcome_layout = QVBoxLayout(welcome_container)
        welcome_layout.setContentsMargins(0, 0, 0, 0)
        welcome_layout.setSpacing(8)
        
        welcome_label = QLabel("ClutCommitCanvas")
        welcome_label.setStyleSheet("""
            QLabel {
                font-size: 32px;
                font-weight: bold;
                color: #ffffff;
                background-color: transparent;
            }
        """)
        
        sub_title = QLabel("A Tools For Git Commit")
        sub_title.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: rgba(255, 255, 255, 0.7);
                background-color: transparent;
            }
        """)
        
        welcome_layout.addWidget(welcome_label)
        welcome_layout.addWidget(sub_title)
        layout.addWidget(welcome_container)
        
   
        # 分隔
        layout.addSpacing(32)
        
        # 按钮区域
        actions_container = QFrame()
        actions_container.setObjectName("actionsContainer")
        actions_layout = QHBoxLayout(actions_container)
        actions_layout.setContentsMargins(0, 0, 0, 0)
        actions_layout.setSpacing(16)
        
        # 左
        left_buttons = QHBoxLayout()
        left_buttons.setSpacing(12)
        self.primary_button = ClutButton("关于软件", primary=True)
        self.primary_button.clicked.connect(self.show_about_dialog)
        
        self.secondary_button = ClutButton("Github", primary=False)
        self.secondary_button.clicked.connect(self.open_github)
        
        left_buttons.addWidget(self.primary_button)
        left_buttons.addWidget(self.secondary_button)

        
        # 右
        right_buttons = QHBoxLayout()
        right_buttons.setSpacing(12)
        
        example_button = ClutButton("帮助", primary=False)
        example_button.clicked.connect(self.show_example_message_box)
        
        right_buttons.addWidget(example_button)
        
        # 弹性空间
        actions_layout.addLayout(left_buttons)
        actions_layout.addStretch()
        actions_layout.addLayout(right_buttons)
        
        layout.addWidget(actions_container)
        
        # 卡片区域
        cards_container = QFrame()
        cards_container.setObjectName("cardsContainer")
        cards_layout = QVBoxLayout(cards_container)
        cards_layout.setContentsMargins(0, 0, 0, 0)
        cards_layout.setSpacing(16)
        
        # 卡片
        card = ClutCard(
            title="ClutCommitCanvas", 
            msg="| 即刻开始你的Git提交之旅吧！\n| Version: v1.0.0.10000\n| Author: ZZBuAoYe"
        )
        cards_layout.addWidget(card)
        
        layout.addWidget(cards_container)
        
        # 弹性空间移到最后
        layout.addStretch()
        
        self.setLayout(layout)
        
        self.setStyleSheet("""
            QFrame#welcomeContainer, QFrame#searchContainer, 
            QFrame#actionsContainer, QFrame#cardsContainer {
                background: rgba(255, 255, 255, 0.03);
                border-radius: 12px;
                padding: 24px;
            }
        """)
        
    def on_search(self):
        print("搜索按钮被点击")

    def show_example_message_box(self):
        ClutMessageBox.show_message(
            self,
            title="ClutCommitCanvas", 
            text="ClutCommitCanvas\n\n一个Git提交的图形界面程序，帮助你快速提交Git和拉取Git",
            buttons=["我知道了"]
        )
    
    def show_about_dialog(self):
        ClutMessageBox.show_message(
            self,
            title="关于软件",
            text="ClutCommitCanvas - 一个美观的Git提交工具\n\n版本: v1.0.0.10000\n作者: ZZBuAoYe",
            buttons=["确定"]
        )
        
    def open_github(self):
        result = ClutMessageBox.show_message(
            self,
            title="跳转Github",
            text="即将跳转到ClutCommitCanvas的Github项目页面\n是否继续?",
            buttons=["确定", "取消"]
        )
        
        if result == "确定":
            webbrowser.open("https://github.com/Clutterbox/ClutUI")
            self.notification.show_message(
                title="跳转成功",
                msg="已为您打开Github页面"
            )
        else:
            self.notification.show_message(
                title="跳转取消",
                msg="您取消了跳转"
            )