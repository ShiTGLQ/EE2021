import numpy as np
import math
import random
import random_map

class AStar(object):
    def __init__(self,map:np.array,direction="4"):
        """
        Brief:
          Astar算法初始化
        Args:
          map(np.array):是由mapgennerator生成的地图，其为一个3d tensor
            具体看map类去
          direction(str):"4"为只有四个方向,"8"为全向
        """
        if direction not in ["4","8"]:
            print("direction(str):'4'为只有四个方向,'8'为全向")
            raise ValueError
        self.direction = direction
        self.open_set = []
        self.close_set = []
        self.map = map
        self.mapsize = map.shape
        self.startpoint = np.array([0,0])
        while self.isobstacle(*self.startpoint):
            self.startpoint = np.random.randint(0,np.min(self.mapsize[1:])-1,size=(2,))
        self.endpoint = np.array([self.mapsize[1]-1,self.mapsize[2]-1])
        while self.isobstacle(*self.endpoint):
            self.endpoint = np.random.randint(0,np.min(self.mapsize[1:])-1,size=(2,))
        self.avgcost = None #地图平均代价
        self.getmeancost()

    def set_start(self,x,y):
        """
        Brief:
          设置起点
        Usage:
        """
        if x<0 or y<0:
            print("索引不得小于0")
        elif (x>=self.mapsize[1] or y>=self.mapsize[2]):
            print("超过地图尺寸({},{})".format(self.mapsize[1],self.mapsize[2]))
        else :
            self.startpoint = np.array([x,y])
        return None
        
    def set_end(self,x,y):
        """
        Brief:
          设置终点
        Usage:
        """
        if x<0 or y<0:
            print("索引不得小于0")
        elif (x>=self.mapsize[1] or y>=self.mapsize[2]):
            print("超过地图尺寸({},{})".format(self.mapsize[1],self.mapsize[2]))
        else :
            self.endpoint = np.array([x,y])
        return None

    def compute_f(self,parent_node,child_node):
        """
        Brief:
          计算f，f = g+h
        Usage:
        Args:
          parent_node(list):[x,y,dx,dy,g,f],dx,dy起到记录父节点的功能
        """
        f_value = self.compute_g(parent_node,child_node)+self.compute_h(child_node)
        return f_value

    def compute_g(self,parent_node,child_node):
        """
        Brief:
          计算g,使用递推
        Usage:
        Args:
          parent(list):[x,y,dx,dy,g,f],dx,dy起到记录父节点的功能
        """
        dx = parent_node[0] - child_node[0]
        dy = parent_node[1] - child_node[1]
        default_cost = self.map[0,parent_node[0],parent_node[1]]
        #穿越父节点的cost代价
        g = default_cost*np.sqrt(dx**2+dy**2)+parent_node[4]
        return g

    def compute_h(self,node):
        """
        Brief:
          计算f，f = g+h
        Usage:
        Args:
          node(list):[x,y,dx,dy,g,f],dx,dy起到记录父节点的功能
        """
        dx = (node[0] - self.endpoint[0])**2
        dy = (node[1] - self.endpoint[1])**2
        if self.avgcost is None:
            self.getmeancost()
        h = self.avgcost*math.sqrt(dx + dy)
        return h

    def getmeancost(self):
        """
        Brief:
          获取地图的平均代价，用于计算h
        """
        noinf_mask = ~np.isinf(self.map)#获取非无穷索引
        self.avgcost = noinf_mask.mean()
        return self.avgcost

    def judge_location(self,node,list_co):
        """
        Brief:
          判断节点是否属于openlist或者closedlist
        Usage:
        Args:
          node(list):[x,y,dx,dy,g,f]
          list_co(list):(n,6)的array，行为每个node的参数
        Returns:
          jud(bool):是否在其中，是为true
          index(int):
        """
        jud = False
        index = 0
        num = len(list_co)
        for i in range(num):
            if (node[0] ==list_co[i][0] and node[1] ==list_co[i][1]):
                jud = True
                index = i
                break
        return jud,index

    def expand_node(self,node):
        """
        Brief:
          根据当前节点扩充搜索，找到f最小的子节点
        Usage:
        Args:
          node(np.array):[x,y,dx,dy,g,f],父节点
        Returns:
        """
        for j in range(-1,2):
            for q in range(-1,2):
                if j==0 and q==0:
                    #如果是自己就跳了
                    continue
                elif (node[0]+j < 0 or node[0]+j >self.mapsize[1]-1):
                    continue
                elif (node[1]+q < 0 or node[1]+q >self.mapsize[2]-1):
                    continue
                elif np.isinf(self.map[0,node[0]+j,node[1]+q]):
                    continue
                if self.direction=="4" and (j+q)%2==0:
                    continue
                tmp_node =[node[0]+j,node[1]+q,j,q,0,0]
                #print("tmp_node{}".format(tmp_node))
                a,index1 = self.judge_location(tmp_node,self.close_set)
                if a:
                    #如果在closeset中
                    continue
                tmp_g = self.compute_g(node,tmp_node)
                tmp_f = self.compute_f(node,tmp_node)
                tmp_node[4] = tmp_g
                tmp_node[5] = tmp_f

                a,index1 = self.judge_location(tmp_node,self.open_set)
                if a:
                    #如果在openset中，那么比较openset中的f和当前f，取最小
                    self.open_set[index1][5] = tmp_f
                    self.open_set[index1][4] = tmp_g
                    self.open_set[index1][3] = tmp_node[3]
                    self.open_set[index1][2] = tmp_node[2]

                else :
                    self.open_set.append(tmp_node)
                #print("tmp_node{}".format(tmp_node))
    
    def planning(self,startpoint=None,endpoint=None):
        """
        Brief:
        Usage:
        Args:
          startpoint(tuple):如果不指定，那么默认用初始化的，即地图左上角
        Returns
          bool:
        """
        #方便重新规划
        self.close_set = []
        self.open_set = []
        if startpoint is not None:
            self.set_start(*startpoint)
        if endpoint is not None:
            self.set_end(*endpoint)
        best = self.startpoint
        init_node = [best[0],best[1],0,0,0,0]
        h0 = self.compute_h(init_node)
        init_node[-1] = h0
        self.open_set.append(init_node)
        ite = 1#设置最大迭代次数，防止无限循环
        while ite <= 1000:
            if len(self.open_set)==0:
                print("planning failed")
                return False
            tmp_array = np.array(self.open_set)
            best_index = tmp_array.argmin(0)[-1]
            #找到f最小对应的索引
            best = self.open_set[best_index]
            #print('检验第%s次当前点坐标*******************' % ite)
            #print(best)
            self.close_set.append(best)
            if best[0] ==self.endpoint[0] and best[1] ==self.endpoint[1]:
                print("搜索成功")
                return True
            
            self.expand_node(best)
            del(self.open_set[best_index])
            
            #print("openset",self.open_set)
            ite +=1

    def traceback(self):
        """
        Brief:
        Usage:
        """
        best_path = [self.endpoint[0],self.endpoint[1]]
        node_path =[]
        node_path.append([self.endpoint[0],self.endpoint[1]])
        j = 0
        node_num = len(self.close_set)
        #for i in range(node_num):
        #    print(self.close_set[i])
        while j < node_num:
            for i in range(node_num):
                if best_path[0] ==self.close_set[i][0] and best_path[1] ==self.close_set[i][1]:
                    x = self.close_set[i][0] -self.close_set[i][2]
                    y = self.close_set[i][1] - self.close_set[i][3]
                    best_path = [x,y]
                    node_path.append(best_path)
                    break
            if best_path[0] ==self.startpoint[0] and self.startpoint[1]==best_path[1]:
                break
            j +=1
            #print("best_node",best_path)
        return np.array(node_path)
      
    def get_closeset(self):
        return np.array(self.close_set)
    
    def isobstacle(self,x,y):
        if np.isinf(self.map[0,x,y]):
            return True
        else:
            return False
        
    def set_map(self,map:np.array,direction="4"):
        """
        Brief:
          重新设置地图并初始化
        Usage:
        """
        if direction not in ["4","8"]:
            print("direction(str):'4'为只有四个方向,'8'为全向")
            raise ValueError
        self.direction = direction
        self.open_set = []
        self.close_set = []
        self.map = map
        self.mapsize = map.shape
        self.startpoint = np.array([0,0])
        while self.isobstacle(*self.startpoint):
            self.startpoint = np.random.randint(0,np.min(self.mapsize[1:])-1,size=(2,))
        self.endpoint = np.array([self.mapsize[1]-1,self.mapsize[2]-1])
        while self.isobstacle(*self.endpoint):
            self.endpoint = np.random.randint(0,np.min(self.mapsize[1:])-1,size=(2,))
        self.avgcost = None #地图平均代价
        self.getmeancost()

              
if __name__ == "__main__":
    mymap = random_map.MapGenerator(height=20,width=20,usecost=False)
    print(mymap.map.shape)
    plan = AStar(mymap.map)
    plan.planning()
    plan.traceback()