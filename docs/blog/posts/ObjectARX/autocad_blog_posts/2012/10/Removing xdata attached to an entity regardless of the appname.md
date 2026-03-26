---
title: "Removing xdata attached to an entity regardless of the appname"
date: 2012-10-01
categories:
  - AutoCAD C++
tags:
  - AutoLISP
  - C++
  - ObjectARX
  - Plugin
description: "The following ObjectARX / Lisp code removes XData that is attached to an entity regardless of the APPNAME. Use it with caution and only if you need..."
author: Autodesk
---
# Removing xdata attached to an entity regardless of the appname

发布日期: 2012-10-01

原始链接: https://adndevblog.typepad.com/autocad/2012/10/removing-xdata-attached-to-an-entity-regardless-of-the-appname.html

## 文章内容

By Balaji Ramamoorthy
The following ObjectARX / Lisp code removes XData that is attached to an entity regardless of the APPNAME. Use it with caution and only if you need to do this, since removing XData from an entity without considering the appname may cause plug-ins that rely on them to misbehave.
Here is the ObjectARX code :
static void AdskTestCommand(void)
{
    ads_name eNam;
    ads_point pt;
    int ret;
    ret = acedEntSel(ACRX_T("\nPick an entity :"), eNam, pt);
    if (RTNORM != ret)
        return;
      AcDbObjectId ObjId;
    acdbGetObjectId(ObjId, eNam);
      AcDbEntity *pEnt = NULL;
    Acad::ErrorStatus es
           = acdbOpenAcDbEntity(pEnt, ObjId, AcDb::kForWrite);
      resbuf *xdata = pEnt->xData(NULL);
    if (xdata)
    {
        xdata->rbnext = NULL;
        pEnt->setXData(xdata);
        acutRelRb(xdata);
    }
    pEnt->close();
}
Here is the Lisp code:
(defun c:DelXdata()
 (setq l (car (entsel "Pick object:")))
 (if l (progn
     (redraw l 3)
     (setq le (entget l '("*")) )
     (setq xdata (assoc '-3 le))
     (setq le
           (subst (cons (car xdata) (list (list (car (car (cdr xdata))))))
xdata le))
     (entmod le)
     (redraw l 4)
     le
    )
 )
)

## 评论

**内容**: petcon said...
how to removing xrecord AND xdict attached to an entity regardless of the appname
Reply
07/16/2015 at 09:27 PM

---
**内容**: Alexander Rivilis said in reply to petcon...
Both dictionary and xrecord has not appname. What do you mean?
Reply
07/24/2015 at 01:44 PM

---
**内容**: petcon said in reply to Alexander Rivilis...
sorry,long time no playing with objectarx. i mean how to remove xrecord and xdict attacher to an entity. make an entity clean. 删除实体所带的所有信息，xdata xrecord xdict，好久不编程，不太记得一个实体能附加哪些信息了，想把实体所带的信息都删除干净。 求 杜长宇翻译。daniel DU.
Reply
07/26/2015 at 08:19 PM

---
**内容**: Alexander Rivilis said...
[code]
static void RemExtDict () {
Acad::ErrorStatus es;
ads_name en; ads_point p;
if (acedEntSel(_T("\nSelect Entity with ExtDictionary: "),en,p) != RTNORM)
return;
AcDbObjectId eId; acdbGetObjectId(eId, en);
AcDbEntityPointer pEnt(eId, AcDb::kForRead);
if (pEnt.openStatus() == Acad::eOk) {
AcDbObjectId idExtDict = pEnt->extensionDictionary();
if (idExtDict.isNull() || idExtDict.isErased()) {
acutPrintf(_T("\nEntity has not Extension Dictionary!"));
return;
}
{
AcDbDictionaryPointer pDict(idExtDict, AcDb::kForWrite);
if (pDict.openStatus() == Acad::eOk) {
AcDbObjectIdArray ids; ids.setPhysicalLength(pDict->numEntries()+1);
AcDbDictionaryIterator *pIter = pDict->newIterator();
for (; !pIter->done(); pIter->next()) {
ids.append(pIter->objectId());
}
delete pIter;
for (int i = 0; i < ids.length(); i++) {
pDict->remove(ids[i]);
}
}
}
if (pEnt->upgradeOpen() == Acad::eOk) {
es = pEnt->releaseExtensionDictionary();
if (es != Acad::eOk) {
acutPrintf(_T("\nError releaseExtensionDictionary() = %s"),
acadErrorStatusText(es));
}
}
}
}
[/code]
Reply
07/29/2015 at 04:49 AM

---
**内容**: petcon said...
i test the ObjectARX code up in the post static void AdskTestCommand(void).
i found there maybe a bug.
i use xdata test in arxdbg to add xdata to entity.
after xdatatest there are two xdata mason and connor. (use entity info in arxdbg)
after run ObjectARX code ,ther is one xdata left connor.
run ObjectARX code one more time ,ther is no xdata left.
so the objectarxcode remove xdata only can remove one xdata at one time.
i think that is not a good code .because the code can not do things right at one time
Reply
01/23/2016 at 12:20 AM

---
