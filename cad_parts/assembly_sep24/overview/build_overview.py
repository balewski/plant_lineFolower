"""Self-contained visualization snapshots; never modifies manufacturing designs."""
from pathlib import Path
import json,math,hashlib
import FreeCAD as App
import Part
R=Path(__file__).resolve().parent.parent; O=R/'overview'; V=App.Vector
files=['main_lower_deck.FCStd','main_pillars.FCStd','main_upper_deck.FCStd','main_photo_sensor.FCStd']
hashes={n:hashlib.sha256((R/n).read_bytes()).hexdigest() for n in files}
lower,pillars,upper,sensor=[App.openDocument(str(R/n)) for n in files]
pi_origin=V(lower.PiOutlineOuter.Shape.BoundBox.Center.x-47,-46.5,4)
doc=App.newDocument('RobotOverview');doc.Label='Robot — assembled and exploded — visualization only'
assembled=doc.addObject('App::DocumentObjectGroup','AssembledRobot');assembled.Label='1 — Fully assembled robot'
exploded=doc.addObject('App::DocumentObjectGroup','ExplodedRobot');exploded.Label='2 — Exploded robot (offset right)'
info=doc.addObject('App::FeaturePython','OverviewInformation')
for key,value in {'Purpose':'Visualization only; embedded snapshots, no links to source CADs','Axes':'X right; Y front; Z up. Ground Z=-20 mm','PiOrientation':f'94 X × 63 Y × 30 Z mm; lower corner ({pi_origin.x:g},-46.5,4)','BatteryOrientation':'76 X × 22 Y × 41 Z mm; lower corner (-38,-82.75,4.3)','Mocks':'Socket, plug, toggles and PCB component heights are illustrative, not measured hardware','Animation':'Run overview/animate_toggles.FCMacro to move both switch levers','ViewingInstructions':'Space toggles AssembledRobot or ExplodedRobot; both visible by default'}.items():
 info.addProperty('App::PropertyString',key,'Read me');setattr(info,key,value)
colors={'lower':(.25,.57,.67),'upper':(.90,.58,.25),'pillar':(.82,.65,.33),'board':(.20,.57,.35),'black':(.15,.17,.20),'metal':(.70,.73,.76),'battery':(.20,.36,.75),'pi':(.63,.66,.70)}
records=[];objects={};switches=[]
def add(name,shape,kind,shift=(0,0,0),source='',mock=False,check=True,color=None):
 obj=doc.addObject('Part::Feature',name);assembled.addObject(obj);obj.Shape=shape.copy();obj.Label=name.replace('_',' ')
 obj.addProperty('App::PropertyBool','VisualizationOnly');obj.VisualizationOnly=True
 obj.addProperty('App::PropertyString','Source');obj.Source=source or 'Illustrative mockup'
 obj.addProperty('App::PropertyBool','ApproximateHardware');obj.ApproximateHardware=mock
 obj.addProperty('App::PropertyVector','ExplosionOffset');obj.ExplosionOffset=V(*shift)
 obj.addProperty('App::PropertyColor','DisplayColor');obj.DisplayColor=color or colors[kind]
 if obj.ViewObject:obj.ViewObject.ShapeColor=obj.DisplayColor
 objects[name]=obj;records.append(dict(name=name,kind=kind,check=check,mock=mock,source=source,shift=list(shift)))
 return obj
for item in lower.PrintedParts.Group:
 shift=(0,0,0) if item.Name=='ChassisWithLeftMotorA' else (0,0,-25) if 'MotorClamp' in item.Name else (0,0,-12)
 add(item.Name,item.Shape,'lower',shift,'main_lower_deck.FCStd#'+item.Name)
for item in lower.HardwareReferences.Group:
 name=item.Name
 side=-1 if name.startswith('Left') else 1
 shift=(side*30,0,-15) if 'Wheel' in name or 'Shaft' in name else (side*15,0,-15) if 'Motor' in name else (0,0,-38)
 add(name,item.Shape,'black' if 'Wheel' in name else 'metal',shift,'main_lower_deck.FCStd#'+name,check='ScrewReference' not in name)
add('PhotoSensorHolder',lower.MountedSensorHolder.Shape,'board',(0,45,-8),'main_lower_deck.FCStd#MountedSensorHolder')
for item in sensor.HardwareReferences.Group:
 sh=item.Shape.copy();sh.translate(V(-30,57,-20))
 add(item.Name,sh,'board' if item.Name.startswith('PCB') else 'black',(0,45,-8),'main_photo_sensor.FCStd#'+item.Name)
for item in pillars.PrintedParts.Group:add(item.Name,item.Shape,'pillar',(0,0,45),'main_pillars.FCStd#'+item.Name)
for item in upper.PrintedParts.Group:
 add(item.Name,item.Shape,'upper' if item.Name=='TeensyPlatform' else 'board',(0,0,105 if item.Name=='TeensyPlatform' else 125),'main_upper_deck.FCStd#'+item.Name)
add('TeensyPCB',upper.TeensyPCBReference.Shape,'board',(0,0,118),'main_upper_deck.FCStd#TeensyPCBReference')
# Exact requested outer envelopes for fit testing; simple colored solids in the overview.
pi=add('PiEnclosure',Part.makeBox(94,63,30,pi_origin),'pi',(0,0,40),source='User envelope: 30 × 63 × 94 mm')
battery=add('BatteryPack',Part.makeBox(76,22,41,V(-38,-82.75,4.3)),'battery',(0,-35,40),source='User envelope: 76 × 41 × 22 mm')
for name,w,h,z in [('PowerA',22,44,60),('PowerB',44,22,60)]:
 b=upper.getObject(name+'OutlineOuter').Shape.BoundBox
 pcb=Part.makeBox(w,h,1.6,V(b.XMin,b.YMin,z))
 for item in upper.Objects:
  if item.Name.startswith(name) and item.Name.endswith('MountPad'):
   c=item.Shape.CenterOfMass;pcb=pcb.cut(Part.makeCylinder(1,3,V(c.x,c.y,z-.5)))
 components=Part.makeBox(w-6,h-12,7,V(b.XMin+3,b.YMin+6,z+1.6))
 add(name+'PCB',pcb,'board',(0,0,125),'Current upper-deck footprint; assumed PCB thickness 1.6 mm',True)
 add(name+'Components',components,'black',(0,0,125),'Illustrative component envelope 7 mm above PCB',True)
# Preserve the existing driver seating reference rather than silently shifting its mounting pattern.
normal=V(-.5,0,math.sqrt(3)/2)
board=upper.MotorDriveSeatingPlane.Shape.extrude(normal*1.6)
original_driver_overlap=board.common(upper.TeensyPlatform.Shape).Volume
tangent=V(math.sqrt(3)/2,0,.5)
stop_face=next(f for f in upper.MotorDriveStopWall1.Shape.Faces if abs(abs(f.normalAt(0,0).dot(tangent))-1)<1e-7)
seat_shift=tangent.dot(stop_face.CenterOfMass)-min(tangent.dot(v.Point) for v in board.Vertexes)
board.translate(tangent*seat_shift)
add('MotorDriverPCB',board,'board',(0,0,130),'Existing driver-board outline, 1.6 mm thick, slid uphill to contact the stops; hole pattern unverified',True)
w=upper.AmmeterDisplayOpening.Shape.BoundBox
body=Part.makeBox(w.XLength-.2,w.YLength-.2,5,V(w.XMin+.1,w.YMin+.1,52))
bezel=Part.makeBox(w.XLength+2,w.YLength+2,1,V(w.XMin-1,w.YMin-1,57))
add('AmmeterDisplay',body.fuse(bezel),'black',(0,0,120),'Display opening with approximate body and bezel',True)
# Panel hardware uses the saved hole axes and outer-face centers.
def world(shape,placement):
 out=shape.copy();out.Placement=placement.multiply(out.Placement);return out
for i in (1,2):
 hole=lower.getObject('SwitchHole'+str(i));n=hole.Placement.Rotation.multVec(V(0,0,1));c=hole.Placement.Base+n
 mount=App.Placement(c,hole.Placement.Rotation)
 shank=Part.makeCylinder(3,5,V(0,0,-1));body=Part.makeBox(10,8,9,V(-5,-4,3.5))
 nut=Part.makeCylinder(4.5,1.5,V(0,0,-1.5)).cut(Part.makeCylinder(3,1.5,V(0,0,-1.5)))
 add('Toggle%dBody'%i,world(body,mount),'black',(0,-30,0),'Approximate 10 × 8 × 9 mm switch body',True)
 add('Toggle%dMount'%i,world(shank.fuse(nut),mount),'metal',(0,-30,0),'Approximate Ø6 threaded stem',True)
 lever=Part.makeCylinder(1.3,12,V(0,0,0),V(0,0,-1)).fuse(Part.makeSphere(2,V(0,0,-12)))
 pivot=App.Placement(c-n*3.5,hole.Placement.Rotation)
 obj=add('Toggle%dLever'%i,lever,'metal',(0,-30,0),'Illustrative moving lever, ±25 degrees',True)
 obj.addProperty('App::PropertyPlacement','MountPlacement');obj.MountPlacement=pivot
 obj.addProperty('App::PropertyAngle','LeverAngle');obj.LeverAngle=25 if i==1 else -25
 obj.Placement=pivot.multiply(App.Placement(V(),App.Rotation(V(1,0,0),obj.LeverAngle.Value)))
 switches.append(obj)
hole=lower.SocketHole;n=hole.Placement.Rotation.multVec(V(0,0,1));c=hole.Placement.Base+n;mount=App.Placement(c,hole.Placement.Rotation)
socket=Part.makeCylinder(4,5,V(0,0,-1)).fuse(Part.makeCylinder(5.5,1,V(0,0,-1)))
socket=socket.fuse(Part.makeCylinder(5,7,V(0,0,4))).cut(Part.makeCylinder(2.8,14,V(0,0,-2)))
add('PowerSocket',world(socket,mount),'black',(0,-30,0),'Approximate barrel socket matching Ø8.4 panel bore',True)
plug=Part.makeCylinder(2.7,9,V(0,0,-7)).fuse(Part.makeCylinder(4.8,19,V(0,0,-26)))
add('PowerPlug',world(plug,mount),'black',(0,-53,0),'Approximate inserted barrel plug',True)
# Decorative lid and battery lettering are deliberately not used for fit calculations.
font=str(R/'assets/DejaVuSans.ttf')
for label,obj,z in [('Pi',pi,34.05),('76 × 41 × 22',battery,45.35)]:
 text=Part.makeCompound([Part.makeFace(w,'Part::FaceMakerBullseye') for w in Part.makeWireString(label,font,3,0) if w])
 b=text.BoundBox;t=obj.Shape.BoundBox;text.translate(V((t.XMin+t.XMax-b.XMin-b.XMax)/2,(t.YMin+t.YMax-b.YMin-b.YMax)/2,z))
 add(obj.Name+'Label',text.extrude(V(0,0,.15)),'black',tuple(obj.ExplosionOffset),'Decorative label',check=False)
doc.recompute()
# Collision checks use assembled shapes only, including every actual printed component.
def overlap(a,b):
 x=a.BoundBox;y=b.BoundBox
 return min(x.XMax,y.XMax)-max(x.XMin,y.XMin)>1e-6 and min(x.YMax,y.YMax)-max(x.YMin,y.YMin)>1e-6 and min(x.ZMax,y.ZMax)-max(x.ZMin,y.ZMin)>1e-6
collisions=[];tested=0
for i,r in enumerate(records):
 if not r['check']:continue
 a=objects[r['name']].Shape
 for q in records[:i]:
  if not q['check']:continue
  names={r['name'],q['name']}
  if names=={'PowerPlug','PowerSocket'} or any(names=={'Toggle%dBody'%j,'Toggle%dMount'%j} for j in (1,2)):continue # intentional mating/integrated hardware
  b=objects[q['name']].Shape
  if not overlap(a,b):continue
  tested+=1;common=a.common(b);volume=common.Volume
  if volume>1e-4:
   collisions.append(dict(parts=sorted(names),overlap_mm3=volume,approximate_hardware_involved=r['mock'] or q['mock']))
# Clearance and support checks for the user-sized envelopes.
clearances={}
for obj in [pi,battery]:
 clearances[obj.Name]={}
 for name in ['TeensyPlatform','AmmeterSupportC','FrontPillarFrame','AftPillarFrame']:
  clearances[obj.Name][name]=obj.Shape.distToShape(objects[name].Shape)[0]
foot=Part.makeBox(76,22,.1,V(-38,-82.75,3))
footprint_outside=foot.cut(lower.RearTransitionFillets.Shape).Volume/.1
# Two independent groups: duplicated snapshots, not external links.
for record in records:
 src=objects[record['name']];offset=V(345,0,0)+src.ExplosionOffset
 obj=doc.addObject('Part::Feature','Exploded_'+src.Name);exploded.addObject(obj);obj.Label=src.Label
 obj.Shape=src.Shape.copy();obj.Placement.Base=obj.Placement.Base+offset
 obj.addProperty('App::PropertyColor','DisplayColor');obj.DisplayColor=src.DisplayColor
 obj.addProperty('App::PropertyBool','VisualizationOnly');obj.VisualizationOnly=True
 if src in switches:
  obj.Shape=src.Shape.copy();obj.addProperty('App::PropertyPlacement','MountPlacement');p=src.MountPlacement;p.Base=p.Base+offset;obj.MountPlacement=p
  obj.addProperty('App::PropertyAngle','LeverAngle');obj.LeverAngle=src.LeverAngle
  # Shape.copy includes the source placement; reset before applying the exploded pivot.
  local=Part.makeCylinder(1.3,12,V(),V(0,0,-1)).fuse(Part.makeSphere(2,V(0,0,-12)))
  obj.Shape=local;obj.Placement=p.multiply(App.Placement(V(),App.Rotation(V(1,0,0),obj.LeverAngle.Value)))
for obj in list(assembled.Group)+list(exploded.Group):
 assert obj.Shape.isValid(),obj.Name
 if obj.ViewObject:
  obj.ViewObject.ShapeColor=obj.DisplayColor;obj.ViewObject.LineColor=(.12,.14,.16);obj.ViewObject.DisplayMode='Flat Lines';obj.ViewObject.Visibility=True
if assembled.ViewObject:assembled.ViewObject.Visibility=True
if exploded.ViewObject:exploded.ViewObject.Visibility=True
report=dict(driver_board={'original_reference_overlap_with_stops_mm3':original_driver_overlap,'shift_up_slope_to_seat_mm':seat_shift,'right_edge_overhang_mm':max(0,board.BoundBox.XMax-upper.UpperFloorBlank.Shape.BoundBox.XMax),'mounting_hole_pattern_verified':False},purpose='Visualization only',source_sha256=hashes,source_designs_modified=False,
 component_count_per_view=len(records),collision_pairs=collisions,boolean_pairs_checked=tested,clearances_mm=clearances,
 battery_footprint_outside_deck_perimeter_mm2=footprint_outside,
 placements={'PiEnclosure':{'size_xyz_mm':[94,63,30],'lower_corner_xyz_mm':[pi_origin.x,pi_origin.y,pi_origin.z]},'BatteryPack':{'size_xyz_mm':[76,22,41],'lower_corner_xyz_mm':[-38,-82.75,4.3]}},
 mock_dimensions_unverified=True,physical_fit_tested=False,manufacturing_exported=False)
tmp_dir = R / 'tmp'
tmp_dir.mkdir(parents=True, exist_ok=True)
(tmp_dir/'fit_report.json').write_text(json.dumps(report,indent=2)+'\n')
doc.recompute();doc.saveAs(str(R/'main_overview.FCStd'))
for path,sha in hashes.items():assert hashlib.sha256((R/path).read_bytes()).hexdigest()==sha
print(json.dumps(report,indent=2),flush=True)
