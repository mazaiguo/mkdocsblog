---
title: "Accessing sub-entities using AssocPersSubentityIdPE in ARX or .Net"
date: 2012-07-01
categories:
  - AutoCAD .NET
tags:
  - .NET
  - AutoCAD
  - C#
  - C++
  - ObjectARX
description: "How do I access the sub-entities of an AutoCAD entity in ObjectARX or .Net?"
author: Autodesk
---
# Accessing sub-entities using AssocPersSubentityIdPE in ARX or .Net

发布日期: 2012-07-01

原始链接: https://adndevblog.typepad.com/autocad/2012/07/accessing-sub-entities-using-assocperssubentityidpe-in-arx-or-net.html

## 文章内容

By Philippe Leefsma
Q:
How do I access the sub-entities of an AutoCAD entity in ObjectARX or .Net?
A:
Below are two samples in C++ and C# that illustrate how to access the AssocPersSubentityIdPE and use it to iterate through the vertices and edges of the selected entity.
////////////////////////////////////////////////////////////////////////////////////
//Use: Retrieves entity vertices & edges using AssocPersSubentityIdPE
//
////////////////////////////////////////////////////////////////////////////////////
void ArxSubEntityPE()
{
        Acad::ErrorStatus err;
          ads_name name;
        ads_point pt;
          if(acedEntSel(L"\nSelect an Entity: ", name, pt) != RTNORM)
                return;
          AcDbObjectId id;
        acdbGetObjectId(id, name);
          AcDbObjectPointer <AcDbEntity> pEntity(id, AcDb::kForRead);
          // Get the Protocol extension associated with the entity
        AcDbAssocPersSubentIdPE* const pAssocPersSubentIdPE =
                AcDbAssocPersSubentIdPE::cast(
                        pEntity->queryX(AcDbAssocPersSubentIdPE::desc()));
          if( pAssocPersSubentIdPE == NULL)
                return;
          AcArray <AcDbSubentId> vertexIds;
        pAssocPersSubentIdPE->getAllSubentities(
                pEntity,
                AcDb::kVertexSubentType,
                vertexIds);
          acutPrintf(L"\n- Vertex Subentities: ");
          for (int i = 0; i<vertexIds.length(); ++i)
        {
                AcDbFullSubentPath path(id, vertexIds[i]);
                  AcDbPoint* pPoint = AcDbPoint::cast(pEntity->subentPtr(path));
                        if (pPoint != NULL)
                {
                   AcGePoint3d pos = pPoint->position();
                   acutPrintf(L"\n . Vertex: [%.2f, %.2f, %.2f]",
                       pos.x, pos.y, pos.z);
                        delete pPoint;
                }
        }
          AcArray <AcDbSubentId> edgeIds;
        pAssocPersSubentIdPE->getAllSubentities(
                pEntity,
                AcDb::kEdgeSubentType,
                edgeIds);
                acutPrintf(L"\n- Edge Subentities: ");
          for (int i = 0; i<edgeIds.length(); ++i)
        {
                AcDbFullSubentPath path(id, edgeIds[i]);
                  AcDbEntity* pSubEntity = pEntity->subentPtr(path);
                        if (pSubEntity != NULL)
                {
                        acutPrintf(L"\n . %s (Id = %d)",
                                pSubEntity->isA()->name(),
                                edgeIds[i].index());
                          delete pSubEntity;
                }
        }
}
      ////////////////////////////////////////////////////////////////////////////////
//Use: Retrieves entity vertices, edges, faces using AssocPersSubentityIdPE
//
////////////////////////////////////////////////////////////////////////////////
[CommandMethod("SubEntityPE")]
public void SubEntityPE()
{
    Document doc = Application.DocumentManager.MdiActiveDocument;
    Database db = doc.Database;
    Editor ed = doc.Editor;
      PromptEntityOptions peo = new PromptEntityOptions(
        "\nSelect an Entity: ");
      PromptEntityResult per = ed.GetEntity(peo);
      if (per.Status != PromptStatus.OK)
        return; 
      using (Transaction Tx = db.TransactionManager.StartTransaction())
    {
        Entity entity = Tx.GetObject(per.ObjectId, OpenMode.ForRead)
            as Entity;
          ObjectId[] entId = new ObjectId[] { entity.ObjectId };
          IntPtr pSubentityIdPE = entity.QueryX(
            AssocPersSubentityIdPE.GetClass(
            typeof(AssocPersSubentityIdPE)));
          if (pSubentityIdPE == IntPtr.Zero)
            //Entity doesn't support the subentityPE
            return;
          AssocPersSubentityIdPE subentityIdPE =
            AssocPersSubentityIdPE.Create(pSubentityIdPE, false)
                as AssocPersSubentityIdPE;
          SubentityId[] vertexIds = subentityIdPE.GetAllSubentities(
            entity,
            SubentityType.Vertex);
          ed.WriteMessage("\n- Vertex Subentities: ");
          foreach (SubentityId subentId in vertexIds)
        {
            FullSubentityPath path = new FullSubentityPath(entId, subentId);
              DBPoint vertex = entity.GetSubentity(path) as DBPoint;
              if (vertex != null)
            {
                ed.WriteMessage(
                    "\n . Vertex: [{0}, {1}, {2}]",
                    vertex.Position.X,
                    vertex.Position.Y,
                    vertex.Position.Z);
                  vertex.Dispose();
            }
        }
          SubentityId[] edgeIds = subentityIdPE.GetAllSubentities(
            entity,
            SubentityType.Edge);
          ed.WriteMessage("\n- Edge Subentities: ");
          foreach (SubentityId subentId in edgeIds)
        {
            FullSubentityPath path = new FullSubentityPath(entId, subentId);
              Entity edgeEntity = entity.GetSubentity(path);
              if (edgeEntity != null)
            {
                ed.WriteMessage("\n . " + edgeEntity.ToString());
                edgeEntity.Dispose();
            }
        }
            SubentityId[] faceIds = subentityIdPE.GetAllSubentities(
            entity,
            SubentityType.Face);
          ed.WriteMessage("\n- Face Subentities: ");
          foreach (SubentityId subentId in faceIds)
        {
            FullSubentityPath path = new FullSubentityPath(entId, subentId);
              Entity faceEntity = entity.GetSubentity(path);
              if (faceEntity != null)
            {
                ed.WriteMessage("\n . " + faceEntity.ToString());
                faceEntity.Dispose();
            }
        }
    }
}

## 评论

**内容**: Konstantin said...
Hello Philippe,
how can i retrieve the color or the colorindex of a face subentity using your C# .NET version of AssocPersSubentityIdPE example above ?
i added the following code using the GetSubentityColor(subentId)method but an exception is generated.... eNotApplicable:
You have reported on this at the thread below as to not have found a way to workaround this behavior
http://forums.autodesk.com/t5/NET/Getsubentitycolor/td-p/5059712
The BREP "path" generates the same exception !
The exception is generated for ALL solids having FACES with no explicitly associated color via SOLIDEDIT command eg. 256 ByLayer, or 257 ByEntity
For solids with ALL faces having subentity color other than 256 or 257 NO exception is generated.
Here is the code
short colIDx = entity.GetSubentityColor(subentId).ColorIndex;

if (faceEntity != null)
{
if (faceEntity.GetType() == typeof(_AcDb.Surface))
{
_AcDb.Surface sEnt = faceEntity as _AcDb.Surface;
ed.WriteMessage(

"\n SubentId IndexPtr : {0}" +
"\n Face Perimeter : {1}" +
"\n Face Area : {2}" +
"\n Color Index : {3}",
subentId.IndexPtr,
sEnt.Perimeter,
sEnt.GetArea(),
colIDx
//face.GetPerimeterLength()
//face.GetArea().ToString()
//brp.Solid.GetSubentityColor(fSubEntpath.SubentId).ColorIndex
//sEnt.ColorIndex.ToString()
);
}
else if (faceEntity.GetType() == typeof(_AcDb.Region))
{
Region rEnt = faceEntity as Region;
ed.WriteMessage(

"\n SubentId IndexPtr : {0}" +
"\n Face Perimeter : {1}" +
"\n Face Area : {2}" +
"\n Color Index : {3}",
subentId.IndexPtr,
rEnt.Perimeter,
rEnt.Area,
colIDx
//face.GetPerimeterLength()
//face.GetArea().ToString()
//brp.Solid.GetSubentityColor(fSubEntpath.SubentId).ColorIndex
//rEnt.ColorIndex.ToString()
);
}
//ed.WriteMessage("\n . " + faceEntity.ToString());
faceEntity.Dispose();
}
Reply
07/14/2014 at 09:41 AM

---
**内容**: Philippe said...
There seem to be no way to overcome the exception: wrap your code that retrieve the face color in a try/catch block. If the face has a subentity color set to it, you can access it, otherwise it will throw an exception.
I hope that helps,
Philippe.
Reply
07/14/2014 at 11:47 AM

---
**内容**: Konstantin said in reply to Philippe...
I hope that the bug will be fixed ASAP !
The exception is generated in ACAD 2012, ACAD 2014, ACAD 2015 in 32+64bit .
I use the code below and it seems to work ...
Thanks for responding
Konstantin
try
{
if (sol != null)
colIdx = sol.GetSubentityColor(face.SubentityPath.SubentId).ColorIndex;
else if (surf != null)
colIdx = surf.GetSubentityColor(face.SubentityPath.SubentId).ColorIndex;
}
catch
{
colIdx = brepEnt.Color.ColorIndex;
//Color color = Color.FromColorIndex(ColorMethod.ByColor, colIdx);
//sol.SetSubentityColor(face.SubentityPath.SubentId, color);
}
Reply
07/15/2014 at 04:18 AM

---
