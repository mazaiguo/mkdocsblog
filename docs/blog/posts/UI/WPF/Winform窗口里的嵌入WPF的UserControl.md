---
title: Winform窗口里的嵌入WPF的UserControl
date: 2024-04-12
categories:
  - windows程序
 
tags:
  - Winform
  - WPF
  - UserControl
  - 事件处理
description: 在Winform窗口中嵌入WPF UserControl并处理窗口关闭事件的详细方法
author: JerryMa
---

# Winform窗口里的嵌入WPF的UserControl,关闭Winform父窗体的方法

## 可以在form_load事件里把this传给UserControl，然后在usercontrol里调用form的各种方法，不过这种做法不太好，耦合性较高。

## 标准做法是用事件传递

### UserControl里加如下代码： 

```csharp
public delegate void FormCloseEventHandler(object sender, EventArgs e);
public event FormCloseEventHandler FormClose;
private void button_quit_Click(object sender, EventArgs e)
{
if (this.FormClose != null)
{
FormClose(this, new EventArgs());
}
}
```

 

### 在Form里添加如下代码： 

form_load事件里：

this.userControl.FormClose += new UserControl.FormCloseEventHandler(this.userControl_FormClose); //不明白为什么是用类方法而非对象方法？

然后用这个方法不好使，还是出现我之前的鬼影问题

```csharp
        private void userControl_FormClose(object sender, EventArgs e)
{
this.Close();
}
```

改成用这个方法， 把elementHost1这个对象给销毁掉，这样似乎就好了， 鬼影的问题是在用了第三方的WpfToolkit之中的DataGrid后出现的，如果用.NET4.0里面的DataGrid就没有问题。 虽然麻烦点，但是也算是个收获。

```csharp
  private void UserControl_FormClose(object sender, EventArgs e)        
  {
              this.elementHost1.Dispose(
              );            
              this.Close();        }
```