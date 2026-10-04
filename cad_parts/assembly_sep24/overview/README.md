# Robot overview — visualization only

Open `../main_overview.FCStd`. The two independent groups, **AssembledRobot** and **ExplodedRobot**, are visible side by side. Select either group and press Space to hide it. All geometry is embedded: opening the file does not require the source documents. Rebuild with `build_overview.py` after design changes; this is a snapshot, not a live assembly.

The overview includes the current decks, pillars, clamps, motor/wheel/caster references, photo sensors, upper electronics, Pi enclosure, battery, socket, inserted plug, and two toggle switches. It is not a manufacturing model.

Pi orientation is 94 × 63 × 30 mm (X/Y/Z), seated at Z4 and centered on the deck marking. The battery is 76 × 22 × 41 mm (X/Y/Z), seated at Z4.3 (0.1 mm above the 0.2 mm raised deck letters), with its front face at Y−60.75. This gives 0.25 mm clearance to the aft frame and keeps its footprint inside the deck perimeter. Pi clearance is 20 mm below the upper floor, or 18 mm below the ammeter support; battery clearance to the upper platform is 8.7 mm.

The motor-driver mock board was slid 7.406 mm up the existing slope to seat against the new stops. It overhangs the right edge by 1.394 mm. Its actual hole pattern is unverified. Plug, socket, toggle dimensions and component heights are illustrative; no connector-access, wiring or physical fit claim is made.

To animate the switches, run `animate_toggles.FCMacro` from FreeCAD's Macro dialog. Both assembled and exploded levers move through ±25 degrees for eight seconds. Animation does not save the document automatically.

Run `build_overview.py` with FreeCAD's Python interpreter (see `../AGENTS.md` for the path). It rewrites `../main_overview.FCStd` and writes `fit_report.json` (envelope placements, collisions, clearances) to `../tmp/`. Run headlessly it saves no GUI view data, so open the file in the FreeCAD GUI and save once to store colors and visibility. Preview PNGs (`assembled`, `assembled_top`, `assembled_side`, `exploded`, `overview`) are regenerated into `../tmp/` from the saved document.

The mockup hardware overlaps slightly in three places (`MotorDriverPCB` with `PowerAPCB`, and each toggle body with the chassis, under 1 mm³ each). These are accepted; no printed part is affected.

The exploded assembly origin is offset 345 mm to the right of the assembled origin, increased 50% from 230 mm. Individual explosion distances are unchanged.
