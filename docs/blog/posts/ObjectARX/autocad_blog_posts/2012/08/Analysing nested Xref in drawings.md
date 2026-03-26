---
title: "Analysing nested Xref in drawings"
date: 2012-08-01
categories:
  - AutoCAD
tags:
  - DWG
  - Plot
  - XREF
description: "When a drawing has nested external references to other drawings, you may want to know the Xref dependencies that exist within the Xref nodes. For e..."
author: Autodesk
---
# Analysing nested Xref in drawings

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/analysing-nested-xref-in-drawings.html

## 文章内容

By Balaji Ramamoorthy
When a drawing has nested external references to other drawings, you may want to know the Xref dependencies that exist within the Xref nodes. For example :  Consider three drawings A, B and C where A is the main drawing, B is an external reference in A and C is an external reference in B. In this case, traversing the Xref graph of A will provide Xref graph nodes for A, B and C, but you may need to be able to get that B is the parent of C and is inserted in A.
Here is a sample code :
<CommandMethod("AnalyseXrefGraph")> _
       Public Shared Sub AnalyseXRefGraphMethod()
    Dim relations As Dictionary(Of [String], [String]) = New Dictionary(Of String, String)()
    AnalyseXref("c:\Temp\Test.dwg", "Test", relations)
      ' Print the results
    Dim ed As Editor = Application.DocumentManager.MdiActiveDocument.Editor
    For Each kv As KeyValuePair(Of [String], [String]) In relations
        ed.WriteMessage([String].Format(vbLf & "{0} - {1}", kv.Key, kv.Value))
    Next
End Sub
  Public Shared Sub AnalyseXref(ByVal drawingFilePath As [String], ByVal baseNodeName As [String], ByRef relations As Dictionary(Of [String], [String]))
    Dim doc As Document = Application.DocumentManager.MdiActiveDocument
    Dim ed As Editor = doc.Editor
      Using db As New Database(False, True)
        db.ReadDwgFile(drawingFilePath, FileOpenMode.OpenForReadAndWriteNoShare, False, "")
        db.ResolveXrefs(True, False)
          Using tr As Transaction = db.TransactionManager.StartTransaction()
            Dim xg As XrefGraph = db.GetHostDwgXrefGraph(True)
            Dim root As GraphNode = xg.RootNode
              Dim numOfNodes As Integer = xg.NumNodes
              For cnt As Integer = 0 To xg.NumNodes - 1
                Dim node As XrefGraphNode = TryCast(xg.GetXrefNode(cnt), XrefGraphNode)
                If Not node.Database.Filename.Equals(drawingFilePath) Then
                    AnalyseXref(node.Database.Filename, node.Name, relations)
                End If
                  If Not node.IsNested Then
                    If Not relations.ContainsKey(node.Name) Then
                        relations.Add(node.Name, baseNodeName)
                    End If
                End If
            Next
            tr.Commit()
        End Using
    End Using
End Sub
Consider a drawing "Test.dwg" that has external references to other drawings as shown in this graph.
The above code snippet will then print the Xref dependencies as :

## 评论

**内容**: ally said...
Is it possible to do this from an external exe using interop?
Reply
05/25/2013 at 03:16 PM

---
