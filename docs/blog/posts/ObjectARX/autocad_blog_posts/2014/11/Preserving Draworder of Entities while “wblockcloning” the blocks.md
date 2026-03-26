---
title: "Preserving Draworder of Entities while “wblockcloning” the blocks"
date: 2014-11-01
categories:
  - AutoCAD C++
tags:
  - API
  - Block
  - C++
description: "The WblockClone API doesn’t guarantee draw order when Blocks are cloned ,wblockclone is very low level function ,it does only copying of entities ,..."
author: Autodesk
---
# Preserving Draworder of Entities while “wblockcloning” the blocks

发布日期: 2014-11-01

原始链接: https://adndevblog.typepad.com/autocad/2014/11/preserving-draworder-of-entities-while-wblockcloning-the-blocks.html

## 文章内容

By Madhukar Moogala
The WblockClone API doesn’t guarantee draw order when Blocks are cloned ,wblockclone is very low level function ,it does only copying of entities ,the high-level functionality likes preserving draw order should be explicitly implement by application developer.
  The above screenshots display correct and incorrect draw orders when wblock clone is perform ,to preserve order same a source block ,we need to use drawordertable API to sort entities as per source block.
C++ Code :
static void ADSKMyGroupWTEST()
{
Acad::ErrorStatus es;
TCHAR fullpath[_MAX_PATH];
  int ret = acedFindFile(_T("C:\\VESSELBLOCKS.dwg"),
                       fullpath );
if ( ret != RTNORM )
return;
  AcDbDatabase *pSrcDb = new AcDbDatabase( false, false );
es = pSrcDb->readDwgFile( fullpath, _SH_DENYNO );
if ( es != Acad::eOk )
{
acutPrintf( _T("\nCan not open file.") );
delete pSrcDb;
return;
}
  AcApDocument *pActiveDoc
    = acDocManager->mdiActiveDocument();
AcDbDatabase *pDestDb
    = pActiveDoc->database();
  AcDbObjectIdArray objIds2Copy;
AcDbBlockTable *pBlockTable,*pBlockTable2;
  es = pSrcDb->getSymbolTable(pBlockTable, AcDb::kForRead);
AcDbObjectId recordId = AcDbObjectId::kNull;
  es = pBlockTable->getAt(ACRX_T("CP_STERN_SY"), recordId, AcDb::kForRead);
objIds2Copy.append(recordId);
  es = pBlockTable->close();
  AcDbIdMapping idMap;
es = pSrcDb->wblockCloneObjects(objIds2Copy,
                  acdbSymUtil()->blockModelSpaceId(pDestDb),
                  idMap, AcDb::kDrcReplace);
    if(es == Acad::eOk)
{
  acutPrintf( _T("\nCloned the block to the current drawing.") );
AcDbObjectId targetBlockId = AcDbObjectId::kNull;
es = pDestDb->getSymbolTable(pBlockTable2, AcDb::kForRead);
es = pBlockTable2->getAt(ACRX_T("CP_STERN_SY"),
                         targetBlockId,
                         AcDb::kForRead);
SetBlockDrawOrder(recordId,targetBlockId,idMap);
es = pBlockTable2->close();
}
else
acutPrintf( _T("\nFailed to clone the block to the current drawing.") );
  delete pSrcDb;
  }
  static void SetBlockDrawOrder(AcDbObjectId srcBlockId,
                              AcDbObjectId targetBlockId,
                              AcDbIdMapping& idMap)
{
AcDbBlockTableRecord *pSrcBlock = NULL;
acdbOpenObject(pSrcBlock,
               srcBlockId,
               AcDb::kForRead);
AcDbSortentsTable *pSortTab1 = NULL;
pSrcBlock->getSortentsTable(pSortTab1,
                            AcDb::kForRead,
                            true);
AcDbObjectIdArray oids;
pSortTab1->getFullDrawOrder(oids);
pSortTab1->close();
pSrcBlock->close();
  AcDbBlockTableRecord *pTargetBlock = NULL;
acdbOpenObject(pTargetBlock,
               targetBlockId,
               AcDb::kForRead);
AcDbSortentsTable *pSortTab2 = NULL;
pTargetBlock->getSortentsTable(pSortTab2,
                               AcDb::kForWrite,
                               true);
AcDbObjectIdArray targetIds;
  int len = oids.length();
for(int cnt = 0; cnt < len; cnt++)
{
AcDbIdPair idPair(oids.at(cnt),
                  AcDbObjectId::kNull,
                  true);
if (idMap.compute (idPair))
targetIds.append(idPair.value());
}
pSortTab2->setRelativeDrawOrder(targetIds);
pSortTab2->close();
pTargetBlock->close();
}
.NET Code :
[CommandMethod("WTEST")]
public void MyWTEST()
{
string blockName = "CP_STERN_SY";
string pathDWG = "C:\\VESSELBLOCKS.dwg";
var doc = Application.DocumentManager.MdiActiveDocument;
using (Database OpenDb = new Database(false, false))
{
OpenDb.ReadDwgFile(pathDWG,
                   System.IO.FileShare.ReadWrite,
                   true, "");
ObjectIdCollection ids = new ObjectIdCollection();
BlockTable bt;
ObjectId sourceBlockId = ObjectId.Null;
using (Transaction tr =
    OpenDb.TransactionManager.StartTransaction())
{
  bt = (BlockTable)tr.GetObject(OpenDb.BlockTableId,
                    OpenMode.ForRead);
if (bt.Has(blockName))
{
ids.Add(bt[blockName]);
sourceBlockId = bt[blockName];
}
  if (ids.Count != 0)
{
Database destdb = doc.Database;
IdMapping iMap = new IdMapping();
OpenDb.WblockCloneObjects(ids,
destdb.BlockTableId,
iMap,
DuplicateRecordCloning.Replace,
false);
using (Transaction t =
    destdb.TransactionManager.StartTransaction())
{
ObjectId targetBlockId = ObjectId.Null;
BlockTable b = (BlockTable)t.GetObject(destdb.BlockTableId,
                                        OpenMode.ForRead);
if (b.Has(blockName))
{
targetBlockId = b[blockName];
}
  SetBlockDrawOrder(sourceBlockId, targetBlockId, iMap);
t.Commit();
  }
  }
tr.Commit();
  }
  }
  }
public void SetBlockDrawOrder(ObjectId sourceBlockId,
                               ObjectId targetBlockId,
                                IdMapping iMap)
{
  Database db = HostApplicationServices.WorkingDatabase;
using (Transaction t = db.TransactionManager.StartTransaction())
{
var sourceBTR =
    (BlockTableRecord)t.GetObject(sourceBlockId,
                                  OpenMode.ForRead);
var dotSource =
    (DrawOrderTable)t.GetObject(sourceBTR.DrawOrderTableId,
                                OpenMode.ForRead, true);
ObjectIdCollection srcDotIds = new ObjectIdCollection();
srcDotIds = dotSource.GetFullDrawOrder(0);
  var targetBTR =
    (BlockTableRecord)t.GetObject(targetBlockId,
                                   OpenMode.ForRead);
var dotTarget =
    (DrawOrderTable)t.GetObject(targetBTR.DrawOrderTableId,
                                OpenMode.ForWrite, true);
ObjectIdCollection trgDotIds = new ObjectIdCollection();
foreach (ObjectId oId in srcDotIds)
{
if (iMap.Contains(oId))
{
IdPair idPair = iMap.Lookup(oId);
trgDotIds.Add(idPair.Value);
}
}
dotTarget.SetRelativeDrawOrder(trgDotIds);
t.Commit();
}
}

## 评论

**内容**: Alain said...
Nice one, Thanks!
Reply
11/16/2014 at 11:12 PM

---
**内容**: Nick Gorlov said...
actually, this code does nothing useful at all. if i have a block with a broken draworder, this code can't fix it. using code (your or mine) i can (almost 5 years i can) insert this block with a correct draworder. but then, if autocad will copy this block (Ctrl+C/Ctrl+V) to the new drawing, draworder become broken again. that's the real situation. it was fixed in Autocad 2015 SP2. but earler versions will live with this bug forever and this code can't fix it. so, this code is just for fun :)
// your code
AcDbObjectId importBlockToCurDWGDatabase(const ACHAR *pBlockName /*block name*/, const ACHAR *pFileName /*full path to the file with this block*/)
{
Acad::ErrorStatus es=Acad::eOk;
AcDbObjectId idImported = AcDbObjectId::kNull; // output ID of our block in current database
AcDbDatabase* pWorkDatabase = acdbHostApplicationServices()->workingDatabase();
AcAxDocLock docLock(pWorkDatabase);
AcDbDatabase* pBlockDatabase = new AcDbDatabase(false,true);
es = pBlockDatabase->readDwgFile(pFileName);
if(es!=Acad::eOk){delete pBlockDatabase;return NULL;}

try
{
AcDbBlockTable* pBlockTable, *pBlockTable2;
es=pBlockDatabase->getSymbolTable(pBlockTable,AcDb::kForRead);
if(es!=Acad::eOk){delete pBlockDatabase;return NULL;}
AcDbObjectId idInsRecord;
es=pBlockTable->getAt(pBlockName,idInsRecord);
AcDbObjectIdArray objIds2Copy;
objIds2Copy.append(idInsRecord);
pBlockTable->close();
if(es!=Acad::eOk){delete pBlockDatabase;return NULL;}
AcDbIdMapping idMap;
es = pBlockDatabase->wblockCloneObjects(objIds2Copy,acdbSymUtil()->blockModelSpaceId(pWorkDatabase),idMap, AcDb::kDrcReplace);
if(es == Acad::eOk)
{
es = pWorkDatabase->getSymbolTable(pBlockTable2, AcDb::kForRead);
es = pBlockTable2->getAt(pBlockName,idImported,AcDb::kForRead);
SetBlockDrawOrder(idInsRecord,idImported,idMap);
es = pBlockTable2->close();
}
}catch(...){delete pBlockDatabase;return NULL;}
delete pBlockDatabase;
return idImported;
}
// my code
AcDbObjectId importBlockToCurDWGDatabase(const ACHAR *pBlockName /*block name*/, const ACHAR *pFileName /*full path to the file with this block*/)
{
Acad::ErrorStatus es=Acad::eOk;
AcDbObjectId idImported = AcDbObjectId::kNull; // output ID of our block in current database
AcDbDatabase* pWorkDatabase = acdbHostApplicationServices()->workingDatabase();
AcAxDocLock docLock(pWorkDatabase);
AcDbDatabase* pBlockDatabase = new AcDbDatabase(false,true);
es = pBlockDatabase->readDwgFile(pFileName);
if(es!=Acad::eOk){delete pBlockDatabase;return NULL;}

try
{
AcDbBlockTable* pBlockTable, *pBlockTable2;
es=pBlockDatabase->getSymbolTable(pBlockTable,AcDb::kForRead);
if(es!=Acad::eOk){delete pBlockDatabase;return NULL;}
AcDbObjectId idInsRecord;
es=pBlockTable->getAt(pBlockName,idInsRecord);
pBlockTable->close();
if(es!=Acad::eOk){delete pBlockDatabase;return NULL;}
AcDbDatabase* pTempDB;
es=pBlockDatabase->wblock(pTempDB,idInsRecord);
if(es!=Acad::eOk){delete pBlockDatabase;return NULL;}
es=pWorkDatabase->insert(idImported,pBlockName,pTempDB);
delete pTempDB;
if(es!=Acad::eOk){delete pBlockDatabase;return NULL;}
}catch(...){delete pBlockDatabase;return NULL;}
delete pBlockDatabase;
return idImported;
}
Reply
11/19/2014 at 01:33 AM

---
**内容**: Madhukar Moogala said in reply to Nick Gorlov...
Hi Nick,
Thanks for your reply ,
I'm not sure I've understood completely , my code is restore\preserve the draworder which the source block has , I'm setting order of target block relative to source block.
Can you share your sample DWG , I will investigate when I get time.
Reply
11/19/2014 at 03:24 AM

---
**内容**: Nick Gorlov said in reply to Madhukar Moogala...
ok. sure i can share one more dwg for you :)
https://yadi.sk/d/A1utxOQKcodWD
1. open the drawing
2. select blocks
3. Ctrl+C
4. create a new drawing
5. Ctrl+V these blocks into the new drawing
Try to do these steps in AutoCAD 2008-2014 (one of them. The results are the same) and in AutoCAD 2015+SP2. Feel the difference :)
Talking about the code. My and your code is able to insert these blocks with a correct draworder (mb it's just a visual effect and the draworder is still broken, but it works), but native autocad commands become able to do this just several months ago. And autodesk keeps silence about the reasons of this behavior. How it happens? Is it possible to fix my own blocks? I still got no answer from their side (topic was started in December, 2013 :):):) )
Reply
11/19/2014 at 04:51 AM

---
**内容**: Madhukar Moogala said in reply to Nick Gorlov...
Hi Nick,
I checked the Dwg ,it contains dynamic parameters , Acad Dynamic block api is very limited , I'm not sure will I be able to fix your problem, thanks for your dwg this will help in understanding more deeply.
Reply
11/19/2014 at 05:14 AM

---
**内容**: Nick Gorlov said in reply to Madhukar Moogala...
actually, the problem is not in dynamic parameters.
here are some static blocks :)
https://yadi.sk/d/Uug7VLqhcohNB
the common for of all of these blocks is the block editor command. all of them were modified in block editor window (if _bedit was used just for adding params everything works fine, but if i draw something inside _bedit, 100% block will have a broken draworder for copy/paste into a new drawing). so, in my mind the problem is in source code of this command, but there is no proofs. and somehow autocad 2015 is now able to draw a correct draworder for a block with a broken one :)
Reply
11/19/2014 at 05:31 AM

---
**内容**: Madhukar Moogala said in reply to Nick Gorlov...
Thanks Nick for further clarification , I will investigate and try to find the answer, if I find,will definitely put a comment here. :)
Reply
11/19/2014 at 05:36 AM

---
**内容**: Madhukar Moogala said in reply to Madhukar Moogala...
Hi Nick ,
I just integrated code and tested on one of your block in the dwg , it seems the draworder is getting restored ,using ctrl C\V ,draworder gets broken in acad 2014,but using above code ,order is same as source block ,you said it is just visual effect , I didn't understand that statement completely ,can you be please more specific, you can drop a email at madhukar.moogala@autodesk.com
Video Link :
https://screencast.autodesk.com/main/details/2b8db1fd-7256-49c5-8bb1-49f5f40f1f88
Reply
11/19/2014 at 05:48 AM

---
**内容**: Nick Gorlov said...
hm..., english is not my native language. "visual effect" was just a joke (looks like it was a bad joke :) ). sure the draworder must be correct if autocad draw the block correctly. your video doesn't show the most interesting part: what would be if you copy/paste this block into a new drawing.
that's why my first message was:"this code is just for fun", because we can do nothing to fix autocad native behavior. also i wrote that your and my code do the same (insert block correctly into a drawing database), but it's not enough for blocks with broken draworder (or mb draworder is correct from the beginning? :):):) and just paste into a new drawing can break it?).
i've found my old video for devhelp. it demonstrates an autocad native behavior in broken block creation :)
https://yadi.sk/d/J1omau3Xcpa2d
PS: may be it's possible to force the block to forget, that it was modified in block editor (mb class variables or something like this)? what is able to force autocad to kill correct draworder during copy/paste?
PS2: If you prefer to continue the conversation via e-mail, i can :):):). there is no difference to me.
Reply
11/20/2014 at 12:24 AM

---
**内容**: Madhukar Moogala said...
Hi Nick ,
The objective of this code is to restore\preserve the draw order while wblockcloning the blocks , not fix the broken draw order after inserting it.And, I was able reproduced your problem on copy and pasting blocks from one dwg to other, where draworder gets broken ,this code doesn't fix that problem.
Instead of using copy\ paste ,as a workaround you may use my code [look at SetBlockDrawOrder method this does correct the order prior to inserting]to copy the desired block in to current dwg ,which will be helpful as I believe.
And I don't have full answers to your question, but I can't even take further as it got fixed in 2015 Sp2.
Reply
11/20/2014 at 12:40 AM

---
**内容**: Nick Gorlov said in reply to Madhukar Moogala...
actually i didn't find a difference in broken block inserting between your and my code. that's why i started this conversation :).
about workaround. problem is not in me, but in my users :). i teach em, that they have to use my mechanism for inserting blocks, but they prefere copy/paste :(
"but I can't even take further as it got fixed in 2015 Sp2" - also there is no comments about this problem and its healing in sp2 documentation :) so, there were no problems at all :). anyway, thx for your help.
by the way, if your code is able to fix draworder, why, after inserting block with your code i still can't copy/paste inserted block to a new drawing? :)
Reply
11/21/2014 at 12:01 AM

---
**内容**: Madhukar Moogala said...
Hi Nick ,
I believe it is not possible to correct the draw order once the block definition has been generated in the current drawing, to correct the draworder we must know it's source draw order ,i.e. when we copy a block and paste it in current drawing we lost the trace of source block and what we left is clone of its ,while performing copy\paste draw order is getting messed up ,since copy\paste is acad feature ,we don’t have enough tools to correct the draw order only the Engineering should be able to fix the problem.
To answer your question why draworder is getting messed up , I did my research and this analysis is based on my observation and may be true or not, I find the draw order is getting messed up only if block contains Hatch entity, what actually happens when we copy\paste , clone of source block definition gets regenerated in the target drawing ,graphics of hatch gets printed last to tackle the performance issues , after cloned block definition got generated in target drawing ,the pasting mechanism should ascertain if the cloned block’s draw order and source block order are same, if not then paste mechanism should correct it ,this is not happening ,and this got fixed in SP2.
One Idea worth trying is if your entity is a custom entity, in your subdeepclone method, you can correct draw order because you‘ll be aware of source blocks draw order, to correct draworder you can SetRelativeDrawOrder API
Hope I was able to answer your query in some way.
Disclaimer: The thoughts above are my own doesn’t reflect my employers, may be true or even worse.
Reply
11/21/2014 at 06:00 AM

---
