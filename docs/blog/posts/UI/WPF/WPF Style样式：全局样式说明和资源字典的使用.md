---
title: WPF Style样式：全局样式说明和资源字典的使用
date: 2024-10-21
categories:
  - windows程序
tags:
  - WPF
  - Style
  - 资源字典
  - UI样式
description: WPF中Style样式的全局应用方法和资源字典的使用技巧
author: JerryMa
---

# Style样式：全局样式说明和资源字典的使用

![image-20241021184738550](http://image.jerryma.xyz//images/20241021-image-20241021184738550.png)

## `结果如下所示`：

![image-20241021184756790](http://image.jerryma.xyz//images/20241021-image-20241021184756790.png)

## 增加样式字典方式如下所示：

![image-20241021184556692](http://image.jerryma.xyz//images/20241021-image-20241021184556692.png)

`ButtonStyle.xaml`

```csharp
<ResourceDictionary xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation" xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">
    <Style TargetType="Button">
        <Setter Property="Background" Value="WhiteSmoke" />
        <Setter Property="Foreground" Value="Black" />
        <Setter Property="FontSize" Value="20" />
        <Setter Property="Margin" Value="10,20" />
    </Style>
    <Style
        x:Key="LoginStyle"
        BasedOn="{StaticResource {x:Type Button}}"
        TargetType="Button">
        <Setter Property="Background" Value="Green" />
    </Style>
    <Style
        x:Key="QuitStyle"
        BasedOn="{StaticResource {x:Type Button}}"
        TargetType="Button">
        <Setter Property="Background" Value="Red" />
    </Style>

    <Style x:Key="MyButtonStyle" TargetType="Button">
        <Setter Property="Background" Value="LightBlue" />
        <Setter Property="Foreground" Value="Black" />
        <Setter Property="FontSize" Value="50" />
        <Setter Property="Margin" Value="10,20" />
    </Style>

    <Style
        x:Key="MyButtonStyle2"
        BasedOn="{StaticResource MyButtonStyle}"
        TargetType="Button">
        <Setter Property="Background" Value="LightGray" />
    </Style>

    <Style
        x:Key="MyButtonStyle3"
        BasedOn="{StaticResource MyButtonStyle}"
        TargetType="Button">
        <Setter Property="FontSize" Value="30" />
        <Setter Property="Background" Value="DarkKhaki" />
    </Style>
</ResourceDictionary>
```

`App.xaml`

```csharp
<Application
    x:Class="ButtonStyle.App"
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
    xmlns:local="clr-namespace:ButtonStyle"
    StartupUri="MainWindow.xaml">
    <Application.Resources>
        <ResourceDictionary>
            <ResourceDictionary.MergedDictionaries>
                <ResourceDictionary Source="ButtonStyle.xaml" />
            </ResourceDictionary.MergedDictionaries>
        </ResourceDictionary>
    </Application.Resources>
</Application>
```

`MainWindow.xaml`

```csharp
<Window
    x:Class="ButtonStyle.MainWindow"
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
    xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
    xmlns:local="clr-namespace:ButtonStyle"
    xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
    Title="MainWindow"
    Width="800"
    Height="450"
    mc:Ignorable="d">
    <Grid>
        <StackPanel>
            <Button Content="登录" Style="{StaticResource LoginStyle}" />
            <Button Content="注册" Style="{StaticResource QuitStyle}" />
            <Button Content="退出" Style="{StaticResource MyButtonStyle2}" />
            <Button Content="保存" Style="{StaticResource MyButtonStyle3}" />
        </StackPanel>
    </Grid>
</Window>
```

