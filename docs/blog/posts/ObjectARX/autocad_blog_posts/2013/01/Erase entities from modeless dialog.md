---
title: "Erase entities from modeless dialog"
date: 2013-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Block
description: "I'm having problems erasing entities from a modeless dialog."
author: Autodesk
---
# Erase entities from modeless dialog

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/erase-entities-from-modeless-dialog.html

## 文章内容

By Xiaodong Liang
Issue
I'm having problems erasing entities from a modeless dialog.
Problem #1 - I know I need to iterate the Model Space Block Table Record, open each entity for write and call erase() on it. The code is executed without errors but the entities are still displayed on the screen.
Problem #2 - When I select the entities for modifications, AutoCAD shows an unhandled exception dialog.
How do I solve these problems?
Solution
Because the dialog is modeless, explicit document locking is needed. Also because its a modeless dialog, graphics display update is not performed (unlike, for example, working from a modal dialog), so you'll need to do that explicitly as well.
The following code snippet solves both the above mentioned problems.
// assume the modeless dialog is CSampDialog
// and there is one button called Button1
void CSampDialog::OnButton1()  
{
    // has to do document locking explicitly
    acDocManager->lockDocument(curDoc());
    AcDbBlockTableRecordPointer pBtr(ACDB_MODEL_SPACE,
                curDoc()->database(),
                AcDb::kForWrite);
    if(pBtr.openStatus() != Acad::eOk)
        return;
    AcDbBlockTableRecordIterator* pIter = NULL;
    pBtr->newIterator(pIter);
    for(; !pIter->done();
            pIter->step())
    {
        AcDbEntity* pEnt = NULL;
        pIter->getEntity(pEnt, AcDb::kForRead);
        AcDbLine* pLine = AcDbLine::cast(pEnt);
        if(pLine)
        {
            pLine->upgradeOpen();
            pLine->erase();
            // force display update
            pLine->draw();
            pLine->close();
        }
        else
            pEnt->close();
    }
    delete pIter;
    // unlock document
    acDocManager->unlockDocument(curDoc());
}

