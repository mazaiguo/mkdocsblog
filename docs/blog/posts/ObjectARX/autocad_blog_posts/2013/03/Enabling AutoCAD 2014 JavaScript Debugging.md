---
title: "Enabling AutoCAD 2014 JavaScript Debugging"
date: 2013-03-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - JavaScript
  - Unicode
description: "New in AutoCAD 2014 is the JavaScript API. Without going into too much detail here (this will be covered in much more detail elsewhere) this basica..."
author: Autodesk
---
# Enabling AutoCAD 2014 JavaScript Debugging

发布日期: 2013-03-01

原始链接: https://adndevblog.typepad.com/autocad/2013/03/enabling-autocad-2014-javascript-debugging.html

## 文章内容

by Fenton Webb
New in AutoCAD 2014 is the JavaScript API. Without going into too much detail here (this will be covered in much more detail elsewhere) this basically allows developers host their Apps via a URL rather than a download/install model – very cool.
If you have tried using the JavaScript API, I’m sure you have started to get frustrated about not being able to debug your code… Well, I have a debugging solution for you…
To enable debugging our JavaScript APIs we use the WebInspector application which is part of the WebKit Open Source. This is a web application written in JavaScript that allows the user to examine things like HTML tags, debug JavaScript code and perform profiling.
You can access these tools by turning on this registry entry…
[HKEY_LOCAL_MACHINE/SOFTWARE/Wow6432Node/Autodesk/WebInspector]
"DevToolsURL"=http://drawingfeed.visualtao.net/DevTools/inspector/devtools.html
Once enabled, you will see a new Right Click menu in the AcWebKit control context menu called “Developer Tools”…
Enjoy!

## 评论

**内容**: Jeremy Tammik said...
Hi Fenton,
That sounds rather Windows specific... do you have a suggestion for the Mac as well? Thank you!
Cheers, Jeremy.
Reply
03/29/2013 at 06:44 AM

---
**内容**: Jeremy Tammik said...
Hi Fenton,
You suggestion above seems rather Windows specific. What would you advise using on the Mac? Have you ever tested FireBug in the Firefox browser? That is available on Mac as well, I see. Thank you!
Cheers, Jeremy.
Reply
03/29/2013 at 07:03 AM

---
**内容**: Fenton Webb said...
Hey Jeremy!
there's no JavaScript API support on AutoCAD 2014 for the Mac just yet.
Reply
03/29/2013 at 08:26 AM

---
**内容**: Fenton Webb said...
Sorry, you can't use Firebug or similar. The reason is because the JavaScript API runs in-proc, which means that you need to be inside of AutoCAD to have access to it.
Reply
03/29/2013 at 08:28 AM

---
**内容**: Daniel Du said...
the URL is truncated due to the layout issue, it is:
https://import.autodeskbutterfly.com/DevTools/inspector/devtools.html
Reply
04/06/2013 at 08:53 PM

---
**内容**: Eddy said...
Had some problems to put it in my windows register...
Put this in a .reg file:
----------------
Windows Registry Editor Version 5.00
[HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Autodesk\WebInspector]
"DevToolsURL"="http://drawingfeed.visualtao.net/DevTools/inspector/devtools.html"
----------------
Reply
09/09/2015 at 11:23 PM

---
