import pytest

from app.services.source_recognizer import (
    Capability,
    Platform,
    SourceRecognitionError,
    inspect_source,
    normalize_source_url,
)


def test_recognizes_youtube_video() -> None:
    result = inspect_source(
        "https://www.youtube.com/watch?v=test123"
    )

    assert result.platform is Platform.YOUTUBE
    assert result.content_kind == "video"
    assert result.requires_probe is True
    assert (
        result.capability
        is Capability.YT_DLP_KNOWN_EXTRACTOR
    )


def test_recognizes_youtube_short() -> None:
    result = inspect_source(
        "https://youtube.com/shorts/test123"
    )

    assert result.platform is Platform.YOUTUBE
    assert result.content_kind == "short"


def test_recognizes_instagram_reel() -> None:
    result = inspect_source(
        "https://www.instagram.com/reel/test123/"
    )

    assert result.platform is Platform.INSTAGRAM
    assert result.content_kind == "reel"
    assert result.authentication_may_be_required is True


def test_recognizes_pinterest_but_requires_probe() -> None:
    result = inspect_source(
        "https://www.pinterest.com/pin/123456/"
    )

    assert result.platform is Platform.PINTEREST
    assert result.content_kind == "pin"
    assert result.requires_probe is True
    assert (
        result.capability
        is Capability.YT_DLP_PROBE_REQUIRED
    )


def test_recognizes_direct_webp() -> None:
    result = inspect_source(
        "https://cdn.example.com/images/photo.webp"
    )

    assert result.platform is Platform.DIRECT_MEDIA
    assert result.input_type == "direct_file"
    assert result.content_kind == "image"
    assert result.detected_extension == ".webp"
    assert result.webp_conversion_available is True
    assert (
        result.capability
        is Capability.DIRECT_DOWNLOAD
    )


def test_generic_site_requires_probe() -> None:
    result = inspect_source(
        "https://media.example.com/article/123"
    )

    assert result.platform is Platform.GENERIC
    assert result.requires_probe is True
    assert (
        result.capability
        is Capability.GENERIC_PROBE_REQUIRED
    )


@pytest.mark.parametrize(
    "url",
    [
        "http://localhost/video",
        "http://127.0.0.1/video",
        "http://10.0.0.1/video",
        "http://169.254.169.254/latest/meta-data",
        "http://192.168.1.10/video",
        "http://[::1]/video",
    ],
)
def test_rejects_private_or_local_urls(
    url: str,
) -> None:
    with pytest.raises(SourceRecognitionError):
        inspect_source(url)


def test_adds_https_when_scheme_is_missing() -> None:
    normalized_url, hostname = normalize_source_url(
        "youtu.be/test123"
    )

    assert normalized_url == "https://youtu.be/test123"
    assert hostname == "youtu.be"


def test_removes_url_fragment() -> None:
    normalized_url, _ = normalize_source_url(
        "https://example.com/video#tracking"
    )

    assert normalized_url == "https://example.com/video"


def test_rejects_nonstandard_port_by_default() -> None:
    with pytest.raises(SourceRecognitionError):
        normalize_source_url(
            "https://example.com:8443/video"
        )

