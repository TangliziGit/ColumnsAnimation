# ColumnsAnimation
Imitates "Jannchie / Historical-ranking-data-visualization-based-on-d3.js "  

a visualization tool, imitates [Jannchie/Historical-ranking-data-visualization-based-on-d3.js](https://github.com/Jannchie/Historical-ranking-data-visualization-based-on-d3.js) almost entirely.  

## Getting Started

### How to run?

Just open `animation.html` in your broswer.

### How to use custom data?

Replace the `data.js` with your data, in a JSON structure like this:
```
var TotalData=[
    {"name": "xxx", "value": "1234", "date": 2019},
    ...
]
```

## the Main Idea

### 前言
首先感谢原作者Jannchie <https://github.com/Jannchie/>  
以及原项目[Historical-ranking-data-visualization-based-on-d3.js](https://github.com/Jannchie/Historical-ranking-data-visualization-based-on-d3.js)  

写这个东西是因为学校某项目的一个练手题目选定了这个  
那我为啥要写前端呢？因为前端那位，我好像联系不到：）  
没办法时间挺紧的，这小项目就我一人写了  
几乎所有的代码都是来自原项目的，考虑到整个项目可能不断需要魔改动态可视化，于是就另开了这个新repo  
期待这个repo以后的变化吧  

顺便写了这个随笔，本意是给自己前端看的，但今天有位同学问优化问题，所以就写的详细点了  

### 模块组织
简单的html+js+css，其中html和css没什么要说的，简单提一下  
1. **HTML部分**
主要引用js和css文件  
有一个地方需要注意一下，就是窗口宽度问题  
```html
<meta name="viewport" content="width=device-width">
```
2. **CSS部分**
设置颜色类：这个点子非常好，可以方便的修改颜色数据  
设置各种元素宽度，文字描边和坐标样式：这里有个问题，如果SVG变宽高，这里的各种元素宽度就会略有问题  

3. **JavaScript部分**
动态可视化核心代码，主要就是标签的组织和更新  
首先讲清楚**SVG内部标签构造，和动态更新的原理**  
运行代码可以简化分析SVG内部标签的设置  

**SVG内部标签**
```
g group标签包含其他所有svg标签
    g x轴（由d3生成）
        text x轴标签（d3生成）
        path x轴（d3生成）
        g*n n个时间竖线(英文是Tick不知道怎么翻译)
            line 竖线
            text x轴数字
    g 这个组不知道干嘛的，可能是y轴，以后考虑去掉？
    text 这个是timer，改源代码时忘记留下来了，最后自己加上的
    g*n n个bar，这是动态的主题
        g 这是标记颜色的，好像没用？
        rect 这是柱子，只有颜色类
        text y轴上的柱后文字，label类颜色类
        text 柱前数字，value类颜色类
        text 柱上文字，barInfo类
```
**动态更新原理**
就是不断的绑定新数据：  
在Enter里初始化新数据  
在upate里更新新元素  
在exit下删除旧元素  
关键在于d3提供了按索引绑定数据的方法，这样的操作才得以简单进行，详细说明在下面  

### 细节问题
1. 利用setInterval()来控制整个时间变化  
首先输入数据data，按时间push到date数组里  
再定义一个iter，同于控制总时间  

2. 获得颜色类
作者使用了一个简单的hash函数，做了一个name到hash值的映射，然取模color.length()取得颜色类  
$$
Hash(name)=\sum name[i]
$$

2. 获取当前时间下的数据
这里原作者是枚举data数组，返回对应时间下的数据（修改的代码中顺便维护了Timer）  
有一个同学也是写了这个项目，但总是有卡顿(win10)，那么我们顺便讲一下优化  
其实这里可以二分达到O(logn)，但首先需要预处理数据排序O(nlogn)，其次我们设置了MaxNumber用来控制显示柱子的数量，就是说这里还能优化  
最好的方法是在后端处理好数据(排序+切片)后传给前端，这种一劳永逸的方式何乐而不为  

3. 刷新图表
这里是核心部分，我们拆开来看  
注意作者将interval间隔时间分成了三份( interval/=3 )  

- 首先维护yScale, xScale, xAxisG, yAxisG和Timer  
原作者在初始化刻度尺时并没有给出domain, range这是很让人舒服的地方，非常优雅  
设置坐标系的更新动画，注意还要添加.call(xAxis)，顺便删除原有tick  
维护Timer，这里有两个要点。其一、在第一次显示Timer时停顿。其二、数字的过度动画d3中没有直接的实现，只能是用tween调d3.interpolate自己写  

- 绑定bar的数据
注意.data(data, [key])中的key是每个元素的键值，对应原有元素的键值进行更新。如果没有设置的话就从头到尾覆盖  

- Enter元素的过渡动画
在绑定了数据后，按道理所有元素的数据都是当前时间下最新数据。  
Enter部分指新加入数据，这里应该是带有新键值的数据。  
这里的更新就像是初始化。  
注意设置以下属性：  
transform, x, y, width, height, fill-opacity, class（带有颜色类）, text, stroke-width  

- Update元素的过渡动画
Update元素就是数据被更新的元素，这里的过渡动画的属性就很少，因为一些属性不需要变化（比如颜色类）  

- Exit元素的过渡动画
Exit元素就是上一次时间的数据，在当前时间的数据中没有出现的元素。  
这里的过渡动画就更简单了，过渡里直接remove()，设置fill-opacity为0即可  

- 更新y坐标
最后我们更新每个bar元素的y坐标即可，这里使用了一开始设置的yScale  

### 效果图
![](https://images2018.cnblogs.com/blog/1225237/201808/1225237-20180801223635843-931453791.png)
