---
title: "AutoCAD OEM: Enabling Ortho in Z Direction"
date: 2019-03-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - OEM
description: "I have received a query from an OEM developer, in his Survey product Ortho snapping functionality doesn’t work in +Z/-Z direction."
author: Autodesk
---
# AutoCAD OEM: Enabling Ortho in Z Direction

发布日期: 2019-03-01

原始链接: https://adndevblog.typepad.com/autocad/2019/03/autocad-oem-enabling-ortho-in-z-direction.html

## 文章内容

By Madhukar Moogala

I have received a query from an OEM developer, in his Survey product Ortho snapping functionality doesn’t work in +Z/-Z direction.
Here is screen GIF.

AutoCAD, AutoCAD OEM, AutoCAD LT and TrueView are different manifestations of same code base, this has been singlehandedly maintained by our beloved Engineer Patti [Patricia Harris] for last 30 years if I’m not wrong, she recently passed away in tragic accident.

By design AutoCAD LT doesn’t enable Ortho in Z direction as LT is not for 3D designs.
But AutoCAD OEM has a setting that needs to be enabled to have this functionality work.

Tracking down the setting variable was an exhilarating experience, I would like to thank my esteem colleague Markus Kraus, one of the most talented programmer, I would call him second generation programmer after John Walker and his gang left.

So the what’s the secret setting that is hidden for AutoCAD LT, and TrueView but not for AutoCAD and AutoCAD OEM.

You need to enable ‘UCSDETECT’ command in your OEM Program .XML


<OemCmd>

<Name>ucsdetect</Name>

<Status>Full</Status>

</OemCmd>
After enabling the Command

## 评论

**内容**: Autocad 2D 3D Training in Dubai said...
Reach out to an Autocad 2D 3D Training in Dubai to help you prepare for your Autocad Certification with a variety of courses.
Reply
10/21/2019 at 05:56 AM

---
**内容**: Autocad 2D 3D Training in Dubai said...
Reach out to an Autocad 2D 3D Training in Dubai to help you prepare for your Autocad Certification with a variety of courses.
Reply
10/22/2019 at 03:51 AM

---
