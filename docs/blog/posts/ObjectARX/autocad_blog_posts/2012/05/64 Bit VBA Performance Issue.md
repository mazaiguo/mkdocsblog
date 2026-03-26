---
title: "64 Bit VBA Performance Issue"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - COM
  - COM Interop
  - VBA
description: "Here is a common question we get through ADN support:"
author: Autodesk
---
# 64 Bit VBA Performance Issue

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/64-bit-vba-performance-issue.html

## 文章内容

By Philippe Leefsma
Here is a common question we get through ADN support:
I ported our existing VBA extension for AutoCAD to Windows 7 64 bit. After installing the VBA enabler and changing the COM references to the new version, everything is now working. Unfortunately, performance is very bad, much slower as on my previous laptop (XP 32 bit, 4 years old).
Do you have any hints where to find the bottleneck?
I did not change anything in coding.
Solution
The fact that VBA runs slower on the 64 bit version of AutoCAD is a known issue. There is already a change request present against the reported behavior, request number 1147047 [AutoCAD has slowed in the 64-bit platforms when loaded VBA projects].
The main reason is that there is no x64 version of VBA. We ship the x32 VBA version in an out-of-process server with x64 AutoCAD. Therefore, a lot of marshaling is required going between the out-of-process VBA server and x64 AutoCAD. As a result, x64 VBA is slower than x86 VBA. As a solution or workaround I would suggest porting the VBA application to a .NET DLL.

## 评论

**内容**: Brad Hamilton said...
Is there any progress on this issue between Microsoft and Autodesk? We have many apps; 60;30;10%, vLISP, .NET & VBA. The few remaining VBA apps are rather substantial but as more of ours customers move to 64bit ac2011, we are getting lots of performance complaints.
Also, in vLISP, especially with extending functionality with typelibs, are these ActiveX components in the same boat?
Reply
11/07/2012 at 09:35 AM

---
**内容**: Madhukar Moogala said in reply to Brad Hamilton...
Hi Brad,
I'm sorry, but I can't talk about future AutoCAD versions. All I can say is that up to and including the current (AutoCAD 2013) release, we have continued to license VBA 6.3 from Microsoft. VBA 6.3 doesn't come in a 64-bit version, so the only way you can speed up your code in the current releases is to migrate to another API/language (e.g. Visual LISP or .NET using COM Interop) to allow your code to run in-process to AutoCAD. The cause of the slowdown is that the VBA engine has to run outside the AutoCAD process, because you can't load a 32-bit DLL into a 64-bit process. (You'll see the same kind of slowdown if you automate AutoCAD from another application using ActiveX on a 32-bit OS).
:-(
Reply
11/07/2012 at 04:49 PM

---
**内容**: Brad Hamilton said in reply to Madhukar Moogala...
Thanks Stephen,
Was the 32-bit OS reference in the last paragraph correct? If so, I'm more confused. If I use (vlax-get-or-create-object "Excel.Application") on a 64-bit machine using office Office 2007, will this exhibit the same performance degradation as having a VBA command do the export? Same question with (vlax-import-type-library...?
Additionally, as I mentioned in my first post, only a few of our remaining apps are VBA, yet the VBA enabler loads upfront. Will this cause a performance hit even if the user never launches one of the VBA apps? Is there a method that we're missing to "demand-load" the VBA enabler?
Reply
11/08/2012 at 09:20 AM

---
**内容**: Madhukar Moogala said in reply to Brad Hamilton...
Any ActiveX/COM call across process boundaries will exhibit the same performance hit. So calling from AutoCAD to Excel should be just as slow as calling AutoCAD from Excel. The reason any AutoCAD VBA macro on AutoCAD 64-bit is slower than on AutoCAD 32-bit is (as I said before) because the 32-bit VBA engine has to sit outside the AutoCAD 64-bit process, whereas it sits inside the AutoCAD 32-bit process and so doesn't have to marshal COM calls across process boundaries. Here's a short Microsoft reference about this - http://msdn.microsoft.com/en-us/library/aa242099(v=vs.60).aspx.
The demandload registry settings for the VBA IDE are located at HKEY_LOCAL_MACHINE\SOFTWARE\Autodesk\AutoCAD\R19.0\ACAD-B001:409\Applications\AcadVBA (or similar), but I'm not going to encourage you to edit the default AutoCAD demandload settings.
Reply
11/08/2012 at 09:45 AM

---
**内容**: Abidi said...
Hello,
I have a VBA code of 32 bit version on a windows 64 bit system. I am asked to transfer it to a windows 32 bit computer. Code runs fine but is extremely slow. The difference is not the excel version but the operating systems type. Older one is 64 bit OS and new one is 32 bit OS. What should I do to make it run faster?
Reply
08/27/2013 at 11:14 PM

---
**内容**: Philippe said...
Hi Abidi,
There is not much you can do to make the code run faster, except writing it in a smart way obviously... VBA code will run faster on 32-bit OS because it runs in process with AutoCAD, versus out-of-process for 64-bit. That's what this blog post is stating.
AutoCAD 2014 64-bit is coming with VBA7, which support in-process 64-bit, so this sure helps performances.
Reply
08/28/2013 at 07:15 AM

---
**内容**: aiyoung said...
When converting an old VBA application to VB.NET, how can one go about searching for code that inadvertently initializes the VBA system?
I've converted an old VAB app to VB.NET using the VBA to VB6 conversion tool, then using visual studio to get everything working with vb.net.
When i run the code, it hangs on one line that calls an old LISP script. AutoCAD invokes the VBA system and the whole application hangs for about 1-3 minutes before continuing.
Reply
02/20/2014 at 11:47 AM

---
**内容**: Madhukar Moogala said in reply to aiyoung...
Have you debugged your LISP script to see where the slowdown occurs? Does your LISP macro include any calls to vla* functions?
Reply
02/20/2014 at 03:18 PM

---
**内容**: CAD bloke said...
Here is a Lisp routine that unloads all the VBA apps so AutoCAD (x64, pre v2014) can resume full speed. You would need to set your VBA apps to demand-load so they will reload when you call them again. https://gist.github.com/CADbloke/b8b8632a954ee191f3d4
Reply
03/30/2015 at 04:43 PM

---
