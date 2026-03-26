---
title: "Creating Link Templates using ActiveX API in VBA and Lisp"
date: 2012-12-01
categories:
  - AutoLISP
tags:
  - API
  - AutoLISP
  - COM
  - VBA
description: "Here is the sample VBA and VLisp code that shows how to create and delete link templates in AutoCAD. Do not forget to set references to CAO type li..."
author: Autodesk
---
# Creating Link Templates using ActiveX API in VBA and Lisp

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/creating-link-templates-using-activex-api-in-vba-and-lisp.html

## 文章内容

By Gopinath Taget
Here is the sample VBA and VLisp code that shows how to create and delete link templates in AutoCAD. Do not forget to set references to CAO type library before running this code in AutoCAD's VBA IDE.
Sub fCreateLinkTemplate()
    Dim pDB As CAO.DbConnect
  Dim pLTs As CAO.LinkTemplates
  Dim pLT As CAO.LabelTemplate
  Dim pKeyDescs As CAO.KeyDescriptions
  Dim psDataSrc As String
  Dim psLinkTempName1 As String
  Dim psLinkTempName2 As String
  psDataSrc = "jet_dbsamples"
  psLinkTempName1 = "LTCreatedByVBCAO"
  psLinkTempName2 = "LTtobeDeleted"
    'get the DBCONNECT object
  Set pDB = ThisDrawing.Application.
    GetInterfaceObject("CAO.DBConnect.16")
  Set pLTs = pDB.GetLinkTemplates(ThisDrawing)
    'prepare the keydescriptions
  Set pKeyDescs = ThisDrawing.Application.
    GetInterfaceObject("CAO.KeyDescriptions.16")
  pKeyDescs.Add "TAG_NUMBER", kCaoTypeInteger
  pKeyDescs.Add "Manufacturer", kCaoTypeText
    'create two Link Templates
  pLTs.Add psDataSrc, "Catalog1",
    "Schema1", "Computer", psLinkTempName1, pKeyDescs
  pLTs.Add psDataSrc, "Catalog2",
    "Schema2", "Computer", psLinkTempName2, pKeyDescs
  'created Link Templates
  MsgBox "Created Link Templates : " & Chr(13) & "1) " &
    pLTs.Item(psLinkTempName1).Name _
  & Chr(13) & "2) " & pLTs.Item(psLinkTempName2).Name _
    'connect to the datasource
  pDB.Connect psDataSrc
  'delete the second linktemplate.
  'Comment the following statement if
  'you want to see both the link templates
  pLTs.Delete psLinkTempName2
End Sub
And here’s the Visual Lisp code using the ActiveX API:
(defun c:CreateLT()
  (vl-load-com)
  (setq pDoc (vla-get-ActiveDocument (vlax-get-acad-object)))
  ;get the DBConnect
  (setq pDBObj (vla-GetInterfaceObject
           (vlax-get-acad-object) "CAO.dbConnect"))
  (if (null pDBObj)
    (progn
      (alert "Cannot create CAO Automation server.")
      (exit)))
  ;get the linktemplates
  (setq pLTs(
       vlax-invoke-method pDBObj "GetLinkTemplates" pDoc))
  ;prepare the keydescriptions
  (setq pKeyDescs (
         vla-GetInterfaceObject (vlax-get-acad-object)
          "CAO.KeyDescriptions"))
  (vlax-invoke-method pKeyDescs
  "ADD" "TAG_NUMBER" 3 nil nil)
  (vlax-invoke-method pKeyDescs
  "ADD" "Manufacturer" 1 nil nil)
  ;create two link templates
  (vlax-invoke-method pLTs "ADD" "jet_dbsamples"
  nil nil "COMPUTER" "LTCreatedByVLispCAO" pKeyDescs)
  (vlax-invoke-method pLTs "ADD" "jet_dbsamples"
  nil nil "COMPUTER" "LTtobeDeleted" pKeyDescs)
  ;sample code to show how to delete the link template
  (vlax-invoke-method pLTs "delete" "LTtobeDeleted")
)

## 评论

**内容**: Hanauer said...
Why not provide examples in AutoCAD. NET? VBA in 64bits with connection in Access, sql, etc.?
I'm migration my old Bubble CAO VBA appliation to AutoCAD .NET and not has reason for today use CAO Library in VBA. And today I have some problems in AutoCAD 2013 with conversion and OldObjectId ObjectId.
I would be very happy if in this blog found detailed examples showing the use of CAO Library with AutoCAD. NET.
Reply
12/20/2012 at 08:50 AM

---
**内容**: Gopinath Taget said in reply to Hanauer...
Hi Hanauer,
Thanks for the feedback. I will look into creating a blog post for using CAO in .NET in the near future.
Cheers
Gopinath
Reply
12/20/2012 at 08:53 AM

---
**内容**: xiaodong said in reply to Hanauer...
Hi Hanauer,
I have posted a similar demo in .NET. Hope it helps:
http://adndevblog.typepad.com/autocad/2013/04/obtaining-the-top-level-object-in-cao-using-net.html
Reply
04/03/2013 at 09:14 PM

---
**内容**: Hanauer said...
Sorry for my bad english.
Its possible create an entity link with DBDictionaty ObjectId?
I'm tried this:

using (Transaction tr = _database.TransactionManager.StartTransaction())
{
DBDictionary dictNODKey = null;
try
{
// open the named object dictionary
dictNODKey = (DBDictionary)tr.GetObject(_linkDictionaryNodObjectId, OpenMode.ForWrite);
}
catch
{
this.GetLinkDictionaryNodObjectId();
dictNODKey = (DBDictionary)tr.GetObject(_linkDictionaryNodObjectId, OpenMode.ForWrite);
}
DBDictionary dictNumber = null;
try
{
dictNumber = (DBDictionary)tr.GetObject(dictNODKey.GetAt(Convert.ToString(number)), OpenMode.ForWrite);
}
catch
{
dictNODKey.UpgradeOpen();
dictNumber = new DBDictionary();
dictNODKey.SetAt(Convert.ToString(number), dictNumber);
tr.AddNewlyCreatedDBObject(dictNumber, true);
try
{
ObjectId dictNumberId = dictNumber.ObjectId;
CAO.Link link = _linkTemplate.CreateLink(dictNumberId.OldId, keyValues);
// CAO.Link link = _linkTemplate.CreateLink(id1.OldId, keyValues);
ObjectId linkObjectId = new ObjectId(link.ObjectID);
_lom.Add(number, linkObjectId);
}
catch (System.Exception ex)
{
MessageBox.Show(ex.ToString());
}
}
// save the new objects to the database
tr.Commit();
}
and not works. Give this exception: "System.Runtime.InteropServices.COMException (0xC022001F): Failed to create link at CAO.LinkTemplateClass.CreateLink(Int32 ObjectID, KeyValues pKeyValues)".
The same above routine works when the link is create to common entities, like lines, circles, blockreferences, etc.
Why is not possible do create an entity link with dictionaries objectIds?
Thanks.
Hanauer.
Reply
03/01/2013 at 11:55 AM

---
