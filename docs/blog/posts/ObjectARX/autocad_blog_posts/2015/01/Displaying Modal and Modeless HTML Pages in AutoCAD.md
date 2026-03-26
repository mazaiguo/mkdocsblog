---
title: "Displaying Modal and Modeless HTML Pages in AutoCAD"
date: 2015-01-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
description: "In AutoCAD 2014 , two new APIs are introduced  to display HTML webpages in AutoCAD , most of you are aware of displaying forms these  API s are lit..."
author: Autodesk
---
# Displaying Modal and Modeless HTML Pages in AutoCAD

发布日期: 2015-01-01

原始链接: https://adndevblog.typepad.com/autocad/2015/01/displaying-modal-and-modeless-html-pages-in-autocad.html

## 文章内容

By Madhukar Moogala
In AutoCAD 2014 , two new APIs are introduced  to display HTML webpages in AutoCAD , most of you are aware of displaying forms these  API s are little addition to the existing ones
Application.ShowModalWindow
public static bool ShowModalWindow(Uri htmlPage);
public static bool ShowModalWindow(IntPtr owner, Uri htmlPage);
public static bool ShowModalWindow(IntPtr owner, Uri htmlPage, bool persistSizeAndPosition);
  Application.ShowModelessWindow.
  public static void ShowModelessWindow(Uri htmlPage);
public static void ShowModelessWindow(IntPtr owner, Uri htmlPage);
public static void ShowModelessWindow(IntPtr owner, Uri htmlPage, bool persistSizeAndPosition);
Sample Code:
public void test()
{
Uri uri = new Uri("http://adndevblog.typepad.com/autocad/");
  IntPtr owner = Autodesk.AutoCAD.ApplicationServices.Application.MainWindow.Handle;
/*Modeless */
//Autodesk.AutoCAD.ApplicationServices.Application.ShowModelessWindow(owner, uri, true);
/*Modal Window*/
bool rc = Autodesk.AutoCAD.ApplicationServices.Application.ShowModalWindow(owner, uri, true);
  }
  Snapshot :

