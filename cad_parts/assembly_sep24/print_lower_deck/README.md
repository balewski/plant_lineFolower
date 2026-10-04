# Lower deck print preparation — September 24

Status: prepared; awaiting approval of the exact layout and confirmation of PETG loaded / clear plate. No upload or print start performed.

Five parts: FinishedChassis, LeftMotorClamp and CableClamp1–3. RightMotorClamp omitted for reuse; current clamp geometries verified interchangeable.

PETG, 0.4 mm nozzle, 0.20 mm layers, four walls, 35% infill. No brim and no skirt. Build-plate-only snug supports retained. Estimated 5 h 02 min and 50.4 g.

Deck top face down, underside motor mounts up. Motor clamp flat with screw-head recesses down; cable clamps flat backs down and end pads up. This keeps the deck and sensor arms in the bed plane; vertical switch/socket panels rely on layer bonding at their reinforced roots.

Exact sliced layout: print_layout_top.png. Bed contact: first_layer_top.png. Validation: toolpath_checks.json and export_validation.json. Source CAD hash verified unchanged, five closed meshes, all objects sliced within bed bounds, no brim/skirt extrusion paths, no negative-Z moves, corrected startup wipes and gentle cutter configuration checked.

Profiles and scripts here are independent local copies. Regenerate with absolute QIDIStudio --outputdir to this directory, then run check_print.py and render_toolpaths.swift. Native assembly CAD is the manufacturing source, not the visualization overview.
