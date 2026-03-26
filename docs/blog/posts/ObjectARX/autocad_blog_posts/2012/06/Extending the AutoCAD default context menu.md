---
title: "Extending the AutoCAD default context menu"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - Plugin
  - Unicode
description: "Previously I have posted an article on adding object specific context menu (that is, extending the context menu only when a particular entity type ..."
author: Autodesk
---
# Extending the AutoCAD default context menu

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/extending-the-autocad-default-context-menu.html

## 文章内容

By Virupaksha Aithal
Previously I have posted an article on adding object specific context menu (that is, extending the context menu only when a particular entity type is selected.) Now, below code shows the procedure to extend the AutoCAD default context menu using API “AddDefaultContextMenuExtension”.
[CommandMethod("DefaultMenuTest")]
static public void DefaultMenuTest()
{
    ContextMenuExtension contectMenu =
                                new ContextMenuExtension();
      contectMenu.Title = "Default Menu Test";
      MenuItem Item1 = new MenuItem("Test1");
    contectMenu.MenuItems.Add(Item1);
      MenuItem Item1a = new MenuItem("Sub Test1");
    Item1a.Click += new EventHandler(Item1a_Click);
    Item1.MenuItems.Add(Item1a);
      MenuItem Item2 = new MenuItem("Test2");
    Item2.Click += new EventHandler(Test2_Click);
    contectMenu.MenuItems.Add(Item2);
      //App Default menu
    Application.AddDefaultContextMenuExtension(contectMenu);
  }
  static void Item1a_Click(object sender, EventArgs e)
{
    Application.ShowAlertDialog("Test1a clicked\n");
}
    static void Test2_Click(object sender, EventArgs e)
{
    Application.ShowAlertDialog("Test2 clicked\n");
}

