( function ( $ ) {
	'use strict';

	var selectorTemplate, MutationObserver;

	function IMESelector( element, options ) {
		console.log(" ### IMESelector ###")
		this.$element = $( element );
		this.options = $.extend( {}, IMESelector.defaults, options );
		this.active = false;
		this.$imeSetting = null;
		this.$menu = null;
		this.inputmethod = null;
		this.init();
		this.prepareInputMethods( 'hi' );
		this.hide();
		this.listen();
	}

	function imeList() {
		return $( '<ul>' ).addClass( 'ime-list' );
	}

	function toggleMenuItem() {
		console.log("toggleMenuItem")
		return $( '<div class="ime-disable selectable-row">' ).append(
			$( '<span>' )
				.attr( {
					'class': 'ime-disable-link',
					'data-i18n': 'jquery-ime-disable-text'
				} )
				.addClass( 'ime-checked' )
				.text( 'System input method' ),
			$( '<span>' )
				.addClass( 'ime-disable-shortcut' )
				.text( 'CTRL+M' )
		);
	}

	/**
	 * Check whether a keypress event corresponds to the shortcut key
	 *
	 * @param {event} event
	 * @return {boolean} true if the key is a shortcut key
	 */
	function isShortcutKey( event ) {
		// 77 - The letter M, for Ctrl-M
		return event.ctrlKey && !event.altKey && ( event.which === 77 );
	}

	IMESelector.prototype = {
		constructor: IMESelector,

		init: function () {
			console.log("INIT")
			this.prepareSelectorMenu();
			this.position();
		},

		prepareSelectorMenu: function () {
			// TODO: In this approach there is a menu for each editable area.
			// With correct event mapping we can probably reduce it to one menu.
			this.$imeSetting = $( selectorTemplate );
			this.$menu = $( '<div class="imeselector-menu" role="menu">' );
			this.$menu.append(
				imeList(),
				toggleMenuItem(),
			);

			if ( $.i18n ) {
				this.$menu.i18n();
			}

			this.$imeSetting.append( this.$menu );
			$( 'body' ).append( this.$imeSetting );
		},

		focus: function () {
			// Hide all other IME settings and collapse open menus
			$( 'div.imeselector' ).hide();
			$( 'div.imeselector-menu' ).removeClass( 'ime-open' );
			this.afterKeydown();
		},

		afterKeydown: function () {
			this.$imeSetting.show();
		},

		show: function () {
			this.$menu.addClass( 'ime-open' );
			this.$imeSetting.show();

			return false;
		},

		hide: function () {
			this.$menu.removeClass( 'ime-open' );
			return false;
		},

		toggle: function () {
			if ( this.$menu.hasClass( 'ime-open' ) ) {
				this.hide();
			} else {
				this.show();
			}
		},

		/**
		 * Bind the events and listen
		 */
		listen: function () {
			var imeselector = this;

			imeselector.$imeSetting.on( 'click.ime', function ( e ) {
				console.log("click: click.ime")
				var t = $( e.target );

				if ( t.hasClass( 'imeselector-toggle' ) ) {
					imeselector.toggle();
				}

				return false;
			} );

			imeselector.$imeSetting.mouseenter( function () {
				// We don't want the selector to disappear
				// while the user is trying to click it
				imeselector.$imeSetting.addClass( 'ime-onfocus' );
			} ).mouseleave( function () {
				imeselector.$imeSetting.removeClass( 'ime-onfocus' );
			} );

			imeselector.$menu.on( 'click.ime', 'li', function () {
				imeselector.$element.focus();

				return false;
			} );

			imeselector.$menu.on( 'click.ime', 'li.ime-im', function () {
				console.log("imeselector.$menu.on click.ime: li.ime-im inputMethod")
				imeselector.selectIM( $( this ).data( 'ime-inputmethod' ) );
				imeselector.$element.trigger( 'setim.ime', $( this ).data( 'ime-inputmethod' ) );

				return false;
			} );

			imeselector.$menu.on( 'click.ime', 'li.ime-lang', function () {
				console.log("imeselector.$menu.on click.ime: li.ime-lang")
				var im = imeselector.selectLanguage( $( this ).attr( 'lang' ) );

				imeselector.$element.trigger( 'setim.ime', im );

				return false;
			} );

			imeselector.$menu.on( 'click.ime', 'div.ime-disable', function () {
				console.log("imeselector.$menu.on click.ime: div.ime-disable")
				imeselector.disableIM();

				return false;
			} );

			imeselector.$element.on( 'focus.ime', function ( e ) {
				console.log("imeselector.element.on focus.ime:")
				imeselector.selectLanguage( imeselector.decideLanguage() );
				imeselector.focus();
				e.stopPropagation();
			} );

			imeselector.$element.attrchange( function () {
				if ( imeselector.$element.is( ':hidden' ) ) {
					imeselector.$imeSetting.hide();
				}
			} );

			// Possible resize of textarea
			imeselector.$element.on( {
				'mouseup.ime': this.position.bind( this ),
				'keydown.ime': this.keydown.bind( this )
			} );

			// Update IM selector position when the window is resized
			// or the browser window is zoomed in or zoomed out
			$( window ).resize( function () {
				imeselector.position();
			} );
		},

		/**
		 * Keydown event handler. Handles shortcut key presses
		 *
		 * @context {HTMLElement}
		 * @param {jQuery.Event} e
		 * @return {boolean}
		 */
		keydown: function ( e ) {
			console.log("keudown shortcut key handler")
			var ime = $( e.target ).data( 'ime' ),
				firstInputmethod,
				previousInputMethods,
				languageCode;

			this.afterKeydown(); // shows the trigger in case it is hidden

			if ( isShortcutKey( e ) ) {
				if ( ime.isActive() ) {
					this.disableIM();
					this.$element.trigger( 'setim.ime', 'system' );
				} else {
					if ( this.inputmethod !== null ) {
						this.selectIM( this.inputmethod.id );
						this.$element.trigger( 'setim.ime', this.inputmethod.id );
					} else {
						languageCode = this.decideLanguage();
						this.selectLanguage( languageCode );

						if ( !ime.isActive() && $.ime.languages[ languageCode ] ) {
							// Even after pressing toggle shortcut again, it is still disabled
							// Check if there is a previously used input method.
							previousInputMethods = $.ime.preferences.getPreviousInputMethods();

							if ( previousInputMethods[ 0 ] ) {
								this.selectIM( previousInputMethods[ 0 ] );
							} else {
								// Provide the default input method in this case.
								firstInputmethod = $.ime.languages[ languageCode ].inputmethods[ 0 ];
								this.selectIM( firstInputmethod );
							}
						}
					}
				}

				e.preventDefault();
				e.stopPropagation();

				return false;
			}

			return true;
		},

		/**
		 * Position the im selector relative to the edit area
		 */
		position: function () {
			var menuWidth, menuTop, menuLeft, elementPosition,
				top, left, cssTop, cssLeft, verticalRoom, overflowsOnRight,
				imeSelector = this,
				rtlElement = this.$element.css( 'direction' ) === 'rtl',
				$window = $( window );

			this.focus(); // shows the trigger in case it is hidden

			elementPosition = this.$element.offset();
			top = elementPosition.top + this.$element.outerHeight();
			left = elementPosition.left;

			// RTL element position fix
			if ( !rtlElement ) {
				left = elementPosition.left + this.$element.outerWidth() -
					this.$imeSetting.outerWidth();
			}

			// While determining whether to place the selector above or below the input box,
			// take into account the value of scrollTop, to avoid the selector from always
			// getting placed above the input box since window.height would be less than top
			// if the page has been scrolled.
			verticalRoom = $window.height() + $( document ).scrollTop() - top;

			if ( verticalRoom < this.$imeSetting.outerHeight() ) {
				top = elementPosition.top - this.$imeSetting.outerHeight();
				menuTop = this.$menu.outerHeight() +
					this.$imeSetting.outerHeight();

				// Flip the menu to the top only if it can fit in the space there
				if ( menuTop < top ) {
					this.$menu
						.addClass( 'ime-position-top' )
						.css( 'top', -menuTop );
				}
			}

			cssTop = top;
			cssLeft = left;
			this.$element.parents().each( function () {
				if ( $( this ).css( 'position' ) === 'fixed' ) {
					imeSelector.$imeSetting.css( 'position', 'fixed' );
					cssTop -= $( document ).scrollTop();
					cssLeft -= $( document ).scrollLeft();
					return false;
				}
			} );

			this.$imeSetting.css( {
				top: cssTop,
				left: cssLeft
			} );

			menuWidth = this.$menu.width();
			overflowsOnRight = ( left - $( document ).scrollLeft() + menuWidth ) > $window.width();

			// Adjust horizontal position if there's
			// not enough space on any side
			if ( menuWidth > left ||
				rtlElement && overflowsOnRight
			) {
				if ( rtlElement ) {
					if ( overflowsOnRight ) {
						this.$menu.addClass( 'ime-right' );
						menuLeft = this.$imeSetting.outerWidth() - menuWidth;
					} else {
						menuLeft = 0;
					}
				} else {
					this.$menu.addClass( 'ime-right' );
					menuLeft = elementPosition.left;
				}

				this.$menu.css( 'left', menuLeft );
			}
		},

		/**
		 * Select a language
		 *
		 * @param {string} languageCode
		 * @return {string|bool} Selected input method id or false
		 */
		selectLanguage: function ( languageCode ) {
			console.log("selectLanguage "+ languageCode)
			var ime, imePref, language;

			// consider language codes case insensitive
			languageCode = languageCode && languageCode.toLowerCase();

			ime = this.$element.data( 'ime' );
			imePref = $.ime.preferences.getIM( languageCode );
			console.log(imePref)
			language = $.ime.languages[ languageCode ];

			if ( !language ) {
				return false;
			}

			if ( ime.getLanguage() === languageCode ) {
				// Nothing to do. It is same as the current language,
				// but check whether the input method changed.
				if ( ime.inputmethod && ime.inputmethod.id !== imePref ) {
					this.selectIM( $.ime.preferences.getIM( languageCode ) );
				}

				return $.ime.preferences.getIM( languageCode );
			}
			console.log("XXXXX")

			// And select the default inputmethod
			ime.setLanguage( languageCode );
			this.inputmethod = null;
			this.selectIM( $.ime.preferences.getIM( languageCode ) );

			return $.ime.preferences.getIM( languageCode );
		},

		/**
		 * Get the autonym by language code.
		 *
		 * @param {string} languageCode
		 * @return {string} The autonym
		 */
		getAutonym: function ( languageCode ) {
			return $.ime.languages[ languageCode ] &&
				$.ime.languages[ languageCode ].autonym;
		},

		/**
		 * Decide on initial language to select
		 * @return {string}
		 */
		decideLanguage: function () {
			console.log("decideLanguage")
			return $.ime.preferences.getDefaultLanguage();
		},

		/**RAJEEV
		 * Select an input method
		 *
		 * @param {string} inputmethodId
		 */
		selectIM: function ( inputmethodId ) {
			console.log("selectIM: " + inputmethodId)
			var imeselector = this,
				ime;

			if ( !inputmethodId ) {
				return;
			}

			this.$menu.find( '.ime-checked' ).removeClass( 'ime-checked' );
			this.$menu.find( 'li[data-ime-inputmethod=' + inputmethodId + ']' )
				.addClass( 'ime-checked' );
			ime = this.$element.data( 'ime' );

			if ( inputmethodId === 'system' ) {
				this.disableIM();//RAJEEV
				return;
			}
			// Load the language rules js file
			ime.load( inputmethodId ).done( function () {
				console.log("ime.load")
				imeselector.inputmethod = $.ime.inputmethods[ inputmethodId ];
				imeselector.hide();
				ime.enable();
				ime.setIM( inputmethodId );

				imeselector.$imeSetting.find( 'a.ime-name' ).text(
					$.ime.sources[ inputmethodId ].name
				);
				imeselector.$imeSetting.find( 'a.ime-name' ).data('ime-inputmethod', inputmethodId);//CHECK

				imeselector.position();

			} );
		},

		/**RAJEEV
		 * Disable the inputmethods (Use the system input method)
		 */
		disableIM: function () {
			console.log("disableIM")
			this.$menu.find( '.ime-checked' ).removeClass( 'ime-checked' );
			this.$menu.find( 'div.ime-disable' ).addClass( 'ime-checked' );
			this.$element.data( 'ime' ).disable();
			this.$imeSetting.find( 'a.ime-name' ).text( '' );
			this.hide();
			this.position();

		},

		/**
		 * Prepare input methods in menu for the given language code
		 *
		 * @param {string} languageCode
		 */
		prepareInputMethods: function ( languageCode ) {
			console.log("prepareInputMethods: " + languageCode)
			var language = $.ime.languages[ languageCode ],
				$imeList = this.$menu.find( '.ime-list' ),
				imeSelector = this;

			$imeList.empty();

			$.each( language.inputmethods, function ( index, inputmethod ) {
				var $imeItem, $inputMethod, source, name;

				source = $.ime.sources[ inputmethod ];
				if ( !source ) {
					return;
				}
				name = source.name;

				$imeItem = $( '<a>' )
					.attr( 'href', '#' )
					.text( name )
					.addClass( 'selectable-row-item' );

				$inputMethod = $( '<li>' )
					.attr( 'data-ime-inputmethod', inputmethod )
					.addClass( 'ime-im selectable-row' )
					.append( '<span class="ime-im-check"></span>', $imeItem );

				$imeList.append( $inputMethod );
			} );
		},

	};

	IMESelector.defaults = {
		defaultLanguage: 'en',
	};

	/*
	 * imeselector PLUGIN DEFINITION
	 */

	$.fn.imeselector = function ( options ) {
		return this.each( function () {
			var $this = $( this ),
				data = $this.data( 'imeselector' );

			if ( !data ) {
				$this.data( 'imeselector', ( data = new IMESelector( this, options ) ) );
			}

			if ( typeof options === 'string' ) {
				data[ options ].call( $this );
			}
		} );
	};

	$.fn.imeselector.Constructor = IMESelector;

	selectorTemplate = '' +
	'<div class="imeselector imeselector-toggle action-button">' +
		'<span class="" style="color: #1a73e8; font-weight: 500; margin-right:8px;">हिन्दी</span>' +
		'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" style="margin-right:8px;">' +
		  '<path d="M20 5H4c-1.1 0-1.99.9-1.99 2L2 17c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm-9 3h2v2h-2V8zm0 3h2v2h-2v-2zM8 8h2v2H8V8zm0 3h2v2H8v-2zm-1 2H5v-2h2v2zm0-3H5V8h2v2zm9 7H8v-2h8v2zm0-4h-2v-2h2v2zm0-3h-2V8h2v2zm3 3h-2v-2h2v2zm0-3h-2V8h2v2z"/>' +
		  '<path d="M0 0h24v24H0zm0 0h24v24H0z" fill="none"/>' +
		'</svg>' +
		'<a class="ime-name imeselector-toggle" href="#"></a>' +
		'<b class="ime-setting-caret imeselector-toggle"></b>' +
	'</div>';

	MutationObserver = window.MutationObserver ||
		window.WebKitMutationObserver ||
		window.MozMutationObserver;

	function isDOMAttrModifiedSupported() {
		var p = document.createElement( 'p' ),
			flag = false;

		if ( p.addEventListener ) {
			p.addEventListener( 'DOMAttrModified', function () {
				flag = true;
			}, false );
		} else if ( p.attachEvent ) {
			p.attachEvent( 'onDOMAttrModified', function () {
				flag = true;
			} );
		} else {
			return false;
		}

		p.setAttribute( 'id', 'target' );

		return flag;
	}

	$.fn.attrchange = function ( callback ) {
		var observer;

		if ( MutationObserver ) {
			observer = new MutationObserver( function ( mutations ) {
				mutations.forEach( function ( e ) {
					callback.call( e.target, e.attributeName );
				} );
			} );

			return this.each( function () {
				observer.observe( this, {
					subtree: false,
					attributes: true
				} );
			} );
		} else if ( isDOMAttrModifiedSupported() ) {
			return this.on( 'DOMAttrModified', function ( e ) {
				callback.call( this, e.originalEvent.attrName );
			} );
		} else if ( 'onpropertychange' in document.body ) {
			return this.on( 'propertychange', function () {
				callback.call( this, window.event.propertyName );
			} );
		}
	};
}( jQuery ) );
