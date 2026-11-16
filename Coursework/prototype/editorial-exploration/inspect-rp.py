"""Read-only survey of gzip members in an Axure RP file; never modifies input."""
from pathlib import Path
import argparse
import zlib

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=Path)
    args = parser.parse_args()
    data = args.file.read_bytes()
    pos = count = 0
    print(f'file={args.file} size={len(data)} bytes magic={data[:8].hex()}')
    while (pos := data.find(b'\x1f\x8b\x08', pos)) != -1:
        try:
            decoder = zlib.decompressobj(31)
            decoded = decoder.decompress(data[pos:], 20_000_001)
            if not decoder.eof or len(decoded) > 20_000_000:
                pos += 3
                continue
            used = len(data) - pos - len(decoder.unused_data)
            prefix = decoded[:256]
            kind = next((s.decode('ascii') for s in prefix.split(b'\x00') if s.startswith(b'Axure:')), '?')
            print(f'offset={pos} compressed={used} decoded={len(decoded)} kind={kind}')
            count += 1
            pos += used
        except zlib.error:
            pos += 3
    print(f'gzip_members={count}')

if __name__ == '__main__':
    main()
