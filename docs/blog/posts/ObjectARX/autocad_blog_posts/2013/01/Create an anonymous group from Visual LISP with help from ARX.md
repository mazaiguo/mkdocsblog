---
title: "Create an anonymous group from Visual LISP with help from ARX"
date: 2013-01-01
categories:
  - AutoCAD C++
tags:
  - AutoLISP
  - C++
description: "The following ARX code does that. You need to however register the ARX function using acedDefun() to be able to use it as an external Lisp function..."
author: Autodesk
---
# Create an anonymous group from Visual LISP with help from ARX

发布日期: 2013-01-01

原始链接: https://adndevblog.typepad.com/autocad/2013/01/create-an-anonymous-group-from-visual-lisp-with-help-from-arx.html

## 文章内容

By Gopinath Taget
The following ARX code does that. You need to however register the ARX function using acedDefun() to be able to use it as an external Lisp function.  It is implemented such that it returns a list, containing the new group's ObjectID, to the external Lisp function.
The ARX function:
int acdbAddAnonGrpRet2Lsp()
{
 // TODO: Implement the command
resbuf *pArg =acedGetArgs ();
   struct resbuf *startRb = NULL;
AcDbGroup *pGroup = new AcDbGroup();
AcDbObjectId grpId;
AcDbDictionary *pGroupDict;
Acad::ErrorStatus es;
AcApDocument *curDoc;
   //get the group dictionary
AcDbDatabase *pDb = acdbHostApplicationServices()->
  workingDatabase();
 if (Acad::eOk == (es = acDocManager->lockDocument(
  curDoc=acDocManager->curDocument())))
  es = pDb->getGroupDictionary(pGroupDict,AcDb::kForWrite);
   if (es != Acad::eOk)
  return es;
     //make an anonymous entry
 if ((es = pGroupDict->setAt(L"*", pGroup, grpId)) ==
  Acad::eOk) {
  //retrieve its name char *pNam;
  pGroup->close();
}
   // create a resbuf with our ObjectID in it
 struct resbuf *newRb = acutBuildList (RTLONG, grpId, RTNONE);
 // if ok
 if (newRb != NULL) {
  // if this is the first time we've done this
  if (startRb == NULL) {
   // then set this as the start
   startRb = newRb;
  }
  // otherwise add it to the end of our list
  else {
   // create a pointer to the beginning of our resbuf list
   struct resbuf *ptr = startRb;
   // find the end of our list
   while (ptr->rbnext != NULL)
    ptr = ptr->rbnext;
   // now attach our newly create resbuf to the end
   ptr->rbnext = newRb;
  }
}
  pGroupDict->close();
acDocManager->unlockDocument(curDoc);
  acedRetList(startRb);
acutRelRb(startRb);
 return (RTNORM);
}
The Lisp code:
  (defun isAppLoaded (app)
   (if (not (member app (arx)))
      (setq bAppLoaded :vlax-false)
      (setq bAppLoaded :vlax-true)
   )
   bAppLoaded
)
  (defun Example_AddLightWeightPolyline()
   (vl-load-com)
   (if (= (isAppLoaded "asdkanonygrplsp.arx") :vlax-false)
      (arxload (findfile "asdkanonygrplsp.arx"))
   )
       (setq oAcad (vlax-get-acad-object)
           oDoc (vla-get-activedocument oAcad)
           *ModelSpace* (vla-get-ModelSpace oDoc)
   )
       ;;Add anonymous group
   (setq myGroup (vl-catch-all-apply
                              'vla-objectidtoobject
                              (list
                                 oDoc
                                 (vlax-make-variant
                               (car (acdbAddAnonGrpRet2Lsp))
                                    vlax-vbLong
                                 )
                              )
                           )
   ) ;setq
       ;;If error encountered making group, then exit
   (if (vl-catch-all-error-p myGroup)
      (princ (vl-catch-all-error-message myGroup))
      ;;otherwise continue...
      (progn
         ;; Define the 2D polyline points
         (setq pt1 (list 1.0 1.0)
                 pt2 (list 1.0 2.0)
                 pt3 (list 2.0 2.0)
                 pt4 (list 3.0 2.0)
                 pt5 (list 4.0 4.0)
         )
     (setq Points (apply 'append (list pt1 pt2 pt3 pt4 pt5)))
         (setq ptlstlen (length Points))
             ;; Make array of 5*2=10 doubles -
     ;; that's an array of dimension 0 to 9
         (setq PointDataA (
        vlax-make-safearray vlax-vbDouble (
                      cons 0 (1- ptlstlen))))
         (vlax-safearray-fill PointDataA Points)
         (setq PointData (vlax-make-variant PointDataA))
          ;; Create a light weight Polyline object in model space
         (setq myLWpoly (
        vla-addLightweightPolyline *ModelSpace* PointData))
             ;; Make array of 1 object (the new LWPolyline)
   (setq myObjA (vlax-make-safearray vlax-vbObject '(0 . 0)))
         (vlax-safearray-put-element myObjA 0 myLWpoly)
             ;; Add the LWPolyline to the group
         (vla-appenditems myGroup myObjA)
      ) ;progn
   ) ;if
   (princ)
)

## 评论

**内容**: Subir Kumar Dutta said...
Hi , During converting some old Lisp code to .Net , I faced a situation. After analysing the Lisp code we understand its calling some ARX functions (not commands , originally ads function - the whole ObjectARX project does not have a single executable commands but all are functions called by AutoLisp ).
For example as below,
int ReturnListToAutoLisp(void)
{
struct resbuf *LIST;
//...
//... = acedGetArgs
//...

acedRetList(LIST);
return RTNORM;
}
The function itself does not return the list but the list is returned by the acedRetList.
Now the below AutoLisp code that calls this functions and store the return value in a list.
(setq returnedList (ReturnListToAutoLisp 5))
Through it looks that the ReturnListToAutoLisp takes an integer ( like 5 here ) but actually in the ObjectARX code its parameter list is void ) . However the parameter value passed are collected by calling acedGetArgs.
Also the return value is not a single integer but a list of strings which are collected in the AutoLisp variable named ‘returnedList’ and which is used to populated DropDown list in DCL UI.
So far its okey.
I have ported the old ObjectARX 2005 code to ObjectARX 2014 version and its working fine when called from AutoLisp.
But while converting the Lisp code to VB.Net , I can’t find a way to collect the return value in a .Net variable of type string List (List(Of String)).
I found samples to call ObjectARX functions from .Net using P/Invoke which focus on passing arguments by creating a ResultBuffer. But I did not find a single sample that demonstrate how to collect the list of values retuned from ObjectARX functions through acedRetList.
I am counting that there must be a way but can’t figure it out.
Please help.
Reply
03/25/2014 at 04:40 AM

---
