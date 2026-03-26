---
title: "Setting/Creating a named View with associated UCS"
date: 2013-03-01
categories:
  - AutoCAD .NET
tags:
  - C#
  - Database
  - UCS
description: "The following C# command will set an existing named view with associated UCS if it exists or create a new one and set it to the drawing extents:"
author: Autodesk
---
# Setting/Creating a named View with associated UCS

发布日期: 2013-03-01

原始链接: https://adndevblog.typepad.com/autocad/2013/03/settingcreating-a-named-view-with-associated-ucs.html

## 文章内容

By Philippe Leefsma
The following C# command will set an existing named view with associated UCS if it exists or create a new one and set it to the drawing extents:
[CommandMethod("SetNamedView")]
public void SetNamedView()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      PromptStringOptions pso = new PromptStringOptions("\nEnter view name: ");
    pso.AllowSpaces = true;
                PromptResult pr = ed.GetString(pso);
      if(pr.Status != PromptStatus.OK)
        return;
      using(Transaction Tx = db.TransactionManager.StartTransaction())
    {
        ViewTable vt = Tx.GetObject(db.ViewTableId, OpenMode.ForRead)
            as ViewTable;
          if(!vt.Has(pr.StringResult))
        {
            PromptKeywordOptions pko = new PromptKeywordOptions(
                "\nView does not exist, do you want to create it?");
              pko.AllowNone = false;
            pko.Keywords.Add("Yes");
            pko.Keywords.Add("No");
            pko.Keywords.Default = "Yes";
              PromptResult pkr = ed.GetKeywords(pko);
              if (pkr.Status != PromptStatus.OK || pkr.StringResult == "No")
                return;
              db.UpdateExt(true);
              ViewTableRecord newView = CreateViewWithExtents(
                db.Extmin,
                db.Extmax);
              newView.ViewDirection = new Vector3d(0, 0, 1);
              newView.Name = pr.StringResult;
              vt.UpgradeOpen();
              vt.Add(newView);
              Tx.AddNewlyCreatedDBObject(newView, true);
        }
          ViewTableRecord vtrToUse = Tx.GetObject(
          vt[pr.StringResult], OpenMode.ForRead)
            as ViewTableRecord;
          using (ViewTableRecord vtr = new ViewTableRecord())
        {
            vtr.CopyFrom(vtrToUse); 
            ed.SetCurrentView(vtr);
        }
          if (vtrToUse.IsUcsAssociatedToView)
        {
            UcsTable ucsTbl = Tx.GetObject(db.UcsTableId, OpenMode.ForRead)
                as UcsTable;
              if (ucsTbl.Has(vtrToUse.UcsName))
            {
                UcsTableRecord ucs = Tx.GetObject(
                    vtrToUse.UcsName, OpenMode.ForRead) as UcsTableRecord;
                  ViewportTableRecord vportTblRec = Tx.GetObject(
                  ed.ActiveViewportId, OpenMode.ForWrite)
                    as ViewportTableRecord;
                  // Display the UCS Icon at the origin of the current viewport
                vportTblRec.IconAtOrigin = true;
                vportTblRec.IconEnabled = true;
                  // Set the UCS current
                vportTblRec.SetUcs(ucs.ObjectId);
                doc.Editor.UpdateTiledViewportsFromDatabase();
            }
        }
          Tx.Commit();
    }
}
  ViewTableRecord CreateViewWithExtents(Point3d p1, Point3d p2)
{
    Point2d min2d = new Point2d(min(p1.X, p2.X), min(p1.Y, p2.Y));
    Point2d max2d = new Point2d(max(p1.X, p2.X), max(p1.Y, p2.Y));
      ViewTableRecord view = new ViewTableRecord();
      view.CenterPoint = min2d + (max2d - min2d) * 0.5;
     view.Height = max2d.Y - min2d.Y;
    view.Width = max2d.X - min2d.X;
      return view;
}
  private double min(double a, double b)
{
    return (a < b ? a : b);
}
  private double max(double a, double b)
{
    return (a > b ? a : b);
}

