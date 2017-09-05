'use strict';
//function makeDoughnut(thing_cost, points) {
function makeDoughnut(goal_id, data1, data2) {
// $(document).on('ready', function () {
    var options = { // these are default values
        responsive: true,
        cutoutPercentage: 75,
        animationSteps: 100,
        animationEasing: "easeOutBounce",
        animateRotate: true,
        animateScale: false,
        maintainAspectRatio: false,
    };

// var myChart = new Chart(ctx, {...});
// var ctx = $("#chartDiv-" + result.goal_id);
    var data = {
        datasets: [{
            label: "Goal",
            backgroundColor: ['rgba(225,185,81, 0.8)',
                               'rgba(43,42,0, 0.6)' ,
                               '#731f0a'],
            data: [data1, data2]
            //data: [points, (thing_cost - points)]
        }],

        // These labels appear in the legend and in the tooltips when hovering different arcs
        labels: [
            'Poins to earn',
            'Poins earned'
        ]
    };

    var ctx = $('#myCharts')[0].getContext('2d');
    // var ctx = $('chart-' + goal_id)[0].getContext('2d');

    ctx.canvas.width = 200;
    ctx.canvas.height = 200;

    // And for a doughnut chart
    var myDoughnutChart = new Chart(ctx, {
        type: 'doughnut',
        data: data,
        options: options,
        
    });
}

// });