---
title: "Bridging the .NET Core and AutoCAD 2025: Exposing and Using COM Server Components with GetInterfaceObject"
date: 2024-12-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - COM
description: "In this blog post, we will explore how to expose COM server components in .NET Core and utilize them in AutoCAD using GetInterfaceObject."
author: Autodesk
---
# Bridging the .NET Core and AutoCAD 2025: Exposing and Using COM Server Components with GetInterfaceObject

发布日期: 2024-12-01

原始链接: https://adndevblog.typepad.com/autocad/2024/12/bridging-the-net-core-and-autocad-2025-exposing-and-using-com-server-components-with-getinterfaceobject.html

## 文章内容

By Madhukar Moogala
In this blog post, we will explore how to expose COM server components in .NET Core and utilize them in AutoCAD using GetInterfaceObject.
Why Use COM in .NET Core?
COM (Component Object Model) provides a standardized way for software components to communicate, making it a popular tool for extending AutoCAD. For decades, it has been used to create external out-of-process applications and automate AutoCAD workflows.
While the .NET Framework offered seamless support for COM, achieving the same functionality in .NET Core or .NET 5+ requires additional effort. This blog post addresses how to migrate and expose COM components in the modern .NET environment.
We will reference Kean's old COM sample project, which works well in .NET Framework 4.8 but encounters issues in .NET 8.0. This post aims to bridge that gap.
As an example, we will create a COM server to calculate the value of Pi and use it within AutoCAD.
Step 1: Create a COM Server in .NET Core
Define Interfaces
To make AutoCAD compatible, we implement a fake IDispatch interface:
00020400-0000-0000-C000-000000000046 is special GUID of IDispatch
  
    [ComVisible(true)]
    [Guid("00020400-0000-0000-C000-000000000046")]
    [InterfaceType(ComInterfaceType.InterfaceIsIDispatch)]
    public interface IDispatch
    {
        [DispId(1)]
        void GetTypeInfoCount(out int pctinfo);
        [DispId(2)]
        void GetTypeInfo(int iTInfo, int lcid, out IntPtr info);
        [DispId(3)]
        void GetIDsOfNames(ref Guid riid, ref IntPtr rgszNames, int cNames, int lcid, ref IntPtr rgDispId);
        [DispId(4)]
        void Invoke(int dispIdMember, ref Guid riid,
         int lcid, short wFlags, ref System.Runtime.InteropServices.ComTypes.DISPPARAMS pDispParams,
         out object pVarResult, ref System.Runtime.InteropServices.ComTypes.EXCEPINFO pExcepInfo,
         out int puArgErr);
    }

    [ComVisible(true)]
    [Guid("BA9AC84B-C7FC-41CF-8B2F-1764EB773D4B")]
    [InterfaceType(ComInterfaceType.InterfaceIsIDispatch)]
    public interface IServer : IDispatch
    {
        [DispId(1)]
        double ComputePi();
    }
  
Implement the COM Server
The server calculates Pi using the Leibniz formula:
    
      [ComVisible(true)]
      [Guid("A8DAD545-A841-4EE4-B4DA-AAAC2FDDD305")]
      public class Server : IServer
      {
          double IServer.ComputePi()
          {
              double sum = 0.0;
              int sign = 1;
              for (int i = 0; i < 1024; ++i)
              {
                  sum += sign / (2.0 * i + 1.0);
                  sign *= -1;
              }
              return 4.0 * sum;
          }

          void IDispatch.GetIDsOfNames(ref Guid riid, ref IntPtr rgszNames, int cNames, int lcid, ref IntPtr rgDispId)
           => throw new NotImplementedException();
          void IDispatch.GetTypeInfo(int iTInfo, int lcid, out IntPtr info)
           => throw new NotImplementedException();
          void IDispatch.GetTypeInfoCount(out int pctinfo)
           => throw new NotImplementedException();
          void IDispatch.Invoke(int dispIdMember, ref Guid riid, int lcid,
          short wFlags, ref System.Runtime.InteropServices.ComTypes.DISPPARAMS pDispParams,
          out object pVarResult, ref System.Runtime.InteropServices.ComTypes.EXCEPINFO pExcepInfo,
          out int puArgErr) => throw new NotImplementedException();
      }
    
  
Step 2: Register the COM Server
Use regsvr32 to register the server *.comhost.dll. Ensure your assembly is visible to COM and has a unique GUID:
    
      [assembly: Guid("A8DAD545-A841-4EE4-B4DA-AAAC2FDDD305")]
      [assembly: TypeLibVersion(1, 0)] //Optional.
    
  
Step 3: Use the Server in AutoCAD
Implement the AutoCAD Plugin
The plugin retrieves the COM server object and uses it to compute Pi:
    
      [CommandMethod("RunDLL")]
      public void RunDLL()
      {
          var doc = Autodesk.AutoCAD.ApplicationServices.Application.DocumentManager.MdiActiveDocument;
          if (doc == null)
              return;
      
          var editor = doc.Editor;
          dynamic acadObj = Autodesk.AutoCAD.ApplicationServices.Application.AcadApplication;
      
          if (acadObj != null)
          {
              try
              {
                  IServer serverObj = acadObj.GetInterfaceObject("COMServer.Server") as IServer;
                  if (serverObj != null)
                  {
                      double pi = serverObj.ComputePi();
                      editor.WriteMessage("\nPi: " + pi);
                  }
              }
              catch (Exception ex)
              {
                  editor.WriteMessage("\nError: " + ex.Message);
              }
          }
      }
    
  
Key Takeaways
Fake IDispatch Interface: Necessary for AutoCAD’s compatibility.
COM Server Registration: Ensures discoverability by AutoCAD.
Please refer GitHub repo for further details.
For more information, please refer to Microsoft article on COM Component in .NET core

