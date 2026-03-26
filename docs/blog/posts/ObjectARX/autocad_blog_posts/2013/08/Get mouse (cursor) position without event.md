---
title: "Get mouse (cursor) position without event"
date: 2013-08-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - DWG
  - Dimension
  - UCS
description: "AutoCAD API provides AcEdInputPointManager.Inputpointmonitor which can monitor any input of the user, including mouse. API also allows you to monit..."
author: Autodesk
---
# Get mouse (cursor) position without event

发布日期: 2013-08-01

原始链接: https://adndevblog.typepad.com/autocad/2013/08/get-mouse-cursor-position-without-event.html

## 文章内容

By Xiaodong Liang
AutoCAD API provides AcEdInputPointManager.Inputpointmonitor which can monitor any input of the user, including mouse. API also allows you to monitor Windows message. Sometimes you may just need to get the current mouse position without any event. The following is code demo. Actually, it just get the current cursor position and convert it to AutoCAD coordinate. It also takes UCS into consideration.
static void getMousePosition(void)
{     
    //get cursor position by Windows API
     POINT CursorPos;
     GetCursorPos(&CursorPos);
     acedGetAcadDwgView()->ScreenToClient(&CursorPos);
       //Returns the viewport number based on
     // Windows client coordinates.
     int vpNum = acedGetWinNum(CursorPos.x, CursorPos.y);
       //Converts coordinates from AutoCAD
     // drawing window
     //to current active viewport's coordinates 
     acedDwgPoint acPt, newPt;
     acedCoordFromPixelToWorld(vpNum,
                               CursorPos,
                               acPt);  
       double worldPoint[3];
     acedCoordFromPixelToWorld(vpNum,
                                CPoint(CursorPos.x,
                                CursorPos.y) ,
                                worldPoint);
     acutPrintf(
         L"\nModel Position (no UCS): [%f, %f, %f]\n",
                    worldPoint[0],
                    worldPoint[1],
                    worldPoint[2]);
         //Take UCS translation in consideration    
     AcGeMatrix3d mat;
     acedGetCurrentUCS(mat);
       AcGePoint3d ptUcs(worldPoint[0],
                     worldPoint[1],
                     worldPoint[2]);
     ptUcs.transformBy(mat.inverse());
       resbuf wcs;
     wcs.restype = RTSHORT;
     wcs.resval.rint = 0;
       resbuf dcs;
     dcs.restype = RTSHORT;
     dcs.resval.rint = 2;
       //translate the WCS coordinate to UCS
     double result[3];
     acedTrans(asDblArray(ptUcs),
                &wcs,
                &dcs,
                0,
                result);
     acutPrintf(
       L"\nModel Position (with UCS): [%f, %f, %f]\n",
         result[0], result[1], result[2]);
}

## 评论

**内容**: priya said...
Hi can anybody help me to Get mouse (cursor) position without event using COM API.
Reply
05/13/2016 at 03:24 AM

---
**内容**: JamesOneil said...
Bag essentials and all point of the order is firm for the advancement for the citizens. He joys of the B2B Tech Marketing Agency are implied for the field. The tip is argued for the top of the bag items or the true value for all positions for thk reform for the links for al buyers.
Reply
07/21/2023 at 05:14 AM

---
