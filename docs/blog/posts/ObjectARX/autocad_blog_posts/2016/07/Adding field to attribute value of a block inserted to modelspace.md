---
title: "Adding field to attribute value of a block inserted to modelspace"
date: 2016-07-01
categories:
  - AutoCAD .NET
tags:
  - Block
  - C#
  - Database
  - Plugin
description: "Here is a blog by Stephen Preston which explains inserting a block with attributes."
author: Autodesk
---
# Adding field to attribute value of a block inserted to modelspace

发布日期: 2016-07-01

原始链接: https://adndevblog.typepad.com/autocad/2016/07/adding-field-to-attribute-value-of-a-block-inserted-to-modelspace.html

## 文章内容

By Deepak Nadig
Here is a blog by Stephen Preston which explains inserting a block with attributes.
Below is a C# code to insert a field to the attribute value of a block. Create a drawing with a block named "test" containing a circle having an
attribute definition(tag to be assigned) to test the code.
  [CommandMethod("addFieldToAttribute")]
public void addFieldToAttribute()
{
    Database db = Application.DocumentManager.MdiActiveDocument.Database;
    Editor ed = Application.DocumentManager.MdiActiveDocument.Editor;
    string blkName = "test";
    using (Transaction acTrans = db.TransactionManager.StartTransaction())
    {
        BlockTable blkTbl = db.BlockTableId.GetObject(OpenMode.ForRead) as BlockTable;
        if (blkTbl.Has(blkName))
        {
            BlockTableRecord blkTblRec = blkTbl[blkName].GetObject(OpenMode.ForRead) 
                as BlockTableRecord;
            using (BlockReference blkRef = new BlockReference(Point3d.Origin, blkTblRec.ObjectId))
            {
                BlockTableRecord ms = blkTbl[BlockTableRecord.ModelSpace].GetObject(OpenMode.ForWrite) 
                    as BlockTableRecord;
                ms.AppendEntity(blkRef);
                acTrans.AddNewlyCreatedDBObject(blkRef, true);
                if (blkTblRec.HasAttributeDefinitions)
                {
                    Point3d cp = new Point3d(0, 0, 0);
                    Circle circ = new Circle();
                    ObjectId objID = new ObjectId();
                    foreach (ObjectId id in blkTblRec)
                    {
                        DBObject obj = id.GetObject(OpenMode.ForRead);
                        if ((obj) is Circle)
                        {
                            circ = (Circle)obj; // get the circle object
                            cp = circ.Center;
                            objID = circ.ObjectId;
                        }
                        if (obj is AttributeDefinition)
                        {
                            AttributeDefinition acAttDef = (AttributeDefinition)obj;
                            //Create a new AttributeReference
                            using (AttributeReference acAttRef = new AttributeReference())
                            {
                                acAttRef.SetAttributeFromBlock(acAttDef, blkRef.BlockTransform);
                                acAttRef.Position = acAttDef.Position.TransformBy(blkRef.BlockTransform);
                                acAttRef.TextString = acAttDef.TextString;
                                acAttRef.Tag = acAttDef.Tag;
                                //Add the AttributeReference to the BlockReference
                                blkRef.AttributeCollection.AppendAttribute(acAttRef);
                                //Assign the centerpoint of the circle to a field code string 
                                string str1 = "%<\\AcObjProp.16.2 Object(%<\\_ObjId ";
                                string strID = objID.OldIdPtr.ToString();
                                string str2 = ">%,1).Center \\f \"%lu2\">%";
                                string str = str1 + strID + str2;
                                string fldstr = string.Format(str, cp.ToString());
                                //crete a new field with field code parameter
                                Field field = new Field(fldstr);
                                field.Evaluate();
                                FieldEvaluationStatusResult fieldEval = field.EvaluationStatus;
                                if (fieldEval.Status != FieldEvaluationStatus.Success)
                                {
                                    acTrans.Abort();
                                    ed.WriteMessage(string.Format("FieldEvaluationStatus Message: {0} - {1}",
                                        fieldEval.Status, fieldEval.ErrorMessage));
                                    return;
                                }
                                else
                                {
                                    try
                                    {   //set the field to attribute reference 
                                        acAttRef.SetField(field);
                                        acTrans.AddNewlyCreatedDBObject(field, true);
                                        ed.WriteMessage(string.Format("Field value ({1}) is inseterd to Attribute '{0}' of the Block '{2}' ",
                                            acAttRef.Tag, field.Value, blkRef.Name));
                                    }
                                    catch
                                    {
                                        field.Dispose();
                                        ed.WriteMessage(string.Format("Failed to set attribute field '{0}' - {1}",
                                            acAttRef.Tag, acAttRef.Handle));
                                    }
                                }
                                acTrans.AddNewlyCreatedDBObject(acAttRef, true);
                            }
                        }
                    }
                }
            }
        }
        acTrans.Commit();
    }
}

## 评论

**内容**: Deepak Singh said...
Mr. Preston's code in this post has a bug in it:
Circle circ = new Circle();
After that, circ variable is assigned to result of call to Transaction.GetObject(), and new Circle entity is never disposed, leading to fatal error.
Reply
05/18/2017 at 04:09 AM

---
**内容**: Kelcyo said...
My field expression is defined by BlockPlaceHolder with "%<\AcObjProp.16.2 Object(?BlockRefId,1).InsertionPoint \f "%lu2%pt2%pr3">%", but it does not work when defined in the string
Reply
07/07/2023 at 07:30 AM

---
