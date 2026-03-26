---
title: "AutoCAD 2019 ObjectARX and .NET wizards"
date: 2018-04-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - C++
  - ObjectARX
description: "We have had many users asking for new versions of wizards that are Visual Studio 2017 compatible to work with AutoCAD 2019. Here they are  :"
author: Autodesk
---
# AutoCAD 2019 ObjectARX and .NET wizards

发布日期: 2018-04-01

原始链接: https://adndevblog.typepad.com/autocad/2018/04/autocad-2019-objectarx-and-net-wizards-.html

## 文章内容

By Deepak Nadig
We have had many users asking for new versions of wizards that are Visual Studio 2017 compatible to work with AutoCAD 2019. Here they are  : 
AutoCAD ObjectARX 2019 Wizard 
AutoCAD .NET 2019 Wizard
P.S:
We will soon have these wizards downloadable from the Tools section of https://www.autodesk.com/developer-network/platform-technologies/autocad

## 评论

**内容**: Alexander Rivilis said...
Hi Deepak!
You forgot disable compile option: Smaller type check in debug configuration.
Reply
04/16/2018 at 11:09 AM

---
**内容**: Alexander Rivilis said...
Other bug:
File: "C:\Program Files (x86)\Autodesk\ObjectARX 2019 Wizards\ArxWizMFCSupport\HTML\1033\default.htm"
In line 336 have to be changed CLASSID to "CLSID:fc1ae18b-0282-42f1-90ae-bbd8f0181013"
Reply
04/16/2018 at 01:03 PM

---
**内容**: Alexander Rivilis said...
File: "C:\Program Files (x86)\Autodesk\ObjectARX 2019 Wizards\ArxWizMFCSupport\HTML\1033\default.htm"
Line 11 have to be commented (or deleted). Otherwise dialog is wrong and impossible press Finish button.
Reply
04/16/2018 at 01:34 PM

---
**内容**: Madhukar Moogala said...
Hi Alexander,
I agree, we need update control Id for MFC, and also need to find the correct path of VCWizards.
Thank you ;)
Reply
04/17/2018 at 08:46 AM

---
**内容**: Alexander Rivilis said in reply to Madhukar Moogala...
Also ObjectARX Wizard 2019 do unusable ObjectARX Wizard 2017 and 2018. It is very bad news. I have to restore both ObjectARX Wizards manually :(
Reply
04/19/2018 at 01:49 AM

---
**内容**: Vladimir Panić said...
I cannot install AutoCAD .NET 2019 Wizard.
Please see:
https://forums.autodesk.com/t5/net/cannot-install-autocad-2019-net-wizard/td-p/7973359

Regards,
Vladimir
Reply
05/03/2018 at 08:26 AM

---
**内容**: Deepak A S Nadig said in reply to Vladimir Panić...
Hi Vladimir,
The .NET wizard is designed to support .NET framework 4.7 environment.
Kindly ensure this for installation.
Regards,
Deepak
Reply
05/03/2018 at 10:56 PM

---
**内容**: Vladimir Panić said in reply to Deepak A S Nadig...
Thank you Deepak,
I'm aware of that and NET framework 4.7 is installed.
It seems that error message is not relevant, there must be something else.
Regards,
Vladimir
Reply
05/03/2018 at 11:52 PM

---
**内容**: Vladimir Panić said...
I haven't found any solution yet.
https://forums.autodesk.com/t5/net/cannot-install-autocad-2019-net-wizard/m-p/7973359/highlight/false#M58836
Sorry, but I expected some help from ADN not only blow-off answer.
Regards,
Vladimir
Reply
05/09/2018 at 04:59 AM

---
**内容**: Vladimir Panić said...
Finally I installed the wizard, thanks to Markus Latz.
In case somebody has the same problem:
https://forums.autodesk.com/t5/installation-licensing/cannot-install-autocad-2019-net-wizard/td-p/7973359
Reply
05/11/2018 at 11:21 AM

---
**内容**: baiqilinux said...
arxcommmon.js failed,due to not have enough right. what's the problem?
Reply
12/01/2018 at 12:24 AM

---
**内容**: Tony said...
When I try to install AutoCAD .NET 2019 Wizard it says that .net framework 4.7 in not installed. So i download .net framework 4.7 and when I try to install that it says that it is present on my computer. When I check I can see it is not on my computer
Any idea what might be happening?
Tony
Reply
12/15/2018 at 05:18 PM

---
**内容**: frustrated said...
You always want people to upgrade to the latest software, I have Visual Studio 2019! where are the wizards for visual studio 2019??. or are you recommending that users always stay a few years back on any and every software/application.
Reply
08/29/2019 at 05:57 AM

---
**内容**: khanh said...
i am using vsto pro 2019,cad 2020,net 4.8 but i canot install this package
the msg display: vsto 2017 must present
what i have to do now
Reply
09/22/2019 at 04:31 AM

---
