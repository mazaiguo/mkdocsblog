---
title: "Error with Visual LISP editor when debugging from .NET"
date: 2012-06-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoLISP
description: "When debugging from a .NET and running the VLIDE an error may occur. A work around is to change a registry setting. (MDA - Managed Debugging Assist..."
author: Autodesk
---
# Error with Visual LISP editor when debugging from .NET

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/error-with-visual-lisp-editor-when-debugging-from-net.html

## 文章内容

By Wayne Brill
When debugging from a .NET and running the VLIDE an error may occur. A work around is to change a registry setting. (MDA - Managed Debugging Assistants = 0). To set this registry key use a tool like regedit and set the string key "MDA" to 0.
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\.NETFramework  
If you do not find the MDA string key, create one and set its value to 0.
  You could also create a .reg file and set its contents as follows:
Windows Registry Editor Version 5.00
[HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\.NETFramework]
"MDA"="0"

## 评论

**内容**: Gaston Nunez said...
Hi,
It's a lot better disabling just the specific issue in the MDA than work without MDA at all. In the case of Vlisp, the main issue is LoaderLock, and we just need to disable that exception (Debug Menu->Exceptions->MDA->LoaderLock). Check this from MS: http://msdn.microsoft.com/en-us/library/d21c150d
Gaston Nunez
Reply
06/28/2012 at 02:46 PM

---
**内容**: Kerry Brown said...

I agree Gaston,
http://www.theswamp.org/index.php?topic=31448.msg369942#msg369942
Regards
kdub
Reply
06/29/2012 at 01:48 AM

---
