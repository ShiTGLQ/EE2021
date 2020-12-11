from random_map import MapGenerator
from astar import AStar

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
import matplotlib
import matplotlib.cbook as cbook

def example():
    mymap = MapGenerator(height=20,width=20,usecost=False)
    plan = AStar(mymap.map)
    plan.planning()
    node_array = plan.traceback()
    closed_array = plan.get_closeset()
    ax = plt.gca()
    ax.set_xlim([0, mymap.height])
    ax.set_ylim([0, mymap.width])
    for i in range(mymap.height): 
        for j in range(mymap.height):
            if mymap.isobstacle(i,j):
                rec = Rectangle((i, j), width=1, height=1, color='gray')
                ax.add_patch(rec)
            else:
                rec = Rectangle((i, j), width=1, height=1, edgecolor='gray', facecolor='w')
                ax.add_patch(rec)

    for i in closed_array:
        rec = Rectangle(i[0:2], width = 1, height = 1, facecolor='c')
        ax.add_patch(rec)

    for i in node_array:
        rec = Rectangle(i[0:2], width = 1, height = 1, facecolor='g')
        ax.add_patch(rec)

    rec = Rectangle(plan.startpoint, width = 1, height = 1, facecolor='b')
    ax.add_patch(rec)

    rec = Rectangle(plan.endpoint, width = 1, height = 1, facecolor='r')
    ax.add_patch(rec)

    ax.fill([11,11,12,12,11],[11,12,12,11,11],c='m')
    plt.axis('equal')
    plt.axis('off')
    plt.tight_layout()

    plt.show()

class MapVisualizer(FigureCanvas):
    def __init__(self,parent=None,width=4,height=4,dpi=100):
        self.fig=Figure(figsize=(width,height),dpi=100)
        #width和height分别定义了画板的宽和高，单位是100（dpi）像素
        super(MapVisualizer,self).__init__(self.fig)
        self.ax=self.fig.add_subplot(111)
        self.ln = None #绘制曲线，默认为None
        #self.fig.canvas.draw()
        #启动动画
    
    def set_map(self,basemap):
        """
        Brief:
          设置代价地图/障碍物地图
        Usage:
        Args:
          map(MapGenerator):3d tensor,MapGenerator类的map属性
          usecost(Bool):False代表绘制障碍物地图
        """
        self.basemap = basemap

    def draw_basemap(self):
        """
        Brief:
          绘制代价地图/障碍物地图
        Usage:
        """
        if self.basemap.usecost:
            self.ax.matshow(self.basemap.map[0])
        else :
            self.ax.set_ylim([0, self.basemap.height])
            self.ax.set_xlim([0, self.basemap.width])
            for i in range(self.basemap.width): 
                for j in range(self.basemap.height):
                    if self.basemap.isobstacle(i,j):
                        rec = Rectangle((i, j), width=1, height=1, color='gray')
                        self.ax.add_patch(rec)
                    else:
                        rec = Rectangle((i, j), width=1, height=1, edgecolor='gray', facecolor='w')
                        self.ax.add_patch(rec)
            self.background = self.fig.canvas.copy_from_bbox(self.ax.bbox)
        self.fig.canvas.draw()#这句要放到绘制完成的最后

    def draw_path(self,path,c='c'):
        """
        Brief:
          绘制路径
        Usage:
        Args:
          path(npl.array):shape = (n,2)的array或者astar规划出的路径
          c(str):颜色，就是matplotlib的c
        """
        #self.fig.canvas.restore_region(self.background)
        for i in path:
            rec = Rectangle(i[0:2], width = 1, height = 1, facecolor=c)
            self.ax.add_patch(rec)
            #self.fig.canvas.blit(self.ax.bbox)
        self.fig.canvas.draw()

    def hide_path(self,path):
        """
        Brief:
          隐藏路径
        Usage:
        Args:
          path(npl.array):shape = (n,2)的array
        """
        self.fig.canvas.draw()
        #self.fig.canvas.restore_region(self.background)
        for i in path:
            rec = Rectangle(i[0:2], width = 1, height = 1,edgecolor='gray', facecolor='w')
            self.ax.add_patch(rec)
            #self.fig.canvas.blit(self.ax.bbox)
        self.fig.canvas.draw()
    def hide_point(self,point):
        """
        Brief:
          隐藏某个点
        Usage:
        Args:
          path(npl.array):shape = (n,2)的array
        """
        self.fig.canvas.draw()
        #self.fig.canvas.restore_region(self.background)
        rec = Rectangle(point, width = 1, height = 1,edgecolor='gray', facecolor='w')
        self.ax.add_patch(rec)
        self.fig.canvas.draw()

    def draw_fixed_point(self,point,c='r'):
        """
        Brief:
          绘制固定点（起点、终点）
        Usage:
        Args:
          point(list/tuple/np.array):shape = (2,)
        """
        rec = Rectangle(point, width = 1, height = 1, facecolor=c)
        self.ax.add_patch(rec)
        self.fig.canvas.draw()

    def draw_move_point(self,point,c='m'):
        """
        Brief:
          绘制移动点初始对应矩形，点为矩形右下角
        Usage:
        Args:
          point(list/tuple/np.array):shape = (2,)
        """
        x = point[0]
        y = point[1]
        ln, = self.ax.plot([x,x,x+1,x+1,x],[y,y+1,y+1,y,y],c=c)
        self.ln = ln

    def update_move_point(self,point,c='m'):
        """
        Brief:
          更新移动点初始对应矩形，点为矩形右下角
        Usage:
        Args:
          point(list/np.array):shape = (2,)
        """
        if self.ln is None :
            self.draw_move_point(point,c=c)
        else :
            x = point[0]
            y = point[1]
            self.ln.set_xdata([x,x,x+1,x+1,x])
            self.ln.set_ydata([y,y+1,y+1,y,y])
            self.ax.draw_artist(self.ln)
            self.fig.canvas.blit(self.ax.bbox)

       


if __name__ == "__main__":
    example()