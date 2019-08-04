const scriptsToLoad = [
	"static/js/ime/libs/rangy/rangy-core.js",
	"static/js/ime/src/jquery.ime.js",
	"static/js/ime/src/jquery.ime.preferences.js",
	"static/js/ime/src/jquery.ime.inputmethods.js",
	"static/js/translator.js"
];
const stylesToLoad = [
	"static/css/inputtools.css"
];

let $ced;
let ime;

const hindiLanguageCode = 'hi';
const hindiInputMethod = 'hi-transliteration';
const systemInputMethod = 'system';


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

var inputtools = {

	// toggle input method
	toggleIM: function() {
		if (this.dataset.inputmethod === systemInputMethod) {
			// Change the input method to hindiInputMethod
			console.log("Enabling IM")
			ime.load( hindiInputMethod )
				.done( function () {
					ime.setIM( hindiInputMethod );
				});
			ime.enable();
			this.setAttribute('data-inputmethod', hindiInputMethod);
			this.classList.add('selected');
		} else {
			// Disable the inputMethods (Use the system input method)
			console.log("Disabling IM")
			ime.disable();
			this.setAttribute('data-inputmethod', systemInputMethod);
			his.classList.remove('selected');
		}
	},

	enableImButton: function(buttonId) {
		// Input method selection button inital config
		let inputMethodButton = document.getElementById(buttonId);
		inputMethodButton.setAttribute('data-inputmethod', systemInputMethod);
		inputMethodButton.classList.remove('selected');
		// Bind event
		document
			.getElementById(buttonId)
			.addEventListener( 'click', function (event) {
				event.preventDefault();
				inputtools.toggleIM.call(this);
			});
	},

	// register IME on all target input elements
	registerIME: function() {
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
	},

};

// Create action buttons
function createActionButtons() {

}

// Bind events
function bindEvents() {
	inputtools.registerIME();
	inputtools.enableImButton('inputMethodButton');
	translator.enableTranslateButton('translateButton');
	translator.enableSaveButton('saveButton');
}

document.addEventListener('DOMContentLoaded', function(event) {

	loadScript("static/js/jquery/jquery-3.3.1.min.js")
		.then(() => {
			const promiseArr = scriptsToLoad.map((file) => loadScript(file))
				.concat(stylesToLoad.map((file) => loadStyle(file)));
			return Promise.all(promiseArr)
		})
		.then(() => {

			createActionButtons();
			bindEvents();

	});
});
