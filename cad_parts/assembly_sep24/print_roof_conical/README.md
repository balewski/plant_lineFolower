# Updated roof print

One current MainRoof exported directly from ../main_roof.FCStd. Includes all four conical transitions, 50 mm columns, 0.4 mm deck clearance, and the 25 mm Power A brim. Source CAD unchanged. Native Boolean check, closed mesh, and mesh/CAD volume agreement passed.

Proposed orientation: rotate 180 degrees around X, broad outer roof face on the bed, columns and structural brims upward. Model footprint 116.8 × 121.8 mm; height 57 mm. Column axes cross layer bonds, making them more vulnerable to sideways bending. Removable snug supports are generated beneath overhangs; some start on the roof itself.

PETG, 0.20 mm layers, four walls, 35% infill, bed 80 C, nozzle 245/250 C. No adhesion brim or skirt. Slow first layer: 15 mm/s walls/support and 20 mm/s infill. Estimate 4 h 42 min, 52.93 g including supports. Warm-up may change elapsed time.

Verified 285 model layers to 57 mm, plate bounds, corrected positive-Z purge, no negative-Z moves, no adhesion brim/skirt, G-code/3MF agreement, and source hash. Q2 ready/standby at preparation; gentler cutter macro read back and verified.

Exact previews: print_layout_top.png and first_layer_top.png. Approved/start state is in print_job.json. User approved this exact updated layout/orientation and confirmed the bed empty with PETG loaded. Uploaded G-code was downloaded and SHA-256 verified against the approved file. Q2 accepted start, and live status confirmed this exact job active and printing. See print_job.json and printer_after_start.json. The older cancelled ../print_roof job is preserved.
