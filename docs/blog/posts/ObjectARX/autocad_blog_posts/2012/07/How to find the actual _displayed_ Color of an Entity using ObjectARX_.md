---
title: "How to find the actual "displayed" Color of an Entity using ObjectARX?"
date: 2012-07-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - Block
  - C++
  - Layer
  - ObjectARX
description: "How do I know what the actual displayed color of an entity is? For example, I have an entity which has color ByBlock and this entity is nested bloc..."
author: Autodesk
---
# How to find the actual "displayed" Color of an Entity using ObjectARX?

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/how-to-find-the-actual-displayed-color-of-an-entity-using-objectarx.html

## 文章内容

By Philippe Leefsma
Q:
How do I know what the actual displayed color of an entity is? For example, I have an entity which has color ByBlock and this entity is nested block reference. I want to know what is the entity's final color is as it appears on the screen.
A:
You can determine the entity’s color by using the colorIndex() method. This method would return the AutoCAD color number of the entity. An entity’s color could also be either BYBLOCK or BYLAYER apart from the actual color values. If the entity has any of these two values for color then the color of the entity is dependent on the block reference’s color or the entity’s layer color as the case may be.
If the entity is in a block then, note that it is the block references (AcDbBlockReference objects) which have the color and this is the color with which entities will appear if they have the color BYBLOCK. For entities which are nested deep in block references the solution is to traverse through the AcDbBlockReference objects using the resbuf returned by the acedNEntSel() function. The function acedNEntSel will return the parent block reference which the actual selected entity is part of. It also returns all the parent block references if the original block reference is nested. If the selected entity has color BYBLOCK, you need to query the parent block references up the order till you find a block reference whose color is *not* BYBLOCK or it does not have any more parent(which means the block reference is in Model Space). The sample code below shows how to implement the above.
  int GetEntColor(const AcDbEntity* pEnt);
  void fGetColor()
{
    ads_point ptres;
      ads_point xformres[4];
      struct resbuf* refstkres;
      ads_name ent;
      if(acedNEntSel(NULL,ent,ptres,xformres,&refstkres) != RTNORM)
                return;
      AcDbObjectId mObjId;
    acdbGetObjectId(mObjId,ent);
      AcDbEntity *pEnt = NULL;
    if(Acad::eOk != acdbOpenObject(pEnt, mObjId, AcDb::kForRead))
        {
        //show error msg here
        return;
    }
      int nEntCol = GetEntColor(pEnt);
      // close the entity
    pEnt->close();
      // check if entities color is BYBLOCK and entity is nested
    if((0 == nEntCol) && (NULL != refstkres))
    {
        // if entity is in block reference then we
        // will have to do extra processing
        // keep traversing up the parent block references as long
        // as the color is BYBLOCK
        while(NULL != refstkres)
        {
            int nBlkRefCol;
              //open the block reference and get the color
            //check for the type of the entity
            mObjId.setFromOldId(refstkres->resval.rlong);
              if(Acad::eOk != acdbOpenObject(pEnt, mObjId, AcDb::kForRead))
                break;
                nBlkRefCol = GetEntColor(pEnt);
            pEnt->close();
              if(0 == nBlkRefCol)
            {
                 refstkres = refstkres->rbnext;
            }
            else
            {
                nEntCol = nBlkRefCol;
                break;
            }
        }
    }
      //clean up
    if(NULL != refstkres)
                acutRelRb(refstkres);
      if(-1 != nEntCol)
    {
        // if it is still zero, then it is BYBLOCK and
        // block reference is in MODEL SPACE
        // in this case entity color depends on the back ground color
        if(0 == nEntCol)
        {
          acutPrintf(
           L"\nEntity color is BYBLOCK and refers to MODEL SPACE",nEntCol);   
        }
        else
        {
            acutPrintf(L"\nColor: %d",nEntCol);
        }
    }
    else
    {
        acutPrintf(L"\nerror: Unable to get the color");
    }
}
  int GetEntColor(const AcDbEntity* pEnt)
{
    int nCol = -1;
      if (NULL != pEnt)
    {                 
        nCol=pEnt->colorIndex();                       
          if(nCol==256)
        { 
            //Entity color is BYLAYER, so get
            //color of entity layer
              AcDbLayerTableRecord *pLayerTableRecord=NULL;
              if (acdbOpenObject(
                pLayerTableRecord,
                pEnt->layerId(),
                AcDb::kForRead) == Acad::eOk)
            {       
                nCol=pLayerTableRecord->color().colorIndex();
                pLayerTableRecord->close();
            }                 
        }
    }
      return nCol;
}

## 评论

**内容**: Dale Bartlett said...
This is very helpful, thank you. Before I launch into another C++ > C# conversion, do you have C# code available? Regards, Dale
Reply
07/10/2012 at 09:34 PM

---
**内容**: Philippe Leefsma said...
This code should be straightforward to convert into C#.
Here is a C# version, but it isn't 100% equivalent:
void PrintColor(Color color)
{
Document doc = Application.DocumentManager.MdiActiveDocument;
Editor ed = doc.Editor;
switch (color.ColorMethod)
{
case ColorMethod.ByAci:
System.Drawing.Color clr = color.ColorValue;
ed.WriteMessage("\n[" +
clr.R.ToString() + ", " +
clr.R.ToString() + ", " +
clr.R.ToString() + "]");
break;
default:
break;
}
}
[CommandMethod("GetEntityColor")]
public void GetEntityColor()
{
Document doc = Application.DocumentManager.MdiActiveDocument;
Database db = doc.Database;
Editor ed = doc.Editor;
PromptEntityOptions peo = new PromptEntityOptions("\nSelect entity: ");
PromptEntityResult per = ed.GetEntity(peo);
if (per.Status != PromptStatus.OK)
return;
using (Transaction Tx = db.TransactionManager.StartTransaction())
{
Entity entity = Tx.GetObject(per.ObjectId, OpenMode.ForRead) as Entity;
switch (entity.Color.ColorMethod)
{
case ColorMethod.ByLayer:
LayerTableRecord ltr = Tx.GetObject(entity.LayerId, OpenMode.ForRead)
as LayerTableRecord;
PrintColor(ltr.Color);
break;
case ColorMethod.ByAci:
case ColorMethod.ByColor:
PrintColor(entity.Color);
break;
default:
break;
}
Tx.Commit();
}
}
Reply
07/11/2012 at 02:50 AM

---
**内容**: Dale Bartlett said...
Thank you Philippe, Dale
Reply
07/17/2012 at 05:46 AM

---
