---
title: "Load and run VBA macro through .NET command"
date: 2016-07-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - VBA
description: "Below code shows the procedure to load and run a VBA macro through .NET command. Here AutoCAD ActiveX API LoadDVB & RunMacro is used. As the code u..."
author: Autodesk
---
# Load and run VBA macro through .NET command

发布日期: 2016-07-01

原始链接: https://adndevblog.typepad.com/autocad/2016/07/load-and-run-vba-macro-through-net-command.html

## 文章内容

By Virupaksha Aithal
Below code shows the procedure to load and run a VBA macro through .NET command. Here AutoCAD ActiveX API LoadDVB & RunMacro is used. As the code uses dynamic keyword, to use this code no need to refer the AutoCAD ActiveX (interop) references.
[CommandMethod("LoadRunVBAcOMMAND")]
public static void LoadDVBFile()
{
    dynamic acadApplication = Application.AcadApplication;
    acadApplication.LoadDVB(@"C:\cases\area.dvb");
    acadApplication.RunMacro("mytest");
}

## 评论

**内容**: Lily said...
Hello, Virupaksha Aithal
i have a problem with my Auto cad 2017. my Auto cad are continuously restarting. i have purchased this software from official site but support centre are not that much responsive.i Am taking Auto Cad Training in surat after googling i got your blog and i have hope you will solve my problem.
Reply
05/09/2017 at 11:55 PM

---
