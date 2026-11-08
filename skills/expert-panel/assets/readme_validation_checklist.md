# README Asset Validation Checklist

- Scope and edit authorization respected.
- Claims match repository evidence.
- Essential instructions remain in Markdown.
- All local image paths resolve.
- SVG XML parses and includes `viewBox`; meaningful assets include `<title>` and `<desc>`.
- README embeds have useful alt text.
- No `<script>`, `foreignObject`, remote font imports, or fragile external raster references.
- Full-width preview checked near 900 CSS px and narrow preview near 360 CSS px.
- Text remains readable; contrast works against GitHub light and dark surroundings.
- GIF is explicitly approved, has a static SVG fallback, calm motion, a meaningful first frame, and acceptable file size.
- No commit, push, publication, embed replacement, or PR without explicit authorization.
