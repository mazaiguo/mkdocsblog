---
title: "Add new attributes to a block using ObjectARX"
date: 2012-05-01
categories:
  - AutoCAD C++
tags:
  - Block
  - C++
  - ObjectARX
description: "The first you need to know is: in AutoCAD, block definitions are AcDbBlockTableRecords, just as are "MODELSPACE" and "PAPERSPACE" AcDbBlockTableRec..."
author: Autodesk
---
# Add new attributes to a block using ObjectARX

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/how-to-add-new-attributes-to-a-block-using-objectarx.html

## 文章内容

By Xiaodong Liang
The first you need to know is: in AutoCAD, block definitions are AcDbBlockTableRecords, just as are "*MODEL_SPACE" and "*PAPER_SPACE" AcDbBlockTableRecords. The Block definition(AcDbBlockTableRecord), as the ACDB_MODEL_SPACE/ACDB_PAPER_SPACE records, have entities associated with them. A Block definition typically has entities and AcDbAttributeDefinition's associated with it. To add a new attribute to the block definition, it is a matter of adding another AcDbAttributeDefinition to the AcDbBlockTableRecord in which you are interested.
The first code below adds one AcDbAttributeDefinition to one AcDbBlockTableRecord. It assumes a drawing is opened and there is one block named “Test” in the drawing.
void AddNewAtt()
{
    AcDbDatabase *pCurDb;
    AcDbBlockTable* pBlkTbl;
    AcDbBlockTableRecord* pBlkRec;
    AcDbObjectId attId;
    Acad::ErrorStatus es;
      AcDbAttributeDefinition* pAttDef;
   // location of the AttributeDefinition in the
   // block definition
    AcGePoint3d attLoc(1.2, -0.5, 0);
     // specify the text,tag and prompt
    ACHAR text[] = {L"NEW VALUE ADDED"};
    ACHAR tag[] = {L"MYTAG"};
    ACHAR prompt[] = {L"Enter a new value"};
          pCurDb =
       acdbHostApplicationServices()->workingDatabase();
      es =
       pCurDb->getBlockTable(pBlkTbl, AcDb::kForRead);
      if(!pBlkTbl->has(L"TEST"))
    {
        acutPrintf(L"\nBlock definition TEST does not
                    exist");
        pBlkTbl->close();
        return;
    }
      es = pBlkTbl->getAt(L"TEST", pBlkRec, AcDb::kForWrite);
    // create a AttributeDefinition
    pAttDef = new AcDbAttributeDefinition(attLoc, text,
                                           tag, prompt);
      // append the AttributeDefinition to the definition
    es = pBlkRec->appendAcDbEntity(attId, pAttDef);
      pAttDef->close();
    pBlkRec->close();
    pBlkTbl->close();
}
  Now, the block definition is modified. If you insert a new block (block reference), you will be asked to provide the value for the attribute. But the previous blocks have not attribute values, yet. To set their values, you could get all blocks which are defined by the block definition, open the them and update the attributes.
void UpdateATT()
{
   AcDbDatabase *pCurDb =
       acdbHostApplicationServices()->workingDatabase(); 
   AcDbBlockTable* pBlkTbl; 
   Acad::ErrorStatus es =
         pCurDb->getBlockTable(pBlkTbl, AcDb::kForRead);
     // if the block definition exists
   if(!pBlkTbl->has(L"TEST"))
   {
        acutPrintf(L"\nBlock definition TEST does not exist");
        pBlkTbl->close();
        return;
   }
     AcDbBlockTableRecord *pBlkRec; 
   // open the block definition
   es = pBlkTbl->getAt(L"TEST", pBlkRec, AcDb::kForWrite);
   if(es != Acad::eOk)
   {
       acutPrintf(L"\nBlock definition TEST does not exist");      
        pBlkTbl->close();
        return;
   }
     // get the blocks (block references)
   // which use the block definition
      AcDbObjectIdArray ids;
    pBlkRec->getBlockReferenceIds(ids);
      pBlkRec->close();
    pBlkTbl->close();
      // iterate each block
      for(int i=0;i<ids.length();i++)
    {
         AcDbObject *pObj;
         AcDbObjectId id = ids[i];
           es = acdbOpenObject(pObj,id,AcDb::
             OpenMode::kForWrite);
         if(es != Acad::eOk)
           continue;
           AcDbBlockReference *pBlkRef =
             AcDbBlockReference::cast(pObj);
         if(pBlkRef == NULL)
           continue;
           // get attributes Iterator
         AcDbObjectIterator *pAttribIter;
         // Step through the attributes and check to see
         // if the attribute 'TAG3' already exists
        pAttribIter = pBlkRef->attributeIterator();
          for(pAttribIter->start();
            !pAttribIter->done();
            pAttribIter->step())
        {
             AcDbObjectId blkRefAttId =
                 pAttribIter->objectId();
             AcDbAttribute *pBlkRefAtt;
             es = pBlkRef->openAttribute(pBlkRefAtt,
                 blkRefAttId,
                 AcDb::kForWrite);
               ACHAR  *pAttTag =
                 pBlkRefAtt->tag();
               if(_tcscmp(pAttTag, L"MYTAG") == 0)
            {
                // update the attribute value
                 pBlkRefAtt->setTextString(L"My Value");
            }
               free(pAttTag);
            pBlkRefAtt->close();
        }
          delete pAttribIter;
        pBlkRef->close(); 
      }
}

## 评论

**内容**: pouria said...
Hi Xiaodong,
Thanks a lot for your code here. I am really a beginner and I need to do the same thing as here, adding new attribute to an existing block. my problem is I dont know the parts that you have summarized in your code, like AcDbDatabase *pCurDb;
AcDbBlockTable* pBlkTbl;
AcDbBlockTableRecord* pBlkRec;
AcDbObjectId attId;
Acad::ErrorStatus es;
can you please write the complete code
Thanks
Pouria
Reply
04/30/2013 at 01:42 AM

---
**内容**: Jo said...
How do I change the "Prompt" tab in the block attributes?
Reply
03/24/2014 at 01:58 PM

---
