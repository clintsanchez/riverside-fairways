---
name: youtube-channel-pending
description: Riverside Fairways has no YouTube channel yet; event clips are self-hosted as an interim step
metadata:
  type: project
---

**Riverside Fairways does not have a YouTube channel yet — it still needs to be
created.** The plan (agreed 2026-08-23) is to host their event clips there and
embed from YouTube.

Current state: the "See It In Action" clip on the homepage is **self-hosted**
(attachment 6050, 415 KB, 720x1280, H.264 +faststart, compressed from a 2.1 MB
phone original). It uses Elementor's native **video widget**, so switching to
YouTube later means changing `video_type` from `hosted` to `youtube` and pasting
the URL — the `.rf-action-video` CSS (340px cap, rounded frame) still applies.

**Why:** the reason to move to YouTube is **distribution** — a channel presence,
video search, and a surface AI assistants can cite. It is *not* a speed win: a
YouTube iframe pulls roughly 500-900 KB of player JS plus third-party cookies
before a frame plays, which is heavier than the 415 KB file for a 6-second silent
loop. A middle option is to publish on YouTube for reach and keep the
self-hosted file as the on-page loop.

**How to apply:** when the channel exists, add **VideoObject schema** — that, not
the embed itself, is what earns video rich results. Also verify the footer's
YouTube icon points at the real channel; several footer links (*Membership*,
*Activity*) are still template-kit placeholders.

The client is sending more footage after **Labor Day weekend 2026**.

Related: [[wpengine-cache-before-verifying]]
