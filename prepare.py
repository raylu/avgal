#!/usr/bin/env python3

import pathlib
import sys

import imageio.v3 as iio
import imageio.plugins.freeimage
import PIL.Image
import pillow_avif  # noqa: F401

imageio.plugins.freeimage.download()

def main():
	path = pathlib.Path(sys.argv[1])
	for raw in path.glob('*.CR2'):
		process_image(raw)

def process_image(raw: pathlib.Path) -> None:
	print(raw)
	avif_path = raw.parent / (raw.stem + '.avif')
	thumb_path = raw.parent / (raw.stem + '-thumb.avif')
	if avif_path.exists() and thumb_path.exists():
		print('\tavif already exists; skipping')
		return

	img = iio.imread(raw)
	iio.imwrite(avif_path, img)

	min_dim = min(img.shape[:2])
	scale_factor = min_dim / 200
	dim = (int(img.shape[0] / scale_factor), int(img.shape[1] / scale_factor))
	print('\t', img.shape[:2], '→', dim)
	thumbnail = PIL.Image.fromarray(img).resize(reversed(dim))
	thumbnail.save(thumb_path)

if __name__ == '__main__':
	main()
