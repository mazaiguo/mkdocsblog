---
title: "Run PlantPipeSupportConvert command using acedCmd"
date: 2013-10-01
categories:
  - Plant 3D
tags:
  - API
  - AutoCAD
  - C#
  - Database
  - Plant 3D
description: "There is not an API to convert an AutoCAD object to a Plant 3D pipe support like the PlantPipeSupportConvert command does. You can run the command ..."
author: Autodesk
---
# Run PlantPipeSupportConvert command using acedCmd

发布日期: 2013-10-01

原始链接: https://adndevblog.typepad.com/autocad/2013/10/run-plantpipesupportconvert-command-using-acedcmd.html

## 文章内容

By Wayne Brill
There is not an API to convert an AutoCAD object to a Plant 3D pipe support like the PlantPipeSupportConvert command does. You can run the command from your code however. This c# example creates a command that has the user select the pipe and an AutoCAD entity to be used as the support. The location of the support is the mid point of the selected pipe. The Plant 3D API is used to get the length of the pipe from the database and it is used to calculate the mid point. The PlantPipeSuportConvert command takes a point for the pipe. (It uses an an input point monitor to get the pipe at that point). 
  Download Plant_3D_PipeSupportConvert
Note: Put the Plant_3D_Test_wB.dll in the PLNT3D folder to avoid errors about missing references. (this issue has been reported to Plant 3D engineering)
C:\Program Files\Autodesk\AutoCAD 2014\PLNT3D
  Here is the command:
[CommandMethod("PipeSupConvert")]
public void myPlantPipeSuppportConvert()
{
    Document docDocument =
       AcadApp.DocumentManager.MdiActiveDocument;
    Database dbDatabase = docDocument.Database;
    Editor ed = docDocument.Editor;
    PromptEntityOptions pmtEntOpts =
        new PromptEntityOptions
("\nSelect a Pipe to connect to new Support : ");
    PromptEntityResult pmtEntRes =
                        ed.GetEntity(pmtEntOpts);
      if (pmtEntRes.Status == PromptStatus.OK)
    {
        Autodesk.AutoCAD.DatabaseServices.
            TransactionManager tmTranMan =
                  dbDatabase.TransactionManager;
        Transaction trans = null;
        ObjectId oidPipeId = pmtEntRes.ObjectId;
        try
        {
            Project currentProject =
                PlantApp.CurrentProject.
                         ProjectParts["Piping"];
            DataLinksManager dlm =
                currentProject.DataLinksManager;
            PnPDatabase pnpdb =
                           dlm.GetPnPDatabase();
              // will use this with acedCmd to
            // send the command
            ResultBuffer rb = new ResultBuffer();
              trans = tmTranMan.StartTransaction();
            Pipe supP3DPipe = trans.GetObject
           (oidPipeId, OpenMode.ForRead) as Pipe;
            if (supP3DPipe == null)
            {
                ed.WriteMessage
("\n   Selected entity is not a Plant 3D Pipe");
            }
            else
            {
                // Output the ObjectId of the
                //Pipe for check purposes
                //  ed.WriteMessage
 //("\n   ObjectId of the Pipe : {0}", oidPipeId);
                  // Get Matrix3d of the selected
                // pipe to extract its Xaxis
                Matrix3d suppM3D =
                        ((Entity)supP3DPipe).Ecs;
                  // Get the RowId of the Pipe in
                // the Plant 3D project database
                int iPipeRowId =
                    dlm.FindAcPpRowId(oidPipeId);
                  // Get the corresponding PnPRow
                // of the Pipe
                PnPRow ppRow =
                         pnpdb.GetRow(iPipeRowId);
                  // Get the insertion point of
                // the selected Pipe
                Point3d p3dPipePosition =
                    new Point3d(
            Convert.ToDouble(ppRow["Position X"]),
            Convert.ToDouble(ppRow["Position Y"]),
           Convert.ToDouble(ppRow["Position Z"]));
                  // Get the Pipe length from the
                // Plant 3D project database
                double dPipeLength =
               Convert.ToDouble(ppRow["Length"]);
                  // Get the position of the
                // middle of the selected Pipe
                Point3d p3dSupportInsertionPoint =
                    new Point3d(
                 p3dPipePosition.X + dPipeLength *
             suppM3D.CoordinateSystem3d.Xaxis.X / 2,
                 p3dPipePosition.Y + dPipeLength *
             suppM3D.CoordinateSystem3d.Xaxis.Y / 2,
                 p3dPipePosition.Z + dPipeLength *
            suppM3D.CoordinateSystem3d.Xaxis.Z / 2);
                  // Commit the transaction have
                // all the data now
                trans.Commit();
                  pmtEntOpts = new PromptEntityOptions
     ("\nSelect AutoCad entity to be converted : ");
                pmtEntRes = ed.GetEntity(pmtEntOpts);
                if (pmtEntRes.Status ==
                                    PromptStatus.OK)
                {
                      ObjectId oidEntityId =
                                 pmtEntRes.ObjectId;
                    // Add the command to the ResBuf
                    rb.Add(new TypedValue
                 (5005, "_PlantPipeSupportConvert"));
                      // Add the selected
                    // entity ObjectId
                    rb.Add(new TypedValue
                                (5006, oidEntityId));
                    // return on the command line
                    rb.Add(new TypedValue(5005, ""));
                      // mid point of the selected pipe
                    rb.Add(new TypedValue
                   (5009, p3dSupportInsertionPoint));
                      acedCmd(rb.UnmanagedObject);
                  }
            }
        }
        catch
        {
            if (trans != null)
            {
                trans.Abort();
                trans.Dispose();
            }
        }
    }
}

## 评论

**内容**: Colin Holloway said...
Hi Wayne,
I really like the procedure you have outlined here and I am trying to get it to work in Plant3D 2014. When it gets to the selection the insertion point for the newly created pipe support it says "Point must be on a pipe or piping component", and the only way I have been able to get it to work (unacceptably) is to switch the NEA Osnap on and zoom out so the width of the pipe is within the aperture.
Do you have an updated version of this code that runs successfully on Plant3D 2014?
Kind Regards,
Colin Holloway
Reply
11/25/2014 at 06:48 PM

---
**内容**: Wayne Brill said...
Hi Colin,
When I posted this example it was working. However I have seen the problem you mention in 2014 and did not find a work around for it. I just tried it in Plant 3D 2015 and it is working every time. I used acedCmdS. Can you try this in the 2015 version?

[DllImport("accore.dll", CharSet = CharSet.Ansi, CallingConvention = CallingConvention.Cdecl, EntryPoint = "acedCmdS")]
private static extern int acedCmdS(System.IntPtr vlist);
...
// acedCmd(rb.UnmanagedObject);
//Testing 2015 - not in blog post
acedCmdS(rb.UnmanagedObject);
In 2015 managed API you could use the Command method of the Editor instead of acedCmdS. This works in my tests in 2015.
ed.Command("_PlantPipeSupportConvert", oidEntityId, "", p3dSupportInsertionPoint);
Thanks,
Wayne
Reply
11/26/2014 at 10:32 AM

---
**内容**: Colin Holloway said...
Hi Wayne,
Thank you for your quick response! Unfortunately the company I work for only has Plant 3D 2014 deployed and they have no plans to upgrade at this time (when they do it will be to 2016).
I will have to find a different way to make this work, like getting the user to select the point manually.
Thanks again,
Colin
Reply
11/26/2014 at 02:29 PM

---
**内容**: Colin Holloway said...
Hi Wayne,
3.5 years later and we are back in the sample place!
The solution I came up with in 2014 was a LISP routine that creates the 3D Solids of the required supports and then runs
(command "_.PlantPipeSupportConvert" supss "" p1)
to create the support.
This worked well in Plant 3D 2016 as well (with a change to command-s). Now we are migrating to Plant 3D 2018 and this issue has reared its head again!
This method works for supports in the middle of a pipe run, but we use a thrust support that is mounted on an elbow and connects to the end of the adjacent pipe. In 2014 and 2016 I was able to use END osnap and the support would attach to the end of the pipe, but in 2018 this doesn't work.
Are you aware of any changes or tips to get a support to connect to the end of a pipe?
Here is a screen cap of what I was able to do in Plant 3D 2016: https://a360.co/2Ha5uUh
Reply
04/02/2018 at 08:34 PM

---
