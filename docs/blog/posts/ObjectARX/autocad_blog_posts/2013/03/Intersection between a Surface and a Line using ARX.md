---
title: "Intersection between a Surface and a Line using ARX"
date: 2013-03-01
categories:
  - AutoCAD C++
tags:
  - C++
  - ObjectARX
  - Surface
description: "In the other post, my colleague Philippe introduces how to get intersection between a planar face and a line. In this post, we will see how to get ..."
author: Autodesk
---
# Intersection between a Surface and a Line using ARX

发布日期: 2013-03-01

原始链接: https://adndevblog.typepad.com/autocad/2013/03/intersection-between-a-surface-and-a-line-using-arx.html

## 文章内容

By Xiaodong Liang
In the other post, my colleague Philippe introduces how to get intersection between a planar face and a line. In this post, we will see how to get intersection of an arbitrary surface and a line.
ARX provides AcGeCurveSurfInt which  allows you to get intersections of a 3D curve and a surface. AcGeCurveSurfInt  construction method or AcGeCurveSurfInt::Set can input the curve and the surface. While it requires the AcGeSurface. So we need some conversion from AcDbSurface to AcGeSurface. This requires AcBrBrep as the intermediate object.
Following is a small demo code. It asks the user to select a surface and get the intersection of a line (from (0,0,0) to (0,0,1)) and the surface.
Note: The Brep objects are provided by separate include files and lib files. You can find them at: ObjectARX SDK\\utils\brep
static AcGePoint3dArray Intersect(AcDbSurface* pSurface,AcGeLine3d line)
{  
    AcGePoint3dArray returnPtArray; 
  AcDbBody* pBody = new AcDbBody();
    // 2013
  // Acad::ErrorStatus es = pBody->setASMBody(pSurface->ASMBodyCopy());
  //before 20123
   Acad::ErrorStatus es = pBody->setBody(pSurface->body());
     //build AcBrBrep
   AcBrBrep* pBrep = new AcBrBrep();
   //
  if(AcBr::eOk == pBrep->set(*pBody))
  {
    AcBrBrepFaceTraverser* pFaceTrav = new AcBrBrepFaceTraverser;
    if(AcBr::eOk == pFaceTrav->setBrep(*pBrep))
   {
       for(pFaceTrav->restart();!pFaceTrav->done();pFaceTrav->next())
       {
        AcBrFace face;
          if(AcBr::eOk == pFaceTrav->getFace(face))
        {
          double area = 0.0f;
         face.getSurfaceArea(area);
           acutPrintf(L"\nSurface Area: %f", area);
          //*****whole surface of the Brep face******         
        //AcGeNurbSurface nurbSurface;
        //face.getSurfaceAsNurb(nurbSurface);
        //AcGeCurveSurfInt curveSI;
        ////input the curve and line
        //curveSI.set(line,nurbSurface);
        ////get the count of intersect points
        //int count = curveSI.numIntPoints(err_1);
        //    if(err_1 == AcGe::kXXOk && count >0 )
        //    {        
        //        AcGeIntersectError err_2;
        //        for(int index = 0 ;index < count; index ++)
        //        {
        //           AcGePoint3d pt =
        //             curveSI.intPoint(index,err_2);       
        //            returnPtArray.append(pt);
        //        }       
        //       
        //    }
        //**********
          //****real surface of the orignal AcDbSurface        
          AcGeExternalBoundedSurface** nurbs = NULL;
          Adesk::UInt32 numNurbs = 0;
          face.getSurfaceAsTrimmedNurbs(numNurbs,nurbs);
          //*****
          for (Adesk::UInt32 i = 0; i < numNurbs; i++)
        {
            AcGeCurveSurfInt curveSI;
            AcGeIntersectError  err_1 = AcGe::kXXOk;           
             //input the curve and line
            curveSI.set(line,*nurbs[i]);
              //get the count of intersect points
            int count = curveSI.numIntPoints(err_1);
            if(err_1 == AcGe::kXXOk && count >0 )
            {
                AcGeIntersectError err_2;
                for(int index = 0 ;index < count; index ++)
                {
                    AcGePoint3d pt =
                        curveSI.intPoint(index,err_2);       
                    returnPtArray.append(pt);
                }       
            }
            delete nurbs[i];
        }
        // your responsibility to delete the
       // array of surfaces
        delete[] nurbs;
      }
    }
  }
  delete pFaceTrav;
  }
  delete pBrep;
      return returnPtArray;
  }
static void getIntersectPts(void)
{
     ads_name ename;
     ads_point pickpt;
       AcDbObjectId objId;
     AcDbObject *pObj;
       int rc;
       // select a surface
     rc= acedEntSel(L"\nSelect Surface: ", ename, pickpt);
       if(rc != RTNORM)
     {
       if (rc != RTCAN)
         acutPrintf(L"\nError selecting entity ");
      return;
     }
       acdbGetObjectId(objId, ename);
     acdbOpenObject(pObj, objId, AcDb::kForRead);
       AcDbSurface* pEntity1 = AcDbSurface::cast(pObj);
       if(!pEntity1)
     {
          acutPrintf(L"\nSelection Invalid...");
          pObj->close();
          return;
     }
     // call Intersect
     AcGePoint3dArray points =
         Intersect(pEntity1,AcGeLine3d(AcGePoint3d(0,0,0),
         AcGePoint3d(0,0,1)));
     if(points.length() >0)
     {
         // iterate the points
     }
       pObj->close();
  }

## 评论

**内容**: Alexander Rivilis said...
Typo: //before 20123
Reply
03/05/2013 at 01:45 AM

---
**内容**: Jason Paterson said...
This sample does not return any intersections in AutoCAD 2015 SP1. numIntPoints always returns 0 with kXXUnknown no matter the surface (even the same surface that works in AutoCAD 2013).
Reply
10/03/2014 at 08:08 AM

---
**内容**: Alexander Rivilis said in reply to Jason Paterson...
It maybe a bug. But you can try this solution: http://adndevblog.typepad.com/autocad/2014/08/acdbregiontransformby-.html
These problems may be related.
Reply
10/04/2014 at 02:40 PM

---
**内容**: Jason Paterson said in reply to Alexander Rivilis...
I was aware of the global tolerance issue but setting it did not fix the problem.
Reply
10/08/2014 at 11:55 AM

---
**内容**: Alexander Rivilis said in reply to Jason Paterson...
Hi Jason!
I found a bug and workaround with this code. Try to replace AcGeLine3d with AcGeLineSeg3d in this code (e.g. change unbounded to bounded curve).
I hope Xiaodong Liang submit this bug to DevTeam.
Reply
10/08/2014 at 02:43 PM

---
**内容**: Alexander Rivilis said in reply to Alexander Rivilis...
Also you can check this code:
http://adn-cis.org/forum/index.php?topic=59.msg4561#msg4561
Reply
10/08/2014 at 03:00 PM

---
**内容**: Jason Paterson said in reply to Alexander Rivilis...
Thanks
Reply
10/09/2014 at 09:12 AM

---
