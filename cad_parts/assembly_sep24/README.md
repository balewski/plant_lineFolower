# September 24 robot assembly

Open [main_lower_deck.FCStd](main_lower_deck.FCStd) for the chassis, two motor clamps, three cable clamps and the installed photo-sensor holder. [main_pillars.FCStd](main_pillars.FCStd) shows both pillar frames on the current deck. [main_photo_sensor.FCStd](main_photo_sensor.FCStd) is the current standalone sensor holder. All design inputs are local to this package. The September 15 originals remain preserved.

## Current deck

The deck is 110 × 115 × 4 mm, with an 86 mm rear edge, 75 mm straight section and 40 mm taper. Its front is Y=32, rear Y=-83 and underside Z=0. Both straight motor clamps use screw axes X=±40. The motor/gearbox reference length is 24 mm plus an 11 mm shaft. Retaining walls are 24.5 mm inward from each side, 2 mm thick and 5 mm below the deck, with Ø5 bottom-open shaft notches. Modeled motor-to-stop clearance is 0.5 mm.

Pi mounting holes are Ø2 at (-31.3,-15) and (23.7,-15), preserving 55 mm pitch after moving both holes 4 mm rearward. The Pi outline moves rearward by the same 4 mm, keeping its alignment with the mounting holes. Pi and battery text is removed; shallow outlines remain and may be crossed by utility openings. The battery outline is 77 × 16 mm at Y=-76..-60. Caster axis Y=-69; the rear strap slot remains. The front and rear edges have 4 × 1.5 mm center triangles, engraved 0.25 mm deep with 0.5 mm edge clearance. The front triangle points forward (+Y), with its tip at Y=31.5.

Rounded brick openings have nominal 10 × 20 mm dimensions, R2.5 corners, 4 mm spacing through the core, and their long dimension along Y. Every opening has a 0.5 mm, 45° chamfer at both plate faces, leaving at least 3 mm between the enlarged mouths. The nominal 10 mm core width opens to 11 mm at the surfaces. Three central lanes are centered at X=-14,0,14, with additional outer lanes wherever structure permits. Adjacent lanes are staggered by 12 mm. Bricks shorten along Y to keep their chamfers clear of mounts; remnants below half the nominal rounded-brick area are omitted. The complete motor footprints plus a 3 mm margin remain solid. Mounting pads, caster support and the outside structural band are preserved. Actual opening count and volume reduction are in validation.json.

The switch wall is 25 mm wide and the socket wall 20 mm wide; both lean outward 20°. Their upper edges now meet the plate top at Z=4. The walls extend to this upper edge while retaining the previous bottom and bore heights. S1 above the inner switch, S2 above the outer switch, and 7V+ above the socket use 5 mm glyph height and 0.35 mm engraving depth, with 1 mm space above each label after moving them 0.5 mm down along the panel face.

Three separate cable clamps sit along the outer side edges, clear of the pillar braces: centers (-51,2), (51,2), and (-51,-29) mm. Their outer edges are 1 mm inside the straight frame edge. Each has a 6 mm wide × 20 mm long × 1.5 mm thick bar, two Ø6 mm round feet projecting 1.5 mm underneath, and two Ø2 mm through-holes. The deck beneath them is undrilled. The builder measures pad support and checks all modeled interferences. These are loose parts in the assembly, without modeled fastening hardware.

## Sensor mount and pillars

Two deck arms are 10 mm wide and 4 mm thick, with 24 mm forward projection, R2 tips and R4 root transitions. The sensor bar's rear face is 25 mm horizontally in front of the deck. Its arm tops touch the underside at Z=0; the arm overlap is 19 mm. Four Ø2 holes are at X=±30, Y=42 and 52. The embedded holder matches the local standalone native geometry. Its lower walls are now 4 mm shorter with straight 1.5 mm dividers, while the original PCB-gripping guides and sensor pilot positions are preserved. A centered triangle projects 4 mm forward. See photo_sensor/README.md.

Front pillar centers are X=±45, Y=27; rear centers are X=±42, Y=-55 after moving each rear pillar 3 mm inward. Deck holes and footprint markings match. The rear mounting pitch is 84 mm; front pitch remains 90 mm. Both frames stand directly on the deck and are 45 mm high, with tops at Z=49. End holes are centered Ø2, 8.2 mm deep. The historical head-joint files are retained but not used in the current assembly.

## Rebuilding and checking

Use the installed FreeCAD Python interpreter with its library path:

```sh
PYTHONPATH=/Applications/FreeCAD.app/Contents/Resources/lib \
/Applications/FreeCAD.app/Contents/Resources/bin/python build_wheels.py
```

Then build pillars/front/build_upper_level.py and pillars/aft/build_aft_pillars.py with the same interpreter, followed by pillars/build_pillars.py. Run render_wheels.FCMacro and pillars/render_pillars.FCMacro in FreeCAD to refresh the actual CAD previews. The frame builders embed the current deck and need rebuilding after deck changes. Archive native files and inputs before editing, especially after manual CAD changes.

validation.json records build checks; verify_sensor_revision.py checks this revision against its archive and writes sensor_revision_validation.json. pillars/validation.json and the frame reports check pillar alignment and interference. verify_independent.py can additionally rebuild from an isolated copy of the local inputs. All native links must remain local. Geometry checks do not establish physical stiffness or fit.

The preceding design is archived under revisions/before_sensor_mount_holes_inward/. Earlier revision reports remain in their respective archives. copy_manifest.json records original provenance; package_manifest.json records current hashes.

Design builds produce native CAD and previews only. Leave WHEELS_EXPORT_MANUFACTURING unset. No manufacturing export or printer action is part of this revision.

## Visualization overview

[main_overview.FCStd](main_overview.FCStd) contains assembled and exploded views with the Pi enclosure, battery and hardware mockups. See [overview/README.md](overview/README.md) for placements, clearances and switch animation. Manufacturing source parts remain unchanged.

Latest deck update: rear upper-deck marker is an engraved triangle outline; three cable clamps are on the lower-deck underside, two along side edges and one along the front. See bottom_view.png and upper_deck/rear_marker_detail.png. The running print_lower_deck job remains frozen with its original files; clamp geometry is unchanged and those clamps can be installed in the new locations.

All active recessed markings now use0.20mm depth, including deck outlines/center markers/panel labels and sensor lettering. Raised pillar letters remain unchanged. See engraving_depth_validation.json. The current printer job retains its approved G-code.

Latest lower deck:25mm motor pockets;2×2mm top front lip between pillars;U2/U16/U17 filled;center triangles0.5mm deep;Pi outline and mounting holes shifted2mm right. See top_view.png and motor_lip_validation.json.
