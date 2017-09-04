'use strict';

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
            backgroundColor: ['rgb(149, 255, 214)',
                               'rgb(156, 43, 178)' ,
                               'rgb(247, 207, 59)'],
            data: [3, 3]
        }],

        // These labels appear in the legend and in the tooltips when hovering different arcs
        labels: [
            'Points earned',
            'Poins to earn'
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