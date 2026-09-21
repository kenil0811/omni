#!/usr/bin/env python3
"""Read and verify an Alpha document snapshot. Python standard library only."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent


def load_manifest(root):
    data = json.loads((root / 'SNAPSHOT_MANIFEST.json').read_text(encoding='utf-8'))
    if data.get('format_version') != 1:
        raise ValueError('Unsupported snapshot manifest version')
    return data


def safe_path(root, relative):
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()) or Path(relative).is_absolute():
        raise ValueError('Path escapes the snapshot: ' + relative)
    return path


def sha256(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def source_digest(sources):
    identity = [{'canonical_path': s['canonical_path'], 'sha256': s['sha256']}
                for s in sorted(sources, key=lambda s: s['canonical_path'])]
    return hashlib.sha256(json.dumps(identity, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def source_entries(manifest, area=None):
    entries = manifest['sources']
    return [s for s in entries if not area or s['area'] == area]


def verify(root, manifest):
    errors = []
    payload = {}
    for item in manifest['files']:
        rel = item['path']
        if rel in payload:
            errors.append('Duplicate payload entry: ' + rel)
            continue
        payload[rel] = item
        try:
            path = safe_path(root, rel)
            if not path.is_file():
                errors.append('Missing file: ' + rel)
            elif path.stat().st_size != item['size_bytes'] or sha256(path) != item['sha256']:
                errors.append('Content mismatch: ' + rel)
        except (OSError, ValueError) as exc:
            errors.append(str(exc))
    seen = set()
    for item in manifest['sources']:
        if item['canonical_path'] in seen:
            errors.append('Duplicate source: ' + item['canonical_path'])
        seen.add(item['canonical_path'])
        actual = payload.get(item['path'])
        if not actual or actual['sha256'] != item['sha256'] or actual['size_bytes'] != item['size_bytes']:
            errors.append('Source/payload mismatch: ' + item['path'])
        for ref in [item.get('text_path'), *item.get('visual_pages', []), item.get('archive_index_path')]:
            if ref and ref not in payload:
                errors.append('Missing companion declaration: ' + ref)
    if len(manifest['sources']) != manifest['source_count']:
        errors.append('Source count mismatch')
    if source_digest(manifest['sources']) != manifest['source_digest_sha256']:
        errors.append('Source identity digest mismatch')
    if errors:
        for error in errors:
            print('FAIL: ' + error, file=sys.stderr)
        return 1
    print('Verified {} source files and {} total payload files.'.format(len(manifest['sources']), len(payload)))
    print('Snapshot: ' + manifest['snapshot_id'])
    print('This verifies local integrity, not live freshness or a cryptographic signature.')
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('verify', help='Check every included source and companion hash')
    listing = commands.add_parser('list', help='List sources and optional area')
    listing.add_argument('--area', choices=['project', 'product', 'architecture', 'specifications', 'delivery', 'research'])
    search = commands.add_parser('search', help='Literal search of original or extracted source text')
    search.add_argument('query')
    search.add_argument('--area', choices=['project', 'product', 'architecture', 'specifications', 'delivery', 'research'])
    search.add_argument('--limit', type=int, default=30)
    search.add_argument('--case-sensitive', action='store_true')
    read = commands.add_parser('read', help='Read a source file or its text companion with line numbers')
    read.add_argument('path', help='For example alpha/architecture/Implementation Blueprint.md')
    read.add_argument('--start', type=int, default=1)
    read.add_argument('--lines', type=int, default=120)
    changes = commands.add_parser('changes', help='Compare this snapshot to another extracted snapshot')
    changes.add_argument('other', type=Path)
    args = parser.parse_args()
    try:
        manifest = load_manifest(ROOT)
        if args.command == 'verify':
            return verify(ROOT, manifest)
        if args.command == 'list':
            for entry in source_entries(manifest, args.area):
                print('{} | {} | {}'.format(entry['path'], entry['role'], entry['sha256'][:12]))
            return 0
        if args.command == 'read':
            if args.start < 1 or args.lines < 1:
                parser.error('--start and --lines must be positive')
            query = args.path.replace('\\', '/').lstrip('/')
            entry = next((s for s in manifest['sources'] if s['path'] == query), None)
            if entry is None:
                raise ValueError('Source not listed in this snapshot; use list: ' + args.path)
            rel = entry.get('text_path')
            if not rel:
                raise ValueError('No text companion; inspect original: ' + entry['path'])
            print('Source: {}\nSnapshot: {}\nSHA-256: {}'.format(entry['canonical_path'], manifest['snapshot_id'], entry['sha256']))
            if rel != entry['path']:
                print('Reading derived text: ' + rel + ' (inspect original for exact visuals/formatting)')
            lines = safe_path(ROOT, rel).read_text(encoding='utf-8').splitlines()
            for index in range(args.start - 1, min(len(lines), args.start - 1 + args.lines)):
                print('{}: {}'.format(index + 1, lines[index]))
            print('Displayed lines {}-{} of {}.'.format(args.start, min(len(lines), args.start - 1 + args.lines), len(lines)))
            return 0
        if args.command == 'search':
            if not args.query or args.limit < 1:
                parser.error('Use a non-empty query and positive --limit')
            query = args.query if args.case_sensitive else args.query.casefold()
            count = 0
            for entry in source_entries(manifest, args.area):
                rel = entry.get('text_path')
                if not rel:
                    continue
                for number, line in enumerate(safe_path(ROOT, rel).read_text(encoding='utf-8').splitlines(), 1):
                    haystack = line if args.case_sensitive else line.casefold()
                    if query in haystack:
                        print('{}:{}: {}'.format(entry['path'], number, line))
                        count += 1
                        if count >= args.limit:
                            print('Result limit reached; narrow --area or increase --limit.', file=sys.stderr)
                            return 0
            print('{} match(es).'.format(count), file=sys.stderr)
            return 0
        if args.command == 'changes':
            other = load_manifest(args.other.resolve())
            old = {s['canonical_path']: s['sha256'] for s in other['sources']}
            new = {s['canonical_path']: s['sha256'] for s in manifest['sources']}
            print('Other: {}\nThis: {}'.format(other['snapshot_id'], manifest['snapshot_id']))
            count = 0
            for path in sorted(set(old) | set(new)):
                if old.get(path) == new.get(path):
                    continue
                status = 'ADDED' if path not in old else ('REMOVED' if path not in new else 'CHANGED')
                print(status + ': ' + path)
                count += 1
            print('{} source difference(s).'.format(count))
            return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print('Error: ' + str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
