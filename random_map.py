import numpy as np


class MapGenerator(object):
    def __init__(self,depth=1,height=20,width=20,usecost= True):
        '''
        Brief:
          生成一个(depth,height,weight)大小的地图
          depth = 1,则不考虑矢量场的移动代价，只有固定移动代价
        Args:
          usecost(bool):是否使用移动代价
        '''
        self.usecost = usecost
        self.width = width
        self.height = height
        if self.usecost:
            self.depth = depth
            self.map_size = (depth,height,width)
            self.map = np.zeros(self.map_size)#初始化地图
            self.map[0,:,:] = np.random.randint(0,10,size=(self.width,self.height))#设置固定移动代价地图
        else:
            self.map_size = (1,height,width)
            self.map = np.ones(self.map_size)#初始化地图
        self.num_obstacles = self.height*self.width//12 #障碍物数目
        self.obstacles_generate()

    def obstacles_generate(self):
        """
        Brief:
          障碍物生成
        """
        self.map[0,self.height//2,self.width//2] = np.inf
        self.map[0,self.height//2,self.width//2-1] = np.inf

        #生成中间障碍物
        for i in range(self.height//2-4, self.height//2):
            self.map[0,i,self.width-i] = np.inf
            self.map[0,i,self.width-i-1] = np.inf
            self.map[0,self.width-i,i] = np.inf
            self.map[0,self.width-i,i-1] = np.inf
        #生成其他障碍
        for i in range(self.num_obstacles-1):
            x = np.random.randint(0, self.width)
            y = np.random.randint(0, self.height)
            self.map[0,x,y] = np.inf

            if (np.random.rand() > 0.5): # Random boolean ⑥
                for l in range(self.height//4):
                    try:
                        self.map[0,x,y+l] = np.inf
                    except IndexError:
                        #如果越界就退出
                        break
            else:
                for l in range(self.width//4):
                    try:
                        self.map[0,x+l,y] = np.inf
                    except IndexError :
                        break
    
                    
    def isobstacle(self,x,y):
        if np.isinf(self.map[0,x,y]):
            return True
        else:
            return False

    def printmap(self):
        print(self.map)

    def remap(self):
        if self.usecost:
            self.map = np.zeros(self.map_size)#初始化地图
            self.map[0,:,:] = np.random.randint(0,10,size=(self.width,self.height))#设置固定移动代价地图
        else:
            self.map = np.ones(self.map_size)#初始化地图
        self.num_obstacles = self.height*self.width//24 #障碍物数目
        self.obstacles_generate()

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    map = MapGenerator(height=20,width=20,usecost=False)
    map.printmap()
    isinf_mask = np.isinf(map.map[0])
    thre_map = map.map[0]*[isinf_mask]
    thre_map = np.reshape(thre_map,(20,20))
    #print(thre_map.shape)
    thre_map[isinf_mask] = 1
    plt.matshow(map.map[0],cmap=plt.cm.Blues)
    plt.show()



