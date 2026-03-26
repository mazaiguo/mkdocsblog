---
title: "Some Tips on AutoCAD OEM"
date: 2013-04-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - OEM
  - ObjectARX
  - VBA
description: "Just some small for new users of AutoCAD OEM…"
author: Autodesk
---
# Some Tips on AutoCAD OEM

发布日期: 2013-04-01

原始链接: https://adndevblog.typepad.com/autocad/2013/04/some-tips-on-autocad-oem.html

## 文章内容

by Fenton Webb
Just some small for new users of AutoCAD OEM…
1) When you install OEM on your system, you install two things - the Toolkit (OemMakeWizard and OemInstallerWizard) and a runnable application called AutoCAD OEM.
2) AutoCAD OEM is a relaxed version of any OEM product you build with the OemMakeWizard. It is used to test OEM specific stuff you are doing, it allows NETLOAD, Appload and the VBAIDE (if VBA is installed)...
3) The modules you add to OEM are usually just your modules and direct dependencies – basically the ones that you load into normal AutoCAD, and the ones that your App relies on (excluding standard runtime modules).
4) DLLs that you include *must* be built with the OEM ObjectARX SDK because OEM modules are dependent on aoem.exe not acad.exe like in the normal ObejctARX SDK. If you try to load modules built with the normal ObjectARX SDK they will not load because they are being physically loaded into the wrong host exe.
5) When you rebuild your app DLLs, you must rebuild your OEM product in order to test them - basically, your application DLLs must be restamped and aligned with your OEM product.
6) In order for your application to load properly, you must have a unique Logical Name in Your Modules declaration page of the OemMakeWizard.

## 评论

**内容**: lalit said...
Hi
This Realy A nice article and tips and Tricks realy good
its help me lot in autocad training and learn Autocad
its really a nice nice software for architectural designing
Reply
05/02/2013 at 04:36 AM

---
**内容**: Lalit Autocad Training said...
Hi
This Realy A nice article and tips and Tricks realy good
its help me lot in autocad training and learn Autocad
its really a nice nice software for architectural designing
Reply
05/02/2013 at 04:37 AM

---
**内容**: Patrick WEBER said...
Hello,
Is there a tip to add registry keys that my application needs to work properly when building with OEMMakeWizard or when I create the installation program with the OEMInstallerWizard.
Thank you.
Reply
07/25/2013 at 11:45 PM

---
**内容**: Fenton Webb said...
Hey Patrick
simply create an MSM merge module with your settings in and then apply the MSM to the master MSI once you have built your installer using the OemInstallerWizard
Reply
07/26/2013 at 10:08 AM

---
**内容**: Patrick WEBER said in reply to Fenton Webb...
Thank you.
Reply
07/29/2013 at 11:43 PM

---
**内容**: Craig said...
Good info.
Also, the OEM wizard does not like spaces in the .Net DLL names. Keep them short and without spaces.
Plus, don't give the .Net DLL the same name as the logical product name.
Reply
03/06/2014 at 02:39 AM

---
**内容**: Autocad Training said...
Woww..Awesome Tips found on Autocad.Thanks to Fenton Webb and Craig for sharing your awesome knowledge.
Reply
07/17/2015 at 03:35 AM

---
