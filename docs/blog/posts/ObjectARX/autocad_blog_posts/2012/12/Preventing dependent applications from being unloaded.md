---
title: "Preventing dependent applications from being unloaded"
date: 2012-12-01
categories:
  - AutoCAD C++
tags:
  - C++
  - ObjectARX
description: "Consider this scenario:  Your custom object is contained within a DBX module and its user interface is in a separate ARX module. How do you ensure ..."
author: Autodesk
---
# Preventing dependent applications from being unloaded

发布日期: 2012-12-01

原始链接: https://adndevblog.typepad.com/autocad/2012/12/preventing-dependent-applications-from-being-unloaded.html

## 文章内容

By Gopinath Taget
Consider this scenario:  Your custom object is contained within a DBX module and its user interface is in a separate ARX module. How do you ensure that the DBX module can't be unloaded before
the ARX module unloads.
The solution is to load one ARX/DBX module from another. You can use AcRxDynamicLinker::loadModule() or AcRxDynamicLinker::loadApp() to respond to the AcRx::kInitAppMsg message in the acrxEntryPoint() function of your module.
This should be paired with AcRxDynamicLinker::unloadModule or
AcRxDynamicLinker::unloadApp respectively to unload the module when you have finished it (usually in response to AcRx::kUnloadAppMsg). The choice of function (loadApp or loadModule) depends on your application configuration. Lets look at both cases:
The loadApp/unloadApp approach:
loadApp can be used when the module you want to use has a registry entry (You should refer to the ObjectARX help files for detailed information about this function). The trick is to set the asCmd parameter to false. This means that if the module is already loaded, its reference counter will be incremented. Such a call would look something like this:
acrxDynamicLinker->loadApp("APPNAME",
   AcadApp::LoadReasons::kOnLoadRequest,
   Adesk::kTrue, Adesk::kFalse);
To unload the module you must call unloadApp with its asCmd parameter also set to false. The corresponding unloadApp call to the loadApp call shown above is:
acrxDynamicLinker->unloadApp("APPNAME",
   Adesk::kFalse);
This will decrement the module's reference counter. The module will only unload if its reference counter reduces to zero. In this way, you can ensure that this module will only unload once every application that has loaded it has unloaded it.
The loadModule/unloadModule approach:
loadModule works in exactly the same way as loadApp (refer to the helpfiles for full details), but it does not require the loaded module to have a registry entry. Instead, it requires the module's pathname. Unfortunately, loadModule does not search the AutoCAD search path, so you have to provide the full absolute pathname. If your module is in the AutoCAD search path, you can use the following function to find and load it:
// Parameter "name" is name of dbx application
 bool loadDependentModules(const ACHAR * name)   
{   
  ACHAR full_app_file_name[512] = L"";   
  if (RTNORM != acedFindFile(name, full_app_file_name))   
  {       
   acutPrintf(L"\nCouldn't find path for %s",name);       
   return false;   
  }   
  if (!acrxDynamicLinker->loadModule(
   full_app_file_name,
   Adesk::kTrue,Adesk::kFalse)
   )   
  {       
   acutPrintf(L"\nloadModule %s failed",
    full_app_file_name);       
   return false;   
  }       
  return true;
}
Unfortunately, using the acedFindFile() means that the above code will only work from an ARX application (not a DBX module). Therefore, DBX modules should either use loadApp/unloadApp, or use a full pathname in loadModule.

