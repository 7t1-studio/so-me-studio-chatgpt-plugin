# Live acceptance — 2026-09-08

Testing is authorized against the owner's connected test accounts. Successful test publications are to remain in place. This report distinguishes backend protocol tests from client-host tests; an MCP harness is not proof of ChatGPT or Codex host behavior.

## Source media

| File | Measured properties |
| --- | --- |
| cta-section.png | PNG, 177256 bytes, 3084 × 1022 |
| add-first-comment-to-suppourted-platforms.mp4 | MP4, 204075995 bytes, 68.666667 seconds, 3840 × 2160, H.264/AAC, 30 fps |

## Findings and fixes

- The production OAuth entry linked signed-in users to the marketing origin, where consent returned 404. Added the authenticated app consent page, safe request details, and a JSON callback response for top-level navigation. Corrected the legacy origin and kept consent out of marketing redirects. Login now preserves the request query string.
- The API-hosted Deny form required credentials. It now permits declining without a password.
- The original 23-tool posting profile excluded required destination lookups. Version 1.2.3 includes 30 tools, adding read-only Pinterest boards, Discord/Slack channels, Reddit subreddits/flairs, Google Business locations, and TikTok creator information. Account/board administration remains excluded.
- Facebook was already marked session expired in the test workspace. LinkedIn was not connected. ChatGPT was logged out in the available browser. These are separate from backend defects.

## Acceptance checklist

- [ ] Authenticated OAuth approval, callback, refresh, and wrong-resource rejection.
- [ ] Live tool discovery and rejection of excluded/unknown tools.
- [ ] Account and posting-option lookup.
- [ ] Image/video metadata compatibility across requested destinations.
- [ ] Upload reservation, rejection before bytes arrive, PUT, and verified library objects.
- [ ] Missing/invalid files, mismatched post type, unsupported types/sizes, and blocked publication.
- [ ] Draft creation/read/edit and media-preserving conversion.
- [ ] Future scheduling, rescheduling, cancellation, and calendar state.
- [ ] Image and video publication confirmed after queue processing.
- [ ] Published attachment/caption inspected through returned post links where accessible.
- [ ] ChatGPT client connection and media workflow.
- [ ] Installed Codex plugin workflow in a fresh task.

Production outcomes will be filled in after the repaired OAuth flow is deployed. Do not treat unchecked items as passed.
