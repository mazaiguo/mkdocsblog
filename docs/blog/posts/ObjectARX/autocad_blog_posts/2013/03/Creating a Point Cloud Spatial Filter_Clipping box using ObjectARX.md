---
title: "Creating a Point Cloud Spatial Filter/Clipping box using ObjectARX"
date: 2013-03-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - API
  - C++
  - ObjectARX
  - Solid
description: "In order to create a Point Cloud clipping region you must use the C++ ObjectARX API as there is no equivalent .NET API. This is mainly due to perfo..."
author: Autodesk
---
# Creating a Point Cloud Spatial Filter/Clipping box using ObjectARX

发布日期: 2013-03-01

原始链接: https://adndevblog.typepad.com/autocad/2013/03/creating-a-point-cloud-spatial-filterclipping-box-using-objectarx.html

## 文章内容

by Fenton Webb
In order to create a Point Cloud clipping region you must use the C++ ObjectARX API as there is no equivalent .NET API. This is mainly due to performance reasons.
All you do is specify a filter callback for a given Point Cloud entity using the acdbModifyPointCloudDataView() function.
Here is an example of how to create a Point Cloud spatial filter using ObjectARX… You’ll see that for fun (and simple usage) I wire in the use of an AcDb3dSolid Box as my filter control object too…
acrxEntryPoint.cpp
//-----------------------------------------------------------------------------
//----- acrxEntryPoint.cpp
//-----------------------------------------------------------------------------
#include "StdAfx.h"
#include "resource.h"
#include "myFilter.h"
#include "MyBoxReactor.h"
  #pragma comment(lib,"AcDbPointCloudObj.lib")
#include "AcPointCloud.h"
  //-----------------------------------------------------------------------------
#define szRDS _RXST("asdk")
  //-----------------------------------------------------------------------------
//----- ObjectARX EntryPoint
class CAcPointCloudTestApp : public AcRxArxApp
{
public:
 CAcPointCloudTestApp () : AcRxArxApp () {}
   virtual AcRx::AppRetCode On_kInitAppMsg (void *pkt) {
  // TODO: Load dependencies here
    // You *must* call On_kInitAppMsg here
  AcRx::AppRetCode retCode =AcRxArxApp::On_kInitAppMsg (pkt) ;
    // TODO: Add your initialization code here
    return (retCode) ;
}
   virtual AcRx::AppRetCode On_kUnloadAppMsg (void *pkt) {
  // TODO: Add your code here
    // You *must* call On_kUnloadAppMsg here
  AcRx::AppRetCode retCode =AcRxArxApp::On_kUnloadAppMsg (pkt) ;
    // TODO: Unload dependencies here
    return (retCode) ;
}
   virtual void RegisterServerComponents () {
}
      ///////////////////////////////////////////////////////////////
 // by Fenton Webb, DevTech, 19/03/2013
 static void asdkAcPointCloudTestaddFilter(void)
{
  // pick a point cloud
  ads_name ename;
  ads_point pnt;
  int res = acedEntSel(_T("\nSelect a Point Cloud : "), ename, pnt);
    // if ok
    if (res == RTNORM)
    {
      // then convert the ename to an object id
   AcDbObjectId id;
   acdbGetObjectId(id,ename);
      // open the selected point cloud entity
    AcDbEntityPointer ent(id, AcDb::kForWrite);
      // if ok
      if (ent.openStatus() == Acad::eOk)
    {
      // reset the point cloud view
        Acad::ErrorStatus es = acdbResetPointCloudDataView(ent);
        // if not ok, possibly not a point cloud
        if (es != Acad::eOk)
        {
          acutPrintf(_T("\nNot a point cloud..."));
          return;
        }
          AcGePoint3d minPnt;
        acedInitGet(RSG_GETZ, NULL);
      // select the first bounding point
      res = acedGetPoint(NULL, _T("\nSelect Bottom Left Corner : "), asDblArray(minPnt));
        // if ok
        if (res == RTNORM)
        {
          AcGePoint3d maxPnt;
          acedInitGet(RSG_GETZ, NULL);
          // select the second bounding point
        res = acedGetPoint(NULL, _T("\nSelect Top Right Corner : "), asDblArray(maxPnt));
          // if ok
          if (res == RTNORM)
          {
            // convert any UCS to world
            AcGeMatrix3d matUcs2Wcs;
            acedGetCurrentUCS(matUcs2Wcs);
            matUcs2Wcs.invert();
            minPnt.transformBy(matUcs2Wcs);
            maxPnt.transformBy(matUcs2Wcs);
              // set up and nice extents box
            AcGeBoundBlock3d filterExtents;
            filterExtents.set(minPnt, maxPnt);
            // draw controller box
            DrawSlicerBox(filterExtents);
              // create a new filter object, my one I mean - document specific
            DocVars.docData().mPCFilter = new MyFilter(filterExtents, id);
          // and apply the filter to the point cloud
          res = acdbModifyPointCloudDataView(ent.object(), DocVars.docData().mPCFilter);
          }
        }
      }
    }
}
    static bool DrawSlicerBox(AcGeBoundBlock3d extents)
  {
    // extract the points
    AcGePoint3d minPnt, maxPnt;
    extents.getMinMaxPoints(minPnt, maxPnt);
      // draw a box
    {
      AcDbObjectPointer<AcDb3dSolid> box;
      box.create();
      box->setRecordHistory(true);
      double xDist = fabs(maxPnt.x - minPnt.x) + 0.001;
      double yDist = fabs(maxPnt.y - minPnt.y) + 0.001;
      double zDist = fabs(maxPnt.z - minPnt.z) + 0.001;
      box->createBox(xDist, yDist, zDist);
      box->transformBy(AcGeMatrix3d().setTranslation(AcGeVector3d(minPnt.x + xDist/2, minPnt.y + yDist/2, minPnt.z + zDist/2)));
      AcDbBlockTableRecordPointer curSpace(curDoc()->database()->currentSpaceId(), AcDb::kForWrite);
      // if ok
      if (curSpace.openStatus() == Acad::eOk)
      {
        curSpace->appendAcDbEntity(box.object());
        // add a reactor to it
        box->addReactor(new MyBoxReactor());
        return true;
      }
    }
      return false;
  }
   // - asdkAcPointCloudTest.removeFilter command (do not rename)
 static void asdkAcPointCloudTestremoveFilter(void)
{
    // pick a point cloud
    ads_name ename;
    ads_point pnt;
    int res = acedEntSel(_T("\nSelect a Point Cloud : "), ename, pnt);
    // if ok
    if (res == RTNORM)
    {
      // then convert the ename to an object id
      AcDbObjectId id;
      acdbGetObjectId(id,ename);
    // just reset the point cloud view
    AcDbEntityPointer ent(id, AcDb::kForWrite);
      // if ok
      if (ent.openStatus() == Acad::eOk)
      {
        // reset the point cloud view
        Acad::ErrorStatus es = acdbResetPointCloudDataView(ent);
        // if not ok, possibly not a point cloud
        if (es != Acad::eOk)
        {
          acutPrintf(_T("\nNot a point cloud..."));
          return;
        }
      }
    }
}
    static void asdkAcPointCloudTesttest(void)
  {
    AcGePoint3d minPnt;
    acedInitGet(RSG_GETZ, NULL);
    // select the first bounding point
    int res = acedGetPoint(NULL, _T("\nSelect Bottom Left Corner : "), asDblArray(minPnt));
    // if ok
    if (res == RTNORM)
    {
      AcGePoint3d maxPnt;
      acedInitGet(RSG_GETZ, NULL);
      // select the second bounding point
      res = acedGetPoint(NULL, _T("\nSelect Top Right Corner : "), asDblArray(maxPnt));
      // if ok
      if (res == RTNORM)
      {
        // set up and nice extents box
        AcGeBoundBlock3d filterExtents;
        filterExtents.set(minPnt, maxPnt);
        DrawSlicerBox(filterExtents);       
          while(res == RTNORM)
        {
          AcGePoint3d inside;
          // select the second bounding point
          res = acedGetPoint(NULL, _T("\nPick a point : "), asDblArray(inside));
            if (filterExtents.contains(inside))
            acutPrintf(_T("\nInside"));
        }
      }
    }
  }
} ;
  //-----------------------------------------------------------------------------
IMPLEMENT_ARX_ENTRYPOINT(CAcPointCloudTestApp)
  ACED_ARXCOMMAND_ENTRY_AUTO(CAcPointCloudTestApp, asdkAcPointCloudTest, addFilter, addFilter, ACRX_CMD_TRANSPARENT, NULL)
ACED_ARXCOMMAND_ENTRY_AUTO(CAcPointCloudTestApp, asdkAcPointCloudTest, removeFilter, removeFilter, ACRX_CMD_TRANSPARENT, NULL)
ACED_ARXCOMMAND_ENTRY_AUTO(CAcPointCloudTestApp, asdkAcPointCloudTest, test, test, ACRX_CMD_TRANSPARENT, NULL)
  MyBoxReactor.cpp
#include "StdAfx.h"
#include "resource.h"
#include "MyBoxReactor.h"
#include "acadi.h"
#include "dynprops.h"
#include "axboiler.h"
#include "axpnt3d.h"
#include "dbobjptr2.h"
  //////////////////////////////////////////////////////////////////////////
void MyBoxReactor::modified(const AcDbObject* obj)
{
  // if we have a n assigned point cloud filter
  if (DocVars.docData().mPCFilter)
  {
    // make sure we have a 3d solid
    AcDb3dSolid *solid = AcDb3dSolid::cast(obj);
    if (solid)
    {
      if (!solid->isErased())
      {
        // extract the minPoint from the existing PCFilter
        AcGePoint3d minPnt, maxPnt;
        DocVars.docData().mPCFilter->mFilterExtents.getMinMaxPoints(minPnt, maxPnt);
          // get the IUknown of the entity, we’ll need it to get the properties for the instance and also so we can set them
        CComPtr<IUnknown> entIUnknown = NULL;
        HRESULT hr = AcAxGetIUnknownOfObject(&entIUnknown, obj->objectId(), acedGetAcadWinApp()->GetIDispatch(TRUE));
        double length=0.001, height=0.001, width=0.001;
          // get the box info
        AcRxClass* pAcrxClass = AcDb3dSolid::desc();
        // Per-instance dynamic property managers
        OPMPerInstancePropertyExtension* pPerInstanceExtension = GET_OPM_PERINSTANCE_EXTENSION_PROTOCOL(pAcrxClass);
        if (NULL != pPerInstanceExtension)
        {
          COleSafeArray sourceNames;
          CComBSTR sourceName;
          // get the property source names stored on the extension object
          pPerInstanceExtension->GetObjectPropertySourceNames((LPVARIANT)sourceNames);
          // find out how many we have
          long start = 0;
          long end = 0;
          sourceNames.GetLBound(1, &start);
          sourceNames.GetUBound(1, &end);
          // loop the property sources
          for (long i=start; i<=end; ++i)
          {
            // extract each one of the property sources out
            CComPtr<IPropertySource> propertySource;
            sourceNames.GetElement(&i, (void*)&sourceName);
            // GetPropertySourceAt does AddRef, so we directly assign pointer here.
            propertySource.p = GET_OPM_PERINSTANCE_PROPERTY_SOURCES()->GetPropertySourceAt(&sourceName);
            // if we have one
            if (propertySource.p)
            {
              // if ok
              if (SUCCEEDED(hr))
              {
                // extract the Dynamic properties from it
                COleSafeArray props;
                hr = propertySource->GetProperties(entIUnknown, props);
                // if ok
                if (SUCCEEDED(hr))
                {
                  // loop all the dynamic properties that we have
                  long start = 0;
                  long end = 0;
                  props.GetLBound(1, &start);
                  props.GetUBound(1, &end);
                  for (long i=start; i<=end; ++i)
                  {
                    // first get the iUknown to make sure we have something
                    CComPtr<IUnknown> unknown = NULL;
                    props.GetElement(&i, (void*)&unknown);
                    // if we have
                    if (unknown.p)
                    {
                      // try and cast it to an updated IDynamicProperty2
                      CComQIPtr<IDynamicProperty2> dynProp = unknown;
                      // if ok
                      if (dynProp.p)
                      {
                        CComBSTR propName;
                        // extract out the property name
                        dynProp->GetDisplayName(&(propName.m_str));
                        // get the value
                        COleVariant getter;
                        dynProp->GetCurrentValueData(entIUnknown, getter);
                        // find out which property we are looking at
                        if (CString(propName) == _T("Length"))
                          length = ((*(tagVARIANT*)(&getter))).dblVal;
                        if (CString(propName) == _T("Width"))
                          width = ((*(tagVARIANT*)(&getter))).dblVal;
                        if (CString(propName) == _T("Height"))
                          height = ((*(tagVARIANT*)(&getter))).dblVal;;
                      }
                    }
                  }
                }
              }
            }
          }
            // now get the position from the solid
          CComQIPtr<IAcad3DSolid> solidCom(entIUnknown);
          if(solidCom != NULL)
          {
            COleVariant olePosition;
            hr = solidCom->get_Position(&olePosition);
            AcAxPoint3d position = olePosition;
              minPnt.x = position.x - length/2.0;
            minPnt.y = position.y - width/2.0;
            minPnt.z = position.z - height/2.0;
          }
            // finally, update the point cloud
          DocVars.docData().mPCFilter->mFilterExtents.set(minPnt, AcGePoint3d(minPnt.x+length, minPnt.y+width, minPnt.z+height));
            // and touch the point cloud for update
          AcDbBlockTableRecordPointer curSpace(curDoc()->database()->currentSpaceId(), AcDb::kForRead);
          // if ok
          if (curSpace.openStatus() == Acad::eOk)
          {
            AcDbObjectPointer<AcDbEntity> pointCloud( DocVars.docData().mPCFilter->mPointcloudId, AcDb::kForRead);
            // if ok
            if (pointCloud.openStatus() == Acad::eOk)
            {
              AcGsModel *gsModel = curDoc()->database()->gsModel();
              gsModel->onModified(AcGiDrawable::cast(pointCloud.object()), curSpace.object());
            }
          }
        }
      }
    }
  }
}
MyFilter.cpp
#include "StdAfx.h"
#include "resource.h"
#include "MyFilter.h"
  //////////////////////////////////////////////////////////////////////////
// this is my point cloud filter implementation, by Fenton Webb, DevTech, Autodesk 27/05/2010
void MyFilter::doFilter(const IAcPcDataBuffer& inBuffer, IAcPcDataBuffer&outBuffer)
{
  AcGePoint3d minPnt, maxPnt;
  mFilterExtents.getMinMaxPoints(minPnt, maxPnt);
    // this is just to show how often the filter function is being called
  acutPrintf(_T("\nfilter is called - min(%.2f,%.2f,%.2f) max(%.2f,%.2f,%.2f)"), minPnt.x, minPnt.y, minPnt.z, maxPnt.x, maxPnt.y, maxPnt.z);
    // ignoring native double buffers for brevity
  if(const_cast<IAcPcDataBuffer&>(inBuffer).nativeDbl())
    return;
    DWORD noOfOutPoints(0);
    AcPcPointFloat *pInPoints = const_cast<IAcPcDataBuffer&>(inBuffer).floatPoints();   
  AcPcPointFloat *pOutPoints = outBuffer.floatPoints();   
    // the points from the point cloud are raw points, we need to convert them into WCS
  // first let's work out the transform matrix
  double x, y, z;   
  inBuffer.offset(x, y, z);
  AcGeMatrix3d mx;
  inBuffer.entityTransform(mx);
    // now lets loop the points
  int length = inBuffer.size();
  int incrementFactor = 1;
  for (int i=0; i<length; i+=incrementFactor, pInPoints+=incrementFactor)
  {
    // now convert the raw point cloud points into WCS
    AcGePoint3d pt(pInPoints->m_x + x, pInPoints->m_y + y, pInPoints->m_z + z);
    pt = mx*pt;
      // finally check to see if the point lays inside of our box
    if (mFilterExtents.contains(pt))
    {
      // if so, add it to the out array list
      *(pOutPoints+noOfOutPoints) = *pInPoints;
      ++noOfOutPoints;
    }
  }
    // finally, we have less points to show obviously so adjust to suit
  outBuffer.shrink(noOfOutPoints);
}

## 评论

**内容**: xerion said...
Pretty useful thing,
Maybe a really simple question but typically users would want to snap to some points of the point cloud, however, the call to
AcDbEntityPointer ent(id, AcDb::kForWrite);
or more specifically the AcDb::kForWrite seems to kill the snapping on to the point cloud points.
Is it possible to have a workaround on that ?
Reply
05/09/2013 at 01:16 AM

---
**内容**: Fenton Webb said in reply to xerion...
Hey Xerion
yes, you are right, the snapping will be disabled.
To get round the problem, simply close the point cloud after the acdbResetPointCloudDataView() then reopen before acdbModifyPointCloudDataView()
Reply
05/09/2013 at 09:42 AM

---
**内容**: xerion said...
By the way should there be a call to acdbModifyPointCloudDataView
in the modified() function of the myBoxReactor ?
The extents are updated then the point cloud points should be updated as well since just notifying the graphic system is not enough to change the point cloud view and thus the acdbModifyPointCloudDataView is required.
Reply
05/09/2013 at 04:55 AM

---
**内容**: Fenton Webb said in reply to xerion...
for your second comment, you don't need to call acdbModifyPointCloudDataView() as the filter is already applied. My call to onModified will queue the graphics refresh at the next asynchronous graphics update.
Reply
05/09/2013 at 09:44 AM

---
**内容**: Richard said...
Good Day
Can you supply a working download of this application.
I usually do a lot of work in C# or Vb.Net so would take me a while to figure out this source code in C++?
Similar to download which one gets at codeproject?
Zip file with all the contents.
Would much appreciate
Please let us know if you can assist.
Best Regards
Richard
Reply
03/27/2014 at 02:37 AM

---
