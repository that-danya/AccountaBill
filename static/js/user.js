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


// on window load


// pipe in var continaing total obj connected to user


// $(window).load(function(){
//     var userObjTotal = 

//     $.get('/user/<int:user_id>.json', function(){


//     for (var i=0; i<=range(1, userObjTotal); i++){
//         var objectiveDiv = $('#to-complete-goals');
//         // TODO add in value="obj_text"
//         objectiveDiv.append("<input type='checkbox' id='obj"+i+"'>");
//         objectiveDiv.append(value=USER_OBJECTIVE_HERE);
//     };

//     });
// });

////////////////////////////////////////////



document.addEventListener('DOMContentLoaded', function() {
    var parentDiv = $('#to-complete-goals');
    parentDiv.append('made it!');
    
    // // create div to append
    // var objDiv = $('<div>').attr({'class': 'objective',
    //                               'id': 'objective' + OBJIDNEEDED,
    // });
    // // checkbox to append
    // var objDivBox = $('<input>').attr({'class': 'objective', 
    //                                    'type': 'checkbox'
    //                                    'name': 'objective-box' + OBJIDNEEDED, 
    //                                    'id': 'objective-box' + OBJIDNEEDED
    // });
    // var objText = $('<div>').attr({'value': 'TEXTGOESHERE',
    //                                'id':

    // });

    // objDiv.append(objDivBox);
    // objDiv.append(objText);

    // // append to parent
    // parentDiv.append(objDiv);

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
            console.log(objs) // this gives back goal num
            var obj_objects = objs_dict[objs]; // this gives back obj object
            for (var obj_keys of Object.keys(obj_objects)) {
                console.log(obj_keys);
            };

            // create Div
            var objDiv = $('<div>').attr({'class': 'objective',
                                  'id': 'objDiv' + objs.obj_id,
            });
            // console.log(objs.obj_id); this is undefined
            objDiv.html(objs.obj_text);
            parentDiv.append(objDiv);
        };

    });


}, false);


// $(window).load(function(){
//     function getObjId(results) {
//         console.log('objectives');
//     }
// });

// function getObjText

// function getGoalId

// function getGoalText