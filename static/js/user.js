'use strict';

// declare global user variable
var user = $('#user-id').html();
var points = $('#points').html();
var aim = $('#thing-cost').html();
console.log((points));
console.log((aim));

document.addEventListener('DOMContentLoaded', function() {
    // name parent divs
    var parentCanvas = $('#myCharts');
    var parentDiv = $('#to-complete-goals');
    var parentDivComplete = $('#completed-goals');
    makeDoughnut(result.goal_id, parseInt(aim) - parseInt(points), parseInt(points));
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
            var chartDiv = $('<canvas>').attr({'class': 'chart',
                                            'id': 'chart-' + goal.goal_id,
                                            'height': 200,
                                            'width': 200,
            });
            
            goalDiv.html(goal.goal_text);
            parentCanvas.append(chartDiv);
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
            // name variable that gives back goal num
            var goal_id = objs;
            var points_left = 0;
            var earned_points = 0;
            // var points_left = ($('#thing_cost').html()) - ($('#points').html());
            // var earned_points = ($('#points').html();
            // makeDoughnut(goal_id, earned_points, points_left);
            var same = [];
            for (var goal of objs_dict[goal_id]) {
                if (same === []) {
                    same = goal.goal_id;
                    if (goal.complete === true) {
                        earned_points += goal.point_cost;
                    } else {
                        points_left += goal.point_cost;
                    }
                } else if (same === goal.goal_id) {
                    if (goal.complete === true) {
                        earned_points += goal.point_cost;
                    } else if (goal.complete === false) {
                        points_left += goal.point_cost;
                    }
                } else {
                    // makeDoughnut(same, earned_points, points_left);
                    if (goal.complete === true) {
                        earned_points += goal.point_cost;
                    } else if (goal.complete === false) {
                        points_left += goal.point_cost;
                    }
                }
          
                
            } // end for goal of goal_id loop

            // name var that gives back objective array
            var obj_array = objs_dict[objs];
            // loop over each set of data in the obj_array
            for (var item of obj_array) {
                
                // create elements with corresponding objective id
                var objDiv = $('<div>').attr({'class': 'objective',
                                              'id': 'objDiv' + item.obj_id});
                var radio = $('<input>').attr({'type': 'radio',
                                                 'name': 'objRadio',
                                                 'value': item.obj_id,
                                                 'class': 'to-complete',
                                                 'id': 'objRadio' + item.obj_id});
                var checkbox = $('<input>').attr({'type': 'checkbox',
                                             'name': 'objCheck',
                                             'value': item.obj_id,
                                             'id': 'objCheck' + item.obj_id,
                                             'checked': 'checked',
                                             'class': 'completed',
                                             'disabled': 'disabled'});
                // add radio to objective div if false, else checkbox
                if (item.complete === true) {
                    objDiv.html(checkbox);
                } else {
                    objDiv.html(radio);
                }
                // append the text of the objective
                objDiv.append(item.obj_text);
                var date = item.due_date;
                objDiv.append(' I will do this by: ' + date.slice(0,10));
                // append to the corresponding goaldiv
                var newDiv = $('#goalDiv-' + goal_id);
                newDiv.append(objDiv);


                // set up data for chart
                // if (goal.complete === true) {
                //     earned_points += goal.point_cost;
                // } else {
                //     points_left += goal.point_cost;
                // }
                // console.log(earned_points);
                // var stats = [earned_points, points_left];
                // makeDoughnut(goal.goal_id, stats);

            }  // end for loop for every item in array
        }  // end for loop for keys
    });  // end get request

}, {passive: false});

// this function updates objective and calls update goal when all objs completed
function updateObjective(evt) {
    evt.preventDefault();

    // package up data
    var formInputs = {
        'obj_id': $('form input[type=radio]:checked').val(),
        'complete': 'True',
        'user_id': user,
    };

    // post request to update obj
    $.post('/user/obj/update.json',
            formInputs,
            function(result) {
                console.log(result);
                alert('Your objective has been updated. Congrats!');
                // replace radio with checkbox, add to completed class
                $('form input[type=radio]:checked').replaceWith('<input type="checkbox" class="objective completed" checked disabled>');
                // for ui, change color of text
                $("#to-complete-goals .goal:not(:has(input[type=radio]))").css('color', '#e7efd2');
                // if a goaldiv has no radio buttons, call updateGoal with goal id passed in
                makeDoughnut(result.goal_id, parseInt(aim) - parseInt(points), parseInt(points));
                if ($('#goalDiv-' + result.goal_id).find(':radio').length === 0) {
                    updateGoal(result.goal_id);
                } // end if
    }); // end post
} // end updateObjective function

// this function updates goal
function updateGoal(goal_id) {
    
    // package up data
    var formInputs = {
        'goal_id': goal_id,
        'complete': 'True',
        'user_id': user,
    };

    // post request to update goal
    $.post('/user/goal/update.json',
        formInputs,
        function(result) {
            console.log(result);
            alert('Congrats, you completed your goal!');
        });

} // end updateGoal function

// event listener on update button
$('#update-objective-button').on('click', updateObjective);

