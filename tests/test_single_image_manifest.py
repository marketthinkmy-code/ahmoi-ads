import json

from adbot.creative_groups import CAROUSEL, SINGLE_IMAGE
from adbot.drive_sync import load_units_from_manifest


def test_load_units_from_manifest_single_images(tmp_path):
    m = tmp_path / "manifest.json"
    m.write_text(json.dumps({"creatives": [
        {"content_id": "image_1", "file_id": "F1", "name": "Image 1：x"},
        {"content_id": "image_2", "file_id": "F2", "name": "Image 2：y", "kind": "single_image"},
        {"content_id": "image_1", "file_id": "DUP", "name": "dup"},  # de-duped by content_id
    ]}), encoding="utf-8")

    units = load_units_from_manifest(m)
    assert [u.content_id for u in units] == ["image_1", "image_2"]  # dup dropped, order kept
    assert units[0].kind == SINGLE_IMAGE
    assert units[0].assets[0].file_id == "F1"
    assert units[0].assets[0].mime == "image/png"  # default mime for a bare file_id
    # Asset filename is a clean, extensioned name (NOT the human label) so Meta /adimages
    # accepts the upload — a label without a .png would fail "type of file is not supported".
    assert units[0].assets[0].name == "image_1.png"


def test_load_units_from_manifest_carousel_files_list(tmp_path):
    m = tmp_path / "m.json"
    m.write_text(json.dumps({"creatives": [
        {"content_id": "carousel_1", "kind": "carousel", "files": [
            {"file_id": "A", "name": "1.png"}, {"file_id": "B", "name": "2.png"}]},
    ]}), encoding="utf-8")

    units = load_units_from_manifest(m)
    assert units[0].kind == CAROUSEL
    assert [a.file_id for a in units[0].assets] == ["A", "B"]
    assert [a.name for a in units[0].assets] == ["carousel_1_1.png", "carousel_1_2.png"]
