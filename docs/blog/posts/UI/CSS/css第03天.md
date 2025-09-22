---
title: CSS第03天
date: 2024-01-18
categories:
  - 前端开发
tags:
  - CSS
description: CSS基础学习第三天，包含传统网页布局方式、浮动和定位等重要概念
author: JerryMa
---

# css第03天

## 浮动

### 1、传统网页布局的三种方式

​	CSS 提供了三种传统布局方式(简单说,就是盒子如何进行排列顺序)：

- 普通流（标准流）

- 浮动

- 定位

  这三种布局方式都是用来摆放盒子的，盒子摆放到合适位置，布局自然就完成了。

注意：实际开发中，一个页面基本都包含了这三种布局方式（后面移动端学习新的布局方式） 。

### 2、标准流（普通流/文档流）

所谓的标准流:  就是标签按照规定好默认方式排列

1. 块级元素会独占一行，从上向下顺序排列。常用元素：div、hr、p、h1~h6、ul、ol、dl、form、table
2. 行内元素会按照顺序，从左到右顺序排列，碰到父元素边缘则自动换行。常用元素：span、a、i、em 等 

以上都是标准流布局，我们前面学习的就是标准流，标准流是最基本的布局方式。

### 3、为什么需要浮动？

​		总结： 有很多的布局效果，标准流没有办法完成，此时就可以利用浮动完成布局。 因为浮动可以改变元素标签默认的排列方式.

​		浮动最典型的应用：可以让多个块级元素一行内排列显示。

​		网页布局第一准则：**多个块级元素纵向排列找标准流，多个块级元素横向排列找浮动**。

### 4、什么是浮动？

​		float 属性用于创建浮动框，将其移动到一边，直到左边缘或右边缘触及包含块或另一个浮动框的边缘。

语法：

```css
 选择器 { float: 属性值; }
```

![1571543209934](https://gitlab.com/zw2d/blogimg/-/raw/main/pictures/2023/12/14_11_59_35_20231214-1571543209934.png)



### 5、浮动特性

加了浮动之后的元素,会具有很多特性,需要我们掌握的.

1、浮动元素会脱离标准流(脱标：浮动的盒子不再保留原先的位置)

![1571544664994](https://gitlab.com/zw2d/blogimg/-/raw/main/pictures/2023/12/14_11_59_32_20231214-1571544664994.png)

2、浮动的元素会一行内显示并且元素顶部对齐

![1571544725757](https://gitlab.com/zw2d/blogimg/-/raw/main/pictures/2023/12/14_11_59_31_20231214-1571544725757.png)

注意： 

​		浮动的元素是互相贴靠在一起的（不会有缝隙），如果父级宽度装不下这些浮动的盒子，多出的盒子会另起一行对齐。

3、浮动的元素会具有行内块元素的特性

​		浮动元素的大小根据内容来决定

​		浮动的盒子中间是没有缝隙的

### 6、浮动元素经常和标准流父级搭配使用

为了约束浮动元素位置, 我们网页布局一般采取的策略是:

​		先用标准流父元素排列上下位置, 之后内部子元素采取浮动排列左右位置.  符合网页布局第一准侧

![1571544991989](https://gitlab.com/zw2d/blogimg/-/raw/main/pictures/2023/12/14_11_59_27_20231214-1571544991989.png)

## 常见网页布局

### 浮动布局注意点

1、浮动和标准流的父盒子搭配。

先用标准流的父元素排列上下位置, 之后内部子元素采取浮动排列左右位置

2、一个元素浮动了，理论上其余的兄弟元素也要浮动。

一个盒子里面有多个子盒子，如果其中一个盒子浮动了，其他兄弟也应该浮动，以防止引起问题。

浮动的盒子只会影响浮动盒子后面的标准流,不会影响前面的标准流.

### 案例1

![image-20231214171207034](https://gitlab.com/zw2d/blogimg/-/raw/main/pictures/2023/12/14_17_12_9_20231214-image-20231214171207034.png)

```html
<style>
    div {
        width: auto;
        height: 120px;
        /* 常见的写法，以下三种都可以：
        以上方法是让块级元素水平居中，
        行内元素或者行内块元素水平居中给其父元素添加 text-align:center 即可。
        margin-left: auto; margin-right: auto;
        margin: auto;
        margin: 0 auto; */
        margin: 0 auto;
        /* margin: 20px; */
    }
    .box,
    .box1,
    .box2,
    .box3,
    .box4,
    .box5 {
        /* float: left; */
        /* 如果父级宽度装不下这些浮动的盒子， 多出的盒子会另起一行对齐。 */
        width: 300px;
    }
    .item1 {
        float: left;
        width: 100px;
        height: 100px;
        background-color: aqua;
    }
    .item2 {
        float: left;
        width: 100px;
        height: 100px;
        background-color: beige;
    }
    .item3 {
        float: left;
        width: 100px;
        height: 100px;
        background-color: blueviolet;
        /* float: right; */
    }
</style>
<!-- 先用标准流的父元素排列上下位置, 之后内部子元素采取浮动排列左右位置. 符合网页布局第一准侧. -->
<div class="box">
    <div class="item1"></div>
    <div class="item2"></div>
    <div class="item3"></div>
</div>
<div class="box1">
    <div class="item1">box1</div>
    <div class="item2">box1</div>
    <div class="item3">box1</div>
</div>
<div class="box2">
    <div class="item1">box2</div>
    <div class="item2">box2</div>
    <div class="item3">box2</div>
</div>
<div class="box3">
    <div class="item1">box3</div>
    <div class="item2">box3</div>
    <div class="item3">box3</div>
</div>
<div class="box4">
    <div class="item1">box4</div>
    <div class="item2">box4</div>
    <div class="item3">box4</div>
</div>
<div class="box5">
    <div class="item1">box5</div>
    <div class="item2">box5</div>
    <div class="item3">box5</div>
</div>
```

### 案例2 小米手机页面

![image-20231214173033431](https://gitlab.com/zw2d/blogimg/-/raw/main/pictures/2023/12/14_17_30_34_20231214-image-20231214173033431.png)

```html
<style>
    .box{
        background-color: antiquewhite;
        width: 1200px;
        height: auto;
        margin: 0 auto;
    }
    .left{
        width: 300px;
        height: 610px;
        background-color: rgb(151, 151, 214);
        float: left;
        line-height: 610px;
        text-align: center;
        font-size: 50px;
    }
    .right{
        width: 840px;
        height: 610px;
        float: left;
        padding-left: 10px;
        /* margin-left: 10px; */
        /* background-color: skyblue; */
    }
    .right div{
        width: 200px;
        height: 300px;
        float: left;
        margin: 0 10px 10px 0;
        line-height: 300px;
        text-align: center;
        font-size: 30px;
    }
    .right div{
        background-color: pink;
    }
</style>
<div class="box">
    <div class="left">
        手机新浪网
    </div>
    <div class="right">
        <div class="item1">1</div>
        <div class="item2">2</div>
        <div class="item3">3</div>
        <div class="item4">4</div>
        <div class="item5">5</div>
        <div class="item6">6</div>
        <div class="item7">7</div>
        <div class="item8">8</div>
    </div>
</div>
```



## 四、清除浮动

### 1、为什么需要清除浮动？

​		由于父级盒子很多情况下，不方便给高度，但是子盒子浮动又不占有位置，最后父级盒子高度为 0 时，就会影响下面的标准流盒子。

![1571555883628](https://gitlab.com/zw2d/blogimg/-/raw/main/pictures/2023/12/14_11_59_22_20231214-1571555883628.png)

### 2、清除浮动本质

清除浮动的本质是清除浮动元素造成的影响：浮动的子标签无法撑开父盒子的高度

注意：

- 如果父盒子本身有高度，则不需要清除浮动
- 清除浮动之后，父级就会根据浮动的子盒子自动检测高度。
- 父级有了高度，就不会影响下面的标准流了

### 3、清除浮动样式

语法：

```css
 选择器{clear:属性值;} 
```

![1571555980419](https://gitlab.com/zw2d/blogimg/-/raw/main/pictures/2023/12/14_11_59_16_20231214-1571555980419.png)

我们实际工作中， 几乎只用 clear: both;

清除浮动的策略是:  闭合浮动. 

### 4、清除浮动的多种方式

#### 4.1、额外标签法

额外标签法也称为隔墙法，是 W3C 推荐的做法。

使用方式：

​		额外标签法会在浮动元素末尾添加一个空的标签。

```html
例如 <div style="clear:both"></div>，或者其他标签（如<br />等）。
```

​		优点： 通俗易懂，书写方便

​		缺点： 添加许多无意义的标签，结构化较差

​		注意： 要求这个新的空标签必须是块级元素。

总结:

​	1、清除浮动本质是?

​			清除浮动的本质是清除浮动元素脱离标准流造成的影响

​	2、清除浮动策略是?

​			闭合浮动.  只让浮动在父盒子内部影响,不影响父盒子外面的其他盒子.

​	3、额外标签法?

​			隔墙法, 就是在最后一个浮动的子元素后面添

​	4、加一个额外标签, 添加 清除浮动样式.

​			实际工作可能会遇到,但是不常用

#### 4.2、父级添加 overflow 属性

可以给父级添加 overflow 属性，将其属性值设置为 hidden、 auto 或 scroll 。

例如：

```css
overflow:hidden | auto | scroll;
```

优点：代码简洁

缺点：无法显示溢出的部分

注意：是给父元素添加代码

#### 4.3、父级添加after伪元素

:after 方式是额外标签法的升级版。给父元素添加：

```css
 .clearfix:after {  
   content: ""; 
   display: block; 
   height: 0; 
   clear: both; 
   visibility: hidden;  
 } 
 .clearfix {  /* IE6、7 专有 */ 
   *zoom: 1;
 }   
```

优点：没有增加标签，结构更简单

缺点：照顾低版本浏览器

代表网站： 百度、淘宝网、网易等

#### 4.4、父级添加双伪元素

给父元素添加

```css
 .clearfix:before,.clearfix:after {
   content:"";
   display:table; 
 }
 .clearfix:after {
   clear:both;
 }
 .clearfix {
    *zoom:1;
 }   
```

优点：代码更简洁

缺点：照顾低版本浏览器

代表网站：小米、腾讯等

### 总结

为什么需要清除浮动？

1. 父级没高度。
2. 子盒子浮动了。
3. 影响下面布局了，我们就应该清除浮动了。

![1571556500074](https://gitlab.com/zw2d/blogimg/-/raw/main/pictures/2023/12/14_11_59_7_20231214-1571556500074.png)

## 五、PS 切图

### 1、图层切图

```html
最简单的切图方式：右击图层 → 导出 → 切片。
```

### 2、切片切图

2.1、利用切片选中图片

```
 利用切片工具手动划出
```

2.2、导出选中的图片

```html
文件菜单 → 存储为 web 设备所用格式 → 选择我们要的图片格式 → 存储 。
```

### 3、PS插件切图

​		Cutterman 是一款运行在 Photoshop 中的插件，能够自动将你需要的图层进行输出，以替代传统的手工 "导出 web 所用格式" 以及使用切片工具进行挨个切图的繁琐流程。

官网：http://www.cutterman.cn/zh/cutterman

注意：Cutterman 插件要求你的 PS 必须是完整版，不能是绿色版，所以大家需要安装完整版本。

![1571556821045](https://gitlab.com/zw2d/blogimg/-/raw/main/pictures/2023/12/14_11_58_59_20231214-1571556821045.png)