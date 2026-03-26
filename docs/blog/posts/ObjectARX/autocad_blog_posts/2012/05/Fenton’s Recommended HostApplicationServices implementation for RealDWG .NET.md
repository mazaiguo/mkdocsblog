---
title: "Fenton’s Recommended HostApplicationServices implementation for RealDWG .NET"
date: 2012-05-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - DWG
description: "Not sure how many of you know about Autodesk RealDWG so I thought I’d write a quick note on what it is and also include a starter HostApplicationSe..."
author: Autodesk
---
# Fenton’s Recommended HostApplicationServices implementation for RealDWG .NET

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/fentons-recommended-hostapplicationservices-implementation-for-realdwg-net.html

## 文章内容

by Fenton Webb
Not sure how many of you know about Autodesk RealDWG so I thought I’d write a quick note on what it is and also include a starter HostApplicationServices implementation for those who want to get started with it.
Autodesk RealDWG can be first be explained via the marketing portal www.autodesk.com/realdwg
Talking shop now, the toolkit basically contains the ObjectARX SDK but without any AutoCAD specific APIs. No plotting, no Ribbon, no SheetSet, etc etc, just the API functions for reading and writing DWG files.
Some answers to common questions:
Yes, it does read all DWG file versions – all the way back to V2 point something.
No you don’t need enablers installed to read the drawing. All DWG files can be read without object enablers being installed, that said, those objects that require object enablers won’t be readable.
Yes you can cut out components you don’t need, this is documented in the Redistribution Requirements section of the readdbx.chm file.
You must create an installer for any RealDWG application you create, that is also described Redistribution Requirements section of the readdbx.chm file.
Now the reason I’m posting a “Recommended HostApplicationServices” implementation is because I have found a lot of a problems people have had with RealDWG boiled down to their implementation of HostApplicationServices, mainly their HostApplicationServices::FindFile().
The HostApplicationServices class, as you can see below, defines what happens when certain types of “special things” happen in a DWG, like how to download an XRef from an FTP site for instance. These “special things” have no default implementation in RealDWG because RealDWG is a raw toolkit which is designed to be implemented as you see fit. It may come as a surprise to you guys, but actually RealDWG knows nothing about AutoCAD, it is AutoCAD that implements the RealDWG HostApplicationServices class in an AutoCAD way; so if you want RealDWG to resolve XRefs in the same way that AutoCAD does you have to specifically code your RealDWG app to do so…
I should mention that the C++ version of HostApplicationServices (AcDbHostApplicationServices) is even more detailed in its implementation which can be seen as a good thing (more control) or a bad thing (more complexity), your choice.
Anyway, here’s the code (originally used for a 2011 RealDWG App I wrote)…
class RealDwgHostServices : HostApplicationServices
{
  static bool _initialized = false;
  #region Imports
  [DllImport("acdb18.dll", CallingConvention = CallingConvention.Cdecl, EntryPoint = "acdbSetDefaultAcGiContext")]
  public static extern IntPtr acdbSetDefaultAcGiContext(IntPtr context);
  #endregion
    public RealDwgHostServices()
  {
    // if not already initialized (we can only call init once)
    if (!_initialized)
    {
      RuntimeSystem.Initialize(realDWGHost, 1033);
        // ensure the internal AcGiContext is setup, Text objects can be affected by this
      acdbSetDefaultAcGiContext(IntPtr.Zero);
        _initialized = true;
    }
  }
  public override string RegistryProductRootKey
  {
    // you need to specify your own...
    // search for ODBXHOSTAPPREGROOT in readdbx.chm for details
    get { return @"ObjectDBX\R18.1"; }
  }
  public override string CompanyName
  {
    get { return @"FentonCAD"; }
  }
  public override string Product
  {
    get { return @"DWGMoneyMaker"; }
  }
    public override string FindFile(string fileName,
                                    Database database,
                                      FindFileHint hint)
  {
    if (fileName.Contains(".") == false)
    {
      string extension = "";
      switch (hint)
      {
        case FindFileHint.Default:
          break;
        case FindFileHint.FontFile:
            break;
        case FindFileHint.CompiledShapeFile:
          extension = ".shx";
          break;
        case FindFileHint.TrueTypeFontFile:
          extension = ".ttf";
          break;
        case FindFileHint.EmbeddedImageFile:
          break;
        case FindFileHint.XRefDrawing:
          extension = ".dwg";
          break;
        case FindFileHint.PatternFile:
          break;
        case FindFileHint.ArxApplication:
          extension = ".dbx";
          break;
        case FindFileHint.FontMapFile:
          extension = ".fmp";
          break;
        case FindFileHint.UnderlayFile:
          break;
        default:
            break;
      }
      if (extension.Length == 0)
      {
        MessageBox.Show("Need to handle this.");
      }
        fileName += extension;
      }
      return SearchPath(new FileInfo(fileName));
  }
    private string SearchPath(FileInfo fileName)
  {
    if (fileName.Exists == true)
      return fileName.FullName;
      // get our RealDWG application folder to check there
    DirectoryInfo appFolder =
       new DirectoryInfo(Path.GetDirectoryName(
         System.Reflection.Assembly.GetExecutingAssembly().Location));
    fileName = new FileInfo(Path.Combine(appFolder.FullName,
                                    fileName.Name));
    if (fileName.Exists == true)
    {
      return fileName.FullName;
    }
      // check the Autodesk shared
    DirectoryInfo adeskSharedFolder =
       new DirectoryInfo(Path.Combine(
         Environment.GetEnvironmentVariable(
         "ProgramFiles"), @"Common Files\Autodesk Shared"));
    fileName = new FileInfo(Path.Combine(adeskSharedFolder.FullName,
                                    fileName.Name));
    if (fileName.Exists == true)
    {
      return fileName.FullName;
    }
      // check our fonts folder
    DirectoryInfo fontsFolder = new DirectoryInfo(
      Path.Combine(appFolder.FullName, "Fonts"));
    fileName = new FileInfo(Path.Combine(fontsFolder.FullName,
                                     fileName.Name));
    if (fileName.Exists == true)
    {
      return fileName.FullName;
    }
      // check the system fonts folder
    DirectoryInfo systemFontsFolder =
       new DirectoryInfo(Path.Combine(
         Environment.GetEnvironmentVariable("SystemRoot"), "Fonts"));
    fileName = new FileInfo(Path.Combine(systemFontsFolder.FullName,
                                      fileName.Name));
    if (fileName.Exists == true)
    {
      return fileName.FullName;
    }
      // search the ACAD Support path system var, in case it's setup
    string acadEnv = Environment.GetEnvironmentVariable("ACAD");
    // if valid
    if (String.IsNullOrEmpty(acadEnv) == false)
    {
      fileName = ScanEnvPath(acadEnv, fileName.Name);
      if (fileName != null && fileName.Exists == true)
      {
        return fileName.FullName;
      }
    }
      // try searching the DOS PATH
    string pathEnv = Environment.GetEnvironmentVariable("PATH");
    // if valid
    if (String.IsNullOrEmpty(pathEnv) == false)
    {
      fileName = ScanEnvPath(pathEnv, fileName.Name);
      if (fileName != null && fileName.Exists == true)
      {
        return fileName.FullName;
      }
    }
    return "";
  }
    private FileInfo ScanEnvPath(string envVariableValue, string fileName)
  {
    // extract each path and loop them
    string[] paths = envVariableValue.Split(';');
    foreach (string path in paths)
    {
      try
      {
        DirectoryInfo dirInfo = new DirectoryInfo(path);
        // if it exists
        if (dirInfo.Exists == true)
        {
          FileInfo newFileName = new FileInfo(dirInfo.FullName + fileName);
          if (newFileName.Exists == true)
            return newFileName;
        }
      }
      catch
      {
        }
    }
      return null;
  }
    #region GetRemoteFile for Urls inside a dwg file
  [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Auto)]
  private struct internet_cache_entry_info
  {
    public int dwstructsize;
    public IntPtr lpszsourceurlname;
    public IntPtr lpszlocalfilename;
    public int cacheentrytype;
    public int dwusecount;
    public int dwhitrate;
    public int dwsizelow;
    public int dwsizehigh;
    public System.Runtime.InteropServices.ComTypes.FILETIME lastmodifiedtime;
    public System.Runtime.InteropServices.ComTypes.FILETIME expiretime;
    public System.Runtime.InteropServices.ComTypes.FILETIME lastaccesstime;
    public System.Runtime.InteropServices.ComTypes.FILETIME lastsynctime;
    public IntPtr lpheaderinfo;
    public int dwheaderinfosize;
    public IntPtr lpszfileextension;
    public int dwexemptdelta;
  }
  private static List<internet_cache_entry_info> _remoteFiles =
                new List<internet_cache_entry_info>();
  [DllImport("wininet.dll", SetLastError = true, CharSet = CharSet.Auto)]
  private static extern IntPtr RetrieveUrlCacheEntryStream
      ([MarshalAs(UnmanagedType.LPTStr)]   string lpszUrlName,
      IntPtr lpcacheentryinfo,
      ref uint lpcbCacheEntryInfo,
      [MarshalAs(UnmanagedType.Bool)] bool fRandomRead,
      uint dwReserved);
  [DllImport("wininet.dll", CharSet = CharSet.Auto)]
  private static extern IntPtr ReadUrlCacheEntryStream(
    IntPtr hUrlCacheStream,
    UInt32 dwLocation,
    IntPtr lpBuffer,
    out UInt32 lpdwLen,
    UInt32 dwReserved);
  [DllImport("wininet.dll", CharSet = CharSet.Auto)]
  private static extern IntPtr FindFirstUrlCacheEntry(
    [MarshalAs(UnmanagedType.LPTStr)]string urlsearchpattern,
    IntPtr lpfirstcacheentryinfo,
    ref int lpdwfirstcacheentryinfobuffersize);
  [DllImport("wininet.dll", SetLastError = true, CharSet = CharSet.Auto)]
  private static extern bool GetUrlCacheEntryInfo(
    [MarshalAs(UnmanagedType.LPTStr)] string lpszurlname,
    IntPtr lpcacheentryinfo,
    ref int lpdwcacheentryinfobuffersize);
  public override string GetRemoteFile(Uri url, bool ignoreCache)
  {
    int nneeded = 0, nbufsize = 0;
    IntPtr buf = IntPtr.Zero;
    FindFirstUrlCacheEntry(null, IntPtr.Zero, ref   nneeded);
    nbufsize = nneeded; buf = Marshal.AllocHGlobal(nbufsize);
    internet_cache_entry_info cacheitem;
    GetUrlCacheEntryInfo(url.AbsoluteUri, buf, ref  nneeded);
    cacheitem = (internet_cache_entry_info)Marshal.PtrToStructure(
      buf, typeof(internet_cache_entry_info));
    string res = Marshal.PtrToStringUni(cacheitem.lpszlocalfilename);
      bool found = false;
    // now add it to the list of remote files, but make sure there are no duplicates
    for (int i = 0; i < _remoteFiles.Count; ++i)
    {
      if (string.Compare(Marshal.PtrToStringUni(
        _remoteFiles[i].lpszsourceurlname), url.AbsoluteUri, true) == 0)
      {
        _remoteFiles[i] = cacheitem;
        found = true;
        break;
      }
    }
    // if we didn't find a duplicate, then add it
    if (!found)
      _remoteFiles.Add(cacheitem);
    // Marshal.PtrToStringAnsi  
    return (res);
  }
  #endregion
    public override bool IsUrl(string filePath)
  {
    return Uri.IsWellFormedUriString(filePath, UriKind.RelativeOrAbsolute);
  }
    public override Uri GetUrl(string localFile)
  {
    foreach (internet_cache_entry_info info in _remoteFiles)
    {
      if (string.Compare(Marshal.PtrToStringUni(info.lpszlocalfilename), localFile, true) == 0)
        return new Uri(Marshal.PtrToStringUni(info.lpszsourceurlname));
    }
      return new Uri("");
  }
    public override string GetPassword(string dwgName, PasswordOptions options)
  {
    PasswordForm form = new PasswordForm();
    form.drawingPath.Text = dwgName;
    form.ShowDialog();
    return form.textBox1.Text;
  }
}

