---
title: "Creating a splined leader using a Jig"
date: 2014-04-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "Here is a sample code to create a splined leader using an EntityJig. This is a modified version of the sample code from this post in Kean's blog."
author: Autodesk
---
# Creating a splined leader using a Jig

发布日期: 2014-04-01

原始链接: https://adndevblog.typepad.com/autocad/2014/04/creating-a-splined-leader-using-a-jig.html

## 文章内容

By Balaji Ramamoorthy
Here is a sample code to create a splined leader using an EntityJig. This is a modified version of the sample code from this post in Kean's blog.
public class SplinedLeaderJig : EntityJig
{
    Point3dCollection _mPts;
    Point3d _mTempPoint;
    public static bool _mIsJigStarted;
      public SplinedLeaderJig()
        : base(new Leader())
    {
        _mPts = new Point3dCollection();
          Leader leader = Entity as Leader;
        leader.SetDatabaseDefaults();
          _mIsJigStarted = false;
          leader.IsSplined = true;
    }
      protected override SamplerStatus Sampler(JigPrompts prompts)
    {
        Editor ed
       = Application.DocumentManager.MdiActiveDocument.Editor;
          JigPromptPointOptions opts = new JigPromptPointOptions();
          opts.UserInputControls = (
            UserInputControls.Accept3dCoordinates |
            UserInputControls.NoNegativeResponseAccepted |
            UserInputControls.NullResponseAccepted);
          if (_mPts.Count >= 1)
        {
            opts.BasePoint = _mPts[_mPts.Count - 1];
            opts.UseBasePoint = true;
        }
          opts.Message = "\nSpecify leader vertex: ";
          PromptPointResult res = prompts.AcquirePoint(opts);
        if (_mTempPoint == res.Value)
        {
            return SamplerStatus.NoChange;
        }
        else if (res.Status == PromptStatus.OK)
        {
            _mTempPoint = res.Value;
            return SamplerStatus.OK;
        }
        return SamplerStatus.Cancel;
    }
      protected override bool Update()
    {
        try
        {
            Leader leader = Entity as Leader;
              Editor ed
                = Application.DocumentManager.MdiActiveDocument.Editor;
            if (_mIsJigStarted)
            {
                // Remove the last vertex since we are only jigging
                leader.RemoveLastVertex();
            }
              Point3d lastVertex
                    = leader.VertexAt(leader.NumVertices - 1);
            if (!_mTempPoint.Equals(lastVertex))
            {
                // Temporarily append the acquired point as a vertex
                leader.AppendVertex(_mTempPoint);
                _mIsJigStarted = true;
            }
        }
        catch (System.Exception ex)
        {
            Document doc
               = Application.DocumentManager.MdiActiveDocument;
            doc.Editor.WriteMessage("\nException: " + ex.Message);
            return false;
        }
        return true;
    }
      public void addVertex()
    {
        Leader leader = Entity as Leader;
          leader.AppendVertex(_mTempPoint);
          _mPts.Add(_mTempPoint);
    }
      public void removeLastVertex()
    {
        Leader leader = Entity as Leader;
        if (_mPts.Count >= 1)
        {
            leader.RemoveLastVertex();
        }
    }
      public Entity getEntity()
    {
        return Entity;
    }
      [CommandMethod("MYSL")]
    public static void MySplinedLeader()
    {
        Document doc
              = Application.DocumentManager.MdiActiveDocument;
        Editor ed = doc.Editor;
        Database db = doc.Database;
          SplinedLeaderJig jig = new SplinedLeaderJig();
          bool bSuccess = true;
        bool bComplete = false;
          while (bSuccess && !bComplete)
        {
            SplinedLeaderJig._mIsJigStarted = false;
              PromptResult dragres = ed.Drag(jig);
              bSuccess = (dragres.Status == PromptStatus.OK);
            if (bSuccess)
                jig.addVertex();
              bComplete = (dragres.Status == PromptStatus.None);
            if (bComplete)
            {
                jig.removeLastVertex();
            }
        }
          if (bComplete)
        {
            // Append entity to DB
            Transaction tr
                    = db.TransactionManager.StartTransaction();
            using (tr)
            {
                BlockTable bt = tr.GetObject(
                        db.BlockTableId, OpenMode.ForRead
                                              ) as BlockTable;
                BlockTableRecord ms =
                    bt[BlockTableRecord.ModelSpace].GetObject
                    (OpenMode.ForWrite) as BlockTableRecord;
                  ms.AppendEntity(jig.getEntity());
                tr.AddNewlyCreatedDBObject(jig.getEntity(),
                                            true);
                tr.Commit();
            }
        }
    }

