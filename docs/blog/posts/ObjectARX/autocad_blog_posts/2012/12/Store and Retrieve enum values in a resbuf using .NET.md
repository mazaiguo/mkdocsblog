---
title: "Store and Retrieve enum values in a resbuf using .NET"
date: 2012-12-01
categories:
  - AutoCAD .NET
tags:
  - .NET
description: "If you store enum values in a resbuf as "ExtendedDataInteger16", then you may get an invalid cast exception if you try to cast the value stored in ..."
author: Autodesk
---
# Store and Retrieve enum values in a resbuf using .NET

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/store-and-retrieve-enum-values-in-a-resbuf-using-net.html

## 文章内容

By Balaji Ramamoorthy
If you store enum values in a resbuf as "ExtendedDataInteger16", then you may get an invalid cast exception if you try to cast the value stored in the resbuf back to the enum.
To overcome this error, you may store the value as an "ExtendedDataIneger32" or use the "Enum.ToObject" as shown in the code snippet :
public enum MyEnumType  
{  
    spring,    
    summer,  
    fall,  
    winter
};
  [CommandMethod("ADDXDATA")]
static public void AddXdata()
{
    Database db = HostApplicationServices.WorkingDatabase;
    Editor ed
        = Application.DocumentManager.MdiActiveDocument.Editor;
      // Prompt the user to select an entity
    PromptEntityResult per = ed.GetEntity("Pick entity ");
    if (per.Status != PromptStatus.OK)
        return;
      using(Transaction tr = db.TransactionManager.StartTransaction())
    {
        RegAppTable regTable
                = (RegAppTable)tr.GetObject(
                                                db.RegAppTableId,
                                                OpenMode.ForWrite,
                                                false
                                            );
          String appName = "ADSK";
        if (regTable.Has(appName) == false)
        {
            RegAppTableRecord app = new RegAppTableRecord();
            app.Name = appName;
            regTable.Add(app);
            tr.AddNewlyCreatedDBObject(app, true);
        }
          Entity ent = tr.GetObject(
                                    per.ObjectId,
                                    OpenMode.ForWrite
                                 ) as Entity;
          //ent.XData = new ResultBuffer(
        //    new TypedValue(1001, appName),
        //    new TypedValue((int)DxfCode.ExtendedDataInteger32, MyEnumType.winter));
          ent.XData = new ResultBuffer(
            new TypedValue(1001, appName),
            new TypedValue((int)DxfCode.ExtendedDataInteger16, MyEnumType.winter));
          tr.Commit();
    }
}
  [CommandMethod("READXDATA")]
static public void ReadXdata()
{
    Database db = HostApplicationServices.WorkingDatabase;
    Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
      // Prompt the user to select an entity
    PromptEntityResult per = ed.GetEntity("Pick entity ");
    if (per.Status != PromptStatus.OK)
        return;
      using(Transaction tr = db.TransactionManager.StartTransaction())
    {
        Entity ent
            = (Entity)tr.GetObject(per.ObjectId, OpenMode.ForWrite);
          using (ResultBuffer buf = ent.XData)
        {
            if (buf != null)
            {
                TypedValue[] tvArr = buf.AsArray();
                foreach (TypedValue tv in tvArr)
                {
                   if (tv.TypeCode == (int)DxfCode.ExtendedDataInteger16)
                    {
                        // Only works if the enum value in
                        // the Xdata was stored as ExtendedDataInteger32
                        //MyEnumType enumValue = (MyEnumType)tv.Value;
                          // Works in both the cases.
                        // if the enum value in the Xdata was
                        // stored as ExtendedDataInteger16
                        // or as ExtendedDataInteger32
                        MyEnumType enumValue
                            = (MyEnumType)Enum.ToObject(typeof(MyEnumType), tv.Value);
                          ed.WriteMessage("\n" + enumValue.ToString());
                    }
                }
            }
        }
        tr.Commit();
    }
}

