const scriptsToLoad = [
	"static/js/jquery/jquery-3.3.1.min.js",
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
	//console.info(url);
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
	// status of inputtools
	active: false,

	// enable/disable buttton element

	/**
	 * Check whether the inputtool is active or not
	 *
	 * @return {boolean}
	 */
	isActive: function () {
		return this.active;
	},

	// Disable the input method
	disable: function () {
		this.active = false;
	},

	// Enable the input method
	enable: function () {
		this.active = true;
	},

	// toggle input method
	toggleIM: function() {
		//console.log(this);
		if (this.dataset.inputmethod === systemInputMethod) {
			// Change the input method to hindiInputMethod
			console.log("Enabling IM")
			ime.load( hindiInputMethod )
				.done( function () {
					ime.setIM( hindiInputMethod );
				});
			ime.enable();
			inputtools.enable();
			this.setAttribute('data-inputmethod', hindiInputMethod);
			this.classList.add('selected');
		} else {
			// Disable the inputMethods (Use the system input method)
			console.log("Disabling IM")
			ime.disable();
			inputtools.disable();
			this.setAttribute('data-inputmethod', systemInputMethod);
			this.classList.remove('selected');
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
			// .addEventListener("click", event => {
			// 	event.preventDefault();
			// 	this.toggleIM();
			// 	// do something
			// });
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

var suggestions = {

	// Max number of suggestions
	max_suggest: 6,

	// Create html elements for input suggestions
	createElements: function() {
		let box = document.createElement("div");
		box.className = "ita-ppe-box";
		box.setAttribute("style", "direction: ltr; display: none; -moz-user-select: none;");
		box.setAttribute("tabindex", "-1");

		let edit = document.createElement("div");
		edit.className = "ita-ppe-edit";
		let span = document.createElement("span");
		span.className = "ita-ppe-uds";
		edit.appendChild(span);
		span = document.createElement("span");
		span.className = "ita-ppe-cur";
		edit.appendChild(span);
		box.appendChild(edit);

		let div = document.createElement("div");
		div.className = "ita-ppe-div";
		let list = document.createElement("div");
		list.className = "ita-ppe-can-list";
		for(let x = 0; x < this.max_suggest; x++) {
			var li = document.createElement("div");
			li.className = "ita-ppe-can";
			li.setAttribute("style", "-moz-user-select: none;");
			li.innerHTML = x + ". desolation";
			list.appendChild(li);
		}
		list.firstChild.classList.add("ita-ppe-hlt");
		div.appendChild(list);
		box.appendChild(div);

		document.body.appendChild(box);
	},

	// Listen for events and bind to handlers
	listen: function () {
		console.log("listen");
		document
			.getElementById("body")
			.addEventListener("keydown", event => {
				suggestions.keypress(event);
	  		// do something
			});
		//			.addEventListener( 'keydown', inputtools.keypress);
	},

	/**
	 * Keypress handler
	 *
	 * @param {jQuery.Event} e Event
	 * @return {boolean}
	 */
	keypress: function ( e ) {
		//console.log($('#body').prop('selectionStart') + ',' + $('#body').prop('selectionEnd'));
		console.log(e.code);
		//console.log(this);
		return false;
		var altGr = false,
			c, input, replacement;

		if ( !this.active ) {
			return true;
		}

		if ( !this.inputmethod ) {
			return true;
		}

		// handle backspace
		if ( e.which === 8 ) {
			// Blank the context
			this.context = '';
			return true;
		}

		if ( e.altKey || e.altGraphKey ) {
			altGr = true;
		}

		// Don't process ASCII control characters except linefeed,
		// as well as anything involving Ctrl, Meta and Alt,
		// but do process extended keymaps
		if ( ( e.which < 32 && e.which !== 13 && !altGr ) || e.ctrlKey || e.metaKey ) {
			// Blank the context
			this.context = '';

			return true;
		}

		c = String.fromCharCode( e.which );

		// Append the character being typed to the preceding few characters,
		// to provide context for the transliteration regexes.
		input = this.textEntry.getTextBeforeSelection( this.inputmethod.maxKeyLength );
		replacement = this.transliterate( input + c, this.context, altGr );

		// Update the context
		this.context += c;

		if ( this.context.length > this.inputmethod.contextLength ) {
			// The buffer is longer than needed, truncate it at the front
			this.context = this.context.substring(
				this.context.length - this.inputmethod.contextLength
			);
		}

		// Allow rules to explicitly define whether we match something.
		// Otherwise we cannot distinguish between no matching rule and
		// rule that provides identical output but consumes the event
		// to prevent normal behavior. See Udmurt layout which uses
		// altgr rules to allow typing the original character.
		if ( replacement.noop ) {
			return true;
		}

		this.textEntry.replaceTextAtSelection( input.length, replacement.output );

		e.stopPropagation();

		return false;
	},

};

// Create action buttons
function createActionButtons() {
	var wrapper = document.getElementById("translatorWrapper");
	if (!wrapper) {
		return;
	}

	var toolbar = document.createElement("div");
	toolbar.className = "trans-toolbar";

	var btn1 = document.createElement("button");
	//btn1.className = "action-button inputmethod";
	btn1.setAttribute("class", "action-button inputmethod");
	btn1.setAttribute("id", "inputMethodButton");
	btn1.setAttribute("title", "हिंदी में टाइप करें | abc → हिन्दी");
	var svg_keyboard =
		'<svg name="keyboard" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">' +
			'<path d="M20 5H4c-1.1 0-1.99.9-1.99 2L2 17c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm-9 3h2v2h-2V8zm0 3h2v2h-2v-2zM8 8h2v2H8V8zm0 3h2v2H8v-2zm-1 2H5v-2h2v2zm0-3H5V8h2v2zm9 7H8v-2h8v2zm0-4h-2v-2h2v2zm0-3h-2V8h2v2zm3 3h-2v-2h2v2zm0-3h-2V8h2v2z"/>' +
			'<path d="M0 0h24v24H0zm0 0h24v24H0z" fill="none"/>' +
		'</svg>';
	btn1.insertAdjacentHTML('beforeend', svg_keyboard);
	btn1.insertAdjacentHTML('beforeend', '<span class="action-button__text">हिन्दी</span>');
	toolbar.appendChild(btn1);

	var btn2 = document.createElement("button");
	btn2.setAttribute("class", "action-button translate");
	btn2.setAttribute("id", "translateButton");
	btn2.setAttribute("title", "हिंदी में अनुवाद करें | Translate into Hindi");
	var svg_translate =
		'<svg name="translate" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">' +
			'<path d="M0 0h24v24H0z" fill="none"/>' +
			'<path d="M12.87 15.07l-2.54-2.51.03-.03c1.74-1.94 2.98-4.17 3.71-6.53H17V4h-7V2H8v2H1v1.99h11.17C11.5 7.92 10.44 9.75 9 11.35 8.07 10.32 7.3 9.19 6.69 8h-2c.73 1.63 1.73 3.17 2.98 4.56l-5.09 5.02L4 19l5-5 3.11 3.11.76-2.04zM18.5 10h-2L12 22h2l1.12-3h4.75L21 22h2l-4.5-12zm-2.62 7l1.62-4.33L19.12 17h-3.24z"/>' +
		'</svg>';
	btn2.insertAdjacentHTML('beforeend', svg_translate);
	btn2.insertAdjacentHTML('beforeend', '<span class="action-button__text">Translate</span>');
	toolbar.appendChild(btn2);

	var btn3 = document.createElement("button");
	btn3.setAttribute("class", "action-button save");
	btn3.setAttribute("id", "saveButton");
	btn3.setAttribute("title", "Save Translation");
	var svg_save =
		'<svg name="cloud_upload" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">' +
			'<path d="M0 0h24v24H0z" fill="none"/>' +
			'<path d="M19.35 10.04C18.67 6.59 15.64 4 12 4 9.11 4 6.6 5.64 5.35 8.04 2.34 8.36 0 10.91 0 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5 0-2.64-2.05-4.78-4.65-4.96zM14 13v4h-4v-4H7l5-5 5 5h-3z"/>' +
		'</svg>';
	btn3.insertAdjacentHTML('beforeend', svg_save);
	btn3.insertAdjacentHTML('beforeend', '<span class="action-button__text">Save</span>');
	toolbar.appendChild(btn3);

	var btn4 = document.createElement("a");
	btn4.setAttribute("class", "action-button help");
	btn4.setAttribute("id", "helpButton");
	btn4.setAttribute("title", "Help");
	btn4.setAttribute("href", "/help");
	btn4.setAttribute("target", "_blank");
	var svg_help =
		'<svg name="help_outline" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">' +
			'<path fill="none" d="M0 0h24v24H0z"/>' +
			'<path d="M11 18h2v-2h-2v2zm1-16C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm0-14c-2.21 0-4 1.79-4 4h2c0-1.1.9-2 2-2s2 .9 2 2c0 2-3 1.75-3 5h2c0-2.25 3-2.5 3-5 0-2.21-1.79-4-4-4z"/>' +
		'</svg>';
	btn4.insertAdjacentHTML('beforeend', svg_help);
	btn4.insertAdjacentHTML('beforeend', '<span class="action-button__text"></span>');
	toolbar.appendChild(btn4);

	wrapper.appendChild(toolbar);
	return true;
}

// Bind events
function bindEvents() {
	inputtools.registerIME();
	inputtools.enableImButton('inputMethodButton');
	translator.enableTranslateButton('translateButton');
	translator.enableSaveButton('saveButton');
}

document.addEventListener('DOMContentLoaded', function(event) {

	Promise.resolve(stylesToLoad.map((file) => loadStyle(file)))
		.then(() => {
			Promise.each = async function(arr) {
			   for(const item of arr) await loadScript(item);
			}
			return Promise.each(scriptsToLoad);
		})
		.then(() => {
			if (createActionButtons()) {
				bindEvents();
			}
			suggestions.createElements();
			//suggestions.listen();
	});
});
