---
title: "How to access and modify a DynamicBlockReference property in ARX and .Net?"
date: 2012-08-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - Block
  - C++
description: "My DynamicBlock has a "Visibility" property that can have two states. How can I access this property for an instance of this block and modify it?"
author: Autodesk
---
# How to access and modify a DynamicBlockReference property in ARX and .Net?

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/how-to-access-and-modify-a-dynamicblockreference-property-in-arx-and-net.html

## 文章内容

By Philippe Leefsma
Q:
My DynamicBlock has a "Visibility" property that can have two states. How can I access this property for an instance of this block and modify it?
A:
Run the following code using the attached drawing. Select the inserted dynamic block reference, it will access the Visibility property and change its state. You can see the result in the UI immediately after the code finishes.
void SetDynamicBlkProperty()
{
 ads_name ename;
 ads_point pt;
 if(acedEntSel(L"\nSelect a dynamic block reference: ", ename, pt) != RTNORM)
 {
  acutPrintf(L"\nError selecting entity.");
  return;
 }
   AcDbObjectId eId;
 acdbGetObjectId(eId, ename);
 AcDbEntity* pEnt = NULL;
   if (acdbOpenObject(pEnt, eId , AcDb::kForRead) != Acad::eOk)
 {
  acutPrintf(L"\nError opening entity.");
  if(pEnt)
    pEnt->close();
  return;
 }
   if(pEnt->isA() != AcDbBlockReference::desc())
 {
  acutPrintf(L"\nMust select a block insert.");
  pEnt->close();
  return;
 }
   AcDbBlockReference *pBlkRef = AcDbBlockReference::cast(pEnt);
   // initialise a AcDbDynBlockReference from the object id of the blockreference
 AcDbDynBlockReference* pDynBlkRef = new AcDbDynBlockReference(pBlkRef->objectId());
   //Don't forget to close the blockreference here,
 //otherwise you wont be able to modify properties
 pEnt->close();
   if (pDynBlkRef)
 {
  AcDbDynBlockReferencePropertyArray blkPropAry;
  pDynBlkRef->getBlockProperties(blkPropAry);
    Acad::ErrorStatus err;
  AcDbDynBlockReferenceProperty blkProp;
    for(long lIndex1=0L ; lIndex1<blkPropAry.length() ; ++lIndex1)
  {
   blkProp = blkPropAry[lIndex1];
     //look for the relevant property
   if (wcscmp(blkProp.propertyName().kACharPtr(), L"Visibility") != 0) continue;
     //Get allowed values for property
   AcDbEvalVariantArray evalAry;
     if ((err = blkProp.getAllowedValues(evalAry)) == Acad::eOk )
   {
    if( evalAry.length() >= 1)
    {
     AcDbEvalVariant eval = evalAry[1];
       if(!blkProp.readOnly())
     {
      if((err = blkProp.setValue(eval)) != Acad::eOk)
      {
       acutPrintf(L"\nError setting property value...");
      }
     }
    }
   }
  }
    //Don't forget to delete this reference, otherwise you will have problems.
  delete pDynBlkRef;
 }
}
  Here is the C# version:
[CommandMethod("SetDynamicBlkProperty")]
static public void SetDynamicBlkProperty()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      PromptEntityOptions prEntOptions = new PromptEntityOptions(
        "Select a dynamic block reference...");
      PromptEntityResult prEntResult = ed.GetEntity(prEntOptions);
      if (prEntResult.Status != PromptStatus.OK)
    {
        ed.WriteMessage("Error...");
        return;
    }
      using(Transaction Tx = db.TransactionManager.StartTransaction())
    {
        BlockReference bref = Tx.GetObject(
            prEntResult.ObjectId,
            OpenMode.ForWrite)
                as BlockReference;
          if (bref.IsDynamicBlock)
        {
            DynamicBlockReferencePropertyCollection props =
                bref.DynamicBlockReferencePropertyCollection;
              foreach (DynamicBlockReferenceProperty prop in props)
            {
                object[] values = prop.GetAllowedValues();
                  //Switch Property
                if (prop.PropertyName == "Visibility" && !prop.ReadOnly)
                {
                    if (prop.Value.ToString() == values[0].ToString())
                        prop.Value = values[1];
                      else
                        prop.Value = values[0];
                }
            }
        }
          Tx.Commit();
    }
}
  Rectangle.dwg

## 评论

**内容**: Chris said...
Is there a way to identify the type of a DynamicBlockReferenceProperty (Distance, Rotation, Visibility, ...) without knowing the name or other details?
Reply
08/14/2012 at 06:34 AM

---
**内容**: Khoa Ho said...
This is also my big concern about PropertyName of dynamic blocks, see the thread: http://forums.autodesk.com/t5/NET/Dynamic-block-parameters-types/td-p/3569558
Reply
08/14/2012 at 09:29 AM

---
**内容**: Márcio said...
I need to create a form to display the properties of a selected block, each on a combo box so the user can change these properties in this friendly interface. I used the login of the code of this article, but when my block properties are changed by this form the block is disfigured. In this case I'm changing a width parameter. If I change the parameter by AutoCAD palette the block is redrawn correctly. Does anyone have an idea what might be happening? Thanks.
Reply
01/09/2014 at 10:41 AM

---
**内容**: Philippe Leefsma said in reply to Márcio...
Hi Marcio, based on that description I can't tell you why... you should rather log a forum thread and provide the sample drawing with your block.
http://forums.autodesk.com/t5/AutoCAD-Customization/ct-p/AutoCADTopic1
Thank you.
Reply
01/10/2014 at 01:40 AM

---
**内容**: Philippe Leefsma said in reply to Márcio...
Hi Marcio, based on that description I can't tell you. You should rather log a new thread in the AutoCAD customization forum and provide a sample drawing with your block.
http://forums.autodesk.com/t5/AutoCAD-Customization/ct-p/AutoCADTopic1
Thank you
Reply
01/10/2014 at 01:42 AM

---
**内容**: John Keays Aus7024 ADN said...
I am selecting a block and then changing the block rotation property. I am having difficulty knowing which object I have selected. the object gets highlighted when selected. I get the rotation angle from the block and place the value in a modal dialog box. I can then change the text value of the rotation and then select the insert button to do the replacement of the block. If I select the wrong block I just hit a cancel button in the dialog box.
I have several options
(1) repaint the block in another colour
(2) Use some form of selection that will repaint the block as dotted or highlighted
(3) Add text or a temporary arrow pointing to the block
What is the best appr0ach and is there some samples that show how this is done.
Cheers
John keays
Reply
12/11/2015 at 05:09 AM

---
**内容**: Sri said...
is it possible to run this DWG file in Visual Studio 2015.
Reply
03/30/2017 at 03:25 AM

---
