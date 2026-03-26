---
title: "Using .NET Framework 4.0 in various AutoCAD versions"
date: 2012-07-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - Migration
description: "We are currently compiling our extensions with .NET 3.5 (which uses CLR 2.0), and they work fine for AutoCAD 2008-2011."
author: Autodesk
---
# Using .NET Framework 4.0 in various AutoCAD versions

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/using-net-framework-40-in-various-autocad-versions.html

## 文章内容

By Adam Nagy
We are currently compiling our extensions with .NET 3.5 (which uses CLR 2.0), and they work fine for AutoCAD 2008-2011.
Is it possible to upgrade our projects to .NET 4.0, which uses the new CLR 4, as long as the .NET 4.0 framework is installed on the client machines?
Also, in case .NET framework 4 is installed on a client machine, will AutoCAD 2010 and 2011 use that version, regardless of whether a .NET 4 DLL has been NetLoaded in AutoCAD?
Solution
You can set acad.exe.config to make AutoCAD 2011 load Framework 4 on startup, and the same with 2010 update 1, but there are likely to be features that are broken if you force AutoCAD to load Framework 4 for those releases – so you’d have to extensively test every AutoCAD feature your customer wants to use. In case of pre-2010 versions, it's even more likely that you'll run into problems when forcing them to load Framework 4.0.
The load behavior of the .NET Framework (i.e. which framework version is loaded) is governed by the .NET Runtime Execution Engine (mscoree.dll) – it’s not AutoCAD specific – so please review Microsoft’s documentation to understand the details of .NET Framework Runtime load behaviors. However, in a nutshell:
Prior to Framework 4, mscoree would load the newest .NET Framework installed on the machine, unless an executable requested a specific (older) framework version. You can do that for AutoCAD by editing acad.exe.config. 
This changed for Framework 4. Mscoree now loads the framework version the executable is bound to, and will not load a newer version unless you explicitly configure the executable to do so. (So the pre-Framework 4 default behavior has been completely reversed in Framework 4). 
The upshot of this is that versions of AutoCAD prior to AutoCAD 2012 will not automatically load Framework 4 even if that Framework is installed on the same machine. Instead they will load the newest installed pre-Framework 4 Framework.
We will not provide support for attempting to use Framework 4 features with older AutoCAD versions, i.e. pre-2012. (those AutoCAD versions have not been extensively tested for this configuration, and so it's not something we can support). If you attempt to load a .NET DLL that uses Framework 4 features into AutoCAD 2011, AutoCAD will display an error on the commandline that the DLL “is built by a runtime newer than the currently loaded runtime and cannot be loaded”.

## 评论

**内容**: Mike LC said...
Hello! Nice article.
I'm developing an application using Vb.net and Autocad 2011 with Franework 4. Everything is fine in my machine.
But when I try to compile it to be used in another machine that has AutoCad 2010, I replace the acmgd.dll and acdbmgd.dll with the 2010 versions, set the framework to 3.5 and this error appears: "object reference not set to an instance of an object" pointing to a .resx file and I can't go on.
Any help, please? I'm stuck here. Thanks
Reply
01/28/2013 at 07:13 AM

---
**内容**: Adam Nagy said in reply to Mike LC...
Hi Mike,
This looks like a VS issue. Searching for
>>>>>
"object reference not set to an instance of an object" resx
<<<<<
on the net I ran into the following page, which I think looks quite promising. Please give it a try. :)
http://www.codeease.com/object-reference-not-set-to-an-instance-of-an-object-in-resx-resource-file.html
Cheers,
Adam
Reply
01/28/2013 at 07:48 AM

---
**内容**: Mike LC said in reply to Adam Nagy...
Adam,
That was exactly what I was looking for!
Many thanks,
Mike
Reply
01/28/2013 at 08:39 AM

---
