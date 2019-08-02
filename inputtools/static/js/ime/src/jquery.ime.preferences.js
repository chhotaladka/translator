( function ( $ ) {
	'use strict';

	$.extend( $.ime.preferences, {
		registry: {
			isDirty: false,
			language: null,
			previousInputMethods: [], // array of previous inputmethods
			imes: {
				en: 'system'
			}
		},

		setLanguage: function ( language ) {
			// Do nothing if there's no actual change
			if ( language === this.registry.language ) {
				return;
			}

			this.registry.language = language;
			this.registry.isDirty = true;
		},

		getLanguage: function () {
			return this.registry.language;
		},

		getDefaultLanguage: function () {
			return 'hi';
		},

		getPreviousInputMethods: function () {
			return this.registry.previousInputMethods;
		},

		// Set the given IM as the last used for the language
		setIM: function ( inputMethod ) {
			if ( !this.registry.imes ) {
				this.registry.imes = {};
			}

			// Do nothing if there's no actual change
			if ( inputMethod === this.registry.imes[ this.registry.language ] ) {
				return;
			}

			this.registry.imes[ this.getLanguage() ] = inputMethod;
			this.registry.isDirty = true;
		},

		// Return the last used or the default IM for language
		getIM: function ( language ) {
			if ( !this.registry.imes ) {
				this.registry.imes = {};
			}

			return this.registry.imes[ language ] || 'system';
		},

	} );
}( jQuery ) );
