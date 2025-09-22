---
title: ObjectARX.net学习1
date: 2024-08-15
categories:
  - windows程序
tags:
  - ObjectARX
  - AutoCAD
  - Csharp
  - CAD插件
description: ObjectARX.net入门教程，包含基础命令开发和绘图功能实现
author: JerryMa
---

# ObjectARX.net学习（1）

## 先下载工具

https://spiderinnet1.typepad.com/

下载[ANAW2017](https://netspiderstudio.com/Downloads/RAIN/ANAW2017.zip)

## 用向导创建项目

## 创建简单demo

```Csharp
#region Namespaces

using System;
using System.Text;
using System.Linq;
using System.Xml;
using System.Reflection;
using System.ComponentModel;
using System.Collections;
using System.Collections.Generic;
using System.Diagnostics;
using System.Windows;
using System.Windows.Media.Imaging;
using System.Windows.Forms;
using System.Drawing;
using System.IO;

using Autodesk.AutoCAD.ApplicationServices;
using Autodesk.AutoCAD.DatabaseServices;
using Autodesk.AutoCAD.Runtime;
using Autodesk.AutoCAD.EditorInput;
using Autodesk.AutoCAD.Geometry;
using Autodesk.AutoCAD.Windows;

using Autodesk.AutoCAD.GraphicsSystem;
using Autodesk.AutoCAD.GraphicsInterface;

using MgdAcApplication = Autodesk.AutoCAD.ApplicationServices.Application;
using MgdAcDocument = Autodesk.AutoCAD.ApplicationServices.Document;
using AcWindowsNS = Autodesk.AutoCAD.Windows;

#endregion


namespace AcadNetAddinCS1
{
    public class CmdGroup1
    {
        [CommandMethod("CmdGroup1", "Command1", null, CommandFlags.Modal, null, "AcadNetAddinCS1", "Command1")]
        public void Command1_Method()
        {
            Database db = HostApplicationServices.WorkingDatabase;
            Editor ed = MgdAcApplication.DocumentManager.MdiActiveDocument.Editor;
            
            try
            {
                using (Transaction tr = db.TransactionManager.StartTransaction())
                {
                    //TODO: add your code below.    
                    Debug.WriteLine("Command1 ran.");
                    ed.WriteMessage("Command1 ran.\n");    


                    tr.Commit();
                }
            }
            catch (System.Exception ex)
            {
                Debug.WriteLine(ex.ToString());
                ed.WriteMessage(ex.ToString());
            }
        }
        [CommandMethod("drawLine")]
        public void Command1_drawLine()
        {
            Database db = HostApplicationServices.WorkingDatabase;
            Point3d startPt = new Point3d(0, 100, 0);
            Point3d endPt = new Point3d(100, 100, 0);
            Line line = new Line(startPt, endPt);
            using (Transaction trans = db.TransactionManager.StartTransaction())
            {
                try
                {
                    BlockTable bt = (BlockTable)trans.GetObject(db.BlockTableId, OpenMode.ForRead);
                    BlockTableRecord btr = (BlockTableRecord)trans.GetObject(bt[BlockTableRecord.ModelSpace], OpenMode.ForWrite);
                    btr.AppendEntity(line);
                    trans.AddNewlyCreatedDBObject(line, true);
                    trans.Commit();
                }
                catch (System.Exception ex)
                {
                    trans.Abort();
                }
            }
        }

    }
}
```

