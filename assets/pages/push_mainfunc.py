from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QScrollArea, QFrame, QComboBox, QLineEdit, QTextEdit, QCheckBox)
from PyQt5.QtCore import Qt
from git import Repo
from typing import Dict, List, Tuple
from assets.utils.clut_card import ClutCard
from assets.utils.notification_manager import NotificationManager
from assets.utils.message_box import ClutMessageBox
from assets.utils.clut_button import ClutButton
from assets.pages.process_page import ProcessPage
import os

class PushMainFuncPage(QWidget):
    def __init__(self):
        super().__init__()
        self.notification = NotificationManager()
        self.process_page = ProcessPage.get_instance()
        self.repos = []  # 存储找到的所有Git仓库
        self.setup_ui()
        
    def setup_ui(self):
        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # 标题区域
        title = QLabel("| Git Push")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
            }
        """)
        subtitle = QLabel("Git Push Management")
        subtitle.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.5);
                font-size: 14px;
            }
        """)

        # 路径选择卡片
        path_card = ClutCard(
            title="仓库路径",
            msg="选择要提交的Git仓库路径"
        )
        path_widget = QWidget()
        path_layout = QHBoxLayout(path_widget)
        path_layout.setContentsMargins(20, 20, 20, 20)
        
        path_label = QLabel("本地路径:")
        path_label.setStyleSheet("color: white;")
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("请选择Git仓库路径")
        self.path_input.setStyleSheet("""
            QLineEdit {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 4px;
                color: white;
                padding: 8px;
            }
        """)
        browse_button = ClutButton("浏览", primary=False)
        browse_button.clicked.connect(self.browse_path)
        
        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(browse_button)
        
        path_card.layout().addWidget(path_widget)

        # 添加仓库选择下拉框
        repo_select_layout = QHBoxLayout()
        self.repo_combo = QComboBox()
        self.repo_combo.setStyleSheet("""
            QComboBox {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 4px;
                color: white;
                padding: 8px;
                background-color: transparent;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(assets/icons/dropdown.png);
                width: 12px;
                height: 12px;
            }
        """)
        self.repo_combo.currentIndexChanged.connect(self.on_repo_selected)
        repo_select_layout.addWidget(QLabel("选择仓库:"))
        repo_select_layout.addWidget(self.repo_combo)

        # 添加分支选择
        branch_layout = QHBoxLayout()
        self.branch_combo = QComboBox()
        self.branch_combo.setStyleSheet(self.repo_combo.styleSheet())
        branch_layout.addWidget(QLabel("目标分支:"))
        branch_layout.addWidget(self.branch_combo)

        # 添加推送选项
        push_options_card = ClutCard(
            title="推送选项",
            msg="配置推送方式"
        )
        options_layout = QVBoxLayout()
        
        # 强制推送选项
        self.force_push_cb = QCheckBox("强制推送")
        self.force_push_cb.setStyleSheet("color: white;background: transparent;")
        self.force_push_cb.stateChanged.connect(self.on_force_push_changed)
        options_layout.addWidget(self.force_push_cb)
        
        # 删除远程分支选项
        self.delete_remote_cb = QCheckBox("删除远程分支")
        self.delete_remote_cb.setStyleSheet("color: white;background: transparent;")
        self.delete_remote_cb.stateChanged.connect(self.on_delete_remote_changed)
        options_layout.addWidget(self.delete_remote_cb)
        
        push_options_card.layout().addLayout(options_layout)

        # 提交信息卡片
        commit_card = ClutCard(
            title="提交信息",
            msg="输入提交说明"
        )
        commit_widget = QWidget()
        commit_layout = QVBoxLayout(commit_widget)
        commit_layout.setContentsMargins(20, 20, 20, 20)
        
        self.commit_input = QTextEdit()
        self.commit_input.setPlaceholderText("请输入提交说明")
        self.commit_input.setStyleSheet("""
            QTextEdit {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 4px;
                background-color: transparent;
                color: white;
                padding: 8px;
            }
        """)
        self.commit_input.setMaximumHeight(100)
        commit_layout.addWidget(self.commit_input)
        
        commit_card.layout().addWidget(commit_widget)

        # 按钮区域
        button_layout = QHBoxLayout()
        refresh_button = ClutButton("刷新", primary=False)
        refresh_button.clicked.connect(self.refresh_changes)
        commit_button = ClutButton("提交", primary=True)
        commit_button.clicked.connect(self.commit_changes)
        view_diff_button = ClutButton("查看详细差异", primary=False)
        view_diff_button.clicked.connect(self.show_diff_page)
        
        button_layout.addWidget(refresh_button)
        button_layout.addWidget(commit_button)
        button_layout.addWidget(view_diff_button)
        button_layout.addStretch()

        # 创建一个主滚动区域
        main_scroll = QScrollArea()
        main_scroll.setWidgetResizable(True)
        main_scroll.setStyleSheet("""
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
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        # 创建一个容器widget来存放所有内容
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(20)
        container_layout.setContentsMargins(30, 30, 30, 30)

        # 将所有内容添加到container_layout中
        container_layout.addWidget(title)
        container_layout.addWidget(subtitle)
        container_layout.addWidget(path_card)
        container_layout.addLayout(repo_select_layout)
        container_layout.addLayout(branch_layout)
        container_layout.addWidget(push_options_card)
        container_layout.addWidget(commit_card)
        container_layout.addLayout(button_layout)
        
        # 变更列表区域直接添加到container中
        self.content_layout = QVBoxLayout()
        self.content_layout.setSpacing(10)
        container_layout.addLayout(self.content_layout)
        
        # 设置主滚动区域的widget
        main_scroll.setWidget(container)
        
        # 将主滚动区域添加到主布局
        main_layout.addWidget(main_scroll)

        # 设置主窗口的布局
        self.setLayout(main_layout)

    def show_diff_page(self):
        result = ClutMessageBox.show_message(
            self,
            title="差异查看帮助",
            text="差异详情教程:\n1.你可以选择在GitHub上面查看\n2.你也可以选择直接在软件内直接查看，只要在此页面查找即可，前提是你已经在上面选择了一个库",
            buttons=["确定"]
        )

    def get_colored_diff(self, repo_path: str, file_path: str) -> str:
        """获取带颜色的diff输出"""
        import subprocess
        
        try:
            # 使用git diff命令并保留颜色输出
            process = subprocess.run(
                ['git', 'diff', '--color=always', file_path],  # --color=always 强制启用颜色
                cwd=repo_path,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            if process.returncode != 0:
                return "获取差异失败"
            
            return process.stdout
            
        except Exception as e:
            return f"无法读取差异信息: {str(e)}"

    def scan_git_repos(self, root_path: str):
        """扫描目录下的所有Git仓库"""
        self.repos.clear()
        self.repo_combo.clear()
        
        for root, dirs, files in os.walk(root_path):
            if '.git' in dirs:
                try:
                    repo = Repo(root)
                    self.repos.append(repo)
                    self.repo_combo.addItem(os.path.basename(root), root)
                except Exception:
                    continue
                dirs.remove('.git')  # 不继续扫描.git目录

    def browse_path(self):
        """浏览选择仓库路径"""
        from PyQt5.QtWidgets import QFileDialog
        path = QFileDialog.getExistingDirectory(
            self,
            "选择Git仓库目录",
            "",
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        if path:
            self.scan_git_repos(path)
            self.path_input.setText(path)

    def on_repo_selected(self, index):
        """当选择仓库时更新分支列表"""
        if index >= 0:
            repo_path = self.repo_combo.itemData(index)
            repo = Repo(repo_path)
            self.branch_combo.clear()
            
            # 添加本地分支
            for branch in repo.heads:
                self.branch_combo.addItem(branch.name)
                
            # 设置当前分支为默认选项
            current = repo.active_branch.name
            index = self.branch_combo.findText(current)
            if index >= 0:
                self.branch_combo.setCurrentIndex(index)
            
            self.refresh_changes()

    def on_force_push_changed(self, state):
        """当选择强制推送时显示警告"""
        if state:
            result = ClutMessageBox.show_message(
                self,
                title="强制推送警告",
                text="强制推送可能会覆盖远程仓库的更改。确定要启用吗？",
                buttons=["确定", "取消"]
            )
            if result != "确定":
                self.force_push_cb.setChecked(False)

    def on_delete_remote_changed(self, state):
        """当选择删除远程分支时显示警告"""
        if state:
            result = ClutMessageBox.show_message(
                self,
                title="删除远程分支警告",
                text="此操作将删除远程仓库的分支。确定要继续吗？",
                buttons=["确定", "取消"]
            )
            if result != "确定":
                self.delete_remote_cb.setChecked(False)

    def push_changes(self):
        """推送更改到远程"""
        try:
            current_repo = self.repos[self.repo_combo.currentIndex()]
            target_branch = self.branch_combo.currentText()
            
            # 构建推送选项
            push_options = []
            if self.force_push_cb.isChecked():
                push_options.append("--force")
            if self.delete_remote_cb.isChecked():
                push_options.append("--delete")
            
            # 执行推送
            result = current_repo.git.push(
                "origin",
                target_branch,
                *push_options
            )
            
            self.notification.show_message(
                title="推送成功",
                msg=f"已推送到 {target_branch}",
                duration=2000
            )
            
        except Exception as e:
            self.notification.show_message(
                title="推送失败",
                msg=str(e),
                duration=3000
            )

    def refresh_changes(self):
        """刷新变更"""
        try:
            # 清空现有内容
            for i in reversed(range(self.content_layout.count())):
                widget = self.content_layout.itemAt(i).widget()
                if widget:
                    widget.deleteLater()

            # 获取当前选中的仓库路径
            if self.repo_combo.currentIndex() >= 0:
                repo_path = self.repo_combo.currentData()
            else:
                repo_path = self.path_input.text()

            if not repo_path:
                self.notification.show_message(
                    title="刷新失败",
                    msg="请选择有效的Git仓库路径",
                    duration=3000
                )
                return

            # 验证是否为有效的Git仓库
            try:
                repo = Repo(repo_path)
                if not repo.git_dir:
                    raise Exception("无效的Git仓库")
            except Exception as e:
                self.notification.show_message(
                    title="刷新失败",
                    msg=f"无效的Git仓库: {str(e)}",
                    duration=3000
                )
                return

            # 获取所有变更
            untracked = repo.untracked_files
            diff_index = repo.index.diff(None)  # 工作区和暂存区的差异
            staged_diff = repo.head.commit.diff()  # 暂存区和最后一次提交的差异
            
            # 统计信息
            stats = {
                "new": len(untracked),
                "modified": len([d for d in diff_index if not d.new_file]),
                "staged": len(staged_diff)
            }
            
            # 修改统计信息卡片的样式和间距
            stats_card = ClutCard(
                title="变更统计",
                msg=f"新增文件: {stats['new']} | 修改文件: {stats['modified']} | 已暂存文件: {stats['staged']}"
            )
            stats_card.setContentsMargins(0, 0, 0, 20)  # 添加底部间距
            self.content_layout.addWidget(stats_card)

            # 如果没有任何变更，显示提示信息
            if stats["new"] == 0 and stats["modified"] == 0 and stats["staged"] == 0:
                no_changes_label = QLabel("没有检测到任何变更")
                no_changes_label.setStyleSheet("""
                    QLabel {
                        color: rgba(255, 255, 255, 0.5);
                        font-size: 14px;
                        padding: 20px;
                        margin: 10px 0;
                        qproperty-alignment: AlignCenter;
                    }
                """)
                self.content_layout.addWidget(no_changes_label)
                return

            # 显示已暂存的文件
            if staged_diff:
                staged_header = QLabel("已暂存的更改")
                staged_header.setStyleSheet("""
                    QLabel {
                        color: #4CAF50;
                        font-size: 16px;
                        font-weight: bold;
                        padding: 10px 0;
                        margin-top: 20px;
                    }
                """)
                self.content_layout.addWidget(staged_header)
                
                for d in staged_diff:
                    diff_text = repo.git.diff("--cached", "--color-words", d.a_path)
                    card = FileChangeCard(
                        d.a_path,
                        "已暂存",
                        diff_text,
                        len(diff_text.split('\n'))
                    )
                    card.setContentsMargins(0, 0, 0, 10)  # 添加卡片间距
                    self.content_layout.addWidget(card)

            # 显示未暂存的修改
            if diff_index:
                modified_header = QLabel("未暂存的更改")
                modified_header.setStyleSheet("""
                    QLabel {
                        color: #FFC107;
                        font-size: 16px;
                        font-weight: bold;
                        padding: 10px 0;
                        margin-top: 20px;
                    }
                """)
                self.content_layout.addWidget(modified_header)
                
                for d in diff_index:
                    if not d.new_file:
                        diff_text = repo.git.diff("--color-words", d.a_path)
                        card = FileChangeCard(
                            d.a_path,
                            "修改",
                            diff_text,
                            len(diff_text.split('\n'))
                        )
                        card.setContentsMargins(0, 0, 0, 10)  # 添加卡片间距
                        self.content_layout.addWidget(card)

            # 显示新文件
            if untracked:
                new_header = QLabel("未跟踪的文件")
                new_header.setStyleSheet("""
                    QLabel {
                        color: #2196F3;
                        font-size: 16px;
                        font-weight: bold;
                        padding: 10px 0;
                        margin-top: 20px;
                    }
                """)
                self.content_layout.addWidget(new_header)
                
                for file in untracked:
                    file_path = os.path.join(repo.working_dir, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        card = FileChangeCard(
                            file,
                            "新增",
                            f"+++ {file}\n{content}",
                            len(content.split('\n'))
                        )
                        card.setContentsMargins(0, 0, 0, 10)  # 添加卡片间距
                        self.content_layout.addWidget(card)
                    except UnicodeDecodeError:
                        card = FileChangeCard(
                            file,
                            "新增",
                            "[二进制文件]",
                            1
                        )
                        self.content_layout.addWidget(card)

            self.notification.show_message(
                title="刷新成功",
                msg="已更新变更列表",
                duration=2000
            )

        except Exception as e:
            self.notification.show_message(
                title="刷新失败",
                msg=str(e),
                duration=3000
            )

    def _add_file_card(self, file_path: str, change_type: str, lines: int):
        """添加文件变更卡片"""
        card = ClutCard(
            title=f"{change_type}: {file_path}",
            msg=f"变更行数: {lines}"
        )
        self.content_layout.addWidget(card)

    def commit_changes(self):
        """提交变更"""
        try:
            # 使用输入框中的路径
            repo_path = self.path_input.text() or "."
            repo = Repo(repo_path)
            
            # 检查提交信息是否为空
            commit_msg = self.commit_input.toPlainText().strip()
            if not commit_msg:
                self.notification.show_message(
                    title="提交失败",
                    msg="请输入提交说明",
                    duration=3000
                )
                return
            
            result = ClutMessageBox.show_message(
                self,
                title="确认提交",
                text="是否确认提交所有变更？",
                buttons=["确定", "取消"]
            )
            
            if result == "确定":
                # 添加所有更改到暂存区
                repo.git.add('.')
                # 提交更改
                repo.index.commit(commit_msg)
                self.notification.show_message(
                    title="提交成功",
                    msg="变更已提交到本地仓库",
                    duration=2000
                )
                # 刷新显示
                self.refresh_changes()

        except Exception as e:
            self.notification.show_message(
                title="提交失败",
                msg=str(e),
                duration=3000
            )

    def get_file_diff_stats(self, repo: Repo) -> Tuple[Dict[str, int], List[str], List[str]]:
        """获取文件差异统计信息"""
        diff_stats = {}
        new_files = []
        modified_files = []
        
        # 获取未暂存的更改
        diff = repo.index.diff(None)
        
        # 获取未跟踪的文件
        untracked = repo.untracked_files
        
        # 处理新文件
        for file in untracked:
            new_files.append(file)
            with open(os.path.join(repo.working_dir, file), 'r', encoding='utf-8') as f:
                try:
                    lines = len(f.readlines())
                    diff_stats[file] = lines
                except UnicodeDecodeError:
                    diff_stats[file] = 1

        # 处理修改的文件
        for d in diff:
            if d.a_path not in diff_stats:
                modified_files.append(d.a_path)
                # 使用 git diff 命令获取差异
                diff_output = repo.git.diff(d.a_path, ignore_blank_lines=True, unified=0)
                diff_stats[d.a_path] = len(diff_output.split('\n'))
                
        return diff_stats, new_files, modified_files

    def format_diff_output(self, repo: Repo, file_path: str, is_new: bool = False) -> str:
        try:
            if is_new:
                file_path_full = os.path.join(repo.working_dir, file_path)
                try:
                    with open(file_path_full, 'r', encoding='utf-8') as f:
                        content = f.read()
                    return f"新文件: {file_path}\n\n{content}"
                except UnicodeDecodeError:
                    return f"新文件: {file_path}\n[二进制文件]"
            else:
                # 使用git diff命令获取差异，并指定输出编码
                diff_text = repo.git.diff(
                    file_path,
                    unified=3,
                    no_color=True,  # 禁用颜色代码
                    no_prefix=True,  # 禁用文件前缀
                    encoding='utf-8'  # 指定编码
                ).encode('utf-8').decode('unicode_escape')
                
                return diff_text
                
        except Exception as e:
            return f"无法读取差异信息: {str(e)}"

class FileChangeCard(ClutCard):
    """文件变更卡片组件，用于显示单个文件的变更信息"""
    
    def __init__(self, file_path: str, change_type: str, diff_text: str, lines_changed: int):
        super().__init__(
            title=f"{change_type}: {file_path}",
            msg=f"变更行数: {lines_changed}"
        )
        self.diff_text = diff_text
        self._setup_ui()
        
    def _highlight_diff(self, diff_text: str) -> str:
        """保留git原生颜色的diff显示"""
        html_text = ['<pre style="margin: 0; white-space: pre-wrap; font-family: Consolas, monospace; line-height: 1.5;">']
        
        # ANSI颜色代码到CSS颜色的映射
        color_map = {
            '\x1b[32m': '<span style="color: #00AF00;">',  # 绿色 - 新增
            '\x1b[31m': '<span style="color: #FF0000;">',  # 红色 - 删除
            '\x1b[36m': '<span style="color: #00AFAF;">',  # 青色 - 文件信息
            '\x1b[1m': '<span style="font-weight: bold;">',  # 粗体
            '\x1b[0m': '</span>',  # 重置
            '\x1b[m': '</span>'  # 新增
        }
        
        # 处理ANSI颜色代码
        current_text = diff_text
        for ansi_code, html_tag in color_map.items():
            current_text = current_text.replace(ansi_code, html_tag)
        
        # 添加处理后的文本
        html_text.append(current_text)
        html_text.append('</pre>')
        
        return ''.join(html_text)
        
    def _setup_ui(self):
        """设置卡片UI"""
        # 创建差异文本显示区域
        self.diff_view = QTextEdit()
        self.diff_view.setReadOnly(True)
        self.diff_view.setStyleSheet("""
            QTextEdit {
                background: rgba(0, 0, 0, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 4px;
                color: white;
                font-family: 'Consolas', 'Courier New', monospace;
                padding: 8px;
                line-height: 1.4;
            }
        """)
        
        # 设置HTML格式的差异文本
        self.diff_view.setHtml(self._highlight_diff(self.diff_text))
        self.diff_view.setMinimumHeight(100)
        self.diff_view.setMaximumHeight(300)
        
        # 添加到卡片布局
        self.layout().addWidget(self.diff_view)
