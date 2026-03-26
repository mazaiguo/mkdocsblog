---
title: "How to show a block when positioning it, using C#?"
date: 2012-07-01
categories:
  - AutoCAD .NET
tags:
  - Block
  - C#
description: "I want to insert a block showing it while the mouse is being moved until the block is placed. How can I do it?"
author: Autodesk
---
# How to show a block when positioning it, using C#?

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/how-to-show-a-block-when-positioning-it-using-c.html

## 文章内容

By Marat Mirgaleev
Issue
I want to insert a block showing it while the mouse is being moved until the block is placed. How can I do it?
Solution
You need to create a DrawJig-derived class and override its Sampler() and WorldDraw() methods.
When the WorldDraw() method is called, create a BlockReference instance in memory and pass it to the WorldDraw.Geometry.Draw() method.
The C# sample code below demonstrates this approach.
There is a "BlockJig" command defined in the code. It assumes that there is a block named "TEST" in the current drawing.
When the command is run the block is being previewed. When the user clicks the left mouse button, a block insert will be created.
using Autodesk.AutoCAD.Geometry;
using Autodesk.AutoCAD.DatabaseServices;
using Autodesk.AutoCAD.ApplicationServices;
using Autodesk.AutoCAD.EditorInput;
using Autodesk.AutoCAD.Runtime;
    namespace MySamples
{
    public class BlockJigCmds
  {
      // Ask the user to place the block named "TEST", showing it
    //   during the dragging.
    // Make sure that a block with this name exists in the drawing.
    //===============================================================
    [CommandMethod("BlockJig")]
    static public void BlockJig()
    {
      Editor ed =
              Application.DocumentManager.MdiActiveDocument.Editor;
      Database db = ed.Document.Database;
      try
      {
        using (Transaction tr =
                           db.TransactionManager.StartTransaction())
        {
          // Find the "TEST" block in the current drawing
          BlockTable bt = (BlockTable)tr.GetObject(db.BlockTableId,
                                                   OpenMode.ForRead);
          BlockTableRecord block = (BlockTableRecord)tr.GetObject(
                                       bt["TEST"], OpenMode.ForRead);
            // Create the Jig and ask the user to place the block
          //----------------------------------------------------
          MyBlockJig blockJig = new MyBlockJig();
          Point3d point;
          PromptResult res = blockJig.DragMe( block.ObjectId,
                                              out point);
          if (res.Status == PromptStatus.OK)
          {
            // Now we need to do the usual steps to place
            //   the block insert at the position where the user
            //   did the click
            BlockTableRecord curSpace =
              (BlockTableRecord)tr.GetObject(
                               db.CurrentSpaceId, OpenMode.ForWrite);
            BlockReference insert = new BlockReference(point,
                                                     block.ObjectId);
            curSpace.AppendEntity(insert);
            tr.AddNewlyCreatedDBObject(insert, true);
          }
          tr.Commit();
        } // using
      }
      catch (System.Exception ex)
      {
        ed.WriteMessage(ex.ToString());
      }
    } // BlockJig()
    } // class BlockJigCmds
      // This Jig will show the given block during the dragging.
  //=================================================================
  public class MyBlockJig : DrawJig
  {
    public Point3d _point;
    private ObjectId _blockId = ObjectId.Null;
      // Shows the block until the user clicks a point.
    // The 1st parameter is the Id of the block definition.
    // The 2nd is the clicked point.
    //---------------------------------------------------------------
    public PromptResult DragMe(ObjectId i_blockId, out Point3d o_pnt)
    {
      _blockId = i_blockId;
      Editor ed =
              Application.DocumentManager.MdiActiveDocument.Editor;
        PromptResult jigRes = ed.Drag(this);
      o_pnt = _point;
      return jigRes;
    }
        // Need to override this method.
    // Updating the current position of the block.
    //--------------------------------------------------------------
    protected override SamplerStatus Sampler(JigPrompts prompts)
    {
      JigPromptPointOptions jigOpts = new JigPromptPointOptions();
      jigOpts.UserInputControls =
                          (UserInputControls.Accept3dCoordinates |
                           UserInputControls.NullResponseAccepted);
      jigOpts.Message = "Select a point:";
      PromptPointResult jigRes = prompts.AcquirePoint(jigOpts);
        Point3d pt = jigRes.Value;
      if (pt == _point)
        return SamplerStatus.NoChange;
        _point = pt;
      if (jigRes.Status == PromptStatus.OK)
        return SamplerStatus.OK;
        return SamplerStatus.Cancel;
    }
        // Need to override this method.
    // We are showing our block in its current position here.
    //--------------------------------------------------------------
    protected override bool WorldDraw(
                  Autodesk.AutoCAD.GraphicsInterface.WorldDraw draw)
    {
      BlockReference inMemoryBlockInsert =
                               new BlockReference(_point, _blockId);
      draw.Geometry.Draw(inMemoryBlockInsert);
        inMemoryBlockInsert.Dispose();
        return true;
    } // WorldDraw()
    } // class BlockJig
  } // namespace MySamples

## 评论

**内容**: Brendan Mallon said...
Marat,
This jig works brilliantly for blocks being placed into model space.
However, the 'preview' of a block does not appear when the block is destined for a layout.
I have a requirement for some blocks to be placed in paper space (layout specific legends, notes, 'stamps' etc).
I'm guessing that it's something to do with block content being in model space.
Is there a trick to getting the block drag preview to show up in Layout as well?
Kind regards
Brendan Mallon
Reply
04/29/2013 at 08:38 PM

---
**内容**: Ben said in reply to Brendan Mallon...
Hey Brendan
this works perfectly for me in the paper space.
forgive my impertinence: perhaps check you've got the right space in the code and have the paper space current when running the plug in?
rgds
Ben
Reply
12/03/2015 at 07:16 PM

---
**内容**: Ben said...
http://help.autodesk.com/view/ACD/2015/ENU/?guid=GUID-C3F3C736-40CF-44A0-9210-55F6A939B6F2
I searched for the world "Jig" in the .Net developers resources. Almost nothing came up Nada, Zero. there were three pages with the word 'jig' in them. i surely cannot be alone: any ideas on where some good documentation with jigs exist?
that would be very handy.
rgds
Ben
Reply
12/03/2015 at 07:17 PM

---
