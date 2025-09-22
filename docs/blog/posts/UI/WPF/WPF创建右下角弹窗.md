---
title: WPF创建右下角弹窗
date: 2024-09-01
categories:
  - windows程序
tags:
  - WPF
  - 弹窗
  - 通知
  - UI设计
description: WPF中创建右下角通知弹窗的完整实现，包含动画效果和自动关闭功能
author: JerryMa
---

# WPF创建右下角弹窗

`WpfRightNotify.xaml`

 `SizeToContent="Height"`//可以根据内容调整高度

```csharp
<Window
    x:Class="ZwWhForXhhk.Net.View.WpfRightNotify"
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
    xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
    xmlns:local="clr-namespace:ZwWhForXhhk.Net.View"
    xmlns:materialDesign="http://materialdesigninxaml.net/winfx/xaml/themes"
    xmlns:materialDesignColors="clr-namespace:MaterialDesignColors;assembly=MaterialDesignColors"
    xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
    Width="300"
    Height="150"
    AllowsTransparency="True"
    Background="Transparent"
    Opacity="0"
    ShowInTaskbar="False"
    Topmost="True"
    SizeToContent="Height"
    WindowStyle="None">
    <Window.Resources>
        <ResourceDictionary>
            <ResourceDictionary.MergedDictionaries>
                <materialDesign:BundledTheme
                    BaseTheme="Light"
                    PrimaryColor="DeepPurple"
                    SecondaryColor="Blue" />
                <ResourceDictionary Source="pack://application:,,,/MaterialDesignThemes.Wpf;component/Themes/MaterialDesign2.Defaults.xaml" />
            </ResourceDictionary.MergedDictionaries>
        </ResourceDictionary>
    </Window.Resources>
    <Border
        x:Name="RootBorder"
        Padding="10"
        Background="#FF333333"
        CornerRadius="10">
        <Grid>
            <Grid.RowDefinitions>
                <RowDefinition Height="Auto" />
                <RowDefinition Height="*" />
            </Grid.RowDefinitions>
            <Grid.ColumnDefinitions>
                <ColumnDefinition Width="Auto" />
                <ColumnDefinition Width="*" />
            </Grid.ColumnDefinitions>

            <!--<Button
                    x:Name="IconButton"
                    Background="Transparent"
                    Style="{StaticResource MaterialDesignFlatButton}">
                    <materialDesign:PackIcon
                        Width="24"
                        Height="24"
                        Kind="{Binding Icon}" />
                </Button>-->
            <StackPanel Orientation="Horizontal">
                <materialDesign:PackIcon
                    x:Name="IconImage"
                    VerticalAlignment="Center"
                    Kind="{Binding Icon}" />
                <TextBlock
                    x:Name="IconText"
                    Margin="10,0,0,0"
                    VerticalAlignment="Center"
                    FontSize="16"
                    FontWeight="Bold" />
            </StackPanel>
            <Button
                x:Name="CloseButton"
                Grid.Column="1"
                HorizontalAlignment="Right"
                Background="Transparent"
                Click="CloseButton_Click"
                Style="{StaticResource MaterialDesignFlatButton}"
                ToolTip="Close">
                <materialDesign:PackIcon Kind="Close" />
            </Button>
            <RichTextBox
                x:Name="MessageText"
                Grid.Row="1"
                Grid.ColumnSpan="2"
                AcceptsReturn="True"
                FontSize="12"
                Foreground="White"
                IsReadOnly="True"
                VerticalScrollBarVisibility="Auto" />
        </Grid>
    </Border>
</Window>

```

`WpfRightNotify.xaml.cs`

```csharp
namespace ZwWhForXhhk.Net.View
{
    /// <summary>
    /// WpfRightNotify.xaml 的交互逻辑
    /// </summary>
    public partial class WpfRightNotify : Window
    {
        private DispatcherTimer timer;

        public WpfRightNotify(string message, ToastType type, int durationSeconds)
        {
            InitializeComponent();
            MessageText.AppendText(message);
            SetStyle(type);

            Loaded += (s, e) =>
            {
                var area = SystemParameters.WorkArea;
                Left = area.Right - Width/* - 10*/;
                Top = area.Bottom - Height/* - 10*/ - ToastManager.GetYOffset(this);
                ShowAnimation(durationSeconds);
            };
        }
        private void SetStyle(ToastType type)
        {
            switch (type)
            {
                case ToastType.Success:
                    RootBorder.Background = new System.Windows.Media.SolidColorBrush(System.Windows.Media.Colors.SeaGreen);
                    IconText.Text = "成功";
                    IconImage.Kind = (MaterialDesignThemes.Wpf.PackIconKind)Enum.Parse(typeof(MaterialDesignThemes.Wpf.PackIconKind), "CheckBold");
                    IconImage.Background = new System.Windows.Media.SolidColorBrush(System.Windows.Media.Colors.SeaGreen);
                    IconImage.Foreground = new System.Windows.Media.SolidColorBrush(System.Windows.Media.Colors.DarkGreen);
                    break;
                case ToastType.Warning:
                    RootBorder.Background = new System.Windows.Media.SolidColorBrush(System.Windows.Media.Colors.Orange);
                    IconText.Text = "警告";
                    IconImage.Kind = (MaterialDesignThemes.Wpf.PackIconKind)Enum.Parse(typeof(MaterialDesignThemes.Wpf.PackIconKind), "Alert");
                    IconImage.Background = new System.Windows.Media.SolidColorBrush(System.Windows.Media.Colors.Orange);
                    IconImage.Foreground = new System.Windows.Media.SolidColorBrush(System.Windows.Media.Colors.DarkOrange);
                    break;
                case ToastType.Error:
                    RootBorder.Background = new System.Windows.Media.SolidColorBrush(System.Windows.Media.Colors.IndianRed);
                    IconText.Text = "错误";
                    IconImage.Kind = (MaterialDesignThemes.Wpf.PackIconKind)Enum.Parse(typeof(MaterialDesignThemes.Wpf.PackIconKind), "Close");
                    IconImage.Background = new System.Windows.Media.SolidColorBrush(System.Windows.Media.Colors.IndianRed);
                    IconImage.Foreground = new System.Windows.Media.SolidColorBrush(System.Windows.Media.Colors.DarkRed);
                    break;
                default:
                    RootBorder.Background = new System.Windows.Media.SolidColorBrush(System.Windows.Media.Colors.DimGray);
                    IconText.Text = "信息";
                    IconImage.Kind = (MaterialDesignThemes.Wpf.PackIconKind)Enum.Parse(typeof(MaterialDesignThemes.Wpf.PackIconKind), "InformationVariantBoxOutline");
                    IconImage.Background = new System.Windows.Media.SolidColorBrush(System.Windows.Media.Colors.DimGray);
                    IconImage.Foreground = new System.Windows.Media.SolidColorBrush(System.Windows.Media.Colors.DarkGray);
                    break;
            }
        }

        private void ShowAnimation(int durationSeconds)
        {
            //var fadeIn = new DoubleAnimation(0, 1, TimeSpan.FromMilliseconds(300));
            double right = System.Windows.SystemParameters.WorkArea.Right;//工作区最右边的值
            DoubleAnimation animation = new DoubleAnimation();
            animation.Duration = new Duration(TimeSpan.FromMilliseconds(3000));//NotifyTimeSpan是自己定义的一个int型变量，用来设置动画的持续时间
            animation.From = right;
            animation.To = right - 300;//设定通知从右往左弹出
            BeginAnimation(OpacityProperty, animation);

            timer = new DispatcherTimer { Interval = TimeSpan.FromSeconds(durationSeconds) };
            timer.Tick += (s, e) =>
            {
                timer.Stop();
                CloseAnimation();
            };
            timer.Start();
        }

        private void CloseAnimation()
        {
            var fadeOut = new DoubleAnimation(1, 0, TimeSpan.FromMilliseconds(300));
            fadeOut.Completed += (s, e) =>
            {
                Close();
                ToastManager.RemoveToast(this);
            };
            BeginAnimation(OpacityProperty, fadeOut);
        }

        private void CloseButton_Click(object sender, RoutedEventArgs e)
        {
            this.Close();
            ToastManager.RemoveToast(this);
            //System.Windows.MessageBox.Show("关闭");
        }
    }

    public enum ToastType
    {
        Info,
        Success,
        Warning,
        Error
    }

    public static class ToastManager
    {
        private static List<WpfRightNotify> toasts = new List<WpfRightNotify>();

        public static void ShowToast(string message, ToastType type = ToastType.Info, int durationSeconds = 3)
        {
            var toast = new WpfRightNotify(message, type, durationSeconds);
            toasts.Add(toast);
            toast.Show();
        }

        public static double GetYOffset(WpfRightNotify current)
        {
            double offset = 0;
            foreach (var toast in toasts)
            {
                if (toast == current) break;
                offset += toast.Height + 10;
            }
            return offset;
        }

        public static void RemoveToast(WpfRightNotify toast)
        {
            toasts.Remove(toast);
        }
    }
}
```

`调用方式`

```csharp
ToastManager.ShowToast("操作成功！", ToastType.Success, 15);
ToastManager.ShowToast("操作失败！", ToastType.Error, 15);
ToastManager.ShowToast("警告！", ToastType.Warning, 15);
ToastManager.ShowToast("#define ACED_SERVICES  ACRX_T(\"AcEdServices\")\r\n#define ACED_EDITOR_OBJ ACRX_T(\"AcEditor\")\r\n\r\n// The various modes for context menus.\r\nenum AcadContextMenuMode {\r\n    kDefault = 0,           // No selection set, no command active.\r\n    kEdit,                  // Select set, no command active.\r\n    kCommand,               // Command active.\r\n    kHotGrip,               // Hot grip exists.\r\n    kOsnap,                 // Shift key down.   \r\n#ifdef _ADESK_MAC_\r\n\tkCMPaperSpace           // In paper space. \r\n#endif\r\n};！", ToastType.Info, 15);
```

![image-20250417194136084](http://image.jerryma.xyz//images/20250417-image-20250417194136084.png)