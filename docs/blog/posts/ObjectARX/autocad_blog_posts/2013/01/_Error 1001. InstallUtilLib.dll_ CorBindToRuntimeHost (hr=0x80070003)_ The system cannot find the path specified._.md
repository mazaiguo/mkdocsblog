---
title: ""Error 1001. InstallUtilLib.dll: CorBindToRuntimeHost (hr=0x80070003): The system cannot find the path specified.""
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "Recently, our AppStore team ran into a problem with the AppStore build process by which a developer had sent us an MSM Merge Module for merging int..."
author: Autodesk
---
# "Error 1001. InstallUtilLib.dll: CorBindToRuntimeHost (hr=0x80070003): The system cannot find the path specified."

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/error-1001-installutillibdll-corbindtoruntimehost-hr0x80070003-the-system-cannot-find-the-path-specified.html

## 文章内容

By Fenton Webb
Recently, our AppStore team ran into a problem with the AppStore build process by which a developer had sent us an MSM Merge Module for merging into our AppStore MSI. The problem was that when the installer ran, this error appeared:
"Error 1001. InstallUtilLib.dll: CorBindToRuntimeHost (hr=0x80070003): The
system cannot find the path specified."
The problem appears to be that MSM’s created with Visual Studio only like to be merged with MSI’s that are also built with Visual Studio. So even if you merge a Visual Studio MSM with a verifiably decent MSI tool like InstallSheild or Wise project it will still fail.
I worked out a pretty simple solution, which took me quite a bit of effort to master Basically, I created my own merge module MSM which contained the missing MSI components that the Visual Studio MSM was looking for, it’s called VisualStudioCompatibility.msm.
If you merge the VisualStudioCompatibility.msm into your non VS MSI before merging your VS MSM, it should work fine.
By the way, feel free to use the VisualStudioCompatibility.msm as you wish, but at your own risk.

## 评论

**内容**: Jack said...
hello, this has worked for me, thanx you very much,
But now the problem is while uninstalling, I get the same error again,
Reply
03/20/2013 at 10:11 PM

---
**内容**: Fenton Webb said...
Hey Jack
probably, you will have to change your MSI (the one that has been fully merged with my solution above) so that the InstallExecuteSequence table contains "Not Installed" for the sequence items that cause the issue.
Or, you can solve the issue where the InstallUtil components are not found on uninstall and put us all out of our misery!!!
Reply
03/21/2013 at 10:36 AM

---
**内容**: Jack said...
Thanx Fenton, will chk it out..
Reply
03/22/2013 at 02:25 AM

---
**内容**: Arne Smebye said...
Thank you, this worked for me. We have a merge module created by a VS setup project. It's used in a IS msi project.
Reply
04/13/2015 at 02:46 AM

---
