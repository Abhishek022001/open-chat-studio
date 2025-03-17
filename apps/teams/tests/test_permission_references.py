import os
import re
import subprocess

import pytest
from django.conf import settings

from apps.teams.backends import CONTENT_TYPES

PERM_NAME_GREEDY_REGEX = r".*\.{}_.*"
PERM_NAME_REGEX = r"[a-z_A-Z]*\.{}_.*?"


def test_permission_references():
    """Check that all permissions referenced in the codebase are valid."""
    permission_references = get_all_permission_references()
    assert permission_references, "No permission references found"
    assert "fake_app.view_model" in permission_references, "Expected to find 'fake_app' in permission references"
    for permission in permission_references:
        app_label, code = permission.split(".")
        if app_label == "fake_app":
            continue
        assert app_label in CONTENT_TYPES, "Unknown app label in permission"
        _, model_name = code.split("_")
        assert model_name in CONTENT_TYPES[app_label], "Unknown model name in permission"


@pytest.mark.parametrize(
    ("perm_type", "lines", "expected"),
    [
        # return unique
        ("view", ['"fake_app.view_model"', '"fake_app.view_model"'], {"fake_app.view_model"}),
        # find multiple on same line
        (
            "change",
            ['"fake_app.change_model" with another "fake_app.change_other"'],
            {"fake_app.change_model", "fake_app.change_other"},
        ),
        # find multiple on different lines
        (
            "delete",
            ['"fake_app.delete_model"', '"fake_app.delete_other"'],
            {"fake_app.delete_model", "fake_app.delete_other"},
        ),
    ],
)
def test_get_permissions_from_lines(perm_type, lines, expected):
    output = _get_permissions_from_lines(perm_type, lines)
    assert output == expected


def get_all_permission_references():
    permissions = set()
    for perm_type in ["view", "change", "delete", "add"]:
        permissions |= _get_permission_references(perm_type)
    return permissions


def _get_permission_references(perm_type):
    lines = _get_lines_with_permission(perm_type)
    return _get_permissions_from_lines(perm_type, lines)


def _get_permissions_from_lines(perm_type: str, lines: list[str]) -> set[str]:
    permissions = set()
    name_rx = PERM_NAME_REGEX.format(perm_type)
    name_extract_rx = re.compile(f'"({name_rx})"')
    for line in lines:
        if line:
            matches = name_extract_rx.findall(line)
            permissions.update(matches)
    return permissions


def _get_lines_with_permission(perm_type):
    permissions = set()
    pattern = re.compile(rf'".*\.{perm_type}_.*"')

    for root, _, files in os.walk("apps"):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        if pattern.search(line):
                            permissions.add(line.strip())

    return list(permissions)
