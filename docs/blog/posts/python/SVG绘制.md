---
title: SVG绘制
date: 2024-04-05
categories:
  - windows程序
tags:
  - SVG
  - 矢量图形
  - 图形绘制
  - Web开发
description: SVG矢量图形的基础绘制教程，包含各种基本图形元素的使用方法
author: JerryMa
---

# SVG绘制

## 基础绘制

### 绘制一个字母

```xml
<svg
  width="64"
  height="64"
  xmlns="http://www.w3.org/2000/svg"
>
  <rect
    width="100%"
    height="100%"
    fill="#424c58"
  />
  <text
    x="32"
    y="38"
    font-family="Arial"
    font-size="70"
    text-anchor="middle"
    dominant-baseline="middle"
    fill="yellow"
  >
    S
  </text>
</svg>
```

![image-20241031140756164](http://image.jerryma.xyz//images/20241031-image-20241031140756164.png)

## SVG基本图形绘制教程

###  矩形 `<rect>`

矩形是[SVG](https://so.csdn.net/so/search?q=SVG&spm=1001.2101.3001.7020)中最基本的图形之一。通过`<rect>`元素可以绘制矩形和正方形。

**参数:**

- `x` 和 `y`：定义矩形左上角的坐标。
- `width` 和 `height`：定义矩形的宽度和高度。
- `rx` 和 `ry`：定义矩形边角的圆滑程度。

**代码示例:**

```xml
<svg width="100" height="100"  xmlns="http://www.w3.org/2000/svg">
  <!-- 简单的矩形 -->
  <rect x="10" y="10" width="30" height="30" fill="blue"/>

  <!-- 圆角矩形 -->
  <rect x="50" y="10" width="30" height="30" rx="5" ry="5" fill="aqua"/>
</svg>
```

![image-20241031141056901](http://image.jerryma.xyz//images/20241031-image-20241031141056901.png)

**说明:**

- 第一个`<rect>`元素绘制了一个简单的矩形。
- 第二个`<rect>`元素绘制了一个圆角矩形，`rx` 和 `ry` 参数使得角变得圆滑。

###  圆形 `<circle>`

圆形通过`<circle>`元素来绘制。

**参数:**

- `cx` 和 `cy`：定义圆心的坐标。
- `r`：定义圆的半径。

**代码示例:**

```xml
<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="40" fill="red"/>
</svg>
```

![image-20241031141300550](http://image.jerryma.xyz//images/20241031-image-20241031141300550.png)

**说明:**

- `cx` 和 `cy` 参数定义了圆心在SVG画布上的位置，`r` 参数定义了圆的大小。

### 椭圆 `<ellipse>`

椭圆通过`<ellipse>`元素来绘制。

**参数:**

- `cx` 和 `cy`：定义椭圆中心的坐标。
- `rx` 和 `ry`：定义椭圆的主半径和次半径。

**代码示例:**

```xml
<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="50" cy="50" rx="30" ry="20" fill="lightblue"/>
</svg>
```

![image-20241031141406068](http://image.jerryma.xyz//images/20241031-image-20241031141406068.png)

**说明:**

- `rx` 和 `ry` 参数定义了椭圆的形状，其中`rx`是水平半径，`ry`是垂直半径。

###  线 `<line>`

直线通过`<line>`元素来绘制。

**参数:**

- `x1` 和 `y1`：定义线的起点坐标。
- `x2` 和 `y2`：定义线的终点坐标。

**代码示例:**

```xml
<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">
  <line x1="10" y1="10" x2="90" y2="90" stroke="#23e723" />
</svg>
```

![image-20241031141500004](http://image.jerryma.xyz//images/20241031-image-20241031141500004.png)

**说明:**

- `stroke` 属性定义了线的颜色。

###  多边形 `<polygon>`

多边形通过`<polygon>`元素来绘制。

**参数:**

- `points`：定义多边形每个顶点的坐标。

**代码示例:**

```xml
<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">
  <polygon points="50,10 90,90 10,90" fill="aliceblue"/>
</svg>
```

![image-20241031141546615](http://image.jerryma.xyz//images/20241031-image-20241031141546615.png)

**说明:**

- `points` 参数是一系列坐标，用空格分隔，定义了多边形的形状。

###  折线 `<polyline>`

折线通过`<polyline>`元素来绘制。

**参数:**

- `points`：定义折线每个拐点的坐标。

**代码示例:**

```xml
<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">
  <polyline points="10,10 50,50 90,10" stroke="green" fill="yellow" />
</svg>
```

![image-20241031141642150](C:/Users/localuser/AppData/Roaming/Typora/typora-user-images/image-20241031141642150.png)

**说明:**

- `fill="none"` 确保折线中间不被填充颜色。

## [SVG Path高级教程](https://www.cnblogs.com/lovesong/p/5982900.html)

### **Path概述**

<path> 标签用来定义路径，Path字符串是由命令及其参数组组成的字符串，是非常强大的绘图工具。

**例如：**

```
<path  d="M0,0L10,20C30-10,40,20,100,100" stroke="red">
```

**命令汇总**

| 命令                      | 含义                                       |
| ------------------------- | ------------------------------------------ |
| M/m (x,y)                 | 移动当前位置                               |
| L/l (x,y)                 | 从当前位置绘制线段到指定位置               |
| H/h (x)                   | 从当前位置绘制水平线到达指定的 x 坐标      |
| V/v (y)                   | 从当前位置绘制竖直线到达指定的 y 坐标      |
| Z/z                       | 闭合当前路径                               |
| C/c (x1,y1,x2,y2,x,y)     | 从当前位置绘制三次贝塞尔曲线到指定位置     |
| S/s (x2,y2,x,y)           | 从当前位置光滑绘制三次贝塞尔曲线到指定位置 |
| Q/q (x1,y1,x,y)           | 从当前位置绘制二次贝塞尔曲线到指定位置     |
| T/t (x,y)                 | 从当前位置光滑绘制二次贝塞尔曲线到指定位置 |
| A/a (rx,ry,xr,laf,sf,x,y) | 从当前位置绘制弧线到指定位置               |

**命令基本规律**

1. 参数之间可以用空格或逗号隔开，如果下一个数值是负数，才可以省略。

2. 区分大小写：大写表示坐标参数为绝对位置，小写则为相对位置 。

3. 最后的参数表示最终要到达的位置 。

4. 上一个命令结束的位置就是下一个命令开始的位置 。

5. 命令可以重复参数表示重复执行同一条命令。

### **移动和直线命令**

M  (x,  y)： 移动画笔，后面如果有重复参数，会当做是  L  命令处理 。

L  (x,  y)：  绘制直线到指定位置 。

H  (x)： 绘制水平线到指定的  x  位置 。

V  (y)： 绘制竖直线到指定的  y  位置 。

m、l、h、v  使用相对位置绘制。

PS：绝对位置是相对原始坐标系来讲的，相对位置是相对于上一个命名的结束位置。

**例子：**

```
<path d="M40,40L100,100H200V300" stroke="red" fill="none"/>
<path d="M40,40l60,60h100v200" stroke="red" fill="none"/>
```

这两条路径的效果是一样的：

![img](http://image.jerryma.xyz//images/20241031-555379-20161020221828388-1296345544.png)

PS：这里看到1width的斜线，也就是最前面那一段，它的宽度看起来要细一些。

### **弧线命令**

弧线命令是用A  (rx,  ry,  xr,  laf,  sf,  x,  y) 绘制，这里弧线也就是某一个圆弧的一段。

![img](http://image.jerryma.xyz//images/20241031-555379-20161020221849513-1309696573.png)

**参数**

| 参数  | 描述                                          | 取值                  |
| ----- | --------------------------------------------- | --------------------- |
| rx    | （radius-x）弧线所在椭圆的  x  半轴长         |                       |
| ry    | （radius-y）弧线所在椭圆的  y  半轴长         |                       |
| xr    | （xAxis-rotation）弧线所在椭圆的长轴角度      |                       |
| laf   | （large-arc-flag）是否选择弧长较长的那一段弧  | 1 为大弧 0 为小弧     |
| sf    | （sweep-flag）是否选择逆时针方向的那一段弧    | 1 为顺时针 0 为逆时针 |
| x,  y | 弧的终点位置                                  |                       |

laf、sf取值效果：

![img](http://image.jerryma.xyz//images/20241031-555379-20161020221855810-2040391662.png)

**例子：**

```
<path d="M40,40A100 50 0 0 0 100 100" stroke="red" fill="none"/>
```

**效果：**

![image-20241031142059941](http://image.jerryma.xyz//images/20241031-image-20241031142059941.png)

### **贝塞尔曲线** 

在大学时候，接触贝塞尔曲线是在图形学的课程，不过由于比较久远，数学的概念记不清了。（哈哈哈哈）

**贝塞尔曲线概念**

Bézier curve(贝塞尔曲线)是应用于二维图形应用程序的数学曲线。 曲线定义：起始点、终止点、控制点。通过调整控制点，贝塞尔曲线的形状会发生变化。

数学上的计算公式，B(t)为t时间下点的坐标，P0为起点， Pn为终点，Pi为控制点。

一次贝塞尔曲线(线段)：

![img](http://image.jerryma.xyz//images/20241031-555379-20161020221916967-50792042.jpeg)

二次贝塞尔曲线(抛物线)：

![img](http://image.jerryma.xyz//images/20241031-555379-20161020221923107-519354869.jpeg)

三次贝塞尔曲线：

![img](http://image.jerryma.xyz//images/20241031-555379-20161020221928920-264555541.jpeg)

高次贝塞尔曲线（通项公式）：

![img](http://image.jerryma.xyz//images/20241031-555379-20161020221934779-2085659752.jpeg)

PS：计算公式可以让我们直接算出一条贝塞尔曲线。

网上有很多资料介绍贝塞尔曲线是通过下面动图的，当然是基于上面的数学公式，例如下面的三次贝塞尔曲线。

![img](https://images2015.cnblogs.com/blog/555379/201610/555379-20161020221956310-583168424.gif)

**四条贝塞尔曲线命令**

SVG中，只能绘制二次和三次贝塞尔曲线。

| C/c (x1,y1,x2,y2,x,y) | 从当前位置绘制三次贝塞尔曲线到指定位置x1,y1,x2,y2是控制点x,y是终止点 |
| --------------------- | ------------------------------------------------------------ |
| Q/q (x1,y1,x,y)       | 从当前位置绘制二次贝塞尔曲线到指定位置x1,y1是控制点x,y是终止点 |

例子：

```
<path d="M200,400Q300 250 400 400" stroke="red" fill="none"/>
<path d="M200,200C250 100 400 100 400 200" stroke="red" fill="none"/>
```

效果：

![img](http://image.jerryma.xyz//images/20241031-555379-20161020222007076-1957895731.png)

T和S命令中的控制点是来自上一段曲线控制点的镜像位置作为一个控制点。

T: 上一段曲线的控制点关于当前曲线起始点的镜像位置形成当前曲线的控制点。 （这里说的都是二次贝塞尔曲线）

S: 上一段曲线的第二个控制点关于当前曲线起始点的镜像位置形成当前曲线的第一个控制点。

![img](http://image.jerryma.xyz//images/20241031-555379-20161020222020685-152976015.png)

好处：

1. 可以简化写法，少写一个点。

2. 两条曲线形成的曲线是光滑曲线。（当曲线上每一点处都具有切线，且切线随切点的移动而连续转动，这样的曲线成为光滑曲线）

例子：

```
<path d="M100,200C100,100 250,100 250,200S400,300 400,200" stroke="red" fill="none"/>
<path d="M100,400Q150,300 250,400 T400,400" stroke="red" fill="none"/> 
```

效果：

![img](http://image.jerryma.xyz//images/20241031-555379-20161020222028076-1617173409.png) 

## 部分demo

`zoomMinus.svg`

```xml
<svg
    xmlns="http://www.w3.org/2000/svg"
    width="64"
    height="64"
>
    <rect
        width="100%"
        height="100%"
        fill="#424C58"
    />
    <path
        d="M 32 16 C 23.164 16 16 23.164 16 32 C 16 40.836 23.164 48 32 48 C 40.836 48 48 40.836 48 32 C 48 23.164 40.836 16 32 16 Z"
        fill="none"
        stroke-width="2"
        stroke="#5FBCFE"
    />
    <path
        d="M43.315 43.315L 64 64"
        fill="none"
        stroke-width="2"
        stroke="#5FBCFE"
    />
    <path
        d="M 24 32 L 40 32 "
        stroke-width="2"
        stroke="#5FBCFE"
    />
</svg>
```

![image-20241101114447565](http://image.jerryma.xyz//images/20241101-image-20241101114447565.png)![image-20241101114645290](http://image.jerryma.xyz//images/20241101-image-20241101114645290.png)![image-20241101114535803](http://image.jerryma.xyz//images/20241101-image-20241101114605336.png)![image-20241101114554793](http://image.jerryma.xyz//images/20241101-image-20241101114554793.png)

`zoomplus.svg`

```xml
<svg
    xmlns="http://www.w3.org/2000/svg"
    width="64"
    height="64"
>
    <rect
        width="100%"
        height="100%"
        fill="#424C58"
    />
    <path
        d="M 32 16 C 23.164 16 16 23.164 16 32 C 16 40.836 23.164 48 32 48 C 40.836 48 48 40.836 48 32 C 48 23.164 40.836 16 32 16 Z"
        fill="none"
        stroke-width="2"
        stroke="#5FBCFE"
    />
    <path d="M43.315 43.315L 64 64" fill="none" stroke-width="4" stroke="#5FBCFE" />
    <path
        d="M 24 32 L 40 32 M 32 24 L 32 40"
        stroke-width="4"
        stroke="#5FBCFE"
    />
</svg>
```

`open.svg`

```xml
<svg
    xmlns="http://www.w3.org/2000/svg"
    width="64"
    height="64"
>
    <rect
        width="100%"
        height="100%"
        fill="#424C58"
    />
    <path
        d="M0,48L0,0L64,0L64,48"
        stroke="#5FBCFE"
        fill="none"
        stroke-width="5"
    />
    <path
        d="M0,48L32,48"
        stroke="#5FBCFE"
        fill="none"
        stroke-width="2.5"
    />
    <path
        d="M40,48L56,48 M48,40L48,56"
        stroke="#5FBCFE"
        fill="none"
        stroke-width="5"
    />
</svg>
```

`new.svg`

```xml
<svg
    xmlns="http://www.w3.org/2000/svg"
    width="64"
    height="64"
>
    <rect
        width="100%"
        height="100%"
        fill="#424C58"
    />
    <path
        d="M0,0L48,0L64,15L64,64L0,64Z M48,0L48,15L64,15Z M17,32,L49,32 M32,17,L32,49"
        stroke="#5FBCFE"
        fill="none"
        stroke-width="5"
    />
</svg>
```

`foruse.xaml`

![image-20241101143142981](http://image.jerryma.xyz//images/20241101-image-20241101143142981.png)

![image-20241101153806569](http://image.jerryma.xyz//images/20241101-image-20241101153806569.png)

```xaml
<ResourceDictionary xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation" xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
  <Geometry x:Key="flagGeometry">F1 M1024,1024z M0,0z M288,128L896,128 736,384 896,640 288,640 288,960 192,960 192,64 288,64z</Geometry>
  <DrawingGroup x:Key="flagDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource flagGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="flagDrawingImage" Drawing="{StaticResource flagDrawingGroup}" />
  <Geometry x:Key="menuGeometry">F1 M1024,1024z M0,0z M160,448A32,32,0,0,1,128,416L128,160.064A32,32,0,0,1,160,128.064L416,128.064A32,32,0,0,1,448,160.064L448,416A32,32,0,0,1,416,448z M608,448A32,32,0,0,1,576,416L576,160.064A32,32,0,0,1,608,128.064L863.936,128.064A32,32,0,0,1,895.936,160.064L895.936,416A32,32,0,0,1,863.936,448z M160,896A32,32,0,0,1,128,864L128,608A32,32,0,0,1,160,576L416,576A32,32,0,0,1,448,608L448,864A32,32,0,0,1,416,896z M608,896A32,32,0,0,1,576,864L576,608A32,32,0,0,1,608,576L863.936,576A32,32,0,0,1,895.936,608L895.936,864A32,32,0,0,1,863.936,896z</Geometry>
  <DrawingGroup x:Key="menuDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource menuGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="menuDrawingImage" Drawing="{StaticResource menuDrawingGroup}" />
  <Geometry x:Key="maleGeometry1">F1 M1024,1024z M0,0z M399.5,849.5A225,225,0,1,0,399.5,399.5A225,225,0,0,0,399.5,849.5 M399.5,905.75A281.25,281.25,0,1,1,399.5,343.25A281.25,281.25,0,0,1,399.5,905.75 M652.625,118.25L877.625,118.25Q905.75,118.25 905.75,146.375 905.75,174.5 877.625,174.5L652.625,174.5Q624.5,174.5 624.5,146.375 624.5,118.25 652.625,118.25</Geometry>
  <Geometry x:Key="maleGeometry2">F1 M1024,1024z M0,0z M877.625,118.25Q905.75,118.25,905.75,146.375L905.75,371.375Q905.75,399.5 877.625,399.5 849.5,399.5 849.5,371.375L849.5,146.375Q849.5,118.25,877.625,118.25</Geometry>
  <Geometry x:Key="maleGeometry3">F1 M1024,1024z M0,0z M604.813,458.9L565.1,419.131 857.713,126.463 897.538,166.287z</Geometry>
  <DrawingGroup x:Key="maleDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource maleGeometry1}" />
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource maleGeometry2}" />
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource maleGeometry3}" />
  </DrawingGroup>
  <DrawingImage x:Key="maleDrawingImage" Drawing="{StaticResource maleDrawingGroup}" />
  <Geometry x:Key="plusGeometry">F1 M1024,1024z M0,0z M480,480L480,128A32,32,0,0,1,544,128L544,480 896,480A32,32,0,1,1,896,544L544,544 544,896A32,32,0,1,1,480,896L480,544 128,544A32,32,0,0,1,128,480z</Geometry>
  <DrawingGroup x:Key="plusDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource plusGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="plusDrawingImage" Drawing="{StaticResource plusDrawingGroup}" />
  <Geometry x:Key="refreshGeometry">F1 M1024,1024z M0,0z M771.776,794.88A384,384,0,0,1,128,512L192,512A320,320,0,0,0,747.712,728.448L654.72,728.448A32,32,0,1,1,654.72,664.448L803.776,664.448A32,32,0,0,1,835.776,696.448L835.776,845.376A32,32,0,1,1,771.776,845.376L771.776,794.816z M276.288,295.616L369.28,295.616A32,32,0,0,1,369.28,359.616L220.16,359.616A32,32,0,0,1,188.16,327.616L188.16,178.56A32,32,0,0,1,252.16,178.56L252.16,229.12A384,384,0,0,1,896.128,512L832.128,512A320,320,0,0,0,276.352,295.616z</Geometry>
  <DrawingGroup x:Key="refreshDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource refreshGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="refreshDrawingImage" Drawing="{StaticResource refreshDrawingGroup}" />
  <Geometry x:Key="MuteNotificationGeometry1">F1 M1024,1024z M0,0z M241.216,832L304.832,768 768,768 768,448C768,405.632,757.76,365.696,739.52,330.496L786.432,283.264C815.36,331.392,832,387.84,832,448L832,768 928,768A32,32,0,1,1,928,832z M150.976,832L96,832A32,32,0,1,1,96,768L192,768 192,448A320.128,320.128,0,0,1,448,134.4L448,128A64,64,0,1,1,576,128L576,134.4A319.552,319.552,0,0,1,747.648,231.488L702.464,276.928A256,256,0,0,0,256,448L256,726.336 151.04,832z M448,896L576,896A64,64,0,0,1,448,896</Geometry>
  <Geometry x:Key="MuteNotificationGeometry2">F1 M1024,1024z M0,0z M150.72,859.072A32,32,0,0,1,105.28,814.016L809.28,105.472A32,32,0,0,1,854.72,150.528L150.72,859.072z</Geometry>
  <DrawingGroup x:Key="MuteNotificationDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource MuteNotificationGeometry1}" />
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource MuteNotificationGeometry2}" />
  </DrawingGroup>
  <DrawingImage x:Key="MuteNotificationDrawingImage" Drawing="{StaticResource MuteNotificationDrawingGroup}" />
  <Geometry x:Key="documentremoveGeometry">F1 M1024,1024z M0,0z M805.504,320L640,154.496 640,320z M832,384L576,384 576,128 192,128 192,896 832,896z M160,64L640,64 896,320 896,928A32,32,0,0,1,864,960L160,960A32,32,0,0,1,128,928L128,96A32,32,0,0,1,160,64 M352,576L672,576 672,640 352,640z</Geometry>
  <DrawingGroup x:Key="documentremoveDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FFF03A17" Geometry="{StaticResource documentremoveGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="documentremoveDrawingImage" Drawing="{StaticResource documentremoveDrawingGroup}" />
  <Geometry x:Key="shareGeometry">F1 M1024,1024z M0,0z M679.872,348.8L378.112,537.408A127.808,127.808,0,0,1,383.232,589.568L663.168,694.528A128,128,0,1,1,640.704,754.432L360.832,649.472A128,128,0,1,1,344.192,483.2L645.888,294.592A128,128,0,1,1,679.808,348.864z</Geometry>
  <DrawingGroup x:Key="shareDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource shareGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="shareDrawingImage" Drawing="{StaticResource shareDrawingGroup}" />
  <Geometry x:Key="folderOpenedGeometry">F1 M1024,1024z M0,0z M878.08,448L241.92,448 145.92,832 782.08,832 878.08,448z M832,384L832,320 485.76,320 357.504,192 128,192 128,640 185.92,408.256A32,32,0,0,1,216.96,384z M807.04,896L96,896A32,32,0,0,1,64,864L64,160A32,32,0,0,1,96,128L383.872,128 512.256,256 864,256A32,32,0,0,1,896,288L896,384 919.04,384A32,32,0,0,1,950.08,423.744L838.08,871.744A32,32,0,0,1,807.04,896</Geometry>
  <DrawingGroup x:Key="folderOpenedDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FFFFFF00" Geometry="{StaticResource folderOpenedGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="folderOpenedDrawingImage" Drawing="{StaticResource folderOpenedDrawingGroup}" />
  <Geometry x:Key="refreshleftGeometry">F1 M1024,1024z M0,0z M289.088,296.704L382.08,296.704A32,32,0,0,1,382.08,360.704L232.96,360.704A32,32,0,0,1,200.96,328.704L200.96,179.712A32,32,0,0,1,264.96,179.712L264.96,230.272A384,384,0,0,1,908.8,513.152A384,384,0,0,1,524.864,897.152A384,384,0,0,1,140.864,513.152L204.864,513.152A320,320,0,1,0,844.864,513.152A320,320,0,0,0,289.152,296.704z</Geometry>
  <DrawingGroup x:Key="refreshleftDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource refreshleftGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="refreshleftDrawingImage" Drawing="{StaticResource refreshleftDrawingGroup}" />
  <DrawingGroup x:Key="no7DrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <DrawingGroup>
      <GlyphRunDrawing ForegroundBrush="#FF5FBCFE">
        <GlyphRunDrawing.GlyphRun>
          <GlyphRun PixelsPerDip="1" BaselineOrigin="227.25,512" FontRenderingEmSize="1024" BidiLevel="0" IsSideways="False" CaretStops="1 1" ClusterMap="0" Characters="7" GlyphIndices="26" AdvanceWidths="569.5" GlyphOffsets="0,0" Language="en-us">
            <GlyphRun.GlyphTypeface>
              <GlyphTypeface FontUri="C:\WINDOWS\FONTS\ARIALBD.TTF" StyleSimulations="None" />
            </GlyphRun.GlyphTypeface>
          </GlyphRun>
        </GlyphRunDrawing.GlyphRun>
      </GlyphRunDrawing>
    </DrawingGroup>
  </DrawingGroup>
  <DrawingImage x:Key="no7DrawingImage" Drawing="{StaticResource no7DrawingGroup}" />
  <Geometry x:Key="listminusGeometry">F1 M1024,1024z M0,0z M113.75,790.083333333333C103.083333333333,786.791666666667 92.5833333333333,777.916666666667 87.375,767.75 84.8333333333333,762.75 84.375,760.083333333333 84.375,750 84.375,739.916666666667 84.8333333333333,737.25 87.4166666666667,732.208333333333 91.25,724.625 99.625,716.25 107.208333333333,712.416666666667L113.125,709.375 394,709.041666666667 674.833333333333,708.708333333333 681.833333333333,711.333333333333C690.833333333333,714.708333333333 700.291666666667,723.875 704.666666666667,733.416666666667 709.291666666667,743.541666666667 709.333333333333,756.458333333333 704.708333333333,766.5 700.75,775.125 692.708333333333,783.458333333333 684.333333333333,787.583333333333L678.125,790.625 397.5,790.833333333333C243.166666666667,790.958333333333,115.458333333333,790.625,113.75,790.083333333333 M113.75,540.083333333333C103.083333333333,536.833333333333 92.5833333333333,527.958333333333 87.375,517.75 84.8333333333333,512.75 84.375,510.083333333333 84.375,500 84.375,489.916666666667 84.8333333333333,487.25 87.4166666666667,482.208333333333 91.25,474.625 99.625,466.25 107.208333333333,462.416666666667L113.125,459.375 289.583333333333,459.041666666667 466.083333333333,458.708333333333 473.291666666667,461.416666666667C482.416666666667,464.833333333333 491.416666666667,473.125 495.916666666667,482.333333333333 498.875,488.333333333333 499.375,490.916666666667 499.375,500 499.375,509.125 498.875,511.625 495.875,517.75 491.5,526.666666666667 482.083333333333,535.291666666667 473,538.666666666667 466.208333333333,541.25 464.75,541.25 291.5,541.125 195.458333333333,541.083333333333 115.458333333333,540.625 113.75,540.083333333333 M613.75,540.083333333333C603.041666666667,536.791666666667 592.583333333333,527.916666666667 587.375,517.75 584.833333333333,512.75 584.375,510.083333333333 584.375,500 584.375,489.916666666667 584.833333333333,487.25 587.416666666667,482.208333333333 591.25,474.625 599.625,466.25 607.208333333333,462.416666666667L613.125,459.375 750,459.375 886.875,459.375 892.791666666667,462.416666666667C900.375,466.25 908.75,474.625 912.583333333333,482.208333333333 915.166666666667,487.25 915.625,489.916666666667 915.625,500 915.625,510.083333333333 915.166666666667,512.75 912.625,517.75 908.708333333333,525.416666666667 900.958333333333,533.166666666667 893.125,537.333333333333L886.875,540.625 751.875,540.833333333333C677.625,540.958333333333,615.458333333333,540.625,613.75,540.083333333333 M113.75,290.083333333333C103.083333333333,286.791666666667 92.5833333333333,277.916666666667 87.375,267.75 84.8333333333333,262.75 84.375,260.083333333333 84.375,250 84.375,239.916666666667 84.8333333333333,237.25 87.4166666666667,232.208333333333 91.25,224.625 99.625,216.25 107.208333333333,212.416666666667L113.125,209.375 394,209.041666666667 674.833333333333,208.708333333333 681.833333333333,211.333333333333C690.833333333333,214.708333333333 700.291666666667,223.875 704.666666666667,233.416666666667 709.291666666667,243.541666666667 709.333333333333,256.458333333333 704.708333333333,266.5 700.75,275.125 692.708333333333,283.458333333333 684.333333333333,287.583333333333L678.125,290.625 397.5,290.833333333333C243.166666666667,290.958333333333,115.458333333333,290.625,113.75,290.083333333333</Geometry>
  <DrawingGroup x:Key="listminusDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FFF03A17" Geometry="{StaticResource listminusGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="listminusDrawingImage" Drawing="{StaticResource listminusDrawingGroup}" />
  <Geometry x:Key="successfilledGeometry">F1 M1024,1024z M0,0z M512,64A448,448,0,1,1,512,960A448,448,0,0,1,512,64 M456.192,600.384L356.672,500.8A38.4,38.4,0,1,0,302.336,555.136L429.056,681.856A38.272,38.272,0,0,0,483.392,681.856L745.792,419.392A38.4,38.4,0,1,0,691.52,365.056z</Geometry>
  <DrawingGroup x:Key="successfilledDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF67C23A" Geometry="{StaticResource successfilledGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="successfilledDrawingImage" Drawing="{StaticResource successfilledDrawingGroup}" />
  <Geometry x:Key="cameraGeometry">F1 M1024,1024z M0,0z M896,256L128,256 128,832 896,832z M696.576,192L664.512,128 359.552,128 327.552,192z M96,192L256,192 302.336,99.392A64,64,0,0,1,359.552,64L664.512,64A64,64,0,0,1,721.728,99.328L768.192,192 928,192A32,32,0,0,1,960,224L960,864A32,32,0,0,1,928,896L96,896A32,32,0,0,1,64,864L64,224A32,32,0,0,1,96,192 M512,704A160,160,0,1,0,512,384A160,160,0,0,0,512,704 M512,768A224,224,0,1,1,512,320A224,224,0,0,1,512,768</Geometry>
  <DrawingGroup x:Key="cameraDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource cameraGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="cameraDrawingImage" Drawing="{StaticResource cameraDrawingGroup}" />
  <Geometry x:Key="homefilledGeometry">F1 M1024,1024z M0,0z M512,128L128,447.936 128,896 383.936,896 383.936,640 640,640 640,896 895.936,896 895.936,447.936z</Geometry>
  <DrawingGroup x:Key="homefilledDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource homefilledGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="homefilledDrawingImage" Drawing="{StaticResource homefilledDrawingGroup}" />
  <Geometry x:Key="viewGeometry">F1 M1024,1024z M0,0z M512,160C832,160 1024,512 1024,512 1024,512 832,864 512,864 192,864 0,512 0,512 0,512 192,160 512,160 M512,224C286.72,224 127.872,432.064 75.2,512 127.808,591.872 286.656,800 512,800 737.28,800 896.128,591.936 948.8,512 896.192,432.128 737.344,224 512,224z M512,288A224,224,0,1,1,512,736A224,224,0,0,1,512,288 M512,352A160.192,160.192,0,0,0,352,512C352,600.192 423.744,672 512,672 600.256,672 672,600.192 672,512 672,423.808 600.256,352 512,352</Geometry>
  <DrawingGroup x:Key="viewDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource viewGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="viewDrawingImage" Drawing="{StaticResource viewDrawingGroup}" />
  <Geometry x:Key="documentaddGeometry">F1 M1024,1024z M0,0z M832,384L576,384 576,128 192,128 192,896 832,896z M805.504,320L640,154.496 640,320z M160,64L640,64 896,320 896,928A32,32,0,0,1,864,960L160,960A32,32,0,0,1,128,928L128,96A32,32,0,0,1,160,64 M480,576L480,448 544,448 544,576 672,576 672,640 544,640 544,768 480,768 480,640 352,640 352,576z</Geometry>
  <DrawingGroup x:Key="documentaddDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource documentaddGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="documentaddDrawingImage" Drawing="{StaticResource documentaddDrawingGroup}" />
  <Geometry x:Key="checkGeometry">F1 M1024,1024z M0,0z M406.656,706.944L195.84,496.256A32,32,0,1,0,150.592,541.504L406.592,797.504 918.592,285.504A32,32,0,0,0,873.344,240.256L406.592,706.944z</Geometry>
  <DrawingGroup x:Key="checkDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF409EFF" Geometry="{StaticResource checkGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="checkDrawingImage" Drawing="{StaticResource checkDrawingGroup}" />
  <Geometry x:Key="printerGeometry">F1 M1024,1024z M0,0z M256,768L105.024,768C90.752,768,85.568,766.528,80.384,763.712A29.056,29.056,0,0,1,68.224,751.616C65.536,746.432,64,741.248,64,727.04L64,379.072C64,336.256 68.48,320.768 76.8,305.088 85.184,289.472 97.472,277.184 113.088,268.8 128.768,260.48 144.256,256 187.072,256L256,256 256,64 768,64 768,256 836.928,256C879.744,256 895.232,260.48 910.912,268.8 926.528,277.184 938.816,289.472 947.2,305.088 955.52,320.768 960,336.256 960,379.072L960,726.976C960,741.248,958.528,746.432,955.712,751.616A29.056,29.056,0,0,1,943.616,763.776C938.432,766.528,933.248,768,918.976,768L768,768 768,960 256,960z M320,576L320,896 704,896 704,576z M256,704L256,512 768,512 768,704 896,704 896,379.072C896,349.696,894.592,342.592,890.752,335.296A23.296,23.296,0,0,0,880.704,325.248C873.472,321.408,866.304,320,836.928,320L187.072,320C157.696,320,150.592,321.408,143.296,325.248A23.296,23.296,0,0,0,133.248,335.296C129.408,342.528,128,349.696,128,379.072L128,704z M320,256L704,256 704,128 320,128z M256,384L320,384 320,448 256,448z M384,384L448,384 448,448 384,448z</Geometry>
  <DrawingGroup x:Key="printerDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource printerGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="printerDrawingImage" Drawing="{StaticResource printerDrawingGroup}" />
  <Geometry x:Key="documentGeometry">F1 M1024,1024z M0,0z M832,384L576,384 576,128 192,128 192,896 832,896z M805.504,320L640,154.496 640,320z M160,64L640,64 896,320 896,928A32,32,0,0,1,864,960L160,960A32,32,0,0,1,128,928L128,96A32,32,0,0,1,160,64 M320,512L704,512 704,576 320,576z M320,320L480,320 480,384 320,384z M320,704L704,704 704,768 320,768z</Geometry>
  <DrawingGroup x:Key="documentDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FFFFFFFF" Geometry="{StaticResource documentGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="documentDrawingImage" Drawing="{StaticResource documentDrawingGroup}" />
  <Geometry x:Key="femaleGeometry1">F1 M1024,1024z M0,0z M512,640A256,256,0,1,0,512,128A256,256,0,0,0,512,640 M512,704A320,320,0,1,1,512,64A320,320,0,0,1,512,704</Geometry>
  <Geometry x:Key="femaleGeometry2">F1 M1024,1024z M0,0z M512,640Q544,640,544,672L544,928Q544,960 512,960 480,960 480,928L480,672Q480,640,512,640</Geometry>
  <Geometry x:Key="femaleGeometry3">F1 M1024,1024z M0,0z M352,800L672,800Q704,800 704,832 704,864 672,864L352,864Q320,864 320,832 320,800 352,800</Geometry>
  <DrawingGroup x:Key="femaleDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource femaleGeometry1}" />
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource femaleGeometry2}" />
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource femaleGeometry3}" />
  </DrawingGroup>
  <DrawingImage x:Key="femaleDrawingImage" Drawing="{StaticResource femaleDrawingGroup}" />
  <Geometry x:Key="removefilledGeometry">F1 M1024,1024z M0,0z M512,64A448,448,0,1,1,512,960A448,448,0,0,1,512,64 M288,512A38.4,38.4,0,0,0,326.4,550.4L697.6,550.4A38.4,38.4,0,0,0,697.6,473.6L326.4,473.6A38.4,38.4,0,0,0,288,512</Geometry>
  <DrawingGroup x:Key="removefilledDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FFF03A17" Geometry="{StaticResource removefilledGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="removefilledDrawingImage" Drawing="{StaticResource removefilledDrawingGroup}" />
  <Geometry x:Key="folderGeometry">F1 M1024,1024z M0,0z M128,192L128,832 896,832 896,320 485.76,320 357.504,192z M96,128L383.872,128 512.256,256 928,256A32,32,0,0,1,960,288L960,864A32,32,0,0,1,928,896L96,896A32,32,0,0,1,64,864L64,160A32,32,0,0,1,96,128</Geometry>
  <DrawingGroup x:Key="folderDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FFFFFF00" Geometry="{StaticResource folderGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="folderDrawingImage" Drawing="{StaticResource folderDrawingGroup}" />
  <Geometry x:Key="editGeometry1">F1 M1024,1024z M0,0z M832,512A32,32,0,1,1,896,512L896,864A32,32,0,0,1,864,896L160,896A32,32,0,0,1,128,864L128,160A32,32,0,0,1,160,128L512,128A32,32,0,0,1,512,192L192,192 192,832 832,832z</Geometry>
  <Geometry x:Key="editGeometry2">F1 M1024,1024z M0,0z M469.952,554.24L522.752,546.688 847.104,222.4A32,32,0,1,0,801.856,177.152L477.44,501.44 469.888,554.24z M892.352,131.84A96,96,0,0,1,892.352,267.648L560.512,599.488A32,32,0,0,1,542.4,608.576L436.8,623.68A32,32,0,0,1,400.576,587.456L415.68,481.856A32,32,0,0,1,424.704,463.744L756.608,131.904A96,96,0,0,1,892.352,131.904z</Geometry>
  <DrawingGroup x:Key="editDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource editGeometry1}" />
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource editGeometry2}" />
  </DrawingGroup>
  <DrawingImage x:Key="editDrawingImage" Drawing="{StaticResource editDrawingGroup}" />
  <DrawingGroup x:Key="no2DrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <DrawingGroup>
      <GlyphRunDrawing ForegroundBrush="#FF5FBCFE">
        <GlyphRunDrawing.GlyphRun>
          <GlyphRun PixelsPerDip="1" BaselineOrigin="227.25,512" FontRenderingEmSize="1024" BidiLevel="0" IsSideways="False" CaretStops="1 1" ClusterMap="0" Characters="2" GlyphIndices="21" AdvanceWidths="569.5" GlyphOffsets="0,0" Language="en-us">
            <GlyphRun.GlyphTypeface>
              <GlyphTypeface FontUri="C:\WINDOWS\FONTS\ARIALBD.TTF" StyleSimulations="None" />
            </GlyphRun.GlyphTypeface>
          </GlyphRun>
        </GlyphRunDrawing.GlyphRun>
      </GlyphRunDrawing>
    </DrawingGroup>
  </DrawingGroup>
  <DrawingImage x:Key="no2DrawingImage" Drawing="{StaticResource no2DrawingGroup}" />
  <Geometry x:Key="moreGeometry">F1 M1024,1024z M0,0z M176,416A112,112,0,1,0,176,640A112,112,0,0,0,176,416 M176,480A48,48,0,1,1,176,576A48,48,0,0,1,176,480 M512,416A112,112,0,1,1,512,640A112,112,0,0,1,512,416 M512,480A48,48,0,1,0,512,576A48,48,0,0,0,512,480 M848,416A112,112,0,1,1,848,640A112,112,0,0,1,848,416 M848,480A48,48,0,1,0,848,576A48,48,0,0,0,848,480</Geometry>
  <DrawingGroup x:Key="moreDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource moreGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="moreDrawingImage" Drawing="{StaticResource moreDrawingGroup}" />
  <Geometry x:Key="gridGeometry">F1 M1024,1024z M0,0z M640,384L640,640 384,640 384,384z M704,384L896,384 896,640 704,640z M640,896L384,896 384,704 640,704z M704,896L704,704 896,704 896,896z M640,128L640,320 384,320 384,128z M704,128L896,128 896,320 704,320z M320,384L320,640 128,640 128,384z M320,896L128,896 128,704 320,704z M320,128L320,320 128,320 128,128z</Geometry>
  <DrawingGroup x:Key="gridDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource gridGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="gridDrawingImage" Drawing="{StaticResource gridDrawingGroup}" />
  <Geometry x:Key="foldGeometry">F1 M1024,1024z M0,0z M896,192L128,192 128,320 896,320z M896,448L384,448 384,576 896,576z M896,704L128,704 128,832 896,832z M320,384L128,512 320,640z</Geometry>
  <DrawingGroup x:Key="foldDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource foldGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="foldDrawingImage" Drawing="{StaticResource foldDrawingGroup}" />
  <Geometry x:Key="uploadfilledGeometry">F1 M1024,1024z M0,0z M544,864L544,672 672,672 512,480 352,672 480,672 480,864 320,864 320,862.4C314.624,862.72,309.504,864,304,864A240,240,0,0,1,64,624C64,500.864,157.12,400.512,276.608,386.752A239.808,239.808,0,0,1,512,192A239.872,239.872,0,0,1,747.456,386.752C866.944,400.512,959.936,500.864,959.936,624A240,240,0,0,1,719.936,864C714.56,864,709.376,862.72,703.936,862.4L703.936,864z</Geometry>
  <DrawingGroup x:Key="uploadfilledDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource uploadfilledGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="uploadfilledDrawingImage" Drawing="{StaticResource uploadfilledDrawingGroup}" />
  <Geometry x:Key="deleteGeometry">F1 M1024,1024z M0,0z M160,256L96,256A32,32,0,0,1,96,192L352,192 352,95.936A32,32,0,0,1,384,63.936L640,63.936A32,32,0,0,1,672,95.936L672,192 928,192A32,32,0,1,1,928,256L864,256 864,928A32,32,0,0,1,832,960L192,960A32,32,0,0,1,160,928z M608,192L608,128 416,128 416,192z M224,896L800,896 800,256 224,256z M416,768A32,32,0,0,1,384,736L384,416A32,32,0,0,1,448,416L448,736A32,32,0,0,1,416,768 M608,768A32,32,0,0,1,576,736L576,416A32,32,0,0,1,640,416L640,736A32,32,0,0,1,608,768</Geometry>
  <DrawingGroup x:Key="deleteDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FFF03A17" Geometry="{StaticResource deleteGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="deleteDrawingImage" Drawing="{StaticResource deleteDrawingGroup}" />
  <DrawingGroup x:Key="no9DrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <DrawingGroup>
      <GlyphRunDrawing ForegroundBrush="#FF5FBCFE">
        <GlyphRunDrawing.GlyphRun>
          <GlyphRun PixelsPerDip="1" BaselineOrigin="227.25,512" FontRenderingEmSize="1024" BidiLevel="0" IsSideways="False" CaretStops="1 1" ClusterMap="0" Characters="9" GlyphIndices="28" AdvanceWidths="569.5" GlyphOffsets="0,0" Language="en-us">
            <GlyphRun.GlyphTypeface>
              <GlyphTypeface FontUri="C:\WINDOWS\FONTS\ARIALBD.TTF" StyleSimulations="None" />
            </GlyphRun.GlyphTypeface>
          </GlyphRun>
        </GlyphRunDrawing.GlyphRun>
      </GlyphRunDrawing>
    </DrawingGroup>
  </DrawingGroup>
  <DrawingImage x:Key="no9DrawingImage" Drawing="{StaticResource no9DrawingGroup}" />
  <Geometry x:Key="avatarGeometry">F1 M1024,1024z M0,0z M628.736,528.896A416,416,0,0,1,928,928L96,928A415.872,415.872,0,0,1,395.264,528.896L512,704z M720,304A208,208,0,1,1,304,304A208,208,0,0,1,720,304</Geometry>
  <DrawingGroup x:Key="avatarDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource avatarGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="avatarDrawingImage" Drawing="{StaticResource avatarDrawingGroup}" />
  <Geometry x:Key="commentGeometry">F1 M1024,1024z M0,0z M736,504A56,56,0,1,1,736,392A56,56,0,0,1,736,504 M512,504A56,56,0,1,1,512,392A56,56,0,0,1,512,504 M288,504A56,56,0,1,1,288,392A56,56,0,0,1,288,504 M128,128L128,768 320,768 320,928 544,768 896,768 896,128z</Geometry>
  <DrawingGroup x:Key="commentDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource commentGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="commentDrawingImage" Drawing="{StaticResource commentDrawingGroup}" />
  <Geometry x:Key="switchGeometry">F1 M1024,1024z M0,0z M118.656,438.656A32,32,0,0,1,118.656,393.408L416,96 420.48,92.224A32,32,0,0,1,461.248,96L464.96,100.48A32.064,32.064,0,0,1,461.248,141.312L218.56,384 928,384A32,32,0,1,1,928,448L141.248,448A32,32,0,0,1,118.656,438.656z M64,608A32,32,0,0,1,96,576L882.752,576A32,32,0,0,1,905.408,630.592L608,928 603.52,931.776A32.064,32.064,0,0,1,562.688,882.752L805.632,640 96,640A32,32,0,0,1,64,608</Geometry>
  <DrawingGroup x:Key="switchDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource switchGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="switchDrawingImage" Drawing="{StaticResource switchDrawingGroup}" />
  <Geometry x:Key="listGeometry">F1 M1024,1024z M0,0z M704,192L864,192 864,928 160,928 160,192 320,192 320,256 704,256z M288,512L736,512 736,448 288,448z M288,768L736,768 736,704 288,704z M384,192L384,96 640,96 640,192z</Geometry>
  <DrawingGroup x:Key="listDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FFFFFFFF" Geometry="{StaticResource listGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="listDrawingImage" Drawing="{StaticResource listDrawingGroup}" />
  <Geometry x:Key="linkGeometry">F1 M1024,1024z M0,0z M715.648,625.152L670.4,579.904 760.896,489.344C835.904,414.4 846.016,302.976 783.552,240.448 721.024,177.984 609.6,188.096 534.592,263.104L444.16,353.6 398.912,308.352 489.408,217.856C589.44,117.888 741.376,107.776 828.864,195.2 916.352,282.688 906.176,434.624 806.208,534.656L715.712,625.152z M625.152,715.648L534.656,806.144C434.624,906.112 282.688,916.224 195.2,828.8 107.712,741.312 117.888,589.376 217.856,489.344L308.352,398.848 353.6,444.096 263.104,534.656C188.096,609.6 177.984,721.024 240.448,783.552 302.976,846.016 414.4,835.904 489.408,760.896L579.904,670.4z M625.152,353.6L670.4,398.848 398.848,670.4 353.6,625.152z</Geometry>
  <DrawingGroup x:Key="linkDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource linkGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="linkDrawingImage" Drawing="{StaticResource linkDrawingGroup}" />
  <Geometry x:Key="removeGeometry1">F1 M1024,1024z M0,0z M352,480L672,480A32,32,0,1,1,672,544L352,544A32,32,0,0,1,352,480</Geometry>
  <Geometry x:Key="removeGeometry2">F1 M1024,1024z M0,0z M512,896A384,384,0,1,0,512,128A384,384,0,0,0,512,896 M512,960A448,448,0,1,1,512,64A448,448,0,0,1,512,960</Geometry>
  <DrawingGroup x:Key="removeDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FFF03A17" Geometry="{StaticResource removeGeometry1}" />
    <GeometryDrawing Brush="#FFF03A17" Geometry="{StaticResource removeGeometry2}" />
  </DrawingGroup>
  <DrawingImage x:Key="removeDrawingImage" Drawing="{StaticResource removeDrawingGroup}" />
  <Geometry x:Key="zoomplusGeometry">F1 M1024,1024z M0,0z M795.904,750.72L920.896,875.648A32,32,0,0,1,875.648,920.896L750.656,795.904A416,416,0,1,1,795.904,750.656z M480,832A352,352,0,1,0,480,128A352,352,0,0,0,480,832 M448,448L448,352A32,32,0,0,1,512,352L512,448 608,448A32,32,0,0,1,608,512L512,512 512,608A32,32,0,0,1,448,608L448,512 352,512A32,32,0,0,1,352,448z</Geometry>
  <DrawingGroup x:Key="zoomplusDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource zoomplusGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="zoomplusDrawingImage" Drawing="{StaticResource zoomplusDrawingGroup}" />
  <Geometry x:Key="uploadGeometry">F1 M1024,1024z M0,0z M160,832L864,832A32,32,0,1,1,864,896L160,896A32,32,0,1,1,160,832 M544,253.696L544,704 480,704 480,247.296 237.248,490.048 192,444.8 508.8,128 825.6,444.8 780.288,490.048z</Geometry>
  <DrawingGroup x:Key="uploadDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource uploadGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="uploadDrawingImage" Drawing="{StaticResource uploadDrawingGroup}" />
  <Geometry x:Key="documentcheckedGeometry">F1 M1024,1024z M0,0z M805.504,320L640,154.496 640,320z M832,384L576,384 576,128 192,128 192,896 832,896z M160,64L640,64 896,320 896,928A32,32,0,0,1,864,960L160,960A32,32,0,0,1,128,928L128,96A32,32,0,0,1,160,64 M478.4,646.144L659.392,465.152 704.64,510.4 478.4,736.64 320,578.304 365.248,532.992z</Geometry>
  <DrawingGroup x:Key="documentcheckedDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF67C23A" Geometry="{StaticResource documentcheckedGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="documentcheckedDrawingImage" Drawing="{StaticResource documentcheckedDrawingGroup}" />
  <Geometry x:Key="folderAddGeometry">F1 M1024,1024z M0,0z M128,192L128,832 896,832 896,320 485.76,320 357.504,192z M96,128L383.872,128 512.256,256 928,256A32,32,0,0,1,960,288L960,864A32,32,0,0,1,928,896L96,896A32,32,0,0,1,64,864L64,160A32,32,0,0,1,96,128 M480,544L480,416 544,416 544,544 672,544 672,608 544,608 544,736 480,736 480,608 352,608 352,544z</Geometry>
  <DrawingGroup x:Key="folderAddDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FFFFFF00" Geometry="{StaticResource folderAddGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="folderAddDrawingImage" Drawing="{StaticResource folderAddDrawingGroup}" />
  <Geometry x:Key="refreshrightGeometry">F1 M1024,1024z M0,0z M784.512,230.272L784.512,179.712A32,32,0,1,1,848.512,179.712L848.512,328.768A32,32,0,0,1,816.512,360.768L667.52,360.768A32,32,0,1,1,667.52,296.768L760.512,296.768A320,320,0,1,0,524.8,833.152A320,320,0,0,0,844.8,513.152L908.8,513.152A384,384,0,0,1,524.8,897.152A384,384,0,0,1,140.8,513.152A384,384,0,0,1,784.512,230.272z</Geometry>
  <DrawingGroup x:Key="refreshrightDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource refreshrightGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="refreshrightDrawingImage" Drawing="{StaticResource refreshrightDrawingGroup}" />
  <Geometry x:Key="listplusGeometry">F1 M1024,1024z M0,0z M113.75,790.083333333333C103.083333333333,786.791666666667 92.5833333333333,777.916666666667 87.375,767.75 84.8333333333333,762.75 84.375,760.083333333333 84.375,750 84.375,739.916666666667 84.8333333333333,737.25 87.4166666666667,732.208333333333 91.25,724.625 99.625,716.25 107.208333333333,712.416666666667L113.125,709.375 394,709.041666666667 674.833333333333,708.708333333333 681.833333333333,711.333333333333C690.833333333333,714.708333333333 700.291666666667,723.875 704.666666666667,733.416666666667 709.291666666667,743.541666666667 709.333333333333,756.458333333333 704.708333333333,766.5 700.75,775.125 692.708333333333,783.458333333333 684.333333333333,787.583333333333L678.125,790.625 397.5,790.833333333333C243.166666666667,790.958333333333,115.458333333333,790.625,113.75,790.083333333333 M738.75,665.166666666667C727.75,661.541666666667 717.583333333333,652.916666666667 712.375,642.75 709.375,636.875 709.375,636.75 709,589.125L708.625,541.375 660.875,541 613.125,540.625 606.875,537.333333333333C599.041666666667,533.166666666667 591.291666666667,525.416666666667 587.375,517.75 584.833333333333,512.75 584.375,510.083333333333 584.375,500 584.375,489.916666666667 584.833333333333,487.25 587.416666666667,482.208333333333 591.25,474.625 599.625,466.25 607.208333333333,462.416666666667 613.125,459.375 613.166666666667,459.375 660.875,459L708.625,458.625 709,410.875C709.375,363.166666666667 709.375,363.125 712.416666666667,357.208333333333 716.25,349.625 724.625,341.25 732.208333333333,337.416666666667 737.25,334.833333333333 739.916666666667,334.375 750,334.375 760.083333333333,334.375 762.75,334.833333333333 767.791666666667,337.416666666667 775.375,341.25 783.75,349.625 787.583333333333,357.208333333333 790.625,363.125 790.625,363.166666666667 791,410.875L791.375,458.625 839.125,459C886.833333333333,459.375 886.875,459.375 892.791666666667,462.416666666667 900.375,466.25 908.75,474.625 912.583333333333,482.208333333333 915.166666666667,487.25 915.625,489.916666666667 915.625,500 915.625,510.083333333333 915.166666666667,512.75 912.625,517.75 908.708333333333,525.416666666667 900.958333333333,533.166666666667 893.125,537.333333333333L886.875,540.625 839.125,541 791.375,541.375 791,589.125C790.625,636.75 790.625,636.875 787.625,642.75 783.666666666667,650.458333333333 775.916666666667,658.208333333333 768.125,662.208333333333 763.25,664.708333333333 759.666666666667,665.5 751.875,665.791666666667 746.375,666 740.458333333333,665.708333333333 738.75,665.166666666667 M113.75,540.083333333333C103.083333333333,536.833333333333 92.5833333333333,527.958333333333 87.375,517.75 84.8333333333333,512.75 84.375,510.083333333333 84.375,500 84.375,489.916666666667 84.8333333333333,487.25 87.4166666666667,482.208333333333 91.25,474.625 99.625,466.25 107.208333333333,462.416666666667L113.125,459.375 289.583333333333,459.041666666667 466.083333333333,458.708333333333 473.291666666667,461.416666666667C482.416666666667,464.833333333333 491.416666666667,473.125 495.916666666667,482.333333333333 498.875,488.333333333333 499.375,490.916666666667 499.375,500 499.375,509.125 498.875,511.625 495.875,517.75 491.5,526.666666666667 482.083333333333,535.291666666667 473,538.666666666667 466.208333333333,541.25 464.75,541.25 291.5,541.125 195.458333333333,541.083333333333 115.458333333333,540.625 113.75,540.083333333333 M113.75,290.083333333333C103.083333333333,286.791666666667 92.5833333333333,277.916666666667 87.375,267.75 84.8333333333333,262.75 84.375,260.083333333333 84.375,250 84.375,239.916666666667 84.8333333333333,237.25 87.4166666666667,232.208333333333 91.25,224.625 99.625,216.25 107.208333333333,212.416666666667L113.125,209.375 394,209.041666666667 674.833333333333,208.708333333333 681.833333333333,211.333333333333C690.833333333333,214.708333333333 700.291666666667,223.875 704.666666666667,233.416666666667 709.291666666667,243.541666666667 709.333333333333,256.458333333333 704.708333333333,266.5 700.75,275.125 692.708333333333,283.458333333333 684.333333333333,287.583333333333L678.125,290.625 397.5,290.833333333333C243.166666666667,290.958333333333,115.458333333333,290.625,113.75,290.083333333333</Geometry>
  <DrawingGroup x:Key="listplusDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource listplusGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="listplusDrawingImage" Drawing="{StaticResource listplusDrawingGroup}" />
  <Geometry x:Key="downloadGeometry">F1 M1024,1024z M0,0z M160,832L864,832A32,32,0,1,1,864,896L160,896A32,32,0,1,1,160,832 M544,578.304L780.288,341.952 825.536,387.2 508.8,704 192,387.2 237.248,341.952 480,584.704 480,128 544,128z</Geometry>
  <DrawingGroup x:Key="downloadDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource downloadGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="downloadDrawingImage" Drawing="{StaticResource downloadDrawingGroup}" />
  <Geometry x:Key="unlockGeometry1">F1 M1024,1024z M0,0z M224,448A32,32,0,0,0,192,480L192,864A32,32,0,0,0,224,896L800,896A32,32,0,0,0,832,864L832,480A32,32,0,0,0,800,448z M224,384L800,384A96,96,0,0,1,896,480L896,864A96,96,0,0,1,800,960L224,960A96,96,0,0,1,128,864L128,480A96,96,0,0,1,224,384</Geometry>
  <Geometry x:Key="unlockGeometry2">F1 M1024,1024z M0,0z M512,544A32,32,0,0,1,544,576L544,768A32,32,0,1,1,480,768L480,576A32,32,0,0,1,512,544 M690.304,248.704A192.064,192.064,0,0,0,320,320L320,384 672,384 768,422.4 768,448 256,448 256,320A256,256,0,0,1,749.76,224.896z</Geometry>
  <DrawingGroup x:Key="unlockDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource unlockGeometry1}" />
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource unlockGeometry2}" />
  </DrawingGroup>
  <DrawingImage x:Key="unlockDrawingImage" Drawing="{StaticResource unlockDrawingGroup}" />
  <Geometry x:Key="platformGeometry">F1 M1024,1024z M0,0z M448,832L448,768 576,768 576,832 768,832 768,896 256,896 256,832z M128,704L128,128 896,128 896,704z</Geometry>
  <DrawingGroup x:Key="platformDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource platformGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="platformDrawingImage" Drawing="{StaticResource platformDrawingGroup}" />
  <DrawingGroup x:Key="no1DrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <DrawingGroup>
      <GlyphRunDrawing ForegroundBrush="#FF5FBCFE">
        <GlyphRunDrawing.GlyphRun>
          <GlyphRun PixelsPerDip="1" BaselineOrigin="227.25,512" FontRenderingEmSize="1024" BidiLevel="0" IsSideways="False" CaretStops="1 1" ClusterMap="0" Characters="1" GlyphIndices="20" AdvanceWidths="569.5" GlyphOffsets="0,0" Language="en-us">
            <GlyphRun.GlyphTypeface>
              <GlyphTypeface FontUri="C:\WINDOWS\FONTS\ARIALBD.TTF" StyleSimulations="None" />
            </GlyphRun.GlyphTypeface>
          </GlyphRun>
        </GlyphRunDrawing.GlyphRun>
      </GlyphRunDrawing>
    </DrawingGroup>
  </DrawingGroup>
  <DrawingImage x:Key="no1DrawingImage" Drawing="{StaticResource no1DrawingGroup}" />
  <Geometry x:Key="warningGeometry">F1 M1024,1024z M0,0z M512,64A448,448,0,1,1,512,960A448,448,0,0,1,512,64 M512,896A384,384,0,0,0,512,128A384,384,0,0,0,512,896 M560,720A48,48,0,1,1,464,720A48,48,0,0,1,560,720 M512,256A32,32,0,0,1,544,288L544,576A32,32,0,0,1,480,576L480,288A32,32,0,0,1,512,256</Geometry>
  <DrawingGroup x:Key="warningDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FFE6A23C" Geometry="{StaticResource warningGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="warningDrawingImage" Drawing="{StaticResource warningDrawingGroup}" />
  <Geometry x:Key="pictureGeometry1">F1 M1024,1024z M0,0z M160,160L160,864 864,864 864,160z M128,96L896,96A32,32,0,0,1,928,128L928,896A32,32,0,0,1,896,928L128,928A32,32,0,0,1,96,896L96,128A32,32,0,0,1,128,96</Geometry>
  <Geometry x:Key="pictureGeometry2">F1 M1024,1024z M0,0z M384,288Q448,288 448,352 448,416 384,416 320,416 320,352 320,288 384,288 M185.408,876.992L134.592,838.08 350.72,556.032A96,96,0,0,1,485.312,538.176L487.168,539.648 610.048,638.784A32,32,0,0,0,655.04,633.92L871.04,364.032 920.96,403.968 705.152,673.792 704.896,674.112A96,96,0,0,1,569.856,688.576L446.976,589.504 446.336,588.992A32,32,0,0,0,401.536,594.944z</Geometry>
  <DrawingGroup x:Key="pictureDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource pictureGeometry1}" />
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource pictureGeometry2}" />
  </DrawingGroup>
  <DrawingImage x:Key="pictureDrawingImage" Drawing="{StaticResource pictureDrawingGroup}" />
  <Geometry x:Key="starGeometry">F1 M1024,1024z M0,0z M512,747.84L740.16,867.776A6.4,6.4,0,0,0,749.44,861.056L705.92,606.976 890.432,427.072A6.4,6.4,0,0,0,886.912,416.192L631.808,379.072 517.76,147.904A6.4,6.4,0,0,0,506.24,147.904L392.192,379.072 137.088,416.192A6.4,6.4,0,0,0,133.568,427.072L318.08,606.976 274.496,861.056A6.4,6.4,0,0,0,283.776,867.776z M313.6,924.48A70.4,70.4,0,0,1,211.456,850.24L249.344,629.312 88.96,472.96A70.4,70.4,0,0,1,128,352.896L349.76,320.64 448.96,119.68A70.4,70.4,0,0,1,575.168,119.68L674.368,320.64 896.192,352.896A70.4,70.4,0,0,1,935.232,472.96L774.72,629.376 812.608,850.304A70.4,70.4,0,0,1,710.464,924.544L512,820.096 313.6,924.416z</Geometry>
  <DrawingGroup x:Key="starDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FFFFFFFF" Geometry="{StaticResource starGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="starDrawingImage" Drawing="{StaticResource starDrawingGroup}" />
  <Geometry x:Key="turnoffGeometry1">F1 M1024,1024z M0,0z M329.956,257.138A254.862,254.862,0,0,0,329.956,766.862L694.044,766.862A254.862,254.862,0,0,0,694.044,257.138z M329.956,184.32L694.044,184.32A327.68,327.68,0,1,1,694.044,839.68L329.956,839.68A327.68,327.68,0,1,1,329.956,184.32z</Geometry>
  <Geometry x:Key="turnoffGeometry2">F1 M1024,1024z M0,0z M329.956,621.227A109.227,109.227,0,1,0,329.956,402.773A109.227,109.227,0,0,0,329.956,621.227 M329.956,694.044A182.044,182.044,0,1,1,329.956,329.956A182.044,182.044,0,0,1,329.956,694.044</Geometry>
  <DrawingGroup x:Key="turnoffDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource turnoffGeometry1}" />
    <GeometryDrawing Brush="#FF000000" Geometry="{StaticResource turnoffGeometry2}" />
  </DrawingGroup>
  <DrawingImage x:Key="turnoffDrawingImage" Drawing="{StaticResource turnoffDrawingGroup}" />
  <Geometry x:Key="searchGeometry">F1 M1024,1024z M0,0z M795.904,750.72L920.896,875.648A32,32,0,0,1,875.648,920.896L750.656,795.904A416,416,0,1,1,795.904,750.656z M480,832A352,352,0,1,0,480,128A352,352,0,0,0,480,832</Geometry>
  <DrawingGroup x:Key="searchDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource searchGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="searchDrawingImage" Drawing="{StaticResource searchDrawingGroup}" />
  <Geometry x:Key="documentdeleteGeometry">F1 M1024,1024z M0,0z M805.504,320L640,154.496 640,320z M832,384L576,384 576,128 192,128 192,896 832,896z M160,64L640,64 896,320 896,928A32,32,0,0,1,864,960L160,960A32,32,0,0,1,128,928L128,96A32,32,0,0,1,160,64 M468.992,610.304L378.496,519.68 423.744,474.432 514.304,564.928 604.8,474.496 650.048,519.744 559.552,610.304 650.048,700.8 604.8,746.048 514.304,655.552 423.744,746.048 378.496,700.8 468.992,610.304z</Geometry>
  <DrawingGroup x:Key="documentdeleteDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FFF03A17" Geometry="{StaticResource documentdeleteGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="documentdeleteDrawingImage" Drawing="{StaticResource documentdeleteDrawingGroup}" />
  <Geometry x:Key="settingGeometry">F1 M1024,1024z M0,0z M600.704,64A32,32,0,0,1,631.168,86.208L666.368,195.584C681.152,202.816,695.296,210.944,708.8,220.096L821.184,195.904A32,32,0,0,1,855.616,211.264L944.32,364.8A32,32,0,0,1,940.288,402.304L863.168,487.424A357.12,357.12,0,0,1,863.168,536.448L940.288,621.696A32,32,0,0,1,944.32,659.2L855.616,812.8A32,32,0,0,1,821.184,828.096L708.8,803.904C695.36,812.992,681.152,821.184,666.432,828.416L631.168,937.792A32,32,0,0,1,600.704,960L423.296,960A32,32,0,0,1,392.832,937.792L357.696,828.48A351.616,351.616,0,0,1,315.136,803.84L202.816,828.096A32,32,0,0,1,168.384,812.736L79.68,659.2A32,32,0,0,1,83.712,621.696L160.832,536.448A357.12,357.12,0,0,1,160.832,487.552L83.712,402.304A32,32,0,0,1,79.68,364.8L168.384,211.2A32,32,0,0,1,202.816,195.904L315.136,220.16C328.704,211.008,342.912,202.752,357.696,195.52L392.896,86.208A32,32,0,0,1,423.232,64L600.64,64z M577.28,128L446.72,128 410.368,241.088 385.856,253.056A294.113,294.113,0,0,0,351.04,273.152L328.384,288.512 212.16,263.424 146.88,376.576 226.56,464.768 224.64,491.904A293.12,293.12,0,0,0,224.64,532.096L226.56,559.232 146.752,647.424 212.096,760.576 328.32,735.552 350.976,750.848A294.113,294.113,0,0,0,385.792,770.944L410.304,782.912 446.72,896 577.408,896 613.888,782.848 638.336,770.944A288.282,288.282,0,0,0,673.088,750.848L695.68,735.552 811.968,760.576 877.248,647.424 797.504,559.232 799.424,532.096A293.12,293.12,0,0,0,799.424,491.84L797.504,464.704 877.312,376.576 811.968,263.424 695.68,288.384 673.088,273.152A287.616,287.616,0,0,0,638.336,253.056L613.888,241.152 577.344,128z M512,320A192,192,0,1,1,512,704A192,192,0,0,1,512,320 M512,384A128,128,0,1,0,512,640A128,128,0,0,0,512,384</Geometry>
  <DrawingGroup x:Key="settingDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource settingGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="settingDrawingImage" Drawing="{StaticResource settingDrawingGroup}" />
  <Geometry x:Key="view_offGeometry1">F1 M1024,1024z M0,0z M876.8,156.8C876.8,147.2 873.6,140.8 867.2,134.4 860.8,128 854.4,124.8 844.8,124.8 835.2,124.8 828.8,128 822.4,134.4L736,220.8C672,188.8 598.4,169.6 512,160 352,176 224,233.6 134.4,336 44.8,438.4 0,496 0,512 0,528 48,585.6 134.4,688 156.8,713.6 179.2,736 208,755.2L121.6,844.8C115.2,851.2 112,857.6 112,867.2 112,876.8 115.2,883.2 121.6,889.6 128,896 134.4,899.2 144,899.2 153.6,899.2 160,896 166.4,889.6L870.4,179.2C873.6,172.8,876.8,166.4,876.8,156.8z M230.4,684.8C153.6,614.4 102.4,556.8 76.8,512 105.6,464 156.8,406.4 230.4,339.2 304,272 400,230.4 512,224 576,227.2 636.8,243.2 688,268.8L633.6,323.2C598.4,300.8 560,288 512,288 448,288 396.8,310.4 352,352 307.2,393.6 288,448 288,512 288,560 300.8,601.6 323.2,636.8L256,707.2C246.4,700.8,236.8,691.2,230.4,684.8z M371.2,588.8C358.4,566.4 352,540.8 352,512 352,467.2 368,428.8 400,400 432,371.2 467.2,352 512,352 540.8,352 566.4,358.4 585.6,371.2z M889.599,336C876.799,320,860.799,307.2,847.999,294.4L799.999,342.4C873.599,409.6 924.799,467.2 950.399,512 921.599,560 870.399,617.6 796.799,684.8 723.199,752 623.999,793.6 511.999,800 460.799,796.8 412.799,787.2 371.199,771.2L323.199,819.2C380.799,841.6 441.599,857.6 511.999,864 671.999,848 799.999,790.4 889.599,688 979.199,585.6 1024,528 1024,512 1024,496 975.999,438.4 889.599,336z</Geometry>
  <Geometry x:Key="view_offGeometry2">F1 M1024,1024z M0,0z M511.998,672C499.198,672,486.398,668.8,473.598,665.6L422.398,716.8C451.198,729.6 479.998,736 511.998,736 575.998,736 627.198,713.6 671.998,672 713.598,630.4 735.998,576 735.998,512 735.998,480 729.598,448 716.798,422.4L665.598,473.6C668.798,486.4 671.998,499.2 671.998,512 671.998,556.8 655.998,595.2 623.998,624 591.998,652.8 556.798,672 511.998,672z</Geometry>
  <DrawingGroup x:Key="view_offDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource view_offGeometry1}" />
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource view_offGeometry2}" />
  </DrawingGroup>
  <DrawingImage x:Key="view_offDrawingImage" Drawing="{StaticResource view_offDrawingGroup}" />
  <Geometry x:Key="collectiontagGeometry">F1 M1024,1024z M0,0z M256,128L256,826.88 452.032,670.016A96,96,0,0,1,571.968,670.016L768,826.816 768,128z M224,64L800,64A32,32,0,0,1,832,96L832,893.44A32,32,0,0,1,780.032,918.4L531.968,720A32,32,0,0,0,492.032,720L243.968,918.4A32,32,0,0,1,192,893.44L192,96A32,32,0,0,1,224,64</Geometry>
  <DrawingGroup x:Key="collectiontagDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource collectiontagGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="collectiontagDrawingImage" Drawing="{StaticResource collectiontagDrawingGroup}" />
  <Geometry x:Key="circleplusGeometry1">F1 M1024,1024z M0,0z M512,896A384,384,0,1,0,512,128A384,384,0,0,0,512,896 M512,960A448,448,0,1,1,512,64A448,448,0,0,1,512,960</Geometry>
  <Geometry x:Key="circleplusGeometry2">F1 M1024,1024z M0,0z M480,672L480,352A32,32,0,1,1,544,352L544,672A32,32,0,0,1,480,672</Geometry>
  <Geometry x:Key="circleplusGeometry3">F1 M1024,1024z M0,0z M352,480L672,480A32,32,0,1,1,672,544L352,544A32,32,0,0,1,352,480</Geometry>
  <DrawingGroup x:Key="circleplusDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource circleplusGeometry1}" />
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource circleplusGeometry2}" />
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource circleplusGeometry3}" />
  </DrawingGroup>
  <DrawingImage x:Key="circleplusDrawingImage" Drawing="{StaticResource circleplusDrawingGroup}" />
  <Geometry x:Key="CompassGeometry1">F1 M1024,1024z M0,0z M512,896A384,384,0,1,0,512,128A384,384,0,0,0,512,896 M512,960A448,448,0,1,1,512,64A448,448,0,0,1,512,960</Geometry>
  <Geometry x:Key="CompassGeometry2">F1 M1024,1024z M0,0z M725.888,315.008C676.48,428.672 624,513.28 568.576,568.64 513.152,624.064 428.608,676.544 315.008,725.952A12.8,12.8,0,0,1,298.112,709.12C347.648,595.392 400.128,510.848 455.424,455.488 510.784,400.192 595.328,347.712 709.056,298.176A12.8,12.8,0,0,1,725.888,315.008</Geometry>
  <DrawingGroup x:Key="CompassDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource CompassGeometry1}" />
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource CompassGeometry2}" />
  </DrawingGroup>
  <DrawingImage x:Key="CompassDrawingImage" Drawing="{StaticResource CompassDrawingGroup}" />
  <Geometry x:Key="bellGeometry1">F1 M1024,1024z M0,0z M512,64A64,64,0,0,1,576,128L576,192 448,192 448,128A64,64,0,0,1,512,64</Geometry>
  <Geometry x:Key="bellGeometry2">F1 M1024,1024z M0,0z M256,768L768,768 768,448A256,256,0,1,0,256,448z M512,128A320,320,0,0,1,832,448L832,832 192,832 192,448A320,320,0,0,1,512,128</Geometry>
  <Geometry x:Key="bellGeometry3">F1 M1024,1024z M0,0z M96,768L928,768Q960,768 960,800 960,832 928,832L96,832Q64,832 64,800 64,768 96,768 M448,896L576,896A64,64,0,0,1,448,896</Geometry>
  <DrawingGroup x:Key="bellDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource bellGeometry1}" />
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource bellGeometry2}" />
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource bellGeometry3}" />
  </DrawingGroup>
  <DrawingImage x:Key="bellDrawingImage" Drawing="{StaticResource bellDrawingGroup}" />
  <Geometry x:Key="folderdeleteGeometry">F1 M1024,1024z M0,0z M128,192L128,832 896,832 896,320 485.76,320 357.504,192z M96,128L383.872,128 512.256,256 928,256A32,32,0,0,1,960,288L960,864A32,32,0,0,1,928,896L96,896A32,32,0,0,1,64,864L64,160A32,32,0,0,1,96,128 M466.752,576L376.256,485.504 421.504,440.256 512,530.752 602.496,440.256 647.744,485.504 557.248,576 647.744,666.496 602.496,711.744 512,621.248 421.504,711.744 376.256,666.496z</Geometry>
  <DrawingGroup x:Key="folderdeleteDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FFF03A17" Geometry="{StaticResource folderdeleteGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="folderdeleteDrawingImage" Drawing="{StaticResource folderdeleteDrawingGroup}" />
  <Geometry x:Key="morefilledGeometry">F1 M1024,1024z M0,0z M176,416A112,112,0,1,1,176,640A112,112,0,0,1,176,416 M512,416A112,112,0,1,1,512,640A112,112,0,0,1,512,416 M848,416A112,112,0,1,1,848,640A112,112,0,0,1,848,416</Geometry>
  <DrawingGroup x:Key="morefilledDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource morefilledGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="morefilledDrawingImage" Drawing="{StaticResource morefilledDrawingGroup}" />
  <Geometry x:Key="collectionGeometry1">F1 M1024,1024z M0,0z M192,736L832,736 832,128 256,128A64,64,0,0,0,192,192z M256,64L864,64A32,32,0,0,1,896,96L896,768A32,32,0,0,1,864,800L160,800 128,857.536 128,192A128,128,0,0,1,256,64</Geometry>
  <Geometry x:Key="collectionGeometry2">F1 M1024,1024z M0,0z M240,800A48,48,0,1,0,240,896L832,896 832,800z M240,736L896,736 896,896A64,64,0,0,1,832,960L240,960A112,112,0,0,1,240,736 M384,128L384,378.88 480,302.08 576,378.88 576,128z M320,64L640,64 640,445.44A32,32,0,0,1,588.032,470.4L480,384 371.968,470.4A32,32,0,0,1,320,445.44z</Geometry>
  <DrawingGroup x:Key="collectionDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource collectionGeometry1}" />
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource collectionGeometry2}" />
  </DrawingGroup>
  <DrawingImage x:Key="collectionDrawingImage" Drawing="{StaticResource collectionDrawingGroup}" />
  <Geometry x:Key="folderRemoveGeometry">F1 M1024,1024z M0,0z M128,192L128,832 896,832 896,320 485.76,320 357.504,192z M96,128L383.872,128 512.256,256 928,256A32,32,0,0,1,960,288L960,864A32,32,0,0,1,928,896L96,896A32,32,0,0,1,64,864L64,160A32,32,0,0,1,96,128 M352,544L672,544 672,608 352,608z</Geometry>
  <DrawingGroup x:Key="folderRemoveDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FFFFFF00" Geometry="{StaticResource folderRemoveGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="folderRemoveDrawingImage" Drawing="{StaticResource folderRemoveDrawingGroup}" />
  <DrawingGroup x:Key="no4DrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <DrawingGroup>
      <GlyphRunDrawing ForegroundBrush="#FF5FBCFE">
        <GlyphRunDrawing.GlyphRun>
          <GlyphRun PixelsPerDip="1" BaselineOrigin="227.25,512" FontRenderingEmSize="1024" BidiLevel="0" IsSideways="False" CaretStops="1 1" ClusterMap="0" Characters="4" GlyphIndices="23" AdvanceWidths="569.5" GlyphOffsets="0,0" Language="en-us">
            <GlyphRun.GlyphTypeface>
              <GlyphTypeface FontUri="C:\WINDOWS\FONTS\ARIALBD.TTF" StyleSimulations="None" />
            </GlyphRun.GlyphTypeface>
          </GlyphRun>
        </GlyphRunDrawing.GlyphRun>
      </GlyphRunDrawing>
    </DrawingGroup>
  </DrawingGroup>
  <DrawingImage x:Key="no4DrawingImage" Drawing="{StaticResource no4DrawingGroup}" />
  <Geometry x:Key="cancelGeometry">F1 M1024,1024z M0,0z M764.288,214.592L512,466.88 259.712,214.592A31.936,31.936,0,0,0,214.592,259.712L466.752,512 214.528,764.224A31.936,31.936,0,1,0,259.648,809.408L512,557.184 764.288,809.472A31.936,31.936,0,0,0,809.408,764.352L557.12,512.064 809.408,259.712A31.936,31.936,0,1,0,764.288,214.528z</Geometry>
  <DrawingGroup x:Key="cancelDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FFF03A17" Geometry="{StaticResource cancelGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="cancelDrawingImage" Drawing="{StaticResource cancelDrawingGroup}" />
  <DrawingGroup x:Key="no6DrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <DrawingGroup>
      <GlyphRunDrawing ForegroundBrush="#FF5FBCFE">
        <GlyphRunDrawing.GlyphRun>
          <GlyphRun PixelsPerDip="1" BaselineOrigin="227.25,512" FontRenderingEmSize="1024" BidiLevel="0" IsSideways="False" CaretStops="1 1" ClusterMap="0" Characters="6" GlyphIndices="25" AdvanceWidths="569.5" GlyphOffsets="0,0" Language="en-us">
            <GlyphRun.GlyphTypeface>
              <GlyphTypeface FontUri="C:\WINDOWS\FONTS\ARIALBD.TTF" StyleSimulations="None" />
            </GlyphRun.GlyphTypeface>
          </GlyphRun>
        </GlyphRunDrawing.GlyphRun>
      </GlyphRunDrawing>
    </DrawingGroup>
  </DrawingGroup>
  <DrawingImage x:Key="no6DrawingImage" Drawing="{StaticResource no6DrawingGroup}" />
  <Geometry x:Key="tableGeometry">F1 M1024,1024z M0,0z M324.576,786.272L324.576,676.544Q324.576,668.544 319.424,663.392 314.272,658.24 306.272,658.24L123.424,658.24Q115.424,658.24 110.272,663.392 105.12,668.544 105.12,676.544L105.12,786.272Q105.12,794.272 110.272,799.424 115.424,804.576 123.424,804.576L306.272,804.576Q314.272,804.576 319.424,799.424 324.576,794.272 324.576,786.272z M324.576,566.848L324.576,457.12Q324.576,449.12 319.424,443.968 314.272,438.816 306.272,438.816L123.424,438.816Q115.424,438.816 110.272,443.968 105.12,449.12 105.12,457.12L105.12,566.848Q105.12,574.848 110.272,580 115.424,585.152 123.424,585.152L306.272,585.152Q314.272,585.152 319.424,580 324.576,574.848 324.576,566.848z M617.152,786.272L617.152,676.544Q617.152,668.544 612,663.392 606.848,658.24 598.848,658.24L416,658.24Q408,658.24 402.848,663.392 397.696,668.544 397.696,676.544L397.696,786.272Q397.696,794.272 402.848,799.424 408,804.576 416,804.576L598.848,804.576Q606.848,804.576 612,799.424 617.152,794.272 617.152,786.272z M324.576,347.424L324.576,237.696Q324.576,229.696 319.424,224.544 314.272,219.392 306.272,219.392L123.424,219.392Q115.424,219.392 110.272,224.544 105.12,229.696 105.12,237.696L105.12,347.424Q105.12,355.424 110.272,360.576 115.424,365.728 123.424,365.728L306.272,365.728Q314.272,365.728 319.424,360.576 324.576,355.424 324.576,347.424z M617.152,566.848L617.152,457.12Q617.152,449.12 612,443.968 606.848,438.816 598.848,438.816L416,438.816Q408,438.816 402.848,443.968 397.696,449.12 397.696,457.12L397.696,566.848Q397.696,574.848 402.848,580 408,585.152 416,585.152L598.848,585.152Q606.848,585.152 612,580 617.152,574.848 617.152,566.848z M909.728,786.272L909.728,676.544Q909.728,668.544 904.576,663.392 899.424,658.24 891.424,658.24L708.576,658.24Q700.576,658.24 695.424,663.392 690.272,668.544 690.272,676.544L690.272,786.272Q690.272,794.272 695.424,799.424 700.576,804.576 708.576,804.576L891.424,804.576Q899.424,804.576 904.576,799.424 909.728,794.272 909.728,786.272z M617.152,347.424L617.152,237.696Q617.152,229.696 612,224.544 606.848,219.392 598.848,219.392L416,219.392Q408,219.392 402.848,224.544 397.696,229.696 397.696,237.696L397.696,347.424Q397.696,355.424 402.848,360.576 408,365.728 416,365.728L598.848,365.728Q606.848,365.728 612,360.576 617.152,355.424 617.152,347.424z M909.728,566.848L909.728,457.12Q909.728,449.12 904.576,443.968 899.424,438.816 891.424,438.816L708.576,438.816Q700.576,438.816 695.424,443.968 690.272,449.12 690.272,457.12L690.272,566.848Q690.272,574.848 695.424,580 700.576,585.152 708.576,585.152L891.424,585.152Q899.424,585.152 904.576,580 909.728,574.848 909.728,566.848z M909.728,347.424L909.728,237.696Q909.728,229.696 904.576,224.544 899.424,219.392 891.424,219.392L708.576,219.392Q700.576,219.392 695.424,224.544 690.272,229.696 690.272,237.696L690.272,347.424Q690.272,355.424 695.424,360.576 700.576,365.728 708.576,365.728L891.424,365.728Q899.424,365.728 904.576,360.576 909.728,355.424 909.728,347.424z M982.848,164.576L982.848,786.304Q982.848,824.032 956,850.88 929.152,877.728 891.424,877.728L123.424,877.728Q85.696,877.728 58.848,850.88 32,824.032 32,786.304L32,164.576Q32,126.848 58.848,100 85.696,73.152 123.424,73.152L891.424,73.152Q929.152,73.152 956,100 982.848,126.848 982.848,164.576z</Geometry>
  <DrawingGroup x:Key="tableDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource tableGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="tableDrawingImage" Drawing="{StaticResource tableDrawingGroup}" />
  <Geometry x:Key="starfilledGeometry">F1 M1024,1024z M0,0z M283.84,867.84L512,747.776 740.16,867.712A6.4,6.4,0,0,0,749.44,860.992L705.92,606.912 890.432,427.008A6.4,6.4,0,0,0,886.912,416.128L631.808,379.008 517.76,147.904A6.4,6.4,0,0,0,506.24,147.904L392.192,379.072 137.088,416.192A6.4,6.4,0,0,0,133.568,427.072L318.08,606.976 274.496,861.056A6.4,6.4,0,0,0,283.776,867.776z</Geometry>
  <DrawingGroup x:Key="starfilledDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FFE6A23C" Geometry="{StaticResource starfilledGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="starfilledDrawingImage" Drawing="{StaticResource starfilledDrawingGroup}" />
  <Geometry x:Key="pointerGeometry">F1 M1024,1024z M0,0z M511.552,128C475.968,128,447.168,156.8,447.168,192.448L447.168,708.928 274.048,570.88A94.272,94.272,0,0,0,161.152,567.424A44.416,44.416,0,0,0,152.192,629.632L332.8,870.4A64,64,0,0,0,384,896L896,896 896,575.232A64,64,0,0,0,850.368,513.92L644.416,452.16A96,96,0,0,1,576,360.192L576,192.448C576,156.8,547.2,128,511.552,128 M359.04,556.8L383.168,576 383.168,192.448A128.448,128.448,0,1,1,640,192.448L640,360.192A32,32,0,0,0,662.784,390.848L868.8,452.608A128,128,0,0,1,960,575.232L960,896A64,64,0,0,1,896,960L384,960A128,128,0,0,1,281.6,908.8L101.056,668.032A108.416,108.416,0,0,1,128,512.512A158.272,158.272,0,0,1,313.984,520.832z</Geometry>
  <DrawingGroup x:Key="pointerDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource pointerGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="pointerDrawingImage" Drawing="{StaticResource pointerDrawingGroup}" />
  <Geometry x:Key="bellfilledGeometry">F1 M1024,1024z M0,0z M640,832A128,128,0,0,1,384,832z M832,768L134.4,768A38.4,38.4,0,0,1,134.4,691.2L192,691.2 192,448C192,293.12,302.08,163.84,448.32,134.4A64,64,0,1,1,575.68,134.4A320.128,320.128,0,0,1,832,448L832,691.2 889.6,691.2A38.4,38.4,0,0,1,889.6,768z</Geometry>
  <DrawingGroup x:Key="bellfilledDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource bellfilledGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="bellfilledDrawingImage" Drawing="{StaticResource bellfilledDrawingGroup}" />
  <Geometry x:Key="messageboxGeometry">F1 M1024,1024z M0,0z M288,384L736,384 736,448 288,448z M384,256L640,256 640,320 384,320z M131.456,512L384,512 384,640 640,640 640,512 892.544,512 721.856,192 302.144,192z M896,576L704,576 704,704 320,704 320,576 128,576 128,832 896,832z M275.776,128L748.224,128A32,32,0,0,1,776.832,145.664L956.672,505.216A32,32,0,0,1,960,519.552L960,864A32,32,0,0,1,928,896L96,896A32,32,0,0,1,64,864L64,519.552A32,32,0,0,1,67.392,505.216L247.168,145.664A32,32,0,0,1,275.776,128z</Geometry>
  <DrawingGroup x:Key="messageboxDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource messageboxGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="messageboxDrawingImage" Drawing="{StaticResource messageboxDrawingGroup}" />
  <Geometry x:Key="FilterGeometry">F1 M1024,1024z M0,0z M384,523.392L384,928A32,32,0,0,0,430.336,956.608L622.336,860.608A32,32,0,0,0,640,832L640,523.392 920.768,180.288A32,32,0,1,0,871.232,139.712L583.232,491.712A32,32,0,0,0,576,512L576,812.224 448,876.224 448,512A32,32,0,0,0,440.768,491.712L195.52,192 704,192A32,32,0,1,0,704,128L128,128A32,32,0,0,0,103.232,180.288z</Geometry>
  <DrawingGroup x:Key="FilterDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource FilterGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="FilterDrawingImage" Drawing="{StaticResource FilterDrawingGroup}" />
  <DrawingGroup x:Key="no3DrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <DrawingGroup>
      <GlyphRunDrawing ForegroundBrush="#FF5FBCFE">
        <GlyphRunDrawing.GlyphRun>
          <GlyphRun PixelsPerDip="1" BaselineOrigin="227.25,512" FontRenderingEmSize="1024" BidiLevel="0" IsSideways="False" CaretStops="1 1" ClusterMap="0" Characters="3" GlyphIndices="22" AdvanceWidths="569.5" GlyphOffsets="0,0" Language="en-us">
            <GlyphRun.GlyphTypeface>
              <GlyphTypeface FontUri="C:\WINDOWS\FONTS\ARIALBD.TTF" StyleSimulations="None" />
            </GlyphRun.GlyphTypeface>
          </GlyphRun>
        </GlyphRunDrawing.GlyphRun>
      </GlyphRunDrawing>
    </DrawingGroup>
  </DrawingGroup>
  <DrawingImage x:Key="no3DrawingImage" Drawing="{StaticResource no3DrawingGroup}" />
  <Geometry x:Key="minusGeometry">F1 M1024,1024z M0,0z M128,544L896,544A32,32,0,1,0,896,480L128,480A32,32,0,0,0,128,544</Geometry>
  <DrawingGroup x:Key="minusDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FFF03A17" Geometry="{StaticResource minusGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="minusDrawingImage" Drawing="{StaticResource minusDrawingGroup}" />
  <Geometry x:Key="arrowrightGeometry">F1 M1024,1024z M0,0z M754.752,480L160,480A32,32,0,1,0,160,544L754.752,544 521.344,777.344A32,32,0,0,0,566.656,822.656L854.656,534.656A32,32,0,0,0,854.656,489.344L566.656,201.344A32,32,0,1,0,521.344,246.656z</Geometry>
  <DrawingGroup x:Key="arrowrightDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource arrowrightGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="arrowrightDrawingImage" Drawing="{StaticResource arrowrightDrawingGroup}" />
  <Geometry x:Key="filesGeometry">F1 M1024,1024z M0,0z M128,384L128,832 896,832 896,384z M96,320L928,320A32,32,0,0,1,960,352L960,864A32,32,0,0,1,928,896L96,896A32,32,0,0,1,64,864L64,352A32,32,0,0,1,96,320 M160,192L864,192 864,256 160,256z M256,64L768,64 768,128 256,128z</Geometry>
  <DrawingGroup x:Key="filesDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FFFFFF00" Geometry="{StaticResource filesGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="filesDrawingImage" Drawing="{StaticResource filesDrawingGroup}" />
  <Geometry x:Key="lockGeometry1">F1 M1024,1024z M0,0z M224,448A32,32,0,0,0,192,480L192,864A32,32,0,0,0,224,896L800,896A32,32,0,0,0,832,864L832,480A32,32,0,0,0,800,448z M224,384L800,384A96,96,0,0,1,896,480L896,864A96,96,0,0,1,800,960L224,960A96,96,0,0,1,128,864L128,480A96,96,0,0,1,224,384</Geometry>
  <Geometry x:Key="lockGeometry2">F1 M1024,1024z M0,0z M512,544A32,32,0,0,1,544,576L544,768A32,32,0,1,1,480,768L480,576A32,32,0,0,1,512,544 M704,384L704,320A192,192,0,1,0,320,320L320,384z M512,64A256,256,0,0,1,768,320L768,448 256,448 256,320A256,256,0,0,1,512,64</Geometry>
  <DrawingGroup x:Key="lockDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource lockGeometry1}" />
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource lockGeometry2}" />
  </DrawingGroup>
  <DrawingImage x:Key="lockDrawingImage" Drawing="{StaticResource lockDrawingGroup}" />
  <Geometry x:Key="cirecleplusfilledGeometry">F1 M1024,1024z M0,0z M512,64A448,448,0,1,1,512,960A448,448,0,0,1,512,64 M473.6,473.6L326.4,473.6A38.4,38.4,0,1,0,326.4,550.4L473.6,550.4 473.6,697.6A38.4,38.4,0,0,0,550.4,697.6L550.4,550.4 697.6,550.4A38.4,38.4,0,0,0,697.6,473.6L550.4,473.6 550.4,326.4A38.4,38.4,0,1,0,473.6,326.4L473.6,473.6z</Geometry>
  <DrawingGroup x:Key="cirecleplusfilledDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource cirecleplusfilledGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="cirecleplusfilledDrawingImage" Drawing="{StaticResource cirecleplusfilledDrawingGroup}" />
  <Geometry x:Key="documentcopyGeometry">F1 M1024,1024z M0,0z M128,320L128,896 704,896 704,320z M96,256L736,256A32,32,0,0,1,768,288L768,928A32,32,0,0,1,736,960L96,960A32,32,0,0,1,64,928L64,288A32,32,0,0,1,96,256 M960,96L960,800A32,32,0,0,1,928,832L832,832 832,768 896,768 896,128 384,128 384,192 320,192 320,96A32,32,0,0,1,352,64L928,64A32,32,0,0,1,960,96 M256,672L576,672 576,736 256,736z M256,480L576,480 576,544 256,544z</Geometry>
  <DrawingGroup x:Key="documentcopyDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource documentcopyGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="documentcopyDrawingImage" Drawing="{StaticResource documentcopyDrawingGroup}" />
  <Geometry x:Key="turnonGeometry1">F1 M1024,1024z M0,0z M329.956,257.138A254.862,254.862,0,0,0,329.956,766.862L694.044,766.862A254.862,254.862,0,0,0,694.044,257.138z M329.956,184.32L694.044,184.32A327.68,327.68,0,1,1,694.044,839.68L329.956,839.68A327.68,327.68,0,1,1,329.956,184.32z</Geometry>
  <Geometry x:Key="turnonGeometry2">F1 M1024,1024z M0,0z M694.044,621.227A109.227,109.227,0,1,0,694.044,402.773A109.227,109.227,0,0,0,694.044,621.227 M694.044,694.044A182.044,182.044,0,1,1,694.044,329.956A182.044,182.044,0,0,1,694.044,694.044</Geometry>
  <DrawingGroup x:Key="turnonDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource turnonGeometry1}" />
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource turnonGeometry2}" />
  </DrawingGroup>
  <DrawingImage x:Key="turnonDrawingImage" Drawing="{StaticResource turnonDrawingGroup}" />
  <Geometry x:Key="helpfilledGeometry">F1 M1024,1024z M0,0z M926.784,480L701.312,480A192.512,192.512,0,0,0,544,322.688L544,97.216A416.064,416.064,0,0,1,926.784,480 M926.784,544A416.064,416.064,0,0,1,544,926.784L544,701.312A192.512,192.512,0,0,0,701.312,544z M97.28,544L322.752,544A192.512,192.512,0,0,0,480,701.312L480,926.784A416.064,416.064,0,0,1,97.216,544z M97.28,480A416.064,416.064,0,0,1,480,97.216L480,322.688A192.512,192.512,0,0,0,322.688,480L97.216,480z</Geometry>
  <DrawingGroup x:Key="helpfilledDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource helpfilledGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="helpfilledDrawingImage" Drawing="{StaticResource helpfilledDrawingGroup}" />
  <Geometry x:Key="zoomMinusGeometry">F1 M1024,1024z M0,0z M795.904,750.72L920.896,875.648A32,32,0,0,1,875.648,920.896L750.656,795.904A416,416,0,1,1,795.904,750.656z M480,832A352,352,0,1,0,480,128A352,352,0,0,0,480,832 M352,448L608,448A32,32,0,0,1,608,512L352,512A32,32,0,0,1,352,448</Geometry>
  <DrawingGroup x:Key="zoomMinusDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource zoomMinusGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="zoomMinusDrawingImage" Drawing="{StaticResource zoomMinusDrawingGroup}" />
  <Geometry x:Key="deletefilledGeometry">F1 M1024,1024z M0,0z M352,192L352,95.936A32,32,0,0,1,384,63.936L640,63.936A32,32,0,0,1,672,95.936L672,192 928,192A32,32,0,1,1,928,256L96,256A32,32,0,0,1,96,192z M416,192L608,192 608,128 416,128z M192,960A32,32,0,0,1,160,928L160,256 864,256 864,928A32,32,0,0,1,832,960z M416,768A32,32,0,0,0,448,736L448,416A32,32,0,0,0,384,416L384,736A32,32,0,0,0,416,768 M608,768A32,32,0,0,0,640,736L640,416A32,32,0,0,0,576,416L576,736A32,32,0,0,0,608,768</Geometry>
  <DrawingGroup x:Key="deletefilledDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FFF03A17" Geometry="{StaticResource deletefilledGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="deletefilledDrawingImage" Drawing="{StaticResource deletefilledDrawingGroup}" />
  <Geometry x:Key="expandGeometry">F1 M1024,1024z M0,0z M128,192L896,192 896,320 128,320z M128,448L640,448 640,576 128,576z M128,704L896,704 896,832 128,832z M704,352L896,512 704,640z</Geometry>
  <DrawingGroup x:Key="expandDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource expandGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="expandDrawingImage" Drawing="{StaticResource expandDrawingGroup}" />
  <Geometry x:Key="loadingGeometry">F1 M1024,1024z M0,0z M512,64A32,32,0,0,1,544,96L544,288A32,32,0,0,1,480,288L480,96A32,32,0,0,1,512,64 M512,704A32,32,0,0,1,544,736L544,928A32,32,0,1,1,480,928L480,736A32,32,0,0,1,512,704 M960,512A32,32,0,0,1,928,544L736,544A32,32,0,1,1,736,480L928,480A32,32,0,0,1,960,512 M320,512A32,32,0,0,1,288,544L96,544A32,32,0,0,1,96,480L288,480A32,32,0,0,1,320,512 M195.2,195.2A32,32,0,0,1,240.448,195.2L376.32,331.008A32,32,0,0,1,331.072,376.256L195.2,240.448A32,32,0,0,1,195.2,195.2z M647.744,647.744A32,32,0,0,1,692.992,647.744L828.8,783.552A32,32,0,0,1,783.552,828.8L647.744,692.992A32,32,0,0,1,647.744,647.744z M828.8,195.264A32,32,0,0,1,828.8,240.448L692.992,376.32A32,32,0,0,1,647.744,331.072L783.552,195.264A32,32,0,0,1,828.8,195.264 M376.256,647.744A32,32,0,0,1,376.256,692.992L240.448,828.8A32,32,0,0,1,195.2,783.552L331.008,647.744A32,32,0,0,1,376.256,647.744z</Geometry>
  <DrawingGroup x:Key="loadingDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource loadingGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="loadingDrawingImage" Drawing="{StaticResource loadingDrawingGroup}" />
  <Geometry x:Key="toolsGeometry">F1 M1024,1024z M0,0z M764.416,254.72A351.68,351.68,0,0,1,850.752,403.904L960,403.904 960,595.968 850.752,595.968A351.68,351.68,0,0,1,764.416,745.28L819.136,840 652.864,936 598.272,841.28A352.64,352.64,0,0,1,425.792,841.28L371.136,936 204.864,840 259.584,745.28A351.68,351.68,0,0,1,173.248,595.968L64,595.968 64,403.968 173.248,403.968A351.68,351.68,0,0,1,259.584,254.656L204.8,160 371.008,64 371.2,64 425.856,158.592A352.64,352.64,0,0,1,598.336,158.592L652.8,64 652.928,64 819.2,160 764.48,254.72z M704,499.968A192,192,0,1,0,320,499.968A192,192,0,0,0,704,499.968</Geometry>
  <DrawingGroup x:Key="toolsDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource toolsGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="toolsDrawingImage" Drawing="{StaticResource toolsDrawingGroup}" />
  <Geometry x:Key="calendarGeometry">F1 M1024,1024z M0,0z M128,384L128,896 896,896 896,192 768,192 768,224A32,32,0,1,1,704,224L704,192 320,192 320,224A32,32,0,0,1,256,224L256,192 128,192 128,320 896,320 896,384z M320,128L704,128 704,96A32,32,0,1,1,768,96L768,128 928,128A32,32,0,0,1,960,160L960,928A32,32,0,0,1,928,960L96,960A32,32,0,0,1,64,928L64,160A32,32,0,0,1,96,128L256,128 256,96A32,32,0,0,1,320,96z M288,512L352,512A32,32,0,0,1,352,576L288,576A32,32,0,0,1,288,512 M288,704L352,704A32,32,0,1,1,352,768L288,768A32,32,0,1,1,288,704 M480,512L544,512A32,32,0,0,1,544,576L480,576A32,32,0,0,1,480,512 M480,704L544,704A32,32,0,1,1,544,768L480,768A32,32,0,1,1,480,704 M672,512L736,512A32,32,0,1,1,736,576L672,576A32,32,0,1,1,672,512 M672,704L736,704A32,32,0,1,1,736,768L672,768A32,32,0,1,1,672,704</Geometry>
  <DrawingGroup x:Key="calendarDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource calendarGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="calendarDrawingImage" Drawing="{StaticResource calendarDrawingGroup}" />
  <Geometry x:Key="arrowdownGeometry">F1 M1024,1024z M0,0z M544,805.888L544,168A32,32,0,1,0,480,168L480,805.888 246.656,557.952A30.72,30.72,0,0,0,201.344,557.952A35.52,35.52,0,0,0,201.344,606.016L489.344,912.064A30.72,30.72,0,0,0,534.656,912.064L822.656,606.016A35.52,35.52,0,0,0,822.656,558.016A30.72,30.72,0,0,0,777.344,558.016L544,805.824z</Geometry>
  <DrawingGroup x:Key="arrowdownDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource arrowdownGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="arrowdownDrawingImage" Drawing="{StaticResource arrowdownDrawingGroup}" />
  <Geometry x:Key="arrowupGeometry">F1 M1024,1024z M0,0z M572.235,205.282L572.235,805.647A30.118,30.118,0,1,1,512,805.647L512,205.282 292.382,438.633A28.913,28.913,0,0,1,249.736,438.633A33.43,33.43,0,0,1,249.736,393.397L520.794,105.352A28.913,28.913,0,0,1,563.441,105.352L834.5,393.397A33.43,33.43,0,0,1,834.5,438.573A28.913,28.913,0,0,1,791.853,438.573L572.235,205.343z</Geometry>
  <DrawingGroup x:Key="arrowupDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource arrowupGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="arrowupDrawingImage" Drawing="{StaticResource arrowupDrawingGroup}" />
  <DrawingGroup x:Key="no8DrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <DrawingGroup>
      <GlyphRunDrawing ForegroundBrush="#FF5FBCFE">
        <GlyphRunDrawing.GlyphRun>
          <GlyphRun PixelsPerDip="1" BaselineOrigin="227.25,512" FontRenderingEmSize="1024" BidiLevel="0" IsSideways="False" CaretStops="1 1" ClusterMap="0" Characters="8" GlyphIndices="27" AdvanceWidths="569.5" GlyphOffsets="0,0" Language="en-us">
            <GlyphRun.GlyphTypeface>
              <GlyphTypeface FontUri="C:\WINDOWS\FONTS\ARIALBD.TTF" StyleSimulations="None" />
            </GlyphRun.GlyphTypeface>
          </GlyphRun>
        </GlyphRunDrawing.GlyphRun>
      </GlyphRunDrawing>
    </DrawingGroup>
  </DrawingGroup>
  <DrawingImage x:Key="no8DrawingImage" Drawing="{StaticResource no8DrawingGroup}" />
  <DrawingGroup x:Key="no5DrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <DrawingGroup>
      <GlyphRunDrawing ForegroundBrush="#FF5FBCFE">
        <GlyphRunDrawing.GlyphRun>
          <GlyphRun PixelsPerDip="1" BaselineOrigin="227.25,512" FontRenderingEmSize="1024" BidiLevel="0" IsSideways="False" CaretStops="1 1" ClusterMap="0" Characters="5" GlyphIndices="24" AdvanceWidths="569.5" GlyphOffsets="0,0" Language="en-us">
            <GlyphRun.GlyphTypeface>
              <GlyphTypeface FontUri="C:\WINDOWS\FONTS\ARIALBD.TTF" StyleSimulations="None" />
            </GlyphRun.GlyphTypeface>
          </GlyphRun>
        </GlyphRunDrawing.GlyphRun>
      </GlyphRunDrawing>
    </DrawingGroup>
  </DrawingGroup>
  <DrawingImage x:Key="no5DrawingImage" Drawing="{StaticResource no5DrawingGroup}" />
  <Geometry x:Key="frameGeometry">F1 M1024,1024z M0,0z M864,160L160,160A64,64,0,0,0,96,224L96,800A64,64,0,0,0,160,864L864,864A64,64,0,0,0,928,800L928,224A64,64,0,0,0,864,160z M160,224L864,224 864,384 160,384z M864,800L448,800 448,448 864,448 864,800z</Geometry>
  <DrawingGroup x:Key="frameDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource frameGeometry}" />
  </DrawingGroup>
  <DrawingImage x:Key="frameDrawingImage" Drawing="{StaticResource frameDrawingGroup}" />
  <Geometry x:Key="messageGeometry1">F1 M1024,1024z M0,0z M128,224L128,736A64,64,0,0,0,192,800L832,800A64,64,0,0,0,896,736L896,224z M128,160L896,160A64,64,0,0,1,960,224L960,736A128,128,0,0,1,832,864L192,864A128,128,0,0,1,64,736L64,224A64,64,0,0,1,128,160</Geometry>
  <Geometry x:Key="messageGeometry2">F1 M1024,1024z M0,0z M904,224L656.512,506.88A192,192,0,0,1,367.488,506.88L120,224z M205.056,224L415.616,464.704A128,128,0,0,0,608.32,464.704L818.944,224 205.056,224</Geometry>
  <DrawingGroup x:Key="messageDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource messageGeometry1}" />
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource messageGeometry2}" />
  </DrawingGroup>
  <DrawingImage x:Key="messageDrawingImage" Drawing="{StaticResource messageDrawingGroup}" />
  <Geometry x:Key="arrowleftGeometry1">F1 M1024,1024z M0,0z M224,480L864,480A32,32,0,1,1,864,544L224,544A32,32,0,0,1,224,480</Geometry>
  <Geometry x:Key="arrowleftGeometry2">F1 M1024,1024z M0,0z M237.248,512L502.656,777.344A32,32,0,0,1,457.344,822.656L169.344,534.656A32,32,0,0,1,169.344,489.344L457.344,201.344A32,32,0,1,1,502.656,246.656z</Geometry>
  <DrawingGroup x:Key="arrowleftDrawingGroup" ClipGeometry="M0,0 V1024 H1024 V0 H0 Z">
    <GeometryDrawing Brush="#FF424C58">
      <GeometryDrawing.Geometry>
        <RectangleGeometry RadiusX="0" RadiusY="0" Rect="0,0,1024,1024" />
      </GeometryDrawing.Geometry>
    </GeometryDrawing>
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource arrowleftGeometry1}" />
    <GeometryDrawing Brush="#FF5FBCFE" Geometry="{StaticResource arrowleftGeometry2}" />
  </DrawingGroup>
  <DrawingImage x:Key="arrowleftDrawingImage" Drawing="{StaticResource arrowleftDrawingGroup}" />
</ResourceDictionary>
```

