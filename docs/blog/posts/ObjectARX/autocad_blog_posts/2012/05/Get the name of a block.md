---
title: "Get the name of a block"
date: 2012-05-01
categories:
  - AutoCAD C++
tags:
  - Block
  - C++
  - ObjectARX
description: "Can I use ObjectARX to get the name of a block-reference inside an ObjectARX application? I know that I can do this by using adsentget, and then lo..."
author: Autodesk
---
# Get the name of a block

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/get-the-name-of-a-block.html

## 文章内容

By Xiaodong Liang
Issue
Can I use ObjectARX to get the name of a block-reference inside an ObjectARX application? I know that I can do this by using ads_entget, and then look at the corresponding Group Code.
Solution
There is no method on the block reference class that returns the name of the block definition. The block reference (class AcDbBlockReference) keeps an object ID of the used block definition object (class AcDbBlockTableRecord). The name of the block is stored by the block definition object. To get the block name, you have to obtain the object ID of the block definition and to open it. Then you can ask the block definition for the block name. The following code lets the user select a block reference and extracts the block name:
 void AsdkGetBlockName()
{
     // Let the user select an INSERT (Block reference).
     ads_name ename;
     ads_point pt;
       if (RTNORM != acedEntSel(L"\nSelect INSERT: ",
                             ename,
                            pt))
       return;
       AcDbObjectId objId;
     AcDbEntity *pEnt;
     AcDbBlockReference *pInsert;
     Acad::ErrorStatus es;
       // Test the entity type.
     acdbGetObjectId(objId, ename);
     if (Acad::eOk != (es = acdbOpenAcDbEntity(pEnt,
                            objId,
                            AcDb::kForRead)))
     {
       acutPrintf(L"\nCannot access selected entity.\n");
       return;
     }
       pInsert = AcDbBlockReference::cast(pEnt);
     if (!pInsert)
     {
       acutPrintf(L"\nSelected entity is not an INSERT.\n");
       pEnt->close();
       return;
     }
       // Get the objectID of the block definition.
     AcDbObjectId blockDefId = pInsert->blockTableRecord();
       // Close the selected INSERT.
     pInsert->close();
       // Open the block definition.
     AcDbBlockTableRecord *pBlkRecord;
     if (Acad::eOk != (es = acdbOpenObject(pBlkRecord,
                                    blockDefId,
    AcDb::kForRead)))
     {
       acutPrintf(L"\nCannot access block definition.\n");
       return;
     }
       // Get the name of the block definition.
     const TCHAR* pBlkName;
     es = pBlkRecord->getName(pBlkName);
     pBlkRecord->close();
     if ((Acad::eOk != es) || !pBlkName)
     {
       acutPrintf(L"\nCannot extract block definition name.\n");
       return;
     }
       acutPrintf(L"\nName of block definition: '%s'\n", pBlkName);
}

## 评论

**内容**: Eugene Rymski said...
I would add that the returned string should be freed by caller (or it's easier to use overload method with AcString as parameter).
Reply
05/30/2012 at 07:49 AM

---
**内容**: Owen Wengerd said in reply to Eugene Rymski...
Actually his code is correct. Notice that it is using the const ACHAR*& version of the getName() function.
Reply
05/30/2012 at 09:25 AM

---
**内容**: Eugene Rymski said in reply to Owen Wengerd...
@Owen: Oops... my bad, just did quick overview of the code. Thanks for the note!
@Xiaodong: feel free to delete my original comment as misleading.
Reply
05/30/2012 at 02:58 PM

---
**内容**: Account Deleted said...
//
// Print name of selected block (dynamic or static)
//
static void PrintBlockName(void)
{
ads_name en; ads_point p;
if (acedEntSel(_T("\nSelect block reference: "),en,p) == RTNORM) {
AcDbObjectId eId; acdbGetObjectId(eId,en);
AcDbObjectPointer pBlkRef(eId,AcDb::kForRead);
if (pBlkRef.openStatus() == Acad::eOk) {
AcDbObjectId idBlkTblRec = pBlkRef->blockTableRecord();
AcDbDynBlockReference dynBlk(eId);
if (dynBlk.isDynamicBlock()) {
AcDbBlockTableRecordPointer pBTR(dynBlk.dynamicBlockTableRecord(),AcDb::kForRead);
if (pBTR.openStatus() == Acad::eOk){
const ACHAR *blkName = NULL; pBTR->getName(blkName);
acutPrintf(_T("\nDynamic block with name: \"%s\""), blkName);
}
} else {
AcDbBlockTableRecordPointer pBTR(pBlkRef->blockTableRecord(),AcDb::kForRead);
const ACHAR *blkName = NULL; pBTR->getName(blkName);
acutPrintf(_T("\nStatic block with name: \"%s\""), blkName);
}
}
}
}
Reply
05/30/2012 at 01:33 PM

---
