from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.services.template_service import TemplateService
from app.utils.validators import validate_pptx, validate_topic

TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


# ── TemplateService ──────────────────────────────────────────────────────────

def test_create_and_get_template(db):
    from app.api.schemas import TemplateCreate

    svc = TemplateService(db)
    payload = TemplateCreate(name="my_tmpl", description="desc", config={"k": "v"})
    created = svc.create_template(payload)
    assert created.id is not None

    fetched = svc.get_template(created.id)
    assert fetched is not None
    assert fetched.name == "my_tmpl"


def test_delete_template(db):
    from app.api.schemas import TemplateCreate

    svc = TemplateService(db)
    payload = TemplateCreate(name="delete_me", config={})
    created = svc.create_template(payload)

    assert svc.delete_template(created.id) is True
    assert svc.get_template(created.id) is None


def test_delete_nonexistent_template(db):
    svc = TemplateService(db)
    assert svc.delete_template(9999) is False


def test_load_builtin_default(db):
    svc = TemplateService(db)
    config = svc.load_builtin("default_template")
    assert "colors" in config


def test_load_builtin_missing(db):
    svc = TemplateService(db)
    with pytest.raises(FileNotFoundError):
        svc.load_builtin("nonexistent_template")


# ── Validators ───────────────────────────────────────────────────────────────

def test_validate_pptx_valid():
    assert validate_pptx("presentation.pptx") is True


def test_validate_pptx_invalid():
    assert validate_pptx("document.pdf") is False
    assert validate_pptx(None) is False
    assert validate_pptx("") is False


def test_validate_topic_valid():
    assert validate_topic("AI in Healthcare") is True


def test_validate_topic_empty():
    assert validate_topic("") is False
    assert validate_topic("   ") is False


def test_validate_topic_too_long():
    assert validate_topic("a" * 501) is False
