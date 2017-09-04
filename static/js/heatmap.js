'use strict';

// d3 heatmap derived from tutorial from CAX Mohan S on CrowdAnalytix 

// declare variables
var width = 900,
    height = 105,
    cellSize = 12; // cell size
    week_days = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']
    month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

var day = d3.time.format("%w"),
    week = d3.time.format("%U"),
    percent = d3.format(".1%"),
    format = d3.time.format("%Y%m%d");
    parseDate = d3.time.format("%Y%m%d").parse;

// select div, append svg and change attributes to chart, width, height
chart = d3.select('heatmap') 
        .append('svg')
        .attr('class', 'chart')
        .attr('width', width)
        .attr('height', height)

// style chart class with background and margin
.chart {
  background: #fff;
  margin: 5px;
}

// format data, convert date to js datetime object
var cellSize = 17
var percent = d3.format('.1%'), 
        format = d3.time.format('%Y%m%d');

// Add color range
var color = d3.scale.linear().range(['paper', '#fffbef'])
    .domain([0, 1])

// read data in from csv file