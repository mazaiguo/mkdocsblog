---
title: "Use 64 bit ActiveX component from a .NET assembly"
date: 2012-07-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - COM
  - Plugin
description: "I've been using the ADN utilities, which include some ActiveX controls. Now I'm migrating my project to x64 OS and have downloaded the 64 bit versi..."
author: Autodesk
---
# Use 64 bit ActiveX component from a .NET assembly

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/use-64-bit-activex-component-from-a-net-assembly.html

## 文章内容

By Adam Nagy
I've been using the ADN utilities, which include some ActiveX controls. Now I'm migrating my project to x64 OS and have downloaded the 64 bit version of the controls, however I cannot place them on my Form in Visual Studio.
Solution
Visual Studio is 32 bit on a 64 bit operating system as well, and it does not support 64 bit ActiveX components in the Form Designer. What you could do is create the component programmatically in your code.
In the following example I will be adding the AcadColor.ocx control to my .NET Form.
First, we need to create a wrapper for the ActiveX control. I start up Visual Studio 2008 x64 Win64 Command Prompt, go to the directory where the control is and run aximp.exe on it: Note: in case of Vista/Windows 7 you need to run the Command Prompt utility with elevated rights - right-click on the Command Prompt shortcut and select Run as administrator
If you get back the error AxImp Error: Did not find a registered ActiveX control in ..., then register the control first in the same command prompt window using regsvr32 AcadColor.ocx.
Now we can reference the created 2 dll's from the project (AutoCADColor.dll and AxAutoCADColor.dll) and then add the following code to the Form's constructor:
using System;
using System.Windows.Forms;
  namespace TestActiveX
{
  public partial class Form1 : Form
  {
    private AxAutoCADColor.AxAcadColor acadColor;
      public Form1()
    {
      InitializeComponent();
        acadColor = new AxAutoCADColor.AxAcadColor();
      acadColor.Location = new System.Drawing.Point(7, 7);
      acadColor.Size = new System.Drawing.Size(150, 20);
      acadColor.Visible = true;
      this.Controls.Add(acadColor);
    }
  }
}
Once we compiled the project to either Any CPU or x64, we can run it:

