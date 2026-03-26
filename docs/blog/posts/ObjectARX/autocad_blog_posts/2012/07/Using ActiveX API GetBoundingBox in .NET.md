---
title: "Using ActiveX API GetBoundingBox in .NET"
date: 2012-07-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - AutoCAD
  - COM
  - Database
description: "Below code shows the procedure to use activeX API GetBoundingBox in AutoCAD.NET. As GetBoundingBox returns the points, we need to "InvokeMember" me..."
author: Autodesk
---
# Using ActiveX API GetBoundingBox in .NET

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/using-activex-api-getboundingbox-in-net.html

## 文章内容

By Virupaksha Aithal
Below code shows the procedure to use activeX API GetBoundingBox in AutoCAD.NET. As GetBoundingBox returns the points, we need to "InvokeMember" member with "ParameterModifier" parameters.
[CommandMethod("GetBoundingBox")]
static public void GetBoundingBox()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      PromptEntityOptions options =
          new PromptEntityOptions("\nSelect an entity");
      PromptEntityResult acSSPrompt = ed.GetEntity(options);
    if (acSSPrompt.Status != PromptStatus.OK)
    return;
    // obtain transaction manager
    using (Transaction Tx = db.TransactionManager.StartTransaction())
    {
        Entity text = Tx.GetObject(acSSPrompt.ObjectId,
                                         OpenMode.ForRead) as Entity;
          object oAcadObjpl1 = text.AcadObject;
          object[] argspl1 = new object[2];
        argspl1[0] = new VariantWrapper(0);
        argspl1[1] = new VariantWrapper(0);
        ParameterModifier pmpl1 = new ParameterModifier(2);
        pmpl1[0] = true;
        pmpl1[1] = true;
          ParameterModifier[] modifierspl1 =
            new ParameterModifier[] { pmpl1 };
        oAcadObjpl1.GetType().InvokeMember("GetBoundingBox",
               BindingFlags.InvokeMethod, null, oAcadObjpl1, argspl1,
               modifierspl1, null, null);
        Point3d pt1 =
            new Point3d((double[])argspl1[0]);
        Point3d pt2 =
            new Point3d((double[])argspl1[1]);
        ed.WriteMessage("\n");
        ed.WriteMessage(pt1.X + "," + pt1.Y + "," + pt1.Z + "\n");
        ed.WriteMessage(pt2.X + "," + pt2.Y + "," + pt2.Z + "\n");
          Tx.Commit();
    }
}

## 评论

**内容**: BJHuffine said...
I understand that the VariantWrapper class is creating a COM Variant ByRef data type to supply the COM object GetBoundingBox method. But I don't understand what the ParamterModifier[] is doing? It looks like it's supplying the Type.InvokeMember() method with an array of a list type class. But why did you set it with two items? Why are both values true? Why does it have to be supplied at all?
Reply
07/31/2012 at 05:42 AM

---
**内容**: Virupaksha Aithal said in reply to BJHuffine...
For details on ParamterModifier please refer http://msdn.microsoft.com/en-us/library/system.reflection.parametermodifier.aspx and http://msdn.microsoft.com/en-us/library/de3dhzwy.aspx
Thanks
Viru
Reply
08/02/2012 at 01:46 AM

---
**内容**: NY said...
If the purpose of this post is purely to show how to make late-binding call to COM API, it would be better to use a more appropriate tile, so beginners are not misled to think this is the way to get entity's extent size/BoundingBox, because one has already had an entity open in transaction, Entity.GeometricExtents is the all code one need to write, why bother with COM API and late-binding?
Reply
07/31/2012 at 11:02 AM

---
