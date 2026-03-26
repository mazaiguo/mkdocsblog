---
title: "Registering a custom entity for load on proxy detection"
date: 2012-05-01
categories:
  - AutoCAD
tags:
  - AutoCAD
description: "I have my custom entity which I registered for load on proxy detection, but AutoCAD does not load it automatically when a drawing containing my ent..."
author: Autodesk
---
# Registering a custom entity for load on proxy detection

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/registering-a-custom-entity-for-load-on-proxy-detection.html

## 文章内容

By Adam Nagy
I have my custom entity which I registered for load on proxy detection, but AutoCAD does not load it automatically when a drawing containing my entity is opened. What could be the problem?
Here is my code:
void RegisterDbxApp()
{
  AcadAppInfo appInfo;
  appInfo.setAppName(L"MYAPP");
    HMODULE hModule=GetModuleHandle(L"MyApp.dll");
  TCHAR modulePath[512];
  DWORD pathLength = GetModuleFileName(hModule, modulePath, 512);
  if (pathLength)
    appInfo.setModuleName(modulePath);
    appInfo.setAppDesc(L"My DBX module");
  appInfo.setLoadReason(
    AcadApp::LoadReasons(
    AcadApp::kOnProxyDetection |
    AcadApp::kOnLoadRequest));
    appInfo.writeToRegistry(true,true);
}
Solution
When AutoCAD tries to find your object enabler application then it is using the application name you defined in the ACRX_DXF_DEFINE_MEMBERS macro, which in your case is:
ACRX_DXF_DEFINE_MEMBERS (
  MyEnt, AcDbEntity,
  AcDb::kDHL_CURRENT, AcDb::kMReleaseCurrent,
  AcDbProxyEntity::kNoOperation, MyEnt,
  "MYAPP"
  "|Product Desc:     My App"
  "|Company:          My Company"
  "|WEB Address:      www.mycompany.com"
)
Since the macro already converts the parameters to string, therefore the application name will get extra " characters: "MYAPP" instead of MYAPP, so AutoCAD won’t find it in the registry:

You just have to remove the extra " characters. This way AutoCAD can find your application in the registry and can load it the next time a drawing containing your entity is opened:
ACRX_DXF_DEFINE_MEMBERS (
  MyEnt, AcDbEntity,
  AcDb::kDHL_CURRENT, AcDb::kMReleaseCurrent,
  AcDbProxyEntity::kNoOperation, MyEnt,
  MYAPP
  |Product Desc:     My App
  |Company:          My Company
  |WEB Address:      www.mycompany.com
)

## 评论

**内容**: Owen Wengerd said...
It is my experience that leaving the first and last quote mark is necessary to preserve white space within the string and keep things lined up:
ACRX_DXF_DEFINE_MEMBERS (
MyEnt, AcDbEntity,
AcDb::kDHL_CURRENT, AcDb::kMReleaseCurrent,
AcDbProxyEntity::kNoOperation, MyEnt,
"MYAPP|Product Desc: My App|Company: My Company|WEB Address: www.mycompany.com"
)
Reply
05/28/2012 at 08:33 AM

---
**内容**: Adam Nagy said...
Thanks for the comment, Owen.
The problem is that the quotation mark added at the beginning will appear in the application name: "MYAPP instead of MYAPP, so probably AutoCAD will not find that application either.
I just checked in the watch window what string the sample code I pasted creates. Here it is:
MYAPP |Product Desc: My App |Company: My Company |WEB Address: www.mycompany.com
So it seems that the space characters are preserved.
If you modified the DXF_MACRO to use ACRX_T(APP) instead of the original ACRX_T(#APP), then your extra quotation marks would be necessary and would not show up in the string.
Reply
05/29/2012 at 06:49 AM

---
**内容**: Owen Wengerd said in reply to Adam Nagy...
Adam, what you say is correct, but you should test my assertion not by looking at the watch window, but by looking at what is displayed in the proxy notice dialog box. You should also perform a test with an actual registered application name rather than making assumptions about how AutoCAD parses the string.
If you think I am wrong, please edify me via email, as this blog is inhospitable to conversation.
Reply
05/29/2012 at 09:40 AM

---
**内容**: Adam Nagy said...
Just a final word after discussing this topic directly with Owen. He seems to be right in saying that if you want the information shown by the LIST command to be nicely formatted, then you should place the application information inside quotation marks - as he showed in his comment. Your application will still be recognised and the additional space characters will be kept in the string.
Thanks, Owen!
Reply
06/19/2012 at 07:46 AM

---
