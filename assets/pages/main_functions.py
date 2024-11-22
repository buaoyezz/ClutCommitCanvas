# -*- coding: utf-8 -*-
#=========================
# Git Clone Page
# ClutCommitCanvas Git Clone Page
# B1
#=========================

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QLineEdit, QScrollArea, QFrame, QSpacerItem,
                           QSizePolicy, QProgressDialog)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from assets.utils.clut_card import ClutCard
from assets.utils.notification_manager import NotificationManager
from assets.utils.message_box import ClutMessageBox
from assets.utils.clut_button import ClutButton
from assets.pages.process_page import ProcessPage
from assets.utils.progress_dialog import ClutProgressDialog
import os
import git
import json
import requests
from concurrent.futures import ThreadPoolExecutor
import shutil
from datetime import datetime
import subprocess
import time

class GitClonePage(QWidget):
    def __init__(self):
        super().__init__()
        self.notification = NotificationManager()
        self.config_file = "config/git_config.json"
        self.setup_ui()
        self.load_config()

    def setup_ui(self):
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # 标题区域
        title = QLabel("| Git Clone")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
            }
        """)
        subtitle = QLabel("Git Clone Management")
        subtitle.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.5);
                font-size: 14px;
            }
        """)
        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        # 本地路径配置卡片
        path_card = ClutCard(
            title="本地路径配置",
            msg="设置Git仓库的本地存储路径"
        )
        
        path_widget = QWidget()
        path_layout = QHBoxLayout(path_widget)
        path_layout.setContentsMargins(20, 20, 20, 20)
        
        path_label = QLabel("本地路径:")
        path_label.setStyleSheet("color: white;")
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("请选择Git仓库存储路径")
        self.path_input.setStyleSheet("""
            QLineEdit {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 4px;
                color: white;
                padding: 8px;
            }
        """)
        browse_button = ClutButton("浏览文件夹", primary=False)
        browse_button.clicked.connect(self.browse_path)
        
        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(browse_button)
        
        path_card_layout = path_card.layout()
        path_card_layout.addWidget(path_widget)
        main_layout.addWidget(path_card)

        # Git仓库链接卡片
        repo_card = ClutCard(
            title="仓库链接",
            msg="输入要克隆的Git仓库链接"
        )
        
        repo_widget = QWidget()
        repo_layout = QVBoxLayout(repo_widget)
        repo_layout.setContentsMargins(20, 20, 20, 20)
        repo_layout.setSpacing(16)
        
        # Git链接输入
        link_layout = QHBoxLayout()
        link_label = QLabel("Git Link:")
        link_label.setStyleSheet("color: white;")
        self.link_input = QLineEdit()
        self.link_input.setPlaceholderText("请输入Git仓库链接")
        self.link_input.setStyleSheet(self.path_input.styleSheet())
        
        clone_button = ClutButton("克隆", primary=True)
        clone_button.clicked.connect(self.clone_repository)
        
        link_layout.addWidget(link_label)
        link_layout.addWidget(self.link_input)
        link_layout.addWidget(clone_button)
        
        repo_layout.addLayout(link_layout)
        
        # 快捷克隆区域
        quick_clone_label = QLabel("快捷克隆")
        quick_clone_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
                margin-top: 16px;
            }
        """)
        repo_layout.addWidget(quick_clone_label)
        
        # 仓库列表滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: rgba(255, 255, 255, 0.1);
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 0.2);
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        self.repos_container = QWidget()
        self.repos_layout = QVBoxLayout(self.repos_container)
        self.repos_layout.setContentsMargins(0, 0, 0, 0)
        self.repos_layout.setSpacing(10)
        
        scroll_area.setWidget(self.repos_container)
        repo_layout.addWidget(scroll_area)
        
        repo_card_layout = repo_card.layout()
        repo_card_layout.addWidget(repo_widget)
        main_layout.addWidget(repo_card)
        
        # 添加弹性空间
        main_layout.addStretch()

    def browse_path(self):
        """浏览选择本地路径"""
        from PyQt5.QtWidgets import QFileDialog
        
        path = QFileDialog.getExistingDirectory(
            self,
            "选择仓库存储路径",
            os.path.expanduser("~"),
            QFileDialog.ShowDirsOnly
        )
        
        if path:
            self.path_input.setText(path)
            self.save_config()

    def clone_repository(self):
        """克隆仓库"""
        local_path = self.path_input.text().strip()
        repo_link = self.link_input.text().strip()
        
        if not local_path:
            ClutMessageBox.show_message(
                self,
                title="路径错",
                text="请先设置本地存储路径",
                buttons=["确定"]
            )
            return
            
        if not repo_link:
            ClutMessageBox.show_message(
                self,
                title="链接错误",
                text="请输入Git仓库链接",
                buttons=["确定"]
            )
            return
            
        # 从链接中提取仓库名
        repo_name = repo_link.split('/')[-1]
        if repo_name.endswith('.git'):
            repo_name = repo_name[:-4]
                
        # 完整的克隆路径
        clone_path = os.path.join(local_path, repo_name)
        
        # 检查目标路径是否已存在
        if os.path.exists(clone_path):
            result = ClutMessageBox.show_message(
                self,
                title="路径已存在",
                text=f"目标路径 '{clone_path}' 已存在。\n是否覆盖现有内容？",
                buttons=["确定", "取消"]
            )
            if result == "取消":
                return
                
            # 修改删除逻辑，添加错误处理
            try:
                # 先尝试修改文件权限
                import stat
                def on_rm_error(func, path, exc_info):
                    # 修改文件权限
                    os.chmod(path, stat.S_IWRITE)
                    # 再次尝试删除
                    func(path)
                    
                # 使用错误处理函数删除目录
                shutil.rmtree(clone_path, onerror=on_rm_error)
            except Exception as e:
                ClutMessageBox.show_message(
                    self,
                    title="删除失败",
                    text=f"无法删除现有目录，请手动删除或选择其他位置。\n错误信息：{str(e)}",
                    buttons=["确定"]
                )
                return
        
        # 创建进度对话框
        progress_dialog = ClutProgressDialog(self, title="克隆进度")
        
        # 创建并启动克隆线程
        self.clone_thread = CloneThread(repo_link, clone_path)
        self.clone_thread.progress.connect(progress_dialog.set_status)
        self.clone_thread.speed.connect(lambda s: progress_dialog.speed_label.setText(f"速度: {s} KB/s"))
        
        # 处理克隆完成
        def on_clone_complete(success, message):
            if success:
                progress_dialog.on_clone_complete()
                
        # 处理后台按钮点击
        def on_background_clicked():
            progress_dialog.close()
            process_page = ProcessPage.get_instance()
            process_page.add_task(
                repo_url=repo_link,
                thread=self.clone_thread
            )
            # 在需要时导入
            from assets.utils.page_manager import PageManager
            PageManager.get_instance().slide_to_page("process_page")
        
        # 处理查看按钮点击
        def on_view_clicked():
            progress_dialog.close()
            # 在需要时导入
            from assets.utils.page_manager import PageManager
            PageManager.get_instance().slide_to_page("process_page")
        
        # 处理关闭按钮点击
        def on_close_clicked():
            progress_dialog.close()
        
        # 连接按钮信号
        progress_dialog.background_button.clicked.connect(on_background_clicked)
        progress_dialog.view_button.clicked.connect(on_view_clicked)
        progress_dialog.close_button.clicked.connect(on_close_clicked)
        self.clone_thread.finished.connect(on_clone_complete)
        
        self.clone_thread.start()
        progress_dialog.exec_()

    def on_clone_finished(self, success, message):
        """克隆完成的回调函数"""
        if success:
            self.notification.show_message(
                title="克隆成功",
                msg=message,
                duration=2000
            )
            self.link_input.clear()
        else:
            # 显示错误消息
            ClutMessageBox.show_message(
                self,
                title="克隆失败",
                text=f"Git克隆失败: {message}",
                buttons=["确定"]
            )
            print(f"Git克隆失败: {message}")
            
            # 保存错误日志
            os.makedirs("./ErrorMsg", exist_ok=True)
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            error_file = f"./ErrorMsg/clone_error_{current_time}.log"
            ClutMessageBox.show_message(
                None,
                title="克隆失败",
                text=f"错误日志已保存到: {error_file}",
                buttons=["确定"]
            )
            
            with open(error_file, "w", encoding="utf-8") as f:
                f.write(f"克隆失败时间: {current_time}\n")
                f.write(f"错误信息: {message}\n")

    def load_user_repos(self):
        """加载用户的GitHub仓库列表"""
        try:
            # 从配置文件获取Token
            if not os.path.exists(self.config_file):
                self.show_login_reminder()
                return
                
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                token = config.get('password')
                username = config.get('username')
                
            if not token or not username:
                self.show_login_reminder()
                return
                
            for i in reversed(range(self.repos_layout.count())): 
                self.repos_layout.itemAt(i).widget().setParent(None)
                
            # 获取仓库列表
            headers = {
                'Authorization': f'token {token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            response = requests.get(
                f'https://api.github.com/users/{username}/repos',
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                repos = response.json()
                
                # 过滤掉个人配置仓库
                repos = [repo for repo in repos if not repo['name'].endswith('profile')]
                
                for repo in repos:
                    repo_card = ClutCard(
                        title=repo['name'],
                        msg=repo['description'] or "暂无描述"
                    )
                    
                    # 添加点击事件
                    repo_url = repo['clone_url']
                    repo_card.mousePressEvent = lambda _, url=repo_url: self.quick_clone(url)
                    
                    self.repos_layout.addWidget(repo_card)
                    
        except Exception as e:
            print(f"加载仓库列表失败: {str(e)}")
            self.notification.show_message(
                title="加载失败",
                msg="无法获取仓库列表，请检查网络连接",
                duration=2000
            )

    def show_login_reminder(self):
        """显示登录提醒"""
        result = ClutMessageBox.show_message(
            self,
            title="需要登录",
            text="使用快捷克隆功能需要先登录GitHub账户。\n是否现在去登录？",
            buttons=["去登录", "取消"]
        )
        
        if result == "去登录":
            # TODO: 跳转到登录页面
            pass

    def quick_clone(self, repo_url):
        """快捷克隆指定仓库"""
        # 添加确认对话框
        result = ClutMessageBox.show_message(
            self,
            title="确认克隆",
            text=f"是否克隆该仓库？\n{repo_url}",
            buttons=["确定", "取消"]
        )
        
        if result == "确定":
            self.link_input.setText(repo_url)
            self.clone_repository()

    def load_config(self):
        """加载配置"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    last_path = config.get('clone_path')
                    if last_path and os.path.exists(last_path):
                        self.path_input.setText(last_path)
                        
            # 加载用户仓库列表
            self.load_user_repos()
                        
        except Exception as e:
            print(f"加载配置失败: {str(e)}")

    def save_config(self):
        """保存配置"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
            else:
                config = {}
                
            config['clone_path'] = self.path_input.text()
            
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(config, f)
                
        except Exception as e:
            print(f"保存配置失败: {str(e)}")

class RepoListThread(QThread):
    def __init__(self, username):
        super().__init__()
        self.username = username
        
    def run(self):
        try:
            self.status.emit("正在获取仓库列表...")
            
            # 禁用 SSL 验证
            import ssl
            ssl._create_default_https_context = ssl._create_unverified_context
            
            # 设置请求头和超时时间
            headers = {
                'User-Agent': 'Mozilla/5.0',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            url = f'https://api.github.com/users/{self.username}/repos'
            response = requests.get(
                url, 
                headers=headers,
                verify=False,  # 禁用 SSL 验证
                timeout=30     # 增加超时时间
            )
            
            if response.status_code == 200:
                repos = response.json()
                self.finished.emit(True, repos)
            else:
                raise Exception(f"API 请求失败: {response.status_code}")
                
        except Exception as e:
            self.finished.emit(False, str(e))

class CloneThread(QThread):
    progress = pyqtSignal(str)  # 进度信号
    finished = pyqtSignal(bool, str)  # 完成信号(成功/失败, 消息)
    speed = pyqtSignal(float)  # 添加速度信号，单位为 KB/s
    
    def __init__(self, repo_link, clone_path):
        super().__init__()
        self.repo_link = repo_link
        self.clone_path = os.path.abspath(clone_path)
        self._last_bytes = 0
        self._last_time = time.time()

    def _update_speed(self, current_bytes):
        """更新克隆速度"""
        current_time = time.time()
        time_diff = current_time - self._last_time
        if time_diff >= 1.0:  # 每秒更新一次速度
            bytes_diff = current_bytes - self._last_bytes
            speed = bytes_diff / 1024 / time_diff  # 转换为 KB/s
            self.speed.emit(speed)
            self._last_bytes = current_bytes
            self._last_time = current_time

    def run(self):
        try:
            self.progress.emit("正在克隆仓库...")
            
            # 配置 git
            git_cmds = [
                ['git', 'config', '--global', 'http.sslVerify', 'false'],
                ['git', 'config', '--global', 'https.sslVerify', 'false'],
                # 增加缓冲区大小
                ['git', 'config', '--global', 'http.postBuffer', '524288000'],
                # 增加超时时间
                ['git', 'config', '--global', 'http.lowSpeedLimit', '1000'],
                ['git', 'config', '--global', 'http.lowSpeedTime', '300']
            ]
            
            for cmd in git_cmds:
                subprocess.run(cmd, check=True)
            
            # 克隆命令
            clone_cmd = [
                'git',
                'clone',
                '--depth', '1',  # 浅克隆以加快速度
                '--progress',
                self.repo_link,
                self.clone_path
            ]
            
            process = subprocess.Popen(
                clone_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                encoding='utf-8'
            )
            
            while True:
                output = process.stderr.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.progress.emit(output.strip())
                    self._update_speed(process.stderr.tell())
            
            if process.returncode == 0:
                self.finished.emit(True, "克隆成功")
            else:
                raise Exception("克隆失败，请检查网络连接")
                
        except Exception as e:
            self.finished.emit(False, f"克隆失败: {str(e)}")