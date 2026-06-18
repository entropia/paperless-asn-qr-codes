# pylint: disable=R0801
"""Blackbox-like testing of the paperless-asn-qrcode cli tool"""

import shutil
import magic

from cli_test_helpers import shell


def test_entrypoint():
    """Is entrypoint script installed? (pyproject.toml)"""
    assert shutil.which("paperless-asn-qr-code")


def test_help():
    """Does the help command work?"""
    result = shell("paperless-asn-qr-code --help")
    assert result.exit_code == 0
    assert "usage:" in result.stdout


def test_empty():
    """Does the command fails with no arguments?"""
    result = shell("paperless-asn-qr-code")
    assert result.exit_code == 2
    assert "usage:" in result.stderr


def test_new_file(tmp_path):
    """Does the command create a new pdf file with labels content?"""
    pdffile = tmp_path / "labels.pdf"
    result = shell(f"paperless-asn-qr-code 0 {pdffile}")
    assert result.exit_code == 0
    assert pdffile.exists()
    # test pdffile size is greater 10000 bytes
    assert pdffile.stat().st_size > 10000
    assert magic.Magic(mime=True).from_file(pdffile) == "application/pdf"