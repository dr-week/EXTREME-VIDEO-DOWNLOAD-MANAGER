from pathlib import Path

import pytest
from PIL import Image

from app.services.image_converter import (
    ImageConversionError,
    convert_webp,
    pillow_has_webp_support,
)


pytestmark = pytest.mark.skipif(
    not pillow_has_webp_support(),
    reason="Pillow WebP support is unavailable.",
)


def create_rgb_webp(path: Path) -> None:
    image = Image.new(
        "RGB",
        (32, 24),
        (40, 80, 120),
    )

    image.save(
        path,
        format="WEBP",
        quality=90,
    )


def create_transparent_webp(path: Path) -> None:
    image = Image.new(
        "RGBA",
        (32, 24),
        (40, 80, 120, 100),
    )

    image.save(
        path,
        format="WEBP",
        lossless=True,
    )


def test_auto_converts_opaque_webp_to_jpeg(
    tmp_path: Path,
) -> None:
    source = tmp_path / "photo.webp"
    create_rgb_webp(source)

    result = convert_webp(source)

    output = Path(result.output_path)

    assert output.exists()
    assert output.suffix == ".jpg"
    assert result.output_format == "JPEG"
    assert source.exists()
    assert result.source_deleted is False


def test_auto_converts_transparent_webp_to_png(
    tmp_path: Path,
) -> None:
    source = tmp_path / "transparent.webp"
    create_transparent_webp(source)

    result = convert_webp(source)

    output = Path(result.output_path)

    assert output.exists()
    assert output.suffix == ".png"
    assert result.output_format == "PNG"
    assert source.exists()


def test_explicit_png_conversion(
    tmp_path: Path,
) -> None:
    source = tmp_path / "photo.webp"
    create_rgb_webp(source)

    result = convert_webp(
        source,
        target_format="png",
    )

    assert Path(result.output_path).suffix == ".png"
    assert result.output_format == "PNG"


def test_does_not_overwrite_by_default(
    tmp_path: Path,
) -> None:
    source = tmp_path / "photo.webp"
    existing = tmp_path / "photo.jpg"

    create_rgb_webp(source)
    existing.write_bytes(b"existing")

    with pytest.raises(ImageConversionError):
        convert_webp(source)


def test_can_overwrite_when_explicitly_enabled(
    tmp_path: Path,
) -> None:
    source = tmp_path / "photo.webp"
    existing = tmp_path / "photo.jpg"

    create_rgb_webp(source)
    existing.write_bytes(b"existing")

    result = convert_webp(
        source,
        overwrite=True,
    )

    assert Path(result.output_path).stat().st_size > 8


def test_rejects_non_webp_content(
    tmp_path: Path,
) -> None:
    source = tmp_path / "fake.webp"

    Image.new(
        "RGB",
        (16, 16),
        (255, 255, 255),
    ).save(
        source,
        format="PNG",
    )

    with pytest.raises(ImageConversionError):
        convert_webp(source)


def test_deletes_source_only_when_requested(
    tmp_path: Path,
) -> None:
    source = tmp_path / "photo.webp"
    create_rgb_webp(source)

    result = convert_webp(
        source,
        delete_source=True,
    )

    assert result.source_deleted is True
    assert not source.exists()
    assert Path(result.output_path).exists()

