---
title: "Object specific context menu using .NET"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - Unicode
description: "Use "AddObjectContextMenuExtension" API passing the type of the class and the content menu to attach a menu to an entity type. Refer below code sam..."
author: Autodesk
---
# Object specific context menu using .NET

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/object-specific-context-menu-using-net.html

## 文章内容

By Virupaksha Aithal
Use "AddObjectContextMenuExtension" API passing the type of the class and the content menu to attach a menu to an entity type. Refer below code sample.
[CommandMethod("ContextMenuExtTest")]
static public void ContextMenuExtTest()
{
    ContextMenuExtension contectMenu =
                                new ContextMenuExtension();
      MenuItem item0 = new MenuItem("Line context menu");
    contectMenu.MenuItems.Add(item0);
    MenuItem Item1 = new MenuItem("Test1");
    Item1.Click += new EventHandler(Test1_Click);
    item0.MenuItems.Add(Item1);
    MenuItem Item2 = new MenuItem("Test2");
    Item2.Click += new EventHandler(Test2_Click);
    item0.MenuItems.Add(Item2);
      //for custom entity, replace the "Line" with .NET
    //(managed) wrapper of custom entity
    Application.AddObjectContextMenuExtension(
                Line.GetClass(typeof(Line)), contectMenu);
  }
static void Test1_Click(object sender, EventArgs e)
{
    Application.ShowAlertDialog("Test1 clicked\n");
}
  static void Test2_Click(object sender, EventArgs e)
{
    Application.ShowAlertDialog("Test2 clicked\n");
}

## 评论

**内容**: Jürgen A. Becker said...
Hi,
is it possible to ad an context menu to an object identified by an EED not with typeof()?
Many thanks for your help.
Jürgen
Reply
06/15/2012 at 05:34 AM

---
**内容**: Virupaksha Aithal said...
Hi Jurgen,
Yes, i think it possible. Please take a look at my new post http://adndevblog.typepad.com/autocad/2012/06/enabledisable-object-context-menu-for-specific-entity.html
Thanks
Viru
Reply
06/18/2012 at 12:34 AM

---
**内容**: Jürgen said in reply to Virupaksha Aithal...
Hi,
thanks for your answer.
I think you meann this or not?
"for custom entity, replace the "Line" with .NET (managed) wrapper of custom entity"
Do you have an example for that?
Thanks Jürgen
Reply
06/22/2012 at 05:46 AM

---
**内容**: Sanjay Kulkarni said...
The statement
ContextMenuExtension contectMenu = _
new ContextMenuExtension();
creates an error
Type 'ContextMenuExtension' is not defined.
I am importing the 'Autodesk.AutoCAD.Windows' Namespace which I have imported in my class.
Am I missing something?
Reply
08/13/2012 at 07:53 AM

---
