---
title: CSS学习第二天
date: 2024-02-28
categories:
  - 前端开发
  - CSS
tags:
  - CSS
  - 权重
  - 继承
  - 前端基础
description: CSS基础知识第二天学习内容，包含CSS权重、继承、层叠等重要概念
author: JerryMa
---

# CSS学习第二天

## CSS 的三大特性

CSS 有三个非常重要的三个特性：层叠性、继承性、优先级。

### 优先级

1. 权重是有4组数字组成,但是不会有进位。
2. 可以理解为类选择器永远大于元素选择器, id选择器永远大于类选择器,以此类推..
3. 等级判断从左向右，如果某一位数值相同，则判断下一位数值。
4. 可以简单记忆法: `通配符和继承权重为0, 标签选择器为1,类(伪类)选择器为 10, id选择器 100, 行内样式表为 1000, !important 无穷大`.
5. 继承的权重是0， 如果该元素没有直接选中，不管父元素权重多高，子元素得到的权重都是 0。

### 层叠性

CSS 层叠性口诀：长江后浪推前浪，前浪死在沙滩上。

* 样式冲突，遵循的原则是就近原则，哪个样式离结构近，就执行哪个样式
* 样式不冲突，不会层叠

### 继承性

继承性口诀：`龙生龙，凤生凤，老鼠生的孩子会打洞`

CSS中的继承: 子标签会继承父标签的某些样式，如文本颜色和字号。简单的理解就是：子承父业。

## 盒子模型

网页布局的核心本质： `就是利用 CSS 摆盒子`。

所谓 盒子模型：就是把 HTML 页面中的布局元素看作是一个矩形的盒子，也就是一个盛装内容的容器。
CSS 盒子模型本质上是一个盒子，封装周围的 HTML 元素，它包括：边框、外边距、内边距、和 实际内容

![](https://gitlab.com/zw2d/blogimg/-/raw/main/pictures/2023/12/14_9_26_54_20231214-20231214092652.png)



### 边框（border）

border可以设置元素的边框。边框有三部分组成:边框宽度(粗细) 边框样式 边框颜色

```css
border : border-width || border-style || border-color
```

| 属性         | 作用                   |
| ------------ | ---------------------- |
| border-width | 定义边框粗细，单位是px |
| border-style | 边框的样式             |
| border-color | 边框颜色               |

边框样式 border-style 可以设置如下值：

* none：没有边框即忽略所有边框的宽度（默认值）
* solid：边框为单实线(最为常用的)
* dashed：边框为虚线
* dotted：边框为点线

demo:请给一个 200*200 的盒子，设置上边框为红色，其余边框为蓝色（提示：一定注意边框的层叠性）

```html
<style>
    .box {
        width: 200px;
        height: 200px;
        border: 1px solid blue;
        border-top: 1px solid red;
    }
</style>
<div class="box"></div>
```

### 内边距（padding）

padding 属性用于设置内边距，即边框与内容之间的距离。

| 属性                        | 表达意思                                                     |
| --------------------------- | ------------------------------------------------------------ |
| padding:5px;                | 1个值，代表上下左右都有5像素内边距                           |
| padding:5px 10px;           | 2个值，代表上下内边距是5像素，左右内边距是10像素；           |
| padding:5px 10px 20px;      | 3个值，代表上内边距5像素，左边内边距10像素，下内边距20像素； |
| padding:5px 10px 20px 30px; | 4个值，上、右、下、左，遵循顺时针                            |

#### 案例

![image-20231214103810762](https://gitlab.com/zw2d/blogimg/-/raw/main/pictures/2023/12/14_10_38_12_20231214-image-20231214103810762.png)

```html
<style>
    .nav {
        height: 41px;
        border-top: 3px solid #ff8500;
        border-bottom: 1px solid #edeef0;
        background-color: #fcfcfc;
        line-height: 41px;
    }
    .nav a {
        /* a属于行内元素 此时必须要转换 行内块元素 */
        display: inline-block;
        height: 41px;
        padding: 0 20px;
        font-size: 12px;
        color: #4c4c4c;
        text-decoration: none;
    }
    .nav a:hover {
        background-color: #eee;
        color: #ff8500;
    }
</style>
<div class="nav">
    <a href="">设为首页</a>
    <a href="">手机新浪网</a>
    <a href="">移动客户端</a>
    <a href="">博客</a>
    <a href="">微博</a>
    <a href="">关注我们</a>
</div>
```

可以把display改成block和inline看看效果。

#### 案例2

![image-20231214113428560](https://gitlab.com/zw2d/blogimg/-/raw/main/pictures/2023/12/14_11_34_30_20231214-image-20231214113428560.png)

```html
<style>
    body {
    background-color: #f5f5f5;
    }
    .product {
    width: 298px;
    height: 415px;
    background-color: #fff;
    /* 让块级的盒子水平居中对齐 */
    margin: 100px auto;
    }
    .product .review {
    height: 70px;
    font-size: 14px;
    padding: 0 28px;
    margin-top: 30px;
    }
    .product img {
    /* 图片的宽度和父亲一样宽 */
    width: 100%;
    }
    .appraise {
    font-size: 12px;
    color: #b0b0b0;
    margin-top: 20px;
    padding: 0 28px;
    }
    .info {
    font-size: 14px;
    margin-top: 15px;
    padding: 0 28px;
    }
    .info span {
    color: #ff6700;    
    }
    .info em {
    font-style: normal;
    color: #ebe4e0;
    margin: 0 6px 0 15px;
    }
</style>
<div class="product">
    <img src="images/img.jpg" />
    <p class="review">快递牛，整理不错蓝牙可以说秒连。红米给力</p>
    <div class="appraise">来自于117384232的评价</div>
    <div class="info">
        Redmi AirDots真无线...
        <em>|</em>
        <span>99.00元</span>
    </div>
</div>
```

### 圆角边框

在 CSS3 中，新增了圆角边框样式，这样我们的盒子就可以变圆角了。

border-radius 属性用于设置元素的外边框圆角。

语法：

```css
border-radius:length;
```

* 参数值可以为数值或百分比的形式
* 如果是正方形，想要设置为一个圆，把数值修改为高度或者宽度的一半即可，或者直接写为 50%
* 该属性是一个简写属性，可以跟四个值，分别代表左上角、右上角、右下角、左下角
* 分开写：border-top-left-radius、border-top-right-radius、border-bottom-right-radius 和border-bottom-left-radius
* 兼容性 ie9+ 浏览器支持, 但是不会影响页面布局,可以放心使用.

### 盒子阴影

CSS3 中新增了盒子阴影，我们可以使用 box-shadow 属性为盒子添加阴影。

语法：

```css
box-shadow: h-shadow v-shadow blur spread color inset;
```

![image-20231214115203023](https://gitlab.com/zw2d/blogimg/-/raw/main/pictures/2023/12/14_11_52_4_20231214-image-20231214115203023.png)

`注意：`

1.默认的是外阴影(outset), 但是不可以写这个单词,否则造成阴影无效
2.盒子阴影不占用空间，不会影响其他盒子排列。

### 文字阴影

在 CSS3 中，我们可以使用 text-shadow 属性将阴影应用于文本。

语法：

```css
text-shadow: h-shadow v-shadow blur color;
```

![image-20231214115243978](https://gitlab.com/zw2d/blogimg/-/raw/main/pictures/2023/12/14_11_52_45_20231214-image-20231214115243978.png)