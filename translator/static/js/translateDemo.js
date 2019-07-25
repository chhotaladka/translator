var translator = translator || {};
$(document).ready(function(){
  translator = {
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
        },/* end getCookie */
        
    csrfSafeMethod : function(method){
          return(/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
      },/* end csrfSafeMethod */
    
    handleAjaxError : function(xhRequest, ErrorText, thrownError){
          //alert( "Sorry, there was a problem!" );
          console.log( "Error: " + thrownError );
          console.log( "Status: " + ErrorText );
          console.dir( xhRequest );
      },
    
    addTranslateButton: function(){
      console.log('Adding translate button to DOM');
      
      cancelButton = $('input[name="cancelbutton"]');
      tdElement = cancelButton.closest('td');
      tdElement.after("<td align='center'><input id='translateButton' type='button'  name='translateButton' value='Translate'/></td>");
      $('#translateButton').on("click", translator.translate);
      
      return(false);
    },
    
    renderTranslation: function(response){
        console.log(response);
        
        text = response['text']+'\n\n********\n\n'+response['translation'];
        $('#body').val(text);
    },
    
    translate: function(event){
      console.log('Translating...');
      
      event.preventDefault();
      text = $('#body').val();
      
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
    }
  };
  
  translator.csrftoken = translator.getCookie('csrftoken');
  
  translator.addTranslateButton();
});
