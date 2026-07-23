# Visual acceptance contract

## Evidence matrix

Select only rows relevant to the change, but do not omit a materially different
state or viewport.

| Surface | Minimum evidence |
| --- | --- |
| UI/layout | Normal state, constrained size, interaction/expanded state |
| Drawing/2D | Full composition and 100% detail crop |
| Model/material | Front/side/three-quarter views under representative light |
| Animation | Bounded video or key-frame sequence including transitions |
| VFX | Anticipation, active, impact, and decay frames or video |
| Scene/map/terrain | Player-scale view, overview, traversal/occlusion view |
| Responsive browser | Required desktop and mobile viewport captures |

## Review checks

- Reference fidelity and declared art direction
- Visual hierarchy and focal point
- Text clarity and contrast
- Spacing, alignment, clipping, and overlap
- Scale and proportions
- Camera-dependent artifacts and occlusion
- Motion timing, discontinuities, and state transitions
- Material, lighting, transparency, and edge quality
- Interaction feedback and disabled/error states
- Performance only when the visual effect depends on stable frame delivery

## Rejection conditions

- Artifact predates the current change.
- Artifact comes from a mock instead of the acceptance surface.
- Only source code, unit tests, or build output is supplied.
- Review says “looks good” without a specific check.
- A referenced state, viewport, or camera with materially different behavior is
  missing.
- The reviewer identifies an unresolved acceptance defect.
