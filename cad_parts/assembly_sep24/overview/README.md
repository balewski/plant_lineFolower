# Robot overview — visualization only

Open `../main_overview.FCStd`. The two independent groups, **AssembledRobot** and **ExplodedRobot**, are visible side by side. Select either group and press Space to hide it. All geometry is embedded: opening the file does not require the source documents. Rebuild with `build_overview.py` after design changes; this is a snapshot, not a live assembly.

The overview includes the current decks, pillars, clamps, motor/wheel/caster references, photo sensors, upper electronics, Pi enclosure, battery, socket, inserted plug, and two toggle switches. It is not a manufacturing model.

Pi orientation is 94 × 63 × 30 mm (X/Y/Z), seated at Z4 and centered on the deck marking. The battery is 76 × 22 × 41 mm (X/Y/Z), seated at Z4, with its front face at Y−60.75. This gives 0.25 mm clearance to the aft frame and keeps its footprint inside the deck perimeter. Pi clearance is 20 mm below the upper floor, or 18 mm below the ammeter bars; battery clearance is 9 mm.

The motor-driver mock board was slid 7.406 mm up the existing slope to seat against the new stops. It overhangs the right edge by 1.394 mm. Its actual hole pattern is unverified. Plug, socket, toggle dimensions and component heights are illustrative; no connector-access, wiring or physical fit claim is made.

To animate the switches, run `animate_toggles.FCMacro` from FreeCAD's Macro dialog. Both assembled and exploded levers move through ±25 degrees for eight seconds. Animation does not save the document automatically.

`fit_report.json` contains envelope placements, collisions and clearances. `verification.json` checks both views and sampled switch positions. `animation_validation.json` records the GUI animation check. `assembled.png`, `exploded.png` and `overview.png` are previews.

The exploded assembly origin is offset 345 mm to the right of the assembled origin, increased 50% from 230 mm. Individual explosion distances are unchanged.
