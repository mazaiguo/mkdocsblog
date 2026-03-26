---
title: "How to handle references to other entities"
date: 2019-02-01
categories:
  - AutoCAD C++
tags:
  - Block
  - C++
  - Database
description: "An example of handling some common operations for certain types of entities. This does not attempt to be a full-featured entity in the sense that i..."
author: Autodesk
---
# How to handle references to other entities

发布日期: 2019-02-01

原始链接: https://adndevblog.typepad.com/autocad/2019/02/how-to-handle-references-to-other-entities.html

## 文章内容

By Madhukar Moogala
An example of handling some common operations for certain types of entities. This does not attempt to be a full-featured entity in the sense that it fills out every single function that it is supposed to. Its main purpose is to illustrate how to deal with pointing to a dictionary-resident"Style" object This sample is stripped out from Jim Awe's classic ArxDBG, this mainly focus on establishing hard linkage to other entities, dealing copy with in and across database.
I received a query from ADN partner who is facing WBlock cloning issues i.e., when copying an entity with hard refererence to another entity
You need to be very cautious while copy and pasting entities, in below I have shown steps need to follow in both wblockclone and deepclone
Acad::ErrorStatus
ArxDbgDbEntity::subWblockClone(AcRxObject* pOwner, AcDbObject*& pClone,
                    AcDbIdMapping& idMap, Adesk::Boolean isPrimary) const
{
       if (ArxDbgOptions::m_instance.m_showWblockCloneDetails) {
             CString titleStr, tmpStr;
             titleStr.Format(_T("Beginning -- wblockClone: %s"),
                           ArxDbgUtils::objToClassAndHandleStr(const_cast(this), tmpStr));
             ArxDbgUiTdmIdMap dbox(&idMap, acedGetAcadDwgView(), titleStr);
             dbox.DoModal();
       }
 
    AcDb::DeepCloneType type = idMap.deepCloneContext();
 
        // if xrefInsert or xrefBind, we know everything will
        // be cloned, so just let normal routine handle this
    if ((type == AcDb::kDcXrefBind) || (type == AcDb::kDcXrefInsert)) {
        return AcDbEntity::subWblockClone(pOwner, pClone, idMap, isPrimary);
    }
             // if we've already been cloned, just return
       AcDbIdPair idPair(objectId(), AcDbObjectId::kNull, true);
    if (idMap.compute(idPair) && (idPair.value() != AcDbObjectId::kNull)) {
        return Acad::eOk;
    }
 
        // If isPrimary is kTrue, then override the default cloning
        // within our own cloning, which would set it to kFalse,
        // by cloning our referenced entity first.
    if (isPrimary) {
                    // now ask derived classes what references they want cloned for them
             AcDbObjectIdArray refEntIds;
             AcDbIntArray refTypes;
             getCloneReferences(type, refEntIds, refTypes);
 
             ASSERT(refEntIds.length() == refTypes.length());
 
            // clone each entity we reference first and change the value
            // of isPrimary to fake it out.  Since we clone these first,
            // when the normal wblockClone is called, it will see that
            // they are already in the set of cloned objects and will not
            // try to clone it again.
        AcDbEntity* ent;
        Acad::ErrorStatus es;
             int len = refEntIds.length();
             for (int i=0; iblockId()) {
                                               // Use the same owner, and pass in the same isPrimary value
                                        AcDbObject* pSubClone = NULL;
                                        es = ent->wblockClone(pOwner, pSubClone, idMap, Adesk::kTrue);
                                        if (pSubClone != NULL)
                                               pSubClone->close();
 
                                        if (es != Acad::eOk) {
                                               ASSERT(0);
                                        }
                                 }
                                 else {
                                        ASSERT(0);
                                 }
 
                                 ent->close();
                           }
                    }
             }
    }
        // Now we can clone ourselves via calling our parent's method.
       Acad::ErrorStatus es =  AcDbEntity::subWblockClone(pOwner, pClone, idMap, isPrimary);
 
       if (ArxDbgOptions::m_instance.m_showWblockCloneDetails) {
             CString titleStr, tmpStr;
             titleStr.Format(_T("End -- wblockClone: %s"),
                           ArxDbgUtils::objToClassAndHandleStr(const_cast(this), tmpStr));
             ArxDbgUiTdmIdMap dbox(&idMap, acedGetAcadDwgView(), titleStr);
             dbox.DoModal();
       }
 
       return es;
}
 
 
 
Acad::ErrorStatus
ArxDbgDbEntity::subDeepClone(AcDbObject* pOwner,
              AcDbObject*& pClonedObject,
              AcDbIdMapping& idMap,
              Adesk::Boolean isPrimary) const
{
        // You should always pass back pClonedObject == NULL
        // if, for any reason, you do not actually clone it
        // during this call.  The caller should pass it in
        // as NULL, but to be safe, we set it here as well.
    pClonedObject = NULL;
 
       if (ArxDbgOptions::m_instance.m_showDeepCloneDetails) {
             CString titleStr, tmpStr;
             titleStr.Format(_T("Beginning -- deepClone: %s"),
                           ArxDbgUtils::objToClassAndHandleStr(const_cast(this), tmpStr));
             ArxDbgUiTdmIdMap dbox(&idMap, acedGetAcadDwgView(), titleStr);
             dbox.DoModal();
       }
 
    AcDb::DeepCloneType type = idMap.deepCloneContext();
 
        // if we know everything will be cloned for us, just let
             // the base class do everything for us.
    if ((type == AcDb::kDcInsert) ||
             (type == AcDb::kDcInsertCopy) ||
             (type == AcDb::kDcExplode))
        return AcDbEntity::subDeepClone(pOwner, pClonedObject, idMap, isPrimary);
 
        // following case happens when doing a AcDbDatabase::deepCloneObjects()
        // and the owner happens to be the same... then its really like a
        // kDcCopy, otherwise deepCloneObjects() is like a kDcBlock
    if (type == AcDb::kDcObjects) {
             if (ownerId() == pOwner->objectId())
                    type = AcDb::kDcCopy;
             else
                    type = AcDb::kDcBlock;
       }
 
             // now ask derived classes what references they want cloned for them
       AcDbObjectIdArray refEntIds;
       AcDbIntArray refTypes;
       getCloneReferences(type, refEntIds, refTypes);
       ASSERT(refEntIds.length() == refTypes.length());
 
             // if derived class doesn't have any references to take care of, then
             // we will just let the AcDbEntity::deepClone() take care of things.
       if (refEntIds.isEmpty())
             return AcDbEntity::subDeepClone(pOwner, pClonedObject, idMap, isPrimary);
 
        // If this object is in the idMap and is already
        // cloned, then return.
       bool tmpIsPrimary = isPrimary ? true : false;   // get around compiler performance warning
    AcDbIdPair idPair(objectId(), AcDbObjectId::kNull, false, tmpIsPrimary);
    if (idMap.compute(idPair) && (idPair.value() != NULL))
        return Acad::eOk;
 
    // STEP 1:
    // Create the clone
    //
    AcDbObject *pClone = (AcDbObject*)isA()->create();
    if (pClone != NULL)
        pClonedObject = pClone;    // set the return value
    else
        return Acad::eOutOfMemory;
 
    // STEP 2:
    // Append the clone to its new owner.  In this example,
    // we know that we are derived from AcDbEntity, so we
    // can expect our owner to be an AcDbBlockTableRecord,
    // unless we have set up an ownership relationship with
    // another of our objects.  In that case, we need to
    // establish how we connect to that owner in our own
    // way.  This sample shows a generic method using
    // setOwnerId().
    //
    AcDbBlockTableRecord *pBTR = AcDbBlockTableRecord::cast(pOwner);
    if (pBTR != NULL) {
        AcDbEntity* ent = AcDbEntity::cast(pClone);
        pBTR->appendAcDbEntity(ent);
    }
    else {
        if (isPrimary)
            return Acad::eInvalidOwnerObject;
 
        // Some form of this code is only necessary if
        // anyone has set up an ownership for our object
        // other than with an AcDbBlockTableRecord.
        //
        pOwner->database()->addAcDbObject(pClone);
        pClone->setOwnerId(pOwner->objectId());
    }
 
    // STEP 3:
    // Now we copy our contents to the clone.  This is done
    // using an AcDbDeepCloneFiler.  This filer keeps a
    // list of all AcDbHardOwnershipIds and
    // AcDbSoftOwnershipIds we, and any classes we derive
    // from,  have.  This list is then used to know what
    // additional, "owned" objects need to be cloned below.
    //
    AcDbDeepCloneFiler filer;
    dwgOut(&filer);
 
    // STEP 4:
    // Rewind the filer and read the data into the clone.
 
    //
    filer.seek(0L, AcDb::kSeekFromStart);
    pClone->dwgIn(&filer);
 
    // STEP 5:
    // This must be called for all newly created objects
    // in deepClone.  It is turned off by endDeepClone()
    // after it has translated the references to their
    // new values.
    //
    pClone->setAcDbObjectIdsInFlux();
 
    // STEP 6:
    // Add the new information to the idMap.  We can use
    // the idPair started above.
    //
    idPair.setValue(pClonedObject->objectId());
    idPair.setIsCloned(Adesk::kTrue);
    idMap.assign(idPair);
 
    // STEP 7:
    // Using the filer list created above, find and clone
    // any owned objects.
    //
    AcDbObject *pSubObject;
    AcDbObject *pClonedSubObject;
    AcDbObjectId id;
    Acad::ErrorStatus es;
    while (filer.getNextOwnedObject(id)) {
            // Open the object and clone it.  Note that we now
            // set "isPrimary" to kFalse here because the object
            // is being cloned, not as part of the primary set,
            // but because it is owned by something in the
            // primary set.
        es = acdbOpenAcDbObject(pSubObject, id, AcDb::kForRead);
        if (es != Acad::eOk)
            continue;   // could have been NULL or erased
 
        pClonedSubObject = NULL;
        pSubObject->deepClone(pClonedObject, pClonedSubObject, idMap, Adesk::kFalse);
 
            // If this is a kDcInsert context, the objects
            // may be "cheapCloned".  In this case, they are
            // "moved" instead of cloned.  The result is that
            // pSubObject and pClonedSubObject will point to
            // the same object.  So, we only want to close
            // pSubObject if it really is a different object
            // than its clone.
        if (pSubObject != pClonedSubObject)
            pSubObject->close();
 
            // The pSubObject may either already have been
            // cloned, or for some reason has chosen not to be
            // cloned.  In that case, the returned pointer will
            // be NULL.  Otherwise, since we have no immediate
            // use for it now, we can close the clone.
        if (pClonedSubObject != NULL)
            pClonedSubObject->close();
    }
 
        // clone the referenced entities
    AcDbObject* ent;
       int len = refEntIds.length();
       for (int i=0; ideepClone(pOwner, pClonedSubObject, idMap, Adesk::kTrue);
                           if (es == Acad::eOk) {
                                        // see comment above about cheap clone
                                 if (ent != pClonedSubObject)
                                        ent->close();
 
                                 if (pClonedSubObject != NULL)
                                        pClonedSubObject->close();
                           }
                    }
             }
                    // this case is needed for RefEdit so we can pass its validation
                    // test when editing a blockReference.  We don't actually clone it
                    // but we add it to the map so it thinks it got cloned and is therefore
                    // a valid "Closed Set" of objects.
             else if (refTypes[i] == kFakeClone) {
            AcDbIdPair idPair(refEntIds[i], refEntIds[i], false, false, true);
            idMap.assign(idPair);
             }
       }
 
       if (ArxDbgOptions::m_instance.m_showDeepCloneDetails) {
             CString titleStr, tmpStr;
             titleStr.Format(_T("End -- deepClone: %s"),
                           ArxDbgUtils::objToClassAndHandleStr(const_cast(this), tmpStr));
             ArxDbgUiTdmIdMap dbox(&idMap, acedGetAcadDwgView(), titleStr);
             dbox.DoModal();
       }
 
        // Leave pClonedObject open for the caller
    return Acad::eOk;
}
Complete Source
AdskLogo-Project

## 评论

**内容**: Hanauer said...
A .NET version would be cool!
Reply
02/16/2019 at 05:04 AM

---
**内容**: Madhukar Moogala said...
Hi Hanauer,
Unfortunately it is not possible to port to .NET, blog sample mainly talks about filing and dealing Hard References with in a custom entity, concept of custom entity doesn't exist in .NET, it is only in C++.
Reply
02/17/2019 at 09:15 PM

---
**内容**: Hanauer said in reply to Madhukar Moogala...
I know custom entities do not exist in .NET, but a well crafted example with custom objects spanning extension dictionary, XRecord, HardPointerId, SoftPointerId, TreatElementsAsHard, wblock, copy clip, paste clip would be very good.
The ObjectArxGuide says that the hard pointer reference protects an object from purge.
What are the differences between HardPointerId and SoftPointeId?
How to correctly use HardPointerId and SoftPointerId involving operations of wblock, ctrl c, ctrl v, etc.
I have a plugin written in C # that uses relationships between objects through extension dictionary, XRecord and HardpointerId and when I use copy clip and then paste clip the relationship information between objects is lost.
The alternative I found was to use events and intercept the copyclip and pasteclip commands and restore the relationships. Besides being a poor solution it is not reliable ( if the plug-in is not loaded the solution does not work).
Is there an efficient solution for this? Is it possible to post an example in .NET?
Reply
02/18/2019 at 05:13 AM

---
**内容**: Madhukar Moogala said...
Spanning extension dictionary, XRecord, HardPointerId, SoftPointerId, TreatElementsAsHard, wblock, copy clip, paste clip would be very good
I assume you are asking this C++, yes there is, you can check the stripped down version of sample posted below my blog.
https://github.com/MadhukarMoogala/adn_adskLogo
or ArxDBG, full blown sample ADESKLogo [SDK\samples\database\ARXDBG\AdeskLogo]
What are the differences between HardPointerId and SoftPointeId?
-- https://slideplayer.com/slide/4391931/, Devdays PPT.
The ObjectArxGuide says that the hard pointer reference protects an object from purge.
Exactly, the distinction between soft and hard object reference lies in the survival of the object and existence of object being referred.
Hard Reference: An object's fate of survival depends on the existence of the object that is being referred.
Soft Reference: An object relationship with its referring object is trival and not important for it's own survival.

How to correctly use HardPointerId and SoftPointerId involving operations of wblock, ctrl c, ctrl v, etc.
Wblock Operations - Wblock
Wblock need to use Hard Owner and Pointer References.
Ctrl-C\Ctrl-V - "Wblock (_copyclip) + DeepClone during insert i.e _PasteCLip"
DeepClone - Hard and Soft Ownership Reference
Wblock - Hard Owner and Pointer References

Example:

Assume we have a 3DPline with 3 vertices with a layer, linetype and material.
HardOwnership - 3Dpline hard owns these three vertices, now if you want purge vertices, you can't purge, since they are hard owned by 3DPline.
HardPointer- 3Dpline hard points layer, linetype and material, you can't purge any of these, as these are referred by 3dpline, hence these are protected from purge.
SoftOwnership - The Material Dictionary [AcDbDictionary] soft owns material [m1] which is being referred by 3DPline, now if you change the material of 3dPline from [m1] to [m2], you can purge m1.
SoftPointer - Material holds a soft pointer reference to its owner AcDbDictionary, i.e Material Dictionary.
Generally, all AutoCAD in built Dictionaries soft owns its objects, each object soft pointers reference to its owner.
But, if Treat Its Elements [TreatElementsAsHard] is set to True, then elements of dictionary hard owns its objects

Besides being a poor solution, it is not reliable ( if the plug-in is not loaded the solution does not work). Is there an efficient solution for this? Is it possible to post an example in .NET?

To create an anonymous group with all the objects that belong together, and you need not worry about _copyclip,pasteclip,wblock etc.
AcDbGroup plants persistent reactors on its entries when the entries are added to the group. To accomplish this, it must have an objectId. When the group is added to the group dictionary, it is also added to the database, and thus it obtains an objectId. Therefore, do not attempt to add entries to a newly created group before adding the group to the group dictionary.
For example, the code for creating a group should be like:

AcDbGroup *pGroup = new AcDbGroup;
AcDbObjectId groupObjectId;
AcDbDictionary *pGroupDict = NULL;
acdbCurDwg()->getGroupDictionary(pGroupDict, AcDb::kForWrite);
pGroupDict->setAt("GroupName", pGroup, groupObjectId);
pGroupDict->close();
pGroup->append(objectId1); // objectId1 and objectId2
// are objId's of the
pGroup->append(objectId2); // entities which will be in the group.
pGroup->close();
For .Net similar you can.
https://adndevblog.typepad.com/autocad/2012/05/create-an-anonymous-group.html
Reply
02/19/2019 at 03:49 AM

---
**内容**: Hanauer said...
Thanks for the clarifications. I apologize for not being clear.
I have no relationship problems in the same file but rather, when I use CTRL C and in another file I give CTRL V, the relationship (xrecord, hardpointerid, handle) between entities is lost.
Same situation occurs with groups. I create a unnamed group for a circle and a line. I select the group and press CTRL C. I change the file and give CTRL V and the group no longer exists.
Already in AutoCAD Archtecture if I give CTRL C in a window and change file and give CTRL V, the window is inserted along with the wall in which it is contained. There is no loss of relationships. How is this implemented in ACA? What is the way to do this in AutoCAD .NET?
Reply
02/22/2019 at 09:34 AM

---
**内容**: Madhukar Moogala said in reply to Hanauer...
Hi Hanauer,
Same situation occurs with groups. I create an unnamed group for a circle and a line. I select the group and press CTRL C. I change the file and give CTRL V and the group no longer exists.
Thanks for clarification, Group will not survive through ctrl-c/ctrl-v across database, precisely during Wblock clone operation.
This is because AcDbGroup only has hard pointer connection with its objects and is not hard owned by its parent NOD.
So, we need enforce copying AcDbGroup object as well during Wblock clone operation,
The problem with the WBLOCK /CTRL-C was that it first wblockClone's objects into a temporary in-memory database, then calls save() to save the temporary database to disk. But save honors only the ownership references (hard owner and soft owner). This means one kind of hard reference called the hard pointer reference will not be honored by save and that means objects pointed to by hard pointer references would not be saved. Put another way, objects that have been cloned during wblockClone are not saved to the drawing file if their owners haven't been cloned during wblockClone.
To avoid this problem with wblockClone, dictionaries and custom objects (Inheriting from AcDbObject) now automatically file a hardpointer id of their owners. In this way, the complete ownership hierarchy is preserved, and save() can save them all.
Unfortunately, AcDbGroup seems be lone wolf left out 😉
To fix this-
Override the virtual method "beginDeepCloneXlation",this method will be called when you AutoCAD needs to perform a deep clone.
In this overridden method, you get access to the "source" database as well as the "destination" database. Ensure that you explicitly "wblockClone" the dictionary that you want to be wblocked to the destination database.
I will work on a sample and get back to you. Please expect some delay, I'm fully occupied with forge work.
Already in AutoCAD Archtecture if I give CTRL C in a window and change file and give CTRL V, the window is inserted along with the wall in which it is contained. There is no loss of relationships. How is this implemented in ACA? What is the way to do this in AutoCAD .NET?
This what my blog post talks about, ACA entities are custom entities deriving from AcDbEntity, in your example, Window is hard owned by Wall entity hence relationship will remain intact during Wblock clone across database.
In window class implementation, a hard ownership reference to Wall entity is filed.
Reply
02/27/2019 at 03:58 AM

---
**内容**: Hanauer said in reply to Madhukar Moogala...
Hi,
Have news about this:
"I will work on a sample and get back to you. Please expect some delay, I'm fully occupied with forge work."
Thanks.
Reply
08/23/2019 at 09:46 AM

---
**内容**: technodata group said...
Nice post content is impressive to read ,Thanks for proving some helpful information.Hope you will keep on sharing articles.
This provides good insight. You might also be interested to know more about generating more leads and getting the right intelligence to engage prospects. Techno Data Group implements new lead gen ideas and strategies for generating more leads and targeting the right leads and accounts.
href="https://technodatagroup.com/autodesk-autocad-users-email-list">TECHNO DATA GROUP
Reply
10/28/2019 at 10:54 PM

---
