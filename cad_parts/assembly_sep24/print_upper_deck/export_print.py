"""Export the three upper-deck parts in a fixed PETG print layout."""
from pathlib import Path
import json,hashlib,zipfile,xml.etree.ElementTree as ET
import FreeCAD as App
import MeshPart
import Part
import Mesh
r=Path(__file__).resolve().parent
tmp_dir=r.parent/'tmp'
tmp_dir.mkdir(parents=True, exist_ok=True)
ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02'
ET.register_namespace('',ns)
def node(parent,name,attrs={}):return ET.SubElement(parent,'{'+ns+'}'+name,attrs)
model=ET.Element('{'+ns+'}model',{'unit':'millimeter','{http://www.w3.org/XML/1998/namespace}lang':'en-US'})
resources=node(model,'resources');build=node(model,'build')
sources={f:App.openDocument(str(r.parent/f)) for f in ['main_upper_deck.FCStd']}
hashes={f:hashlib.sha256((r.parent/f).read_bytes()).hexdigest() for f in sources}
report={'source_sha256':hashes,'parts':[],'orientation':'Upper deck underside flat on bed, mounts and ramps upward. Board retaining clamp and ammeter support printed flat beside it. Supports may start on the bed or deck surfaces.','bed_mm':[270,270]}
layout=[('TeensyPlatform','main_upper_deck.FCStd',0,65,75),('BoardRetainingClamp','main_upper_deck.FCStd',0,65,55),('AmmeterSupportC','main_upper_deck.FCStd',0,130,55)]
for i,(name,filename,angle,x,y) in enumerate(layout,1):
 source=r.parent/filename;doc=sources[filename]
 shape=doc.getObject(name).Shape.copy()
 assert shape.isValid() and len(shape.Solids)==1
 shape.rotate(App.Vector(),App.Vector(1,0,0),angle)
 bb=shape.BoundBox;shape.translate(App.Vector(-bb.XMin,-bb.YMin,-bb.ZMin))
 shape=shape.removeSplitter()
 fresh=Part.Shape();fresh.importBrepFromString(shape.exportBrepToString());shape=fresh
 mesh=MeshPart.meshFromShape(Shape=shape,LinearDeflection=.01,AngularDeflection=.06,Relative=False)
 print('Mesh before cleanup:',mesh.CountPoints,mesh.CountFacets,mesh.isSolid(),flush=True)
 mesh.removeDuplicatedPoints();mesh.removeDuplicatedFacets();mesh.fixDegenerations();mesh.harmonizeNormals()
 if not mesh.isSolid():
  for tol,ang in [(.02,.1),(.005,.04),(.03,.15)]:
   fresh=Part.Shape();fresh.importBrepFromString(shape.exportBrepToString())
   trial=MeshPart.meshFromShape(Shape=fresh,LinearDeflection=tol,AngularDeflection=ang,Relative=False)
   trial.removeDuplicatedPoints();trial.removeDuplicatedFacets();trial.fixDegenerations();trial.harmonizeNormals()
   print('Alternate tessellation',name,tol,ang,trial.isSolid(),flush=True)
   if trial.isSolid():mesh=trial;break
 if not mesh.isSolid():
  original_facets={tuple(sorted(tuple(round(v,8) for v in point) for point in facet.Points)) for facet in mesh.Facets}
  # Tessellation can leave microscopic loops at multi-face bevel joins.
  from collections import Counter
  pts,facets=mesh.Topology
  edges=Counter(tuple(sorted((f[j],f[(j+1)%3]))) for f in facets for j in range(3))
  boundary=[e for e,c in edges.items() if c==1]
  assert all(c<=2 for c in edges.values())
  print('Boundary diagnostics',name,len(boundary),sorted((round((pts[a]-pts[b]).Length,8) for a,b in boundary)),flush=True)
  assert len(boundary)<=20 and all((pts[a]-pts[b]).Length<0.75 for a,b in boundary)
  # Split mismatched triangulations along collinear boundary vertices.
  for attempt in range(3):
   edges=Counter(tuple(sorted((f[j],f[(j+1)%3]))) for f in facets for j in range(3))
   boundary={e for e,c in edges.items() if c==1}
   candidates=set(v for e in boundary for v in e);split=[];changed=False
   for face in facets:
    for j in range(3):
     a,b,c=face[j],face[(j+1)%3],face[(j+2)%3]
     if tuple(sorted((a,b))) not in boundary:continue
     ab=pts[b]-pts[a];length2=ab.dot(ab)
     if length2<1e-12:continue
     interior=[]
     for v in candidates-{a,b,c}:
      t=(pts[v]-pts[a]).dot(ab)/length2
      if 1e-5<t<1-1e-5 and (pts[v]-pts[a]-ab*t).Length<1e-5:interior.append((t,v))
     if interior:
      chain=[a]+[v for _,v in sorted(interior)]+[b]
      split.extend((u,v,c) for u,v in zip(chain,chain[1:]));changed=True;break
    else:split.append(face)
   facets=split
   if not changed:break
  mesh=Mesh.Mesh([(pts[a],pts[b],pts[c]) for a,b,c in facets])
  mesh.removeDuplicatedPoints();mesh.removeDuplicatedFacets();mesh.fixDegenerations()
  mesh.fillupHoles(20);mesh.harmonizeNormals()
  if not mesh.isSolid():
   pts,facets=mesh.Topology
   edges=Counter(tuple(sorted((f[j],f[(j+1)%3]))) for f in facets for j in range(3))
   boundary=[(f[j],f[(j+1)%3]) for f in facets for j in range(3) if edges[tuple(sorted((f[j],f[(j+1)%3])))]==1]
   print('Remaining boundary:',[(tuple(pts[a]),tuple(pts[b])) for a,b in boundary],flush=True)
   todo=dict(boundary);patches=[]
   assert len(todo)==len(boundary)
   while todo:
    first=next(iter(todo));cycle=[first];current=todo.pop(first)
    while current!=first:
     cycle.append(current);current=todo.pop(current)
    assert 3<=len(cycle)<=8
    assert max((pts[a]-pts[b]).Length for a in cycle for b in cycle)<0.5
    center=App.Vector(0,0,0)
    for a in cycle:center+=pts[a]
    center/=len(cycle)
    for a,b in zip(cycle,cycle[1:]+cycle[:1]):patches.append((pts[b],pts[a],center))
   mesh=Mesh.Mesh([(pts[a],pts[b],pts[c]) for a,b,c in facets]+patches)
   mesh.harmonizeNormals()
 if 'original_facets' in locals():
  repairs=[f for f in mesh.Facets if tuple(sorted(tuple(round(v,8) for v in point) for point in f.Points)) not in original_facets]
  assert len(repairs)<=100
  assert sum(f.Area for f in repairs)<.1
  for f in repairs:assert Part.Vertex(sum((App.Vector(*point) for point in f.Points),App.Vector())/3).distToShape(shape)[0]<.03
  print('Verified seam repair area',sum(f.Area for f in repairs),flush=True)
  del original_facets
 print('Mesh after cleanup:',mesh.CountPoints,mesh.CountFacets,mesh.isSolid(),flush=True)
 assert mesh.isSolid(),name
 assert abs(abs(mesh.Volume)-shape.Volume)/shape.Volume<0.001
 mb=mesh.BoundBox;mesh.translate(-mb.XMin,-mb.YMin,-mb.ZMin)
 target=tmp_dir/(name+'.stl');mesh.write(str(target))
 points,triangles=mesh.Topology
 obj=node(resources,'object',{'id':str(i),'type':'model','name':name});m=node(obj,'mesh');vertices=node(m,'vertices');faces=node(m,'triangles')
 for p in points:node(vertices,'vertex',{'x':str(p.x),'y':str(p.y),'z':str(p.z)})
 for tri in triangles:node(faces,'triangle',dict(zip(('v1','v2','v3'),map(str,tri))))
 node(build,'item',{'objectid':str(i),'transform':f'1 0 0 0 1 0 0 0 1 {x} {y} 0'})
 report['parts'].append({'id':name,'source_file':'../'+filename,'rotation_x_deg':angle,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'stl_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'position_mm':[x,y,0],'bounds_mm':[mesh.BoundBox.XLength,mesh.BoundBox.YLength,mesh.BoundBox.ZLength],'triangles':len(triangles),'valid_closed_mesh':True})
with zipfile.ZipFile(tmp_dir/'upper_deck_layout.3mf','w',zipfile.ZIP_DEFLATED) as z:
 z.writestr('[Content_Types].xml','<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
 z.writestr('_rels/.rels','<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
 z.writestr('3D/3dmodel.model',ET.tostring(model,encoding='utf-8',xml_declaration=True))
(tmp_dir/'export_validation.json').write_text(json.dumps(report,indent=2)+'\n')
print('SUCCESS: three closed meshes in fixed layout; current CAD only, no printer action.')
