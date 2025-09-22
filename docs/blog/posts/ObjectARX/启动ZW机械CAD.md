---
title: 启动ZW机械CAD
date: 2024-11-20
categories:
  - windows程序
tags:
  - ZWCAD
  - CAD自动化
  - Csharp
  - COM接口
description: 通过C#代码启动和控制ZW机械CAD应用程序的接口调用方法
author: JerryMa
---

# 启动ZW机械CAD

```csharp
private ZWCAD.ZcadApplication m_cadApp;
private ZwmToolKitLib.ZwmApp m_objZwmApp;
private ZwmToolKitLib.ZwmDb m_objZwmDb;
private ZwmToolKitLib.Title m_objZwmTitle;
private ZwmToolKitLib.Bom m_objZwmBom;
private ZwmToolKitLib.Frame m_objZwmFrame;

try
{
    //取得一个正在运行的ZWCAD实例 
    m_cadApp = (ZWCAD.ZcadApplication)Marshal.GetActiveObject("ZWCAD.Application.2025");

}//end of try 
catch
{
    try
    {
        //建立一个新的AUTOCAD实例，并标识已经建立成功。 
        //        m_cadApp = new AutoCAD.AcadApplication();
        //m_cadApp = new ZWCAD.ZcadApplication();
        Type comType = Type.GetTypeFromProgID("ZWCAD.Application.2025");
        object comObj = Activator.CreateInstance(comType);
        m_cadApp = (ZWCAD.ZcadApplication)comObj;
        m_cadApp.Visible = true;
    }
    catch
    {
        throw new Exception("无法起动CAD应用程序，确认已经安装");
    }
}//end of catch 
 if (m_cadApp != null && m_objZwmApp == null)
 {
     m_objZwmApp = m_cadApp.GetInterfaceObject("ZwmToolKit.ZwmApp");
     m_objZwmApp.GetDb(out m_objZwmDb);
     if (m_objZwmApp != null)
     {
         String strCadPath = "";
         String strZwmPath = "";
         String strVersion = "";

         m_objZwmApp.GetCadPath(out strCadPath);
         m_objZwmApp.GetZwmPath(out strZwmPath);
         m_objZwmApp.GetVersion(out strVersion);

         textBox_cad_path.Text = strCadPath;
         textBox_zwm_path.Text = strZwmPath;
         textBox_version.Text = strVersion;
     }
     else
         MessageBox.Show("创建 ZwmToolKit.ZwmApp 失败！请检查机械软件启动是否正常");
 }

```

![image-20250604093310804](http://image.jerryma.xyz//images/20250604-image-20250604093310804.png)
