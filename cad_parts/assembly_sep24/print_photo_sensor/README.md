# Photo-sensor print: all three current parts

Prepared directly from ../main_photo_sensor.FCStd: SensorHolder, CoverStrip and BuzzerHolder. Native CAD unchanged. The current builder supersedes outdated AGENTS/README descriptions: two blind M3 insert pockets replace the four holder mounting holes. Both insert pockets were checked empty; their floors are intentional.

Holder enclosure bottom down, arms parallel to layers with removable supports. U-cover broad face down; buzzer ring bottom and flat tab down. This keeps arm and ring lengths in the layer plane. Support contact may leave texture beneath the arms. The 0.30 mm cover is thin and needs care during removal.

PETG, 0.20 mm first layer then 0.10 mm layers, four walls, 35% nominal infill, snug build-plate supports, 80 C bed. No brim or skirt. Exact U-cover thickness preserved as two layers: 0.20 + 0.10 mm. Estimate 2 h 09 min, 10.8 g. Actual startup time can differ.

All three meshes are closed and their volumes agree with CAD within 0.1%. FreeCAD reports a curve-on-surface Boolean-check warning in the existing buzzer CAD; the solid is valid and its mesh has no self-intersections. The holder has 17 tessellation seam contacts shorter than 0.040 mm, all within 0.020 mm of its valid CAD surface; no CAD geometry was changed. Diagnostics are in export_validation.json. QIDI slicing and toolpath checks passed, including all three heights, the cover's exact two layers, source hash, bed bounds, no brim/skirt, corrected positive-Z purge and embedded G-code agreement. Gentler cutter macro verified on the idle printer at preparation.

Preview: print_layout_top.png. First-layer contact: first_layer_top.png. print_job.json records the exact G-code hash. User approved this exact layout and confirmed the bed clear and PETG loaded. Uploaded file was downloaded and checksum verified. Q2 accepted start and live status confirmed printing the exact approved filename. See print_job.json and printer_after_start.json.
