# -*- coding: utf-8 -*-
#=========================
# Account Page 
# ClutCommitCanvas Account Page
# B1
#=========================

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QLineEdit, QPushButton, QFrame, QSpacerItem,
                           QSizePolicy)
from PyQt5.QtCore import Qt
from assets.utils.clut_card import ClutCard
from assets.utils.clut_image_card import ClutImageCard
from assets.utils.notification_manager import NotificationManager
from assets.utils.message_box import ClutMessageBox
from assets.utils.clut_button import ClutButton
import os
import json
import webbrowser
from PyQt5.QtCore import QTimer
import base64

class AccountPage(QWidget):
    def __init__(self):
        super().__init__()
        self.notification = NotificationManager()
        self.config_file = "config/git_config.json"
        self.is_logged_in = False
        self.user_info = None
        self.setup_ui()
        
        # 加载凭据并自动登录
        QTimer.singleShot(500, self.load_saved_credentials)
        
    def setup_ui(self):
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # 标题区域
        title_area = QWidget()
        title_layout = QVBoxLayout(title_area)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(4)

        title = QLabel("| 账户管理")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
            }
        """)
        subtitle = QLabel("Account Management")
        subtitle.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.5);
                font-size: 14px;
            }
        """)

        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)
        main_layout.addWidget(title_area)

        # 按钮区域
        button_area = QWidget()
        button_layout = QHBoxLayout(button_area)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(10)

        self.status_button = ClutButton("账户状态", primary=True)
        self.status_button.clicked.connect(self.show_account_status)
        self.logout_button = ClutButton("退出登录", primary=False)
        self.logout_button.clicked.connect(self.logout)
        self.logout_button.hide()  # 初始隐藏

        # 添加刷新按钮
        self.refresh_button = ClutButton("刷新", primary=False)
        self.refresh_button.clicked.connect(self.refresh_user_info)
        self.refresh_button.hide()  # 初始隐藏

        button_layout.addWidget(self.status_button)
        button_layout.addWidget(self.logout_button)
        button_layout.addWidget(self.refresh_button)
        button_layout.addStretch()

        help_button = ClutButton("帮助", primary=False)
        help_button.clicked.connect(self.show_help_dialog)
        button_layout.addWidget(help_button)

        main_layout.addWidget(button_area)

        # 登录区域
        self.login_widget = QWidget()
        login_layout = QVBoxLayout(self.login_widget)
        login_layout.setContentsMargins(0, 0, 0, 0)
        login_layout.setSpacing(16)

        # 登录卡片
        login_card = ClutCard(
            title="Git账户登录",
            msg="请输入您的Git账户信息以登录"
        )
        
        # 表单区域
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setSpacing(16)

        # 用户名输入
        username_layout = QVBoxLayout()
        username_label = QLabel("用户名")
        username_label.setStyleSheet("color: white; font-size: 14px;")
        self.username_input = QLineEdit()
        self.username_input.setStyleSheet("""
            QLineEdit {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 4px;
                color: white;
                padding: 8px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid rgba(255, 255, 255, 0.3);
            }
        """)
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)

        # 密码输入
        password_layout = QHBoxLayout()
        password_input_layout = QVBoxLayout()
        password_label = QLabel("密码/Token")
        password_label.setStyleSheet("color: white; font-size: 14px;")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(self.username_input.styleSheet())
        
        # 添加显示/隐藏密码按钮
        self.toggle_password_btn = QPushButton()
        self.toggle_password_btn.setFixedSize(30, 30)
        self.toggle_password_btn.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
                color: white;
            }
            QPushButton:checked {
                color: rgba(255, 255, 255, 0.5);
            }
        """)
        self.toggle_password_btn.setText("👁")  # 使用 Unicode 字符替代 SVG
        self.toggle_password_btn.clicked.connect(self.toggle_password_visibility)
        
        password_input_layout.addWidget(password_label)
        password_input_layout.addWidget(self.password_input)
        password_layout.addLayout(password_input_layout)
        password_layout.addWidget(self.toggle_password_btn)

        # 登录按钮
        self.login_button = ClutButton("登录", primary=True)
        self.login_button.clicked.connect(self.login)

        # 添加到表单布局
        form_layout.addLayout(username_layout)
        form_layout.addLayout(password_layout)
        form_layout.addWidget(self.login_button)

        login_card_layout = login_card.layout()
        login_card_layout.addWidget(form_widget)
        
        login_layout.addWidget(login_card)
        
        # 用户信息卡片(初始隐藏)
        self.user_info_widget = QWidget()
        self.user_info_widget.hide()
        user_info_layout = QVBoxLayout(self.user_info_widget)
        user_info_layout.setContentsMargins(0, 0, 0, 0)
        
        self.user_card = ClutImageCard(
            title="未登录",
            msg="请先登录您的Git账户",
            image_url="./assets/images/avatars/user_avatars.png",
            image_mode=1
        )
        user_info_layout.addWidget(self.user_card)

        # 在用户信息卡片下方添加仓库列表区域
        self.repos_widget = QWidget()
        self.repos_widget.hide()
        repos_layout = QVBoxLayout(self.repos_widget)
        repos_layout.setContentsMargins(0, 0, 0, 0)
        repos_layout.setSpacing(16)

        # 仓库列表标题
        repos_title = QLabel("仓库")
        repos_title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
            }
        """)
        repos_layout.addWidget(repos_title)

        # 仓库列表容器
        self.repos_container = QWidget()
        self.repos_container_layout = QVBoxLayout(self.repos_container)
        self.repos_container_layout.setContentsMargins(0, 0, 0, 0)
        self.repos_container_layout.setSpacing(16)
        repos_layout.addWidget(self.repos_container)

        # 添加到主布局
        main_layout.addWidget(self.login_widget)
        main_layout.addWidget(self.user_info_widget)
        main_layout.addWidget(self.repos_widget)
        main_layout.addStretch()

    def toggle_password_visibility(self):
        """切换密码显示/隐藏"""
        if self.toggle_password_btn.isChecked():
            self.password_input.setEchoMode(QLineEdit.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.Password)

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

    def load_saved_credentials(self):
        """加载保存的凭据"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    
                    # 设置用户名和密码
                    self.username_input.setText(config.get('username', ''))
                    self.password_input.setText(config.get('password', ''))
                    
                    # 如果有凭据就自动登录
                    if self.username_input.text() and self.password_input.text():
                        QTimer.singleShot(1000, self.login)
                    
        except Exception as e:
            print(f"加载配置失败: {str(e)}")

    def save_credentials(self):
        """保存Git凭据"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            return
        
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            
            # 直接保存配置
            config = {
                'username': username,
                'password': password  # 直接保存密码，不加密
            }
            
            with open(self.config_file, 'w') as f:
                json.dump(config, f)
                
        except Exception as e:
            print(f"保存凭据失败: {str(e)}")
            self.notification.show_message(
                title="保存失败",
                msg="无法保存登录信息",
                duration=2000
            )

    def test_connection(self):
        """测试Git连接"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            ClutMessageBox.show_message(
                self,
                title="输入错误",
                text="请先填写Git账户息",
                buttons=["确定"]
            )
            return
            
        try:
            import tempfile
            import shutil
            import git  
            
            temp_dir = tempfile.mkdtemp()
            repo = git.Repo.init(temp_dir)
            
            remote_url = f"https://{username}:{password}@github.com/{username}/test.git"
            origin = repo.create_remote('origin', remote_url)
            
            # 测试
            origin.fetch()
            
            shutil.rmtree(temp_dir)
            
            self.notification.show_message(
                title="连接成功",
                msg="Git连接测试成功!",
                duration=2000
            )
            
            # TODO: 添加实际的连接测试逻辑
            
        except Exception as e:
            ClutMessageBox.show_message(
                self,
                title="连接失败",
                text=f"Git连接测试失败: {str(e)}",
                buttons=["确定"]
            )
    
    def verify_git_credentials(self, username, token):
        """验证Git凭据"""
        try:
            import requests
            
            # 添加提示信息
            if not token.startswith('ghp_') and not token.startswith('github_pat_'):
                return False, "无效的Token格式，请确保复制了完整的Personal Access Token"
            
            headers = {
                'Authorization': f'token {token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            response = requests.get(
                'https://api.github.com/user',
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                user_data = response.json()
                # 验证用户名是否匹配
                if user_data['login'].lower() == username.lower():
                    # 提取所需的用户信息
                    return True, {
                        'username': user_data['login'],
                        'name': user_data.get('name'),
                        'email': user_data.get('email'),
                        'avatar_url': user_data.get('avatar_url'),
                        'location': user_data.get('location'),
                        'blog': user_data.get('blog'),
                        'public_repos': user_data.get('public_repos'),
                        'followers': user_data.get('followers'),
                        'following': user_data.get('following')
                    }
                else:
                    return False, "用户名与Token不匹配"
            else:
                error_msg = response.json().get('message', '验证失败')
                error_details = f"状态码: {response.status_code}, 错误信息: {error_msg}"
                print(f"API响应详情: {error_details}")
                return False, f"GitHub API错误: {error_msg}"
                
        except Exception as e:
            print(f"验证异常详情: {str(e)}")
            return False, f"验证过程出错: {str(e)}"
    
    def login(self):
        """处理登录"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            ClutMessageBox.show_message(
                self,
                title="入错误",
                text="请填写完整的用户名和密码/Token",
                buttons=["确定"]
            )
            return
            
        try:
            # 验证凭据
            success, result = self.verify_git_credentials(username, password)
            
            if success:
                # 保存凭据
                config = {
                    'username': username,
                    'password': password
                }
                os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
                with open(self.config_file, 'w') as f:
                    json.dump(config, f)
                
                # 更新登录状态和用户信息
                self.is_logged_in = True
                self.user_info = {
                    'username': username,
                    'avatar_url': result.get('avatar_url'),
                    'name': result.get('name', username),
                    'email': result.get('email', ''),
                    'public_repos': result.get('public_repos', 0),
                    'location': result.get('location', ''),
                    'blog': result.get('blog', ''),
                    'followers': result.get('followers', 0),
                    'following': result.get('following', 0),
                    'created_at': result.get('created_at', '')
                }
                
                # 更新UI
                self.update_ui_after_login()
                
                self.notification.show_message(
                    title="登录成功",
                    msg=f"欢迎回来, {self.user_info['name']}!",
                    duration=2000
                )
            else:
                raise Exception(result)
                
        except Exception as e:
            ClutMessageBox.show_message(
                self,
                title="登录失败",
                text=f"验证失败: {str(e)}",
                buttons=["确定"]
            )
            print(f"登录失败: {str(e)}")
    
    def update_ui_after_login(self):
        """登录后更新UI"""
        import os  # 将 import 移到方法开始处
        import requests  # 提前导入 requests
        
        self.login_widget.hide()
        self.user_info_widget.show()
        self.logout_button.show()
        
        # 更新用户信息卡片
        if self.user_card:
            # 设置头像路径
            avatar_path = os.path.join("assets", "images", "avatars", f"user_avatars.png")
            default_avatar = os.path.join("assets", "images", "avatars", "user_avatars.png")
            
            # 如果有头像URL则下载
            if self.user_info.get('avatar_url'):
                try:
                    # 确保目录存在
                    os.makedirs(os.path.join("assets", "images", "avatars"), exist_ok=True)
                    
                    # 下载头像
                    response = requests.get(self.user_info['avatar_url'])
                    if response.status_code == 200:
                        with open(avatar_path, 'wb') as f:
                            f.write(response.content)
                        self.user_card.image_url = avatar_path
                    else:
                        self.user_card.image_url = default_avatar
                except Exception as e:
                    print(f"下载头像失败: {str(e)}")
                    self.user_card.image_url = default_avatar
            else:
                self.user_card.image_url = default_avatar
            
            # 更新标题和信息
            name_display = self.user_info.get('name', '') or self.user_info['username']
            info_text = [
                f"@{self.user_info['username']}",  # GitHub用户名
                f"状态: 已登录"
            ]
            
            # 添加可选信息
            if self.user_info.get('email'):
                info_text.append(f"邮箱: {self.user_info['email']}")
            if self.user_info.get('public_repos'):
                info_text.append(f"公开仓库: {self.user_info['public_repos']}")
            if self.user_info.get('location'):
                info_text.append(f"位置: {self.user_info['location']}")
            if self.user_info.get('blog'):
                info_text.append(f"网站: {self.user_info['blog']}")
            if self.user_info.get('followers'):
                info_text.append(f"粉丝: {self.user_info['followers']}")
            if self.user_info.get('following'):
                info_text.append(f"关注: {self.user_info['following']}")
            if self.user_info.get('created_at'):
                info_text.append(f"账户创建于: {self.user_info['created_at']}")
            
            self.user_card.title_label.setText(name_display)
            self.user_card.msg_label.setText('\n'.join(info_text))
            
            # 强制更新卡片
            self.user_card.update()
        
        # 显示刷新按钮
        self.refresh_button.show()
        
        # 获取并显示仓库列表
        self.fetch_and_display_repos()
        
        # 更新按钮状态
        self.status_button.setText("已登录")
    
    def logout(self):
        """处理登出"""
        result = ClutMessageBox.show_message(
            self,
            title="确认退出",
            text="确定要退出登录吗？",
            buttons=["确定", "取消"]
        )
        
        if result == "确定":
            # 清除配置文件
            if os.path.exists(self.config_file):
                os.remove(self.config_file)
            
            # 重置状态
            self.is_logged_in = False
            self.user_info = None
            
            # 更新UI
            self.login_widget.show()
            self.user_info_widget.hide()
            self.logout_button.hide()
            self.status_button.setText("账户状态")
            
            # 清空输入框
            self.username_input.clear()
            self.password_input.clear()
            
            self.notification.show_message(
                title="已退出登录",
                msg="您成功退出登录",
                duration=2000
            )
    
    def show_account_status(self):
        """显示账户状态"""
        if self.is_logged_in:
            status_text = f"当前登录账户: {self.user_info['username']}\n状态: 已登录"
        else:
            status_text = "当前未登录\n请登录您的Git账户"
            
        ClutMessageBox.show_message(
            self,
            title="账户状态",
            text=status_text,
            buttons=["确定"]
        )
    
    def show_help_dialog(self):
        """显示帮助信息"""
        help_text = (
            "如何登录 GitHub 账户：\n\n"
            "1. 首先需要创建个人访问令牌(Personal Access Token)：\n"
            "   • 访问 GitHub.com 并登录\n"
            "   • 点击右上角头像 -> Settings\n"
            "   • 滚动到底部，点击 Developer settings\n"
            "   • 选择 Personal access tokens -> Tokens (classic)\n"
            "   • 点击 Generate new token (classic)\n\n"
            "2. 生成令牌时的设置：\n"
            "   • Note: 填写一个好记的名字（如：ClutCommitCanvas）\n"
            "   • Expiration: 建议选择 No expiration\n"
            "   • 勾选权限范围：至少选择 repo（完整仓库访问权限）\n"
            "   • 点击底部的 Generate token\n\n"
            "3. 在本软件登录：\n"
            "   • 用户名：输入你的 GitHub 用户名\n"
            "   • 密码/Token：粘贴你刚刚生成的令牌\n\n"
            "注意：令牌只显示一次，请务必保存好！\n"
            "需要查看详细教程吗？"
        )
        
        result = ClutMessageBox.show_message(
            self,
            title="登录教程",
            text=help_text,
            buttons=["查看详细教程", "我知道了"]
        )
        
        if result == "查看详细教程":
            webbrowser.open("https://docs.github.com/cn/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token")
            self.notification.show_message(
                title="已打开教程",
                msg="已为您打开GitHub官方教程页面"
            )
    
    def refresh_user_info(self):
        """刷新用户信息和仓库列表"""
        if not self.is_logged_in:
            return
            
        try:
            # 重新验证并获取用户信息
            success, result = self.verify_git_credentials(
                self.user_info['username'], 
                self.password_input.text().strip()
            )
            
            if success:
                # 更新用户信息
                self.user_info.update(result)
                self.update_ui_after_login()
                
                # 获取并更新仓库列表
                self.fetch_and_display_repos()
                
                self.notification.show_message(
                    title="刷新成功",
                    msg="用户信息已更新",
                    duration=2000
                )
            else:
                raise Exception(result)
                
        except Exception as e:
            self.notification.show_message(
                title="刷新失败",
                msg=f"更新信息失败: {str(e)}",
                duration=2000
            )
        
        # 在这里添加刷新用户信息和仓库列表的逻辑

    def fetch_and_display_repos(self):
        """获取并显示用户的仓库列表"""
        try:
            import requests
            
            headers = {
                'Authorization': f'token {self.password_input.text().strip()}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            response = requests.get(
                f'https://api.github.com/users/{self.user_info["username"]}/repos',
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                # 清除现有的仓库卡片
                for i in reversed(range(self.repos_container_layout.count())): 
                    self.repos_container_layout.itemAt(i).widget().setParent(None)
                
                repos = response.json()
                for repo in repos:
                    # 构建卡片显示信息
                    description = repo['description'] or "暂无描述"
                    info_text = []
                    if repo['language']:
                        info_text.append(f"主要语言: {repo['language']}")
                    info_text.append(f"⭐ {repo['stargazers_count']}")
                    
                    # 完整描述文本
                    full_msg = f"{description}\n" + " | ".join(info_text)
                    
                    # 创建卡片
                    repo_card = ClutCard(
                        title=repo['name'],
                        msg=full_msg  # 直接在创建时设置完整消息
                    )
                    
                    # 添加点击事件
                    repo_url = repo['html_url']  # 保存URL到局部变量
                    repo_card.mousePressEvent = lambda e, url=repo_url: self.show_repo_dialog(url)
                    
                    self.repos_container_layout.addWidget(repo_card)
                
                # 显示仓库列表区域
                self.repos_widget.show()
                
        except Exception as e:
            print(f"获取仓库列表失败: {str(e)}")
            self.notification.show_message(
                title="获取失败",
                msg="无法获取仓库列表",
                duration=2000
            )

    def show_repo_dialog(self, repo_url):
        """显示仓库跳转确认对话框"""
        result = ClutMessageBox.show_message(
            self,
            title="查看仓库",
            text="是否在浏览器中打开该仓库？",
            buttons=["确定", "取消"]
        )
        
        if result == "确定":
            webbrowser.open(repo_url)
            self.notification.show_message(
                title="跳转成功",
                msg="已为您打开仓库页面",
                duration=2000
            )