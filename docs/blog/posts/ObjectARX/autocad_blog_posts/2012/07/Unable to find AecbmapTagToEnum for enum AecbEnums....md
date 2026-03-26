---
title: "Unable to find AecbmapTagToEnum for enum AecbEnums..."
date: 2012-07-01
categories:
  - AutoCAD COM
tags:
  - AutoCAD
  - COM
  - DWG
description: "In several places, I found some people said that they got “Unable to find AecbmapTagToEnum for enum AecbEnums...” error when opening some dwg file ..."
author: Autodesk
---
# Unable to find AecbmapTagToEnum for enum AecbEnums...

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/unable-to-find-aecbmaptagtoenum-for-enum-aecbenums.html

## 文章内容

By Barbara Han
In several places, I found some people said that they got “Unable to find AecbmapTagToEnum for enum AecbEnums...” error when opening some dwg file and didn’t know how to resolve this problem, so I posted the answer here to help.
The AecbMapTagToEnum is probably defined by AutoCAD MEP. If the MEP Object Enablers are installed on your machine, and you call CoInitialize() at the beginning of the program considering the fact that MEP OEs need COM support, then this problem would be gone.
The latest version of RealDWG SDK have included almost all of Autodesk vertical OEs. If you are using older versions of RealDWG SDK and those OEs are not included in RealDWG SDK installation package, you can install those OEs manually. They are downloadable from:
http://usa.autodesk.com/adsk/servlet/index?siteID=123112&id=2753223&linkID=9240618
acdbModelerStart() should be called as well to prevent some other problems.
The following is a code sample that you can refer to:
// MEP drawings have issues without this
::CoInitialize(NULL);
acdbSetHostApplicationServices(&gDumpDwgHostApp);
long lcid = 0x00000409; // English
acdbValidateSetup(lcid);
// Could also be useful to call this, though things
// seem to work even without it
acdbModelerStart();

## 评论

**内容**: Sonic exe said...
I'm interested in learning more about this topic but don't know where to look. I'm hoping everyone can help me now that you initiated this conversation. quordle now.
Reply
04/10/2023 at 09:35 PM

---
