---
title: "Progress and cancellation of long ObjectARX tasks"
date: 2012-05-01
categories:
  - AutoCAD C++
tags:
  - C++
  - ObjectARX
description: "To provide the user with graphical feedback during long tasks, and also ensure that any user cancellation (due to the Escape key being pressed) is ..."
author: Autodesk
---
# Progress and cancellation of long ObjectARX tasks

发布日期: 2012-05-01

原始链接: https://adndevblog.typepad.com/autocad/2012/05/progress-and-cancellation-of-long-objectarx-tasks.html

## 文章内容

By Balaji Ramamoorthy
To provide the user with graphical feedback during long tasks, and also ensure that any user cancellation (due to the Escape key being pressed) is handled, you can use the following functions:
int acedSetStatusBarProgressMeter(const ACHAR* pszLabel, int nMinPos, int nMaxPos);
int acedSetStatusBarProgressMeterPos(int nPos);
void acedRestoreStatusBar();
To check for cancellation by the user you can use this function:
int acedUsrBrk();
It returns 1 if the user has cancelled the operation, or 0 otherwise. I would check it regularly (though not excessively so), and on finding the return value is true your application should perform the necessary cleanup and return control to the user.
In the code sample, a long task is simulated using nested for loops and the Win32 Sleep() function. The methods used here are part of rxmfcapi.h and you will have this included in your project automatically if you choose MFC support while creating your project using the ObjectARX Wizard.
Here is the sample code :
static void ADSProjectMyCommand(void)
{
   Adesk::Boolean bContinue = Adesk::kTrue;
     acutPrintf
             (
               ACRX_T("\nStarting Progress Meter...\r")
             );
     acedSetStatusBarProgressMeter
             (
               ACRX_T("Test Progress Bar"), 0, 100
             );
   for( int i =0; i <= 100; i++ )
   {
      for( int j = 0; j <= 10; j++ )
      {
         Sleep( 100 );
           if ( acedUsrBrk() )
         {
            // Perform cleanup on cancel
            bContinue = Adesk::kFalse;
            acutPrintf(
                        ACRX_T("\nCancelled !")
                      );
            break;
         }
      }
        if ( !bContinue )
         break;
        acedSetStatusBarProgressMeterPos( i );
   }
   acedRestoreStatusBar();
}
For a .Net implementation of similar functionality, please take a look at this blog post : Displaying a progress meter during long operations in AutoCAD using .NET

## 评论

**内容**: petcon said...
//通过长度来对acdbcurve采样
bool samplingByLenth( AcDbObjectId curId, double sampleLen, vector &pArr )
{
acutPrintf
(
ACRX_T("\n开始采样...\r")
);

bool flag = true;
AcDbEntity *pEnt;
if (Acad::eOk == acdbOpenAcDbEntity(pEnt,curId,AcDb::kForWrite))
{
if (pEnt->isKindOf(AcDbCurve::desc()))
{
AcDbCurve *pCur = AcDbCurve::cast(pEnt);
//double startPam;
double endPam;
double totalLen;
AcGePoint3d pTmp;
//pCur->getStartParam(startPam);
pCur->getEndParam(endPam);
pCur->getDistAtParam(endPam,totalLen);
acedSetStatusBarProgressMeter
(
ACRX_T("采样..."), 0, totalLen
);
for (double lentmp = 0.0;lentmp<=totalLen;lentmp = lentmp + sampleLen)
{
if (acedUsrBrk())
{
flag = false;
break;
}
acedSetStatusBarProgressMeterPos( lentmp );
pCur->getPointAtDist(lentmp,pTmp);
pArr.push_back(pTmp);
}
acedRestoreStatusBar();
pCur->getPointAtParam(endPam,pTmp);
pArr.push_back(pTmp);
pCur->close();
}
pEnt->close();
}
return flag;
}
in this code i still can not stop by esc key
Reply
09/14/2012 at 09:46 PM

---
**内容**: Account Deleted said in reply to petcon...
Try this function:
void OnIdleAcadInternal(void) {
CWinApp *app = acedGetAcadWinApp();
CWnd *wnd = app->GetMainWnd ();
MSG msg;
while (::PeekMessage(&msg, wnd->m_hWnd, 0, 0, PM_NOREMOVE)) {
if (!app->PumpMessage()) {
::PostQuitMessage(0);
break;
}
}
}
And call OnIdleAcadInternal() before calling acedUsrBrk()
Reply
09/15/2012 at 07:05 AM

---
