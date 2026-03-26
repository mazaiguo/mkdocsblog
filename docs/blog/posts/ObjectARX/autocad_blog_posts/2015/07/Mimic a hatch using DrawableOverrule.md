---
title: "Mimic a hatch using DrawableOverrule"
date: 2015-07-01
categories:
  - AutoCAD
tags:
  - Hatch
description: "If you need an entity to appear hatched temporarily, drawable overrule can be used for this purpose. Drawing the hatch pattern from an WorldDraw / ..."
author: Autodesk
---
# Mimic a hatch using DrawableOverrule

发布日期: 2015-07-01

原始链接: https://adndevblog.typepad.com/autocad/2015/07/mimic-a-hatch-using-drawableoverrule.html

## 文章内容

By Balaji Ramamoorthy
If you need an entity to appear hatched temporarily, drawable overrule can be used for this purpose. Drawing the hatch pattern from an WorldDraw / ViewportDraw can be simple or a little complex depending on the pattern that you want to use. To let the hatch pattern correctly fill the boundary, a clip boundary can be created in your overrule. This simplifies the overrule implementation as the pattern can be created to cover the entity while the clip boundary takes care of clipping it to the actual entity bounds.
Here are two screenshots before and after clipping



Here is a sample code to hatch a circle with the cross pattern using DrawableOverrule
 public  class  HatchedCircleOverrule  
                 : DrawableOverrule
 {
     public  override  bool  IsApplicable(RXObject subject)
     {
         Circle circle = subject as  Circle;
           if  (circle.Database == null )
             return  false ;
           return  true ;
     }
       public  override  void  ViewportDraw
         (Drawable drawable, ViewportDraw vd)
     {
         base .ViewportDraw(drawable, vd);
           Circle circle = (Circle)drawable;
         Point3d cenPt = circle.Center;
           ClipBoundary cb = new  ClipBoundary();
         cb.DrawBoundary = false ;
         FrontAndBackClipping clipping 
             = vd.Viewport.FrontAndBackClipping;
         cb.ClippingBack = clipping.ClipBack;
         cb.ClippingFront = clipping.ClipFront;
         cb.NormalVector = vd.Viewport.ViewDirection;
         cb.BackClipZ = clipping.Back;
         cb.FrontClipZ = clipping.Front;
           Point2dCollection clipPts 
             = new  Point2dCollection();
           double  paramIncr = 
             (circle.EndParam - circle.StartParam) / 100;
         double  param = circle.StartParam;
         Plane pln = new  Plane(cenPt, circle.Normal);
         for  (int  cnt = 0; cnt < 100; cnt++)
         {
             clipPts.Add(
             circle.GetPointAtParameter(param).Convert2d(pln));
             param += paramIncr;
         }
         clipPts.Add(
         circle.GetPointAtParameter(circle.EndParam).Convert2d(pln));
         cb.SetAptPoints(clipPts);
         vd.Geometry.PushClipBoundary(cb);
           vd.SubEntityTraits.TrueColor 
             = new  EntityColor(0, 255, 0);
           Point3dCollection vertices 
             = new  Point3dCollection();
           int  divs = 8;
         double  delX = circle.Diameter / divs;
         double  delY = circle.Diameter / divs;
           for  (int  row = 0; row <= divs; row++)
         {
             Point3d currPt = 
                 cenPt 
                 - Vector3d.XAxis * circle.Radius 
                 - Vector3d.YAxis * circle.Radius 
                 + Vector3d.YAxis * row * delY;
               for  (int  col = 0; col <= divs; col++)
             {
                 vertices.Clear();
                 vertices.Add(
                     currPt + Vector3d.XAxis * delX * 0.25);
                 vertices.Add(
                     currPt - Vector3d.XAxis * delX * 0.25);
                 vd.Geometry.Polyline(
                     vertices, Vector3d.ZAxis, new  IntPtr (-1));
                   vertices.Clear();
                 vertices.Add(
                     currPt + Vector3d.YAxis * delY * 0.25);
                 vertices.Add(
                     currPt - Vector3d.YAxis * delY * 0.25);
                 vd.Geometry.Polyline(
                     vertices, Vector3d.ZAxis, new  IntPtr (-1));
                   currPt = currPt + Vector3d.XAxis * delX;
             }
         }
           vd.Geometry.PopClipBoundary();
     }
       public  override  bool  WorldDraw
         (Drawable drawable, WorldDraw wd)
     {
         base .WorldDraw(drawable, wd);
           // call viewportdraw 
         return  false ;
     }
 }
   public  class  Commands  : IExtensionApplication
 {
     private  static  HatchedCircleOverrule  _hco;
       void  IExtensionApplication.Initialize() { }
       void  IExtensionApplication.Terminate()
     {
         if  (_hco != null )
         {
             Overrule.RemoveOverrule
                 (RXClass.GetClass(typeof (Circle)), _hco);
             _hco.Dispose();
             _hco = null ;
         }
     }
       [CommandMethod("StartOR" )]
     public  void  StartORMethod()
     {
         Document doc 
             = Application .DocumentManager.MdiActiveDocument;
         if  (_hco == null )
         {
             _hco = new  HatchedCircleOverrule ();
             _hco.SetCustomFilter();
             Overrule.AddOverrule
                 (RXClass.GetClass(typeof (Circle)), 
                 _hco, true );
             Overrule.Overruling = true ;
         }
         doc.Editor.WriteMessage("\nOverruling started !" );
         doc.Editor.Regen();
     }
       [CommandMethod("StopOR" )]
     public  void  StopORMethod()
     {
         Document doc 
             = Application .DocumentManager.MdiActiveDocument;
           if  (_hco != null )
         {
             Overrule.RemoveOverrule(
                 RXClass.GetClass(typeof (Circle)), _hco);
             Overrule.Overruling = false ;
             _hco.Dispose();
             _hco = null ;
         }
         doc.Editor.WriteMessage("\nOverruling stopped !" );
         doc.Editor.Regen();
     }
 }

## 评论

**内容**: baiqilinux said...
what to do if i want wo clip the outside region?which i want to clip the partten within the circle and left the outside ones
Reply
12/04/2018 at 11:06 PM

---
**内容**: drift boss said...
I adore your sensitivity. This episode, I suppose, has strengthened my grip on the awful situation we’ve found ourselves in, and I’m convinced that it won’t worry me enough anymore that I’ve gained some different insights on it.
Reply
09/24/2022 at 08:45 PM

---
