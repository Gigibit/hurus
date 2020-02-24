var radarCharts = {};
const MIN_DAYS_FOR_CHART = 14;

function count(obj) { return Object.keys(obj).length; }


function barChart(chartDiv, data, relatedChart) {

	buff = []

	for (var i = 0; i < data.length; i++) {
		var d = data[i]
		buff[d.mood] = buff[d.mood] ? buff[d.mood] + 1 : 1
	}

	barData = []
	Object.keys(buff).forEach(function (key) {
		barData.push({
			key: key,
			value: buff[key]
		})
	});

	var margin = {
			top: 20,
			right: 20,
			bottom: 30,
			left: 40
		},
		width = window.innerWidth / 2.5, // Use the window's width
		height = window.innerHeight / 2.5; // Use the window's height

	// set the ranges
	var x = d3.scaleBand()
		.range([0, width])

		.padding(0.1);
	var y = d3.scaleLinear()
		.range([height, 0]);
	var maxValue = d3.max(barData, function (d) {
		return d.value;
	});

	// append the svg object to the body of the page
	// append a 'group' element to 'svg'
	// moves the 'group' element to the top left margin
	var svg = d3.select(chartDiv).append("svg")
		.attr("width", width + margin.left + margin.right)
		.attr("height", '400px')
		.append("g")
		.attr("transform",
			"translate(" + margin.left + "," + margin.top + ")");

	// format the data
	data.forEach(function (d) {
		d.sales = +d.sales;
	});

	// Scale the range of the data in the domains
	x.domain(barData.map(function (d) {
		return d.key;
	}));
	y.domain([0, maxValue]);
	// append the rectangles for the bar chart
	let bars = svg.selectAll(".bar")
		.data(barData)
		.enter()
		.append("g")
		bars.append("rect")
		.attr('fill', function(d){ return moods[d.key]['color']})
		.attr("class", "bar")
		.attr("x", function (d) {
			return x(d.key);
		})
		.attr("width", x.bandwidth())
		.attr("y", function (d) {
			return y(d.value);
		})
		.attr("height", function (d) {
			return height - y(d.value);
		})
		bars.append('text')
		.attr('class', 'bar-text')
		.attr("x", function (d) {
			return x(d.key) + x.bandwidth()/2;
		})
		.attr("y", function (d) {
			return (height+y(d.value))/2;
		})
		.text(function (d) {
			return d.value
		})


	// add the x Axis
	svg.append("g")
		.attr("transform", "translate(0," + height + ")")
		.attr('class', 'axis')
		.call(d3.axisBottom(x))
		.selectAll(".tick").each(function (d, i) {
			d3.select(this)
				.append('image')
				.attr('class', 'axis-image')
				.attr('xlink:href', moods[ d.mood && Math.round(d.mood.replace(",",".")) || d].icon)
				.attr("transform", "translate(-10 , 5)")
				.attr('y', 0)
				.attr('width', 20)
				.attr('height', 20)
				.attr('cursor', 'pointer')
				.on('click', (d) => updateChart(radarCharts[relatedChart], d, data))

		}); // Create an axis component with d3.axisLeft;

}


function lineChart(chartDiv, data) {
	if(diffBetweenDateInDays(data[0].date, data[data.length-1].date) < MIN_DAYS_FOR_CHART)
		throw new Exception('data evaluation unavailable')
	
	var margin = {
			top: 50,
			right: 50,
			bottom: 50,
			left: 50
		},
		width = window.innerWidth / 2.5 // Use the window's width
		,
		height = window.innerHeight / 2.5; // Use the window's height


	// 1. Add the SVG to the page and employ #2
	var svg = d3.select(chartDiv).append("svg")
		.attr("width", width + margin.left + margin.right)
		.attr("height", height + margin.top + margin.bottom)
		.append("g")
		.attr("transform", "translate(" + margin.left + "," + margin.top + ")");


	// gridlines in x axis function
	function make_x_gridlines() {
		return d3.axisBottom(xScale)
			.ticks(5)
	}

	// gridlines in y axis function
	function make_y_gridlines() {
		return d3.axisLeft(yScale)
			.ticks(5)
	}


	var minMood = d3.min(Object.keys(moods), d => d);
	var maxMood = d3.max(Object.keys(moods), d => d);

	var minDate = d3.max(data, function (d) {
		return d.date
	})
	var maxDate = new Date();

	// 5. X scale will use the index of our data
	var xScale = d3.scaleTime()
		.domain(d3.extent(data, function (d) {
			return d.date;
		}))
		// TODO: invert when data will be available
		.range([0, width]); // output

	// Create an axis component with d3.axisBottom
	var xAxis = svg.append('g')
		.attr("class", "x axis")
		.attr("transform", "translate(0," + height + ")")
		.call(d3.axisBottom(xScale)
			.ticks(5)
			.tickFormat(d3.timeFormat("%d %b")));

	// 6. Y scale will use the randomly generate number
	var yScale = d3.scaleLinear()
		.domain([minMood, maxMood]) // input
		.range([height, 1]); // output


	svg.on("dblclick", function () {
		d3.selectAll('.path-image').attr('display', 'auto')
		xScale.domain(d3.extent(data, function (d) {
			return d.date;
		}))
		xAxis.transition().call(d3.axisBottom(xScale).ticks(5)
			.tickFormat(d3.timeFormat("%d %b")))
		line.select('.line')
			.transition()
			.attr("d", d3.line()
				.x(function (d) {
					return xScale(d.date)
				})
				.y(function (d) {
					return yScale(d.mood)
				})
				.curve(d3.curveMonotoneX)
			)

	});
	// add the X gridlines
	svg.append("g")
		.attr("class", "grid")
		.attr("transform", "translate(0," + height + ")")
		.call(make_x_gridlines()
			.tickSize(-height)
			.tickFormat("")
		)

	// add the Y gridlines
	svg.append("g")
		.attr("class", "grid")
		.call(make_y_gridlines()
			.tickSize(-width)
			.tickFormat("")
		)

	// 4. Call the y axis in a group tag
	svg.append("g")
		.attr("class", "y axis")
		.call(d3.axisLeft(yScale).ticks(count(moods)))
		.selectAll(".tick").each(function (d, i) {

			d3.select(this)
				.append('image')
				.attr('class', 'axis-image')
				.attr('xlink:href', moods[d].icon)
				.attr("transform", "translate(-27 ,-12)")
				.attr('y', 0)
				.attr('width', 20)
				.attr('height', 20);
		}); // Create an axis component with d3.axisLeft


	d3.selectAll('.x.axis .tick text').attr('style', 'transform:rotateZ(270deg) translate(-15px, -12px)')

	// 9. Append the path, bind the data, and call the line generator
	svg.append("path")
		.datum(data) // 10. Binds data to the line
		.attr("class", "line") // Assign a class for styling
		.attr("d", line); // 11. Calls the line generator


	var clip = svg.append("defs").append("svg:clipPath")
		.attr("id", "clip")
		.append("svg:rect")
		.attr("width", width)
		.attr("height", height)
		.attr("x", 0)
		.attr("y", 0);

	// Add brushing
	var brush = d3.brushX() // Add the brush feature using the d3.brush function
		.extent([
			[0, 0],
			[width, height]
		]) // initialise the brush area: start at 0,0 and finishes at width,height: it means I select the whole graph area
		.on("end", updateChart) // Each time the brush selection changes, trigger the 'updateChart' function


	// A function that set idleTimeOut to null
	var idleTimeout

	function idled() {
		idleTimeout = null;
	}
	// 7. d3's line generator
	var line = svg.append('g')
		.attr("clip-path", "url(#clip)")
	// A function that update the chart for given boundaries
	function updateChart() {

		// What are the selected boundaries?
		extent = d3.event.selection

		// If no selection, back to initial coordinate. Otherwise, update X axis domain
		if (!extent) {
			if (!idleTimeout) return idleTimeout = setTimeout(idled, 350); // This allows to wait a little bit
			xScale.domain([4, 8])
		} else {
			xScale.domain([xScale.invert(extent[0]), xScale.invert(extent[1])])
			line.select(".brush").call(brush.move, null) // This remove the grey brush area as soon as the selection has been done
		}
		d3.selectAll('.path-image').attr('display', 'none')

		// Update axis and line position
		xAxis.transition().duration(1000).call(
			d3.axisBottom(xScale)
			.ticks(5)
			.tickFormat(d3.timeFormat('%H')))
		line
			.select('.line')
			.transition()
			.duration(1000)
			.attr("d", d3.line()
				.x(function (d) {
					return xScale(d.date)
				})
				.y(function (d) {
					return yScale(d.mood)
				})
				.curve(d3.curveMonotoneX)
			)
	}


	line.append("g")
		.attr("class", "brush")
		.call(brush);

	line.append("path")
		.datum(data)
		.attr("class", "line") // I add the class line to be able to modify this line later on.
		.attr("fill", "none")
		.attr("stroke", "steelblue")
		.attr("stroke-width", 1.5)
		.attr("d", d3.line()
			.x(function (d, i) {
				return xScale(d.date);
			}) // set the x values for the line generator
			.y(function (d) {
				return yScale(d.mood);
			}) // set the y values for the line generator
			.curve(d3.curveMonotoneX))
	// 12. Appends a circle for each datapoint
	svg.selectAll(".dot")
		.data(data)
		.enter().append("g") // Uses the enter().append() method
		.attr("class", "dot") // Assign a class for styling
		.attr("cx", function (d, i) {
			return xScale(d.date)
		})
		.attr("cy", function (d) {
			return yScale(d.mood)
		})
		.attr("r", 5)
		.each(function (d, i) {
			if (i % 7 != 0 && i % 7 != 6) return
			d3.select(this)
				.append('image')
				.attr('class', 'path-image')
				.attr('transform', 'translate(' +
					(Math.ceil(this.getAttributeNode("cx").value) - 12) + ',' +
					(Math.ceil(this.getAttributeNode("cy").value) - 4) + ')')
				.attr('xlink:href', moods[Math.round(d.mood)].icon)
				.attr('width', 20)
				.attr('height', 20);
		});

}


$('.freetime-mood-button').click(function(event){
	let mood = $(this).data('mood')
	updateChart(radarCharts['freetime-radar-chart'], mood, dataFreetime)
	updateChart(radarCharts['related-freetime-radar-chart'], mood, dataFreetime)

})

$('.workplace-mood-button').click(function(event){
	let mood = $(this).data('mood')
	updateChart(radarCharts['workplace-radar-chart'], mood, dataWorkPlace)
	updateChart(radarCharts['related-workplace-radar-chart'], mood, dataWorkPlace)
})

function updateChart(chart, selectedMood, _data) {
	if (chart != null) {
		let labels = getActivities(selectedMood, _data)
		let data = getDataForActivities(labels, selectedMood, _data)
		if (labels.length > 0 && data.length > 0) {
			chart.data.labels = labels
			chart.data.datasets[0].data = data
			chart.update()
			$(chart.canvas).show(500)
		}
		else{
			$(chart.canvas).hide(500)
			snackbar(i18n['NO_DATA'])
		}

	}
}

function diffBetweenDateInDays(date1, date2){
	const diffTime = Math.abs(date2 - date1);
	return Math.ceil(diffTime / (1000 * 60 * 60 * 24)); 
}


function configRadarChart(chartDiv, selectedMood, data) {
    var el = document.getElementById(chartDiv);

	let labels = getActivities(selectedMood, data) || []
	if(labels.length <= 0){
		return el.replaceWith('<div class="wip-warning"></div>')
	}
	var context = el.getContext('2d');
    let datasetData = getDataForActivities(labels, selectedMood, data)
	var causeEffectChartData = {
		labels: [' '].concat(labels),
		datasets: [{
            scaleOverride: true,
            scaleSteps: 5,
            scaleStepWidth: 5,
            scaleStartValue: 0,
            pointLabelFontSize: 16,
            fillColor: "rgba(0,120,0,0.2)",
            strokeColor: "rgba(0,120,0,1)",
            pointColor: "rgba(10,10,10,1)",
            pointStrokeColor: "#ccc",
            pointHighlightFill: "#333",
            pointHighlightStroke: "rgba(255,255,0,1)",
			backgroundColor: moods[selectedMood]['color'],
			data: [0].concat(datasetData)
		}]

	};
	radarCharts[chartDiv] = new Chart(context, {
		type: 'radar',
		data: causeEffectChartData,
		options: {
            wrapWidth: 60,
            levels: 5,
            roundStrokes: true,
			legend: {
				display: false
            },
            scale: {
                ticks: {
                    beginAtZero: true,
                    stepSize: 1
                }
            },
            tooltips: {
                enabled: false
            }
    
		}
    });

}

function activityRadarChart(chartDiv, selectedMood, data){
	var el = document.getElementById(chartDiv)
	if(data.length <= 0){
		return el.replaceWith('<div class="wip-warning"></div>')
	}
	console.log(data)
	let labels = getActivities(selectedMood, data)
	var relatedContext = el.getContext('2d');
    let datasetData = getDataForActivities(labels, selectedMood, data)
    var opt = {
        legend: {
            display: false
        },
        plugins: {
            datalabels: {
                clamp: true,
                align: 'center',
                anchor: 'center',
                font: {
                  size: 11,
                  weight: 700
                },
                offset: 8,
                color: 'white'
            }
        },
        scales:{
            xAxes: [{
                display: false, //this will remove all the x-axis grid lines
                ticks : {
                    beginAtZero: true
                }
            }],
        },
        tooltips: {
            enabled: false
        },
        maintainAspectRatio: false,

    };
	radarCharts[chartDiv] = new Chart(relatedContext, {
        type: 'horizontalBar',
        data: {
          labels: labels,
          datasets: [
            {
              backgroundColor: datasetData.map(d => randomRgba()),
              data: datasetData
            }
          ]
        },
        options: opt
    });
}



function getActivities(forMood, data) {
	activities = data.filter(t => forMood == t.mood)
		.flatMap(tought => tought.activities.map(opt => {
			return {
				'i18n_key': opt.i18n_key,
				'name': opt.name
			}
		}))
		.map(opt => opt.i18n_key || opt.name)

	return activities.filter((item, pos) => activities.indexOf(item) == pos)

}
function getDataForActivities(labels, forMood, data) {
	var result = []
	for (var i = 0; i < labels.length; i++) {
        let label = labels[i]
		result[i] = data.filter(t => {
			return t.activities.map(opt => {
				return {
					'i18n_key': opt.i18n_key,
					'name': opt.name
				}
			}).filter(opt => opt.i18n_key == label || opt.name == label).length > 0 && t.mood == forMood
		}).length

    }
	return result
}
let backgroundColors = []
function doughnutChart(div,toughts){
        let doughnutDataSet = []
		let moodsLabels = []
		let total = 0
		Object.keys(moods).forEach(function(mood,i){
			total += toughts.filter((tought,i) => tought.mood == mood ).length
		 })
        Object.keys(moods).forEach(function(mood,i){
			moodsLabels.push(moods[mood])
			doughnutDataSet[i] = /*Math.round(*/ toughts.filter((tought,i) => tought.mood == mood ).length ///total * 100)

            if(!backgroundColors[i] ) //not configured yet
            {

                backgroundColors[i] = moods[mood]['color'];
                $('.legend').append(
                    '<div class="legend-mood col-md-2">' + 
                        '<div class="row">' + 
                            '<div class="legend-mood-img-wrp col-md-2">'+
                                '<img class="legend-mood-img" src="' + moods[mood].icon + '"/>' + 
                            '</div>'+
                            '<div class="legend-mood-color col-md-6" style="background-color:' + backgroundColors[i] + '"></div>'+
                        '</div>' + 
                    '</div>'
                )
            }
		})

        new Chart(document.getElementById(div).getContext('2d'), {
            type: "doughnut",
            data:{ 
                  datasets:[{
                          data:doughnutDataSet,
                          backgroundColor: backgroundColors
                        }]
			},

            options:{
                rotation: 1 * Math.PI,
				circumference: 1 * Math.PI,
				plugins: {
					datalabels: {
					   // hide datalabels for all datasets
					   display: false
					}
				},
                legend: {
                    display: false
                },
				tooltips: {
					callbacks: {
					//   title: function(tooltipItem, data) {
					// 	return data['labels'][tooltipItem[0]['index']];
					//   },
					  label: function(tooltipItem, data) {
						return data['datasets'][0]['data'][tooltipItem['index']];
					  },
					  afterLabel: function(tooltipItem, data) {
						var dataset = data['datasets'][0];
						var percent = Math.round((dataset['data'][tooltipItem['index']] / dataset["_meta"][Object.keys(dataset['_meta'])[0]]['total']) * 100)
						return percent + '%';
					  }
					},
					backgroundColor: '#FFF',
					// titleFontSize: 16,
					// titleFontColor: '#0066ff',
					bodyFontColor: '#000',
					bodyFontSize: 15,
					displayColors: false
				  },
            }
        });
    }

	function doughnutMoodCountChart(div,mood){
	        let doughnutDataSet = []
		if(!mood) return
		doughnutDataSet = [mood.count] 

		let backgroundColors = [mood.color];
		$('#'+div+'-legend').append(
			'<div class="legend-mood col-md-2">' + 
				'<div class="row">' + 
					'<div class="legend-mood-img-wrp col-md-2">'+
						'<img style="height:20px; width:20px;" class="legend-mood-img" src="/static/' + mood.icon + '"/>' + 
					'</div>'+
				'</div>' + 
			'</div>'
		)

        new Chart(document.getElementById(div).getContext('2d'), {
            type: "doughnut",
            data:{ 
                  datasets:[{
                          data:doughnutDataSet,
                          backgroundColor: backgroundColors
                        }]
			},
		
            options:{
                rotation: 1 * Math.PI,
                circumference: 1 * Math.PI,
                legend: {
                    display: false
				},
				plugins: {
					datalabels: {
					   // hide datalabels for all datasets
					   display: false
					}
				},
				tooltips: {
					callbacks: {
					  title: function(tooltipItem, data) {
						return data['labels'][tooltipItem[0]['index']];
					  },
					  label: function(tooltipItem, data) {
						return data['datasets'][0]['data'][tooltipItem['index']];
					  },
					  afterLabel: function(tooltipItem, data) {
						var dataset = data['datasets'][0];
						var percent = Math.round((dataset['data'][tooltipItem['index']] / dataset["_meta"][0]['total']) * 100)
						return '(' + percent + '%)';
					  }
					},
					backgroundColor: '#FFF',
					titleFontSize: 16,
					titleFontColor: '#0066ff',
					bodyFontColor: '#000',
					bodyFontSize: 14,
					displayColors: false
				  },
            }
        });
    }



			function randomRgba(){
				var maximum = 255;
				var minimum = 100;
				var range = maximum - minimum;
				var red = Math.floor(Math.random()*range)+minimum;
				var green = Math.floor(Math.random()*range)+minimum;
				var blue = Math.floor(Math.random()*range)+minimum;
				var redToHex = red.toString(16);
				var greenToHex = green.toString(16);
				var blueToHex = blue.toString(16);
				return "rgb(" + red + "," + green + "," + blue + ")";
				//this.hexValue = "#" + redToHex + "" + greenToHex + "" + blueToHex;
			}
			RndColor.prototype.getRGB = function(){
				return this.rgbValue;
			}
			RndColor.prototype.getHex = function(){
				return this.hexValue;
			}