---
title: "Supporting AcDbOle2Frame objects in RealDWG"
date: 2013-03-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - C++
  - DWG
description: "Supporting AcDbOle2Frame objects inside of RealDWG unfortunately requires some extra work to make happen, I’ve pasted some sample code below which ..."
author: Autodesk
---
# Supporting AcDbOle2Frame objects in RealDWG

发布日期: 2013-03-01

原始链接: https://adndevblog.typepad.com/autocad/2013/03/supporting-acdbole2frame-objects-in-realdwg.html

## 文章内容

by Fenton Webb
Supporting AcDbOle2Frame objects inside of RealDWG unfortunately requires some extra work to make happen, I’ve pasted some sample code below which shows how to implement the code into your RealDWG C++ application.
The bad news is that if you are a .NET user of RealDWG then you will need to touch into unmanaged C++ via a Mixed Mode Dll in order to add support for your Ole2Frame class. That’s because, at the time of writing, the .NET version of the HostApplicationServices class does not export the functions you need.
Here’s how to create a Mixed Mode RealDWG app.
////////////////////////////////////////////
// RealDwg_App1Dlg.cpp : implementation file
#include "stdafx.h"
#include "RealDwg_App1.h"
#include "RealDwg_App1Dlg.h"
#include "AcIOxClientItemMgr.h"
  #ifdef _DEBUG
#define new DEBUG_NEW
#endif
  // CAboutDlg dialog used for App About
class CAboutDlg : public CDialog
{
public:
  CAboutDlg();
    // Dialog Data
  enum { IDD = IDD_ABOUTBOX };
  protected:
  virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support
    // Implementation
protected:
  DECLARE_MESSAGE_MAP()
};
  CAboutDlg::CAboutDlg() : CDialog(CAboutDlg::IDD)
{
}
  void CAboutDlg::DoDataExchange(CDataExchange* pDX)
{
  CDialog::DoDataExchange(pDX);
}
  BEGIN_MESSAGE_MAP(CAboutDlg, CDialog)
END_MESSAGE_MAP()
  class CreatentHostApp : public AcDbHostApplicationServices
{
  Acad::ErrorStatus findFile(TCHAR* pcFullPathOut, int nBufferLength,
    const TCHAR* pcFilename, AcDbDatabase* pDb = NULL,
    AcDbHostApplicationServices::FindFileHint = kDefault);
    // These two functions return the full path to the root folder where roamable/local
  // customizable files were installed. Note that the user may have reconfigured
  // the location of some the customizable files using the Options Dialog
  // therefore these functions should not be used to locate customizable files.
  // To locate customizable files either use the findFile function or the
  // appropriate system variable for the given file type.
  //
  Acad::ErrorStatus getRoamableRootFolder(const TCHAR*& folder);
  Acad::ErrorStatus getLocalRootFolder(const TCHAR*& folder);
  Acad::ErrorStatus getNewOleClientItem(COleClientItem*& pItem);
  Acad::ErrorStatus serializeOleItem(COleClientItem* pItem, CArchive* pArchive);
    // Support redo
  virtual bool  supportsMultiRedo() const { return true; }
  // make sure you implement getAlternateFontName. In case your findFile implementation
  // fails to find a font you should return a font name here that is guaranteed to exist.
  virtual TCHAR * getAlternateFontName() const
  {
    return _T("txt.shx"); //findFile will be called again with this name
  }
};
  // Return the Install directory for customizable files
Acad::ErrorStatus
  CreatentHostApp::getRoamableRootFolder(const TCHAR*& folder)
{
  Acad::ErrorStatus ret = Acad::eOk;
  static TCHAR buf[MAX_PATH] = _T("\0"); //MDI SAFE
  if (buf[0]==0)
    if (GetModuleFileName(NULL, buf, MAX_PATH) != 0)
      ret = Acad::eRegistryAccessError;
  folder = buf;
  return ret;
}
  // Return the Install directory for customizable files
Acad::ErrorStatus
  CreatentHostApp::getLocalRootFolder(const TCHAR*& folder)
{
  Acad::ErrorStatus ret = Acad::eOk;
  static TCHAR buf[MAX_PATH] = _T("\0"); //MDI SAFE
  if (buf[0]==0)
    if (GetModuleFileName(NULL, buf, MAX_PATH) != 0)
      ret = Acad::eRegistryAccessError;
  folder = buf;
  return ret;
}
  Acad::ErrorStatus
  CreatentHostApp::findFile(TCHAR* pcFullPathOut, int nBufferLength,
  const TCHAR* pcFilename, AcDbDatabase* pDb,
  AcDbHostApplicationServices::FindFileHint hint)
{
  TCHAR pExtension[5];
  switch (hint)
  {
  case kCompiledShapeFile:
    _tcscpy_s(pExtension, _T(".shx"));
    break;
  case kTrueTypeFontFile:
    _tcscpy_s(pExtension, _T(".ttf"));
    break;
  case kPatternFile:
    _tcscpy_s(pExtension, _T(".pat"));
    break;
  case kARXApplication:
    _tcscpy_s(pExtension, _T(".dbx"));
    break;
  case kFontMapFile:
    _tcscpy_s(pExtension, _T(".fmp"));
    break;
  case kXRefDrawing:
    _tcscpy_s(pExtension, _T(".dwg"));
    break;
  case kFontFile:                // Fall through.  These could have
  case kEmbeddedImageFile:       // various extensions
  default:
    pExtension[0] = _T('\0');
    break;
  }
  TCHAR* filePart;
  DWORD result;
  result = SearchPath(NULL, pcFilename, pExtension, nBufferLength,
    pcFullPathOut, &filePart);
  if (result && result < (DWORD)nBufferLength)
    return Acad::eOk;
  else
    return Acad::eFileNotFound;
}
  Acad::ErrorStatus
  CreatentHostApp::getNewOleClientItem(COleClientItem*& pItem)
{
  AcDbDatabase* pClientItemOwner = 0;
    pClientItemOwner = acdbHostApplicationServices()->workingDatabase();
  if (pClientItemOwner) {
    pItem = AcIOxClientItemMgr::GetNewOleClientItem(pClientItemOwner);
    ASSERT(pItem != 0);
  }
    return Acad::eOk;
}
  Acad::ErrorStatus
  CreatentHostApp::serializeOleItem(COleClientItem* pItem, CArchive* pArchive)
{
  TRY{
      if ((*pArchive).IsStoring()){
      ASSERT(pItem->m_lpObject != 0);
    }
      pItem->Serialize(*pArchive);
      if ((*pArchive).IsStoring())
      (*pArchive) << 0L << 0L << 0L << 0L << 0L << 0L;
  }
  CATCH_ALL(e){
    //This may be an acceptable situation with some corrupt data sets. A warning
    //assert is good enough.
    ASSERT(!_T("Failed to serialize a COleClientItem object!"));
      return Acad::eNotImplemented;
  }
  END_CATCH_ALL
      return Acad::eOk;
}
  CreatentHostApp gCreatentHostApp;
  // CRealDwg_App1Dlg dialog
CRealDwg_App1Dlg::CRealDwg_App1Dlg(CWnd* pParent /*=NULL*/)
  : CDialog(CRealDwg_App1Dlg::IDD, pParent)
{
  m_hIcon = AfxGetApp()->LoadIcon(IDR_MAINFRAME);
}
  void CRealDwg_App1Dlg::DoDataExchange(CDataExchange* pDX)
{
  CDialog::DoDataExchange(pDX);
    DDX_Control(pDX, IDC_OUTPUT_LIST, m_outputList);
}
  INT_PTR CRealDwg_App1Dlg::DoModal()
{
  acdbSetHostApplicationServices(&gCreatentHostApp);
  long lcid = 0x00000409; // English
  acdbValidateSetup(lcid);
    INT_PTR int_ptr = CDialog::DoModal();
    acdbCleanUp();
    return int_ptr;
}
  BEGIN_MESSAGE_MAP(CRealDwg_App1Dlg, CDialog)
  ON_WM_SYSCOMMAND()
  ON_WM_PAINT()
  ON_WM_QUERYDRAGICON()
    ON_BN_CLICKED(IDC_SELECT_BTN, OnSelectFile)
    //}}AFX_MSG_MAP
END_MESSAGE_MAP()
    // CRealDwg_App1Dlg message handlers
BOOL CRealDwg_App1Dlg::OnInitDialog()
{
  CDialog::OnInitDialog();
    // Add "About..." menu item to system menu.
    // IDM_ABOUTBOX must be in the system command range.
  ASSERT((IDM_ABOUTBOX & 0xFFF0) == IDM_ABOUTBOX);
  ASSERT(IDM_ABOUTBOX < 0xF000);
    CMenu* pSysMenu = GetSystemMenu(FALSE);
  if (pSysMenu != NULL)
  {
    BOOL bNameValid;
    CString strAboutMenu;
    bNameValid = strAboutMenu.LoadString(IDS_ABOUTBOX);
    ASSERT(bNameValid);
    if (!strAboutMenu.IsEmpty())
    {
      pSysMenu->AppendMenu(MF_SEPARATOR);
      pSysMenu->AppendMenu(MF_STRING, IDM_ABOUTBOX, strAboutMenu);
    }
  }
    // Set the icon for this dialog.  The framework does this automatically
  //  when the application's main window is not a dialog
  SetIcon(m_hIcon, TRUE);   // Set big icon
  SetIcon(m_hIcon, FALSE);  // Set small icon
    // TODO: Add extra initialization here
    CRect rect;
  m_outputList.GetWindowRect(&rect);
  const int nScrollWidth = ::GetSystemMetrics(SM_CXVSCROLL);
  const int nColumnWidth = rect.Width() - 2 * nScrollWidth;
  m_outputList.InsertColumn(0, _T("Dimension Type"), LVCFMT_LEFT, nColumnWidth*2/5, 0);
  m_outputList.InsertColumn(1, _T("Dimension Text Point"), LVCFMT_LEFT, nColumnWidth*3/5, 0);
    return TRUE;  // return TRUE  unless you set the focus to a control
}
  void CRealDwg_App1Dlg::OnSysCommand(UINT nID, LPARAM lParam)
{
  if ((nID & 0xFFF0) == IDM_ABOUTBOX)
  {
    CAboutDlg dlgAbout;
    dlgAbout.DoModal();
  }
  else
  {
    CDialog::OnSysCommand(nID, lParam);
  }
}
  // If you add a minimize button to your dialog, you will need the code below
//  to draw the icon.  For MFC applications using the document/view model,
//  this is automatically done for you by the framework.
  void CRealDwg_App1Dlg::OnPaint()
{
  if (IsIconic())
  {
    CPaintDC dc(this); // device context for painting
      SendMessage(WM_ICONERASEBKGND, reinterpret_cast<WPARAM>(dc.GetSafeHdc()), 0);
      // Center icon in client rectangle
    int cxIcon = GetSystemMetrics(SM_CXICON);
    int cyIcon = GetSystemMetrics(SM_CYICON);
    CRect rect;
    GetClientRect(&rect);
    int x = (rect.Width() - cxIcon + 1) / 2;
    int y = (rect.Height() - cyIcon + 1) / 2;
      // Draw the icon
    dc.DrawIcon(x, y, m_hIcon);
  }
  else
  {
    CDialog::OnPaint();
  }
}
  // The system calls this function to obtain the cursor to display while the user drags
//  the minimized window.
HCURSOR CRealDwg_App1Dlg::OnQueryDragIcon()
{
  return static_cast<HCURSOR>(m_hIcon);
}
  void CRealDwg_App1Dlg::OnSelectFile()
{
#if 0
  CFileDialog selectDwgDlg(
    TRUE,
    _T("DXF Files (*dxf)"),
    NULL,
    OFN_HIDEREADONLY | OFN_OVERWRITEPROMPT |OFN_ENABLESIZING,
    _T("DXF File (*.dxf)|*.dxf;)||")
    );
#endif
  #if 1
  CFileDialog selectDwgDlg(
    TRUE,
    _T("DWG Files (*dwg)"),
    NULL,
    OFN_HIDEREADONLY | OFN_OVERWRITEPROMPT |OFN_ENABLESIZING,
    _T("DWG File (*.dwg)|*.dwg;)||")
    );
#endif
    if (selectDwgDlg.DoModal() == IDOK) {
      CString dwgPathName = selectDwgDlg.GetPathName();
      // Create an AcDbDatabase and initialize its tables.
    AcDbDatabase *pDb = new AcDbDatabase(false);
    if (pDb == NULL)
      return;
      Acad::ErrorStatus es = pDb->readDwgFile(dwgPathName, _SH_DENYWR);
    if (es == Acad::eOk) {
        acdbHostApplicationServices()->setWorkingDatabase(pDb);
        pDb->saveAs(_T("c:\\test.dwg"));
    }
      delete pDb; pDb = NULL;
  }
}
  ////////////////////////////////////////////
#include "StdAfx.h"
#include "AcIOxClientItemMgr.h"
//
#include <map>
#include <set>
//
#include <dbmain.h>
  //////////////////////////////////////////////////////////////////////////
//AcIOxOleClientItem implementation
//////////////////////////////////////////////////////////////////////////
  /////////////////////////////////////////////////////////////////
//AcIOxOleClientItem
//////////////////////////////////////////////////////////////////////////
class AcIOxOleClientItem : public COleClientItem {
    DECLARE_DYNAMIC(AcIOxOleClientItem)
  AcIOxOleClientItem(const AcIOxOleClientItem&);
  AcIOxOleClientItem& operator=(const AcIOxOleClientItem&);
  public:
  AcIOxOleClientItem(COleDocument* pContainerDoc, AcDbDatabase* pClientItemOwner, bool bMakeTransient = false);
  virtual ~AcIOxOleClientItem();
  public:
  bool IsTransient() const {return m_bTransient;}
  private:
  bool m_bTransient; //Flag to indicate whether the object is marked as transient or not
  //A transient AcIOxOleClientItem object is deleted after the owning
  //AcDbDatabase is saved
};
  IMPLEMENT_DYNAMIC(AcIOxOleClientItem, COleClientItem)
    AcIOxOleClientItem::AcIOxOleClientItem(COleDocument* pContainerDoc,
  AcDbDatabase* pClientItemOwner,
  bool bMakeTransient /* = false */):
COleClientItem(pContainerDoc),
  m_bTransient(bMakeTransient)
{
  //COleDocument's ctor allows a null container, which isn't supported
  //when instatiating this class
  ASSERT(pContainerDoc != 0);
  //
  //Register the client item with the owner
  ASSERT(pClientItemOwner != 0);
  AcIOxClientItemMgr::RegisterClientItem(this, pClientItemOwner);
}
  AcIOxOleClientItem::~AcIOxOleClientItem()
{
}
//////////////////////////////////////////////////////////////////////////
  namespace
{
  typedef std::set<AcIOxOleClientItem *> SetClientItems_t;
  typedef std::map<AcDbDatabase *, SetClientItems_t> MapOwnerToClientItems_t;
  MapOwnerToClientItems_t g_OwnerToClientItemsMap;
  COleDocument* g_OleDocument = NULL;
    void _RegisterClientItem(AcIOxOleClientItem* pItem, AcDbDatabase* pClientItemOwner)
  {
    g_OwnerToClientItemsMap[pClientItemOwner].insert(pItem);
  }
    void _UnregisterClientItems(AcDbDatabase* pClientItemOwner, bool bTransientItemsOnly)
  {
    if (!pClientItemOwner){
      return;
    }
      MapOwnerToClientItems_t::const_iterator iter = g_OwnerToClientItemsMap.find(pClientItemOwner);
    if (iter == g_OwnerToClientItemsMap.end()){
      return;
    }
      SetClientItems_t items = iter->second;
    SetClientItems_t::iterator it = items.begin();
    while(it != items.end()){
        AcIOxOleClientItem * pItem = (*it);
      ASSERT(pItem);
      if (!pItem){
        ASSERT(false);//Null entry!
        it++;
        continue;
      }
        if (bTransientItemsOnly && !pItem->IsTransient()){
        it++;
        continue;
      }
        it = items.erase(it);
        COleDocument* pContainerDoc = pItem->GetDocument();
      ASSERT(pContainerDoc != 0);
        //Release the item
      pItem->Release();
        //Remove the item from the container
      if (pContainerDoc){
        pContainerDoc->RemoveItem(pItem);
      }
        //Internal release the item
      ULONG ulRef = pItem->InternalRelease();
        //Delete the item
      if (ulRef > 0){
        delete pItem;
      }
      pItem = 0;
    }
      //Erase the owner entry from the map, if there are no more registered items
    //associated to this owner
    if (items.empty()){
      g_OwnerToClientItemsMap.erase(pClientItemOwner);
    }else{
      g_OwnerToClientItemsMap[pClientItemOwner] = items;
    }
      //The hosting COleDocument needs to be deleted when
    //no longer in use. This object holds onto a lock count
    //on the Afx module state, and failure to delete this
    //can prevent the host process from going away at the
    //time of shut down
    if (g_OleDocument && g_OwnerToClientItemsMap.empty()){
      delete g_OleDocument;
      g_OleDocument = 0;
    }
  }
    void _UnregisterClientItemOwner(AcDbDatabase* pClientItemOwner)
  {
    if (!pClientItemOwner){
      return;
    }
      MapOwnerToClientItems_t::const_iterator iter = g_OwnerToClientItemsMap.find(pClientItemOwner);
    if (iter == g_OwnerToClientItemsMap.end()){
      return;
    }
      //Unregister all client item objects registered for this owner
    const bool bTransientItemsOnly = false;
    _UnregisterClientItems(pClientItemOwner, bTransientItemsOnly);
      //Erase the owner entry from the map
    g_OwnerToClientItemsMap.erase(pClientItemOwner);
      //The hosting COleDocument needs to be deleted when
    //no longer in use. This object holds onto a lock count
    //on the Afx module state, and failure to delete this
    //can prevent the host process from going away at the
    //time of shut down
    if (g_OleDocument && g_OwnerToClientItemsMap.empty()){
      delete g_OleDocument;
      g_OleDocument = 0;
    }
  }
    bool _HasRegisteredItems()
  {
    return (g_OwnerToClientItemsMap.size() > 0);
  }
}
  //////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////
  COleDocument*
  AcIOxClientItemMgr::GetHostingDocument(bool bCreateIfNotInitialized /* = true */)
{
  if (!g_OleDocument){
    if (bCreateIfNotInitialized){
      g_OleDocument = new COleDocument();
    }
  }
  return g_OleDocument;
}
  COleClientItem*
  AcIOxClientItemMgr::GetNewOleClientItem(AcDbDatabase* pClientItemOwner, bool bMakeTransient /* = false */)
{
  AcIOxOleClientItem* pItem = new AcIOxOleClientItem(AcIOxClientItemMgr::GetHostingDocument(), pClientItemOwner, bMakeTransient);
  return pItem;
}
  void
  AcIOxClientItemMgr::RegisterClientItem(AcIOxOleClientItem* pItem, AcDbDatabase* pClientItemOwner)
{
  _RegisterClientItem(pItem, pClientItemOwner);
}
  void
  AcIOxClientItemMgr::UnregisterClientItems(AcDbDatabase* pClientItemOwner, bool bTransientItemsOnly /* = false */)
{
  _UnregisterClientItems(pClientItemOwner, bTransientItemsOnly);
}
  void
  AcIOxClientItemMgr::UnregisterClientItemOwner(AcDbDatabase* pClientItemOwner)
{
  _UnregisterClientItemOwner(pClientItemOwner);
}
  bool
  AcIOxClientItemMgr::HasRegisteredItems()
{
  return _HasRegisteredItems();
}

## 评论

**内容**: Daniel Rojas said...
And how can this be used to for example insert a bitmap or jpg inside of the active database?
Reply
07/31/2020 at 01:06 PM

---
