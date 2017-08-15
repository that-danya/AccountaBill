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
                                  'id': 'goalDiv' + goal.goal_id,
            });
            goalDiv.html(goal.goal_text);
            parentDiv.append(goalDiv);
        };

        // loop over object-objs_dict to get keys
        for (var objs of Object.keys(objs_dict)) {
            var goal_id = objs // this gives back goal num
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
                // add radio to objective div
                objDiv.html(radio);
                // append the text of the objective
                objDiv.append(item.obj_text);
                // append that div to the corresponding goaldiv
                var newDiv = $('#goalDiv' + goal_id);
                newDiv.append(objDiv);
                // append it to the main div
                parentDiv.append(newDiv);
            };
        };

    });


}, false);

function updateObjective(evt) {
    evt.preventDefault();

    var formInputs = {
        'obj_id': $('form input[type=radio]:checked').val(),
        'complete': 'True',
    };

    $.post('/user/update.json',
           formInputs,
           function(result){
           console.log(result);
           alert('Your objective has been updated. Congrats!');
           });
}

$('#update-objective-button').on('click', updateObjective);

// function getObjText

// function getGoalId

// function getGoalText