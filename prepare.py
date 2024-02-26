#!/usr/bin/env python3

from __future__ import annotations

import pathlib
import sys
import typing

import imageio.v3 as iio
import imageio.plugins.freeimage
import PIL.Image
import pillow_avif  # type: ignore # noqa: F401
import rawpy # type: ignore

if typing.TYPE_CHECKING:
	import numpy

def main():
	path = pathlib.Path(sys.argv[1])
	imageio.plugins.freeimage.download()
	for raw in path.iterdir():
		if raw.suffix.casefold() in ('.cr2', '.jpg'):
			process_image(raw)

def process_image(raw: pathlib.Path) -> None:
	print(raw)
	avif_path = raw.parent / (raw.stem + '.avif')
	thumb_path = raw.parent / (raw.stem + '-thumb.avif')
	if avif_path.exists() and thumb_path.exists():
		print('\tavif already exists; skipping')
		return

	if raw.suffix.casefold() == '.cr2':
		img = rawpy.imread(str(raw)).postprocess(use_camera_wb=True)
	else:
		img = iio.imread(raw)
	max_dim = min(img.shape[:2])
	scale_factor = 1
	while max_dim // scale_factor > 3000:
		scale_factor *= 2
	if scale_factor > 1:
		scaled = scale(img, scale_factor)
		scaled.save(avif_path)
	else:
		iio.imwrite(avif_path, img)

	min_dim = min(img.shape[:2])
	scale_factor = min_dim / 200
	thumbnail = scale(img, scale_factor)
	thumbnail.save(thumb_path)

def scale(img: numpy.ndarray, scale_factor: float) -> PIL.Image:
	dim = (int(img.shape[0] / scale_factor), int(img.shape[1] / scale_factor))
	print('\t', img.shape[:2], '→', dim)
	return PIL.Image.fromarray(img).resize(reversed(dim))


if __name__ == '__main__':
	main()
