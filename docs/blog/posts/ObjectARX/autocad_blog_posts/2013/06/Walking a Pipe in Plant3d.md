---
title: "Walking a Pipe in Plant3d"
date: 2013-06-01
categories:
  - Plant 3D
tags:
  - .NET
  - Plant 3D
description: "Here’s how to iterate a pipe network in Plant3d…"
author: Autodesk
---
# Walking a Pipe in Plant3d

发布日期: 2013-06-01

原始链接: https://adndevblog.typepad.com/autocad/2013/06/walking-a-pipe-in-plant3d.html

## 文章内容

by Fenton Webb
Here’s how to iterate a pipe network in Plant3d…
First in .NET…
[CommandMethod("PipeWalk")]
public void pipeWalk()
{
  // 4.1 Declare a variable as a PlantProject. Instantiate it using
  // the CurrentProject of PlantApplication
  PlantProject mainPrj = PlantApplication.CurrentProject;
    // 4.2 Declare a Project and instantiate it using 
  // ProjectParts[] of the PlantProject from step 4.1
  // use "Piping" for the name. This will get the Piping project
  Project prj = mainPrj.ProjectParts["Piping"];
    // 4.3 Declare a variable as a DataLinksManager. Instantiate it using
  // the DataLinksManager property of the Project from 4.2.
  DataLinksManager dlm = prj.DataLinksManager;
    //  PipingProject pipingPrj = (PipingProject) mainPrj.ProjectParts["Piping"];
  //  DataLinksManager dlm = pipingPrj.DataLinksManager;
      // Get the TransactionManager
  TransactionManager tm =
  AcadApp.DocumentManager.MdiActiveDocument.Database.TransactionManager;
    // Get the AutoCAD editor
  Editor ed = AcadApp.DocumentManager.MdiActiveDocument.Editor;
    // Prompt the user to select a pipe entity
  PromptEntityOptions pmtEntOpts = new PromptEntityOptions("Select a Pipe : ");
  PromptEntityResult pmtEntRes = ed.GetEntity(pmtEntOpts);
  if (pmtEntRes.Status == PromptStatus.OK)
  {
    // Get the ObjectId of the selected entity
    ObjectId entId = pmtEntRes.ObjectId;
      // Use the using statement and start a transaction
    // Use the transactionManager created above (tm)
    using (Transaction tr = tm.StartTransaction())
    {
        try
      {
          // 4.4 Declare a variable as a Part. Instantiate it using
        // the GetObject Method of the Transaction created above (tr)
        // for the ObjectId argument use the ObjectId from above (entId)
        // Open it for read. (need to cast it to Part)
        Part pPart = (Part)tr.GetObject(entId, OpenMode.ForRead);
          // 4.5 Declare a variable as a PortCollection. Instantiate it
        // using the GetPorts method of the Part from step 4.4.
        // use PortType.All for the PortType.
        PortCollection portCol = pPart.GetPorts(PortType.All); // (PortType.Both);
          // 4.6 Use the WriteMessage function of the Editor created above (ed)
        // print the Count property of the PortCollection from step 4.5.
        // use a string similar to this: "\n port collection count = "
        ed.WriteMessage("\n port collection count = " + portCol.Count);
          // 4.7 Declare a ConnectionManager variable.
        // (Autodesk.ProcessPower.PnP3dObjects.ConnectionManager)
        // Instantiate the ConnectionManager variable by making it
        // equal to a new Autodesk.ProcessPower.PnP3dObjects.ConnectionManager();
        ConnectionManager conMgr = new Autodesk.ProcessPower.PnP3dObjects.ConnectionManager();
          // 4.8 Declare a bool variable named bPartIsConnected and make it false
        bool bPartIsConnected = false;
            // 4.9 Use a foreach loop and iterate through all of the Port in
        // the PortCollection from step 4.5.
        // Note: Put the closing curly brace below step 4.18
        foreach (Port pPort in portCol)
        {
          // 4.10 Use the WriteMessage function of the Editor created above (ed)
          // print the Name property of the Port (looping through the ports)
          // use a string similar to this: "\nName of this Port = " +
          ed.WriteMessage("\nName of this Port = " + pPort.Name);
            // 4.11 Use the WriteMessage function of the Editor created above (ed)
          // print the X property of the Position from the Port
          // use a string similar to this: "\nX of this Port = " +
          ed.WriteMessage("\nX of this Port = " + pPort.Position.X.ToString());
            // 4.12 Declare a variable as a Pair and make it equal to a
          // new Pair().
          Pair pair1 = new Pair();
            // 4.13 Make the ObjectId property of the Pair created in step 4.10
          // equal to the ObjectId of the selected Part (entId)
          pair1.ObjectId = entId;
            // 4.14 Make the Port property of the Pair created in step 4.10
          // equal to the port from the foreach cycle (step 4.7)
          pair1.Port = pPort;
              // 4.15 Use an if else and the IsConnected method of the ConnectionManager
          // from step 4.7. Pass in the Pair from step 4.12
          // Note: Put the else statement below step 4.17 and the closing curly
          // brace for the else below step 4.18
          if (conMgr.IsConnected(pair1))
          {
            // 4.16 Use the WriteMessage function of the Editor (ed)
            // and put this on the command line:
            // "\n Pair is connected "
            ed.WriteMessage("\n Pair is connected ");
              // 4.17 Make the bool from step 4.8 equal to true.
            // This is used in an if statement in step 4.19.
            bPartIsConnected = true;
          }
          else
          {
            // 4.18 Use the WriteMessage function of the Editor (ed)
            // and put this on the command line:
            // "\n Pair is NOT connected "
            ed.WriteMessage("\n Pair is NOT connected ");
          }
          }
            // 4.19 Use an If statement and the bool from step 4.8. This will be
        // true if one of the pairs tested in loop above loop was connected.
        // Note: Put the closing curly brace after step 4.26
        if (bPartIsConnected)
        {
            // 4.20 Declare an ObjectId named curObjID make it
          // equal to ObjectId.Null
          ObjectId curObjId = ObjectId.Null;
              // 4.21 Declare an int name it rowId
          int rowId;
            // 4.22 Declare a variable as a  ConnectionIterator instantiate it
          // using the NewIterator method of ConnectionIterator (Autodesk.ProcessPower.PnP3dObjects.)
          // Use the ObjectId property of the Part from step 4.4
          ConnectionIterator connectIter = ConnectionIterator.NewIterator(pPart.ObjectId);                       //need PnP3dObjectsMgd.dll
            // You could Also use this, need to ensure that pPort is connected
          // Use the ConnectionManager and a Pair as in the example above.
          // conIter = ConnectionIterator.NewIterator(pPart.ObjectId, pPort);
            // 4.23 Use a for loop and loop through the connections in the
          // ConnectionIterator from step 4.22. The initializer can be empty.
          // Use !.Done for the condition. use .Next for the iterator. 
          // Note: Put the closing curly brace after step 4.26
          for (; !connectIter.Done(); connectIter.Next())
          {
              // 4.24 Make the ObjectId from step 4.20 equal to the ObjectId
            // property of the ConnectionIterator
            curObjId = connectIter.ObjectId;
              // 4.25 Make the integer from step 4.21 equal to the return from
            // FindAcPpRowId method of the DataLinksManager from step 4.3.
            // pass in the ObjectId from step 4.24
            rowId = dlm.FindAcPpRowId(curObjId);
              //4.26 Use the WriteMessage function of the Editor (ed)
            // and pring the integer from step 4.25. Use a string similar to this
            // this on the command line:
            // "\n PnId = " +
            ed.WriteMessage("\n PnId = " + rowId);
            }
          }
      }
      catch (System.Exception ex)
      {
          ed.WriteMessage(ex.ToString());
      }
    }
  }
}
  now in C++…
  // Iterate a pipe network (from specific part / port)
void ct_iter_port()
{
  ads_name  entname;
  ads_point pt;
  int ret = acedEntSel(L"\nSelect part on a network: ", entname, pt);
  if (ret != RTNORM)
  {
    return; // cancelled
  }
    AcPp3dConnectionIterator* pIter = NULL;
  try
  {
    AcDbObjectId objId;
    eOkThrow(acdbGetObjectId(objId, entname));
      AcDbObjectPointer<AcPpDb3dPart> pPart(objId, AcDb::kForRead);
    eOkThrow(pPart.openStatus());
      AcPp3dPortArray ports;
    eOkThrow(pPart->getPorts(ports, AcPpDb3dPart::kBoth));
    eOkThrow(pPart.close());
      int index = -1;
    do
    {
      ret = acedGetInt(L"\nEnter the port index: ", &index);
      if (ret != RTNORM)
      {
            return; // cancelled
      }
    } while (index < 0 || index >= ports.length());
      AcPp3dPair pair(objId, ports[index]);
    eOkThrow(AcPp3dConnectionIterator::newIterator(pair, pIter));
    for ( ; !pIter->done(); pIter->next())
    {
      AcDbObjectId curObjId;
      eOkThrow(pIter->getObjectId(curObjId));
        listPart(curObjId);
    }
  }
  catch (const Acad::ErrorStatus& es)
  {
        acutPrintf(L"\nERROR: %d", es);
  }
    if (pIter != NULL)
  {
        delete pIter;
  }
}

