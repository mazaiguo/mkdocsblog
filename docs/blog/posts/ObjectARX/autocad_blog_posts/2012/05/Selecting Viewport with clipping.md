---
title: "Selecting Viewport with clipping"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - Polyline
description: "I prompt the user to select a Viewport. This works fine, unless the Viewport has a clipping polyline in which case I get back the polyline instead ..."
author: Autodesk
---
# Selecting Viewport with clipping

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/selecting-viewport-with-clipping.html

## 文章内容

By Adam Nagy
I prompt the user to select a Viewport. This works fine, unless the Viewport has a clipping polyline in which case I get back the polyline instead of the Viewport. How could I get back the Viewport from the polyline?
ads_name ss;
ads_name eName;
ads_point pt;
if( RTNORM != acedEntSel(_T("\nPlease pick a viewport"), eName, pt ))
  return;
// eName might be a polyline even though the user selected a Viewport
Solution
You can get back the Viewport (if the selected entity is a clipping boundary of a viewport) using AcDbLayoutManager::getNonRectVPIdFromClipId():
AcDbObjectId polyId;
acdbGetObjectId(polyId, eName);
  AcDbLayoutManager *layoutMgr;
layoutMgr = acdbHostApplicationServices()->layoutManager();
  AcDbObjectId viewportId =
  layoutMgr->getNonRectVPIdFromClipId(polyId);
  if (viewportId.isNull())
{
  // not a viewport clipping polyline
}
You could also restrict the user to selecting Viewports only:
ads_name ss;
ads_name eName;
ads_point pt;
  // instead of...
// if( RTNORM != acedEntSel(
//   _T("\nPlease pick a viewport"), eName, pt ))
// return;
  resbuf filter;
filter.resval.rstring = _T("VIEWPORT");
filter.rbnext = NULL;
filter.restype = 0;
  ACHAR* texts[] = {_T("\nPlease pick a viewport"), _T("")};
  int ret = acedSSGet(_T("_-M:S:$"), texts, NULL, &filter, ss);
if (RTNORM != ret)
  return;
  acedSSName(ss, 0, eName);

