from PIL import Image, ExifTags
from PySide6.QtWidgets import (QApplication, QMainWindow, QFrame, QVBoxLayout,
                               QHBoxLayout, QLabel, QTextEdit, QPushButton, QMessageBox)
from PySide6.QtCore import Qt, Signal, QPoint
from PySide6.QtGui import QDragEnterEvent, QDropEvent
import os
from qfluentwidgets import ListWidget, PrimaryPushButton, CardWidget, CheckBox, isDarkTheme, qconfig
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QPixmap, QColor, QPainter, QBrush, QImage
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel,
                               QScrollArea, QFrame, QHBoxLayout)

from qfluentwidgets import CheckBox, SubtitleLabel, CaptionLabel, CardWidget, themeColor


def get_exif_data(image_path):
    try:
        # 打开图片
        img = Image.open(image_path)

        # 获取 EXIF 数据
        exif_data = img._getexif()

        if exif_data is None:
            print("未找到 EXIF 信息 (可能是截图或已被清除)")
            return
        return_string = "EXIF 信息\n"
        # 将数字 ID 转换为可读的标签名
        for tag_id, value in exif_data.items():
            # 获取标签名称，如果未知则跳过
            tag_name = ExifTags.TAGS.get(tag_id, tag_id)

            # 过滤掉数据量过大的二进制数据（如缩略图），只打印文本/数字
            if tag_name == "MakerNote" or tag_name == "UserComment":
                continue

            return_string += f"{tag_name}: {value}\n"
            return return_string


    except Exception as e:
        print(f"读取错误: {e}")


class DropFrame(QFrame):
    receive_file = Signal(list)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.file = None


    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setStyleSheet("""
                QFrame {
                    border: 2px dashed #0078d7;
                    border-radius: 10px;
                    background-color: #e3f2fd;
                }
            """)

    def dragLeaveEvent(self, event):
        self.setStyleSheet("""
        """)

    def dropEvent(self, event: QDropEvent):
        self.setStyleSheet("""
        """)

        files = []
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if os.path.isfile(file_path):
                files.append(file_path)

        if files:
            # 发送自定义信号或调用父窗口的方法
            if hasattr(self.parent(), 'process_files'):
                self.parent().process_files(files)
            else:
                self.receive_file.emit(files)
        else:
            QMessageBox.warning(self, "无效文件", "请拖放有效的文件")


class DropList(ListWidget):
    receive_file = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setStyleSheet("""
            QListWidget {
                border: 2px dashed #cccccc;
                border-radius: 5px;
            }
        """)  # 设置默认样式

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setStyleSheet("""
                QListWidget {
                    border: 2px dashed #0078d7;
                    border-radius: 5px;
                    background-color: #e3f2fd;
                }
            """)
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self.setStyleSheet("""
            QListWidget {
                border: 2px dashed #cccccc;
                border-radius: 5px;
            }
        """)
        super().dragLeaveEvent(event)  # 重要：调用父类方法

    def dropEvent(self, event: QDropEvent):
        self.setStyleSheet("""
            QListWidget {
                border: 2px dashed #cccccc;
                border-radius: 5px;
            }
        """)

        files = []
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if os.path.isfile(file_path):
                files.append(file_path)

        if files:
            self.receive_file.emit(files)
            print(f"拖放的文件: {files}")
        else:
            QMessageBox.warning(self, "无效文件", "请拖放有效的文件")

        event.acceptProposedAction()  # 重要：接受拖放操作
        super().dropEvent(event)  # 调用父类方法


class RightClickButton(PrimaryPushButton):
    """自定义按钮类，右键点击时发出信号"""

    # 定义右键点击信号，可以传递点击位置
    rightClicked = Signal(QPoint)

    def __init__(self, *args, **kwargs):
        # 处理不同的参数传递方式
        if args and isinstance(args[0], str):
            # 第一个参数是文本
            text = args[0]
            parent = args[1] if len(args) > 1 else None
            super().__init__(parent)
            self.setText(text)
        else:
            # 第一个参数是父控件或没有参数
            parent = args[0] if args else None
            super().__init__(parent)

        self.setMinimumSize(150, 40)

    def mousePressEvent(self, event):
        # 如果是右键点击，发出自定义信号
        if event.button() == Qt.RightButton:
            # 将局部坐标转换为全局坐标
            global_pos = self.mapToGlobal(event.pos())
            self.rightClicked.emit(global_pos)
            event.accept()  # 标记事件已处理，防止默认行为
        else:
            # 左键等其他按钮保持原有行为
            super().mousePressEvent(event)


from PySide6.QtGui import QFontMetrics


class InfoOverlay(CardWidget):
    fitChanged = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.display_text = None
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(16, 12, 16, 12)
        self.layout.setSpacing(8)

        # 1. 文本标签
        self.infoLabel = CaptionLabel("等待图片...", self)
        self.infoLabel.setWordWrap(True)  # 允许换行
        # 允许标签在必要时变宽，而不是死守着宽度换行
        self.infoLabel.setMinimumWidth(200)

        # 2. 复选框
        self.fitCheckBox = CheckBox("适合窗口大小", self)
        self.fitCheckBox.setChecked(True)
        self.fitCheckBox.stateChanged.connect(lambda: self.fitChanged.emit(self.fitCheckBox.isChecked()))

        self.layout.addWidget(SubtitleLabel("图片详情", self))
        self.layout.addWidget(self.infoLabel)
        self.layout.addWidget(self.fitCheckBox)

        # 【修改点 1】不再设置固定的 FixedWidth
        # 而是设置一个范围，让它能伸缩
        self.setMinimumWidth(240)
        self.setMaximumWidth(600)  # 最大允许宽到 600px

        # 初始化样式
        self.updateStyle()
        qconfig.themeChanged.connect(self.updateStyle)

    def updateStyle(self):
        # ... (保持之前的样式代码不变) ...
        if isDarkTheme():
            bg_color = "rgba(32, 32, 32, 0.9)"
            border_color = "rgba(255, 255, 255, 0.1)"
        else:
            bg_color = "rgba(255, 255, 255, 0.9)"
            border_color = "rgba(0, 0, 0, 0.1)"

        self.setStyleSheet(f"""
            InfoOverlay {{
                background-color: {bg_color};
                border: 1px solid {border_color};
                border-radius: 8px;
            }}
        """)

    def set_more_info(self,text):
        display_info = self.display_text + "\n\n" + text
        self.infoLabel.setText(display_info)
        self.adjustSize()

    def update_info(self, width, height, fmt="N/A", path="", exif_text=""):
        """
        智能更新：根据文字长度自动调整组件宽度
        """
        # 1. 构造显示的文本
        # 为了美观，我们把路径单独放一行，并加上 "路径:" 前缀
        display_text = f"尺寸: {width} x {height} | 格式: {fmt}"

        if path:
            display_text += f"\n路径: {path}"

        if exif_text:
            display_text += f"\n\n{exif_text}"
        self.display_text = display_text
        self.infoLabel.setText(display_text)
        self.infoLabel.setToolTip(path)  # 【修改点 2】鼠标悬停显示完整路径，防止截断

        # 【修改点 3】根据内容计算理想宽度 (智能伸缩核心)
        # 获取字体的测量工具
        fm = QFontMetrics(self.infoLabel.font())

        # 计算最长的一行文字有多宽
        # 我们把文本按换行符切开，找最长的那一行
        longest_line_width = 0
        for line in display_text.split('\n'):
            w = fm.horizontalAdvance(line)
            if w > longest_line_width:
                longest_line_width = w

        # 加上内边距 (左右各16px + 一些冗余)
        ideal_width = longest_line_width + 40

        # 限制在 Min(240) 和 Max(600) 之间
        final_width = max(240, min(ideal_width, 600))

        # 应用新的宽度并刷新高度
        self.setFixedWidth(final_width)
        self.adjustSize()


class ImagePreviewWidget(QScrollArea):
    """
    主组件：支持背景网格、图片自适应
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(False)
        self.setAlignment(Qt.AlignCenter)
        self.setFrameShape(QScrollArea.NoFrame)

        # 让 ScrollArea 透明，以便绘制自定义网格
        self.setStyleSheet("QScrollArea { background: transparent; }")
        self.viewport().setStyleSheet("background: transparent;")

        # 内部 Label
        self.imageLabel = QLabel()
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.imageLabel.setScaledContents(True)
        self.imageLabel.setStyleSheet("background: transparent;")
        self.setWidget(self.imageLabel)

        self.originalPixmap = None
        self.isFitWindow = True

        # 悬浮层
        self.overlay = InfoOverlay(self)
        self.overlay.fitChanged.connect(self.setFitWindow)

        # 【关键修改 3】连接主题信号，重新绘制网格
        qconfig.themeChanged.connect(self.viewport().update)

    def paintEvent(self, event):
        """ 绘制棋盘格背景 """
        painter = QPainter(self.viewport())

        # 【关键修改 4】根据主题动态决定网格颜色
        if isDarkTheme():
            # 深色模式：深灰 + 更深灰
            light_color = QColor(45, 45, 45)
            dark_color = QColor(35, 35, 35)
        else:
            # 浅色模式：白 + 浅灰
            light_color = QColor(255, 255, 255)  # 纯白
            dark_color = QColor(240, 240, 240)  # 浅灰

        grid_size = 20
        width = self.viewport().width()
        height = self.viewport().height()

        rows = height // grid_size + 1
        cols = width // grid_size + 1

        painter.setPen(Qt.NoPen)

        for r in range(rows):
            for c in range(cols):
                if (r + c) % 2 == 0:
                    painter.setBrush(light_color)
                else:
                    painter.setBrush(dark_color)

                painter.drawRect(c * grid_size, r * grid_size, grid_size, grid_size)

    def setImage(self, image_path):
        pixmap = QPixmap(image_path)
        if pixmap.isNull(): return
        self.originalPixmap = pixmap

        # 获取格式
        fmt = image_path.split('.')[-1].upper() if '.' in image_path else "UNK"

        # 获取 EXIF
        exif_info = ""
        if fmt in ["JPG", "JPEG", "TIFF"]:
            # 假设你已经定义了之前的 get_exif_info 函数
            exif_info = get_exif_data(image_path)

            # 【修改点】传参时加上 image_path
        self.overlay.update_info(pixmap.width(), pixmap.height(), fmt, image_path, exif_info)

        self.refreshView()

    def set_more_info(self,info):
        self.overlay.set_more_info(info)



    def setFitWindow(self, is_fit):
        self.isFitWindow = is_fit
        self.refreshView()

    def refreshView(self):
        # ... (与之前相同) ...
        if self.originalPixmap is None: return
        if self.isFitWindow:
            viewport_size = self.viewport().size()
            scaled = self.originalPixmap.scaled(viewport_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.imageLabel.setPixmap(scaled)
            self.imageLabel.resize(scaled.size())
        else:
            self.imageLabel.setPixmap(self.originalPixmap)
            self.imageLabel.resize(self.originalPixmap.size())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # 保持悬浮层在右上角
        self.overlay.move(self.width() - self.overlay.width() - 20, 20)
        if self.isFitWindow:
            self.refreshView()