---
title: "Determining xref hierarchy using ObjectARX"
date: 2012-08-01
categories:
  - AutoCAD C++
tags:
  - Block
  - C++
  - ObjectARX
  - Plot
  - XREF
description: "To iterate through the drawing and pull out all the attached xrefs and to determine the level of hierarchy of each xref, here is a sample code. For..."
author: Autodesk
---
# Determining xref hierarchy using ObjectARX

发布日期: 2012-08-01

原始链接: https://adndevblog.typepad.com/autocad/2012/08/determining-xref-hierarchy-using-objectarx.html

## 文章内容

By Balaji Ramamoorthy
To iterate through the drawing and pull out all the attached xrefs and to determine the level of hierarchy of each xref, here is a sample code. For example, an xref named xref1 in a drawing which in turn has xref2 and xref3 attached within it, you can find out if xref1 is the parent, and xref2 and xref3 are the children.
A class, AcDbXrefGraph, facilitates the traversal of a drawing's xref hierarchy. The graph's nodes allow access to information corresponding to an xref's block table record. One stipulation, though, is that the graph maps singular parent-child linkages, even for xrefs that are multiply referenced in the current drawing. Therefore, only one parent xref will be recognized and graphed for each child xref.
The following code steps through the branches of an xref graph and prints the xref node names:
// - AdskXrefGraph._XRG command
// Command to print Xref graph as a table
static void AdskXrefGraph_XRG(void)
{
    Acad::ErrorStatus es = Acad::eOk;
    AcDbXrefGraph graph;
    AcDbXrefGraphNode *node;
      TCHAR status[32];
    TCHAR nested[12];
      es = acedGetCurDwgXrefGraph(graph);
      acutPrintf(_T("Number of nodes: %d\n\n"), graph.numNodes());
    acutPrintf
    (
        _T("%3s%10s%15s%10s%12s\n"),
        _T("#"),
        _T("Name"),
        _T("Status"),
        _T("BTR ID"),
        _T("Nested")
    );
      for (int i=0; i<graph.numNodes(); i++)
    {
        node = graph.xrefNode(i);
          if (node != NULL)
        {
            switch(node->xrefStatus())
            {
            case AcDb::kXrfResolved :
                _stprintf(status, _T("Resolved\0"));
                break;
            case AcDb::kXrfUnloaded :
                _stprintf(status, _T("Unloaded\0"));
                break;
            case AcDb::kXrfUnreferenced :
                _stprintf(status, _T("Unreferenced\0"));
                break;
            case AcDb::kXrfFileNotFound :
                _stprintf(status, _T("File not found\0"));
                break;
            case AcDb::kXrfUnresolved :
                _stprintf(status, _T("Unresolved\0"));
                break;
            default :
                _stprintf
                (
                    status,
                    _T("Unknown(%d)\0"),
                    node->xrefStatus()
                );
            }
              if (node->btrId() == 0)
                _stprintf(nested, _T("(root dwg)\0"));
            else
                _stprintf(   
                            nested,
                            node->isNested() ? _T("Yes\0"):_T("No\0"));
              acutPrintf(_T("%3d%10s%15s%10d%12s\n"), i, node->name(), status, node->btrId(), nested);
        }
    }
}
  // - AdskXrefGraph._PXRG command (do not rename)
// Command that prints the Xref graph as a tree
static void AdskXrefGraph_PXRG(void)
{
    AcDbXrefGraph graph;
      acedGetCurDwgXrefGraph(graph);
      if (graph.numNodes() <= 1)
        return;
      acutPrintf(_T("\n"));
    printNode(graph.hostDwg(), graph.numNodes(), 0);
}
  static void printNode(AcDbXrefGraphNode *node, int numNodes, int depth)
{
    for (int i=1; i<= depth; i++)
        acutPrintf(_T("   |"));
    acutPrintf(_T("-> %s\n"), node->name());
    if (node->numOut() > 0)
    {
        AcDbXrefGraphNode *nextNode;
        for (int i=0; i<node->numOut(); i++)
        {
            nextNode = (AcDbXrefGraphNode *) node->out(i);
            if (nextNode != NULL)
                printNode(nextNode, numNodes, depth+1);
        }
    }
}

