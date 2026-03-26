---
title: "Changing setup icon in AutoCAD OEM product installer"
date: 2015-04-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - OEM
description: "Here is a short blog post about a query from a developer on changing the setup icon for their AutoCAD OEM product."
author: Autodesk
---
# Changing setup icon in AutoCAD OEM product installer

发布日期: 2015-04-01

原始链接: https://adndevblog.typepad.com/autocad/2015/04/changing-setup-icon-in-autocad-oem-product-installer.html

## 文章内容

By Balaji Ramamoorthy
Here is a short blog post about a query from a developer on changing the setup icon for their AutoCAD OEM product.
In the OEM MakeWizard, the company name defaults to "Autodesk". If you leave it unchanged for your product, then the OEM InstallerWizard can automatically start using the "Autodesk" icon as its setup icon. This is regardless of the icon path provided in the OEM InstallerWizard for the setup icon. If you need your company icon to show up in your product installer, please remember to change the "Company name" and rebuild your product.

## 评论

**内容**: Patrick WEBER said...
Hello from France,
I have changed the company name in the OEM make wizard. I have changed IDR_MAINFRAME in the Change Icons screen, but nothing happened.
Reply
05/05/2015 at 03:25 AM

---
**内容**: Balaji said...
Hi Patrick,
This blog post is only relevant when you want change the setup icon which appears in your product installer. If you are trying to get an icon set for your product then you will need to follow the steps provided in the OEM developer's guide and change IDR_MAINFRAME. After you click on Browse button, select both your product exe and AcBrandRes.dll paths.
Regards,
Balaji
Reply
05/05/2015 at 03:31 AM

---
