---
title: "Remote debugging using msvsmon.exe"
date: 2012-07-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - Plugin
description: "I would like to debug my AddIn running on a virtual machine from my local machine. Could you list the steps I need to follow?"
author: Autodesk
---
# Remote debugging using msvsmon.exe

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/remote-debugging-using-msvsmonexe.html

## 文章内容

By Adam Nagy
I would like to debug my AddIn running on a virtual machine from my local machine. Could you list the steps I need to follow?
Solution
I think it does not really matter if you are trying to debug remotely between virtual machines or real ones, the procedure should be the same. I tested the below steps using two virtual machines: adam3596 is the one that I'm debugging from (local computer), and adam3597 is the one where the application that loads my addin is running (remote computer). Also, I'm testing with a .NET AddIn that is loaded into AutoCAD MEP 2009.
We'll be usig Windows Authentication to access one pc from the other, and for this we need to make sure that both the local and remote pc has a local account with the same name and password
  As msvsmon.exe would warn us about it as well, we need to set the local policy on both computers as follows:
Local Security Settings > Security Settings > Local Policies > Security Options > Network access: Sharing and security model for local accounts = Classic - local users authenticate as themselves
 

  We need to copy msvsmon.exe and its related files over to the remote pc or virtual machine. Just copy the whole Remote Debugger folder to the remote machine. In case of Visual Studio 2008 you'll find the necessary folder under
C:\Program Files\Microsoft Visual Studio 9.0\Common7\IDE\Remote Debugger
  Set up a folder that is visible from both computers and use that as your project's build folder
 

In some cases I had issues with attaching to the remote process - e.g. AutoCAD simply froze - but if I started the exe from Visual Studio then all worked fine. In the project's debug settings use the remote pc and set the path of the executable you want to start
 

If you also want to set the working folder then it's better to avoid using network names that are not mapped. If you want to use a network folder just right-click on the network drive in Explorer and choose Map Network Drive... and then use the mapped name, e.g. Z:\VMwareShare instead of \\.host\Shared Folders\VMwareShare
  Start msvsmon.exe on the remote pc
 

Start debugging your project on the local pc and NETLOAD your addin in AutoCAD on the remote pc
 
You'll find several articles on the net about remote debugging if you simply search for msvsmon.exe.

