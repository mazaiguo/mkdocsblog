---
title: "Dynamic P/Invoke for custom native exported methods"
date: 2012-05-01
categories:
  - AutoCAD C++
tags:
  - API
  - AutoCAD
  - C++
  - ObjectARX
description: "When P/Invoking an exported ObjectARX or Win32 method, you usually do not need to specify the full path of the dll/executable that contains that me..."
author: Autodesk
---
# Dynamic P/Invoke for custom native exported methods

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/dynamic-pinvoke-for-custom-native-exported-methods.html

## 文章内容

By Philippe Leefsma
  When P/Invoking an exported ObjectARX or Win32 method, you usually do not need to specify the full path of the dll/executable that contains that method, as it will be already loaded either by AutoCAD or the operating system in case of a Win32 API.
Here is a couple of examples:
[DllImport("user32.dll",
    CharSet = CharSet.Auto,
    CallingConvention = CallingConvention.StdCall)]
public static extern int SetWindowsHookEx(
    int idHook, HookFunc lpfn, IntPtr hInstance, int threadId);
  [DllImport("acad.exe",
    CharSet = CharSet.Unicode,
    CallingConvention = CallingConvention.Cdecl,
    EntryPoint = "acedCmd")]
public static extern int acedCmd(System.IntPtr vlist);
  However it might happen that you have exported a C++ method from one of your custom dll or arx and do not have the dll loaded inside AutoCAD process. In that case you will have to specify the full path of that dll inside the DllImport attribute, as follow:
[DllImport(@"C:\Temp\myDll.dll")]
public static extern int MyExportedMethod();
  We can see that the approach is not convenient, because of the hardcoded path inside the DllImport attribute.
I will expose two ways to workaround that limitation. In order to test them, let’s first create an exported method from a custom arx. It requires 3 steps:
1/ Declare the exported method in some header file:
extern "C" HWND _declspec(dllexport) getViewHandle();
2/ Implement the method:
/////////////////////////////////////////////////////////////
//Use: Exported View Handle
//
/////////////////////////////////////////////////////////////
HWND getViewHandle()
{
       CView *pView = acedGetAcadDwgView();
         if (pView != NULL)
       {
              return pView->m_hWnd;
       }
         return NULL;
}
3/ Declare the exported method in a .def file:
LIBRARY       "myArx"
         EXPORTS getViewHandle
That’s it concerning our custom exported method, we are now able to P/invoke “getViewHandle” from .Net as follow and the arx does not have to be loaded in AutoCAD for this to work:
[DllImport(@"C:\Temp\myDll\myArx.arx",
    CharSet = CharSet.Unicode,
    CallingConvention = CallingConvention.Cdecl,
    EntryPoint = "getViewHandle")]
private static extern IntPtr getViewHandle();
So how to avoid the hardcode path in DllImport?
1/ First approach:  Rely on the SetDllDirectory Win32 API and dynamically specify the path of the dll on your system.
  /////////////////////////////////////////////////////////////
// Use: Dynamic P/Invoke using Win API SetDllDirectory
// Author: Philippe Leefsma
/////////////////////////////////////////////////////////////
[DllImport("Kernel32.dll")]
public static extern bool SetDllDirectory([In]string lpPathName);
  [DllImport("myArx.arx",
    CharSet = CharSet.Unicode,
    CallingConvention = CallingConvention.Cdecl,
    EntryPoint = "getViewHandle")]
private static extern IntPtr getViewHandle();
  [CommandMethod("DllDirPInvoke")]
public void DllDirPInvoke()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      bool b = SetDllDirectory(@"C:\Temp\");
      IntPtr res = getViewHandle();
      ed.WriteMessage("\nViewHandle: " + res.ToString());
}
2/ Handle loading and unloading of the dll yourself using LoadLibraryEx / FreeLibrary, then access the method with GetProcAddress:
  /////////////////////////////////////////////////////////////
// Use: Dynamic P/Invoke
// Author: Philippe Leefsma
/////////////////////////////////////////////////////////////
private const uint LOAD_LIBRARY_AS_DATAFILE = 0x00000002;
private const uint DONT_RESOLVE_DLL_REFERENCES = 0x00000001;
private const uint LOAD_WITH_ALTERED_SEARCH_PATH = 0x00000008;
private const uint LOAD_IGNORE_CODE_AUTHZ_LEVEL = 0x00000010;
private const uint LOAD_LIBRARY_AS_DATAFILE_EXCLUSIVE = 0x00000040;
  [DllImport("kernel32.dll")]
private static extern IntPtr LoadLibraryEx(
    string lpFileName, IntPtr hFile, uint dwFlags);
  [DllImport("kernel32.dll")]
private static extern bool FreeLibrary(IntPtr dllPointer);
  [DllImport("kernel32.dll", CharSet = CharSet.Ansi)]
private static extern IntPtr GetProcAddress(
    IntPtr dllPointer, string functionName);
    //Default calling convention used by interop is __stdcall,
//so need to specify
[UnmanagedFunctionPointerAttribute(CallingConvention.Cdecl)]
private delegate IntPtr DllFuncDelegate();
  [CommandMethod("DynamicPInvoke")]
public void DynamicPInvoke()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      string lpFileName = @"C:\Temp\myArx.arx";
      string FunctionName = "getViewHandle";
      IntPtr moduleHandle = LoadLibraryEx(
        lpFileName,
        IntPtr.Zero,
        LOAD_WITH_ALTERED_SEARCH_PATH);
      if (moduleHandle != IntPtr.Zero)
    {
        IntPtr pProc = GetProcAddress(moduleHandle, FunctionName);
          if (pProc != IntPtr.Zero)
        {
            DllFuncDelegate delegateFunc = (DllFuncDelegate)
                Marshal.GetDelegateForFunctionPointer(
                    pProc,
                    typeof(DllFuncDelegate));
              IntPtr res = delegateFunc();
              ed.WriteMessage("\nView Handle: " + res.ToString());
        }
          bool free = FreeLibrary(moduleHandle);
    }
}

## 评论

**内容**: Mario Minati said...
Hello Philippe,
I'm looking for a way to dynamically handle DLLImport of acedCmd as this has moved into DLL in AC2013, and we would like to circumvent creating different versions for 2012 and 2013.
Is it possible?
How to define the parameters or is it handled by Marshal.GetDelegateForFunctionPointer?
Do we have to skip FreeLibrary as we use the method later on?
Or won't it work this way at all? Would there be a different way?
Many questions :-)

Best greets,
Mario
Reply
01/12/2013 at 12:45 PM

---
**内容**: Alexander Rivilis said...
Hi, Mario!
You can handle version 2012/2013 as far as x86/x64: http://forums.autodesk.com/t5/NET/Determine-32-or-64-bit-application/m-p/3748030#M32834
Reply
01/13/2013 at 10:46 PM

---
**内容**: Philippe Leefsma said...
Hi Mario,
Yes as Alexander pointed out, you can declare several P/Invoke declarations and determine which one to use at run time. The size of IntPtr can be used to determine 32/64 bit platform and ACADVER system variable can be used to determine the AutoCAD version you are running.
You don't need to invoke FreeLibrary in that case, as long as you are dealing with standard dlls that are loaded/unloaded automatically by AutoCAD.
Here is an example of P/Invoking acedCmd:
[System.Runtime.InteropServices.DllImport("acad.exe",
CharSet = System.Runtime.InteropServices.CharSet.Unicode,
CallingConvention = System.Runtime.InteropServices.CallingConvention.Cdecl,
EntryPoint = "acedCmd")]
public static extern int acedCmd(System.IntPtr vlist);

[CommandMethod("ExportDwf")]
public void ExportDwf()
{
object filedia = Application.GetSystemVariable("FILEDIA");
Application.SetSystemVariable("FILEDIA", 0);
ResultBuffer rb = new ResultBuffer();
rb.Add(new TypedValue(5005, "_EXPORT"));
rb.Add(new TypedValue(5005, "C:\\Temp\\Test.dwf"));
rb.Add(new TypedValue(5005, "ALL"));
rb.Add(new TypedValue(5005, "YES"));

acedCmd(rb.UnmanagedObject);
Application.SetSystemVariable("FILEDIA", filedia);
}
Reply
01/14/2013 at 12:03 AM

---
