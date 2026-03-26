---
title: "3DWalk through an AutoCAD Model"
date: 2014-02-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "Here is a sample code to demonstrate the navigation through an AutoCAD model. In this sample code, the camera and target positions follow the selec..."
author: Autodesk
---
# 3DWalk through an AutoCAD Model

发布日期: 2014-02-01

原始链接: https://adndevblog.typepad.com/autocad/2014/02/3dwalk-through-an-autocad-model.html

## 文章内容

By Balaji Ramamoorthy
Here is a sample code to demonstrate the navigation through an AutoCAD model. In this sample code, the camera and target positions follow the selected spline entity which defines the navigation path.
Here is a recording of the output :
  Here is the sample code :
[CommandMethod("MyWalk")]
public static void MyWalkMethod()
{
    Document doc
                = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      PromptEntityOptions peo2
                = new PromptEntityOptions("\nSelect a spline :");
    peo2.SetRejectMessage(
        "Please select a spline for defining the 3D walk path");
    peo2.AddAllowedClass(
        typeof(Autodesk.AutoCAD.DatabaseServices.Spline), false);
    PromptEntityResult per2 = ed.GetEntity(peo2);
    if (per2.Status != PromptStatus.OK)
        return;
    ObjectId splineId = per2.ObjectId;
      int steps = 3000;
      Point3d position = Point3d.Origin;
    Point3d target = Point3d.Origin;
      // Create and add our message filter to know if
    // escape is pressed during walk.
    MyMessageFilter filter = new MyMessageFilter();
    System.Windows.Forms.Application.AddMessageFilter(filter);
      ViewportTableRecord backupVTR = new ViewportTableRecord();
      const double DIAG35MM = 42.0;
    double lensLength = 50.0;
    double projectionPlaneDistance = 50.0;
    double sp = 0.0;
    double ep = 0.0;
    double aspectRatio = 1.0;
      using (Transaction tr = db.TransactionManager.StartTransaction())
    {
        ViewTable viewTable = tr.GetObject(
                                            db.ViewTableId,
                                            OpenMode.ForWrite
                                            ) as ViewTable;
          ViewportTable vpTbl = tr.GetObject(
                                            db.ViewportTableId,
                                            OpenMode.ForRead
                                            ) as ViewportTable;
          ViewportTableRecord viewportTableRec = tr.GetObject
                                    (
                                            vpTbl["*Active"],
                                            OpenMode.ForRead
                                    ) as ViewportTableRecord;
          backupVTR.CopyFrom(viewportTableRec);
        aspectRatio =
            (viewportTableRec.Width / viewportTableRec.Height);
          Spline spline = tr.GetObject(
                                        splineId,
                                        OpenMode.ForWrite
                                    ) as Spline;
        sp = spline.StartParam;
        ep = spline.EndParam;
        spline.Visible = false;
          tr.Commit();
    }
      using (Transaction tr
                    = db.TransactionManager.StartTransaction())
    {
        Spline spline = tr.GetObject(
                                        splineId,
                                        OpenMode.ForRead
                                    ) as Spline;
          double paramincr = (ep - sp) / steps;
          for (double param = sp; param <= ep; param += paramincr)
        {
            if (filter.bCanceled == true)
            {
                ed.WriteMessage("\nWalk cancelled.");
                break;
            }
              position = spline.GetPointAtParameter(param);
            Vector3d tangent = spline.GetFirstDerivative(param);
            target = position +
                    tangent.GetNormal() * projectionPlaneDistance;
              double fieldHeight =
                    (projectionPlaneDistance * DIAG35MM) /
                    (lensLength *
                    Math.Sqrt(1.0 + aspectRatio * aspectRatio));
              double fieldWidth = aspectRatio * fieldHeight;
              using (ViewTableRecord vtr = new ViewTableRecord())
            {
                vtr.BackClipEnabled = false;
                vtr.BackClipDistance = 0.0;
                vtr.CenterPoint = Point2d.Origin;
                vtr.FrontClipAtEye = false;
                vtr.FrontClipEnabled = true;
                vtr.FrontClipDistance = projectionPlaneDistance;
                vtr.LensLength = lensLength;
                vtr.PerspectiveEnabled = true;
                vtr.RenderMode
                    = ViewTableRecordRenderMode.GouraudShaded;
                vtr.Target = target;
                vtr.ViewTwist = 0.0;
                vtr.ViewDirection = position - target;
                vtr.Width = fieldWidth;
                vtr.Height = fieldHeight;
                  ed.SetCurrentView(vtr);
            }
              System.Threading.Thread.Sleep(10);
              // Check for user input events
            System.Windows.Forms.Application.DoEvents();
        }
          // Restore the view to what it was at start
        spline.UpgradeOpen();
        spline.Visible = true;
          ViewportTable vpTbl = tr.GetObject(
                                            db.ViewportTableId,
                                            OpenMode.ForRead
                                            ) as ViewportTable;
        ViewportTableRecord viewportTableRec = tr.GetObject(
                                            vpTbl["*Active"],
                                            OpenMode.ForWrite
                                    ) as ViewportTableRecord;
        viewportTableRec.UpgradeOpen();
        viewportTableRec.CopyFrom(backupVTR);
        ed.UpdateTiledViewportsFromDatabase();
          tr.Commit();
    }
      System.Windows.Forms.Application.RemoveMessageFilter(filter);
}
  public class MyMessageFilter : System.Windows.Forms.IMessageFilter
{
    public const int WM_KEYDOWN = 0x0100;
    public bool bCanceled = false;
      public bool PreFilterMessage(ref System.Windows.Forms.Message m)
    {
        if (m.Msg == WM_KEYDOWN)
        {
            // Check for the Escape keypress
            System.Windows.Forms.Keys kc
                = (System.Windows.Forms.Keys)
                (int)m.WParam & System.Windows.Forms.Keys.KeyCode;
            if (m.Msg == WM_KEYDOWN &&
                kc == System.Windows.Forms.Keys.Escape)
            {
                bCanceled = true;
            }
            // Return true to filter all keypresses
            return true;
        }
        // Return false to let other messages through
        return false;
    }
}
For the recording and testing of the sample code, I downloaded a nice sample drawing of a little house from here and made some minor changes to make it to more realistic. The modified sample drawing can be downloaded here : 
Download House.dwg
To try the sample code, build the sample code and netload in AutoCAD. Open the sample drawing and run "MyWalk" command. Select the yellow spline when prompted for the 3D walk path. During the walk, press escape key to stop the navigation if you need to stop it.

## 评论

**内容**: Erik said...
This is a nice suggestion. Could you increase the number of steps and decrease the sleep time in order to get a smoother animation?
Reply
02/20/2014 at 05:31 AM

---
**内容**: Balaji said in reply to Erik...
Hi Erik,
Thanks for your comment. I have updated the sample code and the recording. The animation is much smoother than what it was earlier.
Regards,
Balaji
Reply
02/20/2014 at 10:31 PM

---
**内容**: BJHuffine said...
Curious... now that RenderMode is gone, how would you handle that part?
Reply
03/18/2015 at 06:16 AM

---
**内容**: Balaji said...
Hi Jason,
In AutoCAD 2015, instead of the RenderMode, you can set vtr.VisualStyleId. But for the drawing that is attached to this post,
simply commenting out the vtr.RenderMode should also work ok.
Regards,
Balaji
Reply
03/18/2015 at 11:35 PM

---
