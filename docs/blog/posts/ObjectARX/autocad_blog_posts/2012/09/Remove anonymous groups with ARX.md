---
title: "Remove anonymous groups with ARX"
date: 2012-09-01
categories:
  - AutoCAD C++
tags:
  - AutoCAD
  - C++
  - Database
description: "When an end user creates a 'group' in AutoCAD, it may be an anonymous group. However, all group (anonymous or otherwise) are stored in the Named Ob..."
author: Autodesk
---
# Remove anonymous groups with ARX

发布日期: 2012-09-01

原始链接: https://adndevblog.typepad.com/autocad/2012/09/remove-anonymous-groups-with-arx.html

## 文章内容

By Xiaodong Liang 
When an end user creates a 'group' in AutoCAD, it may be an anonymous group. However, all group (anonymous or otherwise) are stored in the Named Objects Dictionary under the key 'ACAD_GROUP'. If the group is anonymous, AutoCAD assigns it a value such as '*A1', '*A2' and so on. Although to the end user it's anonymous, the group has a unique key name in the AutoCAD database.
Users may add or remove entities from groups so it is possible to have empty groups. The code below is a small demo to remove an anonymous group.
  static void removeGroup()
{
  Acad::ErrorStatus es;
AcDbDictionary *pGroupDict;
AcDbGroup *pGroup;
AcDbDictionaryIterator *pDictIter;
AcDbObjectId groupId;
long numItems;
AcDbObjectIdArray groupMembers;
  es =
acdbHostApplicationServices()->workingDatabase()->
   getGroupDictionary(pGroupDict,AcDb::kForWrite);
pDictIter = pGroupDict->newIterator();
  for(; !pDictIter->done(); pDictIter->next())
{
    pDictIter->getObject(
        (AcDbObject*&)pGroup, AcDb::kForRead);
    // Is the group anonymous?
    if(pGroup->isAnonymous())
    {
        // Does the anonymous group have
        // any members associated with it?
        numItems = pGroup->numEntities();
        if(numItems > 0)
        {
            // Empty the group
            // Upgrade it first
            es = pGroup->upgradeOpen();
            es = pGroup->clear();
            es = pGroup->downgradeOpen();
              pGroup->close();
        }
          // Get the group ID and remove the
        // group from the dictionary
        groupId = pDictIter->objectId();
        es = pGroupDict->remove(groupId);
      } // if
      pGroup->close();
  } // for
  pGroupDict->close();
  }

## 评论

**内容**: Andre said...
Do anonymous groups pose any threat to corrupt file or else... why would I want to remove these empty groups?
Thanks
Reply
06/02/2014 at 04:21 AM

---
