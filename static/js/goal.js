'use strict';

    // on click, add objective element to form
    $(document).on('click', '#objective-button', function() {
        
        // get jQuery DOM elements to use in function
        // set variable name to parent div
        var parentDiv = $('#objective-holder');
        // counter
        var totalObjField = $('#obj-counter');

        // get data from DOM to use
        var totalObj = Number(totalObjField.val()) + 1;
        // reflect totalObj in hidden field
        totalObjField.val(totalObj);

        // create div
        var objDiv = $('<div>').attr({'class': 'objective',
                                      'id': 'objective' + totalObj});
        var objAction = $('<input>').attr({'class': 'objective',
                                           'type': 'text',
                                           'value': 'do',
                                           'id': 'obj-action' + totalObj,
                                           'required' : ''});
        var objNoun = $('<input>').attr({'class': 'objective',
                                         'type': 'text',
                                         'id': 'obj-noun' + totalObj,
                                         'value': 'something',
                                         'required' : ''});
        var objCheck = $('<input>').attr({'class': 'objective',
                                          'type': 'checkbox',
                                          'id': 'obj-noun' + totalObj});
        var objDate = $('<input>').attr({'class': 'objective',
                                         'type': 'date',
                                         'id': 'obj-noun' + totalObj,
                                         'required' : ''});
        
        objDiv.append('I will ');
        objDiv.append(objAction);
        objDiv.append(objNoun);
        objDiv.append('<br>');
        objDiv.append('Daily? If yes, check the box');
        objDiv.append(objCheck);
        objDiv.append('<br>');
        objDiv.append('I will accomplish this by/until: ');
        objDiv.append(objDate);
        objDiv.append('<br><br>');

        // append div to end of parent
        parentDiv.append(objDiv);

        // // more var
        // var contentAttributes
        // var objNum = totalObj;

        // contentAttributes = {
        //     'type': 'text',
        //     'name': 'objective' + objNum
        //     // 'value': 'do/something/date'
        // };
        // contentAttributes.attr()


    });
// $('#objective-button').on('click', function() {
//     console.log('yay!');
// });


// // counter variable
// var totalObjective = 0;
// // on click, run function
// $(document).on('click', '.objective-button', function() {
//     console.log('YAY!')
//     // increment counter
//     var objectNum = totalObjective + 1;
//     // set variable for what is being created
//     var createDiv = $(document.createElement('div'));
//         // set variable for total num of objective elements
//         // var objTotalField = $('#obj-num-total');
//         // var totalObj = Number(objTotalField.val() + 1);
//     // var for id tag, add to div
//     var objId = 'objective' + objectNum;
//     createDiv.attr('id', objId);
//     // insert html for div
//     createDiv.html("<label>Objective:<br>" + "
//         <span>I will <input type='text' name='obj-action" + objectNum +"' required value='do'/>" + " 
//         <input type='text' name='obj-noun" + objectNum +"' required value='something'/>" + " 
//         (Daily? Check the box.)" + "
//         <input type='checkbox' name='daily" + objectNum +"' checked value='yes_daily'/>" + "<br>" + "
//         I will accomplish this by: <input type='date' name='obj-date" + objectNum +"' required min='2017-08-07'/></span>" + "
//         <!--  TODO: THIS IS HARDCODED, NEED TO UPDATE WITH ARROW?DATETIME -->" + "
//     </label>
//     ");
 


//     contentAttributes = {
//     'type': 'text',
//     'name': 'objective' + objectNum
//     // 'value': 'do/something/date'
//     };

// });
















