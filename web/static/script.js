function initGraph(){

   ctx1=document.getElementById("chart1");
   myChart1 = new Chart(ctx1, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'market',
            data: [],
            borderColor: [
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        },
        {
            label: 'sentiment',
            data: [],
            borderColor: [
                'rgba(75, 192, 192, 1)'
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

function loadData(){
    var vocabulary = $("#vocabulary").val();
    var market = $("#market").val();
    var emission_mod = $("#emission_mod").val();
    var transition_mod = $("#transition_mod").val();
    var sentiment_tollerance = $("#sentiment_tollerance").val();
    var market_tollerance = $("#market_tollerance").val();
    
    var jsonObject="{\"vocabulary\":\""+vocabulary+"\",\"market\":\""+market+"\",\"emission_mod\":\""+emission_mod+"\",\"transition_mod\":\""+transition_mod+"\",\"sentiment_tollerance\":\""+sentiment_tollerance+"\",\"market_tollerance\":\""+market_tollerance+"\"}"
     $.ajax({
      type: "GET",
      url: "load/graph",
      contentType:"applicaton/json",
      data: JSON.parse(jsonObject),
      dataType: "json",
      success: function(input)
      {  
          $('#chart1').remove();
          $('#graph-container-1').append('<canvas class="chart" id="chart1"><canvas>');
              canvas = document.querySelector('#chart1'); // why use jQuery?
              ctx1=document.getElementById("chart1");

              labels=input[0];
              var str_labels ="["
              
              for(i=0;i<labels.length;i++){
                    str_labels+="\""+labels[i]+"\""
                    if( i != labels.length-1)
                        str_labels+=","
              }
              

            str_labels+="]"
            

            market_val=input[1];
              var str_market ="["
              
              for(i=0;i<market_val.length;i++){
                    str_market+="\""+market_val[i]+"\""
                    if( i != market_val.length-1)
                        str_market+=","
              }
              
            str_market+="]"
            

            sentiment_val=input[2];
              var str_sentiment ="["
              
              for(i=0;i<sentiment_val.length;i++){
                    str_sentiment+="\""+sentiment_val[i]+"\""
                    if( i != sentiment_val.length-1)
                        str_sentiment+=","
              }
              
            str_sentiment+="]"
            
              graph="{\"type\": \"line\","+
   " \"data\": {"+
      "  \"labels\": "+str_labels+","+
      "  \"datasets\": [{"+
         "   \"label\": \""+market+"\","+
         "   \"data\": "+str_market+","+

        "    \"borderColor\": ["+
        "        \"rgba(255, 159, 64, 1)\","+
        "        \"rgba(54, 162, 235, 1)\","+
        "        \"rgba(255, 206, 86, 1)\","+
        "        \"rgba(75, 192, 192, 1)\","+
        "        \"rgba(153, 102, 255, 1)\","+
        "        \"rgba(255, 159, 64, 1)\""+
        "    ],"+
        "    \"borderWidth\":\" 1\""+
        "},"+
        "{"+
         "   \"label\": \""+vocabulary+"\","+
         "   \"data\": "+str_sentiment+","+

        "    \"borderColor\": ["+
        "        \"rgba(75, 192, 192, 1)\","+
        "        \"rgba(54, 162, 235, 1)\","+
        "        \"rgba(255, 206, 86, 1)\","+
        "        \"rgba(75, 192, 192, 1)\","+
        "        \"rgba(153, 102, 255, 1)\","+
        "        \"rgba(255, 159, 64, 1)\""+
        "    ],"+
        "    \"borderWidth\":\" 1\""+
        "}]"+
    "},"+
    "\"options\": {"+
    "      \"lineTension\" : \"0\","+
    "    \"scales\": {"+
    "        \"yAxes\": [{"+
    "\"override\": {"+
    "               \"stepWidth\": \"20\","+
    "                \"start\":\" 0\","+
    "                \"steps\": \"10\""+
    "            },"+
    "            \"ticks\": {"+
    "                \"beginAtZero\":\"true\""+
    "                }"+
    "            }]"+
    "        }"+
    "    }"+
    "}"

              myChart1 = new Chart(ctx1, JSON.parse(graph));

        if(vocabulary=="bing" && market=="ecb.europa.eu"){
            $('#correlation').empty();
            $('#correlation').append("<p>0.1239667313</p>");}
         if(vocabulary=="bing" && market=="exchangerates.com"){
            $('#correlation').empty();
            $('#correlation').append("<p>0.08265921705</p>");}
         if(vocabulary=="bing" && market=="investing.com"){
            $('#correlation').empty();
            $('#correlation').append("<p>0.1242033466</p>");}
         if(vocabulary=="bing" && market=="ofx.com"){
            $('#correlation').empty();
            $('#correlation').append("<p>0.1140285951</p>");}
        if(vocabulary=="bing" && market=="pundsterlinglive.com"){
            $('#correlation').empty();
            $('#correlation').append("<p>0.04148639478</p>");}

        if(vocabulary=="afinn96" && market=="ecb.europa.eu"){
            $('#correlation').empty();
            $('#correlation').append("<p>0.02221130648</p>");}
         if(vocabulary=="afinn96" && market=="exchangerates.com"){
            $('#correlation').empty();
            $('#correlation').append("<p>0.1502933845</p>");}
         if(vocabulary=="afinn96" && market=="investing.com"){
            $('#correlation').empty();
            $('#correlation').append("<p>0.1760352967</p>");}
         if(vocabulary=="afinn96" && market=="ofx.com"){
            $('#correlation').empty();
            $('#correlation').append("<p>0.1370666617</p>");}
        if(vocabulary=="afinn96" && market=="pundsterlinglive.com"){
            $('#correlation').empty();
            $('#correlation').append("<p>0.00726145137</p>");}

        if(vocabulary=="afinn111" && market=="ecb.europa.eu"){
            $('#correlation').empty();
            $('#correlation').append("<p>0.03285372612</p>");}
         if(vocabulary=="afinn111" && market=="exchangerates.com"){
            $('#correlation').empty();
            $('#correlation').append("<p>0.1638144082</p>");}
         if(vocabulary=="afinn111" && market=="investing.com"){
            $('#correlation').empty();
            $('#correlation').append("<p>0.194199966</p>");}
         if(vocabulary=="afinn111" && market=="ofx.com"){
            $('#correlation').empty();
            $('#correlation').append("<p>0.1631030304</p>");}
        if(vocabulary=="afinn111" && market=="pundsterlinglive.com"){
            $('#correlation').empty();
            $('#correlation').append("<p>0.02081030481</p>");}

        if(vocabulary=="nrc" && market=="ecb.europa.eu"){
            $('#correlation').empty();
            $('#correlation').append("<p>0.1665703968</p>");}
         if(vocabulary=="nrc" && market=="exchangerates.com"){
            $('#correlation').empty();
            $('#correlation').append("<p>0.2167100513</p>");}
         if(vocabulary=="nrc" && market=="investing.com"){
            $('#correlation').empty();
            $('#correlation').append("<p>0.2566511862</p>");}
         if(vocabulary=="nrc" && market=="ofx.com"){
            $('#correlation').empty();
            $('#correlation').append("<p>0.2189560183</p>");}
        if(vocabulary=="nrc" && market=="pundsterlinglive.com"){
            $('#correlation').empty();
            $('#correlation').append("<p>-0.09409046011</p>");}
        
        if(vocabulary=="afinn_bing_base_afinn" && market=="ecb.europa.eu"){
            $('#correlation').empty();
            $('#correlation').append("<p>0.08692247128</p>");}
         if(vocabulary=="afinn_bing_base_afinn" && market=="exchangerates.com"){
            $('#correlation').empty();
            $('#correlation').append("<p>0.1203632819</p>");}
         if(vocabulary=="afinn_bing_base_afinn" && market=="investing.com"){
            $('#correlation').empty();
            $('#correlation').append("<p>0.1798397364</p>");}
         if(vocabulary=="afinn_bing_base_afinn" && market=="ofx.com"){
            $('#correlation').empty();
            $('#correlation').append("<p>0.1497037507</p>");}
        if(vocabulary=="afinn_bing_base_afinn" && market=="pundsterlinglive.com"){
            $('#correlation').empty();
            $('#correlation').append("<p>0.03978643258</p>");}

        if(vocabulary=="afinn_bing_base_bing" && market=="ecb.europa.eu"){
            $('#correlation').empty();
            $('#correlation').append("<p>-0.04485758168</p>");}
         if(vocabulary=="afinn_bing_base_bing" && market=="exchangerates.com"){
            $('#correlation').empty();
            $('#correlation').append("<p>-0.1346175019</p>");}
         if(vocabulary=="afinn_bing_base_bing" && market=="investing.com"){
            $('#correlation').empty();
            $('#correlation').append("<p>-0.1810101498</p>");}
         if(vocabulary=="afinn_bing_base_bing" && market=="ofx.com"){
            $('#correlation').empty();
            $('#correlation').append("<p>-0.1641480791</p>");}
        if(vocabulary=="afinn_bing_base_bing" && market=="pundsterlinglive.com"){
            $('#correlation').empty();
            $('#correlation').append("<p>0.05525965613</p>");}
      },
      error: function()
      {
        alert("Chiamata fallita, si prega di riprovare...");
      }
    })
}