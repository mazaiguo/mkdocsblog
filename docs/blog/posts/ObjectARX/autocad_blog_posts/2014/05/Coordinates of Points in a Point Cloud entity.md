---
title: "Coordinates of Points in a Point Cloud entity"
date: 2014-05-01
categories:
  - AutoCAD
tags:
  - API
  - Dimension
description: "For a PointCloud entity created using a PCG file, a simple way to get the coordinates of the points would be insert a spatial filter using the "acd..."
author: Autodesk
---
# Coordinates of Points in a Point Cloud entity

发布日期: 2014-05-01

原始链接: https://adndevblog.typepad.com/autocad/2014/05/coordinates-of-points-in-a-point-cloud-entity.html

## 文章内容

By Balaji Ramamoorthy
For a PointCloud entity created using a PCG file, a simple way to get the coordinates of the points would be insert a spatial filter using the "acdbModifyPointCloudDataView" method. For the PointCloud entity created using RCP file, the way to insert a spatial filter is to use the "AcDbPointCloudEx::addSpatialFilter" method. While creating a spatial filter would still provide access to the point coordinates, the other method is to use the "AcDbPointCloudEx::traverseAllPointData" method.
Here is a sample code to identify the coordinates of the point using the "traverseAllPointData" method :
#include "AcPointCloud.h"
#include "AcDbPointCloudEx.h"
#include "AcDbPointCloudApi.h"
  class MyPointCloudProcessor
                        : public IAcDbPointCloudPointProcessor
{
public:
    MyPointCloudProcessor(){}
      virtual ~MyPointCloudProcessor(){}
      virtual ProcessSate process(
                    const IAcDbPointCloudDataBuffer* buffer)
    {
        const AcGePoint3d *pts = buffer->points();
        for(int cnt = 0; cnt < buffer->numPoints(); cnt++)
        {
            AcGePoint3d pt = pts[cnt];
            // Get the pt coordinates
        }
        return ProcessSate::Continue;
    }
};
  static void AdskMyTestCommand()
{
    ads_point pt;
    ads_name name;
    if (acedEntSel
        ( L"Select a point cloud",
            name, pt) != RTNORM)
        return;
      AcDbObjectId id;
    if (acdbGetObjectId(id, name) != Acad::eOk)
        return;
      AcDbEntityPointer pEntity(id, AcDb::kForWrite);
    if (pEntity.openStatus() != Acad::eOk)
        return;
      AcDbPointCloudEx *pPtCloud
                            = AcDbPointCloudEx::cast(pEntity);
    if(pPtCloud == NULL)
        return;
      MyPointCloudProcessor *pPCProcessor
                                = new MyPointCloudProcessor();
      // The last parameter is the Level of Detail.
    // There is currently no way to get the maximum LOD value
    // from a pointcloud entity.
    // You can pass a value between 1 and 100 depending
    // on the Level of detail required.
    pPtCloud->traverseAllPointData(pPCProcessor, NULL,
              IAcDbPointCloudDataBuffer::DataType::kColor, 2);
    if(pPCProcessor != NULL)
    {
        delete pPCProcessor;
        pPCProcessor = NULL;
    }
}

## 评论

**内容**: Rik De Peuter said...
This code snippet was a massive help to us, but there is 1 little error in it:
if(pPtCloud != NULL)
return;
Should be:
if(pPtCloud == NULL)
return;
:)
Reply
05/02/2014 at 01:09 AM

---
**内容**: Balaji said in reply to Rik De Peuter...
Thanks Rik.
I have corrected the code snippet.
Regards,
Balaji
Reply
05/02/2014 at 01:16 AM

---
**内容**: dr.lee said in reply to Balaji...
pPtCloud->traverseAllPointData(pPCProcessor, NULL,
IAcDbPointCloudDataBuffer::DataType::kColor, 2);
my question:
how can I define the spatial filter by using IAcDbPointCloudSpatialFilter?
trank you.
dr.lee
Reply
06/22/2014 at 07:18 PM

---
**内容**: dr.lee said in reply to dr.lee...
following are my codes of overriding class of IAcDbPointCloudSpatialFilter.
I write the code as your above AdskMyTestCommand(). If I use following (1) and set the spatial filter to NULL in traverseAllPointData(...), then through my check, the filter is not effect.
and if I give the spatial filter in traverseAllPointData(...), then the process of traverseAllPointData return eOutOfMemory. What is the correct usage of IAcDbPointCloudSpatialFilter in traverseAllPointData?
(1)
pcSpatialFilter.testCell(min, max);
pPCloudEntity->addSpatialFilter(&pcSpatialFilter);
(2)
class IPsAcDbPointCloudSpatialFilter : public IAcDbPointCloudSpatialFilter
{
public:
IPsAcDbPointCloudSpatialFilter() {;}
virtual ~IPsAcDbPointCloudSpatialFilter(){;}
virtual FilterResult testCell(const AcGePoint3d& min, const AcGePoint3d& max) const { return IAcDbPointCloudSpatialFilter::FILTER_OUTSIDE; }
virtual FilterResult testPoint(const AcGePoint3d& point) const { return IAcDbPointCloudSpatialFilter::FILTER_OUTSIDE; }
virtual IAcDbPointCloudSpatialFilter* transformFilter(const AcGeMatrix3d& mat) const { return NULL; }
virtual IAcDbPointCloudSpatialFilter* clone() const { return NULL; }
virtual void freeObject() { ; }
};

regards!
dr.lee.
Reply
06/23/2014 at 12:06 AM

---
**内容**: Balaji said in reply to dr.lee...
Hi Dr.Lee,
My apologies for the delayed response. Your update to this blog post just slipped through and I did not notice it. Sorry about that.
Here is a sample code that my colleague Philippe Leefsma implemented. If you have any more specific questions on this topic, please create a forum post in the AutoCAD discussion forum and you can send me the link. We can continue to discuss it there so it benefits all.
// include AcDbPointCloudApi.h
class TestPointCloudSpatialFilter: public IAcDbPointCloudSpatialFilter
{
public:
TestPointCloudSpatialFilter(const AcGePoint3d& centerPt, const AcGePoint3d& edgePt);
virtual ~TestPointCloudSpatialFilter();
virtual FilterResult testCell(const AcGePoint3d& min, const AcGePoint3d& max) const;
virtual FilterResult testPoint(const AcGePoint3d& point) const;
virtual IAcDbPointCloudSpatialFilter* transformFilter(const AcGeMatrix3d& mat) const;
virtual IAcDbPointCloudSpatialFilter* clone() const;
virtual void freeObject();
AcGePoint3d getCenterPt();
AcGePoint3d getEdgePt();
void setCenterPt(const AcGePoint3d& centerPt);
void setEdgePt (const AcGePoint3d& edgePt);
private:
AcGePoint3d m_centerPt;
AcGePoint3d m_edgePt;
};
//Imp for TestPointCloudSptialFilter
TestPointCloudSpatialFilter::TestPointCloudSpatialFilter(const AcGePoint3d& centerPt, const AcGePoint3d& edgePt)
{
m_centerPt = centerPt;
m_edgePt = edgePt;
}
TestPointCloudSpatialFilter::~TestPointCloudSpatialFilter()
{
}
AcGePoint3d TestPointCloudSpatialFilter::getCenterPt()
{
return m_centerPt;
}
void TestPointCloudSpatialFilter::setCenterPt(const AcGePoint3d& centerPt)
{
m_centerPt = centerPt;
}
AcGePoint3d TestPointCloudSpatialFilter::getEdgePt()
{
return m_edgePt;
}
void TestPointCloudSpatialFilter::setEdgePt(const AcGePoint3d& edgePt)
{
m_edgePt = edgePt;
}
IAcDbPointCloudSpatialFilter::FilterResult TestPointCloudSpatialFilter::testCell(
const AcGePoint3d& min,
const AcGePoint3d& max) const
{
int inNum = 0;
int outNum = 0;
AcGePoint3dArray pts;
bool bHasIntersection = false;
pts.append(AcGePoint3d(min.x, min.y, min.z));
pts.append(AcGePoint3d(min.x, max.y, min.z));
pts.append(AcGePoint3d(min.x, min.y, max.z));
pts.append(AcGePoint3d(min.x, max.y, max.z));
pts.append(AcGePoint3d(max.x, max.y, max.z));
pts.append(AcGePoint3d(max.x, min.y, min.z));
pts.append(AcGePoint3d(max.x, max.y, min.z));
pts.append(AcGePoint3d(max.x, min.y, max.z));
double radius = m_centerPt.distanceTo(m_edgePt);
for (int i = 0; i < pts.length(); i ++)
{
if (testPoint(pts[i]) == IAcDbPointCloudSpatialFilter::FILTER_INSIDE)
{
inNum ++;
}
if (testPoint(pts[i]) == IAcDbPointCloudSpatialFilter::FILTER_OUTSIDE)
{
outNum ++;
}
if (inNum * outNum != 0)
{
return IAcDbPointCloudSpatialFilter::FILTER_INTERSECTS;
}
}
if (outNum == 0)
{
return IAcDbPointCloudSpatialFilter::FILTER_INSIDE;
}
else if (inNum == 0) //The box contains the sphere or the box is outside the sphere.
{
AcGeBoundBlock3d boundBox;
boundBox.set(min,max);
//If the boundblock3d contains the sphere center point and edge point, the boundblock3d should interect with sphere
if ((boundBox.contains(m_edgePt)) && (boundBox.contains(m_centerPt)))
{
return IAcDbPointCloudSpatialFilter::FILTER_INTERSECTS;
}
else
{
return IAcDbPointCloudSpatialFilter::FILTER_OUTSIDE;
}
}
return inNum == 8 ? IAcDbPointCloudSpatialFilter::FILTER_INSIDE : IAcDbPointCloudSpatialFilter::FILTER_OUTSIDE;
}
IAcDbPointCloudSpatialFilter::FilterResult TestPointCloudSpatialFilter::testPoint(const AcGePoint3d& point) const
{
double radius = m_centerPt.distanceTo(m_edgePt);
if (m_centerPt.distanceTo(point) <= radius)
{
return IAcDbPointCloudSpatialFilter::FILTER_INSIDE;
}
else
{
return IAcDbPointCloudSpatialFilter::FILTER_OUTSIDE;
}
}
IAcDbPointCloudSpatialFilter* TestPointCloudSpatialFilter::transformFilter(const AcGeMatrix3d& mat) const
{
TestPointCloudSpatialFilter *pSptailFilter = new TestPointCloudSpatialFilter(*this);
AcGePoint3d &pTransCenterPt = pSptailFilter->m_centerPt.transformBy(mat);
AcGePoint3d &pTransEdgePt = pSptailFilter->m_edgePt.transformBy(mat);
return pSptailFilter;
}
IAcDbPointCloudSpatialFilter* TestPointCloudSpatialFilter::clone() const
{
return new TestPointCloudSpatialFilter(*this);
}
void TestPointCloudSpatialFilter::freeObject()
{
delete this;
}
Regards,
Balaji
Reply
09/05/2014 at 12:12 AM

---
**内容**: Mey said...
Why this breliant methode (traverseAllPointData) not included to .net API of autocad
Reply
06/12/2024 at 07:41 AM

---
