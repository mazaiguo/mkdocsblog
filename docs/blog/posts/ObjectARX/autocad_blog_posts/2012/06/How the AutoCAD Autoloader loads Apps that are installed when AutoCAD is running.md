---
title: "How the AutoCAD Autoloader loads Apps that are installed when AutoCAD is running"
date: 2012-06-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "What you will notice when you install an App off of the AppStore is that AutoCAD (and soon all Autodesk products) “autoload” the installed applicat..."
author: Autodesk
---
# How the AutoCAD Autoloader loads Apps that are installed when AutoCAD is running

发布日期: 2012-06-01

原始链接: https://adndevblog.typepad.com/autocad/2012/06/how-the-autocad-autoloader-loads-apps-that-are-installed-when-autocad-is-running.html

## 文章内容

by Fenton Webb
By now, I’m sure, all of you people out there have taken a look at the Autodesk Exchange App Store… If not I highly recommend that you do so.
What you will notice when you install an App off of the AppStore is that AutoCAD (and soon all Autodesk products) “autoload” the installed applications via an Autoloader module built into the host product. The idea is that all of the App registration is done entirely by the Autodesk product’s Autoloader module and not repeated through thousands of developer’s installer routines around the world, thus allowing for a much easier, more professional and standardized deployment model across all Apps on our store. Another point, because the installers are standardized, we can easily create tools to manage the Apps and even to automatically generate the App installers – indeed, that’s what we do today using the not yet public “Autodesk AppPacker” (APP) tool, 1 minute to create an AutoCAD App installer instead of 1-3 weeks!!!!!
Anyway, back to the the AutoCAD implementation of the Autoloader – the Autoloader module initializes Apps for two specific User scenarios:
OnStartup – Apps are initialized on startup
OnAppearance – Apps are initialized while the host product (AutoCAD say) is already running.
User scenario number two, is fairly interesting, so I want to tell you about it.
In order for a running application to be efficiently notified of a new file or folder appearing on the system you need some sort of notification system. For something like this to work well, you have to be very careful about how you implement it because, without some care, you will either make the host application slow down and/or crash.
So as not to impact the host application performance, it’s best to run those types of folder checks on a separate thread, away from the main thread. The problem with running on a separate (or worker) thread is that when your worker thread eventually needs to carry out work inside the host application (main thread) you have to take extreme care to make sure that the main thread is indeed ready for you, otherwise it will go horribly wrong. As we all know, AutoCAD is not multithreaded so adding multithreaded features takes extreme care, otherwise AutoCAD will quickly crash.
The solution is as follows, and this is indeed a fairly accurate interpretation of how the AutoCAD Autoloader works for the OnAppearance context, taken from my original prototype.
1) Utilize the Microsoft Folder Notification API
Microsoft have there own Folder Notification API, so we may as well use that! AutoCAD implements an interface called IAdComFolderWatchReactor hosted inside of AdComFolderWatch.dll which wraps the Folder Notification API calls for you. This interface runs on a separate worker thread and receives the notifications away from the main thread, it’s very clean and nice to use - and ultimately handles all major multithreaded work for you, we like!
Here’s how the interface is implemented…
e.g.
//////////////////////////////////////////////////////////////////////////////
#import <AdComFolderWatch18.tlb> raw_interfaces_only, raw_native_types, no_namespace, named_guids
class CFolderWatcher : public IAdComFolderWatchReactor
{
  CComPtr<IAdComFolderWatchManager> mFolderWatchManager;
    // AutoCAD main window, so we don't have to risk calling it on another thread
  HWND mAutoCADHWnd;
  // folder watcher unique ids
  AcArray<long> mKeys;
    // singleton
  static CFolderWatcher *mInstance;
    CFolderWatcher(const CFolderWatcher& other);
  CFolderWatcher& operator=(const CFolderWatcher& other);
  public:
    // unique Windows message ID
  AcArray<UINT> mMessageIds;
  // array of folders
  AcArray<CString> mFolders;
    CFolderWatcher();
  virtual ~CFolderWatcher();
    // IUnknown
  virtual HRESULT STDMETHODCALLTYPE QueryInterface(
    /* [in] */ REFIID riid,/* [iid_is][out] */ __RPC__deref_out  void **ppvObject);
  virtual ULONG STDMETHODCALLTYPE AddRef( void);
  virtual ULONG STDMETHODCALLTYPE Release( void);
    // IAdComFolderWatchReactor
  virtual HRESULT __stdcall OnFolderChange (
    /*[in]*/ BSTR foldername,/*[in]*/ SAFEARRAY * * names,/*[in]*/ SAFEARRAY * * actions );
  virtual HRESULT __stdcall OnError (/*[in]*/ long num,/*[in]*/ BSTR description );
    // records a folder to watch
  long watchFolder(CString folder);
    // gets the singleton instance
  static CFolderWatcher* GetInstance();
};
2) How to switch from a worker thread to the main thread
The safest way to switch between a worker thread and the main thread in AutoCAD is to send a custom Windows message from the worker thread to the main thread, and then catch that message in the main thread for processing... That is demonstrated in step 5’s PostMessage() code.
You can create your own custom Windows message, using RegisterWindowMessage()…
e.g.
// generate a unique message handler id string
CString uniqueMessageString;
uniqueMessageString.Format(_T("WM_AutoloaderOnAppearanceMsg%d"), mKeys.length());
// now generate the id from the string
UINT messageId = ::RegisterWindowMessage(uniqueMessageString);
3) Register the folders you want to watch using IAdComFolderWatchReactor
The implementation of the watchFolder() function is as follows, simply call it passing the folder path you want to watch.
e.g.
long CFolderWatcher::watchFolder(CString folder)
{
  long key = 0;
  // now register the callbacks
  if (SUCCEEDED(mFolderWatchManager->AttachReactor(this,
CComBSTR((LPCTSTR)folder), VARIANT_TRUE, (FileNotifyFlags)511, &key)))
  {
    // remember the key
    mKeys.append(key);
    // and the path
    mFolders.append(folder);
      // generate a unique message handler id string
    CString uniqueMessageString;
    uniqueMessageString.Format(_T("WM_AutoloaderOnAppearanceMsg%d"), mKeys.length());
    // now generate the id from the string
    UINT messageId = ::RegisterWindowMessage(uniqueMessageString);
    // now add it to our recorded list
    mMessageIds.append(messageId);
  }
    return key;
}
4) Register our own Message Filter using acedRegisterWatchWinMsg() which watches for the unique Window Message from Step 2
Here’s the constructor of CFolderWatcher(), as you can see it registers a MessageProc() which will receive all AutoCAD Windows messages…
CFolderWatcher::CFolderWatcher()
{
  // if mInstance is NULL
  if (mInstance == NULL)
  {
    // create the folder watcher manager, if it fails no need to do the rest
    if(SUCCEEDED(mFolderWatchManager.CoCreateInstance(CLSID_AdComFolderWatchManager)))
    {
      // record the AutoCAD main window, so we don't have to risk calling it on anotheer thread
      mAutoCADHWnd = adsw_acadMainWnd();
        // register message hook to receive worker thread notification that a change has occurred
      acedRegisterWatchWinMsg(MessageProc);
        mInstance = this;
    }
  }
}
  5) What to do when you get a notification from the OnFolderChange()
When the OnFolderChange() is fired from the IAdComFolderWatchReactor, you are being called from the worker thread. The Autoloader mechanism does not work on the worker thread, only on the main thread – plus, we just don’t know if AutoCAD is ready to do what we want, we need to check isQuiescent() == true first…
From our own implementation of the OnFolderChange(), post our custom message to AutoCAD…
e.g.
//////////////////////////////////////////////////////////////////////////////
HRESULT CFolderWatcher::OnFolderChange (/*[in]*/ BSTR foldername,
                                        /*[in]*/ SAFEARRAY * * names,
                                        /*[in]*/ SAFEARRAY * * actions )
{
  // find the folder in our list of folders that are being watched
  for (int i=0; i<mFolders.length(); ++i)
  {
    // if this is the one we are looking for
    if (foldername == mFolders[i])
    {
      // post to the main thread we need a review of the loaded apps
      ::PostMessage(mAutoCADHWnd, mMessageIds[i], 0, 0);
    }
  }
  return S_OK;
}
now in our MessageProc we need to do something like this (sorry, I cannot post the whole function for legal reasons)
void MessageProc(const MSG *pMsg)
{
  // get the single folder watcher instance
  CFolderWatcher *watcher = CFolderWatcher::GetInstance();
  // if ok
  if (watcher != NULL)
  {
    // now loop through the message Id's and compare them
    for (int i=0; i<watcher->mMessageIds.length(); ++i)
    {
      // if this message is the same
      if (watcher->mMessageIds[i] == pMsg->message)
      {
        // AutoCAD is busy
        if (curDoc()->isQuiescent() == false)
        {
// setup sleep timer, on different thread, to wait 6 seconds
// once the timer has passed, repost the custom message
// and try this code again
          }
      }
    }
  }
}

