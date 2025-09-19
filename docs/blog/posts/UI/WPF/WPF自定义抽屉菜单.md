---
title: WPF自定义抽屉菜单
date: 2025-08-12
categories:
  - WPF
  - CSharp
  - Windows程序
tags:
  - WPF
  - MENU
  - DropMenuControls
  - UI
description: 自定义DropMenu方便在Pallet中使用
authors:
  - JerryMa
---





# WPF自定义抽屉菜单

## 处理wpf自定义控件

![image-20250901162509475](http://image.jerryma.xyz//images/20250901-image-20250901162509475.png)



`DropMenuControls\Converters\BooleanToVisibilityConverter`

```csharp
using System;
using System.Globalization;
using System.Windows;
using System.Windows.Data;

namespace DropMenuControls.Converters
{
    public class BooleanToVisibilityConverter : IValueConverter
    {
        public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
        {
            if (value is bool boolValue)
            {
                return boolValue ? Visibility.Visible : Visibility.Collapsed;
            }
            return Visibility.Collapsed;
        }

        public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
        {
            if (value is Visibility visibility)
            {
                return visibility == Visibility.Visible;
            }
            return false;
        }
    }
}

```

`DropMenuControls\Models\MenuItem`

```csharp
using System.Collections.Generic;

namespace DropMenuControls.Models
{
    public class MenuData
    {
        public List<MenuItem> ItemMenu { get; set; }
    }

    public class MenuItem
    {
        public string Name { get; set; }
        public string Icon { get; set; }
        public int FontSize { get; set; }
        public string Command { get; set; }
        public List<MenuItem> SubItems { get; set; }

        public bool HasSubItems => SubItems != null && SubItems.Count > 0;
    }
}

```

`Generic.xaml`

```csharp
<ResourceDictionary
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
    xmlns:local="clr-namespace:DropMenuControls">

    <!--  DropMenu 控件的默认样式  -->
    <Style TargetType="{x:Type local:DropMenu}">
        <Setter Property="Background" Value="White" />
        <Setter Property="BorderBrush" Value="#DDDDDD" />
        <Setter Property="BorderThickness" Value="1" />
        <Setter Property="FontFamily" Value="Segoe UI" />
        <Setter Property="FontSize" Value="14" />
        <Setter Property="Foreground" Value="#333333" />
        <Setter Property="SnapsToDevicePixels" Value="True" />
        <Setter Property="UseLayoutRounding" Value="True" />
    </Style>

</ResourceDictionary>

```

`DropMenuControls\ViewModels\DropMenuViewModel`

```csharp
using System;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.IO;
using System.Windows;
using Newtonsoft.Json;
using DropMenuControls.Models;
using System.Reflection;

namespace DropMenuControls.ViewModels
{
    public class DropMenuViewModel : INotifyPropertyChanged
    {
        public ObservableCollection<MenuItemViewModel> MenuItems { get; } = new ObservableCollection<MenuItemViewModel>();

        private MenuItemViewModel _selectedItem;
        public MenuItemViewModel SelectedItem
        {
            get => _selectedItem;
            set
            {
                if (_selectedItem != value)
                {
                    _selectedItem = value;
                    OnPropertyChanged(nameof(SelectedItem));
                    // 移除这里的事件触发，避免重复调用
                    // 事件触发应该只在OnMenuItemClicked中处理
                }
            }
        }

        private string _menuConfigPath = "Menu.json";
        /// <summary>
        /// 菜单配置文件路径
        /// </summary>
        public string MenuConfigPath
        {
            get => _menuConfigPath;
            set
            {
                if (_menuConfigPath != value)
                {
                    _menuConfigPath = value;
                    OnPropertyChanged(nameof(MenuConfigPath));
                }
            }
        }

        private string _iconDirectory = "Icons";
        /// <summary>
        /// 图标目录路径
        /// </summary>
        public string IconDirectory
        {
            get => _iconDirectory;
            set
            {
                if (_iconDirectory != value)
                {
                    _iconDirectory = value;
                    OnPropertyChanged(nameof(IconDirectory));
                }
            }
        }

        public event PropertyChangedEventHandler PropertyChanged;

        public DropMenuViewModel()
        {
            LoadMenuFromJson();
        }

        public DropMenuViewModel(string menuConfigPath, string iconDirectory)
        {
            MenuConfigPath = menuConfigPath;
            IconDirectory = iconDirectory;
            LoadMenuFromJson();
        }

        public void LoadMenuFromJson()
        {
            try
            {
                // 使用配置的路径，支持相对路径和绝对路径
                string jsonPath;
                if (Path.IsPathRooted(MenuConfigPath))
                {
                    // 绝对路径
                    jsonPath = MenuConfigPath;
                }
                else
                {
                    // 相对路径，相对于执行程序目录
                    jsonPath = Path.Combine(Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location), MenuConfigPath);
                }
                if (!File.Exists(jsonPath))
                {
                    System.Diagnostics.Debug.WriteLine($"菜单配置文件未找到: {jsonPath}");
                    return;
                }

                string jsonContent = File.ReadAllText(jsonPath);
                
                var settings = new JsonSerializerSettings
                {
                    MissingMemberHandling = MissingMemberHandling.Ignore,
                    NullValueHandling = NullValueHandling.Ignore
                };
                
                MenuData menuData = JsonConvert.DeserializeObject<MenuData>(jsonContent, settings);

                if (menuData?.ItemMenu != null)
                {
                    BuildMenuItems(menuData.ItemMenu);
                }
             
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"加载菜单配置失败: {ex.Message}");
            }
        }

        private void BuildMenuItems(System.Collections.Generic.List<MenuItem> menuItems)
        {
            MenuItems.Clear();
            
            foreach (var item in menuItems)
            {
                var viewModel = new MenuItemViewModel(item, IconDirectory);
                BindMenuItemEvents(viewModel); // 递归绑定所有菜单项的事件
                MenuItems.Add(viewModel);
            }
        }

        // 递归绑定菜单项和所有子项的事件
        private void BindMenuItemEvents(MenuItemViewModel menuItem)
        {
            menuItem.MenuItemClicked += OnMenuItemClicked;
            
            // 为所有子项也绑定事件
            foreach (var subItem in menuItem.SubItems)
            {
                BindMenuItemEvents(subItem);
            }
        }

        private void OnMenuItemClicked(MenuItemViewModel clickedItem)
        {
            System.Diagnostics.Debug.WriteLine($"[DropMenuViewModel] OnMenuItemClicked被调用: {clickedItem.Name}");
            
            // 只有当菜单项有命令时才处理选中状态和触发事件
            if (!string.IsNullOrWhiteSpace(clickedItem.Command))
            {
                System.Diagnostics.Debug.WriteLine($"[DropMenuViewModel] 处理有命令的菜单项: {clickedItem.Command}");
                
                // 清除所有选中状态
                ClearAllSelections();
                
                // 设置当前选中项
                SelectedItem = clickedItem;
                clickedItem.IsSelected = true;

                // 记录命令并触发外部事件（只触发一次）
                ShowCommandMessage(clickedItem.Command);
                RaiseMenuItemClickedEvent(clickedItem);
            }
            else
            {
                System.Diagnostics.Debug.WriteLine($"[DropMenuViewModel] 跳过无命令的菜单项: {clickedItem.Name}");
            }
        }

        private void ClearAllSelections()
        {
            foreach (var item in MenuItems)
            {
                ClearSelectionRecursive(item);
            }
        }

        // 递归清除所有层级的选中状态
        private void ClearSelectionRecursive(MenuItemViewModel menuItem)
        {
            menuItem.IsSelected = false;
            
            foreach (var subItem in menuItem.SubItems)
            {
                ClearSelectionRecursive(subItem);
            }
        }

        private void ShowCommandMessage(string command)
        {
            // 不在ViewModel中显示MessageBox，将这个责任交给UI层处理
            // 这样避免了重复弹出对话框的问题
            System.Diagnostics.Debug.WriteLine($"菜单命令被触发: {command}");
        }

        // 公共方法，供外部调用以触发菜单项点击事件
        public event Action<MenuItemViewModel> MenuItemClickedEvent;

        private void RaiseMenuItemClickedEvent(MenuItemViewModel item)
        {
            System.Diagnostics.Debug.WriteLine($"[DropMenuViewModel] 向外部触发MenuItemClickedEvent: {item.Name}");
            MenuItemClickedEvent?.Invoke(item);
        }

        protected virtual void OnPropertyChanged(string propertyName)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
    }
}

```

`DropMenuControls\ViewModels\MenuItemViewModel`

```csharp
using System;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.IO;
using System.Reflection;
using System.Windows;
using System.Windows.Input;
using System.Windows.Media.Imaging;
using DropMenuControls.Models;

namespace DropMenuControls.ViewModels
{
    public class MenuItemViewModel : INotifyPropertyChanged
    {
        /// <summary>
        /// 图标目录路径
        /// </summary>
        public string IconDirectory { get; set; } = "Icons";

        private string _name;
        private string _icon;
        private int _fontSize;
        private string _command;
        private bool _isExpanded;
        private bool _isSelected;
        private BitmapImage _iconSource;

        public string Name
        {
            get => _name;
            set
            {
                if (_name != value)
                {
                    _name = value;
                    OnPropertyChanged(nameof(Name));
                }
            }
        }

        public string Icon
        {
            get => _icon;
            set
            {
                if (_icon != value)
                {
                    _icon = value;
                    OnPropertyChanged(nameof(Icon));
                    LoadIcon();
                }
            }
        }

        public int FontSize
        {
            get => _fontSize;
            set
            {
                if (_fontSize != value)
                {
                    _fontSize = value;
                    OnPropertyChanged(nameof(FontSize));
                }
            }
        }

        public string Command
        {
            get => _command;
            set
            {
                if (_command != value)
                {
                    _command = value;
                    OnPropertyChanged(nameof(Command));
                }
            }
        }

        public bool IsExpanded
        {
            get => _isExpanded;
            set
            {
                if (_isExpanded != value)
                {
                    _isExpanded = value;
                    OnPropertyChanged(nameof(IsExpanded));
                }
            }
        }

        public bool IsSelected
        {
            get => _isSelected;
            set
            {
                if (_isSelected != value)
                {
                    _isSelected = value;
                    OnPropertyChanged(nameof(IsSelected));
                }
            }
        }

        public BitmapImage IconSource
        {
            get => _iconSource;
            set
            {
                if (_iconSource != value)
                {
                    _iconSource = value;
                    OnPropertyChanged(nameof(IconSource));
                }
            }
        }

        public ObservableCollection<MenuItemViewModel> SubItems { get; } = new ObservableCollection<MenuItemViewModel>();

        public bool HasSubItems => SubItems.Count > 0;

        private void LoadIcon()
        {
            try
            {
                if (!string.IsNullOrWhiteSpace(Icon))
                {
                    string iconPath;
                    if (Path.IsPathRooted(IconDirectory))
                    {
                        // IconDirectory是绝对路径
                        iconPath = Path.Combine(IconDirectory, Icon);
                    }
                    else
                    {
                        // IconDirectory是相对路径，相对于执行程序目录
                        iconPath = Path.Combine(Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location), IconDirectory, Icon);
                    }
                    if (File.Exists(iconPath))
                    {
                        var bitmap = new BitmapImage();
                        bitmap.BeginInit();
                        bitmap.UriSource = new Uri(iconPath, UriKind.Absolute);
                        bitmap.DecodePixelWidth = 24;
                        bitmap.DecodePixelHeight = 24;
                        bitmap.EndInit();
                        IconSource = bitmap;
                    }
                }
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine($"加载图标失败: {ex.Message}");
            }
        }

        public ICommand ExecuteMenuItemCommand { get; }
        public event Action<MenuItemViewModel> MenuItemClicked;
        public event PropertyChangedEventHandler PropertyChanged;

        public MenuItemViewModel()
        {
            ExecuteMenuItemCommand = new RelayCommand(ExecuteMenuItem);
        }

        public MenuItemViewModel(MenuItem menuItem, string iconDirectory = "Icons")
        {
            ExecuteMenuItemCommand = new RelayCommand(ExecuteMenuItem);
            Name = menuItem.Name;
            Icon = menuItem.Icon;
            FontSize = menuItem.FontSize;
            Command = menuItem.Command;
            IconDirectory = iconDirectory;
            LoadIcon();

            if (menuItem.SubItems != null)
            {
                foreach (var subItem in menuItem.SubItems)
                {
                    var subViewModel = new MenuItemViewModel(subItem, iconDirectory);
                    SubItems.Add(subViewModel);
                }
            }
            
            OnPropertyChanged(nameof(HasSubItems));
        }

        private DateTime _lastExecutionTime = DateTime.MinValue;
        private static readonly TimeSpan MinimumInterval = TimeSpan.FromMilliseconds(500); // 500ms防重复间隔
        
        private void ExecuteMenuItem()
        {
            var currentTime = DateTime.Now;
            
            // 防重复触发机制 - 使用时间间隔控制
            if (currentTime - _lastExecutionTime < MinimumInterval)
            {
                System.Diagnostics.Debug.WriteLine($"[MenuItemViewModel] 防止重复执行 (间隔太短): {Name}, 间隔: {(currentTime - _lastExecutionTime).TotalMilliseconds}ms");
                return;
            }
            
            _lastExecutionTime = currentTime;
            System.Diagnostics.Debug.WriteLine($"[MenuItemViewModel] 执行菜单项: {Name}");
            
            // 如果有子项，切换展开状态
            if (HasSubItems)
            {
                IsExpanded = !IsExpanded;
            }
            
            // 总是触发事件，让DropMenuViewModel来处理逻辑（包括选中状态和命令执行）
            MenuItemClicked?.Invoke(this);
        }

        // 清除选中状态（用于实现单选逻辑）
        public void ClearSelection()
        {
            IsSelected = false;
            foreach (var subItem in SubItems)
            {
                subItem.ClearSelection();
            }
        }

        protected virtual void OnPropertyChanged(string propertyName)
        {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
        }
    }

    // Csharp 7.3 兼容的RelayCommand实现
    public class RelayCommand : ICommand
    {
        private readonly Action _execute;
        private readonly Func<bool> _canExecute;

        public RelayCommand(Action execute, Func<bool> canExecute = null)
        {
            _execute = execute ?? throw new ArgumentNullException(nameof(execute));
            _canExecute = canExecute;
        }

        public event EventHandler CanExecuteChanged
        {
            add { CommandManager.RequerySuggested += value; }
            remove { CommandManager.RequerySuggested -= value; }
        }

        public bool CanExecute(object parameter)
        {
            return _canExecute?.Invoke() ?? true;
        }

        public void Execute(object parameter)
        {
            _execute();
        }
    }
}

```

`DropMenu.xaml`

```csharp
<UserControl
    x:Class="DropMenuControls.DropMenu"
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
    xmlns:converters="clr-namespace:DropMenuControls.Converters"
    xmlns:vm="clr-namespace:DropMenuControls.ViewModels">

    <UserControl.Resources>
        <converters:BooleanToVisibilityConverter x:Key="BooleanToVisibilityConverter" />

        <!--  主菜单按钮样式 - 现代化动态效果  -->
        <Style x:Key="MenuButtonStyle" TargetType="Button">
            <Setter Property="Background" Value="#F8F9FA" />
            <Setter Property="BorderBrush" Value="#E0E0E0" />
            <Setter Property="BorderThickness" Value="1" />
            <Setter Property="Padding" Value="15,12" />
            <Setter Property="Margin" Value="5,2" />
            <Setter Property="HorizontalContentAlignment" Value="Left" />
            <Setter Property="Cursor" Value="Hand" />
            <Setter Property="FontSize" Value="14" />
            <Setter Property="FontWeight" Value="Medium" />
            <Setter Property="RenderTransformOrigin" Value="0.5,0.5" />
            <Setter Property="Effect">
                <Setter.Value>
                    <DropShadowEffect
                        BlurRadius="0"
                        Opacity="0"
                        ShadowDepth="0"
                        Color="Black" />
                </Setter.Value>
            </Setter>
            <Setter Property="RenderTransform">
                <Setter.Value>
                    <TransformGroup>
                        <ScaleTransform ScaleX="1" ScaleY="1" />
                        <TranslateTransform X="0" Y="0" />
                    </TransformGroup>
                </Setter.Value>
            </Setter>
            <Style.Triggers>
                <DataTrigger Binding="{Binding IsSelected}" Value="True">
                    <Setter Property="Background" Value="#2196F3" />
                    <Setter Property="Foreground" Value="White" />
                    <Setter Property="BorderBrush" Value="#1976D2" />
                    <Setter Property="FontWeight" Value="Bold" />
                    <DataTrigger.EnterActions>
                        <BeginStoryboard>
                            <Storyboard>
                                <DoubleAnimation
                                    Storyboard.TargetProperty="RenderTransform.Children[0].ScaleX"
                                    To="1.03"
                                    Duration="0:0:0.25" />
                                <DoubleAnimation
                                    Storyboard.TargetProperty="RenderTransform.Children[0].ScaleY"
                                    To="1.03"
                                    Duration="0:0:0.25" />
                                <DoubleAnimation
                                    Storyboard.TargetProperty="Effect.BlurRadius"
                                    To="8"
                                    Duration="0:0:0.25" />
                                <DoubleAnimation
                                    Storyboard.TargetProperty="Effect.Opacity"
                                    To="0.4"
                                    Duration="0:0:0.25" />
                                <DoubleAnimation
                                    Storyboard.TargetProperty="Effect.ShadowDepth"
                                    To="2"
                                    Duration="0:0:0.25" />
                            </Storyboard>
                        </BeginStoryboard>
                    </DataTrigger.EnterActions>
                    <DataTrigger.ExitActions>
                        <BeginStoryboard>
                            <Storyboard>
                                <DoubleAnimation
                                    Storyboard.TargetProperty="RenderTransform.Children[0].ScaleX"
                                    To="1"
                                    Duration="0:0:0.25" />
                                <DoubleAnimation
                                    Storyboard.TargetProperty="RenderTransform.Children[0].ScaleY"
                                    To="1"
                                    Duration="0:0:0.25" />
                                <DoubleAnimation
                                    Storyboard.TargetProperty="Effect.BlurRadius"
                                    To="0"
                                    Duration="0:0:0.25" />
                                <DoubleAnimation
                                    Storyboard.TargetProperty="Effect.Opacity"
                                    To="0"
                                    Duration="0:0:0.25" />
                                <DoubleAnimation
                                    Storyboard.TargetProperty="Effect.ShadowDepth"
                                    To="0"
                                    Duration="0:0:0.25" />
                            </Storyboard>
                        </BeginStoryboard>
                    </DataTrigger.ExitActions>
                </DataTrigger>
                <Trigger Property="IsMouseOver" Value="True">
                    <Setter Property="Background" Value="#E8F4FD" />
                    <Setter Property="BorderBrush" Value="#2196F3" />
                    <Trigger.EnterActions>
                        <BeginStoryboard>
                            <Storyboard>
                                <DoubleAnimation
                                    Storyboard.TargetProperty="RenderTransform.Children[1].Y"
                                    To="-1"
                                    Duration="0:0:0.2" />
                                <DoubleAnimation
                                    Storyboard.TargetProperty="RenderTransform.Children[0].ScaleX"
                                    To="1.01"
                                    Duration="0:0:0.2" />
                                <DoubleAnimation
                                    Storyboard.TargetProperty="RenderTransform.Children[0].ScaleY"
                                    To="1.01"
                                    Duration="0:0:0.2" />
                            </Storyboard>
                        </BeginStoryboard>
                    </Trigger.EnterActions>
                    <Trigger.ExitActions>
                        <BeginStoryboard>
                            <Storyboard>
                                <DoubleAnimation
                                    Storyboard.TargetProperty="RenderTransform.Children[1].Y"
                                    To="0"
                                    Duration="0:0:0.2" />
                                <DoubleAnimation
                                    Storyboard.TargetProperty="RenderTransform.Children[0].ScaleX"
                                    To="1"
                                    Duration="0:0:0.2" />
                                <DoubleAnimation
                                    Storyboard.TargetProperty="RenderTransform.Children[0].ScaleY"
                                    To="1"
                                    Duration="0:0:0.2" />
                            </Storyboard>
                        </BeginStoryboard>
                    </Trigger.ExitActions>
                </Trigger>
                <Trigger Property="IsPressed" Value="True">
                    <Trigger.EnterActions>
                        <BeginStoryboard>
                            <Storyboard>
                                <DoubleAnimation
                                    Storyboard.TargetProperty="RenderTransform.Children[0].ScaleX"
                                    To="0.97"
                                    Duration="0:0:0.1" />
                                <DoubleAnimation
                                    Storyboard.TargetProperty="RenderTransform.Children[0].ScaleY"
                                    To="0.97"
                                    Duration="0:0:0.1" />
                                <DoubleAnimation
                                    Storyboard.TargetProperty="RenderTransform.Children[1].Y"
                                    To="1"
                                    Duration="0:0:0.1" />
                            </Storyboard>
                        </BeginStoryboard>
                    </Trigger.EnterActions>
                    <Trigger.ExitActions>
                        <BeginStoryboard>
                            <Storyboard>
                                <DoubleAnimation
                                    Storyboard.TargetProperty="RenderTransform.Children[0].ScaleX"
                                    To="1"
                                    Duration="0:0:0.15" />
                                <DoubleAnimation
                                    Storyboard.TargetProperty="RenderTransform.Children[0].ScaleY"
                                    To="1"
                                    Duration="0:0:0.15" />
                                <DoubleAnimation
                                    Storyboard.TargetProperty="RenderTransform.Children[1].Y"
                                    To="0"
                                    Duration="0:0:0.15" />
                            </Storyboard>
                        </BeginStoryboard>
                    </Trigger.ExitActions>
                </Trigger>
            </Style.Triggers>
        </Style>

        <!--  子菜单项样式  -->
        <Style x:Key="SubMenuItemStyle" TargetType="Border">
            <Setter Property="Background" Value="Transparent" />
            <Setter Property="BorderBrush" Value="#E0E0E0" />
            <Setter Property="BorderThickness" Value="1" />
            <Setter Property="Padding" Value="25,8" />
            <Setter Property="Margin" Value="8,1" />
            <Setter Property="Cursor" Value="Hand" />
            <Setter Property="CornerRadius" Value="4" />
            <Setter Property="RenderTransformOrigin" Value="0.5,0.5" />
            <Setter Property="RenderTransform">
                <Setter.Value>
                    <TransformGroup>
                        <TranslateTransform X="0" />
                        <ScaleTransform ScaleX="1" ScaleY="1" />
                    </TransformGroup>
                </Setter.Value>
            </Setter>
            <Style.Triggers>
                <DataTrigger Binding="{Binding IsSelected}" Value="True">
                    <Setter Property="Background" Value="#43A047" />
                    <Setter Property="BorderBrush" Value="#4CAF50" />
                    <Setter Property="BorderThickness" Value="2" />
                </DataTrigger>
                <Trigger Property="IsMouseOver" Value="True">
                    <Setter Property="Background" Value="#E8F5E8" />
                    <Setter Property="BorderBrush" Value="#4CAF50" />
                    <Trigger.EnterActions>
                        <BeginStoryboard>
                            <Storyboard>
                                <DoubleAnimation
                                    Storyboard.TargetProperty="RenderTransform.Children[0].X"
                                    To="5"
                                    Duration="0:0:0.15" />
                            </Storyboard>
                        </BeginStoryboard>
                    </Trigger.EnterActions>
                    <Trigger.ExitActions>
                        <BeginStoryboard>
                            <Storyboard>
                                <DoubleAnimation
                                    Storyboard.TargetProperty="RenderTransform.Children[0].X"
                                    To="0"
                                    Duration="0:0:0.15" />
                            </Storyboard>
                        </BeginStoryboard>
                    </Trigger.ExitActions>
                </Trigger>
            </Style.Triggers>
        </Style>

        <!--  子菜单按钮样式 - 最简版本，完全稳定  -->
        <Style x:Key="SubMenuButtonStyle" TargetType="Button">
            <Setter Property="Background" Value="Transparent" />
            <Setter Property="BorderBrush" Value="#E0E0E0" />
            <Setter Property="BorderThickness" Value="1" />
            <Setter Property="Padding" Value="25,8" />
            <Setter Property="Margin" Value="8,1" />
            <Setter Property="Cursor" Value="Hand" />
            <Setter Property="HorizontalContentAlignment" Value="Left" />
            <Setter Property="Template">
                <Setter.Value>
                    <ControlTemplate TargetType="Button">
                        <Border
                            Padding="{TemplateBinding Padding}"
                            Background="{TemplateBinding Background}"
                            BorderBrush="{TemplateBinding BorderBrush}"
                            BorderThickness="{TemplateBinding BorderThickness}"
                            CornerRadius="4">
                            <ContentPresenter HorizontalAlignment="{TemplateBinding HorizontalContentAlignment}" />
                        </Border>
                    </ControlTemplate>
                </Setter.Value>
            </Setter>
            <Style.Triggers>
                <DataTrigger Binding="{Binding IsSelected}" Value="True">
                    <Setter Property="Background" Value="#43A047" />
                    <Setter Property="BorderBrush" Value="#4CAF50" />
                    <Setter Property="Foreground" Value="White" />
                    <Setter Property="BorderThickness" Value="2" />
                </DataTrigger>
                <Trigger Property="IsMouseOver" Value="True">
                    <Setter Property="Background" Value="#E8F5E8" />
                    <Setter Property="BorderBrush" Value="#4CAF50" />
                </Trigger>
            </Style.Triggers>
        </Style>

        <!--  菜单项数据模板  -->
        <DataTemplate x:Key="MenuItemTemplate" DataType="{x:Type vm:MenuItemViewModel}">
            <StackPanel>
                <!--  主菜单项按钮  -->
                <Button Command="{Binding ExecuteMenuItemCommand}" Style="{StaticResource MenuButtonStyle}">
                    <StackPanel Orientation="Horizontal">
                        <!--  图标  -->
                        <Image
                            Width="24"
                            Height="24"
                            Margin="0,0,10,0"
                            Source="{Binding IconSource}" />

                        <!--  文本  -->
                        <TextBlock
                            VerticalAlignment="Center"
                            FontSize="{Binding FontSize}"
                            Text="{Binding Name}" />

                        <!--  展开指示器 - 简化版本  -->
                        <TextBlock
                            Margin="5,0,0,0"
                            VerticalAlignment="Center"
                            RenderTransformOrigin="0.5,0.5"
                            Text="▼"
                            Visibility="{Binding HasSubItems, Converter={StaticResource BooleanToVisibilityConverter}}">
                            <TextBlock.RenderTransform>
                                <RotateTransform Angle="0" />
                            </TextBlock.RenderTransform>
                            <TextBlock.Style>
                                <Style TargetType="TextBlock">
                                    <Style.Triggers>
                                        <DataTrigger Binding="{Binding IsExpanded}" Value="True">
                                            <DataTrigger.EnterActions>
                                                <BeginStoryboard>
                                                    <Storyboard>
                                                        <DoubleAnimation
                                                            Storyboard.TargetProperty="RenderTransform.Angle"
                                                            To="180"
                                                            Duration="0:0:0.2" />
                                                    </Storyboard>
                                                </BeginStoryboard>
                                            </DataTrigger.EnterActions>
                                            <DataTrigger.ExitActions>
                                                <BeginStoryboard>
                                                    <Storyboard>
                                                        <DoubleAnimation
                                                            Storyboard.TargetProperty="RenderTransform.Angle"
                                                            To="0"
                                                            Duration="0:0:0.2" />
                                                    </Storyboard>
                                                </BeginStoryboard>
                                            </DataTrigger.ExitActions>
                                        </DataTrigger>
                                    </Style.Triggers>
                                </Style>
                            </TextBlock.Style>
                        </TextBlock>
                    </StackPanel>
                </Button>
                <!--  子菜单项容器 - 简化版本  -->
                <StackPanel
                    Margin="15,0,0,0"
                    RenderTransformOrigin="0.5,0"
                    Visibility="{Binding IsExpanded, Converter={StaticResource BooleanToVisibilityConverter}}">
                    <StackPanel.RenderTransform>
                        <ScaleTransform ScaleY="1" />
                    </StackPanel.RenderTransform>
                    <StackPanel.Style>
                        <Style TargetType="StackPanel">
                            <Setter Property="Opacity" Value="0" />
                            <Style.Triggers>
                                <DataTrigger Binding="{Binding IsExpanded}" Value="True">
                                    <DataTrigger.EnterActions>
                                        <BeginStoryboard>
                                            <Storyboard>
                                                <DoubleAnimation
                                                    Storyboard.TargetProperty="Opacity"
                                                    To="1"
                                                    Duration="0:0:0.25" />
                                                <DoubleAnimation
                                                    Storyboard.TargetProperty="RenderTransform.ScaleY"
                                                    From="0"
                                                    To="1"
                                                    Duration="0:0:0.25" />
                                            </Storyboard>
                                        </BeginStoryboard>
                                    </DataTrigger.EnterActions>
                                </DataTrigger>
                            </Style.Triggers>
                        </Style>
                    </StackPanel.Style>

                    <ItemsControl ItemsSource="{Binding SubItems}">
                        <ItemsControl.ItemTemplate>
                            <DataTemplate>
                                <!--  改用Button统一处理点击事件，避免重复绑定  -->
                                <Button Command="{Binding ExecuteMenuItemCommand}" Style="{StaticResource SubMenuButtonStyle}">
                                    <StackPanel Orientation="Horizontal">
                                        <Image
                                            Width="20"
                                            Height="20"
                                            Margin="0,0,8,0"
                                            Source="{Binding IconSource}" />

                                        <TextBlock FontSize="{Binding FontSize}" Text="{Binding Name}" />
                                    </StackPanel>
                                </Button>
                            </DataTemplate>
                        </ItemsControl.ItemTemplate>
                    </ItemsControl>
                </StackPanel>
            </StackPanel>
        </DataTemplate>
    </UserControl.Resources>

    <ScrollViewer VerticalScrollBarVisibility="Auto">
        <ItemsControl
            Background="White"
            ItemTemplate="{StaticResource MenuItemTemplate}"
            ItemsSource="{Binding MenuItems}" />
    </ScrollViewer>
</UserControl>

```

`DropMenu.cs`

```csharp
using System;
using System.Windows;
using System.Windows.Controls;
using DropMenuControls.ViewModels;

namespace DropMenuControls
{
    /// <summary>
    /// 高级自定义下拉菜单控件
    /// 支持丰富的视觉效果、动画和交互体验
    /// 使用MVVM模式架构
    /// </summary>
    public partial class DropMenu : UserControl
    {
        public DropMenuViewModel ViewModel { get; private set; }

        // 依赖属性 - 菜单配置文件路径
        public static readonly DependencyProperty MenuConfigPathProperty =
            DependencyProperty.Register("MenuConfigPath", typeof(string), typeof(DropMenu),
                new PropertyMetadata("Menu.json", OnMenuConfigPathChanged));

        // 依赖属性 - 图标目录路径
        public static readonly DependencyProperty IconDirectoryProperty =
            DependencyProperty.Register("IconDirectory", typeof(string), typeof(DropMenu),
                new PropertyMetadata("Icons", OnIconDirectoryChanged));

        /// <summary>
        /// 菜单配置文件路径
        /// </summary>
        public string MenuConfigPath
        {
            get { return (string)GetValue(MenuConfigPathProperty); }
            set { SetValue(MenuConfigPathProperty, value); }
        }

        /// <summary>
        /// 图标目录路径
        /// </summary>
        public string IconDirectory
        {
            get { return (string)GetValue(IconDirectoryProperty); }
            set { SetValue(IconDirectoryProperty, value); }
        }

        /// <summary>
        /// 菜单项被点击事件
        /// </summary>
        public event EventHandler<MenuItemClickedEventArgs> MenuItemClicked;

        public DropMenu()
        {
            InitializeComponent();
            
            // 创建ViewModel并设置DataContext，传入配置路径
            ViewModel = new DropMenuViewModel(MenuConfigPath, IconDirectory);
            DataContext = ViewModel;
            
            // 订阅ViewModel的事件
            ViewModel.MenuItemClickedEvent += OnMenuItemClicked;
        }

        private void OnMenuItemClicked(MenuItemViewModel clickedItem)
        {
            // 触发控件的外部事件
            MenuItemClicked?.Invoke(this, new MenuItemClickedEventArgs(clickedItem));
        }

        // 依赖属性变化处理
        private static void OnMenuConfigPathChanged(DependencyObject d, DependencyPropertyChangedEventArgs e)
        {
            if (d is DropMenu control && e.NewValue is string newPath)
            {
                // 更新ViewModel的配置路径
                if (control.ViewModel != null)
                {
                    control.ViewModel.MenuConfigPath = newPath;
                    control.ViewModel.LoadMenuFromJson();
                }
            }
        }

        private static void OnIconDirectoryChanged(DependencyObject d, DependencyPropertyChangedEventArgs e)
        {
            if (d is DropMenu control && e.NewValue is string newIconDirectory)
            {
                // 更新ViewModel的图标目录
                if (control.ViewModel != null)
                {
                    control.ViewModel.IconDirectory = newIconDirectory;
                    control.ViewModel.LoadMenuFromJson(); // 重新加载以应用新的图标路径
                }
            }
        }

        /// <summary>
        /// 公共方法：重新加载菜单
        /// </summary>
        public void ReloadMenu()
        {
            ViewModel?.LoadMenuFromJson();
        }

        /// <summary>
        /// 公共方法：清除所有选中状态
        /// </summary>
        public void ClearSelection()
        {
            if (ViewModel != null)
            {
                foreach (var item in ViewModel.MenuItems)
                {
                    item.ClearSelection();
                }
            }
        }
    }

    /// <summary>
    /// 菜单项点击事件参数
    /// </summary>
    public class MenuItemClickedEventArgs : EventArgs
    {
        public MenuItemViewModel ClickedItem { get; }
        public string Command { get; }
        public string ItemName { get; }

        public MenuItemClickedEventArgs(MenuItemViewModel clickedItem)
        {
            ClickedItem = clickedItem;
            Command = clickedItem?.Command;
            ItemName = clickedItem?.Name;
        }
    }
}

```

`pachages.config`

```csharp
<?xml version="1.0" encoding="utf-8"?>
<packages>
  <package id="Newtonsoft.Json" version="13.0.3" targetFramework="net47" />
</packages>
```

## 在ZWCAD中使用

### 将菜单设定到PalletSet中

`Commands.cs`

```csharp
 public class Commands
 {
     internal static PaletteSet ps = null;
     [CommandMethod("TEST1")]
     public void TEST1()
     {
         if (ps == null)
         {
             ps = new PaletteSet("抽屉菜单");
             ps.Add("Menu", new PaletteBridge());
             ps.Visible = true;
             ps.Dock = ZwSoft.ZwCAD.Windows.DockSides.Left;
             if (ps.Size.Width < 200)
             {
                 ps.Size = new System.Drawing.Size(500, ps.Size.Height);
             }
         }
         else
             ps.Visible = !ps.Visible;
     }
     private static PaletteSet _palette;
     [CommandMethod("ShowDockWpf")]
     public void ShowDockWpf()
     {
         if (_palette == null)
         {
             _palette = new PaletteSet("我的 WPF Dock 面板")
             {
                 Style = PaletteSetStyles.ShowPropertiesMenu |
                     PaletteSetStyles.ShowAutoHideButton |
                     PaletteSetStyles.ShowCloseButton
             };

             _palette.Size = new System.Drawing.Size(300, 400);

             // WPF 控件
             var wpfCtrl = new WpfDropMenu();

             // 通过 ElementHost 封装
             var host = new ElementHost
             {
                 Dock = System.Windows.Forms.DockStyle.Fill,
                 Child = wpfCtrl
             };

             _palette.Add("工具面板", host);
         }

         _palette.Visible = true; // 显示
     }
 }
```

`WpfDropMenu.xaml`

```csharp
<UserControl
    x:Class="ZwObjectZrxNet3.Views.WpfDropMenu"
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
    xmlns:controls="clr-namespace:DropMenuControls;assembly=DropMenuControls"
    xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
    xmlns:local="clr-namespace:ZwObjectZrxNet3.Views"
    xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
    d:DesignHeight="450"
    d:DesignWidth="800"
    mc:Ignorable="d">
    <Grid>
        <controls:DropMenu x:Name="dropMenu" MenuItemClicked="CustomDropMenu_MenuItemClicked" />
    </Grid>
</UserControl>

```

`WpfDropMenu.cs`

```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using ZwSoft.ZwCAD.Windows.Data;
using ZwSoft.ZwCAD.ApplicationServices;
using System.Reflection;
using System.IO;
using Path = System.IO.Path;

namespace ZwObjectZrxNet3.Views
{
    /// <summary>
    /// WpfDropMenu.xaml 的交互逻辑
    /// </summary>
    public partial class WpfDropMenu : UserControl
    {
        public WpfDropMenu()
        {
            InitializeComponent();
            string path = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location);
            dropMenu.IconDirectory = Path.Combine(path, "Icons");
            dropMenu.MenuConfigPath = Path.Combine(path, "Menu.json");
        }

        private void CustomDropMenu_MenuItemClicked(object sender, DropMenuControls.MenuItemClickedEventArgs args)
        {
            string itemName = args.ItemName ?? "未知项目";
            string command = args.Command ?? "无命令";
            using (DocumentLock loc = ZwSoft.ZwCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument.LockDocument())
            {
                Document doc = ZwSoft.ZwCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument;
                if (!string.IsNullOrWhiteSpace(command) && command != "无命令")
                {
                    string testCommand = command;
                    //如果command没有/n 则加上
                    if (!command.StartsWith(" "))
                    {
                        testCommand = command + " ";
                    }

                    doc.SendStringToExecute(testCommand, false, false, false);
                    //MessageBox.Show($"执行命令: {command}",
                    //    "菜单项点击", MessageBoxButton.OK, MessageBoxImage.Information);
                }
            }
        }
    }
}

```

创建一个Winform用户控件做中间层转接WPF控件

`PaletteBridge.cs`

```csharp
namespace ZwObjectZrxNet3
{
    partial class PaletteBridge
    {
        /// <summary> 
        /// 必需的设计器变量。
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary> 
        /// 清理所有正在使用的资源。
        /// </summary>
        /// <param name="disposing">如果应释放托管资源，为 true；否则为 false。</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region 组件设计器生成的代码

        /// <summary> 
        /// 设计器支持所需的方法 - 不要修改
        /// 使用代码编辑器修改此方法的内容。
        /// </summary>
        private void InitializeComponent()
        {
            this.elementHost1 = new System.Windows.Forms.Integration.ElementHost();
            this.wpfDropMenu1 = new Views.WpfDropMenu();
            this.SuspendLayout();
            // 
            // elementHost1
            // 
            this.elementHost1.Dock = System.Windows.Forms.DockStyle.Fill;
            this.elementHost1.Location = new System.Drawing.Point(0, 0);
            this.elementHost1.Name = "elementHost1";
            this.elementHost1.Size = new System.Drawing.Size(150, 150);
            this.elementHost1.TabIndex = 0;
            this.elementHost1.Text = "elementHost1";
            this.elementHost1.Child = wpfDropMenu1;
            // 
            // PallateBridge
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.Controls.Add(this.elementHost1);
            this.Name = "PallateBridge";
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.Integration.ElementHost elementHost1;
        private Views.WpfDropMenu wpfDropMenu1;
    }
}
```

![image-20250901163639624](http://image.jerryma.xyz//images/20250901-image-20250901163639624.png)

`Menu.json`

```json
{
    "ItemMenu": [
        {
            "Name":"Home",
            "Icon":"Home.png",
            "FontSize":16,
            "Command": "Home",
            "SubItems":[]
        },
        {
            "Name": "Customer",
            "Icon": "BootstrapIcons-_1Circle.png",
            "FontSize":16,
            "SubItems": [
                {
                    "Name": "Customer1",
                    "Icon": "notification 22.png",
                    "FontSize":16,
                    "Command": "Test1"
                },
                {
                    "Name": "Customer2",
                    "Icon": "ET 28.png",
                    "FontSize":16,
                    "Command": "Test2"
                },
                {
                    "Name": "Customer3",
                    "Icon": "email 33.png",
                    "FontSize":16,
                    "Command": "Test3"
                },
                {
                    "Name": "Customer4",
                    "Icon": "edit 13.png",
                    "FontSize":16,
                    "Command": "Test4"
                },
                {
                    "Name": "Customer5",
                    "Icon": "credits 6.png",
                    "FontSize":16,
                    "Command": "Test5"
                }
            ]
        },
        {
            "Name": "Providers",
            "Icon": "BootstrapIcons-_2Circle.png",
            "FontSize":16,
            "SubItems":[
                {
                    "Name": "Provider1",
                    "Icon": "phonecall 24.png",
                    "FontSize":16,
                    "Command": "Test1"
                },
                {
                    "Name": "Provider2",
                    "Icon": "cart 11.png",
                    "FontSize":16,
                    "Command": "Test2"
                },
                {
                    "Name": "Provider3",
                    "Icon": "calculator 31.png",
                    "FontSize":16,
                    "Command": "Test3"
                }
            ]
        },
        {
            "Name": "Others",
            "Icon": "BootstrapIcons-_3Circle.png",
            "FontSize":16,
            "SubItems":[
                {
                    "Name": "Other1",
                    "Icon": "social_server_fault 81.png",
                    "FontSize":16,
                    "Command": "Test1"
                },
                {
                    "Name": "Other2",
                    "Icon": "check 43.png",
                    "FontSize":16,
                    "Command": "Test2"
                }
            ]
        }
    ]
}
```


