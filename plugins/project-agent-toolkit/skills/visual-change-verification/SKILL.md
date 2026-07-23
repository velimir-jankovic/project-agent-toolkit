---
name: visual-change-verification
description: Verify UI, drawing, modeling, animation, VFX, scene, terrain, map, or other visual changes with real rendered artifacts and an explicit visual review instead of compile or unit-test evidence alone. Use whenever acceptance depends on appearance, layout, readability, motion, composition, scale, occlusion, or interaction in a visual runtime or authoring tool.
---

# Visual Change Verification

A build proves that visual code executes. It does not prove that the result
looks correct.

## Workflow

1. Read the routed visual, architecture, rules, workflow, and state
   authorities.
2. Identify the real acceptance surface and reference:

   - target application, game, editor, browser, renderer, or DCC tool;
   - required viewport sizes, camera angles, states, themes, and platforms;
   - concept art, mockup, style guide, or prior accepted result.

3. Exercise the real workflow. Do not substitute source inspection or a mock
   when the requested surface can be rendered.
4. Capture fresh artifacts after the change. Use screenshots for static
   results and bounded video or frame sequences for motion and transitions.
5. Inspect the artifacts at useful scale. Check composition, alignment,
   clipping, overlap, hierarchy, readability, consistency, state transitions,
   scale, collision, occlusion, and reference fidelity as applicable.
6. Iterate until the artifacts pass. A known visual defect is not accepted
   because automated tests are green.
7. Run the routed validation command with visual evidence:

   ```console
   python <plugin-root>/scripts/governance.py verify \
     --root <project-root> \
     --task "<visual task>" \
     --path <changed path> \
     --claim "<visual acceptance claim>" \
     --visual-artifact <project-relative screenshot-or-video> \
     --visual-check "<specific check performed>" \
     --visual-verdict pass
   ```

8. Cite the resulting evidence receipt. It binds artifact hashes, review
   checks, validation results, configuration, and revision state.

## Rules

- Visual routes cannot complete with compile/tests alone.
- Evidence must come from the actual changed surface.
- Artifacts must be project-relative image or video files.
- `pass` requires at least one concrete review check.
- When several views or states materially differ, capture all of them.
- Compare against references explicitly; do not rely on memory.
- If the surface cannot be controlled or captured reliably, improve its
  development API or MCP surface before claiming visual completion.
