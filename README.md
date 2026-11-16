# EXIF Guard

Share JPEGs with fewer hidden details. EXIF Guard removes common metadata-bearing JPEG segments while copying the compressed image data unchanged.

![Animated metadata shield](assets/hero.svg)

## Features
- Removes APP1 (EXIF/XMP), APP13 (IPTC/Photoshop), and COM segments.
- Preserves image scan data and unrelated segments.
- Never re-encodes pixels or changes the source file.
- Reports what it removed and writes to a separate destination.

## Run

Python 3.10+, standard library only.

```bash
python tool.py photo.jpg --output photo-clean.jpg
python -m unittest -v
```

## Safety and scope
This version handles JPEG files only. Metadata can also exist in other formats and in non-standard application segments. Keep the original, inspect the result, and do not treat this as a forensic sanitization guarantee.

## Design
A protective shield motif uses a graphite-and-copper palette. Its scanning ring is decorative and reduced-motion aware.

## License
MIT.
