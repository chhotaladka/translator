// Translator APIs
var translator = {
  urls: { 'translate': '/rest/translate/',
          'save': '/rest/save/'
      },
  save_method: 'POST',

  getCookie : function(name){
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

  enableTranslateButton: function(buttonId){
    console.log('Enabling translate button at ' + buttonId);
    document.getElementById(buttonId).addEventListener( 'click', translator.translate);
    return(false);
  },

  enableSaveButton: function(buttonId){
    console.log('Enabling Save button at ' + buttonId);
    document.getElementById(buttonId).addEventListener( 'click', translator.saveTranslation);
    return(false);
  },

  renderTranslation: function(response){
      console.log(response);

      if ($('form').has('iframe').length == 0){
        text = response['text']+'\n\n********\n\n'+response['translation'];
        $('#body').val(text);
      }
      else{
        text = response['text']+'<br/><br/>********<br/><br/>'+response['translation'];
        iframe = $('iframe').contents();
        iframe.find("body").html(text);
      }
  },

  _translate: function(){
    console.log('Translating...');

    var text = '';
    //console.log($('iframe'));
    if ($('form').has('iframe').length == 0){
      //console.log('Here')
      text = $('#body').val();
      //console.log(text);
      if (text.indexOf('********') > 0){
        //console.log(text.indexOf('********'));
        text = text.slice(0, text.indexOf('********'));
      }
    }
    else{
      iframe = $('iframe').contents();
      text = iframe.find("body").html();
    }
    //console.log('text:'+text)
    if (text.length >0){
      data = {'text': text};
      $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!translator.csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", translator.csrftoken);
                    }
                }
            });
      $.ajax({
              cache: false,
              url : translator.urls.translate,
              type: translator.save_method,
              dataType : "json",
              contentType: "application/json;",
              data : JSON.stringify(data),
              context : this,
              success : translator.renderTranslation,
              error : translator.handleAjaxError
            });
    }

    return(false);
  },

  translate: function(event){
    event.preventDefault();
    translator._translate();
    return(false);
  },

  saveTranslation: function(event){
    console.log('Saving...');

    event.preventDefault();
    text = $('#body').val();
    src = text.slice(0, text.indexOf('********'));
    dest = text.slice(text.indexOf('********')+'********'.length, text.length);
    console.log('Text: '+src.trim());
    console.log('Translation: '+dest.trim());

    if (text.length >0){
      data = {'text': src,
              'translation': dest};
      $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!translator.csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", translator.csrftoken);
                    }
                }
            });
      $.ajax({
              cache: false,
              url : translator.urls.save,
              type: translator.save_method,
              dataType : "json",
              contentType: "application/json;",
              data : JSON.stringify(data),
              context : this,
              success : function(response){console.log('Saved.')},
              error : translator.handleAjaxError
            });
    }

    return(false);
  }
};

translator.csrftoken = translator.getCookie('csrftoken');

// https://stackoverflow.com/a/14042239/1157639
//
// $('#element').donetyping(callback[, timeout=1000])
// Fires callback when a user has finished typing. This is determined by the time elapsed
// since the last keystroke and timeout parameter or the blur event--whichever comes first.
//   @callback: function to be called when even triggers
//   @timeout:  (default=1000) timeout, in ms, to to wait before triggering event if not
//              caused by blur.
// Requires jQuery 1.7+
//
;(function($){
    console.log('Typing event enter');

    $.fn.extend({
        donetyping: function(callback,timeout){
            console.log('Extending...');
            timeout = timeout || 1e3; // 1 second default timeout
            var timeoutReference,
                doneTyping = function(el){
                    console.log('doneTyping...');
                    if (!timeoutReference) return;
                    timeoutReference = null;
                    callback.call(el);
                };
            return this.each(function(i,el){
                var $el = $(el);
                // Chrome Fix (Use keyup over keypress to detect backspace)
                // thank you @palerdot
                $el.is(':input') && $el.on('keyup keypress paste',function(e){
                    // This catches the backspace button in chrome, but also prevents
                    // the event from triggering too preemptively. Without this line,
                    // using tab/shift+tab will make the focused element fire the callback.
                    if (e.type=='keyup' && e.keyCode!=8) return;

                    // Check if timeout has been set. If it has, "reset" the clock and
                    // start over again.
                    if (timeoutReference) clearTimeout(timeoutReference);
                    timeoutReference = setTimeout(function(){
                        // if we made it here, our timeout has elapsed. Fire the
                        // callback
                        doneTyping(el);
                    }, timeout);
                }).on('blur',function(){
                    // If we can, fire the event since we're leaving the field
                    doneTyping(el);
                });
            });
        }
    });
})(jQuery);

$('#body').donetyping(function(event){
  console.log('Event last fired @ ' + (new Date().toUTCString()));
  translator._translate();
});
