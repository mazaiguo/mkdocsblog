---
title: "Load additional dll’s"
date: 2012-04-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
description: "If you have a main .NET dll that is loaded into AutoCAD and it needs to access functionality from another dll, then here are a couple of ways you c..."
author: Autodesk
---
# Load additional dll’s

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/load-additional-dlls.html

## 文章内容

By Adam Nagy
If you have a main .NET dll that is loaded into AutoCAD and it needs to access functionality from another dll, then here are a couple of ways you can try to load the extra dll.
Make the extra dll strongly named and modify acad.exe.config:
Note: a dll that is referencing AutoCAD .NET assemblies cannot be made strongly named since those assemblies are not strongly named either
<assemblyBinding xmlns="urn:schemas-microsoft-com:asm.v1">
  <dependentAssembly>
    <assemblyIdentity
      name="DllToLoad"
      publicKeyToken="cace528f15d690ab"
      culture="neutral" />
    <codeBase
      version="1.0.0.0"
      href= "file://C:\Documents and Settings\Administrator\My Documents\Visual Studio 2010\Projects\TestDllLoad\DllToLoad\bin\Debug\DllToLoad.dll"/>
  </dependentAssembly>
</assemblyBinding>
  Register the extra dll for autoload on startup:
either by creating an entry in the registry – look at <objectarx sdk>\docs\arxdoc.chm >> Demand Loading on AutoCAD Startup
or using the AutoLoader mechanism that is available since AutoCAD 2012. Here you can also set dependency between the dll's to make sure that the extra dll is loaded before the main dll
Load the extra dll before actually needing it:
Since .NET does delay loading by default, i.e. it only tries to load extra resources when actually needed, you could place the call to the extra dll into a separate function and call LoadFrom before that. .NET will only try to resolve the function of the external dll when it enters that extra function (CallDllFunction in this case)
using System;
using Autodesk.AutoCAD.Runtime;
  namespace DllCaller
{
  public class Functions
  {
    [CommandMethod("CallDllFunctionWithPreload")]
    public static void CallDllFunctionWithPreload()
    {
      System.Reflection.Assembly.LoadFrom(
        @"C:\Documents and Settings\Administrator\" +
        @"My Documents\Visual Studio 2010\Projects\" +
        @"TestDllLoad\DllToLoad\bin\Debug\DllToLoad.dll");
        CallDllFunction();
    }
      [CommandMethod("CallDllFunction")]
    public static void CallDllFunction()
    {
      // If the user calls this command, then it will fail,
      // but if he calls CallDllFunctionWithPreload command
      // then this will succeed
      DllToLoad.Functions.MyShowMessage();
    }
  }
}
  Handle AppDomain.AssemblyResolve event and load the assembly there
Place the extra dll in a subfolder of the AutoCAD install folder and modify <probing privatepath=""> accordingly in acad.exe.config
Place the dll's of your addin into the AutoCAD install folder. This is the official suggestion, by the way, but it may not always be viable

