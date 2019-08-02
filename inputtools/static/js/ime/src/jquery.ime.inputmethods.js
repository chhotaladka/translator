( function ( $ ) {
	'use strict';

	// All keys have quotes for consistency
	/* eslint-disable quote-props */
	$.extend( $.ime.sources, {
		'hi-inscript': {
			name: 'इनस्क्रिप्ट',
			source: 'rules/hi/hi-inscript.js'
		},
		'hi-inscript2': {
			name: 'देवनागरी (Inscript)',
			source: 'rules/hi/hi-inscript2.js'
		},
		'hi-transliteration': {
			name: 'देवनागरी (लिप्यंतरण)',
			source: 'rules/hi/hi-transliteration.js'
		}
	} );
	/* eslint-disable quote-props */

	$.extend( $.ime.languages, {
		hi: {
			autonym: 'हिन्दी',
			inputmethods: [ 'hi-transliteration', 'hi-inscript2']
		},
		en: {
			autonym: 'english',
			inputmethods: [ 'hi-inscript']
		}
	} );

}( jQuery ) );
