#!/usr/bin/env python3
"""Local, non-diagnostic capture intake for the spa visualization experiment."""
import argparse
import hashlib
import json
import re
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps, UnidentifiedImageError

VERSION = '0.1.0'
SAFE_ID = re.compile(r'^[A-Za-z0-9_-]{1,64}$')

class IntakeError(Exception):
    pass

def load_json(path):
    try:
        with path.open(encoding='utf-8') as f:
            data = json.load(f)
        if not isinstance(data, dict):
            raise ValueError('expected an object')
        return data
    except (OSError, ValueError) as e:
        raise IntakeError(f'Cannot read {path}: {e}') from e

def required(obj, key):
    value = obj.get(key)
    if not isinstance(value, str) or not value.strip():
        raise IntakeError(f'Missing {key}')
    return value.strip()

def timestamp(value, label):
    try:
        parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
        if parsed.tzinfo is None:
            raise ValueError('timezone required')
        return parsed
    except ValueError as e:
        raise IntakeError(f'{label}: use ISO 8601 with timezone') from e

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def intake(manifest_path, profile_path, output_root):
    started = time.monotonic()
    manifest_path, profile_path, output_root = map(Path, (manifest_path, profile_path, output_root))
    m, p = load_json(manifest_path), load_json(profile_path)
    session_id = required(m, 'session_id')
    if not SAFE_ID.fullmatch(session_id):
        raise IntakeError('session_id must contain only letters, numbers, underscores or hyphens')
    profile_id = required(p, 'profile_id')
    profile_version = required(p, 'version')
    if required(m, 'profile_id') != profile_id or required(m, 'profile_version') != profile_version:
        raise IntakeError('Session and device profile do not match')
    if m.get('consent_recorded') is not True:
        raise IntakeError('Record consent before processing photographs')
    if m.get('water_present') is not True:
        raise IntakeError('This intake requires a water-present capture')
    side, body_part = required(m, 'side'), required(m, 'body_part')
    if side not in ('left', 'right'):
        raise IntakeError('side must be left or right')
    required(p, 'water_condition'); required(p, 'window_condition'); required(p, 'calibration_reference')
    cameras, captures = p.get('camera_ids'), m.get('captures')
    if not isinstance(cameras, list) or not cameras or any(not isinstance(c, str) or not SAFE_ID.fullmatch(c) for c in cameras) or len(set(cameras)) != len(cameras):
        raise IntakeError('profile camera_ids must be unique safe IDs')
    if not isinstance(captures, list) or len(captures) != len(cameras) or any(not isinstance(c, dict) for c in captures):
        raise IntakeError('Provide exactly one capture per profile camera')
    camera_ids = [required(c, 'camera_id') for c in captures]
    if len(set(camera_ids)) != len(camera_ids) or set(camera_ids) != set(cameras):
        raise IntakeError('Capture camera IDs must match profile exactly')
    if any(required(c, 'session_id') != session_id or required(c, 'side') != side or required(c, 'body_part') != body_part for c in captures):
        raise IntakeError('Capture session, side or body part does not match')
    target = output_root / session_id
    if target.exists():
        raise IntakeError(f'Session already exists: {target}; originals will not be overwritten')
    # Validate everything possible before creating the session directory.
    checked, hashes = [], set()
    for c in captures:
        captured_at = required(c, 'captured_at')
        timestamp(captured_at, 'captured_at')
        source = (manifest_path.parent / required(c, 'file')).resolve()
        if not source.is_file():
            raise IntakeError(f'Image not found: {source}')
        try:
            with Image.open(source) as image:
                image.verify()
            with Image.open(source) as image:
                if image.format not in ('JPEG', 'PNG'):
                    raise IntakeError(f'Unsupported image format: {source.name}')
                size, fmt = list(ImageOps.exif_transpose(image).size), image.format
        except (UnidentifiedImageError, OSError, ValueError) as e:
            raise IntakeError(f'Unreadable image: {source.name}') from e
        h = digest(source)
        if h in hashes:
            raise IntakeError('Duplicate image content across cameras')
        hashes.add(h)
        checked.append((c, source, h, size, fmt))
    target.mkdir(parents=True, exist_ok=False)
    try:
        originals = target / 'originals'; originals.mkdir()
        tiles = []
        inputs = []
        for c, source, h, size, fmt in checked:
            ext = '.jpg' if fmt == 'JPEG' else '.png'
            dest = originals / (c['camera_id'] + ext)
            shutil.copyfile(source, dest)
            if digest(dest) != h:
                raise OSError('Copied image hash mismatch')
            with Image.open(dest) as image:
                thumb = ImageOps.exif_transpose(image).convert('RGB')
                thumb.thumbnail((600, 450))
                tile = Image.new('RGB', (640, 500), 'white')
                tile.paste(thumb, ((640-thumb.width)//2, 30 + (450-thumb.height)//2))
                ImageDraw.Draw(tile).text((15, 8), c['camera_id'], fill='black')
                tiles.append(tile)
            inputs.append({'camera_id': c['camera_id'], 'captured_at': c['captured_at'], 'original': str(dest.relative_to(target)), 'sha256': h, 'dimensions': size})
        sheet = Image.new('RGB', (1280, ((len(tiles)+1)//2)*500), '#ddd')
        for i, tile in enumerate(tiles):
            sheet.paste(tile, ((i%2)*640, (i//2)*500))
        sheet.save(target / 'contact-sheet.jpg', quality=90)
        result = {'session_id': session_id, 'status': 'input_review_required', 'failure_code': None,
                  'message': 'Input registered; human review required. No anatomy generated or diagnosis performed.',
                  'profile_id': profile_id, 'profile_version': profile_version,
                  'profile_sha256': digest(profile_path), 'side': side, 'body_part': body_part,
                  'water_present': True, 'captures': inputs, 'outputs': ['contact-sheet.jpg'],
                  'software_version': VERSION, 'retry_count': 0, 'manual_edit_count': 0,
                  'elapsed_seconds': round(time.monotonic()-started, 3),
                  'created_at': datetime.now(timezone.utc).isoformat()}
        (target / 'result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        shutil.copyfile(profile_path, target / 'device-profile.json')
        return target
    except Exception:
        # Keep partially written originals for investigation; never present them as success.
        (target / 'FAILED.txt').write_text('Intake failed; inspect this directory before retrying.\n', encoding='utf-8')
        raise

def main():
    parser = argparse.ArgumentParser(description='Register water-present multi-camera captures for manual review; no diagnostic output.')
    parser.add_argument('--manifest', required=True, type=Path)
    parser.add_argument('--profile', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    try:
        target = intake(args.manifest, args.profile, args.output)
        print(f'Input registered for review: {target}')
    except (IntakeError, OSError) as e:
        print(f'Intake failed: {e}', file=sys.stderr)
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())
