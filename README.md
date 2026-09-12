# Social media studio plugin

Version **1.3.0** supports social media text, image, and video posting, thread chains, an automatic first comment, and typed TikTok options. Social media studio connects to So-me Studio's hosted MCP backend and uses the logo supplied by 7t1 Studio.

## Included

- Find connected social accounts.
- Look up existing Pinterest boards, Discord/Slack channels, Reddit communities/flairs, Google Business locations, and TikTok creator options needed for posting.
- Compare file sizes, types, pixel size, aspect ratio, codec, and frame rate across destinations and decide how to handle incompatible media.
- Publish a multi-post chain on X, Threads, Bluesky, or Mastodon.
- Add an automatic first comment for hashtags or a link on the platforms that support one.
- Collect the TikTok privacy level and interaction options from the creator before publication.
- Upload images/videos or select existing library media.
- Verify that uploads finished and match their declared type and size.
- Save and edit text, image, and video drafts.
- Publish posts now or schedule them for later, preserving attached media.
- Replace attachments on upcoming posts; reuse media across destinations.
- Review the posting calendar and publication status.
- Edit, reschedule, cancel, delete, or retry posts when requested.

The posting endpoint exposes 31 tools. Analytics, inbox, account administration, AI generation, bulk deletion, and other product features are excluded. Post types include TEXT, IMAGE, MULTIPLE_IMAGES, VIDEO, REEL, STORY, and CAROUSEL where the destination supports them. File format, duration, dimensions, and platform limits still apply.

## Image and video upload flow

1. Run `validate_post_media` for all intended destinations using local file metadata or existing library file IDs. Review each result and resolve any incompatibility or unknown checks with the user. Then call `presign_media_upload` with each file's `filename`, `mimetype`, and exact `size` in bytes.
2. Upload the raw bytes with HTTP PUT to the returned `uploadUrl`, using the same Content-Type. The bundled `scripts/upload_media.py` streams local files without third-party dependencies; its input is a temporary JSON plan with `filePath`, `fileId`, `uploadUrl`, `mimetype`, and `size` for each file.
3. Call `get_media_file` with `verifyUpload: true` for each returned `fileId`.
4. Pass those `fileIds` and a matching `postType` to `create_post` or `create_draft`. Supply `scheduledAt` to schedule; omitting it on `create_post` publishes now. Saved draft media carries into `convert_draft`.

The backend checks ownership and completed uploads before attaching media. Each post receives independent storage copies so deleting/reusing a library item does not break scheduled posts. Image selection order is retained during publishing. Existing drafts with only URLs need library file IDs attached before MCP conversion. No database migration is needed: draft media uses existing JSON metadata and posts use the existing file relation.

Direct local upload requires access to the source file and an HTTP upload capability (the bundled helper requires Python 3). Clients that cannot transfer bytes can use media already uploaded through the So-me Studio app. Presigned URLs alone do not upload anything. This is upload support for your own files, not AI image/video generation.

## Thread chains, first comment, and TikTok options

`create_post`, `update_post`, `schedule_post`, `create_draft`, and `update_draft` take three new top-level fields.

`threadParts` is the ordered list of posts that follow the head post, which stays in `text`. A three-post chain is `text` plus two thread parts. Each part is `{ text, fileIds }` or a plain string. Chains work on X (280 characters, 4 media per part), Threads (500, 20), Bluesky (300 graphemes, 4), and Mastodon (500, 4), at most 24 parts each. Every other destination rejects the field. Publishing past the head is best effort: a failed part leaves the head live and the post carries a warning naming how many parts published.

`firstComment` is one comment posted automatically under the post right after it publishes, usually hashtags or a link. Limits are Facebook 8000, Instagram 2200, X 280, LinkedIn and LinkedIn Page 1250, Threads 500, YouTube 10000 characters. An unsupported destination is not rejected: the post publishes there without the comment and the response carries a `FIRST_COMMENT_UNSUPPORTED` warning. `list_accounts` and `get_account` return `capabilities.firstComment`, `capabilities.firstCommentMaxLength`, `capabilities.threads`, and `capabilities.threadPartMaxLength` per account, so the plugin reads support from the server. On a chain the comment goes under the last part.

`tiktok` carries `privacyLevel`, `allowComments`, `allowDuet`, and `allowStitch`. TikTok rejects a post that has no privacy level, and only the creator may choose one, so the plugin calls `get_tiktok_creator_info`, offers only the returned `privacy_level_options`, recommends `PUBLIC_TO_EVERYONE`, and asks whether comments are allowed. A TikTok post without `tiktok.privacyLevel` is rejected with `TIKTOK_PRIVACY_LEVEL_REQUIRED` and the payload lists the allowed options. Settings the creator disabled account-wide are forced off and reported as `TIKTOK_SETTING_FORCED` warnings.

## Different limits across destinations

`validate_post_media` returns every target's status, filename, actual size/type, allowed types, byte/count/duration limits, issues, warnings and user choices. It reuses the backend's `FILE_VALIDATION_RULES`; these are So-me Studio configured limits, not a freshly verified catalog of external platform API limits. For example, the current configuration allows a 150 MiB MP4 under Facebook VIDEO's size limit but rejects it for Instagram VIDEO (100 MiB). The plugin presents both outcomes before publishing anywhere. The user can choose destinations, provide another file, request conversion/compression, save a draft or cancel. Nothing is silently skipped or changed.

`validate_post_media` also measures each library file from its own bytes and compares the measured width, height, duration, video codec, and frame rate against each destination's rules. Mismatches return `DIMENSIONS_INVALID`, `ASPECT_RATIO_INVALID`, `CODEC_UNSUPPORTED`, or `FRAME_RATE_INVALID`, each with `measured`, `required`, and a `fix` string naming the exact change, such as the crop dimensions for an aspect-ratio failure. The plugin calls the check before `create_post` whenever it generated or edited the media, applies the fix, and revalidates. `get_media_rules` returns the whole per-platform rules table, which is useful for generating media at the right size in the first place.

The backend independently rejects known size/type/count incompatibilities before creating, updating, rescheduling, retrying or converting posts. Missing configured media rules also block that target instead of guessing. Drafts remain available for editing when conversion fails. Video duration is checked when provided to preflight; unknown duration and uninspected codecs/dimensions are explicitly marked for review. Library file records do not store measured duration. Content inspection and final platform/account acceptance are outside this check, so a basic pass is not a publication guarantee.

## Connection

The plugin uses Streamable HTTP at `https://api.so-me.studio/mcp/posting`, with browser-based OAuth. No API keys or client secrets are packaged.

For local Codex use, install from your personal marketplace, connect your So-me Studio account when prompted, and start a new task. The workspace must have API/MCP access, available credits, and its social destinations already connected. The existing connector documents Team+ access; workspace entitlements remain authoritative.

Try: “Upload this image and schedule it on Facebook tomorrow at 10 AM Asia/Dhaka,” “Save this video as a draft,” or “Show my upcoming posts.”

## ChatGPT distribution

This package uses the shared `.codex-plugin/plugin.json` format. Local Codex installation does not publish it to ChatGPT. For ChatGPT developer testing, register the posting MCP URL in developer mode, complete OAuth, and use the technical connection ID issued by ChatGPT to add an `.app.json` mapping if needed. No connection ID has been invented or bundled. Public distribution requires the plugin submission process.

## Backend release prerequisite

**Deploy the accompanying `schedular-app` backend changes before connecting this plugin.** They add:

- `POST /mcp/posting`, with a posting-only allowlist enforced for both tool discovery and invocation.
- `GET /.well-known/oauth-protected-resource/mcp/posting` and a path-specific authentication challenge.
- OAuth matching for variable native loopback ports used by Codex, while preserving exact host/path/query matching.
- Media upload validation and verification, `fileIds` on posts/drafts, and media-preserving draft conversion. The shared `/mcp/directory` endpoint also receives the enhanced posting handlers used by Claude.

Existing `/mcp` and `/mcp/directory` catalogs are preserved. This endpoint is a tool-surface restriction, not a new OAuth permission scope. Existing workspace authentication, plan checks, and credits still apply.

See [release checks](docs/release-checks.md) for validation and the live acceptance flow. Creation of this package does not deploy the backend or submit the plugin to the public directory.

## Files and future releases

`.codex-plugin/plugin.json` holds listing metadata. `.mcp.json` configures the connection. `skills/social-posting/SKILL.md` teaches the posting workflow. `assets/icon.png` is the supplied plugin logo and composer icon. The original `LICENSE` is retained from the MIT-licensed Claude connector.

For future features, explicitly extend the backend posting profile or introduce another profile, update the skill and listing, and bump the plugin version. New backend tools do not automatically enter the posting allowlist.

The local authoring repository is separate from the personal marketplace source at `~/plugins/so-me-studio`. Copy the updated package there before reinstalling during development. The personal marketplace catalog is `~/.agents/plugins/marketplace.json`; use the plugin-creator skill's cachebuster/reinstall workflow for installed-plugin updates. Keep `.git` and local credentials out of distributed packages.

Official references: [OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins) and [Codex MCP](https://learn.chatgpt.com/docs/extend/mcp?surface=cli).

Product: [so-me.studio](https://so-me.studio) · [MCP documentation](https://docs.so-me.studio/mcp/overview) · [Privacy policy](https://so-me.studio/privacy-policy) · Support: support@so-me.studio
