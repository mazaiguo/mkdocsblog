---
title: AutoCAD.net Mleader jig
date: 2025-09-18
categories:
  - windows程序
tags:
  - ObjectARX.net
  - AutoCAD
  - Csharp
  - Jig
  - MLeader
description: 在AutoCAD.net中实现MLeader夹具(Jig)的完整代码示例，支持动态拖拽和方向控制
authors:
  - JerryMa
---

# AutoCAD.net Mleader jig

```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using ZwSoft.ZwCAD.DatabaseServices;
using ZwSoft.ZwCAD.EditorInput;
using ZwSoft.ZwCAD.Geometry;
using ZwSoft.ZwCAD.Runtime;

namespace LeaderPlacement
{
    public class LeaderCmds
    {
        class DirectionalLeaderJig : EntityJig
        {
            private Point3d _start, _end;
            private string _contents;
            private int _index;
            private int _lineIndex;
            private bool _started;
            public DirectionalLeaderJig(string txt, Point3d start, MLeader ld) : base(ld)
            {
                // Store info that's passed in, but don't init the MLeader
                _contents = txt;
                _start = start;
                _end = start;
                _started = false;
            }
            // A fairly standard Sampler function
            protected override SamplerStatus Sampler(JigPrompts prompts)
            {
                var po = new JigPromptPointOptions();
                po.UserInputControls =
                  (UserInputControls.Accept3dCoordinates |
                   UserInputControls.NoNegativeResponseAccepted);
                po.Message = "\nEnd point";
                var res = prompts.AcquirePoint(po);
                if (_end == res.Value)
                {
                    return SamplerStatus.NoChange;
                }
                else if (res.Status == PromptStatus.OK)
                {
                    _end = res.Value;
                    return SamplerStatus.OK;
                }
                return SamplerStatus.Cancel;
            }
            protected override bool Update()
            {
                var ml = (MLeader)Entity;
                if (!_started)
                {
                    if (_start.DistanceTo(_end) > Tolerance.Global.EqualPoint)
                    {
                        // When the jig actually starts - and we have mouse movement -
                        // we create the MText and init the MLeader
                        ml.ContentType = ContentType.MTextContent;
                        var mt = new MText();
                        mt.Contents = _contents;
                        ml.MText = mt;
                        // Create the MLeader cluster and add a line to it
                        _index = ml.AddLeader();
                        _lineIndex = ml.AddLeaderLine(_index);
                        // Set the vertices on the line
                        ml.AddFirstVertex(_lineIndex, _start);
                        ml.AddLastVertex(_lineIndex, _end);
                        // Make sure we don't do this again
                        _started = true;
                    }
                }
                else
                {
                    // We only make the MLeader visible on the second time through
                    // (this also helps avoid some strange geometry flicker)
                    ml.Visible = true;
                    // We already have a line, so just set its last vertex
                    ml.SetLastVertex(_lineIndex, _end);
                }
                if (_started)
                {
                    // Set the direction of the text to depend on the X of the end-point
                    // (i.e. is if to the left or right of the start-point?)
                    var dl = new Vector3d((_end.X >= _start.X ? 1 : -1), 0, 0);
                    ml.SetDogleg(_index, dl);
                }
                return true;
            }
        }

        [CommandMethod("DL")]
        public void DirectionalLeader()
        {
            var doc = ZwSoft.ZwCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument;
            var ed = doc.Editor;
            var db = doc.Database;
            // Ask the user for the string and the start point of the leader
            var pso = new PromptStringOptions("\nEnter text");
            pso.AllowSpaces = true;
            var pr = ed.GetString(pso);
            if (pr.Status != PromptStatus.OK)
                return;
            var ppr = ed.GetPoint("\nStart point of leader");
            if (ppr.Status != PromptStatus.OK)
                return;
            // Start a transaction, as we'll be jigging a db-resident object
            using (var tr = db.TransactionManager.StartTransaction())
            {
                var bt =
                  (BlockTable)tr.GetObject(db.BlockTableId, OpenMode.ForRead, false);
                var btr =
                  (BlockTableRecord)tr.GetObject(db.CurrentSpaceId, OpenMode.ForWrite, false);
                // Create and pass in an invisible MLeader
                // This helps avoid flickering when we start the jig
                var ml = new MLeader();
                ml.Visible = false;
                // Create jig
                var jig = new DirectionalLeaderJig(pr.StringResult, ppr.Value, ml);
                // Add the MLeader to the drawing: this allows it to be displayed
                btr.AppendEntity(ml);
                tr.AddNewlyCreatedDBObject(ml, true);
                // Set end point in the jig
                var res = ed.Drag(jig);
                // If all is well, commit
                if (res.Status == PromptStatus.OK)
                {
                    tr.Commit();
                }
            }
        }
    }
}

```

