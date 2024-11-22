# ClutCommitCanvas
语言: [English](README_en.md) | [简体中文](README.md)<br>
Language: [English](README_en.md) | [Simplified Chinese](README.md)<br>
导航栏: 
- [项目介绍](#项目介绍) 📖
- [功能](#功能) ⚙️
- [安装](#安装) 🛠️
- [使用](#使用) 🚀
- [注意事项](#注意事项) ⚠️
- [反馈](#反馈) 💬
- [许可证](#许可证) 📜
- [第三方库](#第三方库) 📚
<br>
## 项目介绍
ClutCommitCanvas 是一个用于管理和可视化 Git 提交历史的工具。它提供了一个直观的界面，帮助用户更好地理解和管理他们的代码库

## 功能

- **提交历史可视化**: 以图表的形式展示 Git 提交历史，帮助用户更好地理解代码库的演变。
- **提交详情查看**: 点击图表中的节点，可以查看每个提交的详细信息，包括提交信息、作者、日期等。
- **分支管理**: 支持查看和管理多个分支，方便用户进行分支操作。
- **搜索功能**: 提供强大的搜索功能，帮助用户快速找到特定的提交记录。

## 安装

要安装 ClutCommitCanvas，请按照以下步骤操作：

1. 前往 [Release](https://github.com/ZZBuAoYe/ClutCommitCanvas/releases) 页面下载最新版本
2. 解压文件
3. 运行 `ClutCommitCanvas.exe`
4. 登录您的Github账户开始一切


## 使用

安装完成后，你可以通过侧边栏的按钮来开始一切<br>
并且你可以登录GitHub账户来快速选择仓库以及软件将为你提供自动登录的服务<br>
在本软件的clone你将获得比较完美的体验<br>

## 注意事项

- 本软件将使用您的GitHub账户来获取您的仓库信息，请确保您的GitHub账户已经登录
- 本软件一切操作均在本地进行，不会上传任何数据到服务器
- 本软件不会收集任何用户信息，请放心使用
- 本软件的`提交功能`暂时没写完，请耐心等待后续版本更新完善该功能

## 反馈

- 如果您有任何问题或建议，请在 [Issues](https://github.com/ZZBuAoYe/ClutCommitCanvas/issues) 页面提出
- 如果您想参与本项目的开发，请在 [Pull Requests](https://github.com/ZZBuAoYe/ClutCommitCanvas/pulls) 页面提出

## 许可证

> 本项目采用MIT许可证，详情请参阅 [LICENSE](LICENSE) 文件<br>
> 可以免费商用，但请注明出处


## 第三方库

- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/intro) - 用于GUI界面
- [GitPython](https://gitpython.readthedocs.io/) - 用于Git操作
- [PyGithub](https://pygithub.readthedocs.io/) - 用于Github API操作
- [ClutUI](https://github.com/buaoyezz/PyQt-ClutUI) - 用于UI设计
- [Requests](https://docs.python-requests.org/zh_CN/latest/) - 用于HTTP请求
- 以及一些其他的库
> 感谢这些库的作者，本软件才能如此完美地运行
- [Pyinstaller](https://pyinstaller.readthedocs.io/) - 用于打包本软件

## 其他事项

- Spec文件源码不包含在仓库中，请自行编写
- 本软件部分图标来源于[IconFinder](https://www.iconfinder.com/)图标站，如有侵权请联系！立刻删除
- 软件初期存在不足，敬请谅解

## 关于编译

- 本软件使用Pyinstaller打包，请确保您的Python环境已经安装了Pyinstaller
- 编译前请确保您的Python环境已经安装了所有依赖库，否则编译将失败
- Hiddenimports必须写入ClutUI的库否则可能失败
如下
```python
    hiddenimports=[
        'assets.utils.clut_button',
        'assets.utils.clut_card',
        'assets.utils.clut_image_card',
        'assets.utils.events',
        'assets.utils.main_ui',
        'assets.utils.message_box',
        'assets.utils.notification_manager',
        'assets.utils.overlay_notification',
        'assets.utils.page_manager',
        'assets.utils.progress_dialog',
        'assets.utils.settings_manager',
        'assets.utils.style_loader',
        'assets.utils.titlebar',
        'assets.pages.about',
        'assets.pages.account_page',
        'assets.pages.home',
        'assets.pages.main_functions',
        'assets.pages.process_page',
        'assets.pages.push_mainfunc'
    ],
```
+ 打包时若需要考虑非python环境请自行修改added_files的值
```python
added_files = [
    ('assets', 'assets'),  # (源文件夹, 目标文件夹)
    ('config', 'config'),
    ('assets/utils', 'assets/utils'),
    ('assets/pages', 'assets/pages')
]
``` 
+ 所以a = Analysis里面需要修改 datas 的值
```python
    datas=added_files, # 打包进去刚刚的added_files
```
+ exe = EXE中的icon值也是需要修改的
```python
    icon= '' # 在里面改入你的图标路径
    # 路径例子:./ClutCommitCanvas.png
    # 还有一些其他配置请自行修改
```
+ 配置完以上信息后请运行`pyinstaller ClutCommitCanvas.spec`命令进行打包
+ 完成以上spec文件正确的配置和打包后，你将可以删除你assets内的utils和pages文件夹

# 结语
> 喜欢的话支持一下ClutUI和本软件吧！！！！
>> 点个Star⭐对我很重要！