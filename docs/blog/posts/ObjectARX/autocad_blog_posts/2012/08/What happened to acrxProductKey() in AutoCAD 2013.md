---
title: "What happened to acrxProductKey() in AutoCAD 2013"
date: 2012-08-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - C++
  - Database
  - ObjectARX
description: "You may have noticed that the acrxProductKey() has disappeared in ObjectARX 2013. This is because of all the product refactoring that happened for ..."
author: Autodesk
---
# What happened to acrxProductKey() in AutoCAD 2013

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/what-happened-to-acrxproductkey-in-autocad-2013.html

## 文章内容

by Fenton Webb
You may have noticed that the acrxProductKey() has disappeared in ObjectARX 2013. This is because of all the product refactoring that happened for the Mac and the new accoreconsole.exe.
To obtain the same information that acrxProductKey() used to return, you should instead now use:
acdbHostApplicationServices()->getUserRegistryProductRootKey();
In .NET you can access the same property using
Autodesk.AutoCAD.DatabaseServices.HostApplicationServices.UserRegistryProductRootKey

## 评论

**内容**: Tony Tanzillo said...
Hi Fenton. Can you offer an explaination as to why acrxProductKey() was not retained in the interest of source code portability across releases?
Code portability between releases has become a major issue for many, include some who don't think the relative handful of MAC users justifies what is happening, and that could have something to do with Autodesk's recent financial performance, as customers (especially in Europe where customization is actually much more prevalent than it is here in the states) are really starting to get fed up with the seemingly-whimsical breaking changes, and just to be perfectly clear, let's not confused confuse 'binary compatibility' with source code portability.
Reply
08/27/2012 at 05:21 PM

---
**内容**: Jon Rizzo said...
#define acrxProductKey acdbHostApplicationServices()->getUserRegistryProductRootKey
Reply
08/28/2012 at 05:30 AM

---
**内容**: Fenton Webb said...
Hey Tony,
I understand your pain... .
Actually, the Mac port was a major milestone in AutoCAD's history. Whether you use the Mac or not, the fact still remains that the changes implemented for the Mac platform brought us the 'headless' AutoCAD (accoreconsole.exe). As a Windows AutoCAD programmer, this single change has opened the door for lots of awesome programming opportunities!
About the acrxProductKey() - because of major architectural changes to core AutoCAD, this function was substituted with the more aptly named host application services version.
Reply
08/28/2012 at 09:15 AM

---
**内容**: Owen Wengerd said in reply to Fenton Webb...
Fenton, they could have added a #define in migrtion.h so that existing code would migrate and compile without error.
Reply
08/28/2012 at 09:35 AM

---
**内容**: Fenton Webb said...
Hey Owen
you are right - we could have, however, acrxProductKey() is confusing...
Does it mean getUserRegistryProductRootKey()?
Or
does it mean getMachineRegistryProductRootKey()?
We always take binary breaks as an opportunity to try and make sure APIs still make sense.
Reply
08/28/2012 at 11:15 AM

---
**内容**: Jon Rizzo said...
Fenton,
I took these to be the same. Has this been split into two functions now? If so, existing code is actually broken and should be revisited...
Reply
08/28/2012 at 11:48 AM

---
**内容**: Kerry Brown said...
>>> You may have noticed that the acrxProductKey() has disappeared in ObjectARX 2013. <<<
Fenton,
Someone really needs to look at the ARX documentation.
acrxProductKey is still listed in both arxRef.chm and arxDev.chm
//------------
John,
from help AcDbHostApplicationServices::getMachineRegistryProductRootKey Method
[quote]Returns the registry root of the product in the HKEY_LOCAL_MACHINE hive. In case of AutoCAD, the string returned is the same as the one returned by getUserProductRegistryRootKey.[/quote]
Regards
Kerry
Reply
08/28/2012 at 10:05 PM

---
**内容**: Fenton Webb said...
Hey guys
if you find issues with the documentation, simply click the "Comments?" link at the bottom of the page, tell us the problem and it will be fixed.
Reply
08/29/2012 at 01:35 PM

---
