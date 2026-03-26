---
title: "Binding external references"
date: 2012-12-01
categories:
  - AutoCAD
tags:
  - API
  - Database
  - XREF
description: "API “Database.BindXrefs” can be used to bind the resolved external references. Below code shows the sample code to use “BindXrefs” API."
author: Autodesk
---
# Binding external references

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/binding-external-references.html

## 文章内容

By Virupaksha Aithal
API “Database.BindXrefs” can be used to bind the resolved external references. Below code shows the sample code to use “BindXrefs” API.
[CommandMethod("BX")]
public void BindXrefs()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
      ObjectIdCollection xrefCollection = new ObjectIdCollection();
      using (XrefGraph xg = db.GetHostDwgXrefGraph(false))
    {
        int numOfNodes = xg.NumNodes;
        for (int cnt = 0; cnt < xg.NumNodes; cnt++)
        {
            XrefGraphNode xNode = xg.GetXrefNode(cnt)
                                                as XrefGraphNode;
            if (!xNode.Database.Filename.Equals(db.Filename))
            {
                if (xNode.XrefStatus == XrefStatus.Resolved)
                {
                    xrefCollection.Add(xNode.BlockTableRecordId);
                }
            }
        }
    }
      if(xrefCollection.Count != 0)
        db.BindXrefs(xrefCollection, true);
  }

## 评论

**内容**: KH said...
What class do I have to invite
ObjectIdCollection xrefCollection = new ObjectIdCollection();
Was für Klasse muss ich da laden
Reply
12/07/2012 at 01:06 AM

---
**内容**: badziewiak said in reply to KH...
Autodesk.AutoCAD.DatabaseServices from acdbmgd.dll.
Reply
12/07/2012 at 01:45 AM

---
**内容**: KH said...
Thank you but that is loaded
Danke das ist aber geladen
Reply
12/07/2012 at 02:54 AM

---
**内容**: badziewiak said in reply to KH...
using Autodesk.AutoCAD.DatabaseServices;
...
ObjectIdCollection xrefCollection = new ObjectIdCollection();
or
Autodesk.AutoCAD.DatabaseServices.ObjectIdCollection xrefCollection = new Autodesk.AutoCAD.DatabaseServices.ObjectIdCollection();
Reply
12/07/2012 at 06:44 AM

---
**内容**: KH said in reply to badziewiak...
No. Unfortunately this is not even
Danke
Nein geht leider auch nicht
Reply
12/07/2012 at 07:09 AM

---
