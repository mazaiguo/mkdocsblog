---
title: "Updating dimensions associated with a dynamic block"
date: 2012-09-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Block
  - Dimension
description: "I have a dimension in a dynamic block. When I modify the parameter programmatically, the block gets updated but the dimension does not update itsel..."
author: Autodesk
---
# Updating dimensions associated with a dynamic block

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/updating-dimensions-associated-with-a-dynamic-block.html

## 文章内容

By Balaji Ramamoorthy
Issue
I have a dimension in a dynamic block. When I modify the parameter programmatically, the block gets updated but the dimension does not update itself. What can I do to resove this ?
Solution
When the parameter is modified, AutoCAD creates a new anonymous block. To ensure that the dimension also get updated to reflect the change in the parameter, this anonymous block must be opened for write and marked as "modified". This will ensure that AutoCAD updates the dimension.
Here is the sample code. The complete sample project can be downloaded from the link below.
AcDbObjectId selectedObjectId = _blockRefOid;
AcArray<AcDbObjectId> oidArray;
  AcDbBlockReference *pBlockRef = NULL;
acdbOpenObject(pBlockRef, selectedObjectId, AcDb::kForWrite);
  AcDbBlockTableRecord *pBlockTableRecord1 = 0;
acdbOpenObject(
                    pBlockTableRecord1,
                    pBlockRef->blockTableRecord(),
                    AcDb::kForWrite
              );
ACHAR *name = NULL;
pBlockTableRecord1->getName(name);
  AcDbBlockTableRecordIterator *pIterator = NULL;
pBlockTableRecord1->newIterator(pIterator);
  while(pIterator->done() == false)
{
           AcDbEntity *pEnt1 = NULL;
           pIterator->getEntity(pEnt1, AcDb::kForWrite);
             if (pEnt1->isKindOf(AcDbBlockReference::desc()))
           {
                      oidArray.append(pEnt1->objectId());
           }
           pEnt1->assertWriteEnabled();
           pEnt1->recordGraphicsModified(true);
           pEnt1->close();
           pIterator->step();
}
delete pIterator;
pBlockTableRecord1->close();
Download Testblock Download Testapp

## 评论

**内容**: Luc said...
Hi Balaji
I have the same problem , but while DotNet programming and I fail to transcibe your solution
Can you help
regards
Luc
Reply
03/24/2014 at 08:02 AM

---
**内容**: Balaji said...
Hi Luc,
Sorry for the delay in getting back to you.
As I am working on a few migration activities ahead of our upcoming AutoCAD release, I will need some time to investigate this.
I will update you at the earliest.
Regards,
Balaji
Reply
03/26/2014 at 10:48 PM

---
**内容**: Balaji said in reply to Balaji...
Hi Luc,
Using sendstringToExecute and sending "DIMREGEN: and "REGEN" commands updates the dimension inside the dynamic block.
Sorry, I haven't found an elegant way to work around this behavior. We have this behavior logged with our engineering team for this specific behavior with the .Net API.
Regards,
Balaji

Reply
03/28/2014 at 05:32 AM

---
**内容**: Luc said...
Hi Balaji,
work fine
thanks
Luc
Reply
04/02/2014 at 07:58 AM

---
**内容**: Ben said...
Hi Balaji - thank you for this note.
Is it possible to demonstrate this exact thing in .net (c#) - because i'm not sure all of us will be able to completely follow it in ObjectArx.
regards

Ben
Reply
01/30/2016 at 05:51 PM

---
**内容**: Fil said...
Hello. Any way of doing this without programming? Just plain commands? Thanks
Reply
05/19/2016 at 02:04 AM

---
**内容**: shirish said...
Thanks!
Reply
10/18/2019 at 04:18 AM

---
