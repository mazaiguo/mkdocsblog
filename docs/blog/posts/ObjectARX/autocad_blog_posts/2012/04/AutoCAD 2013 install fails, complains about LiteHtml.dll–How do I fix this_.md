---
title: "AutoCAD 2013 install fails, complains about LiteHtml.dll–How do I fix this?"
date: 2012-04-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "This was a problem reported by an an ADN Developer. The solution was also provided by the ADN developer:"
author: Autodesk
---
# AutoCAD 2013 install fails, complains about LiteHtml.dll–How do I fix this?

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/autocad-2013-install-fails-complains-about-litehtmldllhow-do-i-fix-this.html

## 文章内容

By Gopinath Taget
This was a problem reported by an an ADN Developer. The solution was also provided by the ADN developer:
If system administrators implement the policy described by Microsoft in http://support.microsoft.com/kb/2264107 and set CWDIllegalInDllSearch to FFFFFFFF, the AutoCAD 2013 installer will fail being unable to load LiteHtml.dll
You need to detect the bad registry setting and warn people that they need to undo it.
The following .reg file causes the problem:
Windows Registry Editor Version 5.00
[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager]
"CWDIllegalInDllSearch"=dword:FFFFFFFF
This following .reg file fixes it:
Windows Registry Editor Version 5.00
[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager]
"CWDIllegalInDllSearch"=dword:00000000

## 评论

**内容**: ihsan said...
I had similar problem. The information about system:
Windows 8 x64 Enterprise Edition
AutoDesk 3ds Max 2012 x64
The error says that since the LiteHtml.dll cannot be located, the installation cannot start.
Solution:
I have right clicked to the setup.exe and troubleshoot compatilibity. I have selcted windows xp sp3.
It has installed successfully.
Reply
06/12/2013 at 01:03 AM

---
**内容**: matt said in reply to ihsan...
thanks man helped me alot
Reply
06/21/2013 at 09:50 AM

---
**内容**: arunalphonsetagec@gmail.com said in reply to ihsan...
it worked for me
Reply
07/12/2013 at 09:32 AM

---
**内容**: kboko said in reply to ihsan...
it worked for me too!
thanks man!
Reply
07/19/2013 at 12:38 PM

---
**内容**: La_Kula said in reply to ihsan...
Thanks man it worked, but i also made it to runn as both in compatibility and administrator. ;)
Reply
08/17/2013 at 06:05 AM

---
**内容**: sina said in reply to ihsan...
hey man love u so much,worked,thanks,thanks,thanks
Reply
04/18/2014 at 02:12 PM

---
**内容**: hiroliew said in reply to ihsan...
Thanks alot~ :)
Reply
08/31/2014 at 07:37 AM

---
**内容**: Saad said...
@ihsan: tnx buddy :)
Reply
06/20/2013 at 02:12 PM

---
**内容**: mohamed said...
i have the problem of { failed to load riched32.dll } when installing any of autodesk products
please some help to fix this problem
Reply
12/12/2014 at 09:47 AM

---
