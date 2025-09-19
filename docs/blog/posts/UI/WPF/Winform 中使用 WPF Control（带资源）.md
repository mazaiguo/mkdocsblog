---
title: Winform 中使用 WPF Control（带资源）
date: 2024-05-08
categories:
  - Winform
  - WPF
  - Csharp开发
tags:
  - Winform
  - WPF
  - 混合开发
  - Csharp
description: 在Winform应用程序中嵌入和使用WPF控件的方法，包含资源处理技巧
author: JerryMa
---
# Winform 中使用 WPF Control（带资源）

## .Net 中 winform 中使用 [WPF](https://so.csdn.net/so/search?q=WPF&spm=1001.2101.3001.7020) 控件

若控件本身带有引用的资源，则情况变得复杂

### 由于WinForm 默认不含 Application 全局变量，需手动引入。

首先在exe 项目中增加 PresentationForm 的引用

```csharp
namespace Test
{
    public partial class LeftDropMenu : UserControl
    {
        public LeftDropMenu()
        {
            if (null == System.Windows.Application.Current)
            {
                new System.Windows.Application();
            }
            InitializeComponent();
        }
    }
}
```

### 在自定义的 UserControl 子类的构造函数 `InitializeComponent` 执行之前动态增加所需要的资源

将资源定义在应用程序中，使用LoadComponent加载资源，代码如下所示：

```csharp
 public UserControl1()
 {
     System.Uri resourceLocater = new System.Uri("/Test;component/ComUseicons.xaml", System.UriKind.Relative);
     ResourceDictionary rd = (ResourceDictionary)Application.LoadComponent(resourceLocater);
     Application.Current.Resources.MergedDictionaries.Add(rd);
     //System.Uri resourceLocater1 = new System.Uri("", System.UriKind.Relative);
     //ResourceDictionary rd1 = (ResourceDictionary)Application.LoadComponent(resourceLocater1);

     InitializeComponent();
     try
     {
         string jsonFile = GetDllDirectory() + "\\Menu.json";
         // 确保文件存在
         if (!File.Exists(jsonFile))
             throw new FileNotFoundException("The JSON file was not found." + jsonFile);

         // 读取文件内容并反序列化为指定的类型 T
         var reader = new StreamReader(jsonFile);
         var json = reader.ReadToEnd();
         var person = JsonConvert.DeserializeObject<Root>(json);
         Items = person.ItemMenu;

         //遍历items，将icon添加数据
         // 遍历并修改Icon
         foreach (var itemMenu in Items)
         {
             //itemMenu.Icon = GetDllDirectory() + "\\config\\Images\\PNG\\" + itemMenu.Icon;
             foreach (var subItem in itemMenu.SubItems)
             {
                 subItem.Icon = GetDllDirectory() + "\\config\\Images\\PNG\\" + subItem.Icon;
             }
         }

         LeftMenu.ItemsSource = Items;
     }
     catch (Exception)
     {
         throw;
     }
 }
```



## 增加一个转换器，将svg key资源转换成ImageSource

```csharp
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Data;
using System.Windows.Media;

namespace Test.MyDropMenu
{
    class DrawingGroupToImageSourceConverter : IValueConverter
    {
        public static string GetDllDirectory()
        {
            string codeBase = Assembly.GetExecutingAssembly().CodeBase;
            UriBuilder uri = new UriBuilder(codeBase);
            string path = Uri.UnescapeDataString(uri.Path);
            return System.IO.Path.GetDirectoryName(path);
        }
        public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
        {
            var drawingGroup = Application.Current.FindResource(value);
            if (drawingGroup == null)
                return null;
            return (ImageSource)drawingGroup;
        }
        public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
        {
            throw new NotImplementedException();
        }
    }
}
```

在Resource中定义

```csharp
<UserControl.Resources>
<convert:DrawingGroupToImageSourceConverter x:Key="DrawingGroupToImageSourceConverter" />
</UserControl.Resources>
```



在Image中调用方式如下所示：

```csharp
 <Image
     Grid.Column="0"
     Height="{TemplateBinding FontSize}"
     MinHeight="16"
     MaxHeight="32"
     Margin="2,2"
     HorizontalAlignment="Left"
     Source="{Binding Path=Icon, Converter={StaticResource DrawingGroupToImageSourceConverter}}" />
```



在xmal中不需要在引入资源了。

[参考](https://blog.csdn.net/weixin_30896511/article/details/101411336)