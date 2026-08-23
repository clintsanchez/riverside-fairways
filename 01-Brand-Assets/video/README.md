# Video

Client footage and the web-optimised derivatives.

| File | What it is |
| --- | --- |
| `mobile-golf-simulator-swing-clip-2026-08-23.mov` | Original from Christy/Jase, 2026-08-23. 2.1 MB, 5.8s, 720x1280 portrait, H.264. Keep as the master. |
| `riverside-fairways-mobile-golf-simulator-swing-clip.mp4` | Web version on the site. 416 KB (80% smaller), same resolution, CRF 30, `+faststart` so it streams progressively. |

The MP4 is attachment **6050** on the site, playing in the homepage
"See It In Action" section via Elementor's native video widget
(autoplay, muted, loop, playsinline, no controls). Poster frame is
`service-photos/mobile-golf-simulator-swing-indoors-video-still.webp`
(attachment 6049).

**This is interim.** The plan is to publish on the client's YouTube channel —
which does not exist yet — and switch the widget's `video_type` from `hosted`
to `youtube`. The `.rf-action-video` styling survives that change untouched.
Note that a YouTube iframe is *heavier* than this 416 KB file for a 6-second
silent loop; the reason to move is distribution, not speed.

More footage expected after Labor Day weekend 2026.

Re-encode command used:

```
ffmpeg -i input.mov -c:v libx264 -crf 30 -preset slow -profile:v main \
       -pix_fmt yuv420p -an -movflags +faststart -vf "scale=720:-2" out.mp4
```
