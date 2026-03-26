---
title: "AutoCAD 2023 Developer Update"
date: 2022-04-01
categories:
  - AutoLISP
tags:
  - API
  - AutoCAD
  - AutoLISP
  - CUI
description: "This year we have released many good features, for key features refer https://www.autodesk.com/products/autocad/features"
author: Autodesk
---
# AutoCAD 2023 Developer Update

发布日期: 2022-04-01

原始链接: https://adndevblog.typepad.com/autocad/2022/04/autocad-2023-developer-update.html

## 文章内容

This year we have released many good features, for key features refer https://www.autodesk.com/products/autocad/features
Important attraction on API side for this release is AutoCAD LISP API for AutoCAD web app.
This API is exclusively for AutoCAD subscribers. Whether you are on the go, at a job site, or anywhere else, create your own customizations to automate sequences with LISP in the AutoCAD web app.  (Video: 55 sec.)
Some known limitations of Lisp API on web –
- Any functionality that relies on a platform-specific technology (i.e., Visual Lisp and DCL).
- Any functionality that is not supported in AutoCAD Web (AutoCAD Web does not support everything desktop does - 3d editing for example).
- Any functionality that would violate browsers sandboxing rules (such as reading and writing to your local filesystem without going through normal browser restrictions.
System Requirements for AutoCAD 2023
https://knowledge.autodesk.com/support/autocad/learn-explore/caas/sfdcarticles/sfdcarticles/System-requirements-for-AutoCAD-2023-including-Specialized-Toolsets.html
AutoCAD 2023 API Help, covering all API offering, .NET, C++ etc.
https://help.autodesk.com/view/OARX/2023/ENU/
AutoCAD 2023 ObjectARX SDK
https://www.autodesk.com/developer-network/platform-technologies/autocad/objectarx-download
AutoCAD 2023 OMF SDK
Is exclusively available to A D N subscriber through https://adn.autodesk.io/ portal
AutoCAD ObjectARX Wizard for VS 2019
https://github.com/ADN-DevTech/ObjectARX-Wizards/blob/ForAutoCAD2023/ObjectARXWizardsInstaller/ObjectARXWizards-2023.zip
AutoCAD .NET Wizard for VS 2019
https://github.com/ADN-DevTech/AutoCAD-Net-Wizards/blob/ForAutoCAD2023/AutoCADNetWizardsInstaller/AutoCAD_2023_dotnet_wizards.zip
Important Note - AutoCAD 2023 is binary forward compatibility release, ObjectARX application developed in previous versions up to AutoCAD 2021 are compatible with AutoCAD 2023.
Visual Studio 2019 for use with AutoCAD - 2019/2020/2021/2022/2023
With Visual Studio 2019, MSVC v140 (VS 2015.3) and MSVC v141 (VS 2017) Toolsets are available.
Refer- https://knowledge.autodesk.com/community/screencast/f6bdf229-2ea2-4051-ad38-7a82e651800d

## 评论

**内容**: Kerry Brown said...
Madhukar Moogala, Hi
I've been using Visual Studio 2022 for developing .NET addins using AutoCAD 2023.
I'm wondering about the availability of the AutoCAD 2023 API Help import for VS2022 . . I see that it's currently only available for VS2019.
I imagine there will be quite a few people looking for the VS2022 .Net Wizard also :)
Regards,
Kerry Brown
Reply
04/19/2022 at 05:11 PM

---
**内容**: Madhukar Moogala said in reply to Kerry Brown...
I have messaged the author abouut the api import wizard tool for VS2022. I will keep you posted.
Reply
04/19/2022 at 11:04 PM

---
**内容**: Lee Ambrosius said in reply to Kerry Brown...
Hello Kerry,
I did some initial testing with the Integrated ObjectARX 2023 Help installer for VS2019 and it should work with VS2022 as well. The only thing that I noticed at the moment is that you will need to update your VS2022 installer to include the Help Viewer which can be found on the Individual Components tab. Once installed, you should be able to run the Integrated ObjectARX 2023 Help installer as it is only looking for the installed location of MS Help Viewer 2.3 in order to merge the help files into the correct Content Store.
Let me know if this works for you or not. Further testing will need to be done before making any official release of the installer.
Sincerely,
Lee
Reply
04/20/2022 at 09:57 AM

---
**内容**: Kerry Brown said...
Thanks
Reply
04/20/2022 at 12:35 AM

---
**内容**: fnf mod said...
You will need to update your VS2022 installation to include the Help Viewer, which is located on the Individual Components menu, as that is the only problem I have seen so far. Once MS Help Viewer 2.3 is installed, you should be able to execute the Integrated ObjectARX 2023 Help installer because it just needs to find that directory in order to merge the help files into the appropriate Content Store.
Reply
10/03/2022 at 02:55 AM

---
**内容**: Keyur Khalasi said...
Hello Madhukar Sir,
Hi, I am Keyur Khalasi RuleBuddy PlanAssist Developer from Softtech Team Pune,
I had one question for your.
As My Visual Studio 2019 ENterprise is Updated to 16.11.19 and i had made my .arx and .dll file using this for making Our AutoCAD OEM 2021 setup of RuleBuddy PlanAssist. But its give me the error like
rulebuddy2021.arx is incompatible with this version of PlanAssist Software. So please help me out on this.

Development environment: Microsoft® Visual Studio® 2019 version 16.11.19 (with C++ option installed) and .NET 4.8
Autocad oem 2021 make wizard version 5.0 product release version 24.0.47.0

Regards,
Keyur Khalasi.
Reply
10/10/2022 at 01:56 AM

---
**内容**: happy wheels said...
That is really thorough and simple for us to grasp. Thanks
Reply
02/13/2023 at 08:04 PM

---
**内容**: SeanReagle said...
Cursory street is fit for the entanglement for the citizens. The situation of the Selling property without an agent
is good and firm or the steps. The mark displaced for the joys. New models fit for the injunction for the citizens.
Reply
03/13/2023 at 08:30 AM

---
**内容**: vilas jadhav said...
Hi,
How can I install objectArx .NET sdk with visual studio community version.
I am not able to install any version of Object Arx wizard with visual studio 2019 or 2022 community version. But installed Autodesk Inventor 2024 add-in wizard with visual studio 2022 community version.
Please guide me to work.
thanks
vilas Jadhav
Reply
05/18/2023 at 01:28 AM

---
**内容**: slope said...
I must express my sincere admiration for the exceptional quality of the article in question. The author's skillful command of language and masterful organization of ideas create a truly impressive and thought-provoking piece.
Reply
08/03/2023 at 12:58 AM

---
**内容**: immaculate grid said...
AutoCAD LISP API for AutoCAD web app: Create custom automations using LISP routines, even while on the go or using the web app!
Reply
01/28/2024 at 06:13 PM

---
**内容**: Sandra Rabins said...
My expertise is in AutoCAD and reading the related posts of AutoCAD improves my knowledge. And you have told absolutely right about the new update. And now I'm talking about fashion in this season, this Yellowstone Beth Dutton Poncho Coat is your favorite.
Reply
02/15/2024 at 10:16 PM

---
**内容**: fnf said...
I am really impressed with your article. The information you share will be an important document for me to learn more about this topic.
Reply
02/29/2024 at 12:38 AM

---
