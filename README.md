# So-me Studio plugin

Version **1.0.0** focuses on social media text posting. This separate plugin repository reuses So-me Studio's hosted MCP backend and branding from the Claude connector.

## Included

- Find connected social accounts.
- Save and edit text drafts.
- Publish text posts now or schedule them for later.
- Review the posting calendar and publication status.
- Edit, reschedule, cancel, delete, or retry posts when requested.

The posting endpoint exposes 17 tools. Analytics, inbox, account administration, AI generation, bulk deletion, and other product features are excluded. Image/video attachments are not supported by the existing MCP posting handlers; media posting is deferred to a later release. Platform support depends on connected accounts and whether the destination accepts text-only posts.

## Connection

The plugin uses Streamable HTTP at `https://api.so-me.studio/mcp/posting`, with browser-based OAuth. No API keys or client secrets are packaged.

For local Codex use, install from your personal marketplace, connect your So-me Studio account when prompted, and start a new task. The workspace must have API/MCP access, available credits, and its social destinations already connected. The existing connector documents Team+ access; workspace entitlements remain authoritative.

Try: “Save this as a LinkedIn draft in So-me Studio,” “Schedule this text post for tomorrow at 10 AM Asia/Dhaka,” or “Show my upcoming posts.”

## ChatGPT distribution

This package uses the shared `.codex-plugin/plugin.json` format. Local Codex installation does not publish it to ChatGPT. For ChatGPT developer testing, register the posting MCP URL in developer mode, complete OAuth, and use the technical connection ID issued by ChatGPT to add an `.app.json` mapping if needed. No connection ID has been invented or bundled. Public distribution requires the plugin submission process.

## Backend release prerequisite

**Deploy the accompanying `schedular-app` backend changes before connecting this plugin.** They add:

- `POST /mcp/posting`, with a posting-only allowlist enforced for both tool discovery and invocation.
- `GET /.well-known/oauth-protected-resource/mcp/posting` and a path-specific authentication challenge.
- OAuth matching for variable native loopback ports used by Codex, while preserving exact host/path/query matching.

Existing `/mcp` and `/mcp/directory` catalogs are preserved. This endpoint is a tool-surface restriction, not a new OAuth permission scope. Existing workspace authentication, plan checks, and credits still apply.

See [release checks](docs/release-checks.md) for validation and the live acceptance flow. Creation of this package does not deploy the backend or submit the plugin to the public directory.

## Files and future releases

`.codex-plugin/plugin.json` holds listing metadata. `.mcp.json` configures the connection. `skills/social-posting/SKILL.md` teaches the posting workflow. `assets/icon.svg` and `LICENSE` are reused from the MIT-licensed Claude connector.

For future features, explicitly extend the backend posting profile or introduce another profile, update the skill and listing, and bump the plugin version. New backend tools do not automatically enter the posting allowlist.

The local authoring repository is separate from the personal marketplace source at `~/plugins/so-me-studio`. Copy the updated package there before reinstalling during development. The personal marketplace catalog is `~/.agents/plugins/marketplace.json`; use the plugin-creator skill's cachebuster/reinstall workflow for installed-plugin updates. Keep `.git` and local credentials out of distributed packages.

Official references: [OpenAI plugin packaging](https://developers.openai.com/plugins/build/plugins) and [Codex MCP](https://learn.chatgpt.com/docs/extend/mcp?surface=cli).

Product: [so-me.studio](https://so-me.studio) · [MCP documentation](https://docs.so-me.studio/mcp/overview) · [Privacy policy](https://so-me.studio/privacy-policy) · Support: support@so-me.studio
