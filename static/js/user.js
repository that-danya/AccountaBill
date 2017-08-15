'use strict';

// for each goal in user.goal
    // if not goal.complete:
        // for objective in goal.objective:
            // if not objective.complete:

                // insert checkbox with id of 'obj'+obj_id
                // objective.obj_text
            // else:
                // disabled, checked checkbox
                // objective.obj_text
                // add class = 'completed-obj'
    // else:
        // put goal in Completed Goals section with corresponding objectives.
        // ? add how much earned back

////////////////////////////////////////////



document.addEventListener('DOMContentLoaded', function() {
    var parentDiv = $('#to-complete-goals');
    
    var user = $('#user-id').html();

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

        // loop over objectives, + append div to goalDiv
        for (var objs of Object.keys(objs_dict)) {
            var goal_id = objs // this gives back goal num
            var obj_array = objs_dict[objs]; // this gives back obj object
            
            // create Div
            for (var item of obj_array) {
                console.log(item.obj_text);
                var objDiv = $('<div>').attr({'class': 'objective',
                                              'id': 'objDiv' + item.obj_id});
                objDiv.html(item.obj_text);
                var newDiv = $('#goalDiv' + goal_id);
                newDiv.append(objDiv);
                parentDiv.append(newDiv);
            };
        };

    });


}, false);


// function getObjText

// function getGoalId

// function getGoalText