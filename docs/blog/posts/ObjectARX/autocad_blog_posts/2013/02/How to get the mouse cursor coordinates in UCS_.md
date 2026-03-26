---
title: "How to get the mouse cursor coordinates in UCS?"
date: 2013-02-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - DWG
  - Dimension
  - Plot
  - UCS
description: "The following code (essentially a windows message filter) obtains and prints the mouse coordinates in the UCS. The coordinates are the same as the ..."
author: Autodesk
---
# How to get the mouse cursor coordinates in UCS?

发布日期: 2013-02-01

原始链接: https://adndevblog.typepad.com/autocad/2013/02/how-to-get-the-mouse-cursor-coordinates-in-ucs.html

## 文章内容

By Gopinath Taget
The following code (essentially a windows message filter) obtains and prints the mouse coordinates in the UCS. The coordinates are the same as the coordinates displayed in AutoCAD's status bar.
BOOL filterMouse(MSG *pMsg)
{
 if( pMsg->message == WM_MOUSEMOVE )
{
  acedDwgPoint cpt;
  ads_point ptDCS, norm;
  AcGePoint3d  origin;
  AcGeVector3d e0, e1, e2;
  AcGeMatrix3d  matUcs2Wcs, matWcs2Ucs;
    // 1: Get the Mouse coords in DCS
  //
    CPoint cPnt (pMsg->lParam) ;
  acedCoordFromPixelToWorld (cPnt, cpt) ;
  ads_point_set ( cpt, ptDCS );
    // 2: Transform the DCS point to UCS isomatric view
  //
  ads_point result;
  struct resbuf fromrb, torb;
    fromrb.restype = RTSHORT;
  fromrb.resval.rint = 2; // DCS
      torb.restype = RTSHORT;
  torb.resval.rint = 1; // UCS 
      // disp == 0 indicates that pt is a point: 
  acedTrans(ptDCS, &fromrb, &torb, FALSE, result);
    // 3: Project the UCS point to the XY plan of UCS
  //
  struct resbuf rbview;
  ads_getvar( _T("viewdir"), &rbview );
  ads_point_set( rbview.resval.rpoint, norm );
      AcGePlane thePlane; // The default constructor creates XY plan.
    AcGePoint3d  pntInUCS( result[X], result[Y], result[Z] );
  AcGeVector3d vecViewdir( norm [X], norm [Y], norm [Z] );
  AcGePoint3d resPnt = pntInUCS.project (thePlane, vecViewdir);
    // 4: Print the result
  //
  ads_printf ( _T("\nMouse in Ucs-resPnt %f, %f, %f"), 
   resPnt[X],resPnt[Y], resPnt[Z] );
}
 else if( pMsg->message ==WM_LBUTTONDOWN)
{
  acedRemoveFilterWinMsg(filterMouse);
}
 return FALSE; // continue
}
You can register this filter with something like this:
acedRegisterFilterWinMsg(filterMouse)
And unregister it with this:
acedRemoveFilterWinMsg(filterMouse);

## 评论

**内容**: Tony Tanzillo said...
Is there something wrong with AcEdInputPointMonitor that would require a lower-level solution like this?
Reply
02/13/2013 at 07:27 PM

---
**内容**: Mehmet said...
How is it used in c#
Reply
03/06/2020 at 10:38 AM

---
