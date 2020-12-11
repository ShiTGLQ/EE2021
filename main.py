import numpy as np
import sys

from frame import Ui_MainWindow
from random_map import MapGenerator
from astar import AStar
from visualmat import MapVisualizer

from PyQt5.QtWidgets import QApplication,QMainWindow,QGridLayout,QLabel,QLineEdit,QPushButton,QVBoxLayout,QMessageBox
from PyQt5.QtCore import QTimer,Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.Qt import QDialog


    
class MapGUI(QMainWindow,Ui_MainWindow):
    """
    Brief:
    PS:虽然多态继承不太好，但是也不晓得咋改了
    """

    def __init__(self):
        super(MapGUI,self).__init__()
        #初始化地图
        self.map = MapGenerator(height=20,width=20,usecost=False)
        self.astar = AStar(self.map.map)
        self.map_valid = self.astar.planning()
        if not self.map_valid:
            self.map.remap()
            self.astar.set_map(self.map.map)
            self.map_valid = self.astar.planning()
        self.close_set = self.astar.get_closeset()
        self.astar_path = self.astar.traceback()
        self.state_point = self.astar.startpoint.copy()#必须copy，否则会改变startpoint
        self.path_showing = False #是否在显示，False为当前未显示

        self.setupUi(self)
        self.init_widget()
    

    def init_widget(self):
        """
        Brief:
          初始化qt的信号和槽函数\\图表
        Usage:
        """
        self.planbutton.clicked.connect(self.replanning)
        self.remapbutton.clicked.connect(self.remap)
        self.showbutton.clicked.connect(self.show_planning)

        self.upbutton.clicked.connect(self.move_up)
        self.downbutton.clicked.connect(self.move_down)
        self.leftbutton.clicked.connect(self.move_left)
        self.rightbutton.clicked.connect(self.move_right)

        self.init_fig()

    def init_fig(self):
        """
        Brief:
          初始化图表,使用MapVisualizer类
        Usage:
        """
        self.mapfig = MapVisualizer()
        self.mapfig_layout = QGridLayout(self.mapbox)
        self.mapfig_layout.addWidget(self.mapfig)
        self.mapfig.set_map(self.map)
        self.mapfig.draw_basemap()
        self.mapfig.draw_fixed_point(self.astar.startpoint,c='b')
        self.mapfig.draw_fixed_point(self.astar.endpoint,c='r')
        self.mapfig.draw_move_point(self.state_point)

    def show_map(self):
        """
        Brief:
          显示地图
        """
        #self.mapfig.fig.canvas.draw()
        self.mapfig.draw_basemap()
        self.mapfig.draw_fixed_point(self.astar.startpoint,c='b')
        self.mapfig.draw_fixed_point(self.astar.endpoint,c='r')
        self.mapfig.draw_move_point(self.state_point)
        self.mapfig.fig.canvas.draw()

    def replanning(self,*args):
        if self.path_showing:
            self.show_planning()
        self.mapfig.hide_point(self.astar.startpoint)
        self.astar.set_start(self.state_point[0],self.state_point[1])
        self.astar.planning()
        self.close_set = self.astar.get_closeset()
        self.astar_path = self.astar.traceback()
        self.show_planning()
    
    def show_planning(self,*args):
        """
        Brief:
          显示或隐藏路径规划得出的路径
        """
        if self.path_showing:
            self.mapfig.hide_path(self.close_set)
            self.path_showing = False
        else :
            self.mapfig.draw_path(self.close_set,c='c')
            self.mapfig.draw_path(self.astar_path,c='g')
            self.path_showing = True
        self.mapfig.draw_fixed_point(self.astar.startpoint,c='b')
        self.mapfig.draw_fixed_point(self.astar.endpoint,c='r')
        self.mapfig.draw_move_point(self.state_point)

    def move_up(self,*args):
        """
        Brief:
          当前状态格向上(y)方向移动一格并显示
        """
        tmp = self.state_point[1] + 1
        if tmp >=self.map.map_size[2]:
            #如果超过地图范围，什么都不做= 不更新
            pass
        elif np.isinf(self.map.map[0,self.state_point[0],tmp]):
            pass
        else :
            self.state_point[1] = tmp
            self._update_state('w')

    def move_down(self,*args):
        """
        Brief:
          当前状态格向下(y-)方向移动一格并显示
        """
        tmp = self.state_point[1] -1
        if tmp <0:
            #如果超过地图范围，什么都不做= 不更新
            pass
        elif np.isinf(self.map.map[0,self.state_point[0],tmp]):
            pass
        else :
            self.state_point[1] = tmp
            self._update_state('s')

    def move_left(self,*args):
        """
        Brief:
          当前状态格向左(x-)方向移动一格并显示
        """
        tmp = self.state_point[0] - 1
        if tmp <0:
            #如果超过地图范围，什么都不做= 不更新
            pass
        elif np.isinf(self.map.map[0,tmp,self.state_point[1]]):
            pass
        else :
            self.state_point[0] = tmp
            self._update_state('a')

    def move_right(self,*args):
        """
        Brief:
          当前状态格向右(x+)方向移动一格并显示
        """
        tmp = self.state_point[0] + 1
        if tmp >=self.map.map_size[1]:
            #如果超过地图范围，什么都不做= 不更新
            pass
        elif np.isinf(self.map.map[0,tmp,self.state_point[1]]):
            pass
        else :
            self.state_point[0] = tmp
            self._update_state('d')

    def _update_state(self,action:str):
        if action in ['w','a','s','d','W','S','A','D']:
            print("action:",action)
            self.mapfig.update_move_point(self.state_point)
        else :
            return None

    def remap(self,*args):
        self.map.remap()
        self.astar.set_map(self.map.map)
        self.map_valid = self.astar.planning()
        if not self.map_valid:
            self.map.remap()
            self.astar.set_map(self.map.map)
            self.map_valid = self.astar.planning()
        self.close_set = self.astar.get_closeset()
        self.astar_path = self.astar.traceback()
        self.state_point = self.astar.startpoint
        self.path_showing = False
        self.mapfig.ax.cla()
        self.show_map()

    def closeEvent(self,event):
        """
        Brief:
          重写closeEvent事件，关闭窗口时会有提醒
        """
        # 创建一个消息盒子（提示框）
        quitMsgBox = QMessageBox()
        # 设置提示框的标题
        quitMsgBox.setWindowTitle('确认提示')
        # 设置提示框的内容
        quitMsgBox.setText('你确认退出吗？')
        # 设置按钮标准，一个yes一个no
        quitMsgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        # 获取两个按钮并且修改显示文本
        buttonY = quitMsgBox.button(QMessageBox.Yes)
        buttonY.setText('确定')
        buttonN = quitMsgBox.button(QMessageBox.No)
        buttonN.setText('取消')
        quitMsgBox.exec_()
        # 判断返回值，如果点击的是Yes按钮，我们就关闭组件和应用，否则就忽略关闭事件
        if quitMsgBox.clickedButton() == buttonY:
            event.accept()
            #self.SafeExit()
        else:
            event.ignore()


if __name__ == "__main__":
    app=QApplication(sys.argv)
    gui = MapGUI()
    gui.show()
    sys.exit(app.exec_())