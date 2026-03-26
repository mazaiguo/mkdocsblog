---
title: "Reactors using AutoCAD Javascript API"
date: 2013-03-01
categories:
  - AutoCAD
tags:
  - API
  - AutoCAD
  - JavaScript
description: "You must have read that the AutoCAD 2014 has introduced the Javascript API for AutoCAD. Here is a short example demonstrating the use of reactors. ..."
author: Autodesk
---
# Reactors using AutoCAD Javascript API

发布日期: 2013-03-01

原始链接: https://adndevblog.typepad.com/autocad/2013/03/reactors-using-autocad-javascript-api.html

## 文章内容

By Balaji Ramamoorthy
You must have read that the AutoCAD 2014 has introduced the Javascript API for AutoCAD. Here is a short example demonstrating the use of reactors. In this example, we hook/unhook the ObjectModified reactor to a selected entity.
To try this, copy the code to a file and save it as a .js (javascript) file. Start AutoCAD 2014 and run the "WEBLOAD" command and load the js file. Run the "STARTMONITOR" command and select an entity. The "ObjectModified" event is now hooked and changes to the entity results in a call to the "onObjectModified" callback function. To unhook the reactor, run the "ENDMONITOR" command and select the same entity.
Here is the js code :
var observedEntities = new Acad.OSet();
  function onObjectModified(eventname, args)
{
    var entity = new Acad.DBEntity(args.id);
    write("Object Modified: " + args.id);
}
  function onCompleteCallback1(jsonPromptResult)
 {
    var resultObj = JSON.parse(jsonPromptResult);
      if (resultObj)
    {
        if (resultObj.status == 5100)
        {
            observedEntities.add(resultObj.objectId);
              Acad.Application.activedocument.startObserving(
                observedEntities,
                Acad.Application.activedocument.eventname.modified,
                onObjectModified);
        }
    }
}
  function onErrorCallback1(jsonPromptResult)
{
    var resultObj = JSON.parse(jsonPromptResult);
    if (resultObj)
    {
        write("OnError");
    }
}
  function StartMonitorFunction()
{
    try
    {
        var peo = new Acad.PromptEntityOptions();
        peo.setMessageAndKeywords("\nSelect an Entity", "");
        peo.rejectMessage = "\nInvalid selection...";
          peo.singlePickInSpace = true;
        peo.allowObjectOnLockedLayer = true;
          Acad.Editor.getEntity(peo).then(onCompleteCallback1,
                                        onErrorCallback1);
    }
    catch (e)
    {
        write(e.message);
    }
}
  function onCompleteCallback2(jsonPromptResult)
{
    var resultObj = JSON.parse(jsonPromptResult);
      if (resultObj)
    {
        if (resultObj.status == 5100)
        {
            observedEntities.remove(resultObj.objectId);
              var observedEntities1 = new Acad.OSet();
            observedEntities1.add(resultObj.objectId);
              Acad.Application.activedocument.stopObserving(
                observedEntities1,
                Acad.Application.activedocument.eventname.modified,
                onObjectModified);
        }
    }
}
  function onErrorCallback2(jsonPromptResult)
{
    var resultObj = JSON.parse(jsonPromptResult);
    if (resultObj) {
        write("OnError");
    }
}
  function EndMonitorFunction()
{
    try
    {
        var peo = new Acad.PromptEntityOptions();
        peo.setMessageAndKeywords("\nSelect an Entity", "");
        peo.rejectMessage = "\nInvalid selection...";
          peo.singlePickInSpace = true;
        peo.allowObjectOnLockedLayer = true;
          Acad.Editor.getEntity(peo).then(onCompleteCallback2,
                                        onErrorCallback2);
    }
    catch (e)
    {
        write(e.message);
    }
}
  Acad.Editor.addCommand("REACTOR_CMDS",
                        "STARTMONITOR",
                        "STARTMONITOR",
                        Acad.CommandFlag.TRANSPARENT,
                        StartMonitorFunction);
  Acad.Editor.addCommand("REACTOR_CMDS",
                        "ENDMONITOR",
                        "ENDMONITOR",
                        Acad.CommandFlag.TRANSPARENT,
                        EndMonitorFunction);
  write("\nRegistered StartMonitor/EndMonitor commands.\n");

