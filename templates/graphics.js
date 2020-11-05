var ctx = document.getElementById('myChart').getContext('2d');
var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'bar',

    // The data for our dataset
    data: {
        labels: ['2020-05-13', '2020-05-14', '2020-05-15', '2020-05-16', '2020-05-17', '2020-05-18', '2020-05-19'],
        datasets: [
            {
                label: 'Утром',
                backgroundColor: 'rgb(98, 204, 147)', // 'rgb(224, 224, 150)'
                borderColor: 'rgb(45, 196, 116)', // 'rgb(242, 242, 92)'
                data: [10, 170, 50, 15, 88, 5, 170, 50, 15, 88, 5],  // [10, 150, 45, 15, 70, 5, 170, 50, 17, 95, 4]
            },
            {
                label: 'Вечером',
                backgroundColor: 'rgb(224, 224, 150)',
                borderColor: 'rgb(242, 242, 92)',
                data: [10, 150, 45, 15, 70, 5, 170, 50, 17, 95, 4],
            }
            ]

    },

    // Configuration options go here
    options: {}
});

for(var i = 0; i < utro_arr.lenght; i++)
//var ctx = document.getElementById('myChart').getContext('2d');
//var chart = new Chart(ctx, {
    /// The type of chart we want to create
    //type: 'bar',

    /// The data for our dataset
    //data: {
    //    labels: ['2020-05-13', '2020-05-14', '2020-05-15', '2020-05-16', '2020-05-17', '2020-05-18', '2020-05-19'],
    //    datasets: [{
    //       label: 'Вечером',
    //        backgroundColor: 'rgb(224, 224, 150)',
    //        borderColor: 'rgb(242, 242, 92)',
    //        data: [10, 150, 45, 15, 70, 5, 170, 50, 17, 95, 4],
    //    }],

    //},
    // Configuration options go here
    //options: {}
//});