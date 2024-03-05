#!/usr/bin/env python3

from __future__ import annotations

import pathlib
import sys

import imageio.v3 as iio
import imageio.plugins.freeimage
import PIL.Image
import pillow_avif  # type: ignore # noqa: F401
import rawpy # type: ignore

def main():
	path = pathlib.Path(sys.argv[1])
	imageio.plugins.freeimage.download()
	for raw in path.iterdir():
		if raw.suffix.casefold() in ('.cr2', '.jpg', '.tif'):
			process_image(raw)

def process_image(raw: pathlib.Path) -> None:
	print(raw)
	avif_path = raw.parent / (raw.stem + '.avif')
	thumb_path = raw.parent / (raw.stem + '-thumb.avif')
	if avif_path.exists() and thumb_path.exists():
		print('\tavif already exists; skipping')
		return

	if raw.suffix.casefold() == '.cr2':
		array = rawpy.imread(str(raw)).postprocess(use_camera_wb=True)
	else:
		array = iio.imread(raw)
	img = PIL.Image.fromarray(array)

	max_dim = min(array.shape[:2])
	scale_factor = 1
	while max_dim // scale_factor > 3000:
		scale_factor *= 2
	if scale_factor > 1:
		dim = (int(array.shape[0] / scale_factor), int(array.shape[1] / scale_factor))
		print('\t', array.shape[:2], '→', dim)
		scaled = img.resize(reversed(dim), PIL.Image.Resampling.BICUBIC)
		scaled.save(avif_path)
	else:
		iio.imwrite(avif_path, array)

	img.thumbnail((400, 400))
	img.save(thumb_path)


if __name__ == '__main__':
	main()
