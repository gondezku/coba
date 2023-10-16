function Blue(){
    gradientChartOptionsConfigurationWithTooltipBlue = {
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false
            }
        },
        responsive: true,
        onClick: (event, elements, chart) => {
            if (elements[0]) {            
                const i = elements[0].index;
                if ((chart.data.labels[i]).length > 9  ){
                    for (let i = 0; i < 4; i++) {
                        var elementsClass = document.getElementById(i).className;
                        if (elementsClass == "btn btn-sm btn-primary btn-simple active"){
                            document.getElementById(i).setAttribute("class","btn btn-sm btn-primary btn-simple");
                        }
                        document.getElementById("3").setAttribute("class","btn btn-sm btn-primary btn-simple active");
                    }
                    var text2 =$("#text2").text();
                    $("#text2").text(text2 + " on " + chart.data.labels[i]);
                    window.pointSet = chart.data.labels[i];
                    CustomClickHandler1(window.roleId, window.pointSet);
                }
                else {
                    alert("Data sudah paling kecil");
                }
            }
          }
    }
    return gradientChartOptionsConfigurationWithTooltipBlue;
};

function Purple(){
    gradientChartOptionsConfigurationWithTooltipPurple = {
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false
            }
        },
        responsive: true,
        onClick: (event, elements, chart) => {
            if (elements[0]) {            
                const i = elements[0].index;
                if ((chart.data.labels[i]).length > 9 ){
                    for (let i = 0; i < 4; i++) {
                        var elementsClass = document.getElementById(i).className;
                        if (elementsClass == "btn btn-sm btn-primary btn-simple active"){
                            document.getElementById(i).setAttribute("class","btn btn-sm btn-primary btn-simple");
                        }
                        document.getElementById("3").setAttribute("class","btn btn-sm btn-primary btn-simple active");
                    }
                    $("#text1").text(window.textPower + " on " + chart.data.labels[i]);
                    window.pointSet = chart.data.labels[i];
                    CustomClickHandler('all_ch', window.pointSet);
                    if (window.roleId != 'all_ch'){
                        CustomClickHandler1(window.roleId, window.pointSet);
                    }
                }
                else {
                     if ((chart.data.labels[i]).length > 5 ){
                        for (let i = 0; i < 4; i++) {
                            var elementsClass = document.getElementById(i).className;
                            if (elementsClass == "btn btn-sm btn-primary btn-simple active"){
                                document.getElementById(i).setAttribute("class","btn btn-sm btn-primary btn-simple");
                            }
                            document.getElementById("3").setAttribute("class","btn btn-sm btn-primary btn-simple active");
                        }
                        $("#text1").text(window.textPower + " on " + chart.data.labels[i]);
                        window.pointSet = chart.data.labels[i];
                        CustomClickHandler('all_ch', window.pointSet);
                        if (window.roleId != 'all_ch'){
                            CustomClickHandler1(window.roleId, window.pointSet);
                        }
                    }
                    else{
                        alert("Data sudah paling kecil");
                    }
                }
            }
          }
    }
    return gradientChartOptionsConfigurationWithTooltipPurple;
};

function overall(){
    $.ajax({
        url: 'genchar',
        data: {
            'att': 'all_ch',
            'scale': 'overall',
            },
        success: function (data) {
            MakeChart(data);
            MakeChart2(data);
            MakeChart3(data);
            // Percent(data.data);
        }
        
    });
}

function monthly(){
    $.ajax({
        url: 'genchar',
        data: {
            'att': 'all_ch',
            'scale': 'monthly',
            },
        success: function (data) {
            MakeChart(data);
            MakeChart2(data);
            Percent(data.data);
        }
        
    });
}

function CustomClickHandler(data, args){
    $.ajax({
        url: 'genchar',
        data: {
            'att': data,
            'scale': args
            },
        success: function (dataNew) {
            MakeChart(dataNew);
            MakeChart2(dataNew);
            Percent(dataNew.data);
        }
        
    });
}

function CustomClickHandler1(data, args){
    $.ajax({
        url: 'genchar',
        data: {
            'att': data,
            'scale': args
            },
        success: function (dataNew) {
            MakeChart3(dataNew);
        }
        
    });
}

function CustomIdClickHandler(data, args1){
    $.ajax({
        url: 'genchar',
        data: {
            'att': data,
            'scale': args1
            },
        success: function (dataNew) {
            MakeChart3(dataNew);
        }
        
    });
}

function getRandomColor() {
    var letters = '0123456789ABCDEF'.split('');
    var color = '#';
    for (var i = 0; i < 6; i++ ) {
        color += letters[Math.round(Math.random() * 15)];
    }
    return color;
}

function MakeChart(data){
    // var total = data.total;
    var total = data.data;
    var ctx2 = document.getElementById('gen-chart').getContext("2d");
    var randomColor = Math.floor(Math.random()*16777215).toString(16);
    if(window.GenChart2!= null){
        window.GenChart2.destroy();
    }
    
    var test = data.labels;
    var val = Object.values(total)
    var dta = []
    // test.forEach(el => {
        var dic = {}
        dic['label'] = 'Dataset 1'
        dic['backgroundColor'] = getRandomColor();
        // "#" + Math.floor(Math.random()*16777215).toString(16);
        dic['data'] = Object.values(total)
    
    let idx = 0
    test.forEach(el => {
        in_data = [];
        val.forEach(e => {
            in_data.push(e[idx]);
        })
        var dic = {}
        dic['label'] = data.labels[idx]
        dic['backgroundColor'] = "#" + Math.floor(Math.random()*16777215).toString(16);
        dic['data'] = in_data//Object.values(total)
        dta.push(dic)
        idx++

    });

    const aku = {
        type: 'bar',
        data: {
            labels: Object.keys(total),
            },
        options: {
            maintainAspectRatio: false,
            responsive: true,
            scales: {
              x: {
                stacked: true,
              },
              y: {
                stacked: true
              }
            }
          }
    }

    aku.data['datasets'] = dta
    
    window.GenChart2 = new Chart(ctx2, aku);
            
            
}

function MakeChart2(data){
    var total = data.total;
    var ctx = document.getElementById('gen-chart2').getContext("2d");
    if(window.GenChart!= null){
        window.GenChart.destroy();
    }
    var label_ku = Object.keys(total);
    var data_ku = Object.values(total);
    window.GenChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: label_ku,
                    datasets: [{
                        data: data_ku,
                        backgroundColor: ['#184c9c', '#d33035', '#ffc107', '#28a745', '#6f7f8c', '#6610f2', '#6e9fa5', '#fd7e14', '#e83e8c', '#17a2b8', '#6f42c1']
                    }]          
                },
                options: {
                    maintainAspectRatio: false,
                    responsive: true,
                    plugins: {
                        legend: {
                            display: true,
                            position: 'right',
                            align: 'start'
                        }
                    },
                }
            });
}

function MakeChart3(data){
    var total = data.detail;
    var ctx3 = document.getElementById('gen-chart3').getContext("2d");
    if(window.GenChart3!= null){
        window.GenChart3.destroy();
    }
    window.GenChart3 = new Chart(ctx3, {
                type: 'bar',
                data: {
                    labels: Object.keys(total),
                    datasets: [{
                        axis: 'y',
                        borderColor: 'rgba(8,215,218,0.8)',
                        borderWidth: 2,
                        borderDash: [],
                        borderDashOffset: 0.0,
                        fill: true,
                        backgroundColor: 'rgba(8,215,218,0.2)',
                        pointBorderWidth: 2,
                        pointHoverRadius: 4,
                        pointHoverBorderWidth: 10,
                        pointRadius: 4,
                        data: Object.values(total),
                        }]
                    },
                options: {
                    indexAxis: 'y',
                    maintainAspectRatio: false,
                    responsive: true,
                    plugins: {
                        legend: {
                            display: false
                        },
                        datalabels: {
                            anchor: 'start', // Anchor the labels to the start of the datapoint
                            align: 'end', // Align the text after the anchor point
                            formatter: function(value, context) { // Show the label instead of the value
                                return context.chart.data.labels[context.dataIndex];
                            }
                        }
                    },
                    scales: {
                        x: {
                            display:false,
                            grid: {
                              display: true,
                              color: 'transparent'
                            }
                        },
                        y: {
                            grid: {
                              display: true,
                              color:'transparent'
                            },
                            ticks: {
                                mirror: true, //Show y-axis labels inside horizontal bars
                                font: {
                                    size: 12,
                                },
                                color:'#000000'
                                
                            }
                        },
                    },
                  }
            });
            
            
}