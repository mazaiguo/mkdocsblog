---
title: "Is IExtensionApplication.Initialize() called in Document context?"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - Plugin
  - Unicode
description: "It seems that I do not need to lock the document in the Initialize() function of my AddIn in order to modify it. Which suggests that it's in Docume..."
author: Autodesk
---
# Is IExtensionApplication.Initialize() called in Document context?

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/is-iextensionapplicationinitialize-called-in-document-context.html

## 文章内容

By Adam Nagy
It seems that I do not need to lock the document in the Initialize() function of my AddIn in order to modify it. Which suggests that it's in Document context. I thought it would be in application context.
Solution
Depending on how your AddIn is loaded its Initialize() function will be either in Document or Application/Session context.
If it's loaded using the NETLOAD command then Initialize() will run in Document context, but if loaded using the auto-load mechanism available through registry settings, then it will be in Application/Session context.
You can easily test it with a simple application:
using System;
using System.Windows.Forms;
  using Autodesk.AutoCAD.Runtime;
using acApp = Autodesk.AutoCAD.ApplicationServices.Application;
  [assembly: ExtensionApplication(typeof(MyAddIn.MyApp))]
  namespace MyAddIn
{
  public class MyApp : IExtensionApplication
  {
    public void Initialize()
    {
      MessageBox.Show("IsApplicationContext = " +
        acApp.DocumentManager.IsApplicationContext.ToString());
    }
      public void Terminate()
    {
    }
  }
}
If your application is meant to be supporting both loading mechanisms and you're calling context dependent functions inside Initialize(), then you should check the DocumentManager.IsApplicationContext as shown in the above code.

