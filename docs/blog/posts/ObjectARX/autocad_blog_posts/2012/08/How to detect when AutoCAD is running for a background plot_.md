---
title: "How to detect when AutoCAD is running for a background plot?"
date: 2012-08-01
categories:
  - AutoCAD C++
tags:
  - API
  - AutoCAD
  - C++
  - Plot
description: "I need to detect when AutoCAD is running in background plot in order to handle this appropriately concerning my custom applications."
author: Autodesk
---
# How to detect when AutoCAD is running for a background plot?

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/how-to-detect-when-autocad-is-running-for-a-background-plot.html

## 文章内容

By Philippe Leefsma
Q:
I need to detect when AutoCAD is running in background plot in order to handle this appropriately concerning my custom applications.
What is the best way to achieve this?
A:
One suggestion is to check using Win32 API “GetCommandLine” the command line string used to run AutoCAD and parse it to see if it contains the “-b” and “-pl” switches.
Here is my demand loaded arx startup procedure:
virtual AcRx::AppRetCode On_kInitAppMsg (void *pkt)
{
      // TODO: Load dependencies here
        // You *must* call On_kInitAppMsg here
      AcRx::AppRetCode retCode =AcRxArxApp::On_kInitAppMsg (pkt) ;
            // TODO: Add your initialization code here
      ACHAR* cmdline = GetCommandLine();
        std::ofstream ofs(
          L"c:\\Temp\\log.txt",
          std::ios::out | std::ios::binary);
        std::wstring wstr(cmdline);
        ofs.write((char *) wstr.c_str(), wstr.length() * sizeof(wchar_t));
        ofs.close();
            return (retCode) ;
}
-
Once a background plot has been run, the content of my log file is as follow:
"C:\Program Files\Autodesk\ACADM 2009\acad.exe" 
-pl  -b C:\DOCUME~1\leefsmp\LOCALS~1\Temp\BG074D~1\BGPlot.scr

