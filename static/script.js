(async () => {
	'use strict';

	const r = await fetch('files.json');
	const files = await r.json();
	const items = [];
	let lastMonth = null;
	let albumID = 0;
	for (const filename of files) {
		const [base, ext] = filename.split('.', 2);
		const thumbnail = `${base}-thumb.${ext === 'mp4' ? 'avif' : ext}`;

		const month = filename.substring(0, 6);
		if (month !== lastMonth) {
			albumID++;
			items.push({
				'title': `${month.substring(0, 4)}-${month.substring(4)}`,
				'ID': albumID, 'kind': 'album', 'src': thumbnail,
			});
			lastMonth = month;
		}
		items.push({'src': filename, 'srct': thumbnail, albumID});
	}

	jQuery('#nanogallery2').nanogallery2({
		'thumbnailL1Height': 300,
		'thumbnailL1Width': 'auto',
		'thumbnailL1GutterWidth': 20,
		'thumbnailL1GutterHeight': 20,
		'thumbnailHeight': 200,
		'thumbnailWidth': 'auto',
		'items': items,
		'thumbnailBorderHorizontal': 0,
		'thumbnailBorderVertical': 0,
	});
})();
