#!/usr/bin/env python3
"""Strip common metadata segments from JPEG files without re-encoding."""
import argparse, json
from pathlib import Path
NAMES={0xE1:"APP1 (EXIF/XMP)",0xED:"APP13 (IPTC/Photoshop)",0xFE:"COM"}
REMOVE={0xE1,0xED,0xFE}

def inspect_segments(data):
    if not data.startswith(b"\xff\xd8"): raise ValueError("not a JPEG stream")
    found=[]; i=2
    while i<len(data):
        if data[i]!=0xFF: raise ValueError("malformed JPEG marker")
        while i<len(data) and data[i]==0xFF: i+=1
        if i>=len(data): break
        marker=data[i]; i+=1
        if marker in (0xD9,0xD8,0x01) or 0xD0<=marker<=0xD7:
            if marker==0xD9: break
            continue
        if i+2>len(data): raise ValueError("truncated JPEG segment length")
        length=int.from_bytes(data[i:i+2],"big")
        if length<2 or i+length>len(data): raise ValueError("invalid JPEG segment length")
        if marker in NAMES: found.append(NAMES[marker])
        i+=length
        if marker==0xDA: break
    return found

def strip_metadata(data):
    if not data.startswith(b"\xff\xd8"): raise ValueError("not a JPEG stream")
    out=bytearray(data[:2]); i=2; removed=[]
    while i<len(data):
        if data[i]!=0xFF: raise ValueError("malformed JPEG marker")
        start=i
        while i<len(data) and data[i]==0xFF: i+=1
        if i>=len(data): out.extend(data[start:]); break
        marker=data[i]; i+=1
        if marker in (0xD9,0xD8,0x01) or 0xD0<=marker<=0xD7:
            out.extend(data[start:i])
            if marker==0xD9: break
            continue
        if i+2>len(data): raise ValueError("truncated JPEG segment length")
        length=int.from_bytes(data[i:i+2],"big")
        end=i+length
        if length<2 or end>len(data): raise ValueError("invalid JPEG segment length")
        if marker in REMOVE: removed.append(NAMES[marker])
        else: out.extend(data[start:end])
        i=end
        if marker==0xDA:
            out.extend(data[i:]); break
    return bytes(out),removed

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__); p.add_argument("input",type=Path); p.add_argument("--output",type=Path,required=True)
    a=p.parse_args(argv)
    try:
        cleaned,removed=strip_metadata(a.input.read_bytes()); a.output.write_bytes(cleaned)
    except (OSError,ValueError) as exc: p.error(str(exc))
    print(json.dumps({"output":str(a.output),"removed":removed},indent=2))
    return 0
if __name__=="__main__": raise SystemExit(main())
