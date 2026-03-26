---
title: "PipeInlineAsset orientation"
date: 2014-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "The pipe inline orientation can be accessed using XAxis and ZAxis properties. From the help file, we can read:"
author: Autodesk
---
# PipeInlineAsset orientation

发布日期: 2014-01-01

原始链接: https://adndevblog.typepad.com/autocad/2014/01/pipeinlineasset-orientation.html

## 文章内容

By Augusto Goncalves
The pipe inline orientation can be accessed using XAxis and ZAxis properties. From the help file, we can read:
xAxis: Input vector (in WCS) to be used to define the new plane that will contain the inline asset
zAxis: Input X-Direction vector (WCS) for the inline asset
And, as the properties are read-only, we can change them using the SetOrientation method.
Despite the explanation, a graphical visualization can help we understand the properties. After writing a small piece of code to change the properties, we can see the following:
XAxis: change the asset orientation regarding the flow on the pipe line, as shown on the image below.
ZAxis: rotate the asset along the pipe line axis, helping place it properly, as shown below.
If you need to change any of those directions, then notice that the vectors are unit vectors. Below is a sample code that changes both X and Z directions (just invert the values).
[CommandMethod("assetOrient")]
public void CmdAssetOrientation()
{
    Editor ed = Application.DocumentManager.
        MdiActiveDocument.Editor;
      PromptEntityOptions peo = new
        PromptEntityOptions("Select inline asset");
    peo.SetRejectMessage("Only inline asset");
    peo.AddAllowedClass(typeof(PipeInlineAsset), true);
    PromptEntityResult per = ed.GetEntity(peo);
    if (per.Status != PromptStatus.OK) return;
      Database db = Application.DocumentManager.
        MdiActiveDocument.Database;
    using (Transaction trans =
        db.TransactionManager.StartTransaction())
    {
        PipeInlineAsset pipeAsset =
            trans.GetObject(per.ObjectId, OpenMode.ForWrite)
            as PipeInlineAsset;
          // get current values
        Point3d position = pipeAsset.Position;
        Vector3d xDir = pipeAsset.XAxis;
        Vector3d zDir = pipeAsset.ZAxis;
          // change the direction the asset is comparing to the line
        // for instance, a valve will change rotate along the line
        Vector3d zDirInverted = zDir.Negate();
          // change the orientation of the asset
        // for instace, a valve will change the in/out of the flow
        Vector3d xDirInverted = xDir.Negate();
          // apply the new value
        pipeAsset.SetOrientation(xDirInverted, zDirInverted);
          trans.Commit();
    }
}

## 评论

**内容**: Wjasonhudson@gmail.com said...
Thanks for the great write up. On most parts the code works but I get odd results when trying to change the orientation of olets. The olets always skew off the input vectors by 8-15 degrees. Is there a reliable way to change olet orientation?
Reply
01/13/2014 at 06:04 PM

---
**内容**: Augusto Goncalves said in reply to Wjasonhudson@gmail.com...
Hi,
Not sure if I'm following the idea. This sample rotates on the direction and along the direction of the part. Do you have more information or a sample? The best way it to post at http://forums.autodesk.com/t5/AutoCAD-Plant-3D/bd-p/371
Regards,
Augusto Goncalves
Reply
01/24/2014 at 07:37 AM

---
**内容**: Jason said in reply to Augusto Goncalves...
Thanks, I've found that olets behave a bit different from other parts but it is possible to insert them correctly.
Reply
01/29/2014 at 07:35 PM

---
