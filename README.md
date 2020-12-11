# README

### author:GL

## requirement

代码在以下环境中测试通过

1. Python3.7
2. numpy1.1.8
3. matplotlib
4. PyQt5
5. anaconda(optional)

## 文件目录

```
|-README.md :说明文件
|-1190102008-*.doc :大作业报告
|-/src :源文件存放目录
|----astar.py：A*路径规划算法实现类存放的文件，可以直接调用
|----frame.py:qt转换出的类文件
|----main.py：主要实现GUI和交互的文件
|----random_map.py：随机地图生成类，直接调用会使用Matplotlib做可视化
|----visualmat.py：地图可视化，直接调用会显示路径规划的sample
|----planning.ui:使用QtDesigner设计的.ui文件，frame.py为planning.ui使用pyrcc转换的文件
|-/pic ：图片目录
```

## 说明：

不想写了