'use strict';

    // on click, add objective element to form
    $(document).on('click', '#objective-button', function() {

        // get jQuery DOM elements to use in function
        // set variable name to parent div
        var parentDiv = $('#objective-holder');
        // counter
        var totalObjField = $('#obj-counter');
        var click = 0;
        click ++;
        var points = $('#points');
        console.log(points);

        // if objCounter> points, disable button
        if (Math.floor($('#points').val()) < (Math.floor($('#obj-counter').val()))) {
            $('#objective-button').prop("disabled", true);
        }

        // get data from DOM to use
        var totalObj = Number(totalObjField.val()) + 1;
        // reflect totalObj in hidden field
        totalObjField.val(totalObj);

        // create div
        var objDiv = $('<div>').attr({'class': 'objective col-md-4 form group',
                                      'id': 'objective' + totalObj});
        var objAction = $('<input>').attr({'class': 'objective form-control input-md',
                                           'type': 'text',
                                           'placeholder': 'do',
                                           'name': 'obj-action' + totalObj,
                                           'id': 'obj-action' + totalObj,
                                           'required' : ''});
        var objNoun = $('<input>').attr({'class': 'objective form-control input-md',
                                         'type': 'text',
                                         'id': 'obj-noun' + totalObj,
                                         'placeholder': 'something',
                                         'name': 'obj-noun' + totalObj,
                                         'required' : ''});
        var objCheck = $('<input>').attr({'class': 'objective form-control input-md',
                                          'type': 'checkbox',
                                          'name': 'obj-check' + totalObj,
                                          'id': 'obj-check' + totalObj});
        var objDate = $('<input>').attr({'class': 'objective form-control input-md',
                                         'type': 'date',
                                         'name': 'obj-date' + totalObj,
                                         'id': 'obj-date' + totalObj,
                                         'required' : ''});
        
        objDiv.append('I will ');
        objDiv.append(objAction);
        objDiv.append(objNoun);
        objDiv.append('<br>');
        //objDiv.append('Daily? If yes, check the box');
        //objDiv.append(objCheck);
        objDiv.append('<br>');
        objDiv.append('I will accomplish this by: ');
        objDiv.append(objDate);
        objDiv.append('<br><br>');

        // append div to end of parent
        parentDiv.append(objDiv);

    });
