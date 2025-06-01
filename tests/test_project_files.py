import pytest
import importlib.util

def test_requirements_file_exists():
    with open('requirements.txt') as f:
        lines = f.readlines()
    assert any('flet' in line for line in lines)

def test_pyproject_toml_exists():
    with open('pyproject.toml') as f:
        content = f.read()
    assert '[project]' in content or '[tool.poetry]' in content
