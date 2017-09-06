'use strict';

// declare global user variable
var user = $('#user-id').html();
var points = $('#points').html();
var aim = $('#thing-cost').html();


document.addEventListener('DOMContentLoaded', function() {
    // name parent divs
    var parentCanvas = $('#myCharts');
    var parentDiv = $('#to-complete-goals');
    var parentDivComplete = $('#completed-goals');
    
    // get user page, json data
    $.get('/user/'+ user +'.json', function(results){
        // set variables
        var objs_dict = results.objectives;
        var goals = results.goals;
        makeDoughnut(results.goal_id, parseInt(aim) - parseInt(points), parseInt(points));

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
                objDiv.append(" " + item.obj_text);
                // var date = item.due_date;
                // objDiv.append(' I will do this by: ' + date.slice(0,10));
                // append to the corresponding goaldiv
                var newDiv = $('#goalDiv-' + goal_id);
                newDiv.append(objDiv);

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
                alert('Your objective has been updated. Congrats!');
                // replace radio with checkbox, add to completed class
                $('form input[type=radio]:checked').replaceWith('<input type="checkbox" class="objective completed" checked disabled>');
                // for ui, change color of text
                $("#to-complete-goals .goal:not(:has(input[type=radio]))").css('color', '#e7efd2');
                // if a goaldiv has no radio buttons, call updateGoal with goal id passed in
                // removeData(($('#chart' + result.goal_id)));
                // console.log(($('#chart' + result.goal_id)));
                // aim = parseInt(aim) + parseInt(result.point_cost);
                points = parseInt(points) + parseInt(result.point_cost);
                
                makeDoughnut(result.goal_id, parseInt(aim) - points, points);
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
            alert('Congrats, you completed your goal!');
        });

} // end updateGoal function

// event listener on update button
function removeData(chart) {
    chart.data.labels.pop();
    chart.data.datasets.forEach((dataset) => {
        dataset.data.pop();
    });
    chart.update();
}

$('#update-objective-button').on('click', updateObjective);

