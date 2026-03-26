---
title: "Importing AutoCAD solids to Three.js"
date: 2015-01-01
categories:
  - AutoCAD
tags:
  - AutoCAD
  - Solid
description: "Recently I have been looking at using PhysiJS for collision detection in AutoCAD. To get started with it, AutoCAD solids had to be imported in a Th..."
author: Autodesk
---
# Importing AutoCAD solids to Three.js

发布日期: 2015-01-01

原始链接: https://adndevblog.typepad.com/autocad/2015/01/importing-autocad-solids-to-threejs.html

## 文章内容

By Balaji Ramamoorthy
Recently I have been looking at using PhysiJS for collision detection in AutoCAD. To get started with it, AutoCAD solids had to be imported in a Three.js scene. The following nice blog posts in Kean's blog provided the required head start.
Viewing 3d solids using Three.js
Connecting Three.js to an AutoCAD model - Part I
Connecting Three.js to an AutoCAD model - Part II
In these blog posts, the geometric extents of the AutoCAD solids are displayed as bounding boxes in Three.js. To include Physics, it was required to get the actual shape of the solid, so a few changes were needed.
In this blog post, I will only hightlight the changes to import AutoCAD solids into Three.js. I will include the PhysiJS portion of the code in my next blog post. This is to keep the Three.js and PhysiJS portions separate.
Here are the changes to the code from "Connecting Three.js to an AutoCAD model - Part II" :
Changes to Utils.cs
 internal  class  MeshData
 {
     public  double  _dist;
     public  string _handle;
     public  Extents3d _exts;
     public  Point3dCollection _vertices;
     public  Int32Collection _faces;
     public  string _color;
       public  MeshData()
     {
         _dist = 1.0;
         _handle = String.Empty;
         _exts = new  Extents3d();
         _vertices = new  Point3dCollection();
         _faces = new  Int32Collection();
         _color = String.Empty;
     }
       public  MeshData(
   double   dist, 
   string handle, 
   Extents3d exts, 
   Point3dCollection vertices, 
   Int32Collection faces, 
   string color)
     {
         _dist = dist;
         _handle = handle;
         _exts = exts;
         _vertices = vertices;
         _faces = faces;
         _color = color;
     }
 }
   using  Autodesk.AutoCAD.Geometry;
   internal  static  List<MeshData> SolidInfoForCollection(
  Document doc, 
  Point3d camPos, 
  ObjectIdCollection ids)
 {
     var sols = new  List<MeshData>();
        using  (var tr 
   = doc.TransactionManager.StartOpenCloseTransaction())
     {
         foreach (ObjectId id in ids)
         {
             Entity ent = tr.GetObject(
     id, 
     OpenMode.ForRead) as Entity;
               // Entity handle to name the Three.js objects 
             String hand = ent.Handle.ToString();
             Autodesk.AutoCAD.Colors.EntityColor clr 
           = ent.EntityColor;
               // Entity color to use for the Three.js objects 
             long  b, g, r;
             if  (ent.ColorIndex < 256)
             {
                 System.Byte byt 
      = System.Convert.ToByte(ent.ColorIndex);
                 int  rgb = EntityColor.LookUpRgb(byt);
                 b = (rgb & 0xffL);
                 g = (rgb & 0xff00L) >> 8;
                 r = rgb >> 16;
             }
             else 
             {
                 b = 127;
                 g = 127;
                 r = 127;
             }
             String entColor 
    = "0x"  
    + String.Format("{0:X2}{1:X2}{2:X2}" , r, g, b);
               // Entity extents 
             Extents3d ext = ent.GeometricExtents;
                  var tmp = ext.MinPoint + 
     0.5 * (ext.MaxPoint - ext.MinPoint);
               Vector3d dir = ext.MaxPoint - ext.MinPoint;
             var mid = 
     new  Point3d(ext.MinPoint.X, tmp.Y, tmp.Z);
               var dist = camPos.DistanceTo(mid);
               if  (id.ObjectClass.Name.Equals("AcDbSubDMesh" ))
             {
                 // Already a Mesh.  
     //Get the face info and clean it up 
                 // a bit to export it as a THREE.Face3  
     // which only has three vertices 
                   var mesh = ent as SubDMesh;
                   Point3dCollection threeVertices 
       = new  Point3dCollection();
                   Int32Collection threeFaceInfo 
      = new  Int32Collection();
                   Point3dCollection vertices = mesh.Vertices;
                   int [] faceArr = mesh.FaceArray.ToArray();
                 int [] edgeArr = mesh.EdgeArray.ToArray();
                   Int32Collection faceVertices 
         = new  Int32Collection();
                   int  verticesInFace = 0;
                 int  facecnt = 0;
                 for  (int  x = 0; 
      x < faceArr.Length; facecnt++, 
      x = x + verticesInFace + 1)
                 {
                     faceVertices.Clear();
                       verticesInFace = faceArr[x];
                     for  (int  y = x + 1; 
       y <= x + verticesInFace; y++)
                     {
                         faceVertices.Add(faceArr[y]);
                     }
                       // Merging of mesh faces can result in  
      // faces with multiple vertices 
                     // A simple collinearity check can help  
      // remove those redundant vertices 
                     bool  continueCollinearCheck = false ;
                     do 
                     {
                         continueCollinearCheck = false ;
                         for  (int  index = 0; 
        index < faceVertices.Count; 
        index++)
                         {
                             int  v1 = index;
                               int  v2 = 
         (index + 1) >= faceVertices.Count ?
         (index + 1) - faceVertices.Count : 
         index + 1;
                               int  v3 = 
         (index + 2) >= faceVertices.Count ?
         (index + 2) - faceVertices.Count : 
         index + 2;
                               // Check collinear 
                             Point3d p1 
         = vertices[faceVertices[v1]];
                             Point3d p2 
         = vertices[faceVertices[v2]];
                             Point3d p3 
         = vertices[faceVertices[v3]];
                               Vector3d vec1 = p1 - p2;
                             Vector3d vec2 = p2 - p3;
                             if  (vec1.IsCodirectionalTo(vec2))
                             {
                                 faceVertices.RemoveAt(v2);
                                 continueCollinearCheck = true ;
                                 break ;
                             }
                         }
                     } while  (continueCollinearCheck);
                       if  (faceVertices.Count == 3)
                     {
                         Point3d p1 
        = vertices[faceVertices[0]];
                         Point3d p2 
        = vertices[faceVertices[1]];
                         Point3d p3 
        = vertices[faceVertices[2]];
                           if  (!threeVertices.Contains(p1))
                             threeVertices.Add(p1);
                         threeFaceInfo.Add(
        threeVertices.IndexOf(p1));
                           if  (!threeVertices.Contains(p2))
                             threeVertices.Add(p2);
                         threeFaceInfo.Add(
        threeVertices.IndexOf(p2));
                           if  (!threeVertices.Contains(p3))
                             threeVertices.Add(p3);
                         threeFaceInfo.Add(
        threeVertices.IndexOf(p3));
                     }
                     else  if  (faceVertices.Count == 4)
                     { // A face with 4 vertices,  
       // lets split it to  
                         // make it easier later to  
       // create a THREE.Face3  
                         Point3d p1 
        = vertices[faceVertices[0]];
                         Point3d p2 
        = vertices[faceVertices[1]];
                         Point3d p3 
        = vertices[faceVertices[2]];
                           if  (!threeVertices.Contains(p1))
                             threeVertices.Add(p1);
                         threeFaceInfo.Add(
        threeVertices.IndexOf(p1));
                           if  (!threeVertices.Contains(p2))
                             threeVertices.Add(p2);
                         threeFaceInfo.Add(
        threeVertices.IndexOf(p2));
                           if  (!threeVertices.Contains(p3))
                             threeVertices.Add(p3);
                         threeFaceInfo.Add(
        threeVertices.IndexOf(p3));
                           p1 = vertices[faceVertices[2]];
                         p2 = vertices[faceVertices[3]];
                         p3 = vertices[faceVertices[0]];
                           if  (!threeVertices.Contains(p1))
                             threeVertices.Add(p1);
                         threeFaceInfo.Add(
        threeVertices.IndexOf(p1));
                           if  (!threeVertices.Contains(p2))
                             threeVertices.Add(p2);
                         threeFaceInfo.Add(
        threeVertices.IndexOf(p2));
                           if  (!threeVertices.Contains(p3))
                             threeVertices.Add(p3);
                         threeFaceInfo.Add(
        threeVertices.IndexOf(p3));
                     }
                     else 
                     {
                         Application.DocumentManager.MdiActiveDocument.
        Editor.WriteMessage(
        "Face with more than 4 vertices will need triangulation to import in Three.js " );
                     }
                 }
                   sols.Add(new  MeshData(
      dist, 
      hand, 
      ext, 
      threeVertices, 
      threeFaceInfo, 
      entColor));
             }
             else  if (id.ObjectClass.Name.Equals("AcDb3dSolid" ))
             {
                 // Mesh the solid to export to Three.js 
                 Autodesk.AutoCAD.DatabaseServices.Solid3d sld 
      = tr.GetObject(
      id, OpenMode.ForRead) 
      as Autodesk.AutoCAD.DatabaseServices.Solid3d;
                   MeshFaceterData mfd = new  MeshFaceterData();
                 // Only triangles 
                 mfd.FaceterMeshType = 2; 
                   // May need change based on  
     // how granular we want the mesh to be. 
                 mfd.FaceterMaxEdgeLength = dir.Length * 0.025;
                   MeshDataCollection md 
      = SubDMesh.GetObjectMesh(sld, mfd);
                   Point3dCollection threeVertices 
      = new  Point3dCollection();
                   nt32Collection threeFaceInfo 
      = new  Int32Collection();
                   Point3dCollection vertices = md.VertexArray;
                   int [] faceArr = md.FaceArray.ToArray();
                   Int32Collection faceVertices 
      = new  Int32Collection();
                   int  verticesInFace = 0;
                 int  facecnt = 0;
                 for  (int  x = 0; 
      x < faceArr.Length; facecnt++, 
      x = x + verticesInFace + 1)
                 {
                     faceVertices.Clear();
                       verticesInFace = faceArr[x];
                     for  (int  y = x + 1; 
       y <= x + verticesInFace; 
       y++)
                     {
                         faceVertices.Add(faceArr[y]);
                     }
                       if  (faceVertices.Count == 3)
                     {
                         Point3d p1 
        = vertices[faceVertices[0]];
                         Point3d p2 
        = vertices[faceVertices[1]];
                         Point3d p3 
        = vertices[faceVertices[2]];
                           if  (!threeVertices.Contains(p1))
                             threeVertices.Add(p1);
                         threeFaceInfo.Add(
        threeVertices.IndexOf(p1));
                           if  (!threeVertices.Contains(p2))
                             threeVertices.Add(p2);
                         threeFaceInfo.Add(
        threeVertices.IndexOf(p2));
                           if  (!threeVertices.Contains(p3))
                             threeVertices.Add(p3);
                         threeFaceInfo.Add(
        threeVertices.IndexOf(p3));
                     }
                 }
                   sols.Add(new  MeshData(
      dist, 
      hand, 
      ext, 
      threeVertices, 
      threeFaceInfo, 
      entColor));
                   tr.Commit();
             }
         }
     }
     return  sols;
 }
    // Helper function to build a JSON string containing a 
 // sorted extents list 
    internal  static  string SolidsString(
     List<MeshData> lst)
 {
     var sb = new  StringBuilder(
   "{\\"retCode\\":0, \\"result\\":[" );
        var first = true ;
     foreach (var data in lst)
     {
     if  (!first)
         sb.Append("," );
        first = false ;
     var hand = data._handle;
     var ext = data._exts;
     var vertices = data._vertices;
     var faces = data._faces;
     var color = data._color;
       sb.AppendFormat(
           "{{\\"min\\":{0},\\"max\\":{1}, 
   \\"handle\\":\\"{2}\\",\\"vertices\\":{3}, 
   \\"faces\\":{4},\\"color\\":\\"{5}\\"}}" ,
           JsonConvert.SerializeObject(ext.MinPoint),
         JsonConvert.SerializeObject(ext.MaxPoint),
         hand,
         JsonConvert.SerializeObject(vertices),
         JsonConvert.SerializeObject(faces),
         color
     );
     }
     sb.Append("]}" );
        return  sb.ToString();
 }
  Changes to threesolids2.js
 function addSolidsToPalette(args) {
     var obj = JSON.parse(args);
   var sols = obj.result;
     var needRender = false ;
   if  (sols != null) {
     for  (var sol in sols) {
       var s = sols[sol];
       var obj = root.getObjectByName(s.handle, true );
       if  (obj == null) {
         var verticesarray = s.vertices;
         var facesarray = s.faces;
         if  (verticesarray.length != 0) {
             createMesh(s);
         }
         root.add(box);
         needRender = true ;
       }
     }
   }
   if  (needRender) {
     render();
   }
 }
   function refresh() {
     // Clear any previous geometry 
     if  (root != null) {
     scene.remove(root);
     delete  root;
       // Get the geometry info from AutoCAD again 
       sols = getThreeSolidsFromAutoCAD();
   }
     // Create the materials 
     var dark = 
    new  MeshLambertMaterial({ color: 0x000000 });
   light 
    = new  MeshLambertMaterial({ color: 0xFFFFFF });
     // Create our root object 
     boxGeom =
     new  BoxGeometry(rootDim, rootDim, 
  rootDim, segs, segs, segs);
     // Create the mesh from the geometry 
     root = new  Mesh(boxGeom, dark);
     scene.add(root);
     for  (var sol in sols) {
     var s = sols[sol];
     var verticesarray = s.vertices;
     var facesarray = s.faces;
     if  (verticesarray.length != 0) {
         var mesh = createMesh(s);
   root.add(mesh);
     }
   }
     // Draw! 
     renderer.render(scene, camera);
 };
   function createMesh(s) {
       var verticesarray = s.vertices;
     var vertices = [];
     if  (verticesarray != null) {
         var numOfVertices = verticesarray.length;
         for  (var v = 0; v < numOfVertices; v++) {
             var vertex = verticesarray[v];
             vertices.push(
     new  THREE.Vector3(
     vertex.X, vertex.Y, vertex.Z));
         }
     }
       var facesarray = s.faces;
     var faces = [];
     if  (facesarray != null) {
         var numOfFaces = facesarray.length / 3;
         for  (var f = 0; f < numOfFaces; f = f + 1) {
             faces.push(
     new  THREE.Face3(
     facesarray[f * 3], 
     facesarray[f * 3 + 1], 
     facesarray[f * 3 + 2]));
         }
     }
     var geom = new  THREE.Geometry();
     geom.vertices = vertices;
     geom.faces = faces;
     geom.mergeVertices();
     geom.computeFaceNormals();
     geom.computeVertexNormals();
       var material = 
   new  THREE.MeshLambertMaterial(
  { color: 0x00FF00, shading: THREE.FlatShading });
     material.color.setHex(parseInt(s.color, 16));
       var threemesh = new  THREE.Mesh(geom, material);
     threemesh.name = s.handle;
     return  threemesh;
 }
  Here is a screenshot of the AutoCAD solids imported into Three.js :
The modified files can be downloaded here :
Download Utils.cs
Download Threesolids2.js

## 评论

**内容**: Matthias said...
Hi Balaji,
This works great. But for me FaceterMeshType = 0 instead of 2 and manually splitting the rectangluar faces into triangles like with the AcDbSubDMesh gives much better results. And it's faster, too.
Have you tried to add texture to the objects? Seems to be tricky.
Reply
03/23/2016 at 01:43 AM

---
**内容**: Matthias said in reply to Matthias...
I've found something interesting. For the moment I use this code:
http://stackoverflow.com/questions/20774648/three-js-generate-uv-coordinate
It's not perfect - works just fine with flat objects. But it at least allows me to display a texture. Would be better if it's possible to directly get the UV data from the AutoCAD model.
Reply
03/23/2016 at 11:39 AM

---
**内容**: yuzhonghuang said...
Hi Balaji,
I want to ask you some problem about how autocad converse to three.js ?
Reply
04/06/2016 at 11:15 PM

---
