const scriptsToLoad = [
	"static/js/jquery/jquery-3.3.1.min.js",
	"static/js/ime/libs/rangy/rangy-core.js",
	"static/js/ime/src/jquery.ime.js",
	"static/js/ime/src/jquery.ime.preferences.js",
	"static/js/ime/src/jquery.ime.inputmethods.js",
	"static/js/caret-position.js",
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

	url: '/rest/inputtools/',

	// Status of suggestions
	active: false,

	/**
	 * Check whether the suggestions is active or not
	 * @return {boolean}
	 */
	isActive: function () {
		return this.active;
	},

	// Disable suggestions
	disable: function () {
		this.active = false;
	},

	// Enable suggestions
	enable: function () {
		this.active = true;
	},

	/**
	 * Init/constructor function
	 *
	 * @param {string} id element id of textarea
	 * @return {boolean}
	 */
	init: function(id) {
		console.info("init");
		// Text input element
		this.element = document.getElementById(id);
		// check if the element is input/textarea/editiable

		// Max number of suggestions
		this.max_suggest = 15;

		//
		this.context = '';
		this.contextLength = 0;
		this.cursorStart = 0;
		this.cursorEnd = 0;

		// input word for suggestions
		this.input = '';

		this.csrftoken = suggestions.getCookie('csrftoken');

		// suggestion box html element, initialized to none
		this.box = this.createBoxElements();
		this.box_items = this.box.getElementsByClassName('ita-ppe-can-list')[0];
		this.pos_left = 0;
		this.pos_top = 0;
		// display status of suggestion box
		this.visible = false;
	},

	// Create html elements for input suggestions
	createBoxElements: function() {
		let box = document.createElement("div");
		box.className = "ita-ppe-box";
		box.setAttribute("style", "direction: ltr; display: none; user-select: none;");
		box.setAttribute("tabindex", "-1");

		let edit = document.createElement("div");
		edit.className = "ita-ppe-edit";
		edit.setAttribute("style", "user-select: none;");
		let span = document.createElement("span");
		span.className = "ita-ppe-uds";
		span.setAttribute("style", "user-select: none;");
		edit.appendChild(span);
		span = document.createElement("span");
		span.className = "ita-ppe-cur";
		span.setAttribute("style", "user-select: none;");
		edit.appendChild(span);
		box.appendChild(edit);

		let div = document.createElement("div");
		div.className = "ita-ppe-div";
		div.setAttribute("style", "user-select: none;");
		let list = document.createElement("div");
		list.className = "ita-ppe-can-list";
		list.setAttribute("style", "user-select: none;");
		for(let x = 0; x < this.max_suggest; x++) {
			var li = document.createElement("div");
			li.className = "ita-ppe-can";
			li.setAttribute("style", "user-select: none;");
			li.innerHTML = x + ". desolation";
			list.appendChild(li);
		}
		list.firstChild.classList.add("ita-ppe-hlt");
		div.appendChild(list);
		box.appendChild(div);

		return document.body.appendChild(box);
	},

	// Listen for events and bind to handlers
	listen: function () {
		console.info("listen");
		this.element.addEventListener("keydown", event => {
				suggestions.keypress(event);
	  		// do something
		});
		document.addEventListener("click", (e) => {
			// clicked anywhere other than suggestion box
			// Hide suggestion box if active
			if (!this.visible) {
				return;
			}
	    const flyoutElement = this.box; // suggestion box
	    let targetElement = e.target; // clicked element
	    do {
	        if (targetElement == flyoutElement) {
	            // This is a click inside. Do nothing, just return.
	            return;
	        }
	        // Go up the DOM
	        targetElement = targetElement.parentNode;
	    } while (targetElement);
	    // This is a click outside suggestion box.
	    this.hideBox();
		});
		this.element.addEventListener("blur", event => {
			// Hide suggestion box if window goes out of focus
			if (this.visible) {
				this.hideBox();
			}
		});
	},

	resetPosition: function() {
		this.pos_left = 0;
		this.pos_top = 0;
	},
	setPosition: function() {//Calculate the caret position
		let caret = getCaretCoordinates(this.element, this.cursorEnd);
  	console.debug("** setting new position:", caret);
		const domRect = this.element.getBoundingClientRect();
		//console.debug(domRect, this.cursorEnd);
		this.pos_left = caret.left + domRect.left;
		this.pos_top = caret.top + domRect.top + 60; //TODO replce with actual line height
	},
	showBox: function() {
		if (!this.visible) {
			this.setPosition();//new position
		}
		this.box.style.left = this.pos_left+"px";
		this.box.style.top = this.pos_top+"px";
		this.box.style.display = "block";
		this.visible = true;
	},
	hideBox: function() {
		this.box.style.display = "none";
		this.resetPosition();
		this.visible = false;
		this.context = '';
		this.cursorStart = this.cursorEnd = this.element.selectionStart;
	},
	updateBoxEditStr: function() {
		let edit = this.box.getElementsByClassName('ita-ppe-uds')[0];
		edit.innerHTML = this.context;
	},
	selectSuggestion: function() {
		//replace the word at caret with the selected suggestion
		let src = this.box_items.getElementsByClassName('ita-ppe-hlt')[0].lastChild.innerHTML;
		src = src + ' '; //add space at the end
		// there should always be a suggestion
		let dst = this.element.value.substring(this.cursorStart, this.cursorEnd);
		console.debug("src [%s] dst [%s] start %s end %s",src,dst,this.cursorStart,this.cursorEnd)
		this.element.value = this.element.value.substring(0, this.cursorStart+1) + src + this.element.value.substring(this.cursorEnd+1);
		// update cursor
		this.element.selectionStart = this.element.selectionEnd = this.cursorStart + src.length + 1;
	},
	boxScrollDown: function() {
		let curr = this.box_items.getElementsByClassName('ita-ppe-hlt')[0];
		let next = curr.nextElementSibling;
		if (next) {
			next.classList.add("ita-ppe-hlt");
			curr.classList.remove("ita-ppe-hlt");
		} else {
			//TODO move to top
		}
	},
	boxScrollUp: function() {
		let curr = this.box_items.getElementsByClassName('ita-ppe-hlt')[0];
		let prev = curr.previousElementSibling;
		if (prev) {
			prev.classList.add("ita-ppe-hlt");
			curr.classList.remove("ita-ppe-hlt");
		} else {
			//TODO move to top
		}
	},

	renderSuggestions: function(response){
			console.log(response);
			let list = response['suggestions'];
			// list should not be empty and first suggestion should be response['word'] itself
			list.unshift(response['word']);

			this.updateBoxEditStr();
			let num = Math.min(list.length, this.max_suggest);
			this.box_items.innerHTML = "";

			for (let x = 1; x <= num; x++) {
				var li = document.createElement("div");
				li.className = "ita-ppe-can";
				li.setAttribute("style", "user-select: none;");
				li.innerHTML = '<span>' + x + '. </span><span>' + list[x-1] + '</span>';
				this.box_items.appendChild(li);
			}
			this.box_items.firstChild.classList.add("ita-ppe-hlt");
			this.showBox();
	},

	getCookie : function(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie != ''){
          var cookies = document.cookie.split(';');
          for(var i=0; i < cookies.length; i++){
              var cookie = jQuery.trim(cookies[i]);
              if(cookie.substring(0, name.length+1) == (name + '=')){
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
    },

  csrfSafeMethod: function(method){
        return(/^(GET|HEAD|OPTIONS|TRACE|POST)$/.test(method));
    },

  handleAjaxError : function(xhRequest, ErrorText, thrownError){
        //alert( "Sorry, there was a problem!" );
        console.log( "Error: " + thrownError );
        console.log( "Status: " + ErrorText );
        console.dir( xhRequest );
    },

	getSuggestions: function(word) {

		word = word.trim();
		if (word.length < 1) {
			return false;
		}
		let data = {"word": word, "lang": "hi"};
		$.ajaxSetup({
							beforeSend: function(xhr, settings) {
									if (!suggestions.csrfSafeMethod(settings.type) && !this.crossDomain) {
											xhr.setRequestHeader("X-CSRFToken", suggestions.csrftoken);
									}
							}
					});
		$.ajax({
						cache: false,
						url : this.url,
						type: 'POST',
						dataType : "json",
						contentType: "application/json;",
						data : JSON.stringify(data),
						context : this,
						success : suggestions.renderSuggestions,
						error : suggestions.handleAjaxError
					});
	},

	triggerSuggest: function() {
		console.debug("triggerSuggest:", this.cursorStart, this.cursorEnd);
		this.cursorEnd = this.element.selectionStart;
		const a = this.element.value;
		// If user has manually placed the cursor at some location in the text,
		// in that case `this.cursorStart` needs a new value,
		// currently, that is begining of the word under the cursor.
		let i = this.cursorEnd - 1;
		let regex = /[\s!@#$%^&*(),.?":{}|<>]/g
		while(i) {
			//console.debug("i=",i,"a[i]=",a[i]);
			if(a[i].match(regex) != null) break;
			i--;
		}
		this.cursorStart = i;
		this.input = a.substring(this.cursorStart, this.cursorEnd);
		console.debug("word[", this.cursorStart, this.cursorEnd, "] = ", this.input);
		//console.debug("context len", this.context.length);
		// if (!this.context.length) { //update the context
		// 	console.debug("updating context");
		// 	this.context = this.input;
		// }

		this.getSuggestions(this.input);
	},

	/**
	 * Keypress handler
	 *
	 * @param {jQuery.Event} e Event
	 * @return {boolean}
	 */
	keypress: function ( e ) {
		console.debug(" >> keypress START:", e.code, e.which, this.element.selectionStart, this.element.selectionEnd);

		var altGr = false,
			c, input, replacement;

		if ( !inputtools.isActive() ) {
			return true;
		}

		// handle Enter(13) and Space(32)
		if (e.which === 13 || e.which === 32) {
			if (this.visible) {
				console.log("Enter / Space pressed");
				// Replace word with selected suggestion
				this.selectSuggestion();
				// Hide suggestion box TODO
				this.hideBox();
				// caret should not go to the next line
				e.preventDefault();
				return;
			}
		}

		// handle Backspace(8) TODO
		if ( e.which === 8 ) {
			if (this.visible) {
				//console.debug("backspace on context:", this.context, this.context.length);
				// Update the context
				if (this.context.length) {
					this.context = this.context.slice(0, -1);
					this.updateBoxEditStr();
				}
				if (this.context.length == 0) {
					// Hide suggestion box TODO
					this.hideBox();
				} else {
					this.triggerSuggest();
				}
			}
			return true;
		}

		// handle ArrowDown(40)
		if (e.which === 40) {
			if (this.visible) {
				this.boxScrollDown();
				e.preventDefault();
			}
			return true;
		}
		// handle ArrowUp(38)
		if (e.which === 38) {
			if (this.visible) {
				this.boxScrollUp();
				e.preventDefault();
			}
			return true;
		}

		// handle ArrowLeft(37) and ArrowRight(39)
		if (e.which === 37 || e.which === 39) {
			if (this.visible) {
				e.preventDefault();
			}
			return true;
		}

		if (e.altKey || e.altGraphKey) {
			altGr = true;
		}

		// Don't process ASCII control characters except linefeed,
		// as well as anything involving Ctrl, Meta and Alt,
		// but do process extended keymaps
		if ( ( e.which < 32 && e.which !== 13 && !altGr ) || e.ctrlKey || e.metaKey ) {
			console.info('Not sure what to do');
			return true;
		}

		c = String.fromCharCode(e.which).toLowerCase();
		// Update the context
		this.context += c;

		console.log(" >> keypress END:",this.context, this.input, this.cursorStart, this.cursorEnd);
		e.stopPropagation();

		return true;
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

	let transGroup = document.createElement("div");
	transGroup.setAttribute("style", "display: flex;");

	var toggle = document.createElement("button");
	toggle.setAttribute("class", "action-button bNone");
	toggle.setAttribute("id", "translateSwitch");
	toggle.setAttribute("style", "display: flex;");
	toggle.innerHTML =
		'<span class="action-button__text" style="margin: 3px 8px 0px;">Auto-translate</span>' +
		'<label class="mdl-switch mdl-js-switch mdl-js-ripple-effect mdl-js-ripple-effect--ignore-events is-upgraded '+ 
			((eval(translator.getCookie('fastTranslate'))==true)?'is-checked':'')+ '">' +
			'<input type="checkbox" class="mdl-switch__input"' + 
			((eval(translator.getCookie('fastTranslate'))==true)?'checked="checked"':'')+'>' +
  		'<span class="mdl-switch__label"></span>' +
			'<div class="mdl-switch__track"></div>' +
			'<div class="mdl-switch__thumb"><span class="mdl-switch__focus-helper"></span></div>' +
		'</label>'
	transGroup.appendChild(toggle);

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
	transGroup.appendChild(btn2);

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
	transGroup.appendChild(btn4);

	toolbar.appendChild(transGroup);

	var btn3 = document.createElement("button");
	btn3.setAttribute("class", "action-button save");
	btn3.setAttribute("style", "display: none;");
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

	wrapper.appendChild(toolbar);
	return true;
}

// Bind events
function bindEvents() {
	inputtools.registerIME();
	inputtools.enableImButton('inputMethodButton');
	translator.enableTranslateButton('translateButton');
	//translator.enableSaveButton('saveButton');
	document.getElementById('translateSwitch').addEventListener("click", event => {
			event.preventDefault();
			event.stopPropagation();
			const target = document.querySelector('#translateSwitch');
			const checkbox = target.querySelector('input[type="checkbox"]');
  		if (checkbox.checked) {
				target.querySelector('label.mdl-switch').classList.remove('is-checked');
				checkbox.checked = false;
				document.getElementById('translateButton').removeAttribute("disabled");
				//TODO disable automatic translation
				translator.disableFastTranslation();
			} else {
				target.querySelector('label.mdl-switch').classList.add('is-checked');
				checkbox.checked = true;
				document.getElementById('translateButton').setAttribute("disabled", true);
				//TODO enable automatic translation
				translator.enableFastTranslation();
			}

	});
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

			suggestions.init('body');
			suggestions.listen();
	});
});
