---
title: 使用 XAML 格式化工具：XAML Styler
date: 2024-07-16
categories:
  - windows程序
  - 开发工具
tags:
  - XAML
  - WPF
  - 格式化
  - 开发工具
  - Visual Studio
description: XAML Styler格式化工具的使用方法，帮助规范和美化XAML代码格式
author: JerryMa
---
# 使用 XAML 格式化工具：XAML Styler

## 1. XAML 的问题[#](https://www.cnblogs.com/dino623/p/XAML_Styler.html#66162767)

刚入门 WPF/UWP 之类的 XAML 平台，首先会接触到 XAML 这一新事物。初学 XAML 时对它的印象可以归纳为一个词：**一坨**。

随着我在 XAML 平台上工作的时间越来越长，我对 XAML 的了解就越来越深入，从语法、约束、扩展性等方方面面，我明白到 XAML 是桌面开发平台的一个最佳解决方案。这时候我已经对 XAML 有了改观，我重新用一个词归纳了我对它的印象：**一大坨**。

没错，这时候我已经是一个成熟的 XAML 工人了，经过我熟练的双手产生了一坨又一坨 XAML，它们成长相遇结合繁衍，变成了一大坨又一大坨 XAML。

明明 XAML 这么一大坨已经够艰难了，偏偏对于它的格式化微软爸爸也没给个好的方案。对我来说，XAML 格式化主要的难题是下面几个：

- 如果所有属性都写在同一行，它太宽了很难看到后面的属性
- 如果每个属性单独一行，它又太长了很难看清楚它的结构
- 属性之间没有排序，重要属性的属性找起来很困难
- 团队没有统一的标准，不小心格式化一下代码的话全部都会变，CodeReview 烦死个人

如果不想得过且过忍受上述这些问题的话，可以试试用 XAML Styler 这个工具，它正好解决了我最想解决的问题。

## 2. 安装 XAML Styler[#](https://www.cnblogs.com/dino623/p/XAML_Styler.html#2511504520)

XAML Styler 是一个 VisualStudio插件（也可用于其它 IDE），这是它在 Github 上的地址：

https://github.com/Xavalon/XamlStyler

在这里你可以找到具体的文档，而这篇文章我只介绍我关心的其中几个属性，不一定满足到你。

在 VisualStudio 的管理扩展窗口中，输入 XamlStyle 搜索，点击“下载”然后关闭 VisualStudio 即可完成安装。

[![img](http://image.jerryma.xyz//images/20240903-38937-20210120232751020-1871898498.png)](https://img2020.cnblogs.com/blog/38937/202101/38937-20210120232751020-1871898498.png)

安装完成后重启 Visual Studio，可以在“选项”窗口中看到它的配置：

[![img](http://image.jerryma.xyz//images/20240903-38937-20210120232810578-324783095.png)](https://img2020.cnblogs.com/blog/38937/202101/38937-20210120232810578-324783095.png)

之后，每次在 XAML 编辑器中执行保存都会自动进行格式化操作。你也可以在 XAML 编辑器的右键菜单选择 Format XAML 或使用快捷键进行格式化。

[![img](http://image.jerryma.xyz//images/20240903-38937-20210120232822232-333821272.png)](https://img2020.cnblogs.com/blog/38937/202101/38937-20210120232822232-333821272.png)

## 3. 格式化[#](https://www.cnblogs.com/dino623/p/XAML_Styler.html#1826140594)

XAML 的格式主要有两种方式：所有属性放一行和每个属性单独一行。

如果选择所有属性放一行的时候，XAML 结构清晰，结构严谨，段落分明，而且文件也很短。

可是万一很多属性问题就出来了，一行 XAML 会变得很长。而且看看下面两个 ContentPresenter，同样都有 Margin 属性、HorizontalAlignment 属性，VerticalAlignment 属性，RecognizesAccessKey 属性，SnapsToDevicePixels 顺序ing，但你能看到第二个 ContentPresenter 后面偷偷塞了个 Margin 吗：

```XML
Copy<ContentPresenter Margin="{TemplateBinding Padding}" HorizontalAlignment="{TemplateBinding HorizontalContentAlignment}" VerticalAlignment="{TemplateBinding VerticalContentAlignment}" RecognizesAccessKey="True" SnapsToDevicePixels="{TemplateBinding SnapsToDevicePixels}"/>
<ContentPresenter Margin="{TemplateBinding Padding}" HorizontalAlignment="{TemplateBinding HorizontalContentAlignment}" VerticalAlignment="{TemplateBinding VerticalContentAlignment}" RecognizesAccessKey="True" SnapsToDevicePixels="{TemplateBinding SnapsToDevicePixels}" Margin="40"/>
```

如果在 VisualStudio 中“文本编辑器->XAML->格式化->间距->特性间距”这个选项中选择了“将各个属性分别放置”：

[![img](http://image.jerryma.xyz//images/20240903-38937-20210120232837859-1653416211.png)](https://img2020.cnblogs.com/blog/38937/202101/38937-20210120232837859-1653416211.png)

格式化文档后上面的 XAML 就会变成这样：

```XML
Copy<ContentPresenter Margin="{TemplateBinding Padding}"
                  HorizontalAlignment="{TemplateBinding HorizontalContentAlignment}"
                  VerticalAlignment="{TemplateBinding VerticalContentAlignment}"
                  RecognizesAccessKey="True"
                  SnapsToDevicePixels="{TemplateBinding SnapsToDevicePixels}" />
<ContentPresenter Margin="{TemplateBinding Padding}"
                  HorizontalAlignment="{TemplateBinding HorizontalContentAlignment}"
                  VerticalAlignment="{TemplateBinding VerticalContentAlignment}"
                  RecognizesAccessKey="True"
                  SnapsToDevicePixels="{TemplateBinding SnapsToDevicePixels}"
                  Margin="40" />
```

每个属性单独一行不仅不会看漏属性，而且编辑器本身也不会有横向和纵向两种方向的移动，只有从上到下的移动，这就舒服多了。

可是大部分情况下每个属性分行放置会破坏原本清晰的 XAML 层次结构，例如下面这种本来好好的 XAML:

```XML
Copy<Setter Property="FontWeight" Value="Normal" />
<Setter Property="UseSystemFocusVisuals" Value="True" />
<Setter Property="FocusVisualMargin" Value="-3" />
<Setter Property="Height" Value="50" />
<Setter Property="Width" Value="50" />
<Setter Property="Maximum" Value="1" />
```

变成这样：

```XML
Copy<Setter Property="FontWeight"
        Value="Normal" />
<Setter Property="UseSystemFocusVisuals"
        Value="True" />
<Setter Property="FocusVisualMargin"
        Value="-3" />
<Setter Property="Height"
        Value="50" />
<Setter Property="Width"
        Value="50" />
<Setter Property="Maximum"
        Value="1" />
```

这种风格优雅得像诗歌
我偶尔称为豆瓣风
一行变两行
两行变四行
本来
一页看得完
的代码
变成
两页才看得完
也是够
麻烦的。

XAML Styler 很好地解决了这个问题，它通过 “Attribute tolerance” 属性控制每一行的容许的最多的属性数量，如果一个元素的属性数量少于设定值，那就放在一行，如果超过就所有属性单独一行。通常我将这个属性设置为 `2`，再配合 “Keep first attribute on same line = true” 的设置，可以做到下面这种格式化效果：

```XML
Copy<SolidColorBrush x:Key="NormalTextColor" Color="#2E2F33" />
<SolidColorBrush x:Key="PrimaryColor" Color="#FFED5B8C" />
<SolidColorBrush x:Key="LineColor" Color="#E1E1E1" />
<SolidColorBrush x:Key="TransparentBackground" Color="Transparent" />

<ControlTemplate x:Key="CompletedTemplate" TargetType="ContentControl">
    <Grid x:Name="CompletedElement" Margin="-2">
        <control:DropShadowPanel HorizontalContentAlignment="Stretch"
                                 VerticalContentAlignment="Stretch"
                                 BlurRadius="8"
                                 OffsetX="0"
                                 OffsetY="0"
                                 Color="#FFED5B8C">
            <Ellipse x:Name="CompletedRectangle" Fill="{StaticResource PrimaryColor}" />
        </control:DropShadowPanel>
    </Grid>
</ControlTemplate>
```

这样就可以兼顾两种格式化的优点。

## 4. 排序[#](https://www.cnblogs.com/dino623/p/XAML_Styler.html#3430790445)

如果元素有多个属性，要找到它的主要属性（通常是 Name 和 Grid.Row）需要颇费一番功夫。XAML Styler 根据一个可设定的规则自动将元素的各个属性排序，这个规则如下：

```JSON
Copy"AttributeOrderingRuleGroups": [
    "x:Class",
    "xmlns, xmlns:x",
    "xmlns:*",
    "x:Key, Key, x:Name, Name, x:Uid, Uid, Title",
    "Grid.Row, Grid.RowSpan, Grid.Column, Grid.ColumnSpan, Canvas.Left, Canvas.Top, Canvas.Right, Canvas.Bottom",
    "Width, Height, MinWidth, MinHeight, MaxWidth, MaxHeight",
    "Margin, Padding, HorizontalAlignment, VerticalAlignment, HorizontalContentAlignment, VerticalContentAlignment, Panel.ZIndex",
    "*:*, *",
    "PageSource, PageIndex, Offset, Color, TargetName, Property, Value, StartPoint, EndPoint",
    "mc:Ignorable, d:IsDataSource, d:LayoutOverrides, d:IsStaticText",
    "Storyboard.*, From, To, Duration"
],
```

排序结果大致如下：

```XML
Copy<Button x:Name="Show"
        Grid.Row="1"
        Padding="40,20"
        HorizontalAlignment="Center"
        VerticalAlignment="Center"
        Background="#00aef1"
        Content="Show"
        Foreground="White"
        Style="{StaticResource BubbleButtonStyle}" />
```

另外，我不喜欢它自动将 VisualStateManager 排序到后面，虽然这个排序合理，但不符合我的习惯，所以要将 “Record visual state manager” 设置为 None。

## 5. 统一标准[#](https://www.cnblogs.com/dino623/p/XAML_Styler.html#1986661914)

最后，就算自己做好了格式化，团队中的其它成员使用了不同的格式化标准也会引起很多问题。针对这个问题 Xaml Styler 也提供了解决方案。

在项目的根目录创建一个名为“Settings.XamlStyler”的文件，内容参考这个网址：https://github.com/Xavalon/XamlStyler/wiki/External-Configurations 中的 **Default Configuration**。有了这个配置文件，XAML Styler 就会根据它而不是全局配置进行格式化，作为项目的统一格式化标准。

