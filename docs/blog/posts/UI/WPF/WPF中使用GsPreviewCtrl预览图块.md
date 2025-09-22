---
title: WPF中使用GsPreviewCtrl预览图块
date: 2024-09-18
categories:
  - windows程序
tags:
  - WPF
  - GsPreviewCtrl
  - CAD预览
  - 图块显示
description: 在WPF中使用GsPreviewCtrl控件预览CAD图块的完整实现方法
author: JerryMa
---


# WPF中使用GsPreviewCtrl预览图块

## winform控件处理

`GsPreviewCtrl.cs`

```csharp
using System;
using System.IO;
using System.Diagnostics;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Data;
using System.Text;
using System.Windows.Forms;
using AcadApp = ZwSoft.ZwCAD.ApplicationServices.Application;
using ZwSoft.ZwCAD.ApplicationServices;
using ZwSoft.ZwCAD.DatabaseServices;
using ZwSoft.ZwCAD.Windows;
using ZwSoft.ZwCAD.EditorInput;
using ZwSoft.ZwCAD.Runtime;
using ZwSoft.ZwCAD.Geometry;
using ZwSoft.ZwCAD.GraphicsSystem;
namespace BlockView.NET
{
    public class GsPreviewCtrl : Control
    {
        public GsPreviewCtrl()
        {
        }



        // current dwg
        public Database mCurrentDwg = null;
        // Gs specific
        public ZwSoft.ZwCAD.GraphicsSystem.Manager mpManager = null;
        public ZwSoft.ZwCAD.GraphicsSystem.Device mpDevice = null;
        public ZwSoft.ZwCAD.GraphicsSystem.Model mpModel = null;
        public ZwSoft.ZwCAD.GraphicsSystem.View mpView = null;
        public bool mZooming = false;
        public bool mMouseDown = false;
        public bool mMouseMoving = false;
        public bool mbPanning = false;
        public bool mbOrbiting = false;
        public System.Drawing.Point mStartPoint;
        public System.Drawing.Point mEndPoint;

        public static bool IsDesignMode
        {
            get
            {
                return Utils.IsDesignMode(null);
            }
        }

        protected override void Dispose(bool disposing)
        {
            if (disposing)
            {
                // clear up the GS view gadgets
                if (!IsDesignMode)
                    ClearAll();
                if (mCurrentDwg != null)
                {
                    mCurrentDwg.Dispose();
                    mCurrentDwg = null;
                }
            }
            base.Dispose(disposing);

        }

        // called from InitDrawingControl, does GsPreviewCtrl specific initialization
        public void Init(Document doc, Database db)
        {
            mCurrentDwg = db;
            // check to see if the manager is already initalised
            if (null == mpManager)
            {
                // if not let's set it up
                mpManager = doc.GraphicsManager;
                // here's some test code to show the GS Events working
                mpManager.ViewToBeDestroyed += new ViewToBeDestroyedEventHandler(GSUtil.mpManager_ViewToBeDestroyed);
                mpManager.ViewWasCreated += new ViewWasCreatedEventHandler(GSUtil.mpManager_ViewWasCreated);
                mpManager.GsToBeUnloaded += new GsToBeUnloadedEventHandler(GSUtil.mpManager_GsToBeUnloaded);
                mpManager.ConfigWasModified += new ConfigWasModifiedEventHandler(GSUtil.mpManager_ConfigWasModified);

                KernelDescriptor descriptor = new KernelDescriptor();
                descriptor.addRequirement(ZwSoft.ZwCAD.UniqueString.Intern("3D Drawing"));
                GraphicsKernel kernal = Manager.AcquireGraphicsKernel(descriptor);
                // now create the Gs control, create the autocad device passing the handle to the Windows panel
                mpDevice = mpManager.CreateZWCADDevice(kernal, this.Handle);
                // resize the device to the panel size
                mpDevice.OnSize(this.Size);
                // now create a new gs view
                mpView = new ZwSoft.ZwCAD.GraphicsSystem.View();
                // and create the model
                mpModel = mpManager.CreateZWCADModel(kernal);

                // add the view to the device
                mpDevice.Add(mpView);
            }

            SetViewTo(mpView, mCurrentDwg);
            using (Transaction tr = mCurrentDwg.TransactionManager.StartTransaction())
            {
                BlockTableRecord curSpace = tr.GetObject(mCurrentDwg.CurrentSpaceId, OpenMode.ForRead, true) as BlockTableRecord;
                // 在这里进行你的操作
                mpView.Add(curSpace, mpModel);
                tr.Commit();
            }

            refreshView();
        }


        public void ClearAll()
        {
            if (!IsDesignMode)
            {
                if (!(mpDevice is null))
                {
                    bool b = mpDevice.Erase(mpView);
                }
                if (!(mpView is null))
                {
                    mpView.EraseAll();
                    mpView.Dispose();
                    mpView = null;
                }
                if (!(mpManager is null))
                {
                    if (!(mpModel is null))
                    {
                        mpModel.Dispose();
                        mpModel = null;
                    }

                    if (!(mpDevice is null))
                    {
                        mpDevice.Dispose();
                        mpDevice = null;
                    }
                    mpManager = null;
                }
            }
        }

        // [TT]: Refactored to exclude AutoCAD types from methods that run in the designer:

        public void ErasePreview()
        {
            if (!IsDesignMode)
                InternalErasePreview();
        }

        public void InternalErasePreview()
        {
            if (mpView != null)
                mpView.EraseAll();
            if (mpManager != null && mpModel != null)
            {
                mpModel.Dispose();
                mpModel = null;
            }
        }

        private void RubberRectangle(Point p1, Point p2)
        {
            Rectangle rc = new Rectangle();

            // Convert the points to screen coordinates.
            p1 = PointToScreen(p1);
            p2 = PointToScreen(p2);
            // Normalize the rectangle.
            if (p1.X < p2.X)
            {
                rc.X = p1.X;
                rc.Width = p2.X - p1.X;
            }
            else
            {
                rc.X = p2.X;
                rc.Width = p1.X - p2.X;
            }
            if (p1.Y < p2.Y)
            {
                rc.Y = p1.Y;
                rc.Height = p2.Y - p1.Y;
            }
            else
            {
                rc.Y = p2.Y;
                rc.Height = p1.Y - p2.Y;
            }
            // Draw the reversible frame.
            ControlPaint.DrawReversibleFrame(rc, Color.White, FrameStyle.Dashed);
        }

        // [TT]: Refactored to exclude AutoCAD types from methods that run in the designer:

        public void refreshView()
        {
            if (!IsDesignMode)
            {
                InternalRefreshView();
            }
        }

        // This method will never be jit'ed in the designer:

        void InternalRefreshView()
        {
            if (mpView != null)
            {
                mpView.Invalidate();
                mpView.Update();
            }
        }

        protected override void OnPaint(System.Windows.Forms.PaintEventArgs e)
        {
            base.OnPaint(e);
            refreshView();
        }

        // [TT]: Refactored to exclude AutoCAD types from methods that run in the designer:

        protected override void OnMouseMove(System.Windows.Forms.MouseEventArgs e)
        {
            base.OnMouseMove(e);
            if (!IsDesignMode)
            {
                InternalOnMouseMove(e);
            }
        }

        private void InternalOnMouseMove(System.Windows.Forms.MouseEventArgs e)
        {
            if (mpView != null)
            {
                if (mZooming)
                {
                    // if left button is down
                    if (mMouseDown)
                    {
                        if (mMouseMoving)
                        {
                            // erase the old rectangle
                            RubberRectangle(mStartPoint, mEndPoint);
                        }
                        // draw the new rectangle
                        RubberRectangle(mStartPoint, e.Location);
                        mMouseMoving = true;
                        // save the new point for next time
                        mEndPoint = e.Location;
                    }
                }
                else
                {
                    if (mbPanning)
                    {
                        //transform the point from device coordinates to
                        //world coordinates
                        Vector3d pan_vec = new Vector3d(-(e.Location.X - mStartPoint.X), e.Location.Y - mStartPoint.Y, 0);
                        /*pan_vec = */
                        pan_vec.TransformBy(mpView.ViewingMatrix * mpView.WorldToDeviceMatrix.Inverse());
                        mpView.Dolly(pan_vec);
                        refreshView();
                        mStartPoint = e.Location;
                    }
                    if (mbOrbiting)
                    {
                        double Half_Pi = 1.570796326795;

                        System.Drawing.Rectangle view_rect = new System.Drawing.Rectangle((int)mpView.ViewportExtents.MinPoint.X, (int)mpView.ViewportExtents.MinPoint.Y,
                                                                               (int)(mpView.ViewportExtents.MaxPoint.X - mpView.ViewportExtents.MinPoint.X),
                                                                               (int)(mpView.ViewportExtents.MaxPoint.Y - mpView.ViewportExtents.MinPoint.Y));

                        int nViewportX = (view_rect.Right - view_rect.Left) + 1;
                        int nViewportY = (view_rect.Bottom - view_rect.Top) + 1;

                        int centerX = (int)(nViewportX / 2.0f + view_rect.Left);
                        int centerY = (int)(nViewportY / 2.0f + view_rect.Top);

                        double radius = System.Math.Min(nViewportX, nViewportY) * 0.4f;

                        // compute two vectors from last and new cursor positions:

                        Vector3d last_vector = new Vector3d((mStartPoint.X - centerX) / radius,
                             -(mStartPoint.Y - centerY) / radius,
                             0.0);
                        if (last_vector.LengthSqrd > 1.0)     // outside the radius
                        {
                            double x = last_vector.X / last_vector.Length;
                            double y = last_vector.Y / last_vector.Length;
                            double z = last_vector.Z / last_vector.Length;
                            last_vector = new Vector3d(x, y, z);

                        }
                        else
                        {
                            double x = last_vector.X;
                            double y = last_vector.Y;
                            double z = System.Math.Sqrt(1.0 - last_vector.X * last_vector.X - last_vector.Y * last_vector.Y);
                            last_vector = new Vector3d(x, y, z);
                        }

                        Vector3d new_vector = new Vector3d((e.Location.X - centerX) / radius, -(e.Location.Y - centerY) / radius, 0.0);

                        if (new_vector.LengthSqrd > 1.0)     // outside the radius
                        {
                            double x = new_vector.X / new_vector.Length;
                            double y = new_vector.Y / new_vector.Length;
                            double z = new_vector.Z / new_vector.Length;
                            new_vector = new Vector3d(x, y, z);

                        }
                        else
                        {
                            double x = new_vector.X;
                            double y = new_vector.Y;
                            double z = System.Math.Sqrt(1.0 - new_vector.X * new_vector.X - new_vector.Y * new_vector.Y);
                            new_vector = new Vector3d(x, y, z);
                        }

                        // determine angles for proper sequence of camera manipulations:

                        Vector3d rotation_vector = last_vector;
                        rotation_vector = rotation_vector.CrossProduct(new_vector);  // rotation_vector = last_vector x new_vector

                        Vector3d work_vector = rotation_vector;
                        work_vector = new Vector3d(work_vector.X, work_vector.Y, 0.0f);                      // projection of rotation_vector onto xy plane

                        double roll_angle = System.Math.Atan2(work_vector.X,
                             work_vector.Y);        // assuming that the camera's up vector is "up",
                                                    // this computes the angle between the up vector 
                                                    // and the work vector, which is the roll required
                                                    // to make the up vector coincident with the rotation_vector
                        double length = rotation_vector.Length;
                        double orbit_y_angle = (length != 0.0) ? System.Math.Acos(rotation_vector.Z / length) + Half_Pi : Half_Pi;                   // represents inverse cosine of the dot product of the
                        if (length > 1.0f)                                              // rotation_vector and the up_vector divided by the
                            length = 1.0f;                                              // magnitude of both vectors.  We add pi/2 because we 
                                                                                        // are making the up-vector parallel to the the rotation
                        double rotation_angle = System.Math.Asin(length);                // vector ... up-vector is perpin. to the eye-vector.

                        // perform view manipulations

                        mpView.Roll(roll_angle);               // 1: roll camera to make up vector coincident with rotation vector
                        mpView.Orbit(0.0f, orbit_y_angle);     // 2: orbit along y to make up vector parallel with rotation vector
                        mpView.Orbit(rotation_angle, 0.0f);     // 3: orbit along x by rotation angle
                        mpView.Orbit(0.0f, -orbit_y_angle);     // 4: orbit along y by the negation of 2
                        mpView.Roll(-roll_angle);               // 5: roll camera by the negation of 1
                        refreshView();
                        mStartPoint = e.Location;
                    }
                }
            }
        }
        public void SetViewTo(ZwSoft.ZwCAD.GraphicsSystem.View view, Database db)
        {
            // just check we have valid extents
            if (db.Extmax.X < db.Extmin.X || db.Extmax.Y < db.Extmin.Y || db.Extmax.Z < db.Extmax.Z)
            {
                db.Extmin = new Point3d(0, 0, 0);
                db.Extmax = new Point3d(400, 400, 400);
            }
            // get the dwg extents
            Point3d extMax = db.Extmax;
            Point3d extMin = db.Extmin;
            // now the active viewport info
            double height = 0.0, width = 0.0, viewTwist = 0.0;
            Point3d targetView = new Point3d();
            Vector3d viewDir = new Vector3d();
            GSUtil.GetActiveViewPortInfo(ref height, ref width, ref targetView, ref viewDir, ref viewTwist, true);
            // from the data returned let's work out the viewmatrix
            viewDir = viewDir.GetNormal();
            Vector3d viewXDir = viewDir.GetPerpendicularVector().GetNormal();
            viewXDir = viewXDir.RotateBy(viewTwist, -viewDir);
            Vector3d viewYDir = viewDir.CrossProduct(viewXDir);
            Point3d boxCenter = extMin + 0.5 * (extMax - extMin);
            Matrix3d viewMat;
            viewMat = Matrix3d.AlignCoordinateSystem(boxCenter, Vector3d.XAxis, Vector3d.YAxis, Vector3d.ZAxis,
              boxCenter, viewXDir, viewYDir, viewDir).Inverse();
            Extents3d wcsExtents = new Extents3d(extMin, extMax);
            Extents3d viewExtents = wcsExtents;
            viewExtents.TransformBy(viewMat);
            double xMax = System.Math.Abs(viewExtents.MaxPoint.X - viewExtents.MinPoint.X);
            double yMax = System.Math.Abs(viewExtents.MaxPoint.Y - viewExtents.MinPoint.Y);
            Point3d eye = boxCenter + viewDir;
            // finally set the Gs view to the dwg view
            view.SetView(eye, boxCenter, viewYDir, xMax, yMax);

            // now update
            refreshView();
        }

        // [TT]: Refactored to exclude AutoCAD types from methods that run in the designer:
        protected override void OnMouseDown(System.Windows.Forms.MouseEventArgs e)
        {
            base.OnMouseDown(e);
            if (!IsDesignMode)
            {
                InternalOnMouseDown(e);
            }
        }

        private void InternalOnMouseDown(System.Windows.Forms.MouseEventArgs e)
        {
            if (mpView != null)
            {
                if (e.Button == System.Windows.Forms.MouseButtons.Left)
                {
                    // if zooming
                    if (mZooming)
                    {
                        mMouseDown = true;
                        mMouseMoving = false;
                    }
                    else
                    {
                        mbOrbiting = true;
                        this.Focus();
                    }

                }
                else if (e.Button == System.Windows.Forms.MouseButtons.Middle)
                {
                    mbPanning = true;
                }
                mStartPoint = e.Location;
            }
        }

        // [TT]: Refactored to exclude AutoCAD types from methods that run in the designer:
        protected override void OnMouseUp(System.Windows.Forms.MouseEventArgs e)
        {
            base.OnMouseUp(e);
            if (!IsDesignMode)
            {
                InternalOnMouseUp(e);
            }
        }

        private void InternalOnMouseUp(System.Windows.Forms.MouseEventArgs e)
        {
            if (mpView != null)
            {
                if (e.Button == System.Windows.Forms.MouseButtons.Left)
                {
                    if (mZooming && mMouseDown)
                    {
                        // end zoom
                        mZooming = false;
                        mMouseDown = false;
                        mMouseMoving = false;


                        mpView.ZoomWindow(new Point2d(mStartPoint.X, this.Bottom - mStartPoint.Y), new Point2d(mEndPoint.X, this.Bottom - mEndPoint.Y));

                        refreshView();
                    }
                    else
                    {
                        mbOrbiting = false;
                    }
                }
                else if (e.Button == System.Windows.Forms.MouseButtons.Middle)
                {
                    mbPanning = false;
                }
            }
        }

        // [TT]: Refactored to exclude AutoCAD types from methods that run in the designer:
        protected override void OnSizeChanged(EventArgs e)
        {
            base.OnSizeChanged(e);

            /// No AutoCAD types can be in this method, so we've
            /// moved the following code to another method which
            /// appears below, and only call that method when not 
            /// running in the designer:

            //if( mpDevice != null )
            //{
            //   mpDevice.OnSize( this.Size );
            //}

            if (!IsDesignMode)
            {
                InternalOnSizeChanged();
            }
        }

        // This method will never be jit'ed in the designer
        void InternalOnSizeChanged()
        {
            if (!(mpDevice is null))
            {
                mpDevice.OnSize(this.Size);
            }
        }
    }

    /// <summary>
    /// [TT]: Depreciated (using ControlPaint.DrawReversibleFrame() instead)
    /// </summary>

    public class GSUtil
    {
        public const String strActive = "*Active";
        public const String strActiveSettings = "ACAD_RENDER_ACTIVE_SETTINGS";
        public static void CustomUpdate(System.IntPtr parmeter, int left, int right, int bottom, int top)
        {
            MessageBox.Show("Left:" + left + "Right" + right + "Bottom" + bottom + "Top" + top);
        }
        public static System.Drawing.Color[] MyAcadColorPs =
    {
      System.Drawing.Color.FromArgb(255, 0, 0, 255),    //----- 0 - lets make it red for an example
      //{255, 255, 255, 255},//----- 0 - ByBlock - White
      System.Drawing.Color.FromArgb(255, 0, 0, 255),    //----- 1 - Red 
      System.Drawing.Color.FromArgb(255, 255, 0, 255),    //----- 2 - Yellow
      System.Drawing.Color.FromArgb(0, 255, 0, 255),    //----- 3 - Green
      System.Drawing.Color.FromArgb(0, 255, 255, 255),    //----- 4 - Cyan
      System.Drawing.Color.FromArgb(0, 0, 255, 255),    //----- 5 - Blue
      System.Drawing.Color.FromArgb(255, 0, 255, 255),    //----- 6 - Magenta
      System.Drawing.Color.FromArgb(255, 0, 0, 255),    //----- 7 - More red Red 
      System.Drawing.Color.FromArgb(255, 0, 0, 255),    //----- 8 - More red Red 
      System.Drawing.Color.FromArgb(255, 0, 0, 255),    //----- 9 - More red Red 
      /*System.Drawing.Color.FromArgb(255, 255, 255, 255),//----- 7 - White
      System.Drawing.Color.FromArgb(255, 255, 255, 255),//----- 8
      System.Drawing.Color.FromArgb(255, 255, 255, 255),//----- 9*/
      System.Drawing.Color.FromArgb(255, 0, 0, 255),    //----- 10
      System.Drawing.Color.FromArgb(255, 127, 127, 255),//----- 11
      System.Drawing.Color.FromArgb(165, 0, 0, 255),    //----- 12
      System.Drawing.Color.FromArgb(165, 82, 82, 255),    //----- 13
      System.Drawing.Color.FromArgb(127, 0, 0, 255),    //----- 14
      System.Drawing.Color.FromArgb(127, 63, 63, 255),    //----- 15
      System.Drawing.Color.FromArgb(76, 0, 0, 255),        //----- 16
      System.Drawing.Color.FromArgb(76, 38, 38, 255),    //----- 17
      System.Drawing.Color.FromArgb(38, 0, 0, 255),        //----- 18
      System.Drawing.Color.FromArgb(38, 19, 19, 255),    //----- 19
      System.Drawing.Color.FromArgb(255, 63, 0, 255),    //----- 20
      System.Drawing.Color.FromArgb(255, 159, 127, 255),//----- 21
      System.Drawing.Color.FromArgb(165, 41, 0, 255),    //----- 22
      System.Drawing.Color.FromArgb(165, 103, 82, 255),    //----- 23
      System.Drawing.Color.FromArgb(127, 31, 0, 255),    //----- 24
      System.Drawing.Color.FromArgb(127, 79, 63, 255),    //----- 25
      System.Drawing.Color.FromArgb(76, 19, 0, 255),    //----- 26
      System.Drawing.Color.FromArgb(76, 47, 38, 255),    //----- 27
      System.Drawing.Color.FromArgb(38, 9, 0, 255),        //----- 28
      System.Drawing.Color.FromArgb(38, 23, 19, 255),    //----- 29
      System.Drawing.Color.FromArgb(255, 127, 0, 255),    //----- 30
      System.Drawing.Color.FromArgb(255, 191, 127, 255),//----- 31
      System.Drawing.Color.FromArgb(165, 82, 0, 255),    //----- 32
      System.Drawing.Color.FromArgb(165, 124, 82, 255),    //----- 33
      System.Drawing.Color.FromArgb(127, 63, 0, 255),    //----- 34
      System.Drawing.Color.FromArgb(127, 95, 63, 255),    //----- 35
      System.Drawing.Color.FromArgb(76, 38, 0, 255),    //----- 36
      System.Drawing.Color.FromArgb(76, 57, 38, 255),    //----- 37
      System.Drawing.Color.FromArgb(38, 19, 0, 255),    //----- 38
      System.Drawing.Color.FromArgb(38, 28, 19, 255),    //----- 39
      System.Drawing.Color.FromArgb(255, 191, 0, 255),    //----- 40
      System.Drawing.Color.FromArgb(255, 223, 127, 255),//----- 41
      System.Drawing.Color.FromArgb(165, 124, 0, 255),    //----- 42
      System.Drawing.Color.FromArgb(165, 145, 82, 255),    //----- 43
      System.Drawing.Color.FromArgb(127, 95, 0, 255),    //----- 44
      System.Drawing.Color.FromArgb(127, 111, 63, 255),    //----- 45
      System.Drawing.Color.FromArgb(76, 57, 0, 255),    //----- 46
      System.Drawing.Color.FromArgb(76, 66, 38, 255),    //----- 47
      System.Drawing.Color.FromArgb(38, 28, 0, 255),    //----- 48
      System.Drawing.Color.FromArgb(38, 33, 19, 255),    //----- 49
      System.Drawing.Color.FromArgb(255, 255, 0, 255),    //----- 50
      System.Drawing.Color.FromArgb(255, 255, 127, 255),//----- 51
      System.Drawing.Color.FromArgb(165, 165, 0, 255),    //----- 52
      System.Drawing.Color.FromArgb(165, 165, 82, 255),    //----- 53
      System.Drawing.Color.FromArgb(127, 127, 0, 255),    //----- 54
      System.Drawing.Color.FromArgb(127, 127, 63, 255),    //----- 55
      System.Drawing.Color.FromArgb(76, 76, 0, 255),    //----- 56
      System.Drawing.Color.FromArgb(76, 76, 38, 255),    //----- 57
      System.Drawing.Color.FromArgb(38, 38, 0, 255),    //----- 58
      System.Drawing.Color.FromArgb(38, 38, 19, 255),    //----- 59
      System.Drawing.Color.FromArgb(191, 255, 0, 255),    //----- 60
      System.Drawing.Color.FromArgb(223, 255, 127, 255),//----- 61
      System.Drawing.Color.FromArgb(124, 165, 0, 255),    //----- 62
      System.Drawing.Color.FromArgb(145, 165, 82, 255),    //----- 63
      System.Drawing.Color.FromArgb(95, 127, 0, 255),    //----- 64
      System.Drawing.Color.FromArgb(111, 127, 63, 255),    //----- 65
      System.Drawing.Color.FromArgb(57, 76, 0, 255),    //----- 66
      System.Drawing.Color.FromArgb(66, 76, 38, 255),    //----- 67
      System.Drawing.Color.FromArgb(28, 38, 0, 255),    //----- 68
      System.Drawing.Color.FromArgb(33, 38, 19, 255),    //----- 69
      System.Drawing.Color.FromArgb(127, 255, 0, 255),    //----- 70
      System.Drawing.Color.FromArgb(191, 255, 127, 255),//----- 71
      System.Drawing.Color.FromArgb(82, 165, 0, 255),    //----- 72
      System.Drawing.Color.FromArgb(124, 165, 82, 255),    //----- 73
      System.Drawing.Color.FromArgb(63, 127, 0, 255),    //----- 74
      System.Drawing.Color.FromArgb(95, 127, 63, 255),    //----- 75
      System.Drawing.Color.FromArgb(38, 76, 0, 255),    //----- 76
      System.Drawing.Color.FromArgb(57, 76, 38, 255),    //----- 77
      System.Drawing.Color.FromArgb(19, 38, 0, 255),    //----- 78
      System.Drawing.Color.FromArgb(28, 38, 19, 255),    //----- 79
      System.Drawing.Color.FromArgb(63, 255, 0, 255),    //----- 80
      System.Drawing.Color.FromArgb(159, 255, 127, 255),//----- 81
      System.Drawing.Color.FromArgb(41, 165, 0, 255),    //----- 82
      System.Drawing.Color.FromArgb(103, 165, 82, 255),    //----- 83
      System.Drawing.Color.FromArgb(31, 127, 0, 255),    //----- 84
      System.Drawing.Color.FromArgb(79, 127, 63, 255),    //----- 85
      System.Drawing.Color.FromArgb(19, 76, 0, 255),    //----- 86
      System.Drawing.Color.FromArgb(47, 76, 38, 255),    //----- 87
      System.Drawing.Color.FromArgb(9, 38, 0, 255),        //----- 88
      System.Drawing.Color.FromArgb(23, 38, 19, 255),    //----- 89
      System.Drawing.Color.FromArgb(0, 255, 0, 255),    //----- 90
      System.Drawing.Color.FromArgb(127, 255, 127, 255),//----- 91
      System.Drawing.Color.FromArgb(0, 165, 0, 255),    //----- 92
      System.Drawing.Color.FromArgb(82, 165, 82, 255),    //----- 93
      System.Drawing.Color.FromArgb(0, 127, 0, 255),    //----- 94
      System.Drawing.Color.FromArgb(63, 127, 63, 255),    //----- 95
      System.Drawing.Color.FromArgb(0, 76, 0, 255),        //----- 96
      System.Drawing.Color.FromArgb(38, 76, 38, 255),    //----- 97
      System.Drawing.Color.FromArgb(0, 38, 0, 255),        //----- 98
      System.Drawing.Color.FromArgb(19, 38, 19, 255),    //----- 99
      System.Drawing.Color.FromArgb(0, 255, 63, 255),    //----- 100
      System.Drawing.Color.FromArgb(127, 255, 159, 255),//----- 101
      System.Drawing.Color.FromArgb(0, 165, 41, 255),    //----- 102
      System.Drawing.Color.FromArgb(82, 165, 103, 255),    //----- 103
      System.Drawing.Color.FromArgb(0, 127, 31, 255),    //----- 104
      System.Drawing.Color.FromArgb(63, 127, 79, 255),    //----- 105
      System.Drawing.Color.FromArgb(0, 76, 19, 255),    //----- 106
      System.Drawing.Color.FromArgb(38, 76, 47, 255),    //----- 107
      System.Drawing.Color.FromArgb(0, 38, 9, 255),        //----- 108
      System.Drawing.Color.FromArgb(19, 38, 23, 255),    //----- 109
      System.Drawing.Color.FromArgb(0, 255, 127, 255),    //----- 110
      System.Drawing.Color.FromArgb(127, 255, 191, 255),//----- 111
      System.Drawing.Color.FromArgb(0, 165, 82, 255),    //----- 112
      System.Drawing.Color.FromArgb(82, 165, 124, 255),    //----- 113
      System.Drawing.Color.FromArgb(0, 127, 63, 255),    //----- 114
      System.Drawing.Color.FromArgb(63, 127, 95, 255),    //----- 115
      System.Drawing.Color.FromArgb(0, 76, 38, 255),    //----- 116
      System.Drawing.Color.FromArgb(38, 76, 57, 255),    //----- 117
      System.Drawing.Color.FromArgb(0, 38, 19, 255),    //----- 118
      System.Drawing.Color.FromArgb(19, 38, 28, 255),    //----- 119
      System.Drawing.Color.FromArgb(0, 255, 191, 255),    //----- 120
      System.Drawing.Color.FromArgb(127, 255, 223, 255),//----- 121
      System.Drawing.Color.FromArgb(0, 165, 124, 255),    //----- 122
      System.Drawing.Color.FromArgb(82, 165, 145, 255),    //----- 123
      System.Drawing.Color.FromArgb(0, 127, 95, 255),    //----- 124
      System.Drawing.Color.FromArgb(63, 127, 111, 255),    //----- 125
      System.Drawing.Color.FromArgb(0, 76, 57, 255),    //----- 126
      System.Drawing.Color.FromArgb(38, 76, 66, 255),    //----- 127
      System.Drawing.Color.FromArgb(0, 38, 28, 255),    //----- 128
      System.Drawing.Color.FromArgb(19, 38, 33, 255),    //----- 129
      System.Drawing.Color.FromArgb(0, 255, 255, 255),    //----- 130
      System.Drawing.Color.FromArgb(127, 255, 255, 255),//----- 131
      System.Drawing.Color.FromArgb(0, 165, 165, 255),    //----- 132
      System.Drawing.Color.FromArgb(82, 165, 165, 255),    //----- 133
      System.Drawing.Color.FromArgb(0, 127, 127, 255),    //----- 134
      System.Drawing.Color.FromArgb(63, 127, 127, 255),    //----- 135
      System.Drawing.Color.FromArgb(0, 76, 76, 255),    //----- 136
      System.Drawing.Color.FromArgb(38, 76, 76, 255),    //----- 137
      System.Drawing.Color.FromArgb(0, 38, 38, 255),    //----- 138
      System.Drawing.Color.FromArgb(19, 38, 38, 255),    //----- 139
      System.Drawing.Color.FromArgb(0, 191, 255, 255),    //----- 140
      System.Drawing.Color.FromArgb(127, 223, 255, 255),//----- 141
      System.Drawing.Color.FromArgb(0, 124, 165, 255),    //----- 142
      System.Drawing.Color.FromArgb(82, 145, 165, 255),    //----- 143
      System.Drawing.Color.FromArgb(0, 95, 127, 255),    //----- 144
      System.Drawing.Color.FromArgb(63, 111, 127, 255),    //----- 145
      System.Drawing.Color.FromArgb(0, 57, 76, 255),    //----- 146
      System.Drawing.Color.FromArgb(38, 66, 76, 255),    //----- 147
      System.Drawing.Color.FromArgb(0, 28, 38, 255),    //----- 148
      System.Drawing.Color.FromArgb(19, 33, 38, 255),    //----- 149
      System.Drawing.Color.FromArgb(0, 127, 255, 255),    //----- 150
      System.Drawing.Color.FromArgb(127, 191, 255, 255),//----- 151
      System.Drawing.Color.FromArgb(0, 82, 165, 255),    //----- 152
      System.Drawing.Color.FromArgb(82, 124, 165, 255),    //----- 153
      System.Drawing.Color.FromArgb(0, 63, 127, 255),    //----- 154
      System.Drawing.Color.FromArgb(63, 95, 127, 255),    //----- 155
      System.Drawing.Color.FromArgb(0, 38, 76, 255),    //----- 156
      System.Drawing.Color.FromArgb(38, 57, 76, 255),    //----- 157
      System.Drawing.Color.FromArgb(0, 19, 38, 255),    //----- 158
      System.Drawing.Color.FromArgb(19, 28, 38, 255),    //----- 159
      System.Drawing.Color.FromArgb(0, 63, 255, 255),    //----- 160
      System.Drawing.Color.FromArgb(127, 159, 255, 255),//----- 161
      System.Drawing.Color.FromArgb(0, 41, 165, 255),    //----- 162
      System.Drawing.Color.FromArgb(82, 103, 165, 255),    //----- 163
      System.Drawing.Color.FromArgb(0, 31, 127, 255),    //----- 164
      System.Drawing.Color.FromArgb(63, 79, 127, 255),    //----- 165
      System.Drawing.Color.FromArgb(0, 19, 76, 255),    //----- 166
      System.Drawing.Color.FromArgb(38, 47, 76, 255),    //----- 167
      System.Drawing.Color.FromArgb(0, 9, 38, 255),        //----- 168
      System.Drawing.Color.FromArgb(19, 23, 38, 255),    //----- 169
      System.Drawing.Color.FromArgb(0, 0, 255, 255),    //----- 170
      System.Drawing.Color.FromArgb(127, 127, 255, 255),//----- 171
      System.Drawing.Color.FromArgb(0, 0, 165, 255),    //----- 172
      System.Drawing.Color.FromArgb(82, 82, 165, 255),    //----- 173
      System.Drawing.Color.FromArgb(0, 0, 127, 255),    //----- 174
      System.Drawing.Color.FromArgb(63, 63, 127, 255),    //----- 175
      System.Drawing.Color.FromArgb(0, 0, 76, 255),        //----- 176
      System.Drawing.Color.FromArgb(38, 38, 76, 255),    //----- 177
      System.Drawing.Color.FromArgb(0, 0, 38, 255),        //----- 178
      System.Drawing.Color.FromArgb(19, 19, 38, 255),    //----- 179
      System.Drawing.Color.FromArgb(63, 0, 255, 255),    //----- 180
      System.Drawing.Color.FromArgb(159, 127, 255, 255),//----- 181
      System.Drawing.Color.FromArgb(41, 0, 165, 255),    //----- 182
      System.Drawing.Color.FromArgb(103, 82, 165, 255),    //----- 183
      System.Drawing.Color.FromArgb(31, 0, 127, 255),    //----- 184
      System.Drawing.Color.FromArgb(79, 63, 127, 255),    //----- 185
      System.Drawing.Color.FromArgb(19, 0, 76, 255),    //----- 186
      System.Drawing.Color.FromArgb(47, 38, 76, 255),    //----- 187
      System.Drawing.Color.FromArgb(9, 0, 38, 255),        //----- 188
      System.Drawing.Color.FromArgb(23, 19, 38, 255),    //----- 189
      System.Drawing.Color.FromArgb(127, 0, 255, 255),    //----- 190
      System.Drawing.Color.FromArgb(191, 127, 255, 255),//----- 191
      System.Drawing.Color.FromArgb(82, 0, 165, 255),    //----- 192
      System.Drawing.Color.FromArgb(124, 82, 165, 255),    //----- 193
      System.Drawing.Color.FromArgb(63, 0, 127, 255),    //----- 194
      System.Drawing.Color.FromArgb(95, 63, 127, 255),    //----- 195
      System.Drawing.Color.FromArgb(38, 0, 76, 255),    //----- 196
      System.Drawing.Color.FromArgb(57, 38, 76, 255),    //----- 197
      System.Drawing.Color.FromArgb(19, 0, 38, 255),    //----- 198
      System.Drawing.Color.FromArgb(28, 19, 38, 255),    //----- 199
      System.Drawing.Color.FromArgb(191, 0, 255, 255),    //----- 200
      System.Drawing.Color.FromArgb(223, 127, 255, 255),//----- 201
      System.Drawing.Color.FromArgb(124, 0, 165, 255),    //----- 202
      System.Drawing.Color.FromArgb(145, 82, 165, 255),    //----- 203
      System.Drawing.Color.FromArgb(95, 0, 127, 255),    //----- 204
      System.Drawing.Color.FromArgb(111, 63, 127, 255),    //----- 205
      System.Drawing.Color.FromArgb(57, 0, 76, 255),    //----- 206
      System.Drawing.Color.FromArgb(66, 38, 76, 255),    //----- 207
      System.Drawing.Color.FromArgb(28, 0, 38, 255),    //----- 208
      System.Drawing.Color.FromArgb(33, 19, 38, 255),    //----- 209
      System.Drawing.Color.FromArgb(255, 0, 255, 255),    //----- 210
      System.Drawing.Color.FromArgb(255, 127, 255, 255),//----- 211
      System.Drawing.Color.FromArgb(165, 0, 165, 255),    //----- 212
      System.Drawing.Color.FromArgb(165, 82, 165, 255),    //----- 213
      System.Drawing.Color.FromArgb(127, 0, 127, 255),    //----- 214
      System.Drawing.Color.FromArgb(127, 63, 127, 255),    //----- 215
      System.Drawing.Color.FromArgb(76, 0, 76, 255),    //----- 216
      System.Drawing.Color.FromArgb(76, 38, 76, 255),    //----- 217
      System.Drawing.Color.FromArgb(38, 0, 38, 255),    //----- 218
      System.Drawing.Color.FromArgb(38, 19, 38, 255),    //----- 219
      System.Drawing.Color.FromArgb(255, 0, 191, 255),    //----- 220
      System.Drawing.Color.FromArgb(255, 127, 223, 255),//----- 221
      System.Drawing.Color.FromArgb(165, 0, 124, 255),    //----- 222
      System.Drawing.Color.FromArgb(165, 82, 145, 255),    //----- 223
      System.Drawing.Color.FromArgb(127, 0, 95, 255),    //----- 224
      System.Drawing.Color.FromArgb(127, 63, 111, 255),    //----- 225
      System.Drawing.Color.FromArgb(76, 0, 57, 255),    //----- 226
      System.Drawing.Color.FromArgb(76, 38, 66, 255),    //----- 227
      System.Drawing.Color.FromArgb(38, 0, 28, 255),    //----- 228
      System.Drawing.Color.FromArgb(38, 19, 33, 255),    //----- 229
      System.Drawing.Color.FromArgb(255, 0, 127, 255),    //----- 230
      System.Drawing.Color.FromArgb(255, 127, 191, 255),//----- 231
      System.Drawing.Color.FromArgb(165, 0, 82, 255),    //----- 232
      System.Drawing.Color.FromArgb(165, 82, 124, 255),    //----- 233
      System.Drawing.Color.FromArgb(127, 0, 63, 255),    //----- 234
      System.Drawing.Color.FromArgb(127, 63, 95, 255),    //----- 235
      System.Drawing.Color.FromArgb(76, 0, 38, 255),    //----- 236
      System.Drawing.Color.FromArgb(76, 38, 57, 255),    //----- 237
      System.Drawing.Color.FromArgb(38, 0, 19, 255),    //----- 238
      System.Drawing.Color.FromArgb(38, 19, 28, 255),    //----- 239
      System.Drawing.Color.FromArgb(255, 0, 63, 255),    //----- 240
      System.Drawing.Color.FromArgb(255, 127, 159, 255),//----- 241
      System.Drawing.Color.FromArgb(165, 0, 41, 255),    //----- 242
      System.Drawing.Color.FromArgb(165, 82, 103, 255),    //----- 243
      System.Drawing.Color.FromArgb(127, 0, 31, 255),    //----- 244
      System.Drawing.Color.FromArgb(127, 63, 79, 255),    //----- 245
      System.Drawing.Color.FromArgb(76, 0, 19, 255),    //----- 246
      System.Drawing.Color.FromArgb(76, 38, 47, 255),    //----- 247
      System.Drawing.Color.FromArgb(38, 0, 9, 255),        //----- 248
      System.Drawing.Color.FromArgb(38, 19, 23, 255),    //----- 249
      System.Drawing.Color.FromArgb(84, 84, 84, 255),    //----- 250
      System.Drawing.Color.FromArgb(118, 118, 118, 255),//----- 251
      System.Drawing.Color.FromArgb(152, 152, 152, 255),//----- 252
      System.Drawing.Color.FromArgb(186, 186, 186, 255),//----- 253
      System.Drawing.Color.FromArgb(220, 220, 220, 255),//----- 254
      System.Drawing.Color.FromArgb(255, 255, 255, 255),//----- 255
    };

        //////////////////////////////////////////////////////////////////////////////
        // standard autocad colours
        public static System.Drawing.Color[] MyAcadColorMs =
    {
      System.Drawing.Color.FromArgb(255, 255, 255, 255),//----- 0 - ByBlock - White
      System.Drawing.Color.FromArgb(255, 0, 0, 255),    //----- 1 - Red 
      System.Drawing.Color.FromArgb(255, 255, 0, 255),    //----- 2 - Yellow
      System.Drawing.Color.FromArgb(0, 255, 0, 255),    //----- 3 - Green
      System.Drawing.Color.FromArgb(0, 255, 255, 255),    //----- 4 - Cyan
      System.Drawing.Color.FromArgb(0, 0, 255, 255),    //----- 5 - Blue
      System.Drawing.Color.FromArgb(255, 0, 255, 255),    //----- 6 - Magenta
      System.Drawing.Color.FromArgb(255, 255, 255, 255),//----- 7 - White
      System.Drawing.Color.FromArgb(255, 255, 255, 255),//----- 8
      System.Drawing.Color.FromArgb(255, 255, 255, 255),//----- 9
      System.Drawing.Color.FromArgb(255, 0, 0, 255),    //----- 10
      System.Drawing.Color.FromArgb(255, 127, 127, 255),//----- 11
      System.Drawing.Color.FromArgb(165, 0, 0, 255),    //----- 12
      System.Drawing.Color.FromArgb(165, 82, 82, 255),    //----- 13
      System.Drawing.Color.FromArgb(127, 0, 0, 255),    //----- 14
      System.Drawing.Color.FromArgb(127, 63, 63, 255),    //----- 15
      System.Drawing.Color.FromArgb(76, 0, 0, 255),        //----- 16
      System.Drawing.Color.FromArgb(76, 38, 38, 255),    //----- 17
      System.Drawing.Color.FromArgb(38, 0, 0, 255),        //----- 18
      System.Drawing.Color.FromArgb(38, 19, 19, 255),    //----- 19
      System.Drawing.Color.FromArgb(255, 63, 0, 255),    //----- 20
      System.Drawing.Color.FromArgb(255, 159, 127, 255),//----- 21
      System.Drawing.Color.FromArgb(165, 41, 0, 255),    //----- 22
      System.Drawing.Color.FromArgb(165, 103, 82, 255),    //----- 23
      System.Drawing.Color.FromArgb(127, 31, 0, 255),    //----- 24
      System.Drawing.Color.FromArgb(127, 79, 63, 255),    //----- 25
      System.Drawing.Color.FromArgb(76, 19, 0, 255),    //----- 26
      System.Drawing.Color.FromArgb(76, 47, 38, 255),    //----- 27
      System.Drawing.Color.FromArgb(38, 9, 0, 255),        //----- 28
      System.Drawing.Color.FromArgb(38, 23, 19, 255),    //----- 29
      System.Drawing.Color.FromArgb(255, 127, 0, 255),    //----- 30
      System.Drawing.Color.FromArgb(255, 191, 127, 255),//----- 31
      System.Drawing.Color.FromArgb(165, 82, 0, 255),    //----- 32
      System.Drawing.Color.FromArgb(165, 124, 82, 255),    //----- 33
      System.Drawing.Color.FromArgb(127, 63, 0, 255),    //----- 34
      System.Drawing.Color.FromArgb(127, 95, 63, 255),    //----- 35
      System.Drawing.Color.FromArgb(76, 38, 0, 255),    //----- 36
      System.Drawing.Color.FromArgb(76, 57, 38, 255),    //----- 37
      System.Drawing.Color.FromArgb(38, 19, 0, 255),    //----- 38
      System.Drawing.Color.FromArgb(38, 28, 19, 255),    //----- 39
      System.Drawing.Color.FromArgb(255, 191, 0, 255),    //----- 40
      System.Drawing.Color.FromArgb(255, 223, 127, 255),//----- 41
      System.Drawing.Color.FromArgb(165, 124, 0, 255),    //----- 42
      System.Drawing.Color.FromArgb(165, 145, 82, 255),    //----- 43
      System.Drawing.Color.FromArgb(127, 95, 0, 255),    //----- 44
      System.Drawing.Color.FromArgb(127, 111, 63, 255),    //----- 45
      System.Drawing.Color.FromArgb(76, 57, 0, 255),    //----- 46
      System.Drawing.Color.FromArgb(76, 66, 38, 255),    //----- 47
      System.Drawing.Color.FromArgb(38, 28, 0, 255),    //----- 48
      System.Drawing.Color.FromArgb(38, 33, 19, 255),    //----- 49
      System.Drawing.Color.FromArgb(255, 255, 0, 255),    //----- 50
      System.Drawing.Color.FromArgb(255, 255, 127, 255),//----- 51
      System.Drawing.Color.FromArgb(165, 165, 0, 255),    //----- 52
      System.Drawing.Color.FromArgb(165, 165, 82, 255),    //----- 53
      System.Drawing.Color.FromArgb(127, 127, 0, 255),    //----- 54
      System.Drawing.Color.FromArgb(127, 127, 63, 255),    //----- 55
      System.Drawing.Color.FromArgb(76, 76, 0, 255),    //----- 56
      System.Drawing.Color.FromArgb(76, 76, 38, 255),    //----- 57
      System.Drawing.Color.FromArgb(38, 38, 0, 255),    //----- 58
      System.Drawing.Color.FromArgb(38, 38, 19, 255),    //----- 59
      System.Drawing.Color.FromArgb(191, 255, 0, 255),    //----- 60
      System.Drawing.Color.FromArgb(223, 255, 127, 255),//----- 61
      System.Drawing.Color.FromArgb(124, 165, 0, 255),    //----- 62
      System.Drawing.Color.FromArgb(145, 165, 82, 255),    //----- 63
      System.Drawing.Color.FromArgb(95, 127, 0, 255),    //----- 64
      System.Drawing.Color.FromArgb(111, 127, 63, 255),    //----- 65
      System.Drawing.Color.FromArgb(57, 76, 0, 255),    //----- 66
      System.Drawing.Color.FromArgb(66, 76, 38, 255),    //----- 67
      System.Drawing.Color.FromArgb(28, 38, 0, 255),    //----- 68
      System.Drawing.Color.FromArgb(33, 38, 19, 255),    //----- 69
      System.Drawing.Color.FromArgb(127, 255, 0, 255),    //----- 70
      System.Drawing.Color.FromArgb(191, 255, 127, 255),//----- 71
      System.Drawing.Color.FromArgb(82, 165, 0, 255),    //----- 72
      System.Drawing.Color.FromArgb(124, 165, 82, 255),    //----- 73
      System.Drawing.Color.FromArgb(63, 127, 0, 255),    //----- 74
      System.Drawing.Color.FromArgb(95, 127, 63, 255),    //----- 75
      System.Drawing.Color.FromArgb(38, 76, 0, 255),    //----- 76
      System.Drawing.Color.FromArgb(57, 76, 38, 255),    //----- 77
      System.Drawing.Color.FromArgb(19, 38, 0, 255),    //----- 78
      System.Drawing.Color.FromArgb(28, 38, 19, 255),    //----- 79
      System.Drawing.Color.FromArgb(63, 255, 0, 255),    //----- 80
      System.Drawing.Color.FromArgb(159, 255, 127, 255),//----- 81
      System.Drawing.Color.FromArgb(41, 165, 0, 255),    //----- 82
      System.Drawing.Color.FromArgb(103, 165, 82, 255),    //----- 83
      System.Drawing.Color.FromArgb(31, 127, 0, 255),    //----- 84
      System.Drawing.Color.FromArgb(79, 127, 63, 255),    //----- 85
      System.Drawing.Color.FromArgb(19, 76, 0, 255),    //----- 86
      System.Drawing.Color.FromArgb(47, 76, 38, 255),    //----- 87
      System.Drawing.Color.FromArgb(9, 38, 0, 255),        //----- 88
      System.Drawing.Color.FromArgb(23, 38, 19, 255),    //----- 89
      System.Drawing.Color.FromArgb(0, 255, 0, 255),    //----- 90
      System.Drawing.Color.FromArgb(127, 255, 127, 255),//----- 91
      System.Drawing.Color.FromArgb(0, 165, 0, 255),    //----- 92
      System.Drawing.Color.FromArgb(82, 165, 82, 255),    //----- 93
      System.Drawing.Color.FromArgb(0, 127, 0, 255),    //----- 94
      System.Drawing.Color.FromArgb(63, 127, 63, 255),    //----- 95
      System.Drawing.Color.FromArgb(0, 76, 0, 255),        //----- 96
      System.Drawing.Color.FromArgb(38, 76, 38, 255),    //----- 97
      System.Drawing.Color.FromArgb(0, 38, 0, 255),        //----- 98
      System.Drawing.Color.FromArgb(19, 38, 19, 255),    //----- 99
      System.Drawing.Color.FromArgb(0, 255, 63, 255),    //----- 100
      System.Drawing.Color.FromArgb(127, 255, 159, 255),//----- 101
      System.Drawing.Color.FromArgb(0, 165, 41, 255),    //----- 102
      System.Drawing.Color.FromArgb(82, 165, 103, 255),    //----- 103
      System.Drawing.Color.FromArgb(0, 127, 31, 255),    //----- 104
      System.Drawing.Color.FromArgb(63, 127, 79, 255),    //----- 105
      System.Drawing.Color.FromArgb(0, 76, 19, 255),    //----- 106
      System.Drawing.Color.FromArgb(38, 76, 47, 255),    //----- 107
      System.Drawing.Color.FromArgb(0, 38, 9, 255),        //----- 108
      System.Drawing.Color.FromArgb(19, 38, 23, 255),    //----- 109
      System.Drawing.Color.FromArgb(0, 255, 127, 255),    //----- 110
      System.Drawing.Color.FromArgb(127, 255, 191, 255),//----- 111
      System.Drawing.Color.FromArgb(0, 165, 82, 255),    //----- 112
      System.Drawing.Color.FromArgb(82, 165, 124, 255),    //----- 113
      System.Drawing.Color.FromArgb(0, 127, 63, 255),    //----- 114
      System.Drawing.Color.FromArgb(63, 127, 95, 255),    //----- 115
      System.Drawing.Color.FromArgb(0, 76, 38, 255),    //----- 116
      System.Drawing.Color.FromArgb(38, 76, 57, 255),    //----- 117
      System.Drawing.Color.FromArgb(0, 38, 19, 255),    //----- 118
      System.Drawing.Color.FromArgb(19, 38, 28, 255),    //----- 119
      System.Drawing.Color.FromArgb(0, 255, 191, 255),    //----- 120
      System.Drawing.Color.FromArgb(127, 255, 223, 255),//----- 121
      System.Drawing.Color.FromArgb(0, 165, 124, 255),    //----- 122
      System.Drawing.Color.FromArgb(82, 165, 145, 255),    //----- 123
      System.Drawing.Color.FromArgb(0, 127, 95, 255),    //----- 124
      System.Drawing.Color.FromArgb(63, 127, 111, 255),    //----- 125
      System.Drawing.Color.FromArgb(0, 76, 57, 255),    //----- 126
      System.Drawing.Color.FromArgb(38, 76, 66, 255),    //----- 127
      System.Drawing.Color.FromArgb(0, 38, 28, 255),    //----- 128
      System.Drawing.Color.FromArgb(19, 38, 33, 255),    //----- 129
      System.Drawing.Color.FromArgb(0, 255, 255, 255),    //----- 130
      System.Drawing.Color.FromArgb(127, 255, 255, 255),//----- 131
      System.Drawing.Color.FromArgb(0, 165, 165, 255),    //----- 132
      System.Drawing.Color.FromArgb(82, 165, 165, 255),    //----- 133
      System.Drawing.Color.FromArgb(0, 127, 127, 255),    //----- 134
      System.Drawing.Color.FromArgb(63, 127, 127, 255),    //----- 135
      System.Drawing.Color.FromArgb(0, 76, 76, 255),    //----- 136
      System.Drawing.Color.FromArgb(38, 76, 76, 255),    //----- 137
      System.Drawing.Color.FromArgb(0, 38, 38, 255),    //----- 138
      System.Drawing.Color.FromArgb(19, 38, 38, 255),    //----- 139
      System.Drawing.Color.FromArgb(0, 191, 255, 255),    //----- 140
      System.Drawing.Color.FromArgb(127, 223, 255, 255),//----- 141
      System.Drawing.Color.FromArgb(0, 124, 165, 255),    //----- 142
      System.Drawing.Color.FromArgb(82, 145, 165, 255),    //----- 143
      System.Drawing.Color.FromArgb(0, 95, 127, 255),    //----- 144
      System.Drawing.Color.FromArgb(63, 111, 127, 255),    //----- 145
      System.Drawing.Color.FromArgb(0, 57, 76, 255),    //----- 146
      System.Drawing.Color.FromArgb(38, 66, 76, 255),    //----- 147
      System.Drawing.Color.FromArgb(0, 28, 38, 255),    //----- 148
      System.Drawing.Color.FromArgb(19, 33, 38, 255),    //----- 149
      System.Drawing.Color.FromArgb(0, 127, 255, 255),    //----- 150
      System.Drawing.Color.FromArgb(127, 191, 255, 255),//----- 151
      System.Drawing.Color.FromArgb(0, 82, 165, 255),    //----- 152
      System.Drawing.Color.FromArgb(82, 124, 165, 255),    //----- 153
      System.Drawing.Color.FromArgb(0, 63, 127, 255),    //----- 154
      System.Drawing.Color.FromArgb(63, 95, 127, 255),    //----- 155
      System.Drawing.Color.FromArgb(0, 38, 76, 255),    //----- 156
      System.Drawing.Color.FromArgb(38, 57, 76, 255),    //----- 157
      System.Drawing.Color.FromArgb(0, 19, 38, 255),    //----- 158
      System.Drawing.Color.FromArgb(19, 28, 38, 255),    //----- 159
      System.Drawing.Color.FromArgb(0, 63, 255, 255),    //----- 160
      System.Drawing.Color.FromArgb(127, 159, 255, 255),//----- 161
      System.Drawing.Color.FromArgb(0, 41, 165, 255),    //----- 162
      System.Drawing.Color.FromArgb(82, 103, 165, 255),    //----- 163
      System.Drawing.Color.FromArgb(0, 31, 127, 255),    //----- 164
      System.Drawing.Color.FromArgb(63, 79, 127, 255),    //----- 165
      System.Drawing.Color.FromArgb(0, 19, 76, 255),    //----- 166
      System.Drawing.Color.FromArgb(38, 47, 76, 255),    //----- 167
      System.Drawing.Color.FromArgb(0, 9, 38, 255),        //----- 168
      System.Drawing.Color.FromArgb(19, 23, 38, 255),    //----- 169
      System.Drawing.Color.FromArgb(0, 0, 255, 255),    //----- 170
      System.Drawing.Color.FromArgb(127, 127, 255, 255),//----- 171
      System.Drawing.Color.FromArgb(0, 0, 165, 255),    //----- 172
      System.Drawing.Color.FromArgb(82, 82, 165, 255),    //----- 173
      System.Drawing.Color.FromArgb(0, 0, 127, 255),    //----- 174
      System.Drawing.Color.FromArgb(63, 63, 127, 255),    //----- 175
      System.Drawing.Color.FromArgb(0, 0, 76, 255),        //----- 176
      System.Drawing.Color.FromArgb(38, 38, 76, 255),    //----- 177
      System.Drawing.Color.FromArgb(0, 0, 38, 255),        //----- 178
      System.Drawing.Color.FromArgb(19, 19, 38, 255),    //----- 179
      System.Drawing.Color.FromArgb(63, 0, 255, 255),    //----- 180
      System.Drawing.Color.FromArgb(159, 127, 255, 255),//----- 181
      System.Drawing.Color.FromArgb(41, 0, 165, 255),    //----- 182
      System.Drawing.Color.FromArgb(103, 82, 165, 255),    //----- 183
      System.Drawing.Color.FromArgb(31, 0, 127, 255),    //----- 184
      System.Drawing.Color.FromArgb(79, 63, 127, 255),    //----- 185
      System.Drawing.Color.FromArgb(19, 0, 76, 255),    //----- 186
      System.Drawing.Color.FromArgb(47, 38, 76, 255),    //----- 187
      System.Drawing.Color.FromArgb(9, 0, 38, 255),        //----- 188
      System.Drawing.Color.FromArgb(23, 19, 38, 255),    //----- 189
      System.Drawing.Color.FromArgb(127, 0, 255, 255),    //----- 190
      System.Drawing.Color.FromArgb(191, 127, 255, 255),//----- 191
      System.Drawing.Color.FromArgb(82, 0, 165, 255),    //----- 192
      System.Drawing.Color.FromArgb(124, 82, 165, 255),    //----- 193
      System.Drawing.Color.FromArgb(63, 0, 127, 255),    //----- 194
      System.Drawing.Color.FromArgb(95, 63, 127, 255),    //----- 195
      System.Drawing.Color.FromArgb(38, 0, 76, 255),    //----- 196
      System.Drawing.Color.FromArgb(57, 38, 76, 255),    //----- 197
      System.Drawing.Color.FromArgb(19, 0, 38, 255),    //----- 198
      System.Drawing.Color.FromArgb(28, 19, 38, 255),    //----- 199
      System.Drawing.Color.FromArgb(191, 0, 255, 255),    //----- 200
      System.Drawing.Color.FromArgb(223, 127, 255, 255),//----- 201
      System.Drawing.Color.FromArgb(124, 0, 165, 255),    //----- 202
      System.Drawing.Color.FromArgb(145, 82, 165, 255),    //----- 203
      System.Drawing.Color.FromArgb(95, 0, 127, 255),    //----- 204
      System.Drawing.Color.FromArgb(111, 63, 127, 255),    //----- 205
      System.Drawing.Color.FromArgb(57, 0, 76, 255),    //----- 206
      System.Drawing.Color.FromArgb(66, 38, 76, 255),    //----- 207
      System.Drawing.Color.FromArgb(28, 0, 38, 255),    //----- 208
      System.Drawing.Color.FromArgb(33, 19, 38, 255),    //----- 209
      System.Drawing.Color.FromArgb(255, 0, 255, 255),    //----- 210
      System.Drawing.Color.FromArgb(255, 127, 255, 255),//----- 211
      System.Drawing.Color.FromArgb(165, 0, 165, 255),    //----- 212
      System.Drawing.Color.FromArgb(165, 82, 165, 255),    //----- 213
      System.Drawing.Color.FromArgb(127, 0, 127, 255),    //----- 214
      System.Drawing.Color.FromArgb(127, 63, 127, 255),    //----- 215
      System.Drawing.Color.FromArgb(76, 0, 76, 255),    //----- 216
      System.Drawing.Color.FromArgb(76, 38, 76, 255),    //----- 217
      System.Drawing.Color.FromArgb(38, 0, 38, 255),    //----- 218
      System.Drawing.Color.FromArgb(38, 19, 38, 255),    //----- 219
      System.Drawing.Color.FromArgb(255, 0, 191, 255),    //----- 220
      System.Drawing.Color.FromArgb(255, 127, 223, 255),//----- 221
      System.Drawing.Color.FromArgb(165, 0, 124, 255),    //----- 222
      System.Drawing.Color.FromArgb(165, 82, 145, 255),    //----- 223
      System.Drawing.Color.FromArgb(127, 0, 95, 255),    //----- 224
      System.Drawing.Color.FromArgb(127, 63, 111, 255),    //----- 225
      System.Drawing.Color.FromArgb(76, 0, 57, 255),    //----- 226
      System.Drawing.Color.FromArgb(76, 38, 66, 255),    //----- 227
      System.Drawing.Color.FromArgb(38, 0, 28, 255),    //----- 228
      System.Drawing.Color.FromArgb(38, 19, 33, 255),    //----- 229
      System.Drawing.Color.FromArgb(255, 0, 127, 255),    //----- 230
      System.Drawing.Color.FromArgb(255, 127, 191, 255),//----- 231
      System.Drawing.Color.FromArgb(165, 0, 82, 255),    //----- 232
      System.Drawing.Color.FromArgb(165, 82, 124, 255),    //----- 233
      System.Drawing.Color.FromArgb(127, 0, 63, 255),    //----- 234
      System.Drawing.Color.FromArgb(127, 63, 95, 255),    //----- 235
      System.Drawing.Color.FromArgb(76, 0, 38, 255),    //----- 236
      System.Drawing.Color.FromArgb(76, 38, 57, 255),    //----- 237
      System.Drawing.Color.FromArgb(38, 0, 19, 255),    //----- 238
      System.Drawing.Color.FromArgb(38, 19, 28, 255),    //----- 239
      System.Drawing.Color.FromArgb(255, 0, 63, 255),    //----- 240
      System.Drawing.Color.FromArgb(255, 127, 159, 255),//----- 241
      System.Drawing.Color.FromArgb(165, 0, 41, 255),    //----- 242
      System.Drawing.Color.FromArgb(165, 82, 103, 255),    //----- 243
      System.Drawing.Color.FromArgb(127, 0, 31, 255),    //----- 244
      System.Drawing.Color.FromArgb(127, 63, 79, 255),    //----- 245
      System.Drawing.Color.FromArgb(76, 0, 19, 255),    //----- 246
      System.Drawing.Color.FromArgb(76, 38, 47, 255),    //----- 247
      System.Drawing.Color.FromArgb(38, 0, 9, 255),        //----- 248
      System.Drawing.Color.FromArgb(38, 19, 23, 255),    //----- 249
      System.Drawing.Color.FromArgb(84, 84, 84, 255),    //----- 250
      System.Drawing.Color.FromArgb(118, 118, 118, 255),//----- 251
      System.Drawing.Color.FromArgb(152, 152, 152, 255),//----- 252
      System.Drawing.Color.FromArgb(186, 186, 186, 255),//----- 253
      System.Drawing.Color.FromArgb(220, 220, 220, 255),//----- 254
      System.Drawing.Color.FromArgb(255, 255, 255, 255),//----- 255
    };

        public static bool GetActiveViewPortInfo(ref double height, ref double width, ref Point3d target, ref Vector3d viewDir, ref double viewTwist, bool getViewCenter)
        {
            // get the editor object
            Editor ed = ZwSoft.ZwCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument.Editor;
            ed.UpdateTiledViewportsInDatabase();
            Database db = HostApplicationServices.WorkingDatabase;
            using (Transaction t = db.TransactionManager.StartTransaction())
            {
                ViewportTable vt = (ViewportTable)t.GetObject(db.ViewportTableId, OpenMode.ForRead);
                ViewportTableRecord btr = (ViewportTableRecord)t.GetObject(vt[GSUtil.strActive], OpenMode.ForRead);
                height = btr.Height;
                width = btr.Width;
                target = btr.Target;
                viewDir = btr.ViewDirection;
                viewTwist = btr.ViewTwist;
                t.Commit();
            }
            return true;
        }
        public static void mpManager_ViewToBeDestroyed(Object sender, ViewEventArgs e)
        {
            // get the editor object
            Editor ed = ZwSoft.ZwCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument.Editor;
            ed.WriteMessage("BlockView: Event ViewToBeDestroyed fired");
        }
        public static void mpManager_ViewWasCreated(Object sender, ViewEventArgs e)
        {
            // get the editor object
            Editor ed = ZwSoft.ZwCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument.Editor;
            ed.WriteMessage("BlockView: Event ViewWasCreated fired");
        }
        public static void mpManager_GsToBeUnloaded(Object sender, EventArgs e)
        {
            // get the editor object
            Editor ed = ZwSoft.ZwCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument.Editor;
            ed.WriteMessage("BlockView: Event GsToBeUnloaded fired");
        }
        public static void mpManager_ConfigWasModified(Object sender, EventArgs e)
        {
            // get the editor object
            Editor ed = ZwSoft.ZwCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument.Editor;
            ed.WriteMessage("BlockView: Event ConfigWasModified fired");
        }

        /// <summary>
        /// [TT]: Depreciated (using ControlPaint.DrawReversibleFrame() instead)
        /// </summary>

        public class RubberbandRectangle
        {
            public enum PenStyles
            {
                PS_SOLID = 0,
                PS_DASH = 1,
                PS_DOT = 2,
                PS_DASHDOT = 3,
                PS_DASHDOTDOT = 4
            }
            // These values come from the larger set of defines in WinGDI.h,
            // but are all that are needed for this application.  If this class
            // is expanded for more generic rectangle drawing, they should be
            // replaced by enums from those sets of defones.
            private int NULL_BRUSH = 5;
            private int R2_XORPEN = 7;
            private PenStyles penStyle;
            private int BLACK_PEN = 0;

            // Default contructor - sets member fields
            public RubberbandRectangle()
            {
                penStyle = PenStyles.PS_DOT;
            }

            // penStyles property get/set.
            public PenStyles PenStyle
            {
                get
                {
                    return penStyle;
                }
                set
                {
                    penStyle = value;
                }
            }

            public void DrawXORRectangle(Graphics grp, System.Drawing.Point startPt, System.Drawing.Point endPt)
            {
                int X1 = startPt.X;
                int Y1 = startPt.Y;
                int X2 = endPt.X;
                int Y2 = endPt.Y;
                // Extract the Win32 HDC from the Graphics object supplied.
                IntPtr hdc = grp.GetHdc();

                // Create a pen with a dotted style to draw the border of the
                // rectangle.
                IntPtr gdiPen = CreatePen(penStyle,
                                  1, BLACK_PEN);

                // Set the ROP cdrawint mode to XOR.
                SetROP2(hdc, R2_XORPEN);

                // Select the pen into the device context.
                IntPtr oldPen = SelectObject(hdc, gdiPen);

                // Create a stock NULL_BRUSH brush and select it into the device
                // context so that the rectangle isn't filled.
                IntPtr oldBrush = SelectObject(hdc,
                                            GetStockObject(NULL_BRUSH));

                // Now XOR the hollow rectangle on the Graphics object with
                // a dotted outline.
                Rectangle(hdc, X1, Y1, X2, Y2);

                // Put the old stuff back where it was.
                SelectObject(hdc, oldBrush); // no need to delete a stock object
                SelectObject(hdc, oldPen);
                DeleteObject(gdiPen);       // but we do need to delete the pen

                // Return the device context to Windows.
                grp.ReleaseHdc(hdc);
            }

            // Use Interop to call the corresponding Win32 GDI functions
            [System.Runtime.InteropServices.DllImportAttribute("gdi32.dll")]
            private static extern int SetROP2(
                      IntPtr hdc,       // Handle to a Win32 device context
                      int enDrawMode    // Drawing mode
                      );
            [System.Runtime.InteropServices.DllImportAttribute("gdi32.dll")]
            private static extern IntPtr CreatePen(
                      PenStyles enPenStyle, // Pen style from enum PenStyles
                      int nWidth,               // Width of pen
                      int crColor               // Color of pen
                      );
            [System.Runtime.InteropServices.DllImportAttribute("gdi32.dll")]
            private static extern bool DeleteObject(
                      IntPtr hObject    // Win32 GDI handle to object to delete
                      );
            [System.Runtime.InteropServices.DllImportAttribute("gdi32.dll")]
            private static extern IntPtr SelectObject(
                      IntPtr hdc,       // Win32 GDI device context
                      IntPtr hObject    // Win32 GDI handle to object to select
                      );
            [System.Runtime.InteropServices.DllImportAttribute("gdi32.dll")]
            private static extern void Rectangle(
                      IntPtr hdc,           // Handle to a Win32 device context
                      int X1,               // x-coordinate of top left corner
                      int Y1,               // y-cordinate of top left corner
                      int X2,               // x-coordinate of bottom right corner
                      int Y2                // y-coordinate of bottm right corner
                      );
            [System.Runtime.InteropServices.DllImportAttribute("gdi32.dll")]
            private static extern IntPtr GetStockObject(
                      int brStyle   // Selected from the WinGDI.h BrushStyles enum
                      );

            // Csharp version of Win32 RGB macro
            private static int RGB(int R, int G, int B)
            {
                return (R | (G << 8) | (B << 16));
            }
        }
    }
}

```

`EnumToolStripMenuItem.cs`

```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows.Forms;
//using GsRenderMode = Autodesk.AutoCAD.GraphicsSystem.RenderMode;
using System.ComponentModel;
using System.Reflection;

namespace BlockView.NET
{

	// A specialization of ToolStripMenuItem that can be used
	// to represent memberss of an enum type

	public class EnumToolStripMenuItem : ToolStripMenuItem
	{
		bool isFlag = false;
		long intval = 0L;

		EnumToolStripMenuItem( Enum value, EventHandler onClick )
			: base( GetItemText( value ) )
		{
			base.Tag = value;
			if( onClick != null )
				base.Click += onClick;
			isFlag = IsFlags( value.GetType() );
			intval = Convert.ToInt64( value );
		}
		
		public static EnumToolStripMenuItem[] CreateItems<T>() where T : struct 
		{
			return CreateItems( typeof(T), null );
		}

		public static EnumToolStripMenuItem[] CreateItems<T>( EventHandler onClick ) where T : struct
		{
			return CreateItems( typeof( T ), onClick );
		}

		public static EnumToolStripMenuItem[] CreateItems<T>( IEnumerable<T> items, EventHandler onClick ) where T : struct
		{
			return CreateItems( items.Cast<Enum>(), onClick );
		}

		public static EnumToolStripMenuItem[] CreateItems( Type enumType )
		{
			return CreateItems( enumType, null );
		}

		public static EnumToolStripMenuItem[] CreateItems( Type enumType, EventHandler onClick )
		{
			if( enumType == null )
				throw new ArgumentNullException( "enumType" );
			if( !enumType.IsEnum )
				throw new ArgumentException( "Requires an Enum type" );
			return CreateItems( Enum.GetValues( enumType ).Cast<Enum>().Distinct(), onClick );
		}

		// This override can be used to selectively add a specific set of members:
		public static EnumToolStripMenuItem[] CreateItems( IEnumerable<Enum> values, EventHandler onClick )
		{
			return values.Select( v => new EnumToolStripMenuItem( v, onClick ) ).ToArray();
		}

		public static void UpdateCheckedState( ToolStripItemCollection items, Enum value )
		{
			foreach( EnumToolStripMenuItem item in items.OfType<EnumToolStripMenuItem>() )
			{
				item.UpdateCheckedState( value );
			}
		}

		public void UpdateCheckedState( Enum value )
		{
			if( base.Tag != null && base.Tag.GetType() == value.GetType() )
			{
				Int64 flags = Convert.ToInt64( value );
				base.Checked = isFlag ? ( ( intval & flags ) == intval ) : intval == flags;
			}
		}

		static string GetItemText( Enum value )
		{
			FieldInfo fi = value.GetType().GetField( value.ToString() );
			if( fi != null )
			{
				DescriptionAttribute[] att = (DescriptionAttribute[])
					fi.GetCustomAttributes( typeof( DescriptionAttribute ), false );
				if( att != null && att.Length > 0 )
				{
					string desc = att[0].Description;
					if( !string.IsNullOrEmpty( desc ) )
						return desc;
				}
			}
			return value.ToString();
		}

		public Enum Value
		{
			get
			{
				return (Enum) base.Tag;
			}
		}

		public Int64 IntVal
		{
			get
			{
				return intval;
			}
		}

		static bool IsFlags( Type enumType )
		{
			var a = enumType.GetCustomAttributes( typeof( FlagsAttribute ), false );
			return a != null && a.Length > 0;
		}
	}

}
```

`Helpers.cs`

```css
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Collections;
using System.IO;
using System.Diagnostics;
using System.Windows.Forms;

namespace BlockView.NET
{
	public static class BlockViewExtensionMethods
	{
		/// <summary>
		/// 
		/// This extension method can be called on any IEnumerable<T> 
		/// where the element type T implements the IDisposable interface.
		/// It's purpose is to guarantee the entire sequence is disposed
		/// even if an exception is thrown by the call to Dispose() on any
		/// element in the sequence.
		/// 
		/// </summary>
	
		public static void DisposeItems<T>( this IEnumerable<T> items ) where T : IDisposable
		{
			DisposeItems( items.GetEnumerator() );
		}

		static void DisposeItems( IEnumerator e ) 
		{
			while( e.MoveNext() )
			{
				try
				{
					IDisposable disposable = e.Current as IDisposable;
					if( disposable != null )
						disposable.Dispose();
				}
				catch
				{
					DisposeItems( e );
					throw;
				}
			}

		}
	}

	/// <summary>
	///
	/// [TT]: Detecting design-time execution:
	/// 
	/// The IsDesignMode method of this class should be used in preference
	/// to the DesignMode property of Control. The latter is only true when
	/// called on a control that is being designed. It is NOT true when it
	/// is called on an instance of a control that is a child of a control 
	/// that's being designed (e.g., the GsPreviewCtrl), or when called on 
	/// an instance of a base type of a control that is being designed.
	/// 
	/// For example, within the GsPreviewCtrl class, if the GsPreviewCtrl's
	/// DesignMode property is read when the BlockViewDialog is open in the 
	/// designer, it will return false because the GsPreviewCtrl is not what
	/// is being designed (the BlockViewDialog is what's being designed).
	/// 
	/// </summary>

	public static class Utils
	{
		static bool designMode = string.Equals(
			Path.GetFileNameWithoutExtension( Process.GetCurrentProcess().MainModule.FileName ),
			"devenv",
			StringComparison.OrdinalIgnoreCase );

		public static bool IsDesignMode( this Control control )
		{
			return designMode;
		}

		public static bool DesignMode
		{
			get
			{
				return designMode;
			}
		}
	}
}
```

![image-20250415083021590](http://image.jerryma.xyz//images/20250415-image-20250415083021590.png)

## wpf相关处理

`MainWindow.xaml`

```csharp
<Window
    x:Class="WpfApp1.MainWindow"
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
    xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
    xmlns:local="clr-namespace:WpfApp1"
    xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
    xmlns:wf="clr-namespace:BlockView.NET;assembly=BlockView.NET"
    Title="MainWindow"
    Width="800"
    Height="450"
    mc:Ignorable="d">
    <Grid>
        <Grid.RowDefinitions>
            <RowDefinition Height="Auto" />
            <RowDefinition Height="*" />
            <RowDefinition Height="Auto" />
        </Grid.RowDefinitions>
        <Grid.ColumnDefinitions>
            <ColumnDefinition Width="*" />
            <ColumnDefinition Width="2*" />
        </Grid.ColumnDefinitions>
        <WindowsFormsHost
            Name="winFormsHost"
            Grid.RowSpan="2"
            Grid.Column="1">
            <wf:GsPreviewCtrl x:Name="blockView" />
        </WindowsFormsHost>
        <StackPanel Margin="10,20">
            <Button
                Name="btnLoad"
                Margin="0,5"
                Click="btnLoad_Click">
                Load
            </Button>
            <Button
                Name="btnSave"
                Margin="0,5"
                Click="BtnSave_Click">
                Save
            </Button>
            <Button
                Name="btnClear"
                Margin="0,5"
                Click="BtnClear_Click">
                Clear
            </Button>
        </StackPanel>
    </Grid>
</Window>
```

`MainWindow.xaml.cs`

```csharp
namespace WpfApp1
{
    /// <summary>
    /// MainWindow.xaml 的交互逻辑
    /// </summary>
    public partial class MainWindow : Window
    {
        Document document;
        public MainWindow()
        {
            InitializeComponent();
            document = AcadApp.DocumentManager.MdiActiveDocument;
            blockView.Init(document, document.Database);
        }

        private void btnLoad_Click(object sender, RoutedEventArgs e)
        {
            //创建文件选择对话框选择dwg文件
            OpenFileDialog openFileDialog = new OpenFileDialog();
            openFileDialog.Filter = "dwg文件|*.dwg";
            if (openFileDialog.ShowDialog() == true)
            {
                //打开dwg文件
                Database dwg = new Database(false, true);
                // now read it in
                dwg.ReadDwgFile(openFileDialog.FileName, FileOpenMode.OpenForReadAndReadShare, true, "");
                // initialising the drawing control, pass the existing document still as the gs view still refers to it
                blockView.Init(document, dwg);
            }
        }
        private void BtnSave_Click(object sender, RoutedEventArgs e)
        {

        }

        private void BtnClear_Click(object sender, RoutedEventArgs e)
        {
            blockView.Init(document, document.Database);
        }
    }
}
```

![image-20250415083557963](http://image.jerryma.xyz//images/20250415-image-20250415083557963.png)


        private void RubberRectangle(Point p1, Point p2)
        {
            Rectangle rc = new Rectangle();
    
            // Convert the points to screen coordinates.
            p1 = PointToScreen(p1);
            p2 = PointToScreen(p2);
            // Normalize the rectangle.
            if (p1.X < p2.X)
            {
                rc.X = p1.X;
                rc.Width = p2.X - p1.X;
            }
            else
            {
                rc.X = p2.X;
                rc.Width = p1.X - p2.X;
            }
            if (p1.Y < p2.Y)
            {
                rc.Y = p1.Y;
                rc.Height = p2.Y - p1.Y;
            }
            else
            {
                rc.Y = p2.Y;
                rc.Height = p1.Y - p2.Y;
            }
            // Draw the reversible frame.
            ControlPaint.DrawReversibleFrame(rc, Color.White, FrameStyle.Dashed);
        }
    
        // [TT]: Refactored to exclude AutoCAD types from methods that run in the designer:
    
        public void refreshView()
        {
            if (!IsDesignMode)
            {
                InternalRefreshView();
            }
        }
    
        // This method will never be jit'ed in the designer:
    
        void InternalRefreshView()
        {
            if (mpView != null)
            {
                mpView.Invalidate();
                mpView.Update();
            }
        }
    
        protected override void OnPaint(System.Windows.Forms.PaintEventArgs e)
        {
            base.OnPaint(e);
            refreshView();
        }
    
        // [TT]: Refactored to exclude AutoCAD types from methods that run in the designer:
    
        protected override void OnMouseMove(System.Windows.Forms.MouseEventArgs e)
        {
            base.OnMouseMove(e);
            if (!IsDesignMode)
            {
                InternalOnMouseMove(e);
            }
        }
    
        private void InternalOnMouseMove(System.Windows.Forms.MouseEventArgs e)
        {
            if (mpView != null)
            {
                if (mZooming)
                {
                    // if left button is down
                    if (mMouseDown)
                    {
                        if (mMouseMoving)
                        {
                            // erase the old rectangle
                            RubberRectangle(mStartPoint, mEndPoint);
                        }
                        // draw the new rectangle
                        RubberRectangle(mStartPoint, e.Location);
                        mMouseMoving = true;
                        // save the new point for next time
                        mEndPoint = e.Location;
                    }
                }
                else
                {
                    if (mbPanning)
                    {
                        //transform the point from device coordinates to
                        //world coordinates
                        Vector3d pan_vec = new Vector3d(-(e.Location.X - mStartPoint.X), e.Location.Y - mStartPoint.Y, 0);
                        /*pan_vec = */
                        pan_vec.TransformBy(mpView.ViewingMatrix * mpView.WorldToDeviceMatrix.Inverse());
                        mpView.Dolly(pan_vec);
                        refreshView();
                        mStartPoint = e.Location;
                    }
                    if (mbOrbiting)
                    {
                        double Half_Pi = 1.570796326795;
    
                        System.Drawing.Rectangle view_rect = new System.Drawing.Rectangle((int)mpView.ViewportExtents.MinPoint.X, (int)mpView.ViewportExtents.MinPoint.Y,
                                                                               (int)(mpView.ViewportExtents.MaxPoint.X - mpView.ViewportExtents.MinPoint.X),
                                                                               (int)(mpView.ViewportExtents.MaxPoint.Y - mpView.ViewportExtents.MinPoint.Y));
    
                        int nViewportX = (view_rect.Right - view_rect.Left) + 1;
                        int nViewportY = (view_rect.Bottom - view_rect.Top) + 1;
    
                        int centerX = (int)(nViewportX / 2.0f + view_rect.Left);
                        int centerY = (int)(nViewportY / 2.0f + view_rect.Top);
    
                        double radius = System.Math.Min(nViewportX, nViewportY) * 0.4f;
    
                        // compute two vectors from last and new cursor positions:
    
                        Vector3d last_vector = new Vector3d((mStartPoint.X - centerX) / radius,
                             -(mStartPoint.Y - centerY) / radius,
                             0.0);
                        if (last_vector.LengthSqrd > 1.0)     // outside the radius
                        {
                            double x = last_vector.X / last_vector.Length;
                            double y = last_vector.Y / last_vector.Length;
                            double z = last_vector.Z / last_vector.Length;
                            last_vector = new Vector3d(x, y, z);
    
                        }
                        else
                        {
                            double x = last_vector.X;
                            double y = last_vector.Y;
                            double z = System.Math.Sqrt(1.0 - last_vector.X * last_vector.X - last_vector.Y * last_vector.Y);
                            last_vector = new Vector3d(x, y, z);
                        }
    
                        Vector3d new_vector = new Vector3d((e.Location.X - centerX) / radius, -(e.Location.Y - centerY) / radius, 0.0);
    
                        if (new_vector.LengthSqrd > 1.0)     // outside the radius
                        {
                            double x = new_vector.X / new_vector.Length;
                            double y = new_vector.Y / new_vector.Length;
                            double z = new_vector.Z / new_vector.Length;
                            new_vector = new Vector3d(x, y, z);
    
                        }
                        else
                        {
                            double x = new_vector.X;
                            double y = new_vector.Y;
                            double z = System.Math.Sqrt(1.0 - new_vector.X * new_vector.X - new_vector.Y * new_vector.Y);
                            new_vector = new Vector3d(x, y, z);
                        }
    
                        // determine angles for proper sequence of camera manipulations:
    
                        Vector3d rotation_vector = last_vector;
                        rotation_vector = rotation_vector.CrossProduct(new_vector);  // rotation_vector = last_vector x new_vector
    
                        Vector3d work_vector = rotation_vector;
                        work_vector = new Vector3d(work_vector.X, work_vector.Y, 0.0f);                      // projection of rotation_vector onto xy plane
    
                        double roll_angle = System.Math.Atan2(work_vector.X,
                             work_vector.Y);        // assuming that the camera's up vector is "up",
                                                    // this computes the angle between the up vector 
                                                    // and the work vector, which is the roll required
                                                    // to make the up vector coincident with the rotation_vector
                        double length = rotation_vector.Length;
                        double orbit_y_angle = (length != 0.0) ? System.Math.Acos(rotation_vector.Z / length) + Half_Pi : Half_Pi;                   // represents inverse cosine of the dot product of the
                        if (length > 1.0f)                                              // rotation_vector and the up_vector divided by the
                            length = 1.0f;                                              // magnitude of both vectors.  We add pi/2 because we 
                                                                                        // are making the up-vector parallel to the the rotation
                        double rotation_angle = System.Math.Asin(length);                // vector ... up-vector is perpin. to the eye-vector.
    
                        // perform view manipulations
    
                        mpView.Roll(roll_angle);               // 1: roll camera to make up vector coincident with rotation vector
                        mpView.Orbit(0.0f, orbit_y_angle);     // 2: orbit along y to make up vector parallel with rotation vector
                        mpView.Orbit(rotation_angle, 0.0f);     // 3: orbit along x by rotation angle
                        mpView.Orbit(0.0f, -orbit_y_angle);     // 4: orbit along y by the negation of 2
                        mpView.Roll(-roll_angle);               // 5: roll camera by the negation of 1
                        refreshView();
                        mStartPoint = e.Location;
                    }
                }
            }
        }
        public void SetViewTo(ZwSoft.ZwCAD.GraphicsSystem.View view, Database db)
        {
            // just check we have valid extents
            if (db.Extmax.X < db.Extmin.X || db.Extmax.Y < db.Extmin.Y || db.Extmax.Z < db.Extmax.Z)
            {
                db.Extmin = new Point3d(0, 0, 0);
                db.Extmax = new Point3d(400, 400, 400);
            }
            // get the dwg extents
            Point3d extMax = db.Extmax;
            Point3d extMin = db.Extmin;
            // now the active viewport info
            double height = 0.0, width = 0.0, viewTwist = 0.0;
            Point3d targetView = new Point3d();
            Vector3d viewDir = new Vector3d();
            GSUtil.GetActiveViewPortInfo(ref height, ref width, ref targetView, ref viewDir, ref viewTwist, true);
            // from the data returned let's work out the viewmatrix
            viewDir = viewDir.GetNormal();
            Vector3d viewXDir = viewDir.GetPerpendicularVector().GetNormal();
            viewXDir = viewXDir.RotateBy(viewTwist, -viewDir);
            Vector3d viewYDir = viewDir.CrossProduct(viewXDir);
            Point3d boxCenter = extMin + 0.5 * (extMax - extMin);
            Matrix3d viewMat;
            viewMat = Matrix3d.AlignCoordinateSystem(boxCenter, Vector3d.XAxis, Vector3d.YAxis, Vector3d.ZAxis,
              boxCenter, viewXDir, viewYDir, viewDir).Inverse();
            Extents3d wcsExtents = new Extents3d(extMin, extMax);
            Extents3d viewExtents = wcsExtents;
            viewExtents.TransformBy(viewMat);
            double xMax = System.Math.Abs(viewExtents.MaxPoint.X - viewExtents.MinPoint.X);
            double yMax = System.Math.Abs(viewExtents.MaxPoint.Y - viewExtents.MinPoint.Y);
            Point3d eye = boxCenter + viewDir;
            // finally set the Gs view to the dwg view
            view.SetView(eye, boxCenter, viewYDir, xMax, yMax);
    
            // now update
            refreshView();
        }
    
        // [TT]: Refactored to exclude AutoCAD types from methods that run in the designer:
        protected override void OnMouseDown(System.Windows.Forms.MouseEventArgs e)
        {
            base.OnMouseDown(e);
            if (!IsDesignMode)
            {
                InternalOnMouseDown(e);
            }
        }
    
        private void InternalOnMouseDown(System.Windows.Forms.MouseEventArgs e)
        {
            if (mpView != null)
            {
                if (e.Button == System.Windows.Forms.MouseButtons.Left)
                {
                    // if zooming
                    if (mZooming)
                    {
                        mMouseDown = true;
                        mMouseMoving = false;
                    }
                    else
                    {
                        mbOrbiting = true;
                        this.Focus();
                    }
    
                }
                else if (e.Button == System.Windows.Forms.MouseButtons.Middle)
                {
                    mbPanning = true;
                }
                mStartPoint = e.Location;
            }
        }
    
        // [TT]: Refactored to exclude AutoCAD types from methods that run in the designer:
        protected override void OnMouseUp(System.Windows.Forms.MouseEventArgs e)
        {
            base.OnMouseUp(e);
            if (!IsDesignMode)
            {
                InternalOnMouseUp(e);
            }
        }
    
        private void InternalOnMouseUp(System.Windows.Forms.MouseEventArgs e)
        {
            if (mpView != null)
            {
                if (e.Button == System.Windows.Forms.MouseButtons.Left)
                {
                    if (mZooming && mMouseDown)
                    {
                        // end zoom
                        mZooming = false;
                        mMouseDown = false;
                        mMouseMoving = false;


                        mpView.ZoomWindow(new Point2d(mStartPoint.X, this.Bottom - mStartPoint.Y), new Point2d(mEndPoint.X, this.Bottom - mEndPoint.Y));
    
                        refreshView();
                    }
                    else
                    {
                        mbOrbiting = false;
                    }
                }
                else if (e.Button == System.Windows.Forms.MouseButtons.Middle)
                {
                    mbPanning = false;
                }
            }
        }
    
        // [TT]: Refactored to exclude AutoCAD types from methods that run in the designer:
        protected override void OnSizeChanged(EventArgs e)
        {
            base.OnSizeChanged(e);
    
            /// No AutoCAD types can be in this method, so we've
            /// moved the following code to another method which
            /// appears below, and only call that method when not 
            /// running in the designer:
    
            //if( mpDevice != null )
            //{
            //   mpDevice.OnSize( this.Size );
            //}
    
            if (!IsDesignMode)
            {
                InternalOnSizeChanged();
            }
        }
    
        // This method will never be jit'ed in the designer
        void InternalOnSizeChanged()
        {
            if (!(mpDevice is null))
            {
                mpDevice.OnSize(this.Size);
            }
        }
    }
    
    /// <summary>
    /// [TT]: Depreciated (using ControlPaint.DrawReversibleFrame() instead)
    /// </summary>
    
    public class GSUtil
    {
        public const String strActive = "*Active";
        public const String strActiveSettings = "ACAD_RENDER_ACTIVE_SETTINGS";
        public static void CustomUpdate(System.IntPtr parmeter, int left, int right, int bottom, int top)
        {
            MessageBox.Show("Left:" + left + "Right" + right + "Bottom" + bottom + "Top" + top);
        }
        public static System.Drawing.Color[] MyAcadColorPs =
    {
      System.Drawing.Color.FromArgb(255, 0, 0, 255),    //----- 0 - lets make it red for an example
      //{255, 255, 255, 255},//----- 0 - ByBlock - White
      System.Drawing.Color.FromArgb(255, 0, 0, 255),    //----- 1 - Red 
      System.Drawing.Color.FromArgb(255, 255, 0, 255),    //----- 2 - Yellow
      System.Drawing.Color.FromArgb(0, 255, 0, 255),    //----- 3 - Green
      System.Drawing.Color.FromArgb(0, 255, 255, 255),    //----- 4 - Cyan
      System.Drawing.Color.FromArgb(0, 0, 255, 255),    //----- 5 - Blue
      System.Drawing.Color.FromArgb(255, 0, 255, 255),    //----- 6 - Magenta
      System.Drawing.Color.FromArgb(255, 0, 0, 255),    //----- 7 - More red Red 
      System.Drawing.Color.FromArgb(255, 0, 0, 255),    //----- 8 - More red Red 
      System.Drawing.Color.FromArgb(255, 0, 0, 255),    //----- 9 - More red Red 
      /*System.Drawing.Color.FromArgb(255, 255, 255, 255),//----- 7 - White
      System.Drawing.Color.FromArgb(255, 255, 255, 255),//----- 8
      System.Drawing.Color.FromArgb(255, 255, 255, 255),//----- 9*/
      System.Drawing.Color.FromArgb(255, 0, 0, 255),    //----- 10
      System.Drawing.Color.FromArgb(255, 127, 127, 255),//----- 11
      System.Drawing.Color.FromArgb(165, 0, 0, 255),    //----- 12
      System.Drawing.Color.FromArgb(165, 82, 82, 255),    //----- 13
      System.Drawing.Color.FromArgb(127, 0, 0, 255),    //----- 14
      System.Drawing.Color.FromArgb(127, 63, 63, 255),    //----- 15
      System.Drawing.Color.FromArgb(76, 0, 0, 255),        //----- 16
      System.Drawing.Color.FromArgb(76, 38, 38, 255),    //----- 17
      System.Drawing.Color.FromArgb(38, 0, 0, 255),        //----- 18
      System.Drawing.Color.FromArgb(38, 19, 19, 255),    //----- 19
      System.Drawing.Color.FromArgb(255, 63, 0, 255),    //----- 20
      System.Drawing.Color.FromArgb(255, 159, 127, 255),//----- 21
      System.Drawing.Color.FromArgb(165, 41, 0, 255),    //----- 22
      System.Drawing.Color.FromArgb(165, 103, 82, 255),    //----- 23
      System.Drawing.Color.FromArgb(127, 31, 0, 255),    //----- 24
      System.Drawing.Color.FromArgb(127, 79, 63, 255),    //----- 25
      System.Drawing.Color.FromArgb(76, 19, 0, 255),    //----- 26
      System.Drawing.Color.FromArgb(76, 47, 38, 255),    //----- 27
      System.Drawing.Color.FromArgb(38, 9, 0, 255),        //----- 28
      System.Drawing.Color.FromArgb(38, 23, 19, 255),    //----- 29
      System.Drawing.Color.FromArgb(255, 127, 0, 255),    //----- 30
      System.Drawing.Color.FromArgb(255, 191, 127, 255),//----- 31
      System.Drawing.Color.FromArgb(165, 82, 0, 255),    //----- 32
      System.Drawing.Color.FromArgb(165, 124, 82, 255),    //----- 33
      System.Drawing.Color.FromArgb(127, 63, 0, 255),    //----- 34
      System.Drawing.Color.FromArgb(127, 95, 63, 255),    //----- 35
      System.Drawing.Color.FromArgb(76, 38, 0, 255),    //----- 36
      System.Drawing.Color.FromArgb(76, 57, 38, 255),    //----- 37
      System.Drawing.Color.FromArgb(38, 19, 0, 255),    //----- 38
      System.Drawing.Color.FromArgb(38, 28, 19, 255),    //----- 39
      System.Drawing.Color.FromArgb(255, 191, 0, 255),    //----- 40
      System.Drawing.Color.FromArgb(255, 223, 127, 255),//----- 41
      System.Drawing.Color.FromArgb(165, 124, 0, 255),    //----- 42
      System.Drawing.Color.FromArgb(165, 145, 82, 255),    //----- 43
      System.Drawing.Color.FromArgb(127, 95, 0, 255),    //----- 44
      System.Drawing.Color.FromArgb(127, 111, 63, 255),    //----- 45
      System.Drawing.Color.FromArgb(76, 57, 0, 255),    //----- 46
      System.Drawing.Color.FromArgb(76, 66, 38, 255),    //----- 47
      System.Drawing.Color.FromArgb(38, 28, 0, 255),    //----- 48
      System.Drawing.Color.FromArgb(38, 33, 19, 255),    //----- 49
      System.Drawing.Color.FromArgb(255, 255, 0, 255),    //----- 50
      System.Drawing.Color.FromArgb(255, 255, 127, 255),//----- 51
      System.Drawing.Color.FromArgb(165, 165, 0, 255),    //----- 52
      System.Drawing.Color.FromArgb(165, 165, 82, 255),    //----- 53
      System.Drawing.Color.FromArgb(127, 127, 0, 255),    //----- 54
      System.Drawing.Color.FromArgb(127, 127, 63, 255),    //----- 55
      System.Drawing.Color.FromArgb(76, 76, 0, 255),    //----- 56
      System.Drawing.Color.FromArgb(76, 76, 38, 255),    //----- 57
      System.Drawing.Color.FromArgb(38, 38, 0, 255),    //----- 58
      System.Drawing.Color.FromArgb(38, 38, 19, 255),    //----- 59
      System.Drawing.Color.FromArgb(191, 255, 0, 255),    //----- 60
      System.Drawing.Color.FromArgb(223, 255, 127, 255),//----- 61
      System.Drawing.Color.FromArgb(124, 165, 0, 255),    //----- 62
      System.Drawing.Color.FromArgb(145, 165, 82, 255),    //----- 63
      System.Drawing.Color.FromArgb(95, 127, 0, 255),    //----- 64
      System.Drawing.Color.FromArgb(111, 127, 63, 255),    //----- 65
      System.Drawing.Color.FromArgb(57, 76, 0, 255),    //----- 66
      System.Drawing.Color.FromArgb(66, 76, 38, 255),    //----- 67
      System.Drawing.Color.FromArgb(28, 38, 0, 255),    //----- 68
      System.Drawing.Color.FromArgb(33, 38, 19, 255),    //----- 69
      System.Drawing.Color.FromArgb(127, 255, 0, 255),    //----- 70
      System.Drawing.Color.FromArgb(191, 255, 127, 255),//----- 71
      System.Drawing.Color.FromArgb(82, 165, 0, 255),    //----- 72
      System.Drawing.Color.FromArgb(124, 165, 82, 255),    //----- 73
      System.Drawing.Color.FromArgb(63, 127, 0, 255),    //----- 74
      System.Drawing.Color.FromArgb(95, 127, 63, 255),    //----- 75
      System.Drawing.Color.FromArgb(38, 76, 0, 255),    //----- 76
      System.Drawing.Color.FromArgb(57, 76, 38, 255),    //----- 77
      System.Drawing.Color.FromArgb(19, 38, 0, 255),    //----- 78
      System.Drawing.Color.FromArgb(28, 38, 19, 255),    //----- 79
      System.Drawing.Color.FromArgb(63, 255, 0, 255),    //----- 80
      System.Drawing.Color.FromArgb(159, 255, 127, 255),//----- 81
      System.Drawing.Color.FromArgb(41, 165, 0, 255),    //----- 82
      System.Drawing.Color.FromArgb(103, 165, 82, 255),    //----- 83
      System.Drawing.Color.FromArgb(31, 127, 0, 255),    //----- 84
      System.Drawing.Color.FromArgb(79, 127, 63, 255),    //----- 85
      System.Drawing.Color.FromArgb(19, 76, 0, 255),    //----- 86
      System.Drawing.Color.FromArgb(47, 76, 38, 255),    //----- 87
      System.Drawing.Color.FromArgb(9, 38, 0, 255),        //----- 88
      System.Drawing.Color.FromArgb(23, 38, 19, 255),    //----- 89
      System.Drawing.Color.FromArgb(0, 255, 0, 255),    //----- 90
      System.Drawing.Color.FromArgb(127, 255, 127, 255),//----- 91
      System.Drawing.Color.FromArgb(0, 165, 0, 255),    //----- 92
      System.Drawing.Color.FromArgb(82, 165, 82, 255),    //----- 93
      System.Drawing.Color.FromArgb(0, 127, 0, 255),    //----- 94
      System.Drawing.Color.FromArgb(63, 127, 63, 255),    //----- 95
      System.Drawing.Color.FromArgb(0, 76, 0, 255),        //----- 96
      System.Drawing.Color.FromArgb(38, 76, 38, 255),    //----- 97
      System.Drawing.Color.FromArgb(0, 38, 0, 255),        //----- 98
      System.Drawing.Color.FromArgb(19, 38, 19, 255),    //----- 99
      System.Drawing.Color.FromArgb(0, 255, 63, 255),    //----- 100
      System.Drawing.Color.FromArgb(127, 255, 159, 255),//----- 101
      System.Drawing.Color.FromArgb(0, 165, 41, 255),    //----- 102
      System.Drawing.Color.FromArgb(82, 165, 103, 255),    //----- 103
      System.Drawing.Color.FromArgb(0, 127, 31, 255),    //----- 104
      System.Drawing.Color.FromArgb(63, 127, 79, 255),    //----- 105
      System.Drawing.Color.FromArgb(0, 76, 19, 255),    //----- 106
      System.Drawing.Color.FromArgb(38, 76, 47, 255),    //----- 107
      System.Drawing.Color.FromArgb(0, 38, 9, 255),        //----- 108
      System.Drawing.Color.FromArgb(19, 38, 23, 255),    //----- 109
      System.Drawing.Color.FromArgb(0, 255, 127, 255),    //----- 110
      System.Drawing.Color.FromArgb(127, 255, 191, 255),//----- 111
      System.Drawing.Color.FromArgb(0, 165, 82, 255),    //----- 112
      System.Drawing.Color.FromArgb(82, 165, 124, 255),    //----- 113
      System.Drawing.Color.FromArgb(0, 127, 63, 255),    //----- 114
      System.Drawing.Color.FromArgb(63, 127, 95, 255),    //----- 115
      System.Drawing.Color.FromArgb(0, 76, 38, 255),    //----- 116
      System.Drawing.Color.FromArgb(38, 76, 57, 255),    //----- 117
      System.Drawing.Color.FromArgb(0, 38, 19, 255),    //----- 118
      System.Drawing.Color.FromArgb(19, 38, 28, 255),    //----- 119
      System.Drawing.Color.FromArgb(0, 255, 191, 255),    //----- 120
      System.Drawing.Color.FromArgb(127, 255, 223, 255),//----- 121
      System.Drawing.Color.FromArgb(0, 165, 124, 255),    //----- 122
      System.Drawing.Color.FromArgb(82, 165, 145, 255),    //----- 123
      System.Drawing.Color.FromArgb(0, 127, 95, 255),    //----- 124
      System.Drawing.Color.FromArgb(63, 127, 111, 255),    //----- 125
      System.Drawing.Color.FromArgb(0, 76, 57, 255),    //----- 126
      System.Drawing.Color.FromArgb(38, 76, 66, 255),    //----- 127
      System.Drawing.Color.FromArgb(0, 38, 28, 255),    //----- 128
      System.Drawing.Color.FromArgb(19, 38, 33, 255),    //----- 129
      System.Drawing.Color.FromArgb(0, 255, 255, 255),    //----- 130
      System.Drawing.Color.FromArgb(127, 255, 255, 255),//----- 131
      System.Drawing.Color.FromArgb(0, 165, 165, 255),    //----- 132
      System.Drawing.Color.FromArgb(82, 165, 165, 255),    //----- 133
      System.Drawing.Color.FromArgb(0, 127, 127, 255),    //----- 134
      System.Drawing.Color.FromArgb(63, 127, 127, 255),    //----- 135
      System.Drawing.Color.FromArgb(0, 76, 76, 255),    //----- 136
      System.Drawing.Color.FromArgb(38, 76, 76, 255),    //----- 137
      System.Drawing.Color.FromArgb(0, 38, 38, 255),    //----- 138
      System.Drawing.Color.FromArgb(19, 38, 38, 255),    //----- 139
      System.Drawing.Color.FromArgb(0, 191, 255, 255),    //----- 140
      System.Drawing.Color.FromArgb(127, 223, 255, 255),//----- 141
      System.Drawing.Color.FromArgb(0, 124, 165, 255),    //----- 142
      System.Drawing.Color.FromArgb(82, 145, 165, 255),    //----- 143
      System.Drawing.Color.FromArgb(0, 95, 127, 255),    //----- 144
      System.Drawing.Color.FromArgb(63, 111, 127, 255),    //----- 145
      System.Drawing.Color.FromArgb(0, 57, 76, 255),    //----- 146
      System.Drawing.Color.FromArgb(38, 66, 76, 255),    //----- 147
      System.Drawing.Color.FromArgb(0, 28, 38, 255),    //----- 148
      System.Drawing.Color.FromArgb(19, 33, 38, 255),    //----- 149
      System.Drawing.Color.FromArgb(0, 127, 255, 255),    //----- 150
      System.Drawing.Color.FromArgb(127, 191, 255, 255),//----- 151
      System.Drawing.Color.FromArgb(0, 82, 165, 255),    //----- 152
      System.Drawing.Color.FromArgb(82, 124, 165, 255),    //----- 153
      System.Drawing.Color.FromArgb(0, 63, 127, 255),    //----- 154
      System.Drawing.Color.FromArgb(63, 95, 127, 255),    //----- 155
      System.Drawing.Color.FromArgb(0, 38, 76, 255),    //----- 156
      System.Drawing.Color.FromArgb(38, 57, 76, 255),    //----- 157
      System.Drawing.Color.FromArgb(0, 19, 38, 255),    //----- 158
      System.Drawing.Color.FromArgb(19, 28, 38, 255),    //----- 159
      System.Drawing.Color.FromArgb(0, 63, 255, 255),    //----- 160
      System.Drawing.Color.FromArgb(127, 159, 255, 255),//----- 161
      System.Drawing.Color.FromArgb(0, 41, 165, 255),    //----- 162
      System.Drawing.Color.FromArgb(82, 103, 165, 255),    //----- 163
      System.Drawing.Color.FromArgb(0, 31, 127, 255),    //----- 164
      System.Drawing.Color.FromArgb(63, 79, 127, 255),    //----- 165
      System.Drawing.Color.FromArgb(0, 19, 76, 255),    //----- 166
      System.Drawing.Color.FromArgb(38, 47, 76, 255),    //----- 167
      System.Drawing.Color.FromArgb(0, 9, 38, 255),        //----- 168
      System.Drawing.Color.FromArgb(19, 23, 38, 255),    //----- 169
      System.Drawing.Color.FromArgb(0, 0, 255, 255),    //----- 170
      System.Drawing.Color.FromArgb(127, 127, 255, 255),//----- 171
      System.Drawing.Color.FromArgb(0, 0, 165, 255),    //----- 172
      System.Drawing.Color.FromArgb(82, 82, 165, 255),    //----- 173
      System.Drawing.Color.FromArgb(0, 0, 127, 255),    //----- 174
      System.Drawing.Color.FromArgb(63, 63, 127, 255),    //----- 175
      System.Drawing.Color.FromArgb(0, 0, 76, 255),        //----- 176
      System.Drawing.Color.FromArgb(38, 38, 76, 255),    //----- 177
      System.Drawing.Color.FromArgb(0, 0, 38, 255),        //----- 178
      System.Drawing.Color.FromArgb(19, 19, 38, 255),    //----- 179
      System.Drawing.Color.FromArgb(63, 0, 255, 255),    //----- 180
      System.Drawing.Color.FromArgb(159, 127, 255, 255),//----- 181
      System.Drawing.Color.FromArgb(41, 0, 165, 255),    //----- 182
      System.Drawing.Color.FromArgb(103, 82, 165, 255),    //----- 183
      System.Drawing.Color.FromArgb(31, 0, 127, 255),    //----- 184
      System.Drawing.Color.FromArgb(79, 63, 127, 255),    //----- 185
      System.Drawing.Color.FromArgb(19, 0, 76, 255),    //----- 186
      System.Drawing.Color.FromArgb(47, 38, 76, 255),    //----- 187
      System.Drawing.Color.FromArgb(9, 0, 38, 255),        //----- 188
      System.Drawing.Color.FromArgb(23, 19, 38, 255),    //----- 189
      System.Drawing.Color.FromArgb(127, 0, 255, 255),    //----- 190
      System.Drawing.Color.FromArgb(191, 127, 255, 255),//----- 191
      System.Drawing.Color.FromArgb(82, 0, 165, 255),    //----- 192
      System.Drawing.Color.FromArgb(124, 82, 165, 255),    //----- 193
      System.Drawing.Color.FromArgb(63, 0, 127, 255),    //----- 194
      System.Drawing.Color.FromArgb(95, 63, 127, 255),    //----- 195
      System.Drawing.Color.FromArgb(38, 0, 76, 255),    //----- 196
      System.Drawing.Color.FromArgb(57, 38, 76, 255),    //----- 197
      System.Drawing.Color.FromArgb(19, 0, 38, 255),    //----- 198
      System.Drawing.Color.FromArgb(28, 19, 38, 255),    //----- 199
      System.Drawing.Color.FromArgb(191, 0, 255, 255),    //----- 200
      System.Drawing.Color.FromArgb(223, 127, 255, 255),//----- 201
      System.Drawing.Color.FromArgb(124, 0, 165, 255),    //----- 202
      System.Drawing.Color.FromArgb(145, 82, 165, 255),    //----- 203
      System.Drawing.Color.FromArgb(95, 0, 127, 255),    //----- 204
      System.Drawing.Color.FromArgb(111, 63, 127, 255),    //----- 205
      System.Drawing.Color.FromArgb(57, 0, 76, 255),    //----- 206
      System.Drawing.Color.FromArgb(66, 38, 76, 255),    //----- 207
      System.Drawing.Color.FromArgb(28, 0, 38, 255),    //----- 208
      System.Drawing.Color.FromArgb(33, 19, 38, 255),    //----- 209
      System.Drawing.Color.FromArgb(255, 0, 255, 255),    //----- 210
      System.Drawing.Color.FromArgb(255, 127, 255, 255),//----- 211
      System.Drawing.Color.FromArgb(165, 0, 165, 255),    //----- 212
      System.Drawing.Color.FromArgb(165, 82, 165, 255),    //----- 213
      System.Drawing.Color.FromArgb(127, 0, 127, 255),    //----- 214
      System.Drawing.Color.FromArgb(127, 63, 127, 255),    //----- 215
      System.Drawing.Color.FromArgb(76, 0, 76, 255),    //----- 216
      System.Drawing.Color.FromArgb(76, 38, 76, 255),    //----- 217
      System.Drawing.Color.FromArgb(38, 0, 38, 255),    //----- 218
      System.Drawing.Color.FromArgb(38, 19, 38, 255),    //----- 219
      System.Drawing.Color.FromArgb(255, 0, 191, 255),    //----- 220
      System.Drawing.Color.FromArgb(255, 127, 223, 255),//----- 221
      System.Drawing.Color.FromArgb(165, 0, 124, 255),    //----- 222
      System.Drawing.Color.FromArgb(165, 82, 145, 255),    //----- 223
      System.Drawing.Color.FromArgb(127, 0, 95, 255),    //----- 224
      System.Drawing.Color.FromArgb(127, 63, 111, 255),    //----- 225
      System.Drawing.Color.FromArgb(76, 0, 57, 255),    //----- 226
      System.Drawing.Color.FromArgb(76, 38, 66, 255),    //----- 227
      System.Drawing.Color.FromArgb(38, 0, 28, 255),    //----- 228
      System.Drawing.Color.FromArgb(38, 19, 33, 255),    //----- 229
      System.Drawing.Color.FromArgb(255, 0, 127, 255),    //----- 230
      System.Drawing.Color.FromArgb(255, 127, 191, 255),//----- 231
      System.Drawing.Color.FromArgb(165, 0, 82, 255),    //----- 232
      System.Drawing.Color.FromArgb(165, 82, 124, 255),    //----- 233
      System.Drawing.Color.FromArgb(127, 0, 63, 255),    //----- 234
      System.Drawing.Color.FromArgb(127, 63, 95, 255),    //----- 235
      System.Drawing.Color.FromArgb(76, 0, 38, 255),    //----- 236
      System.Drawing.Color.FromArgb(76, 38, 57, 255),    //----- 237
      System.Drawing.Color.FromArgb(38, 0, 19, 255),    //----- 238
      System.Drawing.Color.FromArgb(38, 19, 28, 255),    //----- 239
      System.Drawing.Color.FromArgb(255, 0, 63, 255),    //----- 240
      System.Drawing.Color.FromArgb(255, 127, 159, 255),//----- 241
      System.Drawing.Color.FromArgb(165, 0, 41, 255),    //----- 242
      System.Drawing.Color.FromArgb(165, 82, 103, 255),    //----- 243
      System.Drawing.Color.FromArgb(127, 0, 31, 255),    //----- 244
      System.Drawing.Color.FromArgb(127, 63, 79, 255),    //----- 245
      System.Drawing.Color.FromArgb(76, 0, 19, 255),    //----- 246
      System.Drawing.Color.FromArgb(76, 38, 47, 255),    //----- 247
      System.Drawing.Color.FromArgb(38, 0, 9, 255),        //----- 248
      System.Drawing.Color.FromArgb(38, 19, 23, 255),    //----- 249
      System.Drawing.Color.FromArgb(84, 84, 84, 255),    //----- 250
      System.Drawing.Color.FromArgb(118, 118, 118, 255),//----- 251
      System.Drawing.Color.FromArgb(152, 152, 152, 255),//----- 252
      System.Drawing.Color.FromArgb(186, 186, 186, 255),//----- 253
      System.Drawing.Color.FromArgb(220, 220, 220, 255),//----- 254
      System.Drawing.Color.FromArgb(255, 255, 255, 255),//----- 255
    };
    
        //////////////////////////////////////////////////////////////////////////////
        // standard autocad colours
        public static System.Drawing.Color[] MyAcadColorMs =
    {
      System.Drawing.Color.FromArgb(255, 255, 255, 255),//----- 0 - ByBlock - White
      System.Drawing.Color.FromArgb(255, 0, 0, 255),    //----- 1 - Red 
      System.Drawing.Color.FromArgb(255, 255, 0, 255),    //----- 2 - Yellow
      System.Drawing.Color.FromArgb(0, 255, 0, 255),    //----- 3 - Green
      System.Drawing.Color.FromArgb(0, 255, 255, 255),    //----- 4 - Cyan
      System.Drawing.Color.FromArgb(0, 0, 255, 255),    //----- 5 - Blue
      System.Drawing.Color.FromArgb(255, 0, 255, 255),    //----- 6 - Magenta
      System.Drawing.Color.FromArgb(255, 255, 255, 255),//----- 7 - White
      System.Drawing.Color.FromArgb(255, 255, 255, 255),//----- 8
      System.Drawing.Color.FromArgb(255, 255, 255, 255),//----- 9
      System.Drawing.Color.FromArgb(255, 0, 0, 255),    //----- 10
      System.Drawing.Color.FromArgb(255, 127, 127, 255),//----- 11
      System.Drawing.Color.FromArgb(165, 0, 0, 255),    //----- 12
      System.Drawing.Color.FromArgb(165, 82, 82, 255),    //----- 13
      System.Drawing.Color.FromArgb(127, 0, 0, 255),    //----- 14
      System.Drawing.Color.FromArgb(127, 63, 63, 255),    //----- 15
      System.Drawing.Color.FromArgb(76, 0, 0, 255),        //----- 16
      System.Drawing.Color.FromArgb(76, 38, 38, 255),    //----- 17
      System.Drawing.Color.FromArgb(38, 0, 0, 255),        //----- 18
      System.Drawing.Color.FromArgb(38, 19, 19, 255),    //----- 19
      System.Drawing.Color.FromArgb(255, 63, 0, 255),    //----- 20
      System.Drawing.Color.FromArgb(255, 159, 127, 255),//----- 21
      System.Drawing.Color.FromArgb(165, 41, 0, 255),    //----- 22
      System.Drawing.Color.FromArgb(165, 103, 82, 255),    //----- 23
      System.Drawing.Color.FromArgb(127, 31, 0, 255),    //----- 24
      System.Drawing.Color.FromArgb(127, 79, 63, 255),    //----- 25
      System.Drawing.Color.FromArgb(76, 19, 0, 255),    //----- 26
      System.Drawing.Color.FromArgb(76, 47, 38, 255),    //----- 27
      System.Drawing.Color.FromArgb(38, 9, 0, 255),        //----- 28
      System.Drawing.Color.FromArgb(38, 23, 19, 255),    //----- 29
      System.Drawing.Color.FromArgb(255, 127, 0, 255),    //----- 30
      System.Drawing.Color.FromArgb(255, 191, 127, 255),//----- 31
      System.Drawing.Color.FromArgb(165, 82, 0, 255),    //----- 32
      System.Drawing.Color.FromArgb(165, 124, 82, 255),    //----- 33
      System.Drawing.Color.FromArgb(127, 63, 0, 255),    //----- 34
      System.Drawing.Color.FromArgb(127, 95, 63, 255),    //----- 35
      System.Drawing.Color.FromArgb(76, 38, 0, 255),    //----- 36
      System.Drawing.Color.FromArgb(76, 57, 38, 255),    //----- 37
      System.Drawing.Color.FromArgb(38, 19, 0, 255),    //----- 38
      System.Drawing.Color.FromArgb(38, 28, 19, 255),    //----- 39
      System.Drawing.Color.FromArgb(255, 191, 0, 255),    //----- 40
      System.Drawing.Color.FromArgb(255, 223, 127, 255),//----- 41
      System.Drawing.Color.FromArgb(165, 124, 0, 255),    //----- 42
      System.Drawing.Color.FromArgb(165, 145, 82, 255),    //----- 43
      System.Drawing.Color.FromArgb(127, 95, 0, 255),    //----- 44
      System.Drawing.Color.FromArgb(127, 111, 63, 255),    //----- 45
      System.Drawing.Color.FromArgb(76, 57, 0, 255),    //----- 46
      System.Drawing.Color.FromArgb(76, 66, 38, 255),    //----- 47
      System.Drawing.Color.FromArgb(38, 28, 0, 255),    //----- 48
      System.Drawing.Color.FromArgb(38, 33, 19, 255),    //----- 49
      System.Drawing.Color.FromArgb(255, 255, 0, 255),    //----- 50
      System.Drawing.Color.FromArgb(255, 255, 127, 255),//----- 51
      System.Drawing.Color.FromArgb(165, 165, 0, 255),    //----- 52
      System.Drawing.Color.FromArgb(165, 165, 82, 255),    //----- 53
      System.Drawing.Color.FromArgb(127, 127, 0, 255),    //----- 54
      System.Drawing.Color.FromArgb(127, 127, 63, 255),    //----- 55
      System.Drawing.Color.FromArgb(76, 76, 0, 255),    //----- 56
      System.Drawing.Color.FromArgb(76, 76, 38, 255),    //----- 57
      System.Drawing.Color.FromArgb(38, 38, 0, 255),    //----- 58
      System.Drawing.Color.FromArgb(38, 38, 19, 255),    //----- 59
      System.Drawing.Color.FromArgb(191, 255, 0, 255),    //----- 60
      System.Drawing.Color.FromArgb(223, 255, 127, 255),//----- 61
      System.Drawing.Color.FromArgb(124, 165, 0, 255),    //----- 62
      System.Drawing.Color.FromArgb(145, 165, 82, 255),    //----- 63
      System.Drawing.Color.FromArgb(95, 127, 0, 255),    //----- 64
      System.Drawing.Color.FromArgb(111, 127, 63, 255),    //----- 65
      System.Drawing.Color.FromArgb(57, 76, 0, 255),    //----- 66
      System.Drawing.Color.FromArgb(66, 76, 38, 255),    //----- 67
      System.Drawing.Color.FromArgb(28, 38, 0, 255),    //----- 68
      System.Drawing.Color.FromArgb(33, 38, 19, 255),    //----- 69
      System.Drawing.Color.FromArgb(127, 255, 0, 255),    //----- 70
      System.Drawing.Color.FromArgb(191, 255, 127, 255),//----- 71
      System.Drawing.Color.FromArgb(82, 165, 0, 255),    //----- 72
      System.Drawing.Color.FromArgb(124, 165, 82, 255),    //----- 73
      System.Drawing.Color.FromArgb(63, 127, 0, 255),    //----- 74
      System.Drawing.Color.FromArgb(95, 127, 63, 255),    //----- 75
      System.Drawing.Color.FromArgb(38, 76, 0, 255),    //----- 76
      System.Drawing.Color.FromArgb(57, 76, 38, 255),    //----- 77
      System.Drawing.Color.FromArgb(19, 38, 0, 255),    //----- 78
      System.Drawing.Color.FromArgb(28, 38, 19, 255),    //----- 79
      System.Drawing.Color.FromArgb(63, 255, 0, 255),    //----- 80
      System.Drawing.Color.FromArgb(159, 255, 127, 255),//----- 81
      System.Drawing.Color.FromArgb(41, 165, 0, 255),    //----- 82
      System.Drawing.Color.FromArgb(103, 165, 82, 255),    //----- 83
      System.Drawing.Color.FromArgb(31, 127, 0, 255),    //----- 84
      System.Drawing.Color.FromArgb(79, 127, 63, 255),    //----- 85
      System.Drawing.Color.FromArgb(19, 76, 0, 255),    //----- 86
      System.Drawing.Color.FromArgb(47, 76, 38, 255),    //----- 87
      System.Drawing.Color.FromArgb(9, 38, 0, 255),        //----- 88
      System.Drawing.Color.FromArgb(23, 38, 19, 255),    //----- 89
      System.Drawing.Color.FromArgb(0, 255, 0, 255),    //----- 90
      System.Drawing.Color.FromArgb(127, 255, 127, 255),//----- 91
      System.Drawing.Color.FromArgb(0, 165, 0, 255),    //----- 92
      System.Drawing.Color.FromArgb(82, 165, 82, 255),    //----- 93
      System.Drawing.Color.FromArgb(0, 127, 0, 255),    //----- 94
      System.Drawing.Color.FromArgb(63, 127, 63, 255),    //----- 95
      System.Drawing.Color.FromArgb(0, 76, 0, 255),        //----- 96
      System.Drawing.Color.FromArgb(38, 76, 38, 255),    //----- 97
      System.Drawing.Color.FromArgb(0, 38, 0, 255),        //----- 98
      System.Drawing.Color.FromArgb(19, 38, 19, 255),    //----- 99
      System.Drawing.Color.FromArgb(0, 255, 63, 255),    //----- 100
      System.Drawing.Color.FromArgb(127, 255, 159, 255),//----- 101
      System.Drawing.Color.FromArgb(0, 165, 41, 255),    //----- 102
      System.Drawing.Color.FromArgb(82, 165, 103, 255),    //----- 103
      System.Drawing.Color.FromArgb(0, 127, 31, 255),    //----- 104
      System.Drawing.Color.FromArgb(63, 127, 79, 255),    //----- 105
      System.Drawing.Color.FromArgb(0, 76, 19, 255),    //----- 106
      System.Drawing.Color.FromArgb(38, 76, 47, 255),    //----- 107
      System.Drawing.Color.FromArgb(0, 38, 9, 255),        //----- 108
      System.Drawing.Color.FromArgb(19, 38, 23, 255),    //----- 109
      System.Drawing.Color.FromArgb(0, 255, 127, 255),    //----- 110
      System.Drawing.Color.FromArgb(127, 255, 191, 255),//----- 111
      System.Drawing.Color.FromArgb(0, 165, 82, 255),    //----- 112
      System.Drawing.Color.FromArgb(82, 165, 124, 255),    //----- 113
      System.Drawing.Color.FromArgb(0, 127, 63, 255),    //----- 114
      System.Drawing.Color.FromArgb(63, 127, 95, 255),    //----- 115
      System.Drawing.Color.FromArgb(0, 76, 38, 255),    //----- 116
      System.Drawing.Color.FromArgb(38, 76, 57, 255),    //----- 117
      System.Drawing.Color.FromArgb(0, 38, 19, 255),    //----- 118
      System.Drawing.Color.FromArgb(19, 38, 28, 255),    //----- 119
      System.Drawing.Color.FromArgb(0, 255, 191, 255),    //----- 120
      System.Drawing.Color.FromArgb(127, 255, 223, 255),//----- 121
      System.Drawing.Color.FromArgb(0, 165, 124, 255),    //----- 122
      System.Drawing.Color.FromArgb(82, 165, 145, 255),    //----- 123
      System.Drawing.Color.FromArgb(0, 127, 95, 255),    //----- 124
      System.Drawing.Color.FromArgb(63, 127, 111, 255),    //----- 125
      System.Drawing.Color.FromArgb(0, 76, 57, 255),    //----- 126
      System.Drawing.Color.FromArgb(38, 76, 66, 255),    //----- 127
      System.Drawing.Color.FromArgb(0, 38, 28, 255),    //----- 128
      System.Drawing.Color.FromArgb(19, 38, 33, 255),    //----- 129
      System.Drawing.Color.FromArgb(0, 255, 255, 255),    //----- 130
      System.Drawing.Color.FromArgb(127, 255, 255, 255),//----- 131
      System.Drawing.Color.FromArgb(0, 165, 165, 255),    //----- 132
      System.Drawing.Color.FromArgb(82, 165, 165, 255),    //----- 133
      System.Drawing.Color.FromArgb(0, 127, 127, 255),    //----- 134
      System.Drawing.Color.FromArgb(63, 127, 127, 255),    //----- 135
      System.Drawing.Color.FromArgb(0, 76, 76, 255),    //----- 136
      System.Drawing.Color.FromArgb(38, 76, 76, 255),    //----- 137
      System.Drawing.Color.FromArgb(0, 38, 38, 255),    //----- 138
      System.Drawing.Color.FromArgb(19, 38, 38, 255),    //----- 139
      System.Drawing.Color.FromArgb(0, 191, 255, 255),    //----- 140
      System.Drawing.Color.FromArgb(127, 223, 255, 255),//----- 141
      System.Drawing.Color.FromArgb(0, 124, 165, 255),    //----- 142
      System.Drawing.Color.FromArgb(82, 145, 165, 255),    //----- 143
      System.Drawing.Color.FromArgb(0, 95, 127, 255),    //----- 144
      System.Drawing.Color.FromArgb(63, 111, 127, 255),    //----- 145
      System.Drawing.Color.FromArgb(0, 57, 76, 255),    //----- 146
      System.Drawing.Color.FromArgb(38, 66, 76, 255),    //----- 147
      System.Drawing.Color.FromArgb(0, 28, 38, 255),    //----- 148
      System.Drawing.Color.FromArgb(19, 33, 38, 255),    //----- 149
      System.Drawing.Color.FromArgb(0, 127, 255, 255),    //----- 150
      System.Drawing.Color.FromArgb(127, 191, 255, 255),//----- 151
      System.Drawing.Color.FromArgb(0, 82, 165, 255),    //----- 152
      System.Drawing.Color.FromArgb(82, 124, 165, 255),    //----- 153
      System.Drawing.Color.FromArgb(0, 63, 127, 255),    //----- 154
      System.Drawing.Color.FromArgb(63, 95, 127, 255),    //----- 155
      System.Drawing.Color.FromArgb(0, 38, 76, 255),    //----- 156
      System.Drawing.Color.FromArgb(38, 57, 76, 255),    //----- 157
      System.Drawing.Color.FromArgb(0, 19, 38, 255),    //----- 158
      System.Drawing.Color.FromArgb(19, 28, 38, 255),    //----- 159
      System.Drawing.Color.FromArgb(0, 63, 255, 255),    //----- 160
      System.Drawing.Color.FromArgb(127, 159, 255, 255),//----- 161
      System.Drawing.Color.FromArgb(0, 41, 165, 255),    //----- 162
      System.Drawing.Color.FromArgb(82, 103, 165, 255),    //----- 163
      System.Drawing.Color.FromArgb(0, 31, 127, 255),    //----- 164
      System.Drawing.Color.FromArgb(63, 79, 127, 255),    //----- 165
      System.Drawing.Color.FromArgb(0, 19, 76, 255),    //----- 166
      System.Drawing.Color.FromArgb(38, 47, 76, 255),    //----- 167
      System.Drawing.Color.FromArgb(0, 9, 38, 255),        //----- 168
      System.Drawing.Color.FromArgb(19, 23, 38, 255),    //----- 169
      System.Drawing.Color.FromArgb(0, 0, 255, 255),    //----- 170
      System.Drawing.Color.FromArgb(127, 127, 255, 255),//----- 171
      System.Drawing.Color.FromArgb(0, 0, 165, 255),    //----- 172
      System.Drawing.Color.FromArgb(82, 82, 165, 255),    //----- 173
      System.Drawing.Color.FromArgb(0, 0, 127, 255),    //----- 174
      System.Drawing.Color.FromArgb(63, 63, 127, 255),    //----- 175
      System.Drawing.Color.FromArgb(0, 0, 76, 255),        //----- 176
      System.Drawing.Color.FromArgb(38, 38, 76, 255),    //----- 177
      System.Drawing.Color.FromArgb(0, 0, 38, 255),        //----- 178
      System.Drawing.Color.FromArgb(19, 19, 38, 255),    //----- 179
      System.Drawing.Color.FromArgb(63, 0, 255, 255),    //----- 180
      System.Drawing.Color.FromArgb(159, 127, 255, 255),//----- 181
      System.Drawing.Color.FromArgb(41, 0, 165, 255),    //----- 182
      System.Drawing.Color.FromArgb(103, 82, 165, 255),    //----- 183
      System.Drawing.Color.FromArgb(31, 0, 127, 255),    //----- 184
      System.Drawing.Color.FromArgb(79, 63, 127, 255),    //----- 185
      System.Drawing.Color.FromArgb(19, 0, 76, 255),    //----- 186
      System.Drawing.Color.FromArgb(47, 38, 76, 255),    //----- 187
      System.Drawing.Color.FromArgb(9, 0, 38, 255),        //----- 188
      System.Drawing.Color.FromArgb(23, 19, 38, 255),    //----- 189
      System.Drawing.Color.FromArgb(127, 0, 255, 255),    //----- 190
      System.Drawing.Color.FromArgb(191, 127, 255, 255),//----- 191
      System.Drawing.Color.FromArgb(82, 0, 165, 255),    //----- 192
      System.Drawing.Color.FromArgb(124, 82, 165, 255),    //----- 193
      System.Drawing.Color.FromArgb(63, 0, 127, 255),    //----- 194
      System.Drawing.Color.FromArgb(95, 63, 127, 255),    //----- 195
      System.Drawing.Color.FromArgb(38, 0, 76, 255),    //----- 196
      System.Drawing.Color.FromArgb(57, 38, 76, 255),    //----- 197
      System.Drawing.Color.FromArgb(19, 0, 38, 255),    //----- 198
      System.Drawing.Color.FromArgb(28, 19, 38, 255),    //----- 199
      System.Drawing.Color.FromArgb(191, 0, 255, 255),    //----- 200
      System.Drawing.Color.FromArgb(223, 127, 255, 255),//----- 201
      System.Drawing.Color.FromArgb(124, 0, 165, 255),    //----- 202
      System.Drawing.Color.FromArgb(145, 82, 165, 255),    //----- 203
      System.Drawing.Color.FromArgb(95, 0, 127, 255),    //----- 204
      System.Drawing.Color.FromArgb(111, 63, 127, 255),    //----- 205
      System.Drawing.Color.FromArgb(57, 0, 76, 255),    //----- 206
      System.Drawing.Color.FromArgb(66, 38, 76, 255),    //----- 207
      System.Drawing.Color.FromArgb(28, 0, 38, 255),    //----- 208
      System.Drawing.Color.FromArgb(33, 19, 38, 255),    //----- 209
      System.Drawing.Color.FromArgb(255, 0, 255, 255),    //----- 210
      System.Drawing.Color.FromArgb(255, 127, 255, 255),//----- 211
      System.Drawing.Color.FromArgb(165, 0, 165, 255),    //----- 212
      System.Drawing.Color.FromArgb(165, 82, 165, 255),    //----- 213
      System.Drawing.Color.FromArgb(127, 0, 127, 255),    //----- 214
      System.Drawing.Color.FromArgb(127, 63, 127, 255),    //----- 215
      System.Drawing.Color.FromArgb(76, 0, 76, 255),    //----- 216
      System.Drawing.Color.FromArgb(76, 38, 76, 255),    //----- 217
      System.Drawing.Color.FromArgb(38, 0, 38, 255),    //----- 218
      System.Drawing.Color.FromArgb(38, 19, 38, 255),    //----- 219
      System.Drawing.Color.FromArgb(255, 0, 191, 255),    //----- 220
      System.Drawing.Color.FromArgb(255, 127, 223, 255),//----- 221
      System.Drawing.Color.FromArgb(165, 0, 124, 255),    //----- 222
      System.Drawing.Color.FromArgb(165, 82, 145, 255),    //----- 223
      System.Drawing.Color.FromArgb(127, 0, 95, 255),    //----- 224
      System.Drawing.Color.FromArgb(127, 63, 111, 255),    //----- 225
      System.Drawing.Color.FromArgb(76, 0, 57, 255),    //----- 226
      System.Drawing.Color.FromArgb(76, 38, 66, 255),    //----- 227
      System.Drawing.Color.FromArgb(38, 0, 28, 255),    //----- 228
      System.Drawing.Color.FromArgb(38, 19, 33, 255),    //----- 229
      System.Drawing.Color.FromArgb(255, 0, 127, 255),    //----- 230
      System.Drawing.Color.FromArgb(255, 127, 191, 255),//----- 231
      System.Drawing.Color.FromArgb(165, 0, 82, 255),    //----- 232
      System.Drawing.Color.FromArgb(165, 82, 124, 255),    //----- 233
      System.Drawing.Color.FromArgb(127, 0, 63, 255),    //----- 234
      System.Drawing.Color.FromArgb(127, 63, 95, 255),    //----- 235
      System.Drawing.Color.FromArgb(76, 0, 38, 255),    //----- 236
      System.Drawing.Color.FromArgb(76, 38, 57, 255),    //----- 237
      System.Drawing.Color.FromArgb(38, 0, 19, 255),    //----- 238
      System.Drawing.Color.FromArgb(38, 19, 28, 255),    //----- 239
      System.Drawing.Color.FromArgb(255, 0, 63, 255),    //----- 240
      System.Drawing.Color.FromArgb(255, 127, 159, 255),//----- 241
      System.Drawing.Color.FromArgb(165, 0, 41, 255),    //----- 242
      System.Drawing.Color.FromArgb(165, 82, 103, 255),    //----- 243
      System.Drawing.Color.FromArgb(127, 0, 31, 255),    //----- 244
      System.Drawing.Color.FromArgb(127, 63, 79, 255),    //----- 245
      System.Drawing.Color.FromArgb(76, 0, 19, 255),    //----- 246
      System.Drawing.Color.FromArgb(76, 38, 47, 255),    //----- 247
      System.Drawing.Color.FromArgb(38, 0, 9, 255),        //----- 248
      System.Drawing.Color.FromArgb(38, 19, 23, 255),    //----- 249
      System.Drawing.Color.FromArgb(84, 84, 84, 255),    //----- 250
      System.Drawing.Color.FromArgb(118, 118, 118, 255),//----- 251
      System.Drawing.Color.FromArgb(152, 152, 152, 255),//----- 252
      System.Drawing.Color.FromArgb(186, 186, 186, 255),//----- 253
      System.Drawing.Color.FromArgb(220, 220, 220, 255),//----- 254
      System.Drawing.Color.FromArgb(255, 255, 255, 255),//----- 255
    };
    
        public static bool GetActiveViewPortInfo(ref double height, ref double width, ref Point3d target, ref Vector3d viewDir, ref double viewTwist, bool getViewCenter)
        {
            // get the editor object
            Editor ed = ZwSoft.ZwCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument.Editor;
            ed.UpdateTiledViewportsInDatabase();
            Database db = HostApplicationServices.WorkingDatabase;
            using (Transaction t = db.TransactionManager.StartTransaction())
            {
                ViewportTable vt = (ViewportTable)t.GetObject(db.ViewportTableId, OpenMode.ForRead);
                ViewportTableRecord btr = (ViewportTableRecord)t.GetObject(vt[GSUtil.strActive], OpenMode.ForRead);
                height = btr.Height;
                width = btr.Width;
                target = btr.Target;
                viewDir = btr.ViewDirection;
                viewTwist = btr.ViewTwist;
                t.Commit();
            }
            return true;
        }
        public static void mpManager_ViewToBeDestroyed(Object sender, ViewEventArgs e)
        {
            // get the editor object
            Editor ed = ZwSoft.ZwCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument.Editor;
            ed.WriteMessage("BlockView: Event ViewToBeDestroyed fired");
        }
        public static void mpManager_ViewWasCreated(Object sender, ViewEventArgs e)
        {
            // get the editor object
            Editor ed = ZwSoft.ZwCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument.Editor;
            ed.WriteMessage("BlockView: Event ViewWasCreated fired");
        }
        public static void mpManager_GsToBeUnloaded(Object sender, EventArgs e)
        {
            // get the editor object
            Editor ed = ZwSoft.ZwCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument.Editor;
            ed.WriteMessage("BlockView: Event GsToBeUnloaded fired");
        }
        public static void mpManager_ConfigWasModified(Object sender, EventArgs e)
        {
            // get the editor object
            Editor ed = ZwSoft.ZwCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument.Editor;
            ed.WriteMessage("BlockView: Event ConfigWasModified fired");
        }
    
        /// <summary>
        /// [TT]: Depreciated (using ControlPaint.DrawReversibleFrame() instead)
        /// </summary>
    
        public class RubberbandRectangle
        {
            public enum PenStyles
            {
                PS_SOLID = 0,
                PS_DASH = 1,
                PS_DOT = 2,
                PS_DASHDOT = 3,
                PS_DASHDOTDOT = 4
            }
            // These values come from the larger set of defines in WinGDI.h,
            // but are all that are needed for this application.  If this class
            // is expanded for more generic rectangle drawing, they should be
            // replaced by enums from those sets of defones.
            private int NULL_BRUSH = 5;
            private int R2_XORPEN = 7;
            private PenStyles penStyle;
            private int BLACK_PEN = 0;
    
            // Default contructor - sets member fields
            public RubberbandRectangle()
            {
                penStyle = PenStyles.PS_DOT;
            }
    
            // penStyles property get/set.
            public PenStyles PenStyle
            {
                get
                {
                    return penStyle;
                }
                set
                {
                    penStyle = value;
                }
            }
    
            public void DrawXORRectangle(Graphics grp, System.Drawing.Point startPt, System.Drawing.Point endPt)
            {
                int X1 = startPt.X;
                int Y1 = startPt.Y;
                int X2 = endPt.X;
                int Y2 = endPt.Y;
                // Extract the Win32 HDC from the Graphics object supplied.
                IntPtr hdc = grp.GetHdc();
    
                // Create a pen with a dotted style to draw the border of the
                // rectangle.
                IntPtr gdiPen = CreatePen(penStyle,
                                  1, BLACK_PEN);
    
                // Set the ROP cdrawint mode to XOR.
                SetROP2(hdc, R2_XORPEN);
    
                // Select the pen into the device context.
                IntPtr oldPen = SelectObject(hdc, gdiPen);
    
                // Create a stock NULL_BRUSH brush and select it into the device
                // context so that the rectangle isn't filled.
                IntPtr oldBrush = SelectObject(hdc,
                                            GetStockObject(NULL_BRUSH));
    
                // Now XOR the hollow rectangle on the Graphics object with
                // a dotted outline.
                Rectangle(hdc, X1, Y1, X2, Y2);
    
                // Put the old stuff back where it was.
                SelectObject(hdc, oldBrush); // no need to delete a stock object
                SelectObject(hdc, oldPen);
                DeleteObject(gdiPen);       // but we do need to delete the pen
    
                // Return the device context to Windows.
                grp.ReleaseHdc(hdc);
            }
    
            // Use Interop to call the corresponding Win32 GDI functions
            [System.Runtime.InteropServices.DllImportAttribute("gdi32.dll")]
            private static extern int SetROP2(
                      IntPtr hdc,       // Handle to a Win32 device context
                      int enDrawMode    // Drawing mode
                      );
            [System.Runtime.InteropServices.DllImportAttribute("gdi32.dll")]
            private static extern IntPtr CreatePen(
                      PenStyles enPenStyle, // Pen style from enum PenStyles
                      int nWidth,               // Width of pen
                      int crColor               // Color of pen
                      );
            [System.Runtime.InteropServices.DllImportAttribute("gdi32.dll")]
            private static extern bool DeleteObject(
                      IntPtr hObject    // Win32 GDI handle to object to delete
                      );
            [System.Runtime.InteropServices.DllImportAttribute("gdi32.dll")]
            private static extern IntPtr SelectObject(
                      IntPtr hdc,       // Win32 GDI device context
                      IntPtr hObject    // Win32 GDI handle to object to select
                      );
            [System.Runtime.InteropServices.DllImportAttribute("gdi32.dll")]
            private static extern void Rectangle(
                      IntPtr hdc,           // Handle to a Win32 device context
                      int X1,               // x-coordinate of top left corner
                      int Y1,               // y-cordinate of top left corner
                      int X2,               // x-coordinate of bottom right corner
                      int Y2                // y-coordinate of bottm right corner
                      );
            [System.Runtime.InteropServices.DllImportAttribute("gdi32.dll")]
            private static extern IntPtr GetStockObject(
                      int brStyle   // Selected from the WinGDI.h BrushStyles enum
                      );
    
            // Csharp version of Win32 RGB macro
            private static int RGB(int R, int G, int B)
            {
                return (R | (G << 8) | (B << 16));
            }
        }
    }
}

```

`EnumToolStripMenuItem.cs`

​```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows.Forms;
//using GsRenderMode = Autodesk.AutoCAD.GraphicsSystem.RenderMode;
using System.ComponentModel;
using System.Reflection;

namespace BlockView.NET
{

	// A specialization of ToolStripMenuItem that can be used
	// to represent memberss of an enum type

	public class EnumToolStripMenuItem : ToolStripMenuItem
	{
		bool isFlag = false;
		long intval = 0L;

		EnumToolStripMenuItem( Enum value, EventHandler onClick )
			: base( GetItemText( value ) )
		{
			base.Tag = value;
			if( onClick != null )
				base.Click += onClick;
			isFlag = IsFlags( value.GetType() );
			intval = Convert.ToInt64( value );
		}
		
		public static EnumToolStripMenuItem[] CreateItems<T>() where T : struct 
		{
			return CreateItems( typeof(T), null );
		}

		public static EnumToolStripMenuItem[] CreateItems<T>( EventHandler onClick ) where T : struct
		{
			return CreateItems( typeof( T ), onClick );
		}

		public static EnumToolStripMenuItem[] CreateItems<T>( IEnumerable<T> items, EventHandler onClick ) where T : struct
		{
			return CreateItems( items.Cast<Enum>(), onClick );
		}

		public static EnumToolStripMenuItem[] CreateItems( Type enumType )
		{
			return CreateItems( enumType, null );
		}

		public static EnumToolStripMenuItem[] CreateItems( Type enumType, EventHandler onClick )
		{
			if( enumType == null )
				throw new ArgumentNullException( "enumType" );
			if( !enumType.IsEnum )
				throw new ArgumentException( "Requires an Enum type" );
			return CreateItems( Enum.GetValues( enumType ).Cast<Enum>().Distinct(), onClick );
		}

		// This override can be used to selectively add a specific set of members:
		public static EnumToolStripMenuItem[] CreateItems( IEnumerable<Enum> values, EventHandler onClick )
		{
			return values.Select( v => new EnumToolStripMenuItem( v, onClick ) ).ToArray();
		}

		public static void UpdateCheckedState( ToolStripItemCollection items, Enum value )
		{
			foreach( EnumToolStripMenuItem item in items.OfType<EnumToolStripMenuItem>() )
			{
				item.UpdateCheckedState( value );
			}
		}

		public void UpdateCheckedState( Enum value )
		{
			if( base.Tag != null && base.Tag.GetType() == value.GetType() )
			{
				Int64 flags = Convert.ToInt64( value );
				base.Checked = isFlag ? ( ( intval & flags ) == intval ) : intval == flags;
			}
		}

		static string GetItemText( Enum value )
		{
			FieldInfo fi = value.GetType().GetField( value.ToString() );
			if( fi != null )
			{
				DescriptionAttribute[] att = (DescriptionAttribute[])
					fi.GetCustomAttributes( typeof( DescriptionAttribute ), false );
				if( att != null && att.Length > 0 )
				{
					string desc = att[0].Description;
					if( !string.IsNullOrEmpty( desc ) )
						return desc;
				}
			}
			return value.ToString();
		}

		public Enum Value
		{
			get
			{
				return (Enum) base.Tag;
			}
		}

		public Int64 IntVal
		{
			get
			{
				return intval;
			}
		}

		static bool IsFlags( Type enumType )
		{
			var a = enumType.GetCustomAttributes( typeof( FlagsAttribute ), false );
			return a != null && a.Length > 0;
		}
	}

}
```

`Helpers.cs`

```css
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Collections;
using System.IO;
using System.Diagnostics;
using System.Windows.Forms;

namespace BlockView.NET
{
	public static class BlockViewExtensionMethods
	{
		/// <summary>
		/// 
		/// This extension method can be called on any IEnumerable<T> 
		/// where the element type T implements the IDisposable interface.
		/// It's purpose is to guarantee the entire sequence is disposed
		/// even if an exception is thrown by the call to Dispose() on any
		/// element in the sequence.
		/// 
		/// </summary>
	
		public static void DisposeItems<T>( this IEnumerable<T> items ) where T : IDisposable
		{
			DisposeItems( items.GetEnumerator() );
		}

		static void DisposeItems( IEnumerator e ) 
		{
			while( e.MoveNext() )
			{
				try
				{
					IDisposable disposable = e.Current as IDisposable;
					if( disposable != null )
						disposable.Dispose();
				}
				catch
				{
					DisposeItems( e );
					throw;
				}
			}

		}
	}

	/// <summary>
	///
	/// [TT]: Detecting design-time execution:
	/// 
	/// The IsDesignMode method of this class should be used in preference
	/// to the DesignMode property of Control. The latter is only true when
	/// called on a control that is being designed. It is NOT true when it
	/// is called on an instance of a control that is a child of a control 
	/// that's being designed (e.g., the GsPreviewCtrl), or when called on 
	/// an instance of a base type of a control that is being designed.
	/// 
	/// For example, within the GsPreviewCtrl class, if the GsPreviewCtrl's
	/// DesignMode property is read when the BlockViewDialog is open in the 
	/// designer, it will return false because the GsPreviewCtrl is not what
	/// is being designed (the BlockViewDialog is what's being designed).
	/// 
	/// </summary>

	public static class Utils
	{
		static bool designMode = string.Equals(
			Path.GetFileNameWithoutExtension( Process.GetCurrentProcess().MainModule.FileName ),
			"devenv",
			StringComparison.OrdinalIgnoreCase );

# WPF中使用GsPreviewCtrl预览图块

## winform控件处理

`GsPreviewCtrl.cs`

​```csharp
using System;
using System.IO;
using System.Diagnostics;
using System.Collections.Generic;
using System.ComponentModel;
using System.Drawing;
using System.Data;
using System.Text;
using System.Windows.Forms;
using AcadApp = ZwSoft.ZwCAD.ApplicationServices.Application;
using ZwSoft.ZwCAD.ApplicationServices;
using ZwSoft.ZwCAD.DatabaseServices;
using ZwSoft.ZwCAD.Windows;
using ZwSoft.ZwCAD.EditorInput;
using ZwSoft.ZwCAD.Runtime;
using ZwSoft.ZwCAD.Geometry;
using ZwSoft.ZwCAD.GraphicsSystem;
namespace BlockView.NET
{
    public class GsPreviewCtrl : Control
    {
        public GsPreviewCtrl()
        {
        }



        // current dwg
        public Database mCurrentDwg = null;
        // Gs specific
        public ZwSoft.ZwCAD.GraphicsSystem.Manager mpManager = null;
        public ZwSoft.ZwCAD.GraphicsSystem.Device mpDevice = null;
        public ZwSoft.ZwCAD.GraphicsSystem.Model mpModel = null;
        public ZwSoft.ZwCAD.GraphicsSystem.View mpView = null;
        public bool mZooming = false;
        public bool mMouseDown = false;
        public bool mMouseMoving = false;
        public bool mbPanning = false;
        public bool mbOrbiting = false;
        public System.Drawing.Point mStartPoint;
        public System.Drawing.Point mEndPoint;

        public static bool IsDesignMode
        {
            get
            {
                return Utils.IsDesignMode(null);
            }
        }

        protected override void Dispose(bool disposing)
        {
            if (disposing)
            {
                // clear up the GS view gadgets
                if (!IsDesignMode)
                    ClearAll();
                if (mCurrentDwg != null)
                {
                    mCurrentDwg.Dispose();
                    mCurrentDwg = null;
                }
            }
            base.Dispose(disposing);

        }

        // called from InitDrawingControl, does GsPreviewCtrl specific initialization
        public void Init(Document doc, Database db)
        {
            mCurrentDwg = db;
            // check to see if the manager is already initalised
            if (null == mpManager)
            {
                // if not let's set it up
                mpManager = doc.GraphicsManager;
                // here's some test code to show the GS Events working
                mpManager.ViewToBeDestroyed += new ViewToBeDestroyedEventHandler(GSUtil.mpManager_ViewToBeDestroyed);
                mpManager.ViewWasCreated += new ViewWasCreatedEventHandler(GSUtil.mpManager_ViewWasCreated);
                mpManager.GsToBeUnloaded += new GsToBeUnloadedEventHandler(GSUtil.mpManager_GsToBeUnloaded);
                mpManager.ConfigWasModified += new ConfigWasModifiedEventHandler(GSUtil.mpManager_ConfigWasModified);

                KernelDescriptor descriptor = new KernelDescriptor();
                descriptor.addRequirement(ZwSoft.ZwCAD.UniqueString.Intern("3D Drawing"));
                GraphicsKernel kernal = Manager.AcquireGraphicsKernel(descriptor);
                // now create the Gs control, create the autocad device passing the handle to the Windows panel
                mpDevice = mpManager.CreateZWCADDevice(kernal, this.Handle);
                // resize the device to the panel size
                mpDevice.OnSize(this.Size);
                // now create a new gs view
                mpView = new ZwSoft.ZwCAD.GraphicsSystem.View();
                // and create the model
                mpModel = mpManager.CreateZWCADModel(kernal);

                // add the view to the device
                mpDevice.Add(mpView);
            }

            SetViewTo(mpView, mCurrentDwg);
            using (Transaction tr = mCurrentDwg.TransactionManager.StartTransaction())
            {
                BlockTableRecord curSpace = tr.GetObject(mCurrentDwg.CurrentSpaceId, OpenMode.ForRead, true) as BlockTableRecord;
                // 在这里进行你的操作
                mpView.Add(curSpace, mpModel);
                tr.Commit();
            }

            refreshView();
        }


        public void ClearAll()
        {
            if (!IsDesignMode)
            {
                if (!(mpDevice is null))
                {
                    bool b = mpDevice.Erase(mpView);
                }
                if (!(mpView is null))
                {
                    mpView.EraseAll();
                    mpView.Dispose();
                    mpView = null;
                }
                if (!(mpManager is null))
                {
                    if (!(mpModel is null))
                    {
                        mpModel.Dispose();
                        mpModel = null;
                    }

                    if (!(mpDevice is null))
                    {
                        mpDevice.Dispose();
                        mpDevice = null;
                    }
                    mpManager = null;
                }
            }
        }

        // [TT]: Refactored to exclude AutoCAD types from methods that run in the designer:

        public void ErasePreview()
        {
            if (!IsDesignMode)
                InternalErasePreview();
        }

        public void InternalErasePreview()
        {
            if (mpView != null)
                mpView.EraseAll();
            if (mpManager != null && mpModel != null)
            {
                mpModel.Dispose();
                mpModel = null;
            }
        }
		public static bool IsDesignMode( this Control control )
		{
			return designMode;
		}

		public static bool DesignMode
		{
			get
			{
				return designMode;
			}
		}
	}
}
```

![image-20250415083021590](http://image.jerryma.xyz//images/20250415-image-20250415083021590.png)

## wpf相关处理

`MainWindow.xaml`

```csharp
<Window
    x:Class="WpfApp1.MainWindow"
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
    xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
    xmlns:local="clr-namespace:WpfApp1"
    xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
    xmlns:wf="clr-namespace:BlockView.NET;assembly=BlockView.NET"
    Title="MainWindow"
    Width="800"
    Height="450"
    mc:Ignorable="d">
    <Grid>
        <Grid.RowDefinitions>
            <RowDefinition Height="Auto" />
            <RowDefinition Height="*" />
            <RowDefinition Height="Auto" />
        </Grid.RowDefinitions>
        <Grid.ColumnDefinitions>
            <ColumnDefinition Width="*" />
            <ColumnDefinition Width="2*" />
        </Grid.ColumnDefinitions>
        <WindowsFormsHost
            Name="winFormsHost"
            Grid.RowSpan="2"
            Grid.Column="1">
            <wf:GsPreviewCtrl x:Name="blockView" />
        </WindowsFormsHost>
        <StackPanel Margin="10,20">
            <Button
                Name="btnLoad"
                Margin="0,5"
                Click="btnLoad_Click">
                Load
            </Button>
            <Button
                Name="btnSave"
                Margin="0,5"
                Click="BtnSave_Click">
                Save
            </Button>
            <Button
                Name="btnClear"
                Margin="0,5"
                Click="BtnClear_Click">
                Clear
            </Button>
        </StackPanel>
    </Grid>
</Window>
```

`MainWindow.xaml.cs`

```csharp
namespace WpfApp1
{
    /// <summary>
    /// MainWindow.xaml 的交互逻辑
    /// </summary>
    public partial class MainWindow : Window
    {
        Document document;
        public MainWindow()
        {
            InitializeComponent();
            document = AcadApp.DocumentManager.MdiActiveDocument;
            blockView.Init(document, document.Database);
        }

        private void btnLoad_Click(object sender, RoutedEventArgs e)
        {
            //创建文件选择对话框选择dwg文件
            OpenFileDialog openFileDialog = new OpenFileDialog();
            openFileDialog.Filter = "dwg文件|*.dwg";
            if (openFileDialog.ShowDialog() == true)
            {
                //打开dwg文件
                Database dwg = new Database(false, true);
                // now read it in
                dwg.ReadDwgFile(openFileDialog.FileName, FileOpenMode.OpenForReadAndReadShare, true, "");
                // initialising the drawing control, pass the existing document still as the gs view still refers to it
                blockView.Init(document, dwg);
            }
        }
        private void BtnSave_Click(object sender, RoutedEventArgs e)
        {

        }

        private void BtnClear_Click(object sender, RoutedEventArgs e)
        {
            blockView.Init(document, document.Database);
        }
    }
}
```

![image-20250415083557963](http://image.jerryma.xyz//images/20250415-image-20250415083557963.png)

## `无法正常关闭CAD`等后续再完善