---
title: "Getting point coordinates in UCS from MessageFilter"
date: 2014-11-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Dimension
  - UCS
description: "Here is a code snippet to convert the mouse coordinates retreived from the Windows message in a message filter to an AutoCAD point coordinate in UCS."
author: Autodesk
---
# Getting point coordinates in UCS from MessageFilter

发布日期: 2014-11-01

原始链接: https://adndevblog.typepad.com/autocad/2014/11/getting-point-coordinates-in-ucs-from-messagefilter.html

## 文章内容

By Balaji Ramamoorthy
Here is a code snippet to convert the mouse coordinates retreived from the Windows message in a message filter to an AutoCAD point coordinate in UCS.
 class  MyMessageFilter  : System.Windows.Forms.IMessageFilter 
 {
     private  const  int  WM_LBUTTONDBLCLK = 0x203;
       bool  System.Windows.Forms.IMessageFilter .PreFilterMessage
                         (ref  System.Windows.Forms.Message  m)
     {
         if  (m.Msg == WM_LBUTTONDBLCLK)
         {
             Document doc = 
                Application .DocumentManager.MdiActiveDocument;
             Editor ed = doc.Editor;
               // Double clicked point coordinates in pixels 
             int  x = m.LParam.ToInt32() & 0xffff;
             int  y = (m.LParam.ToInt32() >> 16);
             System.Drawing.Point  p = new  Point (x, y);
               // Pixel to device independent coordinates 
             System.Windows.Point p1 = new  System.Windows.Point();
                           System.Windows.Vector s = 
             Autodesk.AutoCAD.Windows.Window.GetDeviceIndependentScale
             (IntPtr .Zero);
               p1.X = (int )(p.X / s.X);
             p1.Y = (int )(p.Y / s.Y);
               // Device independent coordinates to WCS 
             short  vpNum = 
                 (short )Application .GetSystemVariable("CVPORT" );
             Point3d bp = ed.PointToWorld(p1, vpNum);
               // WCS to UCS 
             bp = bp.TransformBy(
                         ed.CurrentUserCoordinateSystem.Inverse());
               ed.WriteMessage(String .Format("\\n{0} {1}" , bp.X, bp.Y));
         }
         return  false ;
     }
 }
  Please note that there could be slight variation from the coordinates displayed by AutoCAD in its status bar. This is a similar behavior when using "acedCoordFromPixelToWorld" to do such conversion. As AutoCAD uses some internal functions that may be different from what is exposed in the API, so the reply from our engineering to a similar query in the past, was that whatever approach we use, we may never be able to retrieve the exact same values as that of what is displayed in the status bar of AutoCAD UI.

