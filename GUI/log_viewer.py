import os
import re
from datetime import datetime
from typing import List, Dict, Optional, Set
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QPlainTextEdit, QComboBox, QPushButton, 
                              QCheckBox, QFileDialog, QLabel, QScrollArea,
                              QFrame, QSplitter, QGroupBox)
from PySide6.QtCore import QTimer, Qt, QThread, Signal, QFile, QTextStream, QRect, QSize
from PySide6.QtGui import QTextCharFormat, QColor, QFont, QTextCursor, QPainter, QTextFormat

try:
    from qfluentwidgets import (FluentIcon, PushButton, ComboBox, CheckBox, 
                              InfoBar, InfoBarPosition, setTheme, Theme, 
                              FluentBackgroundTheme, isDarkTheme)
    QFLUENT_AVAILABLE = True
except ImportError:
    QFLUENT_AVAILABLE = False


class LogEntry:
    """日志条目类"""
    def __init__(self, timestamp: str, level: str, location: str, message: str, raw_line: str):
        self.timestamp = timestamp
        self.level = level
        self.location = location
        self.message = message
        self.raw_line = raw_line
        self.datetime = self._parse_timestamp(timestamp)
    
    def _parse_timestamp(self, timestamp: str) -> Optional[datetime]:
        """解析时间戳"""
        try:
            return datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
            try:
                return datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return None


class LogFileWatcher(QThread):
    """日志文件监视器线程"""
    new_lines = Signal(list)
    
    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path
        self.last_position = 0
        self.running = False
        self._stop_flag = False
    
    def run(self):
        """运行文件监视"""
        self.running = True
        while not self._stop_flag:
            try:
                if os.path.exists(self.file_path):
                    with open(self.file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        f.seek(self.last_position)
                        new_lines = f.readlines()
                        if new_lines:
                            self.last_position = f.tell()
                            self.new_lines.emit(new_lines)
                self.msleep(1000)  # 每500毫秒检查一次
            except Exception as e:
                print(f"文件监视错误: {e}")
                self.msleep(5000)  # 出错时等待更长时间
    
    def stop(self):
        """停止监视"""
        self._stop_flag = True
        self.wait()


class LineNumberArea(QWidget):
    """行号区域组件"""
    
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
    
    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(), 0)
    
    def paintEvent(self, event):
        self.editor.line_number_area_paint_event(event)


class LogTextEdit(QPlainTextEdit):
    """带行号的文本编辑器"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.line_number_area = LineNumberArea(self)
        
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        
        self.update_line_number_area_width(0)
        self.setFont(QFont("Consolas", 10))
        
    def line_number_area_width(self):
        """计算行号区域宽度"""
        if not QFLUENT_AVAILABLE:
            digits = 1
            max_num = max(1, self.blockCount())
            while max_num >= 10:
                max_num /= 10
                digits += 1
            space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
            return space
        else:
            digits = 1
            max_num = max(1, self.blockCount())
            while max_num >= 10:
                max_num /= 10
                digits += 1
            space = 8 + self.fontMetrics().horizontalAdvance('9') * digits
            return space
    
    def update_line_number_area_width(self, new_block_count):
        """更新行号区域宽度"""
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)
    
    def update_line_number_area(self, rect, dy):
        """更新行号区域"""
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())
        
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)
    
    def resizeEvent(self, event):
        """调整大小事件"""
        super().resizeEvent(event)
        
        cr = self.contentsRect()
        self.line_number_area.setGeometry(QRect(cr.left(), cr.top(), 
                                               self.line_number_area_width(), cr.height()))
    
    def line_number_area_paint_event(self, event):
        """绘制行号"""
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), QColor(240, 240, 240) if not QFLUENT_AVAILABLE or not isDarkTheme() else QColor(60, 60, 60))
        
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()
        
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                if QFLUENT_AVAILABLE and isDarkTheme():
                    painter.setPen(QColor(180, 180, 180))
                else:
                    painter.setPen(QColor(120, 120, 120))
                
                painter.drawText(0, int(top), self.line_number_area.width() - 3, 
                               self.fontMetrics().height(), Qt.AlignRight, number)
            
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1
    
    def clear(self):
        """清空文本"""
        super().clear()
        self.update_line_number_area_width(0)


class LogViewerWindow(QMainWindow):
    """日志查看器主窗口"""
    
    LOG_LEVELS = ['SUCCESS', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    LOG_COLORS = {
        'SUCCESS': QColor(144, 238, 144),  # 浅绿色
        'DEBUG': QColor(211, 211, 211),    # 浅灰色
        'INFO': QColor(173, 216, 230),     # 浅蓝色
        'WARNING': QColor(255, 228, 181),  # 浅橙色
        'ERROR': QColor(255, 182, 193),    # 浅红色
        'CRITICAL': QColor(221, 160, 221)  # 浅紫色
    }
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_file_path = None
        self.log_entries: List[LogEntry] = []
        self.filtered_entries: List[LogEntry] = []
        self.selected_levels: Set[str] = set(self.LOG_LEVELS)
        self.auto_scroll = True
        self.file_watcher = None
        
        # 设置qfluentwidgets主题
        if QFLUENT_AVAILABLE:
            setTheme(Theme.AUTO)
        
        self._init_ui()
        self._setup_timer()
        
        # 信息提示列表
        self.info_bars = []
    
    def _init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("日志查看器")
        self.setGeometry(100, 100, 1200, 800)
        
        # 创建中央窗口
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 创建控制面板
        control_panel = self._create_control_panel()
        main_layout.addWidget(control_panel)
        
        # 创建日志显示区域（带行号）
        self.log_display = LogTextEdit()
        self.log_display.setReadOnly(True)
        main_layout.addWidget(self.log_display)
        
        # 创建状态栏
        self.status_label = QLabel("就绪")
        self.statusBar().addWidget(self.status_label)
    
    def _create_control_panel(self) -> QGroupBox:
        """创建控制面板"""
        group_box = QGroupBox("控制面板")
        layout = QHBoxLayout(group_box)
        
        # 文件选择按钮
        if QFLUENT_AVAILABLE:
            self.file_button = PushButton(FluentIcon.FOLDER, "选择日志文件")
            self.refresh_button = PushButton(FluentIcon.SYNC, "刷新")
            self.clear_button = PushButton(FluentIcon.DELETE, "清空显示")
        else:
            self.file_button = QPushButton("选择日志文件")
            self.refresh_button = QPushButton("刷新")
            self.clear_button = QPushButton("清空显示")
        
        self.file_button.clicked.connect(self._select_file)
        layout.addWidget(self.file_button)
        
        # 刷新按钮
        self.refresh_button.clicked.connect(self._refresh_log)
        self.refresh_button.setEnabled(False)
        layout.addWidget(self.refresh_button)
        
        # 日志级别过滤
        layout.addWidget(QLabel("日志级别:"))
        if QFLUENT_AVAILABLE:
            self.level_combo = ComboBox()
        else:
            self.level_combo = QComboBox()
        self.level_combo.addItems(["全部"] + self.LOG_LEVELS)
        self.level_combo.currentTextChanged.connect(self._filter_logs)
        layout.addWidget(self.level_combo)
        
        # 自动滚动复选框
        if QFLUENT_AVAILABLE:
            self.auto_scroll_checkbox = CheckBox("自动滚动")
        else:
            self.auto_scroll_checkbox = QCheckBox("自动滚动")
        self.auto_scroll_checkbox.setChecked(True)
        self.auto_scroll_checkbox.stateChanged.connect(self._toggle_auto_scroll)
        layout.addWidget(self.auto_scroll_checkbox)
        
        # 清空按钮
        self.clear_button.clicked.connect(self._clear_display)
        layout.addWidget(self.clear_button)
        
        layout.addStretch()
        
        return group_box
    
    def _setup_timer(self):
        """设置定时器用于自动刷新"""
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self._auto_refresh)
        self.refresh_timer.setInterval(1000)  # 每秒刷新一次
    
    def _select_file(self):
        """选择日志文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择日志文件", "", "日志文件 (*.log *.txt);;所有文件 (*)"
        )
        if file_path:
            self._load_file(file_path)
    
    def _show_info_bar(self, title: str, content: str, severity: str = "info"):
        """显示信息提示"""
        if not QFLUENT_AVAILABLE:
            # 如果没有qfluentwidgets，只更新状态栏
            self.status_label.setText(f"{title}: {content}")
            return
        
        # 清除之前的信息提示
        for info_bar in self.info_bars:
            info_bar.hide()
        self.info_bars.clear()
        
        # 创建新的信息提示
        if severity == "success":
            info_bar = InfoBar.success(title, content, parent=self)
        elif severity == "warning":
            info_bar = InfoBar.warning(title, content, parent=self)
        elif severity == "error":
            info_bar = InfoBar.error(title, content, parent=self)
        else:
            info_bar = InfoBar.info(title, content, parent=self)
        
        info_bar.duration = 3000  # 3秒后自动消失
        info_bar.position = InfoBarPosition.TOP
        info_bar.show()
        self.info_bars.append(info_bar)
    
    def _load_file(self, file_path: str):
        """加载日志文件"""
        try:
            self.current_file_path = file_path
            self._show_info_bar("加载中", f"正在加载 {os.path.basename(file_path)}", "info")
            
            # 停止之前的文件监视
            if self.file_watcher:
                self.file_watcher.stop()
                self.file_watcher = None
            
            # 读取文件内容
            self._read_file(file_path)
            
            # 启用刷新按钮
            self.refresh_button.setEnabled(True)
            
            # 启动文件监视
            self._start_file_watcher()
            
            # 启动自动刷新
            self.refresh_timer.start()
            
            self.status_label.setText(f"已加载: {os.path.basename(file_path)} ({len(self.log_entries)} 条记录)")
            self._show_info_bar("加载成功", f"成功加载 {len(self.log_entries)} 条日志记录", "success")
            
        except Exception as e:
            self.status_label.setText(f"加载失败: {str(e)}")
            self._show_info_bar("加载失败", str(e), "error")
    
    def _read_file(self, file_path: str):
        """读取日志文件"""
        self.log_entries.clear()
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                
            for line in lines:
                entry = self._parse_log_line(line.strip())
                if entry:
                    self.log_entries.append(entry)
                    
        except Exception as e:
            raise Exception(f"读取文件失败: {str(e)}")
        
        self._apply_filter()
    
    def _parse_log_line(self, line: str) -> Optional[LogEntry]:
        """解析日志行"""
        if not line:
            return None
            
        # 匹配日志格式: 2025-12-07 19:59:54.111 | DEBUG    | main:_get_duration_opencv | Video duration: 9.3663125 seconds
        pattern = r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(?:\.\d+)?)\s*\|\s*(\w+)\s*\|\s*([^\|]+)\s*\|\s*(.*)$'
        match = re.match(pattern, line)
        
        if match:
            timestamp, level, location, message = match.groups()
            return LogEntry(timestamp, level.strip(), location.strip(), message.strip(), line)
        
        # 如果不匹配标准格式，仍然作为日志条目保存
        return LogEntry("", "UNKNOWN", "", line, line)
    
    def _start_file_watcher(self):
        """启动文件监视"""
        if self.current_file_path:
            self.file_watcher = LogFileWatcher(self.current_file_path)
            self.file_watcher.new_lines.connect(self._handle_new_lines)
            self.file_watcher.start()
    
    def _handle_new_lines(self, lines: List[str]):
        """处理新的日志行"""
        for line in lines:
            entry = self._parse_log_line(line.strip())
            if entry:
                self.log_entries.append(entry)
        
        self._apply_filter()
    
    def _filter_logs(self):
        """过滤日志"""
        selected_text = self.level_combo.currentText()
        
        if selected_text == "全部":
            self.selected_levels = set(self.LOG_LEVELS)
        else:
            self.selected_levels = {selected_text}
        
        self._apply_filter()
    
    def _apply_filter(self):
        """应用过滤器"""
        self.filtered_entries = [
            entry for entry in self.log_entries 
            if entry.level in self.selected_levels
        ]
        
        self._update_display()
    
    def _update_display(self):
        """更新显示"""
        self.log_display.clear()
        
        # 设置文本格式
        cursor = self.log_display.textCursor()
        cursor.movePosition(QTextCursor.Start)
        
        for entry in self.filtered_entries:
            # 根据日志级别设置背景颜色
            color = self.LOG_COLORS.get(entry.level, QColor(255, 255, 255))
            
            char_format = QTextCharFormat()
            char_format.setBackground(color)
            
            cursor.setCharFormat(char_format)
            cursor.insertText(entry.raw_line + "\n")
        
        # 自动滚动到底部
        if self.auto_scroll:
            scrollbar = self.log_display.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())
        
        # 更新状态栏
        self.status_label.setText(f"显示 {len(self.filtered_entries)} / {len(self.log_entries)} 条记录")
    
    def _toggle_auto_scroll(self, state: int):
        """切换自动滚动"""
        self.auto_scroll = (state == Qt.Checked)
    
    def _refresh_log(self):
        """手动刷新日志"""
        if self.current_file_path:
            self._read_file(self.current_file_path)
    
    def _auto_refresh(self):
        """自动刷新"""
        if self.current_file_path and os.path.exists(self.current_file_path):
            # 检查文件是否有更新
            try:
                current_size = os.path.getsize(self.current_file_path)
                if not hasattr(self, 'last_file_size'):
                    self.last_file_size = current_size
                
                if current_size != self.last_file_size:
                    self._read_file(self.current_file_path)
                    self.last_file_size = current_size
            except Exception:
                pass
    
    def _clear_display(self):
        """清空显示"""
        self.log_display.clear()
        self.status_label.setText("显示已清空")
    
    def closeEvent(self, event):
        """关闭事件"""
        # 停止文件监视
        if self.file_watcher:
            self.file_watcher.stop()
        
        # 停止定时器
        if self.refresh_timer.isActive():
            self.refresh_timer.stop()
        
        event.accept()


def create_log_viewer() -> LogViewerWindow:
    """创建日志查看器窗口实例"""
    return LogViewerWindow()


def show_log_viewer(file_path: str = None):
    """显示日志查看器
    
    Args:
        file_path: 可选的日志文件路径
    """
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    
    viewer = create_log_viewer()
    
    if file_path and os.path.exists(file_path):
        viewer._load_file(file_path)
    
    viewer.show()
    return app.exec_()


if __name__ == "__main__":
    show_log_viewer()