---
title: "Working with vertices, edges and faces of a SubDMesh"
date: 2012-04-01
categories:
  - AutoCAD C++
tags:
  - C++
  - Dimension
  - ObjectARX
  - Plot
description: "The "SubDMesh" does provide properties such as "Vertices", "EdgeArray" and "FaceArray", to retrieve the vertices, edges and faces that form the mes..."
author: Autodesk
---
# Working with vertices, edges and faces of a SubDMesh

发布日期: 2012-04-01

原始链接: https://adndevblog.typepad.com/autocad/2012/04/working-with-vertices-edges-and-faces-of-a-subdmesh.html

## 文章内容

By Balaji Ramamoorthy
The "SubDMesh" does provide properties such as "Vertices", "EdgeArray" and "FaceArray", to retrieve the vertices, edges and faces that form the mesh. To make use of this information, it is important to understand the way the vertices, edges and faces are obtained from these methods.
In the "FaceArray", the number of vertices in a face is the first to appear in the array, which is then followed by the indices of the edges that make up the face.
The "EdgeArray" simply returns the indices of the vertices that make each edge.
The "Vertices" are point coordinates of each vertex in the mesh.
For more details on the layout of the face array, please refer to the ObjectARX documentation under the “AcGiGeometry::shell” topic.
Here is a sample code that prints the edges that make the faces and the vertices that make the edges.
[CommandMethod("SubDMeshTest")]
public static void SubDMeshTest()
{
    Document activeDoc
        = Application.DocumentManager.MdiActiveDocument;
    Database db = activeDoc.Database;
    Editor ed = activeDoc.Editor;
      TypedValue[] values ={new TypedValue(
                        (int)DxfCode.Start,
                        "MESH")};
      SelectionFilter filter = new SelectionFilter(values);
    PromptSelectionResult psr = ed.SelectAll(filter);
    SelectionSet ss = psr.Value;
    if (ss == null)
        return;
      using (Transaction trans
        = db.TransactionManager.StartTransaction())
    {
        for (int i = 0; i < ss.Count; ++i)
        {
            SubDMesh mesh =
                trans.GetObject(ss[i].ObjectId,
                        OpenMode.ForRead) as SubDMesh;
              ed.WriteMessage(String.Format("\n Vertices : {0}",
                             mesh.NumberOfVertices));
              ed.WriteMessage(String.Format("\n Edges    : {0}",
                            mesh.NumberOfEdges));
              ed.WriteMessage(String.Format("\n Faces    : {0}",
                           mesh.NumberOfFaces));
              // Get the Face information
            int[] faceArr = mesh.FaceArray.ToArray();
            int edges = 0;
            int fcount = 0;
              for (int x = 0;
                    x < faceArr.Length;
                    x = x + edges + 1
                )
            {
                ed.WriteMessage(String.Format("\n Face {0} : ",
                                        fcount++));
                  edges = faceArr[x];
                for (int y = x + 1;
                        y <= x + edges;
                        y++
                    )
                {
                    ed.WriteMessage(String.Format("\n\t Edge - {0}",
                                     faceArr[y]));
                }
            }
              // Get the Edge information
            int ecount = 0;
            int[] edgeArr = mesh.EdgeArray.ToArray();
              for (int x = 0;
                    x < edgeArr.Length;
                    x = x + 2)
            {
                ed.WriteMessage(String.Format("\n Edge {0} : ",
                                    ecount++));
                  ed.WriteMessage(String.Format("\n Vertex - {0}",
                                    edgeArr[x]));
                  ed.WriteMessage(String.Format("\n Vertex - {0}",
                                    edgeArr[x + 1]));
            }
              // Get the vertices information
            int vcount = 0;
            foreach (Point3d vertex in mesh.Vertices)
            {
                ed.WriteMessage(String.Format(
                                "\n Vertex {0} - {1} {2}",
                                vcount++,
                                vertex.X,
                                vertex.Y));
            }
        }
        trans.Commit();
    }
}
        //Here is the output for very simple SubDMesh :
   Vertices : 9
 Edges    : 12
 Faces    : 4
 Face 0 :
  Edge - 0
  Edge - 1
  Edge - 2
  Edge - 3
 Face 1 :
  Edge - 1
  Edge - 4
  Edge - 5
  Edge - 2
 Face 2 :
  Edge - 5
  Edge - 6
  Edge - 7
  Edge - 2
 Face 3 :
  Edge - 7
  Edge - 8
  Edge - 3
  Edge - 2
 Edge 0 :
 Vertex - 0
 Vertex - 1
 Edge 1 :
 Vertex - 1
 Vertex - 2
 Edge 2 :
 Vertex - 2
 Vertex - 3
 Edge 3 :
 Vertex - 0
 Vertex - 3
 Edge 4 :
 Vertex - 1
 Vertex - 4
 Edge 5 :
 Vertex - 4
 Vertex - 5
 Edge 6 :
 Vertex - 2
 Vertex - 5
 Edge 7 :
 Vertex - 5
 Vertex - 6
 Edge 8 :
 Vertex - 6
 Vertex - 7
 Edge 9 :
 Vertex - 2
 Vertex - 7
 Edge 10 :
 Vertex - 7
 Vertex - 8
 Edge 11 :
 Vertex - 3
 Vertex - 8
   Vertex 0 - 0 0
 Vertex 1 - 0.5 0
 Vertex 2 - 0.5 0.5
 Vertex 3 - 0 0.5
 Vertex 4 - 1 0
 Vertex 5 - 1 0.5
 Vertex 6 - 1 1
 Vertex 7 - 0.5 1
 Vertex 8 - 0 1

