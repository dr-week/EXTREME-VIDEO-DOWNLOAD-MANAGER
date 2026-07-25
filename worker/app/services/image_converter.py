from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from uuid import uuid4

from PIL import (
    Image,
    ImageOps,
    ImageSequence,
    features,
)


class ImageConversionError(RuntimeError):
    """Raised when an image cannot be converted safely."""


@dataclass(frozen=True, slots=True)
class ConversionResult:
    source_path: str
    output_path: str
    source_format: str
    output_format: str
    animated: bool
    frame_count: int
    width: int
    height: int
    output_size_bytes: int
    source_deleted: bool

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


_FORMAT_ALIASES = {
    "auto": "AUTO",
    "png": "PNG",
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "gif": "GIF",
}

_FORMAT_SUFFIXES = {
    "PNG": ".png",
    "JPEG": ".jpg",
    "GIF": ".gif",
}


def pillow_has_webp_support() -> bool:
    try:
        return bool(
            features.check_module("webp")
        )
    except (ValueError, AttributeError):
        return bool(
            features.check("webp")
        )


def _has_alpha(image: Image.Image) -> bool:
    if image.mode in {"RGBA", "LA"}:
        return True

    return (
        image.mode == "P"
        and "transparency" in image.info
    )


def _normalize_target_format(value: str) -> str:
    normalized = value.strip().lower()

    try:
        return _FORMAT_ALIASES[normalized]
    except KeyError as exc:
        allowed = ", ".join(
            sorted(_FORMAT_ALIASES)
        )

        raise ImageConversionError(
            f"Unsupported target format '{value}'. "
            f"Allowed values: {allowed}."
        ) from exc


def _select_output_format(
    requested_format: str,
    *,
    animated: bool,
    has_alpha: bool,
) -> str:
    if requested_format != "AUTO":
        if (
            animated
            and requested_format in {"PNG", "JPEG"}
        ):
            raise ImageConversionError(
                "Animated WebP cannot be converted to PNG "
                "or JPEG without losing animation. Use "
                "target_format='gif' or 'auto'."
            )

        return requested_format

    if animated:
        return "GIF"

    if has_alpha:
        return "PNG"

    return "JPEG"


def _prepare_output_path(
    source: Path,
    output_format: str,
    output_path: str | Path | None,
) -> Path:
    suffix = _FORMAT_SUFFIXES[output_format]

    if output_path is None:
        return source.with_suffix(suffix)

    requested = Path(output_path).expanduser()

    if requested.suffix.lower() != suffix:
        requested = requested.with_suffix(suffix)

    return requested


def _save_animated_gif(
    image: Image.Image,
    temporary_output: Path,
) -> tuple[int, int, int]:
    frames: list[Image.Image] = []
    durations: list[int] = []

    for frame in ImageSequence.Iterator(image):
        rgba_frame = frame.convert("RGBA")

        palette_frame = rgba_frame.convert(
            "P",
            palette=Image.Palette.ADAPTIVE,
        )

        frames.append(palette_frame)

        durations.append(
            int(
                frame.info.get(
                    "duration",
                    image.info.get(
                        "duration",
                        100,
                    ),
                )
            )
        )

    if not frames:
        raise ImageConversionError(
            "The animated WebP contains no readable frames."
        )

    first_frame = frames[0]

    first_frame.save(
        temporary_output,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=int(
            image.info.get(
                "loop",
                0,
            )
        ),
        disposal=2,
        optimize=False,
    )

    width, height = first_frame.size

    return len(frames), width, height


def _save_static_image(
    image: Image.Image,
    output_format: str,
    temporary_output: Path,
    *,
    quality: int,
    jpeg_background: tuple[int, int, int],
) -> tuple[int, int, int]:
    static_image = ImageOps.exif_transpose(
        image.copy()
    )

    width, height = static_image.size

    if output_format == "PNG":
        static_image.save(
            temporary_output,
            format="PNG",
            optimize=True,
        )

    elif output_format == "JPEG":
        if _has_alpha(static_image):
            rgba_image = static_image.convert("RGBA")

            background = Image.new(
                "RGB",
                rgba_image.size,
                jpeg_background,
            )

            background.paste(
                rgba_image,
                mask=rgba_image.getchannel("A"),
            )

            output_image = background
        else:
            output_image = static_image.convert("RGB")

        output_image.save(
            temporary_output,
            format="JPEG",
            quality=quality,
            optimize=True,
            progressive=True,
        )

    elif output_format == "GIF":
        static_image.convert(
            "P",
            palette=Image.Palette.ADAPTIVE,
        ).save(
            temporary_output,
            format="GIF",
            optimize=True,
        )

    else:
        raise ImageConversionError(
            f"Unsupported output format: {output_format}"
        )

    return 1, width, height


def convert_webp(
    source_path: str | Path,
    *,
    target_format: str = "auto",
    output_path: str | Path | None = None,
    quality: int = 92,
    overwrite: bool = False,
    delete_source: bool = False,
    jpeg_background: tuple[int, int, int] = (
        255,
        255,
        255,
    ),
) -> ConversionResult:
    """
    Convert WebP to PNG, JPEG, or GIF.

    Automatic output behavior:

    - animated WebP -> GIF
    - transparent static WebP -> PNG
    - opaque static WebP -> JPEG

    The original file is preserved unless delete_source=True.
    """

    if not pillow_has_webp_support():
        raise ImageConversionError(
            "This Pillow installation does not include "
            "WebP support."
        )

    if not 1 <= quality <= 100:
        raise ImageConversionError(
            "JPEG quality must be between 1 and 100."
        )

    source = Path(
        source_path
    ).expanduser()

    if not source.is_file():
        raise ImageConversionError(
            f"Source file does not exist: {source}"
        )

    requested_format = _normalize_target_format(
        target_format
    )

    try:
        with Image.open(source) as image:
            image.load()

            if (image.format or "").upper() != "WEBP":
                raise ImageConversionError(
                    "Expected a WebP file, but Pillow "
                    f"detected {image.format or 'unknown'}."
                )

            animated = bool(
                getattr(
                    image,
                    "is_animated",
                    False,
                )
            )

            frame_count = int(
                getattr(
                    image,
                    "n_frames",
                    1,
                )
            )

            output_format = _select_output_format(
                requested_format,
                animated=animated,
                has_alpha=_has_alpha(image),
            )

            target = _prepare_output_path(
                source,
                output_format,
                output_path,
            )

            target.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            if target.exists() and not overwrite:
                raise ImageConversionError(
                    f"Output already exists: {target}. "
                    "Set overwrite=True to replace it."
                )

            temporary_output = target.with_name(
                f".{target.stem}."
                f"{uuid4().hex}.tmp"
                f"{target.suffix}"
            )

            try:
                if animated:
                    (
                        written_frames,
                        width,
                        height,
                    ) = _save_animated_gif(
                        image,
                        temporary_output,
                    )
                else:
                    (
                        written_frames,
                        width,
                        height,
                    ) = _save_static_image(
                        image,
                        output_format,
                        temporary_output,
                        quality=quality,
                        jpeg_background=jpeg_background,
                    )

                temporary_output.replace(target)

            except Exception:
                temporary_output.unlink(
                    missing_ok=True
                )
                raise

    except ImageConversionError:
        raise

    except Exception as exc:
        raise ImageConversionError(
            f"WebP conversion failed: {exc}"
        ) from exc

    source_deleted = False

    if (
        delete_source
        and source.resolve() != target.resolve()
    ):
        source.unlink()
        source_deleted = True

    return ConversionResult(
        source_path=str(source.resolve()),
        output_path=str(target.resolve()),
        source_format="WEBP",
        output_format=output_format,
        animated=animated,
        frame_count=(
            written_frames
            if animated
            else frame_count
        ),
        width=width,
        height=height,
        output_size_bytes=target.stat().st_size,
        source_deleted=source_deleted,
    )

