# Release checks

## Local verification

Run the plugin-creator skill's `validate_plugin.py` against the plugin root and skill-creator's `quick_validate.py` against `skills/social-posting`. Run the backend MCP tests covering profiles, factory dispatch, posting controller metadata, OAuth redirects, and existing post/draft handlers.

## Live acceptance after deployment

Use a dedicated workspace and an explicitly authorized test destination.

1. An unauthenticated POST to `/mcp/posting` returns 401 and a `WWW-Authenticate` header containing `resource_metadata="https://api.so-me.studio/.well-known/oauth-protected-resource/mcp/posting"`.
2. The metadata URL returns the posting resource and authorization server. Install/connect the plugin and complete OAuth in the browser. Verify that the Codex callback succeeds with a dynamically selected loopback port.
3. `tools/list` returns exactly the 22 names in `MCP_POSTING_TOOLS`, including media lookup and presigned uploads. Direct calls to `get_analytics_summary`, `reply_to_conversation`, `disconnect_account`, and an unknown tool return errors without charging credits or dispatching handlers.
4. List connected accounts. Save a text draft and verify that no publication is queued. Edit the draft and read it back.
5. Schedule an authorized text post in the future; verify account, timezone, text, and queued status. Reschedule with `schedule_post`, confirm the new queue time, then cancel with `unschedule_post`.
6. On an authorized test destination, publish a text post and read back its status. Do not call a merely queued post published. Convert a separate draft only when authorized; confirm the resulting post and removal of the draft.
7. Verify that an ambiguous account or timezone prompts for clarification; a media-required destination does not receive an empty-media publication; an uncertain write response does not trigger duplicate creation.
8. Reserve an image upload. Before sending bytes, verify that `get_media_file` with `verifyUpload: true` fails and `create_post` cannot queue it. PUT the correct bytes and confirm upload verification succeeds.
9. Schedule a single image and a video on compatible test destinations. Check the actual published attachment and caption, not only the returned post ID. Test multiple images and confirm their order.
10. Save a media draft, change its caption, and convert it. Verify attachments persist. Replace an upcoming post's files, then test clearing attachments together with changing its type to TEXT.
11. Try a missing/foreign-workspace file ID, a mismatched MIME/size, and an IMAGE post with video attachments. Each must fail before publication. Deleting the original library entry after successful scheduling must not break the post copy.

## Release boundaries

Local tests do not prove that production is deployed, OAuth has completed, or a social platform accepted a post. Record those checks separately before public distribution. The package contains no runtime proxy, dependency installer, or credentials. Public-directory submission and deployment are separate release actions.

## Creation validation (2026-09-07)

Plugin and skill validators passed. The four focused backend suites passed 234 tests with isolated transpilation. The default test run exhausted its heap, and existing post/draft handler suites hit a circular dependency during initialization under isolated transpilation; those two suites are not counted as passed. No live social writes were made.

Production OAuth discovery returned 200; the new posting metadata URL returned 404. Backend deployment and authenticated acceptance remain required.

## Media validation (2026-09-08, v1.1)

302 backend tests passed across ten focused suites, including existing post/draft handlers, uploaded-object verification, media conversion, post-copy cleanup, and attachment ordering. Four Python upload-helper tests passed. Plugin and skill validation passed. A TypeScript no-emit check passed with an 8 GB heap during development. The earlier handler-suite initialization failures are resolved by mocking their external service dependencies for unit testing. Live upload/OAuth/publication acceptance remains a separate check after deployment.
