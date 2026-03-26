---
title: "Installing and using RealDWG 32bit on 64bit Windows"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - DWG
description: "If you are developing a RealDWG application for both 32bit and 64bit Windows you have probably wondered if 32bit RealDWG is supported on Windows 64..."
author: Autodesk
---
# Installing and using RealDWG 32bit on 64bit Windows

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/installing-and-using-realdwg-32bit-on-64bit-windows.html

## 文章内容

by Fenton Webb
If you are developing a RealDWG application for both 32bit and 64bit Windows you have probably wondered if 32bit RealDWG is supported on Windows 64bit…
Let me answer some of your questions.
Can you install the RealDWG 32bit SDK on 64bit Windows
Yes you can, installing the RealDWG 32bit SDK is supported on 64bit Windows. 
Can I create a RealDWG 32bit application and install it on 64bit Windows.
Yes you can, but as with all Autodesk products, where we have a 64bit version of the software we don’t support installing the 32bit version on Windows 64bit. The reason is because, although 32bit versions of our software are capable of running on 64bit Windows, due to the huge amount of work needed to test and release a product on a Windows platform, given the total number of user requests for 32bit Autodesk products on 64bit Windows, it doesn’t make business sense to support it.
Does RealDWG even need to be installed to use it?
Actually, as long as you don’t use the RealDWG COM API, then you can use it just like you would the ObjectARX SDK – all I do is copy the RealDWG SDK files from machine to machine, I never install it.
How do I add the RealDWG components to my installer so that they get installed automatically with my runtime?
It’s really easy; all you have to do is add all of the MSI Merge Modules (MSM) files to your installer MSI. Once you have done that, save the MSI. Next, go to the Property table of the MSI and edit the newly created ODBXHOSTAPPREGROOT property – make sure the value of that property reflects the same value that your RealDWG HostApplicationServices.GetRegistryProductRootKey() returns. Check out the Redistribution Requirements section of the readdbx.chm file found in the RealDWG SDK for more information.

## 评论

**内容**: Eric Mills said...
Windows 7 64 bit, RealDWG 2013.
I installed 64bit RealDWG 2013 on my machine.
I added the environment paths:
C:\Program Files\Autodesk\RealDWG 2013
C:\Program Files\Autodesk\RealDWG 2013\Fonts
C:\Program Files\Autodesk\RealDWG 2013\Support
I added the reference
C:\Program Files\Autodesk\RealDWG 2013\AcDbMgd.dll
I built an app and everything was working fine.
Now I have to recreate the app for 32bit machines.
I know that I can develop 32bit apps on 64bit, but it is not working.
When I go to install the 32bit RealDWG, the first error is that the D:\3rdParty\x86\msxml6\msxml6.msi cannot install, but the install continues. The install folder is now Program Files (x86) instead of the 64bit RealDWG install folder Program Files. I continue.
Everything installs and now I have a 64bit version in
C:\Program Files\Autodesk\RealDWG 2013
and a 32bit version in
C:\Program Files (x86)\Autodesk\RealDWG 2013
I went to my Environment path and added these paths
C:\Program Files (x86)\Autodesk\RealDWG 2013
C:\Program Files (x86)\Autodesk\RealDWG 2013\Fonts
C:\Program Files (x86)\Autodesk\RealDWG 2013\Support
I removed the 64bit AcDbMgd.dll reference and added
C:\Program Files (x86)\Autodesk\RealDWG 2013\AcDbMgd.dll
Now when I try to run I get the BadImageFormatException:
Could not load file or assembly Acdbmgd
Do I have to unistall 64bit before developing 32bit on my 64bit machine?
Is it a problem that 32bit is installing in the (x86) folder instead of the normal Program Files folder?
Do I have to create an entirely new project referencing the 32bit dll?
When I remove the 32bit Acdbmgd.dll reference, and add back in the 64bit Acdbmgd.dll reference, it runs fine.
I also tried to copy the 32bit install folder into a Program Files\Autodesk\RealDWG 2013 32bit folder, but I get the same error.
Thanks Fenton
Reply
06/05/2013 at 04:21 PM

---
**内容**: Eric Mills said...
I got it to work Fenton. I changed my project to debug mode from AnyCPU to x86 and now it runs fine.
Reply
06/05/2013 at 09:22 PM

---
**内容**: Fenton Webb said...
Hi Eric
personally, I don't install to Program Files because the user rights are restrictive. I always install to c:\Apis\ObjectDBX\2014
Also, I never add any %PATH% updates to my system where AutoCAD or RealDWG are concerned. It's very dangerous and can cause some serious DLL hell if you are running multiple versions. For development purposes, best thing to do is output your application DLLs/Exes straight to the RealDWG base folder, that quickly resolves any dependency issues.
Also, the findFile(), I like to make it search relative paths first before checking the system path.
Reply
06/06/2013 at 09:21 AM

---
