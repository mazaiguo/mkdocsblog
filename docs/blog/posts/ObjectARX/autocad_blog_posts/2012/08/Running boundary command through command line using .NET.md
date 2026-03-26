---
title: "Running boundary command through command line using .NET"
date: 2012-08-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - COM
  - COM Interop
description: "Below code shows the procedure to run the boundary command through command line. Note, code uses ActiveX API SendCommand to run the command. To avo..."
author: Autodesk
---
# Running boundary command through command line using .NET

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/running-boundary-command-through-command-line-using-net.html

## 文章内容

By Virupaksha Aithal
Below code shows the procedure to run the boundary command through command line. Note, code uses ActiveX API SendCommand to run the command. To avoid the different interop’s issue, code uses late binding technique. Command is run in session mode, so that issued boundary command is run synchronously.
Also, refer blog on identifying the boundary using API here
static ObjectIdCollection collection = new ObjectIdCollection();
static string commandName = "";
  static bool IsCommandActive()
{
    String str = (String)Application.GetSystemVariable("CMDNAMES");
    if (String.Compare(commandName, str, true) != 0)
    {
        return true;
    }
    return false;
}
[CommandMethod("BoundaryCommandLine", CommandFlags.Session)]
static public void BoundaryCommandLine()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Editor ed = doc.Editor;
      PromptPointOptions options =
                    new PromptPointOptions("Pick a point");
    PromptPointResult result = ed.GetPoint(options);
    if (result.Status != PromptStatus.OK)
        return;
      double x = result.Value.X;
    double y = result.Value.Y;
      string strPt = x.ToString() + "," + y.ToString();
    //put the database
    Database db = doc.Database;
    collection.Clear();
      commandName = (String)Application.GetSystemVariable("CMDNAMES");
      db.ObjectAppended +=
                    new ObjectEventHandler(Database_ObjectAppended);
    //run the boundary command using ActiveX send command.
    object[] dataArry = new object[1];
    dataArry[0] = "-boundary " + strPt + "  ";
    doc.AcadDocument.GetType().InvokeMember("SendCommand",
                                        BindingFlags.InvokeMethod,
                                   null, doc.AcadDocument, dataArry);
    if (IsCommandActive() == true)
    {
        dataArry[0] = "Yes ";
        doc.AcadDocument.GetType().InvokeMember(
           "SendCommand",
           BindingFlags.InvokeMethod,
           null, doc.AcadDocument, dataArry
         );
    }
    db.ObjectAppended -=
                    new ObjectEventHandler(Database_ObjectAppended);
        using (DocumentLock lock1 = doc.LockDocument())
    {   
        using (Transaction ta =
                            db.TransactionManager.StartTransaction())
        {
            foreach (ObjectId id in collection)
            {
                if (id.IsErased == true)
                {
                    continue;
                }
                DBObject obj = ta.GetObject(id,
                                               OpenMode.ForRead);
                if (obj is
                      Autodesk.AutoCAD.DatabaseServices.Polyline)
                {
                    //
                    Autodesk.AutoCAD.DatabaseServices.Polyline pl
                   = (Autodesk.AutoCAD.DatabaseServices.Polyline)obj;
                    ed.WriteMessage("area is " +
                                          pl.Area.ToString() + "\n");
                }
                else if (obj is
                            Autodesk.AutoCAD.DatabaseServices.Region)
                {
                    Autodesk.AutoCAD.DatabaseServices.Region rg =
                       (Autodesk.AutoCAD.DatabaseServices.Region)obj;
                    ed.WriteMessage("area is "
                                    + rg.Area.ToString() + "\n");
                }
            }
            ta.Commit();
        }
    }
}
static void Database_ObjectAppended(object sender, ObjectEventArgs e)
{
    collection.Add(e.DBObject.ObjectId);
}

## 评论

**内容**: Jason Huffine said...
I've seen late binding for the AutoCAD COM API mentioned more than once in some of these blogs. Can explain more about these particular interop issues without late binding? I'm curious.
Reply
08/28/2012 at 06:11 AM

---
**内容**: Oleg said...
Hi, Virupaksha Aithal
I used another syntax in that case, say to get a centroid etc:

dataArry[0] = "_-boundary " + strPt + " _A _O _R ";
doc.AcadDocument.GetType().InvokeMember("SendCommand", BindingFlags.InvokeMethod, null, doc.AcadDocument, dataArry);
if (IsCommandActive() == true)
{
dataArry[0] = "\r ";
doc.AcadDocument.GetType().InvokeMember( "SendCommand", BindingFlags.InvokeMethod, null, doc.AcadDocument, dataArry );
}
Thanks for your work,
Regards,
Reply
08/28/2012 at 08:26 AM

---
**内容**: xanhnhnn280683@gmail.com said...
Welcome
Can convert C # to vb.net?, I moved without
Thank you
can you help me?, I need such a geometric area available, just pick a point in the image is calculated area.
Reply
12/19/2012 at 08:43 AM

---
**内容**: Madhukar Moogala said in reply to xanhnhnn280683@gmail.com...
There are a number of C# to VB.NET translators available - many of them free. I use this one - http://www.developerfusion.com/tools/convert/csharp-to-vb/ - simply because this was one of the first ones I found and it worked well enough that I didn't feel the need to look elsewhere.
Reply
12/19/2012 at 11:28 AM

---
