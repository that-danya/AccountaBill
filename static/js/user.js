'use strict';

// for each goal in user.goal
    // if not goal.complete:
        // for objective in goal.objective:
            // if not objective.complete:

                // insert radio with id of 'obj'+obj_id
                // objective.obj_text
            // else:
                // disabled, checked radio
                // objective.obj_text
                // add class = 'completed-obj'
    // else:
        // put goal in Completed Goals section with corresponding objectives.
        // ? add how much earned back

////////////////////////////////////////////
var user = $('#user-id').html();

document.addEventListener('DOMContentLoaded', function() {
    var parentDiv = $('#to-complete-goals');
    var parentDivComplete = $('#completed-goals');
    
    // var user = $('#user-id').html();

    // get user page, json data
    $.get('/user/'+ user +'.json', function(results){
        // set variables
        var objs_dict = results.objectives;
        var goals = results.goals;

        // loop over goals, create div + append to parent
        for (var goal of goals) {
            // create div to append
            var goalDiv = $('<div>').attr({'class': 'goal',
                                  'id': 'goalDiv-' + goal.goal_id,
            });
            goalDiv.html(goal.goal_text);
            // if goal not complete, append div to parent,
            // else append to parentComplete
            if (goal.complete === false) {
                parentDiv.append(goalDiv);
            } else {
                parentDivComplete.append(goalDiv);
            }

        };

        // loop over object-objs_dict to get keys
        for (var objs of Object.keys(objs_dict)) {
            var goal_id = objs; // this gives back goal num

            var obj_array = objs_dict[objs]; // this gives back objective array
            
            // loop over each set of data in the obj_array
            for (var item of obj_array) {
                
                // create elements with corresponding objective id
                var objDiv = $('<div>').attr({'class': 'objective',
                                              'id': 'objDiv' + item.obj_id});
                var radio = $('<input>').attr({'type': 'radio',
                                                 'name': 'objRadio',
                                                 'value': item.obj_id,
                                                 'id': 'objRadio' + item.obj_id});
                var checkbox = $('<input>').attr({'type': 'checkbox',
                                             'name': 'objCheck',
                                             'value': item.obj_id,
                                             'id': 'objCheck' + item.obj_id,
                                             'checked': 'checked',
                                             'disabled': 'disabled'});
                // add radio to objective div
                if (item.complete === true) {
                    objDiv.html(checkbox);
                } else {
                    objDiv.html(radio);
                }
                // append the text of the objective
                objDiv.append(item.obj_text);
                // append that div to the corresponding goaldiv
                var newDiv = $('#goalDiv-' + goal_id);
                newDiv.append(objDiv);
            };
        };

    });


}, false);

function updateData (evt) {
    evt.preventDefault();
    updateObjective();
    updateGoal();
}

function updateObjective() {
    var self = $('form input[type=radio]:checked');

    var formInputs = {
        'obj_id': $('form input[type=radio]:checked').val(),
        'complete': 'True',
        'user_id': user,
    };

    $.post('/user/update.json',
           formInputs,
           function(result){
           console.log(result);
           alert('Your objective has been updated. Congrats!');
           $('form input[type=radio]:checked').replaceWith('<input type="checkbox" class=objective checked disabled>');
           });

    $("#to-complete-goals .goal:not(:has(input[type=radio]))").addClass('completed').css('color', 'gray');

}

function updateGoal(){

    var formInputs = {
        'goal_id': $('.completed').attr('id').split('-')[1],
        'complete': 'True',
        'user_id': user,
    };

    $.post('/user/goal/update.json',
        formInputs,
        function(result) {
        alert('Congrats, you completed your goal!');
        });

    $("#to-complete-goals .goal:not(:has(input[type=radio]))").addClass('completed').css('color', 'gray');
}

$('#update-objective-button').on('click', updateData);

// function getObjText

// function getGoalId

// function getGoalText