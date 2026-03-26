---
title: "Exception while debugging AutoCAD from a .NET project in a multi-project VS 2010 solution"
date: 2013-02-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - C++
  - COM Interop
  - Layer
description: "This problem only occurs when we have multiple projects in a VS 2010 solution with a mix of C++ and .NET projects in the solution. Specifically, if..."
author: Autodesk
---
# Exception while debugging AutoCAD from a .NET project in a multi-project VS 2010 solution

发布日期: 2013-02-01

原始链接: https://adndevblog.typepad.com/autocad/2013/02/exception-while-debugging-autocad-from-a-net-project-in-a-multi-project-vs-2010-solution.html

## 文章内容

By Gopinath Taget
This problem only occurs when we have multiple projects in a VS 2010 solution with a mix of C++ and .NET projects in the solution. Specifically, if we have a .NET project as an active project and we configure the debugger to launch AutoCAD, the debugger will launch AutoCAD from the active .NET project. The exception occurs only when the debugger is launched from a .NET project. It does not occur if the debugger is launched from the C++ projects.
The exception will look something like "Managed Debugging Assistant 'PInvokeStackImbalance' has detected a problem in..."
According to Microsoft, this issue occurs because of changes in interoperability services in .NET 4.0 compared to previous version (.NET 3.5). Specifically, this behavior results from an effort "To improve performance in interoperability with unmanaged code, incorrect calling conventions in a platform invoke now cause the application to fail. In previous versions, the marshaling layer resolved these errors up the stack".
According to Microsoft, here are the recommendations when this exception occurs:
Debugging your applications in Microsoft Visual Studio 2010 will alert you to these errors so you can correct them.
If you have binaries that cannot be updated, you can include the <NetFx40_PInvokeStackResilience> element in your application's configuration file to enable calling errors to be resolved up the stack as in earlier versions. However, this may affect the performance of your application.
For more information, please take a look at the documentation for "Platform invoke" feature under "Interoperability" section in the following link:
http://msdn.microsoft.com/en-us/library/ee941656(v=VS.100).aspx
So setting the NetFx40_PInvokeStackResilience in acad.exe.config file (found in the AutoCAD install folder) will resolve this exception:
<configuration>
<startup useLegacyV2RuntimeActivationPolicy="true">
<supportedRuntime version="v4.0"/>
</startup>
<!--All assemblies in AutoCAD are fully trusted so there's no point generating publisher evidence-->
<runtime>
<generatePublisherEvidence enabled="false"/>
<NetFx40_PInvokeStackResilience enabled="1|0"/>
</runtime>
</configuration>

