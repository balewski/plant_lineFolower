# Pillar frames and photo-sensor holder — September 24

Prepared for layout/orientation approval. Three parts: FrontPillarFrame, AftPillarFrame and SensorHolder, exported from the current main_pillars.FCStd and main_photo_sensor.FCStd. No upload/start performed.

PETG, 0.20 mm layers, four walls, 35% infill; no brim or skirt. Build-plate-only snug supports, 0.20 mm top separation. Corrected positive-Z startup wipes and installed gentle cutter macro verified. Estimated 4 h 23 min, 44.7 g.

Front frame +90 degrees about X (negative-Y braced face down); aft frame -90 degrees (positive-Y braced face down). Broad frame faces keep column/bracing loads predominantly in layer planes; insert holes are horizontal and some projecting features need support. Sensor holder rotated180 degrees about X, separator tops down, mounting arms parallel to layers with removable support beneath. This orientation favors arm bending strength; supported surfaces need cleanup.

print_layout_top.png is an exact G-code top projection. first_layer_top.png shows actual bed contact. All three meshes are closed and differ from CAD volume by less than0.1%. A microscopic four-edge tessellation seam in the sensor mesh was closed: repaired area0.017215mm², repaired triangle centers within0.03mm of CAD. Native CAD unchanged. STL vertex bounds are used instead of conservative spline-control CAD bounds; all mesh minima are normalized to the bed.

Validation: export_validation.json, toolpath_checks.json, startup_verification.json and print_job.json. Every object has a0.20mm first layer; all paths within the270mm bed; no brim/skirt paths or negative-Z movement;3MF and standalone G-code match byte-for-byte. Final user approval and a clear bed are required before starting.
