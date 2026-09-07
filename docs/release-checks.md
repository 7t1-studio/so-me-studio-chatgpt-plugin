# Release checks

For current production results, see [live acceptance on 2026-09-08](live-acceptance-2026-09-08.md). The dated sections below preserve earlier development results; their deployment status is historical.

## Local verification

Run the plugin-creator skill's `validate_plugin.py` against the plugin root and skill-creator's `quick_validate.py` against `skills/social-posting`. Run the backend MCP tests covering profiles, factory dispatch, posting controller metadata, OAuth redirects, and existing post/draft handlers.

## Live acceptance after deployment

Use a dedicated workspace and an explicitly authorized test destination.

1. An unauthenticated POST to `/mcp/posting` returns 401 and a `WWW-Authenticate` header containing `resource_metadata="https://api.so-me.studio/.well-known/oauth-protected-resource/mcp/posting"`.
2. The metadata URL returns the posting resource and authorization server. Install/connect the plugin and complete OAuth in the browser. Verify that the Codex callback succeeds with a dynamically selected loopback port.
3. `tools/list` returns exactly the 30 names in `MCP_POSTING_TOOLS`, including validate_post_media, media lookup and presigned uploads. Direct calls to `get_analytics_summary`, `reply_to_conversation`, `disconnect_account`, and an unknown tool return errors without charging credits or dispatching handlers.
4. List connected accounts. Save a text draft and verify that no publication is queued. Edit the draft and read it back.
5. Schedule an authorized text post in the future; verify account, timezone, text, and queued status. Reschedule with `schedule_post`, confirm the new queue time, then cancel with `unschedule_post`.
6. On an authorized test destination, publish a text post and read back its status. Do not call a merely queued post published. Convert a separate draft only when authorized; confirm the resulting post and removal of the draft.
7. Verify that an ambiguous account or timezone prompts for clarification; a media-required destination does not receive an empty-media publication; an uncertain write response does not trigger duplicate creation.
8. Reserve an image upload. Before sending bytes, verify that `get_media_file` with `verifyUpload: true` fails and `create_post` cannot queue it. PUT the correct bytes and confirm upload verification succeeds.
9. Schedule a single image and a video on compatible test destinations. Check the actual published attachment and caption, not only the returned post ID. Test multiple images and confirm their order.
10. Save a media draft, change its caption, and convert it. Verify attachments persist. Replace an upcoming post's files, then test clearing attachments together with changing its type to TEXT.
11. Try a missing/foreign-workspace file ID, a mismatched MIME/size, and an IMAGE post with video attachments. Each must fail before publication. Deleting the original library entry after successful scheduling must not break the post copy.

12. Before upload, check the same 150 MiB MP4 against Facebook VIDEO and Instagram VIDEO. Verify both targets are returned, Instagram reports its 100 MiB configured limit, and neither a media reservation nor post is created by the check. The plugin must show both results and wait for the user's choice before any publication.
13. Try an AVI file on Facebook VIDEO and Instagram VIDEO. Verify the rejected target lists the actual type and accepted types. Try a file exactly at the size limit and one byte over it.
14. Test unknown duration/codec checks: the plugin must describe them as unchecked, not promise acceptance. Test an overlong supplied duration, too many attachments, excess total size and a target without configured rules.
15. Attempt to create/convert/reschedule/retry a known incompatible media post. It must fail with specific reasons before copying, saving or queueing. A failed draft conversion must preserve the original draft.
16. Choose only one destination after a mixed result, or choose another file/draft/cancel. Verify the plugin follows that choice, never silently drops a destination or modifies a file, and checks changed media again.

## Release boundaries

Local tests do not prove that production is deployed, OAuth has completed, or a social platform accepted a post. Record those checks separately before public distribution. The package contains no runtime proxy, dependency installer, or credentials. Public-directory submission and deployment are separate release actions.

## Creation validation (2026-09-07)

Plugin and skill validators passed. The four focused backend suites passed 234 tests with isolated transpilation. The default test run exhausted its heap, and existing post/draft handler suites hit a circular dependency during initialization under isolated transpilation; those two suites are not counted as passed. No live social writes were made.

Production OAuth discovery returned 200; the new posting metadata URL returned 404. Backend deployment and authenticated acceptance remain required.

## Media validation (2026-09-08, v1.1)

302 backend tests passed across ten focused suites, including existing post/draft handlers, uploaded-object verification, media conversion, post-copy cleanup, and attachment ordering. Four Python upload-helper tests passed. Plugin and skill validation passed. A TypeScript no-emit check passed with an 8 GB heap during development. The earlier handler-suite initialization failures are resolved by mocking their external service dependencies for unit testing. Live upload/OAuth/publication acceptance remains a separate check after deployment.

## Compatibility validation (2026-09-08, v1.2)

325 tests passed across eleven backend suites, including multi-destination reports, exact size boundaries, MIME mismatches, duration warnings, malformed input, tenant-scoped library lookup and blocking incompatible writes before storage/database/queue effects. TypeScript no-emit validation and plugin/skill validation passed. The check uses existing So-me Studio backend rules; no live external-platform policy audit or media-content inspection is claimed. Production deployment and authenticated acceptance are still pending.
