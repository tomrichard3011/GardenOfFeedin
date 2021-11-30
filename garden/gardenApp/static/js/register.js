//(function() {
//    $('form input').keyup(function() {
//
//        var empty = false;
//        $('form input').each(function() {
//            if ($(this).val() == '') {
//                empty = true;
//            }
//        });
//
//        if (empty) {
//            $('#register').attr('disabled', 'disabled'); // updated according to http://stackoverflow.com/questions/7637790/how-to-remove-disabled-attribute-with-jquery-ie
//        } else {
//            $('#register').removeAttr('disabled'); // updated according to http://stackoverflow.com/questions/7637790/how-to-remove-disabled-attribute-with-jquery-ie
//        }
//    });
//})()
//
//// form validation: make sure all fields are filled 
//// source: https://stackoverflow.com/questions/65173448/disable-submit-button-with-jquery-until-field-and-at-least-one-chceckbox-have-va?noredirect=1&lq=1
//$(function() {
//    $('.form-register').on('input',function() {
//        console.clear() // Just for this demo...
//    
//        var email = $('.form-register.required.email').filter((i,el)=>el.value!=="");
//        
//		console.log("email",email.length)
//        
//        var my_condition = email.length>0 && checkboxes.length>0
//        console.log(my_condition)
//        $('.form-register :submit').prop('disabled',!my_condition);
//    });
//});


