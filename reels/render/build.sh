#!/usr/bin/env bash
# Download the generated photos + voice-over clips from Higgsfield and render the final Reel.
# Needs outbound access to d8j0ntlcm91z4.cloudfront.net, plus pip (imageio-ffmpeg, pillow) and npm.
# Usage: reels/render/build.sh [music.mp3]
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
WORK="${WORK:-$HERE/.build}"
CDN=https://d8j0ntlcm91z4.cloudfront.net/user_2z8UpgX5wtqTzSukvLalup3RaQk
mkdir -p "$WORK/assets" "$WORK/vo" "$WORK/fonts"

fetch() { [ -s "$2" ] || curl -sSfL -o "$2" "$CDN/$1"; }

# Photos (9:16, 1520x2688), all the same bathroom.
fetch hf_20260929_153921_6fc3ab3b-2a74-4476-9688-d83d52c0de95.png "$WORK/assets/prima.png"
fetch hf_20260929_154050_29eea8b2-bdfb-4b0f-ad56-86fcbf955fcf.png "$WORK/assets/sopralluogo.png"
fetch hf_20260929_154119_26ba49fc-a3c0-4e9d-bf21-a251b1c22f11.png "$WORK/assets/campioni.png"
fetch hf_20260929_154009_658fd15d-96e1-4eb2-b28e-3945f11950fb.png "$WORK/assets/impianti.png"
fetch hf_20260929_155300_1813edf9-f7a0-4a4e-866a-02d30ca58dbf.png "$WORK/assets/posa.png"
fetch hf_20260929_154023_7519e592-d86c-4382-8e10-84fba6bd0c37.png "$WORK/assets/vetro.png"
fetch hf_20260929_154010_8abfb419-ad36-422f-8282-672418d3e3ed.png "$WORK/assets/dopo.png"
fetch hf_20260929_154118_27d9b4bb-4f3d-4989-8438-e1e167787901.png "$WORK/assets/dettaglio.png"
cp "$HERE/../assets/logo.webp" "$WORK/assets/logo.webp"

# Voice-over, Elena, one clip per scene.
fetch hf_20260929_152711_e155f3da-b335-46f2-8122-b8410808d128.mp3 "$WORK/vo/vo1.mp3"
fetch hf_20260929_153203_735c7492-ba24-42a9-86aa-1da4754f9f86.mp3 "$WORK/vo/vo2.mp3"
fetch hf_20260929_152703_300f0ecb-47d3-4195-9f6f-ea7d6aa9ea98.mp3 "$WORK/vo/vo3.mp3"
fetch hf_20260929_152724_d92a27cd-03ef-4d60-ae91-dc3270091c6f.mp3 "$WORK/vo/vo4.mp3"
fetch hf_20260929_152724_0eaecdc7-67d3-4acb-bb72-b51f329822ad.mp3 "$WORK/vo/vo5.mp3"
fetch hf_20260929_152735_81e0bc3c-e50c-402b-abdd-2febfa618d85.mp3 "$WORK/vo/vo6.mp3"
fetch hf_20260929_152735_44621c17-d4b4-4414-9785-14841a5eb31d.mp3 "$WORK/vo/vo7.mp3"
fetch hf_20260929_152703_3d3eab75-e0e9-4308-9db6-570d09d8bf8a.mp3 "$WORK/vo/vo8.mp3"

# Brand font (Plus Jakarta Sans, OFL).
if [ ! -d "$WORK/fonts/package" ]; then
  (cd "$WORK/fonts" && npm pack -s @fontsource/plus-jakarta-sans >/dev/null && tar xzf fontsource-plus-jakarta-sans-*.tgz)
fi

pip install -q imageio-ffmpeg pillow
MUSIC=()
[ $# -ge 1 ] && MUSIC=(--music "$1")
python3 "$HERE/render_reel.py" "$WORK/assets" "$WORK/fonts/package/files" \
  "$HERE/../video/reel-40s-rpt.mp4" --vo "$WORK/vo" "${MUSIC[@]}"
echo "Done: reels/video/reel-40s-rpt.mp4"
