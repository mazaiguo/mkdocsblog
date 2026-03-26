---
title: "Updating .NET dlls and ObjectARX applications of an OEM product"
date: 2013-04-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - C++
  - OEM
  - ObjectARX
description: "We have an OEM application which is using .NET dlls and ObjectARX applications. We would like to update these on the customer's computer without ha..."
author: Autodesk
---
# Updating .NET dlls and ObjectARX applications of an OEM product

发布日期: 2013-04-01

原始链接: https://adndevblog.typepad.com/autocad/2013/04/updating-net-dlls-and-objectarx-applications-of-an-oem-product.html

## 文章内容

By Adam Nagy
Issue
We have an OEM application which is using .NET dlls and ObjectARX applications. We would like to update these on the customer's computer without having to reinstall the product. Is it possible to do it?
Solution
Yes, it is possible. Just follow these steps:
Rebuild your .NET and ObjectARX applications
Rebind them using OEM Make Wizard, which will update the files in [AutoCAD OEM folder]\oem\[OEM Project folder]
Replace the existing .NET dlls and arx files in the install folder of your product on the customer's computer with the newly created ones residing in the above folder

## 评论

**内容**: Anthony Conte said...
Hello Adam,
As a follow up to my comment yesterday, I think I have answered my own question. The rebuilt assemblies must be the same version. After fixing my assembly version in assemblyinfo.cs, the new assemblies load into my updated OEM product.
Best Regards,
Anthony
Reply
04/29/2017 at 09:10 AM

---
**内容**: Anthony Conte said in reply to Anthony Conte...
I don't see my previous comment, but for anyone interested, my updated assemblies were not loading after being updated in my OEM product folder even after replacing every file with binary differences in the folder tree. It seems that assembly version is still registered somewhere and must remain the same.
Reply
04/29/2017 at 09:17 AM

---
