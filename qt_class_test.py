import sys
import random
import matplotlib

matplotlib.use("Qt5Agg")
from PyQt5.QtWidgets import QApplication
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QLineEdit, QComboBox, QHBoxLayout, QWidget, QTextEdit
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np


class MyMplCanvas(FigureCanvas):

    def __init__(self, parent=None):

        # 配置中文显示
        plt.rcParams['font.family'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

        self.fig = Figure()  # 新建一个figure
        self.axes = self.fig.add_subplot(111)  # 建立一个子图，如果要建立复合图，可以在这里修改

        self.row = 10
        self.col = 10

        self.b = np.zeros((self.row, self.col))

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

    def start_static_plot(self):
        self.axes.imshow(self.b, cmap='Blues', interpolation='none', vmin=0, vmax=1, aspect='equal')
        x, y = np.meshgrid(np.arange(self.b.shape[1]), np.arange(self.b.shape[1]))
        grid = np.ones((self.row, self.col))
        m = np.c_[x[grid.astype(bool)], y[grid.astype(bool)]]

        def rect(pos):
            r = plt.Rectangle(pos - 0.5, 1, 1, facecolor="none", edgecolor="k", linewidth=2)
            self.axes.add_patch(r)

        for pos in m:
            rect(pos)


class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)
        self.initUi()

    def initUi(self):
        self.canvas = MyMplCanvas(self)
        self.canvas.start_static_plot()  # 初始化的时候就呈现静态图

        self.pos_edit = QLineEdit("")
        self.pos_edit.setPlaceholderText("输入位置 如：3 0")

        self.button_cacul = QPushButton("输入")
        self.button_clear = QPushButton("清空")
        self.textEdit = QTextEdit()

        self.type_cb = QComboBox()   # 类型选择框
        self.type_cb.addItem("1-1")
        self.type_cb.addItem("1-2")
        self.type_cb.addItem("2-1")
        self.type_cb.addItem("2-2")
        self.type_cb.addItem("2-3")
        self.type_cb.addItem("2-4")
        self.type_cb.addItem("3-1")
        self.type_cb.addItem("3-2")
        self.type_cb.addItem("3-3")
        self.type_cb.addItem("3-4")
        self.type_cb.addItem("4-1")

        # 连接事件
        self.button_cacul.clicked.connect(self.Caculate)
        self.button_clear.clicked.connect(self.Clear)

        # 设置布局
        wlayout = QHBoxLayout()  # 全局布局
        vlayout1 = QVBoxLayout()  # 局部布局
        vlayout2 = QVBoxLayout()

        wg1 = QWidget()  # 控件，设置局部布局
        wg2 = QWidget()
        vlayout1.addWidget(self.canvas)
        vlayout2.addStretch(1)
        vlayout2.addWidget(self.type_cb)
        vlayout2.addStretch(1)
        vlayout2.addWidget(self.pos_edit)
        vlayout2.addStretch(1)
        vlayout2.addWidget(self.button_cacul)
        vlayout2.addWidget(self.button_clear)
        vlayout2.addStretch(1)
        vlayout2.addWidget(self.textEdit)

        wg1.setLayout(vlayout1)
        wg2.setLayout(vlayout2)
        wlayout.addWidget(wg1)  # 控件添加到全局布局
        wlayout.addWidget(wg2)
        self.setLayout(wlayout)


    def Caculate(self):
        pass

    def Clear(self):
        self.canvas.b = np.zeros((self.canvas.row, self.canvas.col))
        self.textEdit.setPlainText(" ")
        self.canvas.start_static_plot()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MatplotlibWidget()
    # ui.mpl.start_static_plot()  # 测试静态图效果
    ui.show()
    sys.exit(app.exec_())
