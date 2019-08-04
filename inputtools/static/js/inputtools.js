const scriptsToLoad = [
	"static/js/ime/libs/rangy/rangy-core.js",
	"static/js/ime/src/jquery.ime.js",
	"static/js/ime/src/jquery.ime.preferences.js",
	"static/js/translateDemo.js"
];
const stylesToLoad = [
	"static/css/inputtools.css"
];

document.addEventListener('DOMContentLoaded', (event) => {

	function loadScript(url) {
		return new Promise((resolve, reject) => {
			// Adding the script tag to the head
			var head = document.head;
			var script = document.createElement('script');
			script.type = 'text/javascript';
			script.src = url;

			// Then bind the event to the callback function.
			// There are several events for cross browser compatibility.
			script.onreadystatechange = () => resolve();
			script.onload = () => resolve();

			// Fire the loading
			head.appendChild(script);
		});
	}

	function loadStyle(url) {
		return new Promise((resolve, reject) => {
			// Adding the script tag to the head
			var body = document.head;
			var link = document.createElement('link');
			link.rel = 'stylesheet';
			link.href = url;

			// Then bind the event to the callback function.
			// There are several events for cross browser compatibility.
			link.onreadystatechange = () => resolve();
			link.onload = () => resolve();

			// Fire the loading
			body.appendChild(link);
		});
	}

	loadScript("static/js/jquery/jquery-3.3.1.min.js")
		.then(() => {
			const promiseArr = scriptsToLoad.map((file) => loadScript(file))
				.concat(stylesToLoad.map((file) => loadStyle(file)));
			return Promise.all(promiseArr)
		})
		.then(() => {
			var $ced;

			/** Codes from jquery.ime.inputmethods.js **/
			// All keys have quotes for consistency
			$.extend( $.ime.sources, {
			 'hi-inscript2': {
				 name: 'देवनागरी (Inscript)',
				 source: 'rules/hi/hi-inscript2.js'
			 },
			 'hi-transliteration': {
				 name: 'देवनागरी (लिप्यंतरण)',
				 source: 'rules/hi/hi-transliteration.js'
			 }
			} );
			$.extend( $.ime.languages, {
			 hi: {
				 autonym: 'हिन्दी',
				 inputmethods: [ 'hi-transliteration', 'hi-inscript2']
			 }
			} );
			/* END: codes from jquery.ime.inputmethods.js */

			var ime;
			var hindiLanguageCode = 'hi';
			var hindiInputMethod = 'hi-transliteration';
			var systemInputMethod = 'system'
			var $inputMethodButton;

			/**
			 * Toggle input method
			 */
			function toggleIM() {
				if (this.dataset.inputmethod == systemInputMethod) {
					// Change the input method to hindiInputMethod
					console.log("Enabling IM")
					ime.load( hindiInputMethod ).done( function () {
						ime.setIM( hindiInputMethod );
					} );
					ime.enable();
					$(this).attr('data-inputmethod', hindiInputMethod);
					$(this).addClass('selected');
				} else {
					// Disable the inputMethods (Use the system input method)
					console.log("Disabling IM")
					ime.disable();
					$(this).attr('data-inputmethod', systemInputMethod);
					$(this).removeClass('selected');
				}
				return;
			}

			// set `rules` directory path
			$.ime.setPath( '/static/js/ime/');
			// Transliteration element
			$ced = $( '#body' );
			// Initialise IME on this element
			$ced.ime( {
				showSelector: false
			} );
			// Get the IME object
			ime = $ced.data( 'ime' );
			// Enable IME
			ime.enable();
			// Set default IME language
			ime.setLanguage( hindiLanguageCode );

			// Get IME language
			//ime.getLanguage()
			// Get input methods for a given `language`
			//ime.getInputMethods( language )

			// Input method selection button inital config
			$inputMethodButton = $('#inputMethodButton');
			$inputMethodButton.attr('data-inputmethod', systemInputMethod);
			$inputMethodButton.removeClass('selected');

			// Bind events
			document.getElementById('inputMethodButton').addEventListener( 'click', function (event) {
				event.preventDefault();
				toggleIM.call(this);
			});
	});
});
