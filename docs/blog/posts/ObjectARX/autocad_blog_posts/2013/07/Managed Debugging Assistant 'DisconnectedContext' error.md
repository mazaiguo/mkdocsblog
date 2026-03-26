---
title: "Managed Debugging Assistant 'DisconnectedContext' error"
date: 2013-07-01
categories:
  - AutoCAD
tags:
  - Unicode
description: "I start an external application from my custom command and wait until it finishes:"
author: Autodesk
---
# Managed Debugging Assistant 'DisconnectedContext' error

发布日期: 2013-07-01

原始链接: https://adndevblog.typepad.com/autocad/2013/07/managed-debugging-assistant-disconnectedcontext-error.html

## 文章内容

By Marat Mirgaleev
Issue
I start an external application from my custom command and wait until it finishes:
      Dim ExternalApp As New System.Diagnostics.Process()
      ExternalApp.StartInfo.FileName = "myApp.exe"
      ExternalApp.Start()
      ExternalApp.WaitForExit()
The problem is that after 10-15 minutes a message appears:
Managed Debugging Assistant 'DisconnectedContext' has detected a problem in 'C:\Program Files\Autodesk\AutoCAD 2014\acad.exe'.
Additional Information: Context 0x163158 is disconnected. No proxy will be used to service the request on the COM component. This may cause corruption or data loss. To avoid this problem, please ensure that all contexts/apartments stay alive until the application is completely done with the RuntimeCallableWrappers that represent COM components that live inside them.
After that AutoCAD becomes unstable and may crash.
Could you let me know why this happens and how to solve it?
Solution
In the code snippet above the WaitForExit() call is holding up the main thread, so AutoCAD cannot dispatch messages. This is going to cause all sorts of problems (e.g. Windows will “think” that the app is hung and replace the main window with its own shadow copy).
You should come up with a solution that does not block the main thread or, the very least, you should run a message loop that dispatches messages.
If you would like to do some background processing in AutoCAD, this link may help: Use Thread for background processing

