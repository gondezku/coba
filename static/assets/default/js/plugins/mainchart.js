function sortObject(obj) {
    var arr = [];
    for (var prop in obj) {
        if (obj.hasOwnProperty(prop)) {
            arr.push({
                'key': prop,
                'value': obj[prop]
            });
        }
    }
    arr.sort(function(a, b) { return b.value - a.value; });
    //arr.sort(function(a, b) { return a.value.toLowerCase().localeCompare(b.value.toLowerCase()); }); //use this to sort as strings
    
    return arr; // returns array
}

function Percent(ar) {
    var value = [];
    var key = ['Pump Cashing','Motor Cashing','Jet Pump','Rotor','Fin. PC','Fin. MC','Impeller','Stator','Assy','Stator New'];

    var obj = {};

    var sum = 0;
    var tot_perc = 0;
    for (var i = 0; i < ar.length; i++) {
      if(typeof ar[i] == `number`) sum += ar[i];
    };

    for (var i = 0; i < ar.length; i++) {
        tot_perc = ((100*ar[i]) / sum );
        PieChart(IndexPie=i+1, tot_perc);
        value[i] = tot_perc.toFixed(1);
    }

    key.forEach((element, index) => {
        obj[element] = value[index];
      });

    keysSorted = sortObject(obj);
    
    return sum;
  }

function PieChart(IndexPie, pie_value) {
    const sCenterText ={
        id: 'sCenterText',
        afterDatasetsDraw(chart, args, options){
            var TextPec = pie_value; 
            const{ctx, chartArea:{top,bottom,right,left,width,height}} = chart;
            ctx.save();
            ctx.font = '10px Arial';
            ctx.fillStyle = 'rgba(58,245,39,0.8)';
            ctx.textAlign = 'center';
            ctx.fillText(TextPec.toFixed(1),width/2,(height/2)+2.5);
        }
    }
    var config = {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [pie_value, 100-pie_value],
                backgroundColor: ['#d725bb', 'transparent'],
                borderColor: '#344675'
            }]          
        },
        options: {
            maintainAspectRatio: false,
            responsive: true,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    enabled: false // <-- this option disables tooltips
                  }
            }
        },
        plugins: [sCenterText]
        
    }
    var ctx21 = document.getElementById('pie-chart'+IndexPie).getContext("2d");
    if (IndexPie==1){
        if(window.GenChart21!= null){
            window.GenChart21.destroy();
        }
        window.GenChart21 = new Chart(ctx21, config);
    }
    if (IndexPie==2){
        if(window.GenChart22!= null){
            window.GenChart22.destroy();
        }
        window.GenChart22 = new Chart(ctx21, config);
    }
    if (IndexPie==3){
        if(window.GenChart23!= null){
            window.GenChart23.destroy();
        }
        window.GenChart23 = new Chart(ctx21, config);
    }
    if (IndexPie==4){
        if(window.GenChart24!= null){
            window.GenChart24.destroy();
        }
        window.GenChart24 = new Chart(ctx21, config);
    }
    if (IndexPie==5){
        if(window.GenChart25!= null){
            window.GenChart25.destroy();
        }
        window.GenChart25 = new Chart(ctx21, config);
    }
    if (IndexPie==6){
        if(window.GenChart26!= null){
            window.GenChart26.destroy();
        }
        window.GenChart26 = new Chart(ctx21, config);
    }
    if (IndexPie==7){
        if(window.GenChart27!= null){
            window.GenChart27.destroy();
        }
        window.GenChart27 = new Chart(ctx21, config);
    }
    if (IndexPie==8){
        if(window.GenChart28!= null){
            window.GenChart28.destroy();
        }
        window.GenChart28 = new Chart(ctx21, config);
    }
    if (IndexPie==9){
        if(window.GenChart29!= null){
            window.GenChart29.destroy();
        }
        window.GenChart29 = new Chart(ctx21, config);
    }
    if (IndexPie==10){
        if(window.GenChart210!= null){
            window.GenChart210.destroy();
        }
        window.GenChart210 = new Chart(ctx21, config);
    }
    
}

function PointUpdate(){
    
}