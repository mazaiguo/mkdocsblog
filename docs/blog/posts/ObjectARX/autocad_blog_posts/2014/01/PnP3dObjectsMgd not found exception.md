---
title: "PnP3dObjectsMgd not found exception"
date: 2014-01-01
categories:
  - Plant 3D
tags:
  - AutoCAD
  - Plant 3D
  - Plugin
description: "If you are developing to AutoCAD Plant 3D 2014 you may have faced the issue below: ‘Could not load file or assembly PnP3dObjectsMgd (….)’."
author: Autodesk
---
# PnP3dObjectsMgd not found exception

发布日期: 2014-01-01

原始链接: https://adndevblog.typepad.com/autocad/2014/01/pnp3dobjectsmgd-not-found-exception.html

## 文章内容

By Augusto Goncalves
If you are developing to AutoCAD Plant 3D 2014 you may have faced the issue below: ‘Could not load file or assembly PnP3dObjectsMgd (….)’.
A little background information: starting on 2014 release, some vertical products, like Plant 3D, are launched in plain AutoCAD with a startup modifier. This is know as configurable AutoCAD, see more details at this blog post. That way, the AutoCAD folder will have a subfolder /PLNT3D/ with the Plant 3D specific DLL.
But there is a know issue where AutoCAD Plant 3D may not load some required DLLs when a plugin needs it, causing the error message mentioned.
A small trick to solve this exception is ‘help’ Plant 3D find the required DLLs. To do so, create a modify your custom class that implements IExtensionApplication. Inside the Initialize method, include:
void IExtensionApplication.Initialize()
{
    AppDomain.CurrentDomain.AssemblyResolve 
        += CurrentDomain_AssemblyResolve;
}
Now we can customize how and where the .NET engine will search for assemblies it could not find. We just want to include the /PLNT3D/. That can be done in several ways, here is a example:
Assembly CurrentDomain_AssemblyResolve(
    object sender, ResolveEventArgs args)
{
    return TryResolvePlant3D(args);
}
 
private Assembly TryResolvePlant3D(
    ResolveEventArgs args)
{
    string name = GetAssemblyName(args);
    string assemblyPath = System.IO.Path.
        Combine(PLNT3DFolder, name + ".dll");
    if (System.IO.File.Exists(assemblyPath))
    {
        Assembly assembly = 
            Assembly.LoadFrom(assemblyPath);
        if (assembly.FullName == args.Name)
            return assembly;
    }
    return null;
}
 
// based on this post
private string GetAssemblyName(ResolveEventArgs args)
{
    String name;
    if (args.Name.IndexOf(",") > -1)
        name = args.Name.Substring(0, args.Name.IndexOf(","));
    else
        name = args.Name;
    return name;
}
 
private string PLNT3DFolder
{
    get
    {
        return System.IO.Path.Combine(
            AppDomain.CurrentDomain.BaseDirectory,
            "PLNT3D");
    }
}

## 评论

**内容**: Alexander Rivilis said...
Hi Augusto! Due to TypePad Editor bug your code is not readable. Please, repost it.
Best Regards!
Reply
01/25/2014 at 05:19 PM

---
**内容**: Augusto Goncalves said in reply to Alexander Rivilis...
Fixed, thanks Alexander!
Reply
01/28/2014 at 03:34 AM

---
