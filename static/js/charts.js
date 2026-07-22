// Register Plugin
console.log("charts.js loaded");
Chart.register(ChartDataLabels);
Chart.defaults.plugins.datalabels.display = true;
console.log(years);
console.log(votes);
console.log(parties);
console.log(vote_share);
console.log(states);
console.log(state_votes);

console.log(trend_years);
console.log(trend_votes);

console.log(winner_parties);
console.log(winner_counts);

console.log(top_candidates);
console.log(candidate_votes);

// ======================
// Votes Bar Chart
// ======================

new Chart(document.getElementById("votesChart"), {

    type: "bar",

    data: {

        labels: years,

        datasets: [{

            label: "Votes (Billions)",

            data: votes,

            backgroundColor: "#7c3aed",

            borderRadius: 10,

            barThickness: 45

        }]

    },

    options: {

        responsive: true,

        maintainAspectRatio: false,

        plugins: {

            legend: {
                display: false
            },
            tooltip:{
                enabled:false
            },
            title: {

                display: true,

                color: "#fff",

                font: {
                    size: 18,
                    weight: "bold"
                }

            },

            datalabels: {

                display: true,

                color: "#FFD700",   // Yellow text

                textStrokeColor: "#000",

                textStrokeWidth: 2,

                anchor:"end",

                align:"top",

                offset:-8,
                formatter: function(value) {

                    return value.toFixed(2);

                },

                font: {

                    size: 15,

                    weight: "bold"

                }

            }

        },

        scales: {

            x:{

                offset:true,

                ticks:{

                    color:"#fff",

                    padding:20,

                    font:{
                        size:15,
                        weight:"bold"
                    }

                },

                grid:{
                    display:false
                }

            },

            y:{

                beginAtZero:true,

                min:0,

                max:450,
                stepSize:100,

                ticks:{

                    color:"#fff",

                    stepSize:2,

                    callback:function(value){
                        return value + " M";
                    }

                },

                grid:{

                    color:"rgba(255,255,255,.08)"

                }

            }

        }

    }

});



// ======================
// Pie Chart
// ======================

new Chart(document.getElementById("partyChart"), {

    type: "doughnut",

    data: {

        labels: parties,

        datasets: [{

            data: vote_share,

            backgroundColor: [

                "#2563eb",
                "#f97316",
                "#16a34a",
                "#9333ea",
                "#ec4899",
                "#64748b"

            ],

            borderColor: "#121b2d",

            borderWidth: 2

        }]

    },

    options: {

        responsive: true,

        maintainAspectRatio: false,

        cutout: "42%",
        radius: "95%",

        layout:{
            padding:{
                top:0,
                bottom:20,
                left:10,
                right:10
            }
        },

        plugins: {

            title: {

                display: true,

                color: "#fff",

                font: {

                    size: 20,

                    weight: "bold"

                }

            },

            legend: {

                position: "right",

                labels: {

                    color: "#fff",

                    font: {

                        size:18,
                        weight:"bold"

                    },

                    boxWidth:24,
                    boxHeight:24,
                    padding:18

                }

            },

            datalabels:{

                display:true,

                color:"#ffffff",

                formatter:(value)=>value.toFixed(1)+"%",

                font:{
                    size:16,
                    weight:"bold"
                },

                anchor:"center",

                align:"center",

                offset:0,

                clip:false,

                clamp:true

            }
        }

    },

    plugins: [ChartDataLabels],

});


new Chart(document.getElementById("stateChart"), {

    type: "bar",

    data: {
        labels: states,
        datasets: [{
            data: state_votes,
            backgroundColor: "#7c3aed",
            borderRadius: 8
        }]
    },

    options: {

        indexAxis: "y",

        responsive: true,

        maintainAspectRatio: false,

        plugins:{

            legend:{
                display:false
            },

            tooltip:{
                enabled:false
            },

            datalabels:{

                color:"#FFD700",

                anchor:"center",

                align:"center",

                formatter:function(value){
                    return value.toFixed(1)+" M";
                },

                font:{
                    size:14,
                    weight:"bold"
                }

            }

        },

        scales: {

            x: {
                ticks:{
                    color:"#fff",

                    callback:function(value){
                        return value.toFixed(1)+" M";
                    }
                },
                grid: {
                    color: "rgba(255,255,255,.08)"
                }
            },

            y: {
                ticks: {
                    color: "#fff"
                },
                grid: {
                    display: false
                }
            }

        }

    }

});


new Chart(document.getElementById("trendChart"),{

    type:"line",

    data:{

        labels:trend_years,

        datasets:[{

            label:"Total Campaign Spending",

            data:trend_votes,

            borderColor:"#a855f7",

            backgroundColor:"rgba(168,85,247,.25)",

            fill:true,

            tension:.4,

            pointRadius:6,

            pointHoverRadius:8,

            pointBackgroundColor:"#ffffff",

            pointBorderColor:"#a855f7",

            pointBorderWidth:3

        }]

    },

    options:{

        responsive:true,

        maintainAspectRatio:false,

        plugins:{

            legend:{
                display:false
            },

            tooltip:{
                enabled:false
            },

            datalabels:{

                display:true,

                color:"#FFD700",

                textStrokeColor:"#000",

                textStrokeWidth:2,

                formatter:(value)=>"₹ "+value.toFixed(1)+" Cr",

                font:{
                    size:15,
                    weight:"bold"
                },

                anchor:"center",

                align:function(context){

                    switch(context.dataIndex){

                        case 0:
                            return "right";

                        case 1:
                            return "left";

                        case 2:
                            return "bottom";

                        case 3:
                            return "top";

                    }

                },

                offset:12
            }
        },

        scales:{

            x:{
                ticks:{
                    color:"#fff",
                    font:{
                        size:14,
                        weight:"bold"
                    }
                },
                grid:{
                    display:false
                }
            },

            y:{

                beginAtZero:true,

                ticks: {
                    color: "#ffffff",
                    callback: value => "₹ " + value + " Cr"
                },

                grid:{
                    color:"rgba(255,255,255,.08)"
                }

            }

        }

    },

    plugins:[ChartDataLabels]

});



new Chart(document.getElementById("winnerChart"), {

    type: "bar",

    data: {

        labels: winner_parties,

        datasets: [{

            data: winner_counts,

            backgroundColor: "#7c3aed",

            borderRadius: 8

        }]

    },

    options: {

        responsive: true,

        maintainAspectRatio: false,
                layout: {
            padding: {
                top: 35
            }
        },

        plugins:{

            legend:{
                display:false
            },

            tooltip:{
                enabled:false
            },

            datalabels: {
                display: true,

                color: "#FFD700",

                anchor: "end",

                align: "top",

                offset: 8,

                clamp: true,

                clip: false,

                font: {
                    size: 16,
                    weight: "bold"
                },

                formatter: (value) => value
            }


        },

        scales: {

            x: {

                ticks: {

                    color: "#fff"

                }

            },

            y: {

                ticks: {

                    color: "#fff"

                }

            }

        }

    }

});

new Chart(document.getElementById("candidateChart"), {

    type: "bar",

    data: {

        labels: top_candidates,

        datasets: [{

            data: candidate_votes,

            backgroundColor: "#7c3aed",

            borderRadius: 8

        }]

    },

    options: {

        indexAxis: "y",

        responsive: true,

        maintainAspectRatio: false,

        plugins:{

            legend:{
                display:false
            },

            tooltip:{
                enabled:false
            },

            datalabels:{

                color:"#FFD700",

                anchor:"center",

                align:"center",

                formatter: value => value.toFixed(2) + " L",

                font:{
                    size:14,
                    weight:"bold"
                }

            }

        },

        scales: {

            x: {

                ticks: {

                    color: "#fff",

                   callback: value => value.toFixed(2) + " L"

                }

            },

            y: {

                ticks: {

                    color: "#fff"

                }

            }

        }

    }

});