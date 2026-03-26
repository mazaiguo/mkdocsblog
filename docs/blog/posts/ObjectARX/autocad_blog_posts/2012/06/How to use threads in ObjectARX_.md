---
title: "How to use threads in ObjectARX?"
date: 2012-06-01
categories:
  - AutoCAD .NET
tags:
  - C++
  - ObjectARX
description: "How do I call an AutoCAD command from a background thread? When I try to call AcApDocManager::sendStringToExecute(), it causes AutoCAD to terminate..."
author: Autodesk
---
# How to use threads in ObjectARX?

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/how-to-use-threads-in-objectarx.html

## 文章内容

By Adam Nagy
How do I call an AutoCAD command from a background thread? When I try to call AcApDocManager::sendStringToExecute(), it causes AutoCAD to terminate unexpectedly.
Solution
The AutoCAD API functions are not thread safe - i.e. they do not expect to be called from a thread other than the main one.
You can create your own threads for background processing, but if you need to call an ARX function (even just to execute an AutoCAD command), then you need to marshal that call to the main thread.
We have a DevNote on this topic concerning .NET AddIns called "Use Thread for background processing", and you can handle this situation in ARX in a similar fashion.
You could write a helper class that creates a message only window, that could be used to invoke AutoCAD functions on the main thread.
class MyInvoker
{
public:
  MyInvoker()
  {
    WNDCLASS wndclass = {0};
    wndclass.hInstance     = _hdllInstance ;
    wndclass.lpfnWndProc   = wndProcedure;
    wndclass.lpszClassName = L"MessageOnlyWindow";
      // Register the class
    ATOM a = RegisterClass(&wndclass);
      // Create the window object
    _hwnd = CreateWindow(L"MessageOnlyWindow",
      NULL,
      NULL,
      CW_USEDEFAULT,
      CW_USEDEFAULT,
      CW_USEDEFAULT,
      CW_USEDEFAULT,
      NULL,
      NULL,
      _hdllInstance,
      NULL);
  }
    ~MyInvoker()
  {
    DestroyWindow(_hwnd);
  }
    typedef void (*CallbackFunctionType)();
  void InvokeSync(CallbackFunctionType funcPtr)
  {
    SendMessage(_hwnd, _wm, 0, (LPARAM)funcPtr);
  }
  private:
  HWND _hwnd;
  static DWORD _wm;
  static LRESULT CALLBACK wndProcedure(
    HWND hWnd, UINT Msg, WPARAM wParam, LPARAM lParam)
  {
    if (Msg == _wm)
    {
      CallbackFunctionType funcPtr = (CallbackFunctionType)lParam;
      (*funcPtr)();
    }
      return DefWindowProc(hWnd, Msg, wParam, lParam);
  }
};
DWORD MyInvoker::_wm = RegisterWindowMessage(L"MyInvokeMessage");
// a global instance of the helper class
MyInvoker * g_myInvoker;
Create an instance of this class in the kInitAppMsg
virtual AcRx::AppRetCode On_kInitAppMsg (void *pkt)
{
  // TODO: Load dependencies here
    // You *must* call On_kInitAppMsg here
  AcRx::AppRetCode retCode =AcRxArxApp::On_kInitAppMsg(pkt);
    // TODO: Add your initialization code here
  g_myInvoker = new MyInvoker();
    return (retCode) ;
}
And delete it in the kUnloadAppMsg
virtual AcRx::AppRetCode On_kUnloadAppMsg (void *pkt)
{
  // TODO: Add your code here
    // You *must* call On_kUnloadAppMsg here
  AcRx::AppRetCode retCode =AcRxArxApp::On_kUnloadAppMsg(pkt);
    // TODO: Unload dependencies here
  delete g_myInvoker;
    return (retCode) ;
}
You would need to place the ARX calls into a seperate function that then could be invoked on the main thread. Note that now we are in session/application context so if you wanted to modify the database you would need to lock the document
void acadFunctionCalls()
{
  AcApDocument * activeDoc = acDocManager->mdiActiveDocument();   
    acDocManager->sendStringToExecute(
    activeDoc,
    L"\x03\x03(command \"LINE\" \"0,0\" \"100,100\" \"\") "); 
}
Here is the function that the background thread will execute
UINT thread( LPVOID pParam )
{
  // we are doing some calculations in the thread
  Sleep(3000);
    // now we want to call some AutoCAD functions
  g_myInvoker->InvokeSync(acadFunctionCalls);
    return (0);  //exit from thread       
}
And here is the AutoCAD command that will start the background thread
static void MfcThreadTest_StartThread(void)
{
  AfxBeginThread(thread,NULL,THREAD_PRIORITY_LOWEST);
}

