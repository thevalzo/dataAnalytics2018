
function initHome(){
	//$("#chartcloud").jQCloud([{"text":"instagram","weight":"100"},{"text":"sharper","weight":"60"},{"text":"bicocca","weight":"50"}]);
		
	 $.ajax({
	      type: "GET",
	      url: "client/filters",
	      data: {"jsonMessage":"{\"filters\":\"get\"}"},
	      dataType: "json",
	      success: function(input)
	      {  
	    	  for(i=0;i<input.filtersArray.length;i++){
	    	  $('#selectFiltro').append("<option value=\""+input.filtersArray[i].id+"\">"+input.filtersArray[i].name+"</option>");
	      }
	      },
	      error: function()
	      {
	        alert("Chiamata fallita, si prega di riprovare...");
	      }
	    })
	  
	 ctx1=document.getElementById("chart1");
	 myChart1 = new Chart(ctx1, {
    type: 'bar',
    data: {
        labels: [],
        datasets: [{
            label: '# of Votes',
            data: [],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        }
    }
});

var ctx2 = document.getElementById("chart2");
var myChart2 = new Chart(ctx2, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: '# of Votes',
            data: [],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        }
    }
});



var ctx4 = document.getElementById("chart4");
var myChart4 = new Chart(ctx4, {
    type: 'doughnut',
    data: {
        labels: [],
        datasets: [{
            label: '# of Votes',
            data: [],
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero:true
                }
            }]
        }
    }
});
}

function initConfig(){
	/*
	 $.ajax({
	      type: "GET",
	      url: "client/filters",
	      data: {"jsonMessage":"{\"filters\":\"get\"}"},
	      dataType: "json",
	      success: function(input)
	      {  
			$('#delFiltro').empty();
			  $('#deleteUserFiltro').empty();
			  $('#insertUserFiltro').empty();
			  
			  $('#delFiltro').append("<option value=\"\">\\</option>");
			  $('#deleteUserFiltro').append("<option value=\"\">\\</option>");
			  $('#insertUserFiltro').append("<option value=\"\">\\</option>");
			  
	    	  for(i=0;i<input.filtersArray.length;i++){
	    	  $('#delFiltro').append("<option value=\""+input.filtersArray[i].id+"\">"+input.filtersArray[i].name+"</option>");
			  $('#deleteUserFiltro').append("<option value=\""+input.filtersArray[i].id+"\">"+input.filtersArray[i].name+"</option>");
			  $('#insertUserFiltro').append("<option value=\""+input.filtersArray[i].id+"\">"+input.filtersArray[i].name+"</option>");
	      
	      }
	      },
	      error: function()
	      {
	        alert("Chiamata fallita, si prega di riprovare...");
	      }
	    })
	*/
	//PROVA
	var input= {"filtersArray":[{"id":"21", "name":"pokemon"}, {"id":"19", "name":"cats"}] }
				$('#delFiltro').empty();
			  $('#deleteUserFiltro').empty();
			  $('#insertUserFiltro').empty();
			  
			  $('#delFiltro').append("<option value=\"\">\\</option>");
			  $('#deleteUserFiltro').append("<option value=\"\">\\</option>");
			  $('#insertUserFiltro').append("<option value=\"\">\\</option>");
	      
	for(i=0;i<input.filtersArray.length;i++){
	    	  $('#delFiltro').append("<option value=\""+input.filtersArray[i].id+"\">"+input.filtersArray[i].name+"</option>");
			  $('#deleteUserFiltro').append("<option value=\""+input.filtersArray[i].id+"\">"+input.filtersArray[i].name+"</option>");
			  $('#insertUserFiltro').append("<option value=\""+input.filtersArray[i].id+"\">"+input.filtersArray[i].name+"</option>");
	      
	      }	
}

$(document).ready(function() {
  $("#buttonDelFiltro").click(function(){
	var id = $("#delFiltro").val();
	alert("Cancello il filtro "+id);
	initConfig();
	/*
	 $.ajax({
        type: "GET",
        url: "client/filtro/delete",
        data: {"jsonMessage":"{\"idFIltro\":\""+id+"\"}"},
        dataType: "json",
        success: function(input)
        {  
			$("#selectFiltro").val(input.log);
			initConfig();
		 },
        error: function()
        {
          alert("Chiamata fallita, si prega di riprovare...");
        }
      })*/
	  
  });
});

/*UPDATE FILTRO*/
function datiFiltro(){
    var id = $("#selectFiltro").val();
	
	
    $.ajax({
        type: "GET",
        url: "client/basicinfo",
        data: {"jsonMessage":"{\"id\":\""+id+"\"}"},
        dataType: "json",
        success: function(input)
        {  
      	  $('#followers-value').remove();
      	  $('#follows-value').remove();
      	  $('#tot-likes-value').remove();
      	  $('#tot-comments-value').remove();
      	  $('#followers').append('<p class="data-result" id="followers-value">'+input.followers+'</p>');
      	  $('#follows').append('<p class="data-result" id="follows-value">'+input.follows+'</p>');
      	  $('#tot-likes').append('<p class="data-result" id="tot-likes-value">'+input.totlikes+'</p>');
      	  $('#tot-comments').append('<p class="data-result" id="tot-comments">'+input.totcomments+'</p>');
        },
        error: function()
        {
          alert("Chiamata fallita, si prega di riprovare...");
        }
      })
      
    /*GRAPH 1*/
    $.ajax({
      type: "GET",
      url: "client/graph1",
      data: {"jsonMessage":"{\"id\":\""+id+"\"}"},
      dataType: "json",
      success: function(input)
      {  
    	  $('#chart1').remove();
    	  $('#graph-container-1').append('<canvas class="chart" id="chart1"><canvas>');
    		  canvas = document.querySelector('#chart1'); // why use jQuery?
    		  ctx1=document.getElementById("chart1");
    		  myChart1 = new Chart(ctx1, input);
      },
      error: function()
      {
        alert("Chiamata fallita, si prega di riprovare...");
      }
    })
  
	  /*GRAPH 2*/
    $.ajax({
      type: "GET",
      url: "client/graph2",
      data: {"jsonMessage":"{\"id\":\""+id+"\"}"},
      dataType: "json",
      success: function(input)
      {  
    	  $('#chart2').remove();
    	  $('#graph-container-2').append('<canvas class="chart" id="chart2"><canvas>');
    		  canvas = document.querySelector('#chart2'); // why use jQuery?
    		  ctx2=document.getElementById("chart2");
    		  myChart2 = new Chart(ctx2, input);
      },
      error: function()
      {
        alert("Chiamata fallita, si prega di riprovare...");
      }
    })
}


/*UPDATE GRAPH*/
$(document).ready(function() {
  $("#button").click(function(){
    var data_init = $("#data_init").val();
    var data_fine = $("#data_fine").val();
    var id = $("#filtri").val();
    alert("ciao");
    /*GRAPH 3*/
    $.ajax({
      type: "GET",
      url: "client/graph3",
      data: {"jsonMessage":"{\"data_init\":\""+data_init+"\",\"data_fine\":\""+data_fine+"\",\"id\":\""+id+"\"}"},
      dataType: "json",
      success: function(input)
      {  
    	  $("#chartcloud").jQCloud(input.data);
    		
      },
      error: function()
      {
        alert("Chiamata fallita, si prega di riprovare...");
      }
    })
    

  /*GRAPH 4*/
    $.ajax({
      type: "GET",
      url: "client/graph4",
      data: {"jsonMessage":"{\"data_init\":\""+data_init+"\",\"data_fine\":\""+data_fine+"\",\"id\":\""+id+"\"}"},
      dataType: "json",
      success: function(input)
      {  
    	  $('#chart4').remove();
    	  $('#graph-container-4').append('<canvas class="chart" id="chart4"><canvas>');
    		  canvas = document.querySelector('#chart4'); // why use jQuery?
    		  ctx4=document.getElementById("chart4");
    		  myChart4 = new Chart(ctx4, input);
      },
      error: function()
      {
        alert("Chiamata fallita, si prega di riprovare...");
      }
    })

  });
});

$(document).ready(function() {
  $("#startCrawler").click(function(){
	if($('#crawler-state-value').text()=='OFF'){
  /*  $.ajax({
      type: "GET",
      url: "client/crawler/start",
      data: {"jsonMessage":"{\"crawler\":\"start\""},
      dataType: "json",
      success: function(input)
      {  
    	  	$('#crawler-state-value').text('ON');
		  $('#crawler-state').css('background-color', "green");
			$('#stopCrawler').show();
			$('#startCrawler').hide();
      },
      error: function()
      {
        alert("Chiamata fallita, si prega di riprovare...");
      }
    })*/
	
			$('#crawler-state-value').text('ON');
		  $('#crawler-state').css('background-color', "green");
			$('#stopCrawler').show();
			$('#startCrawler').hide();
		
  }   
  });
});

	
$(document).ready(function() {
  $("#stopCrawler").click(function(){
	if($('#crawler-state-value').text()=='ON'){
		
		/*$.ajax({
      type: "GET",
      url: "client/crawler/stop",
      data: {"jsonMessage":"{\"crawler\":\"stop\""},
      dataType: "json",
      success: function(input)
      {  
    	  $('#crawler-state-value').text("OFF");
		$('#crawler-state').css('background-color', "red");
      	$('#stopCrawler').hide();
		$('#startCrawler').show();
      },
      error: function()
      {
        alert("Chiamata fallita, si prega di riprovare...");
      }
    })*/
	    $('#crawler-state-value').text("OFF");
		$('#crawler-state').css('background-color', "red");
      	$('#stopCrawler').hide();
		$('#startCrawler').show();
      	  
	} 
  });
});







