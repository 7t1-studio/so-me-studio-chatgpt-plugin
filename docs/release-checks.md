# Release checks

For current production results, see [live acceptance on 2026-09-08](live-acceptance-2026-09-08.md). The dated sections below preserve earlier development results; their deployment status is historical.

## Local verification

Run the plugin-creator skill's `validate_plugin.py` against the plugin root and skill-creator's `quick_validate.py` against `skills/social-posting`. Run the backend MCP tests covering profiles, factory dispatch, posting controller metadata, OAuth redirects, and existing post/draft handlers.

## Live acceptance after deployment

Use a dedicated workspace and an explicitly authorized test destination.

1. An unauthenticated POST to `/mcp/posting` returns 401 and a `WWW-Authenticate` header containing `resource_metadata="https://api.so-me.studio/.well-known/oauth-protected-resource/mcp/posting"`.
2. The metadata URL returns the posting resource and authorization server. Install/connect the plugin and complete OAuth in the browser. Verify that the Codex callback succeeds with a dynamically selected loopback port.
3. `tools/list` returns exactly the 31 names in `MCP_POSTING_TOOLS`, including validate_post_media, get_media_rules, get_tiktok_creator_info, media lookup and presigned uploads. Direct calls to `get_analytics_summary`, `reply_to_conversation`, `disconnect_account`, and an unknown tool return errors without charging credits or dispatching handlers.
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

## Live acceptance for threads, first comment and TikTok (v1.3)

17. Publish a three-post chain on an authorized X test account: head in `text` and two `threadParts`. Confirm each part replies to the previous one. Repeat on Threads, Bluesky and Mastodon. Send a part over the platform limit and confirm the error names the platform and the limit; check Bluesky counts graphemes by sending one ZWJ emoji.
18. Send `threadParts` to an unsupported destination, for example Facebook, and confirm the 400 names the target and the supported list. Confirm `[]` clears an existing chain and an omitted field leaves it untouched.
19. Force a part to fail after the head publishes. Confirm the head stays live, `metaData.threadPartIds` holds the ids that published, and `metaData.threadPartWarning` says how many published and why the chain stopped. Confirm the plugin reports the warning and does not republish.
20. Publish with `firstComment` on Instagram, X, LinkedIn and Facebook. Read `firstCommentStatus` until it reaches `posted` and check the comment on the platform. Send a comment over the target's limit and confirm the 400 names the limit.
21. Publish with `firstComment` to TikTok. Confirm the post publishes and the response carries `warnings[{ code: "FIRST_COMMENT_UNSUPPORTED" }]` naming TIKTOK, and that the plugin repeats the warning instead of claiming the comment was posted.
22. Combine `threadParts` and `firstComment` on X and confirm the comment lands under the LAST part. Confirm `list_accounts` returns `capabilities.firstComment`, `capabilities.firstCommentMaxLength`, `capabilities.threads` and `capabilities.threadPartMaxLength` per account, and that the plugin reads support from them.
23. On a YouTube account connected before the comment permission was added, confirm the comment fails with an explanation that the account must reconnect.
24. Create a TikTok post without `tiktok.privacyLevel` and confirm `TIKTOK_PRIVACY_LEVEL_REQUIRED` with `privacyLevelOptions`. Confirm the plugin calls `get_tiktok_creator_info` first, offers only the returned options, recommends `PUBLIC_TO_EVERYONE`, and asks about comments. Send a level the creator cannot use and confirm `TIKTOK_PRIVACY_LEVEL_NOT_ALLOWED`.
25. On a creator who disabled comments, confirm the option is forced off and the result carries a `TIKTOK_SETTING_FORCED` warning the plugin repeats. Confirm `convert_draft` validates a draft saved without a privacy level and accepts a `tiktok` object of its own.
26. Validate a 2560x1080 image for Instagram IMAGE. Confirm `ASPECT_RATIO_INVALID` with `measured`, `required`, `fix` and `suggestedDimensions`. Crop to a suggested size, revalidate and confirm it passes. Repeat for `DIMENSIONS_INVALID`, `CODEC_UNSUPPORTED` and `FRAME_RATE_INVALID`. Confirm `get_media_rules` returns the per-platform table and that the plugin reads it before generating media.

## Release boundaries

Local tests do not prove that production is deployed, OAuth has completed, or a social platform accepted a post. Record those checks separately before public distribution. The package contains no runtime proxy, dependency installer, or credentials. Public-directory submission and deployment are separate release actions.

## Creation validation (2026-09-07)

Plugin and skill validators passed. The four focused backend suites passed 234 tests with isolated transpilation. The default test run exhausted its heap, and existing post/draft handler suites hit a circular dependency during initialization under isolated transpilation; those two suites are not counted as passed. No live social writes were made.

Production OAuth discovery returned 200; the new posting metadata URL returned 404. Backend deployment and authenticated acceptance remain required.

## Media validation (2026-09-08, v1.1)

302 backend tests passed across ten focused suites, including existing post/draft handlers, uploaded-object verification, media conversion, post-copy cleanup, and attachment ordering. Four Python upload-helper tests passed. Plugin and skill validation passed. A TypeScript no-emit check passed with an 8 GB heap during development. The earlier handler-suite initialization failures are resolved by mocking their external service dependencies for unit testing. Live upload/OAuth/publication acceptance remains a separate check after deployment.

## Compatibility validation (2026-09-08, v1.2)

325 tests passed across eleven backend suites, including multi-destination reports, exact size boundaries, MIME mismatches, duration warnings, malformed input, tenant-scoped library lookup and blocking incompatible writes before storage/database/queue effects. TypeScript no-emit validation and plugin/skill validation passed. The check uses existing So-me Studio backend rules; no live external-platform policy audit or media-content inspection is claimed. Production deployment and authenticated acceptance are still pending.

## Posting features (2026-09-12, v1.3)

The posting profile carries 31 tools: `get_media_rules` joins `validate_post_media` and `get_tiktok_creator_info`, which were already on the profile. `threadParts`, `firstComment` and `tiktok` are top-level fields on the write tools, not new tools, so the allowlist grows by one entry only. The skill, listing copy and README describe them; nothing in this package validates them offline. Deploy the backend changes, then run the live acceptance steps above. No production publication was performed while preparing this release.
