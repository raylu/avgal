(async () => {
	'use strict';

	const r = await fetch('files.json');
	const files = await r.json();
	const items = files.map((filename) => {
		const [base, ext] = filename.split('.', 2);
		const thumbnail = `${base}-thumb.${ext === 'mp4' ? 'avif' : ext}`;
		return {'src': filename, 'srct': thumbnail};
	});

	jQuery('#nanogallery2').nanogallery2({
		'thumbnailHeight': 200,
		'thumbnailWidth': 'auto',
		'items': items,
		'thumbnailBorderHorizontal': 0,
		'thumbnailBorderVertical': 0,
	});
})();
