from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
import ipaddress
from pathlib import PurePosixPath
import socket
from typing import Final
from urllib.parse import parse_qs, urlsplit, urlunsplit


class SourceRecognitionError(ValueError):
    """Raised when a source URL is invalid or unsafe."""


class Platform(str, Enum):
    YOUTUBE = "youtube"
    INSTAGRAM = "instagram"
    PINTEREST = "pinterest"
    TIKTOK = "tiktok"
    FACEBOOK = "facebook"
    X_TWITTER = "x_twitter"
    VIMEO = "vimeo"
    DAILYMOTION = "dailymotion"
    REDDIT = "reddit"
    SOUNDCLOUD = "soundcloud"
    TWITCH = "twitch"
    DIRECT_MEDIA = "direct_media"
    GENERIC = "generic"


class Capability(str, Enum):
    DIRECT_DOWNLOAD = "direct_download"
    YT_DLP_KNOWN_EXTRACTOR = "yt_dlp_known_extractor"
    YT_DLP_PROBE_REQUIRED = "yt_dlp_probe_required"
    GENERIC_PROBE_REQUIRED = "generic_probe_required"


_IMAGE_EXTENSIONS: Final[set[str]] = {
    ".avif",
    ".bmp",
    ".gif",
    ".heic",
    ".jpeg",
    ".jpg",
    ".png",
    ".tif",
    ".tiff",
    ".webp",
}

_VIDEO_EXTENSIONS: Final[set[str]] = {
    ".avi",
    ".m4v",
    ".mkv",
    ".mov",
    ".mp4",
    ".mpeg",
    ".mpg",
    ".webm",
}

_AUDIO_EXTENSIONS: Final[set[str]] = {
    ".aac",
    ".flac",
    ".m4a",
    ".mp3",
    ".ogg",
    ".opus",
    ".wav",
    ".wma",
}

_PLATFORM_DOMAINS: Final[dict[Platform, tuple[str, ...]]] = {
    Platform.YOUTUBE: (
        "youtube.com",
        "youtu.be",
        "youtube-nocookie.com",
    ),
    Platform.INSTAGRAM: (
        "instagram.com",
        "instagr.am",
    ),
    Platform.PINTEREST: (
        "pinterest.com",
        "pin.it",
        "pinterest.ca",
        "pinterest.co.uk",
        "pinterest.com.au",
        "pinterest.de",
        "pinterest.fr",
        "pinterest.es",
        "pinterest.it",
        "pinterest.jp",
        "pinterest.com.mx",
        "pinterest.pt",
        "pinterest.se",
        "pinterest.ch",
        "pinterest.at",
        "pinterest.dk",
        "pinterest.ie",
        "pinterest.nz",
        "pinterest.ph",
        "pinterest.cl",
    ),
    Platform.TIKTOK: (
        "tiktok.com",
        "vm.tiktok.com",
    ),
    Platform.FACEBOOK: (
        "facebook.com",
        "fb.watch",
    ),
    Platform.X_TWITTER: (
        "x.com",
        "twitter.com",
        "t.co",
    ),
    Platform.VIMEO: (
        "vimeo.com",
        "player.vimeo.com",
    ),
    Platform.DAILYMOTION: (
        "dailymotion.com",
        "dai.ly",
    ),
    Platform.REDDIT: (
        "reddit.com",
        "redd.it",
        "v.redd.it",
    ),
    Platform.SOUNDCLOUD: (
        "soundcloud.com",
    ),
    Platform.TWITCH: (
        "twitch.tv",
        "clips.twitch.tv",
    ),
}

_KNOWN_YT_DLP_PLATFORMS: Final[set[Platform]] = {
    Platform.YOUTUBE,
    Platform.INSTAGRAM,
    Platform.TIKTOK,
    Platform.FACEBOOK,
    Platform.X_TWITTER,
    Platform.VIMEO,
    Platform.DAILYMOTION,
    Platform.REDDIT,
    Platform.SOUNDCLOUD,
    Platform.TWITCH,
}

_AUTH_LIKELY_PLATFORMS: Final[set[Platform]] = {
    Platform.INSTAGRAM,
    Platform.FACEBOOK,
    Platform.TIKTOK,
}

_BLOCKED_HOSTS: Final[set[str]] = {
    "localhost",
    "localhost.localdomain",
    "metadata",
    "metadata.google.internal",
}


@dataclass(frozen=True, slots=True)
class SourceInfo:
    original_url: str
    normalized_url: str
    hostname: str
    platform: Platform
    display_name: str
    input_type: str
    content_kind: str
    capability: Capability
    requires_probe: bool
    authentication_may_be_required: bool
    detected_extension: str | None
    webp_conversion_available: bool
    note: str

    def to_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["platform"] = self.platform.value
        data["capability"] = self.capability.value
        return data


def _host_matches(hostname: str, domain: str) -> bool:
    return hostname == domain or hostname.endswith(f".{domain}")


def _platform_for_host(hostname: str) -> Platform:
    for platform, domains in _PLATFORM_DOMAINS.items():
        if any(_host_matches(hostname, domain) for domain in domains):
            return platform

    return Platform.GENERIC


def _direct_media_kind(extension: str) -> str | None:
    if extension in _IMAGE_EXTENSIONS:
        return "image"

    if extension in _VIDEO_EXTENSIONS:
        return "video"

    if extension in _AUDIO_EXTENSIONS:
        return "audio"

    return None


def _content_kind(
    platform: Platform,
    hostname: str,
    path: str,
    query: str,
    direct_kind: str | None,
) -> str:
    if direct_kind:
        return direct_kind

    lowered_path = path.lower()
    query_values = parse_qs(query)

    if platform is Platform.YOUTUBE:
        if "/shorts/" in lowered_path:
            return "short"

        if "list" in query_values or "/playlist" in lowered_path:
            return "playlist"

        if hostname == "youtu.be" or "/watch" in lowered_path:
            return "video"

        return "youtube_page"

    if platform is Platform.INSTAGRAM:
        if "/reel/" in lowered_path or "/reels/" in lowered_path:
            return "reel"

        if "/stories/" in lowered_path:
            return "story"

        if "/p/" in lowered_path:
            return "post"

        return "instagram_page"

    if platform is Platform.PINTEREST:
        if "/pin/" in lowered_path:
            return "pin"

        return "pinterest_page"

    if platform is Platform.TIKTOK:
        return "short_video"

    if platform is Platform.SOUNDCLOUD:
        return "audio_page"

    if platform is Platform.TWITCH:
        if "/videos/" in lowered_path:
            return "video"

        if "clips.twitch.tv" in hostname or "/clip/" in lowered_path:
            return "clip"

        return "stream_or_channel"

    return "media_page"


def _display_name(
    platform: Platform,
    hostname: str,
) -> str:
    names = {
        Platform.YOUTUBE: "YouTube",
        Platform.INSTAGRAM: "Instagram",
        Platform.PINTEREST: "Pinterest",
        Platform.TIKTOK: "TikTok",
        Platform.FACEBOOK: "Facebook",
        Platform.X_TWITTER: "X / Twitter",
        Platform.VIMEO: "Vimeo",
        Platform.DAILYMOTION: "Dailymotion",
        Platform.REDDIT: "Reddit",
        Platform.SOUNDCLOUD: "SoundCloud",
        Platform.TWITCH: "Twitch",
        Platform.DIRECT_MEDIA: "Direct media file",
        Platform.GENERIC: hostname,
    }

    return names[platform]


def _validate_hostname(hostname: str) -> str:
    try:
        ascii_hostname = (
            hostname
            .rstrip(".")
            .encode("idna")
            .decode("ascii")
            .lower()
        )
    except UnicodeError as exc:
        raise SourceRecognitionError(
            "The URL hostname is invalid."
        ) from exc

    if not ascii_hostname:
        raise SourceRecognitionError(
            "The URL must contain a hostname."
        )

    if (
        ascii_hostname in _BLOCKED_HOSTS
        or ascii_hostname.endswith(".localhost")
        or ascii_hostname.endswith(".local")
        or ascii_hostname.endswith(".internal")
    ):
        raise SourceRecognitionError(
            "Local or internal network URLs are not allowed."
        )

    try:
        address = ipaddress.ip_address(
            ascii_hostname.strip("[]")
        )
    except ValueError:
        return ascii_hostname

    if not address.is_global:
        raise SourceRecognitionError(
            "Private, loopback, reserved, or link-local "
            "IP URLs are not allowed."
        )

    return ascii_hostname


def resolve_and_validate_public_host(
    hostname: str,
) -> tuple[str, ...]:
    """
    Resolve a hostname and reject non-public destinations.

    Call this immediately before network access.

    Deployment-level egress restrictions are still required because
    redirects and DNS rebinding cannot be completely prevented through
    application checks alone.
    """

    validated_hostname = _validate_hostname(hostname)

    try:
        results = socket.getaddrinfo(
            validated_hostname,
            None,
            type=socket.SOCK_STREAM,
        )
    except socket.gaierror as exc:
        raise SourceRecognitionError(
            "The source hostname could not be resolved."
        ) from exc

    seen: set[str] = set()

    for result in results:
        addr = str(result[4][0])
        seen.add(addr)

    addresses = sorted(seen)

    if not addresses:
        raise SourceRecognitionError(
            "The source hostname did not resolve to an address."
        )

    for raw_address in addresses:
        address = ipaddress.ip_address(raw_address)

        if not address.is_global:
            raise SourceRecognitionError(
                "The source hostname resolves to a private, "
                "loopback, reserved, or link-local address."
            )

    return tuple(addresses)


def normalize_source_url(
    value: str,
    *,
    allow_nonstandard_port: bool = False,
) -> tuple[str, str]:
    raw = value.strip()

    if not raw:
        raise SourceRecognitionError(
            "A URL is required."
        )

    if raw.startswith("//"):
        raw = f"https:{raw}"
    elif "://" not in raw:
        raw = f"https://{raw}"

    parsed = urlsplit(raw)

    if parsed.scheme.lower() not in {"http", "https"}:
        raise SourceRecognitionError(
            "Only HTTP and HTTPS URLs are supported."
        )

    if (
        parsed.username is not None
        or parsed.password is not None
    ):
        raise SourceRecognitionError(
            "URLs containing usernames or passwords are not allowed."
        )

    if parsed.hostname is None:
        raise SourceRecognitionError(
            "The URL must contain a hostname."
        )

    hostname = _validate_hostname(parsed.hostname)

    try:
        port = parsed.port
    except ValueError as exc:
        raise SourceRecognitionError(
            "The URL contains an invalid port."
        ) from exc

    if (
        port is not None
        and port not in {80, 443}
        and not allow_nonstandard_port
    ):
        raise SourceRecognitionError(
            "Only standard HTTP and HTTPS ports are allowed."
        )

    safe_host = (
        f"[{hostname}]"
        if ":" in hostname
        else hostname
    )

    netloc = (
        safe_host
        if port is None
        else f"{safe_host}:{port}"
    )

    path = parsed.path or "/"

    normalized_url = urlunsplit(
        (
            parsed.scheme.lower(),
            netloc,
            path,
            parsed.query,
            "",
        )
    )

    return normalized_url, hostname


def inspect_source(value: str) -> SourceInfo:
    normalized_url, hostname = normalize_source_url(value)
    parsed = urlsplit(normalized_url)

    extension = (
        PurePosixPath(parsed.path).suffix.lower()
        or None
    )

    direct_kind = _direct_media_kind(
        extension or ""
    )

    detected_platform = _platform_for_host(hostname)

    platform = (
        Platform.DIRECT_MEDIA
        if direct_kind
        else detected_platform
    )

    if direct_kind:
        capability = Capability.DIRECT_DOWNLOAD
        requires_probe = False
        note = (
            "Direct media URL detected. Validate response "
            "headers before saving."
        )

    elif detected_platform in _KNOWN_YT_DLP_PLATFORMS:
        capability = Capability.YT_DLP_KNOWN_EXTRACTOR
        requires_probe = True
        note = (
            "Recognized platform. Run a yt-dlp metadata probe "
            "because extractor availability, authentication, "
            "and page support can change."
        )

    elif detected_platform is Platform.PINTEREST:
        capability = Capability.YT_DLP_PROBE_REQUIRED
        requires_probe = True
        note = (
            "Pinterest is recognized, but support must be tested "
            "dynamically. Do not promise that every pin or board "
            "can be downloaded."
        )

    else:
        capability = Capability.GENERIC_PROBE_REQUIRED
        requires_probe = True
        note = (
            "Unknown domain. Try the yt-dlp generic extractor "
            "without claiming support before the probe succeeds."
        )

    content_kind = _content_kind(
        detected_platform,
        hostname,
        parsed.path,
        parsed.query,
        direct_kind,
    )

    return SourceInfo(
        original_url=value,
        normalized_url=normalized_url,
        hostname=hostname,
        platform=platform,
        display_name=_display_name(
            platform,
            hostname,
        ),
        input_type=(
            "direct_file"
            if direct_kind
            else "page_url"
        ),
        content_kind=content_kind,
        capability=capability,
        requires_probe=requires_probe,
        authentication_may_be_required=(
            detected_platform
            in _AUTH_LIKELY_PLATFORMS
        ),
        detected_extension=extension,
        webp_conversion_available=(
            extension == ".webp"
        ),
        note=note,
    )

