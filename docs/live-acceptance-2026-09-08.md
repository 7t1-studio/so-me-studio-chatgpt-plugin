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

- [x] Authenticated OAuth approval, callback, refresh, and wrong-resource rejection.
- [x] Live tool discovery and rejection of excluded/unknown tools.
- [x] Account and posting-option lookup.
- [x] Image/video metadata compatibility across requested destinations.
- [x] Upload reservation, rejection before bytes arrive, PUT, and verified library objects.
- [x] Missing/invalid files, mismatched post type, unsupported types/sizes, and blocked publication.
- [x] Draft creation/read/edit and media-preserving conversion.
- [x] Future scheduling, rescheduling, cancellation, and calendar state.
- [x] Clear attachments while switching a future image post to TEXT, then cancel it; readback confirms no attachments, PENDING, and no scheduled time.
- [x] Image and video publication confirmed after queue processing (platform outcomes below).
- [x] Published attachment/caption inspected on Threads, YouTube, and Pinterest video.
- [ ] ChatGPT client connection and media workflow.
- [ ] Installed Codex plugin workflow in a fresh task.

## Publication outcomes

| Destination | Supplied image | Supplied video |
| --- | --- | --- |
| Threads | Published; image and caption visually verified | Not attempted |
| YouTube | Unsupported image post type | Published; playback and 1:08 duration visually verified |
| Pinterest | Published | Published; video attachment and caption visually verified |
| Discord | Published | Blocked by configured 10 MiB file limit |
| Bluesky | Published | Blocked by configured 100 MiB file limit |
| Dribbble | Published | Not attempted |
| TikTok | Private publication reached PUBLISH_COMPLETE | Repaired chunked upload retested successfully: POSTED and PUBLISH_COMPLETE; private visibility, no invented public URL |
| Instagram | Rejected by Instagram: aspect ratio not supported (3084 × 1022, about 3.02:1) | Blocked by configured 100 MiB VIDEO limit; draft retained after failed conversion |
| X | Missing user-context credentials; reconnect required | Not attempted with invalid credentials |
| Facebook | Existing account session expired | Existing account session expired |
| LinkedIn | No connected account | No connected account |
| Telegram / WhatsApp | Inbox-only destinations, posting blocked | Inbox-only destinations, posting blocked |

Published examples (left in place as requested):

- [Threads image](https://www.threads.com/@noobgaming1925007/post/Dc_9VSBDEMJ)
- [Threads image after permalink repair](https://www.threads.com/@noobgaming1925007/post/DdAAY2jDC1b)
- [Threads text-only post](https://www.threads.com/@noobgaming1925007/post/DdAAqQ8DJVv)
- [YouTube video](https://www.youtube.com/watch?v=h4gpaJZEIoY)
- [Pinterest image](https://www.pinterest.com/pin/1134836806144991800/)
- [Pinterest video](https://www.pinterest.com/pin/1134836806144992120/)
- [Bluesky image](https://bsky.app/profile/noobgaming2519007.bsky.social/post/3muxedxswtj2f)
- [Dribbble image](https://dribbble.com/shots/27711422-Social-media-studio-live-test-image-upload-and-publishing)

## Additional defects found through live testing

- Production proxy exhausted its 96 MiB limit and hung during deployment. Increased its allocation to 512 MiB and restarted only the proxy. All three public origins recovered with HTTP 200; later frontend, backend, website, admin, and demo deployments succeeded.
- Added missing configured media rules for Pinterest, Bluesky, and Discord. Telegram/WhatsApp and media-required text-only targets now return explicit incompatibilities.
- Tool schemas omitted several connected platforms even though their handlers worked. Expanded the schema to match account platforms, excluding Webflow (a content source).
- TikTok sent the entire 204 MB video as a single chunk. Added sequential 10 MB chunks with the remainder merged into the final chunk, matching TikTok's transfer protocol.
- Threads constructed a URL from a numeric Graph ID, producing a 404 after successful publication. Fetch the real permalink instead; failure to fetch a URL must not cause duplicate publication.
- TikTok publish job IDs are not public video IDs. Return a link only when TikTok supplies a public post ID; private posts may have no public link.
- Instagram's aspect-ratio rejection now offers replacing, cropping/padding with approval, saving a draft, or excluding that destination. The original file is preserved.
- Draft account assignment stored an account UUID in a relation requiring a platform account ID. Normalize either identifier through a workspace-scoped lookup on creation/update and reject foreign accounts before saving.

Validation: backend type-check passed, all 398 MCP tests passed (17 suites), and 8 focused Threads/TikTok tests passed. A further draft platform-change regression passed in the 9-test draft suite. Large media writes occasionally exceeded the test client's request deadline; recent posts were reconciled before any retry, avoiding duplicate publications. Successful publications are not retried. Live retests confirmed TikTok chunking, Threads permalink retrieval, all platform enum values in tool discovery, and actionable Instagram rejection wording.

Deployment evidence: [proxy recovery](https://github.com/7t1-studio/schedular-app/actions/runs/34158595718), [posting repairs deployed](https://github.com/7t1-studio/schedular-app/actions/runs/34160244040), and [final draft normalization deployed](https://github.com/7t1-studio/schedular-app/actions/runs/34160750105), all successful. Live creation, update, and readback with account UUIDs succeeded after the final deployment; the platform account ID was stored correctly and the image attachment remained intact. Final backend source commit: `e7dde2602421f3e9b649840e78687aa942da0b51`.

## Remaining acceptance boundaries

The [final repository Checks workflow](https://github.com/7t1-studio/schedular-app/actions/runs/34160750189) passed: 1,214 backend unit tests in 86 suites, backend end-to-end tests, and frontend/website/demo lint. These use the repository's existing CI exclusions; they do not establish that every unrelated application feature has been tested.

The [final read-only server inspection](https://github.com/7t1-studio/schedular-app/actions/runs/34161569594) found the application containers healthy, zero backend/frontend/proxy restarts, no OOM flags, valid nginx configuration, and HTTP 200 from API health, app login, and the marketing site. Proxy memory was 174.5 MiB of 512 MiB; backend memory was 234.7 MiB of 768 MiB.

Backend MCP calls and browser OAuth were tested against production. The installed plugin still needs a fresh Codex task to load its tools. ChatGPT remains logged out in the available browser, so ChatGPT connection, its actual attachment-transfer capabilities, and starter-prompt behavior remain unverified. Do not describe the package as submission-ready until those client checks pass. Refreshing expired social credentials requires the account owner's sign-in flow. This report does not claim every file/post type on every platform was tested.
