---
title: HTML标签
date: 2024-03-20
categories:
  - 前端开发
  - HTML
tags:
  - HTML
  - 标签
  - 前端基础
  - Web开发
description: HTML基础标签的使用方法，包括标题标签、段落标签等前端开发基础知识
author: JerryMa
---

# HTML 标签（下）

## 表格标签

`表格不是用来布局页面的,而是用来展示数据的.`

### 表格基本用法

<table>
      <tr>
        <td>单元表格里的文字1</td>
        <td>单元表格里的文字2</td>
        <td>单元表格里的文字3</td>
        <td>单元表格里的文字4</td>
      </tr>
      <tr>
        <td>单元表格里的文字11</td>
        <td>单元表格里的文字21</td>
        <td>单元表格里的文字31</td>
        <td>单元表格里的文字41</td>
      </tr>

`<table>
      <tr>
        <td>单元表格里的文字1</td>
        <td>单元表格里的文字2</td>
        <td>单元表格里的文字3</td>
        <td>单元表格里的文字4</td>
      </tr>
      <tr>
        <td>单元表格里的文字11</td>
        <td>单元表格里的文字21</td>
        <td>单元表格里的文字31</td>
        <td>单元表格里的文字41</td>
      </tr>
    </table>`

1.<table> </table> 是用于定义表格的标签。
2.<tr> </tr> 标签用于定义表格中的行，必须嵌套在 <table> </table>标签中。
3.<td> </td> 用于定义表格中的单元格，必须嵌套在<tr></tr>标签中。
4.字母 td 指表格数据（table data），即数据单元格的内容。

一般表头单元格位于表格的第一行或第一列，表头单元格里面的文本内容加粗居中显示.
<th> 标签表示 HTML 表格的表头部分(table head 的缩写)

### 表格属性

表格标签这部分属性我们实际开发我们不常用，后面通过 CSS 来设置.
目的有2个:
1.记住这些英语单词,后面 CSS 会使用.
2.直观感受表格的外观形态.

| 属性名      | 属性值              | 描述                                      |
| ----------- | ------------------- | ----------------------------------------- |
| align       | left、center、right | 规定表格相对周围元素的对齐方式            |
| border      | 1或“”               | 固定表格单元是否拥有边框，默认没有边框    |
| cellpadding | 像素值              | 规定单元边沿与其内容之间的空白，默认1像素 |
| cellspacing | 像素值              | 规定单元格之间的空白，默认为2像素         |
| width       | 像素值或百分比      | 规定表格的宽度                            |

### 案例

![](https://gitlab.com/zw2d/blogimg/-/raw/main/pictures/2023/12/11_14_13_25_20231211-20231211141322.png)

```html
 <table align="center" width="500" height="249" border="1" cellspacing="0">
     <thead>
         <tr>
             <th>排名</th>
             <th>关键词</th>
             <th>趋势</th>
             <th>进入搜索</th>
             <th>最近七日</th>
             <th>相关链接</th>
         </tr>
     </thead>
     <tbody>
         <tr>
             <td>1</td>
             <td>鬼吹灯</td>
             <td><img src="down.jpg" /></td>
             <td>456</td>
             <td>123</td>
             <td>
                 <a href="#">贴吧</a> <a href="#">图片</a> <a href="#">百科</a>
             </td>
         </tr>

         <tr>
             <td>1</td>
             <td>鬼吹灯</td>
             <td><img src="down.jpg" /></td>
             <td>456</td>
             <td>123</td>
             <td>
                 <a href="#">贴吧</a> <a href="#">图片</a> <a href="#">百科</a>
             </td>
         </tr>
         <tr>
             <td>3</td>
             <td>西游记</td>
             <td><img src="up.jpg" /></td>
             <td>456</td>
             <td>123</td>
             <td>
                 <a href="#">贴吧</a> <a href="#">图片</a> <a href="#">百科</a>
             </td>
         </tr>
         <tr>
             <td>1</td>
             <td>鬼吹灯</td>
             <td><img src="down.jpg" /></td>
             <td>456</td>
             <td>123</td>
             <td>
                 <a href="#">贴吧</a> <a href="#">图片</a> <a href="#">百科</a>
             </td>
         </tr>
         <tr>
             <td>1</td>
             <td>鬼吹灯</td>
             <td><img src="down.jpg" /></td>
             <td>456</td>
             <td>123</td>
             <td>
                 <a href="#">贴吧</a> <a href="#">图片</a> <a href="#">百科</a>
             </td>
         </tr>
         <tr>
             <td>1</td>
             <td>鬼吹灯</td>
             <td><img src="down.jpg" /></td>
             <td>456</td>
             <td>123</td>
             <td>
                 <a href="#">贴吧</a> <a href="#">图片</a> <a href="#">百科</a>
             </td>
         </tr>
     </tbody>
</table>
```

在表格标签中，分别用：<thead>标签 表格的头部区域、<tbody>标签 表格的主体区域. 这样可以更好的分清表格结构。

### 表格结构标签

1. <thead></thead>：用于定义表格的头部。<thead> 内部必须拥有 <tr> 标签。 一般是位于第一行。
2. <tbody></tbody>：用于定义表格的主体，主要用于放数据本体 。
3. 以上标签都是放在 <table></table> 标签中。

### 合并单元格

#### 合并单元格的方式

* 跨行合并：rowspan="合并单元格的个数"
* 跨列合并：colspan="合并单元格的个数"



* 跨行：最上侧单元格为目标单元格, 写合并代码
* 跨列：最左侧单元格为目标单元格, 写合并代码

`<table class="table-interview" align="center" width="600" height="200" border="1" cellspacing="0">
      <thead>
        <tr>
          <th colspan="5" text-size="5" align="center">个人简历</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>姓&nbsp;&nbsp;&nbsp; 名:</td>
          <td>&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;   </td>
          <td>性&nbsp;&nbsp;&nbsp; 别:</td>
          <td>&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;   </td>
          <td rowspan="4">&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;照片&nbsp;&nbsp;&nbsp;</td>
        </tr>
        <tr>
          <td>婚姻状况：</td>
          <td></td>
          <td>出生年月：</td>
          <td></td>
        </tr>
        <tr>
          <td>民&nbsp;&nbsp;&nbsp; 族：</td>
          <td></td>
          <td>政治面貌:</td>
          <td></td>
        </tr>
        <tr>
          <td>身&nbsp;&nbsp;&nbsp; 高：</td>
          <td></td>
          <td>学&nbsp;&nbsp;&nbsp; 历：</td>
          <td></td>
        </tr>
      </tbody>
    </table>`

<table class="table-interview" align="center" width="600" height="200" border="1" cellspacing="0">
      <thead>
        <tr>
          <th colspan="5" text-size="5" align="center">个人简历</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>姓&nbsp;&nbsp;&nbsp; 名:</td>
          <td>&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;   </td>
          <td>性&nbsp;&nbsp;&nbsp; 别:</td>
          <td>&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;   </td>
          <td rowspan="4">&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;照片&nbsp;&nbsp;&nbsp;</td>
        </tr>
        <tr>
          <td>婚姻状况：</td>
          <td></td>
          <td>出生年月：</td>
          <td></td>
        </tr>
        <tr>
          <td>民&nbsp;&nbsp;&nbsp; 族：</td>
          <td></td>
          <td>政治面貌:</td>
          <td></td>
        </tr>
        <tr>
          <td>身&nbsp;&nbsp;&nbsp; 高：</td>
          <td></td>
          <td>学&nbsp;&nbsp;&nbsp; 历：</td>
          <td></td>
        </tr>
      </tbody>
    </table>

### 表格总结

我们学习了

* table 标签
* tr 行 标签
* td 单元格 标签
* th 表头单元格 标签
* thead 表格头部区域标签

## 列表标签

表格是用来显示数据的，那么列表就是用来`布局`的。
列表最大的特点就是整齐、整洁、有序，它作为布局会更加自由和方便。
根据使用情景不同，列表可以分为三大类：无序列表、有序列表和自定义列表。

### 无序列表

1.无序列表的各个列表项之间没有顺序级别之分，是并列的。
2.<ul></ul> 中只能嵌套 <li></li>，直接在 <ul></ul> 标签中输入其他标签或者文字的做法是不被允许的。
3.<li> 与 </li> 之间相当于一个容器，可以容纳所有元素。
4.无序列表会带有自己的样式属性，但在实际使用时，我们会使用 CSS 来设置。

### 有序列表

1.<ol></ol>中只能嵌套<li></li>，直接在<ol></ol>标签中输入其他标签或者文字的做法是不被允许的。
2.<li> 与 </li>之间相当于一个容器，可以容纳所有元素。
3.有序列表会带有自己样式属性，但在实际使用时，我们会使用 CSS 来设置。

<strong>li最小，ul和ol都包含li</strong>

### 自定义列表

在 HTML 标签中，<dl> 标签用于定义描述列表（或定义列表），该标签会与 <dt>（定义项目/名字）和 <dd>（描述每一个项目/名字）一起使用。

其基本语法如下：

1.<dl></dl> 里面只能包含 <dt> 和 <dd>。
2.<dt> 和 <dd>个数没有限制，经常是一个<dt> 对应多个<dd>。

```html
<dl>
    <dt>关注我们</dt>
    <dd>新浪微博</dd>
    <dd>官方微信</dd>
    <dd>联系我们</dd>
    <dt>关注我们</dt>
    <dd>新浪微博</dd>
    <dd>官方微信</dd>
    <dd>联系我们</dd>
</dl>
```



## 表单标签

### <input>表单元素

type 属性的属性值及其描述如下：

![](https://gitlab.com/zw2d/blogimg/-/raw/main/pictures/2023/12/11_15_46_42_20231211-20231211154640.png)

其它属性：

![](https://gitlab.com/zw2d/blogimg/-/raw/main/pictures/2023/12/11_15_51_49_20231211-20231211155147.png)

1.name 和value 是每个表单元素都有的属性值,主要给后台人员使用.
2.name 表单元素的名字, 要求 单选按钮和复选框要有相同的name值.
3.checked属性主要针对于单选按钮和复选框, 主要作用一打开页面,就要可以默认选中某个表单元素.
4.maxlength 是用户可以在表单元素输入的最大字符数, 一般较少使用.



## 综合案例

<table>
      <tr>
        <td>性别</td>
        <td>
          <div class="checkbox">
            <input type="radio" name="sex" value="男" checked="checked" />男
            <input type="radio" name="sex" value="女" />女
          </div>
        </td>
      </tr>
      <tr>
        <td>生日</td>
        <td>
          <div class="birthday">
            <select>
              <option>--请选择年--</option>
            </select>
            <select>
              <option>--请选择月--</option>
            </select>
            <select>
              <option>--请选择日--</option>
            </select>
          </div>
        </td>
      </tr>
      <tr>
        <td>所在地区</td>
        <td><input type="" class="address" value="北京思密达" /></td>
      </tr>
      <tr>
        <td>婚姻状况：</td>
        <td>
          <div class="marry">
            <input
              type="radio"
              name="marryied"
              value="未婚"
              checked="checked"
            />未婚 <input type="radio" name="marryied" value="已婚" />已婚
            <input type="radio" name="marryied" value="离婚" />离婚
          </div>
        </td>
      </tr>
      <tr>
        <td>学历</td>
        <td><input type="" class="education" value="幼儿园" /></td>
      </tr>
      <tr>
        <td>喜欢的类型</td>
        <td>
          <input type="checkbox" name="like" value="帅哥" />帅哥
          <input type="checkbox" name="like" value="妩媚的" />妩媚的
          <input type="checkbox" name="like" value="可爱的" />可爱的
          <input type="checkbox" name="like" value="美女" />美女
          <input type="checkbox" name="like" value="都喜欢" />都喜欢
        </td>
      </tr>
      <tr>
        <td>自我介绍</td>
        <td>
          <textarea>自我介绍</textarea>
        </td>
      </tr>
      <tr>
        <td></td>
        <td>
          <input type="button" value="免费注册" />
        </td>
      </tr>
     <tr>
        <td></td>
        <td>
          <input type="checkbox" checked="checked" />
          我同意注册条款和会员加入标准
        </td>
      </tr>
      <tr>
        <td></td>
        <td><a href="#">我是会员,立即登录</a></td>
      </tr>
      <tr>
        <td></td>
        <td><h1>我承诺</h1>
            <ul>
                <li>年满18岁、单身</li>
                <li>抱着严肃的态度</li>
                <li>真诚寻找另一半</li>
            </ul>
        </td>
      </tr>
    </table>



