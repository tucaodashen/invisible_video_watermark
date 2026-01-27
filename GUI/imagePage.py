import sys
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QColor, QPainter
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel,
                               QScrollArea, QFileDialog)

# 1. 窗口框架从 qframelesswindow 导入
# 注意：使用 FramelessMainWindow 而不是 FramelessWindow，布局更稳定
from qframelesswindow import FramelessMainWindow, StandardTitleBar, WindowEffect

# 2. 组件从 qfluentwidgets 导入
from qfluentwidgets import (CheckBox, SubtitleLabel, CaptionLabel, CardWidget,
                            PrimaryPushButton, setTheme, Theme, isDarkTheme)


# ==========================================
# 第一部分：图片预览组件 (之前的代码)
# ==========================================
class InfoOverlay(CardWidget):
    """ 右上角悬浮层 """
    fitChanged = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(16, 12, 16, 12)
        self.layout.setSpacing(8)

        self.infoLabel = CaptionLabel("等待图片...", self)
        self.fitCheckBox = CheckBox("适合窗口大小", self)
        self.fitCheckBox.setChecked(True)
        self.fitCheckBox.stateChanged.connect(lambda s: self.fitChanged.emit(self.fitCheckBox.isChecked()))

        self.layout.addWidget(SubtitleLabel("图片详情", self))
        self.layout.addWidget(self.infoLabel)
        self.layout.addWidget(self.fitCheckBox)

        self.setFixedWidth(200)
        # 悬浮层背景稍微白一点，防止和底下的亚克力混淆
        self.setStyleSheet("InfoOverlay { background-color: rgba(255, 255, 255, 0.9); border-radius: 8px; }")

    def update_info(self, width, height, fmt="N/A"):
        self.infoLabel.setText(f"尺寸: {width} x {height}\n格式: {fmt}")


class ImagePreviewWidget(QScrollArea):
    """ 主图片显示区域 """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(False)
        self.setAlignment(Qt.AlignCenter)
        self.setFrameShape(QScrollArea.NoFrame)  # 去掉边框，更好看

        # 这一步非常关键！让 ScrollArea 透明，否则它会挡住主窗口的亚克力背景
        self.setStyleSheet("QScrollArea { background: transparent; }")
        self.viewport().setStyleSheet("background: transparent;")

        self.imageLabel = QLabel()
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.imageLabel.setScaledContents(True)
        self.imageLabel.setStyleSheet("background: transparent;")  # Label 也透明
        self.setWidget(self.imageLabel)

        self.originalPixmap = None
        self.isFitWindow = True

        self.overlay = InfoOverlay(self)
        self.overlay.fitChanged.connect(self.setFitWindow)

        # 网格背景设置
        self.gridSize = 20
        self.lightColor = QColor(255, 255, 255, 100)  # 半透明白
        self.darkColor = QColor(200, 200, 200, 100)  # 半透明灰

    def setImage(self, image_path):
        pixmap = QPixmap(image_path)
        if pixmap.isNull(): return
        self.originalPixmap = pixmap
        fmt = image_path.split('.')[-1].upper() if '.' in image_path else "UNK"
        self.overlay.update_info(pixmap.width(), pixmap.height(), fmt)
        self.refreshView()

    def setFitWindow(self, is_fit):
        self.isFitWindow = is_fit
        self.refreshView()

    def refreshView(self):
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
        self.overlay.move(self.width() - self.overlay.width() - 20, 20)
        if self.isFitWindow: self.refreshView()

    def paintEvent(self, event):
        # 绘制半透明网格，这样背景的亚克力效果还能透出来一点
        painter = QPainter(self.viewport())
        width = self.viewport().width()
        height = self.viewport().height()
        rows = height // self.gridSize + 1
        cols = width // self.gridSize + 1
        painter.setPen(Qt.NoPen)
        for r in range(rows):
            for c in range(cols):
                painter.setBrush(self.lightColor if (r + c) % 2 == 0 else self.darkColor)
                painter.drawRect(c * self.gridSize, r * self.gridSize, self.gridSize, self.gridSize)


# ==========================================
# 第二部分：主窗口 (修复透明和控件问题)
# ==========================================
class AcrylicMainWindow(FramelessMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("亚克力图片预览")
        self.resize(900, 700)

        # 1. 必须先把窗口自身的背景设为透明
        # 如果不加这句，Qt 默认的灰色背景会盖住特效
        self.setStyleSheet("AcrylicMainWindow { background: transparent; }")
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 2. 启用 Windows 特效
        self.windowEffect = WindowEffect(self)
        # 根据系统主题决定使用黑色还是白色的半透明效果
        # Win11 推荐使用 setMicaEffect，Win10 使用 setAcrylicEffect
        # 这里为了效果明显，强制开启亚克力模糊
        if isDarkTheme():
            self.windowEffect.setAcrylicEffect(self.winId(), "101010CC")  # CC是透明度
        else:
            self.windowEffect.setAcrylicEffect(self.winId(), "F2F2F2CC")

        # 3. 设置中心控件
        # 我们创建一个 Container，把它也设为透明
        self.container = QWidget()
        self.container.setAttribute(Qt.WA_TranslucentBackground)
        self.setCentralWidget(self.container)

        # 4. 布局与控件
        self.mainLayout = QVBoxLayout(self.container)
        # 顶部留出 40px 给标题栏，否则内容会被标题栏挡住
        self.mainLayout.setContentsMargins(0, 40, 0, 0)
        self.mainLayout.setSpacing(0)

        # 添加我们的图片预览组件
        self.previewWidget = ImagePreviewWidget(self)
        self.mainLayout.addWidget(self.previewWidget, 1)  # stretch=1 占满空间

        # 添加底部控制栏
        self.bottomBar = QWidget()
        self.bottomBar.setFixedHeight(60)
        self.bottomBar.setStyleSheet("background: rgba(255, 255, 255, 0.5);")  # 底部栏半透明白
        self.bottomLayout = QVBoxLayout(self.bottomBar)

        self.openBtn = PrimaryPushButton("打开图片", self)
        self.openBtn.clicked.connect(self.open_image)
        self.bottomLayout.addWidget(self.openBtn, 0, Qt.AlignHCenter)

        self.mainLayout.addWidget(self.bottomBar)

        # 确保标题栏在最上层
        self.titleBar.raise_()

    def open_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择图片", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            self.previewWidget.setImage(file_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 自动识别系统深浅色主题
    setTheme(Theme.AUTO)

    w = AcrylicMainWindow()
    w.show()
    sys.exit(app.exec())