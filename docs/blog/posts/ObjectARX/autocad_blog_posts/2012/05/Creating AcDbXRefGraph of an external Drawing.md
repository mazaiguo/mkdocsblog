---
title: "Creating AcDbXRefGraph of an external Drawing"
date: 2012-05-01
categories:
  - AutoCAD C++
tags:
  - Block
  - C++
  - DWG
  - Database
  - ObjectARX
description: "The "acedGetCurDwgXrefGraph" method in ObjectARX creates an AcDbXRefGraph of the current drawing. To create an AcDbXrefGraph of an external drawing..."
author: Autodesk
---
# Creating AcDbXRefGraph of an external Drawing

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/creating-acdbxrefgraph-of-an-external-drawing.html

## 文章内容

By Balaji Ramamoorthy
The "acedGetCurDwgXrefGraph" method in ObjectARX creates an AcDbXRefGraph of the current drawing. To create an AcDbXrefGraph of an external drawing that has been read in using "readDwgFile", there are two approaches.
In the first method, you only need to set the working database temporarily to the in-memory database and reset it back to its old value soon after the Xref graph has been obtained.
The second method is more elaborate and creates the Xref graph by traversing through the block table records and adds Xref nodes to the graph based on whether the block table record represents an external reference.
Here is a sample code to demonstrate the first approach :
AcApDocument *pActiveDoc = acDocManager->mdiActiveDocument();
AcDbDatabase *pCurDb = pActiveDoc->database();
  // lock the document
AcAxDocLock docLock;
  // now read in an external drawing
AcDbDatabase *pNewDb = new AcDbDatabase (false);
  // if we created the db ok
if (pNewDb != NULL)
{
    Acad::ErrorStatus es;
      // try and read in the drawing
    es = pNewDb->readDwgFile (ACRX_T("c:\\temp\\A.dwg"));
      // if ok
    if (es == Acad::eOk)
    {
        // Work on the new db from now on
        acdbHostApplicationServices()->setWorkingDatabase(pNewDb);
        acdbResolveCurrentXRefs(pNewDb);
          AcDbXrefGraph graph;
        acedGetCurDwgXrefGraph(graph);
          acutPrintf  (
                        ACRX_T("\nNumber of nodes = %d"),
                        graph.numNodes ()
                    );
        for (int i = 0; i < graph.numNodes(); i++)
        {
            AcDbXrefGraphNode* xrefNode = graph.xrefNode(i);
            if( xrefNode->isNested() == false &&
                xrefNode->xrefStatus() == AcDb::XrefStatus::kXrfResolved)
            {
                acutPrintf (ACRX_T("\n%s"), xrefNode->name());
            }
        }     
          // Restore old database
        acdbHostApplicationServices()->setWorkingDatabase(pCurDb);
          // and delete the in-memory db.
        delete pNewDb;
    }
}
Here is the sample code for the second approach :
static void AdsProjectGenXrefGraph(void)
{
    // lock the document
    AcAxDocLock docLock;
      // now read in an external drawing
    AcDbDatabase *db = new AcDbDatabase (false);
      // if we created the db ok
    if (db != NULL)
    {
        Acad::ErrorStatus es;
          // try and read in the drawing
        es = db->readDwgFile (ACRX_T("c:\\temp\\A.dwg"));
          // if ok
        if (es == Acad::eOk)
        {
            AcDbXrefGraph graph;
              // try out our new function
            GetXrefGraph (db, graph);
              acutPrintf  (
                            ACRX_T("\nNumber of nodes = %d"),
                            graph.numNodes ()
                        );
            for (int i = 0; i < graph.numNodes(); i++)
            {
                AcDbXrefGraphNode* xrefNode = graph.xrefNode(i);
                if( xrefNode->isNested() == false &&
                    xrefNode->xrefStatus()
                            == AcDb::XrefStatus::kXrfResolved)
                {
                    acutPrintf (ACRX_T("\n%s"), xrefNode->name());
                }
            }     
        }
        delete db;
    }
}
  static Acad::ErrorStatus GetXrefGraph (
                                        AcDbDatabase *dwgDb,
                                        AcDbXrefGraph& graph
                                      ) throw ()
{
    Acad::ErrorStatus es = Acad::eOk;
    try
    {
        // The following function call will resolve all
        // the Xrefs in the database
        acedXrefResolve(dwgDb,true);
          // delete all of the nodes and cycle nodes, and
        // reset the graph to being empty
        graph.reset();
          // Make hostDwg node.
        const ACHAR *fileName;
          // get the dwg file name
        dwgDb->getFilename (fileName);
          // create a new XRef graph node
        AcDbXrefGraphNode *pNode
            = new AcDbXrefGraphNode (
                                        fileName,
                                        AcDbObjectId::kNull,
                                        dwgDb
                                    );
          // add the newly created node to the graph
        if (graph.addNode (pNode) != Acad::eOk)
            throw ErrorCondition();
          // Loop through the host drawing's block table and
        // create a Node for each Xref.
        AcDbSymbolTable *symbolTable = NULL;
          // if not ok
        es = dwgDb->getBlockTable(
                                    (AcDbBlockTable*&)symbolTable,
                                    AcDb::kForRead
                                 );
        if (es != Acad::eOk)
            throw ErrorCondition();
          AcDbSymbolTableIterator *symbolTableIterator = NULL;
          // create a new iterator so we can loop round
        symbolTable->newIterator(symbolTableIterator);
          // if we failed to create a new iterator
        if (symbolTableIterator == NULL)
            return Acad::eOutOfMemory; 
          // now loop through the records
        for (; !symbolTableIterator->done();
                                    symbolTableIterator->step())
        { 
            AcDbBlockTableRecord *blockTableRec = NULL; 
              // get the block record we are on
            es = symbolTableIterator->getRecord
                    (
                        (AcDbSymbolTableRecord*&)blockTableRec,
                        AcDb::kForRead
                    );
              // if not ok
            if (es != Acad::eOk)
                throw ErrorCondition();
              // if the block table record is indicating an XRef 
            if (blockTableRec->isFromExternalReference())
            {  
                const ACHAR *pName;
                  // get the name of the xref, if not ok
                es = blockTableRec->getName(pName);
                  // if not ok
                if (es != Acad::eOk)
                    throw ErrorCondition();
                  // create a new node
                pNode = new AcDbXrefGraphNode
                            (   
                                pName,
                                blockTableRec->objectId(),
                                blockTableRec->xrefDatabase(),
                                blockTableRec->xrefStatus()
                            );
                  // and add this xref to the tree, if not ok
                es = graph.addNode(pNode);
                  // if not ok
                if (es != Acad::eOk)
                throw ErrorCondition();  
            }
              // tidy up
            blockTableRec->close();
        }
          // tidy up
        delete symbolTableIterator;
        symbolTable->close();
          // Now that the graph has been constructed,
        // we need to find and add edges
        AcDbDatabase      *pDb = NULL;
        AcDbXrefGraphNode *pThisNode = NULL;
        AcDbVoidPtrArray   dupList;
          int i
            = (graph.hostDwg()->btrId() == AcDbObjectId::kNull) ? 1 : 0;
        for (; i < graph.numNodes(); i++)
        {
            pThisNode = graph.xrefNode(i);
              AcDbBlockTableRecord *blockTableRec = NULL; 
            es = acdbOpenAcDbObject
                        (
                            (AcDbObject*&)blockTableRec,
                            pThisNode->btrId(),
                            AcDb::kForRead
                        );
              // if not ok
            if (es != Acad::eOk)
                throw ErrorCondition(); 
              dupList.setLogicalLength(0);
            AcDbBlockReferenceIdIterator *blockRefIdIterator = NULL;
            blockTableRec->newBlockReferenceIdIterator
                                        (
                                            blockRefIdIterator
                                        );
            if (blockRefIdIterator == NULL)
            {
                return Acad::eOutOfMemory;
            }
              for (; !blockRefIdIterator->done();
                                    blockRefIdIterator->step())
            {  
                es = blockRefIdIterator->getDatabase(pDb);
                  // if not ok
                if (es != Acad::eOk)
                    throw ErrorCondition();
                  pNode = graph.xrefNode(pDb);
                  // make sure we have a valid node and the xref is resolved
                if (pNode != NULL && pNode->xrefStatus()
                                        == AcDb::kXrfResolved)
                {   
                    // There could be more than one BlockRef
                    // from the same database
                    if (!dupList.contains(pNode))
                    {
                        es = graph.addEdge(pNode, pThisNode);
                          // if not ok
                        if (es != Acad::eOk)
                            throw ErrorCondition();
                          dupList.append(pNode);
                    }
                }
            }
              // clean up
            delete blockRefIdIterator;
            blockTableRec->close();
        }
    }
    catch (...)
    {
        return es;
    }
      // everything worked!!
    return Acad::eOk;
}

