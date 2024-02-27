(async () => {
	'use strict';

	const r = await fetch('files.json');
	const files = await r.json();

	for (const section of files) {
		const el = document.createElement('section');
		document.querySelector('body').append(el);
		el.append(section['section']);

		const div = document.createElement('div');
		el.append(div);
		const items = section['files'].map((filename) => {
			const [base, ext] = filename.split('.', 2);
			const thumbnail = `${base}-thumb.${ext === 'mp4' ? 'avif' : ext}`;
			return {'src': filename, 'srct': thumbnail};
		});
		jQuery(div).nanogallery2({
			'thumbnailHeight': 200,
			'thumbnailWidth': 'auto',
			'items': items,
			'thumbnailBorderHorizontal': 0,
			'thumbnailBorderVertical': 0,
		});
	}
})();
