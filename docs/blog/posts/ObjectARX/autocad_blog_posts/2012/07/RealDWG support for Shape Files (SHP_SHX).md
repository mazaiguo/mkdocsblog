---
title: "RealDWG support for Shape Files (SHP/SHX)"
date: 2012-07-01
categories:
  - AutoCAD
tags:
  - DWG
description: "Just to let all know, RealDWG does support Shape Files."
author: Autodesk
---
# RealDWG support for Shape Files (SHP/SHX)

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/realdwg-support-for-shape-files-shpshx.html

## 文章内容

by Fenton Webb
Just to let all know, RealDWG does support Shape Files.
By default, the RealDWG SDK comes with a Fonts folder that contains a standard set of compiled SHX files which you can deploy with your RealDWG app.
Just make sure that your HostApplicationServices::FindFile() knows to search where you have your SHX files deployed. That way, when the DWG file is read the SHX files will be resolved.

## 评论

**内容**: Alex Zelenov said...
Are there any ways to decrypt a SHX file using RealDWG? I am looking for glyph's geometry.
Thanks
Alex
Reply
06/30/2016 at 11:08 AM

---
