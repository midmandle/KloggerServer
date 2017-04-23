sessionData = null;
userData = null;
populationData = null;

$(function() {
    $("#tabs").tabs({disabled: [2]});

    $("#tabs").tabs({
      activate: function(event, ui)
      {
        var $activeTab = $('#tabs').tabs('option', 'active');
        if($activeTab == 2)
        {
          //$("#sessionChart").empty();
        }
        if($activeTab == 3)
        {
          getUsersList();
        }
      }
    })

    $("#refreshButton").button().click(function(){refreshContentLog()});
    $("#clearContentLogButton").button().click(function(){clearContentLog()});
    $("#deleteAllButton").button().click(function(){deleteContentsFromServer()});
    $("#makeSessionChart").button().click(function(){generateSessionChart()});
    $("#getUserData").button().click(function(){loadUserData()});
    $("#getPopulationData").button().click(function(){loadPopulationData()});

    $("#chartType").selectmenu(); //For session analysis

    $("#users").selectmenu();
    $("#userChartType").selectmenu();

    $("#populationChartType").selectmenu();

    refreshContentLog();
});

function refreshContentLog()
{
  var resp = $.ajax({
    type: "POST",
    url: "/refreshContentLog"
  });
  resp.done(function(response){
      clearContentLog();
      obj = JSON.parse(response)
      for(var element in obj)
      {
        $("#tableOutput").append('<tr class="table-content'+element+'">');
        $(".table-content"+element).append($('<td>', {text: obj[element].UserID}));
        $(".table-content"+element).append($('<td>', {text: obj[element].StartTime}));
        $(".table-content"+element).append($('<td>', {text: obj[element].EndTime}));
        $(".table-content"+element).append($('<td><button id="view-'+element+'">View Session</button>'));
        $("#tableOutput").append('</tr>');
        $("#view-"+element).button().click(function(){viewSession()});
      }
    });
    $("#contentLog").text("Content: Refreshed log.");
}

function clearContentLog()
{
  $("#contentLog").text("Content: Cleared log.");
  $("#tableOutput").empty();
  $("#tableOutput").html("<tr><th class=\"table-header\"><h1>ID</h1></th><th class=\"table-header\"><h1>Session Start Date/Time</h1></th><th class=\"table-header\"><h1>Session End Date/Time</h1></th><th class=\"table-header\"><h1>View Session</h1></th></tr>")
}

function deleteContentsFromServer()
{
  var resp = $.ajax({
    type: "POST",
    url: "/deleteContentsFromServer"
  });
  resp.done(function(response){
    $("#contentLog").html("Content: "+response);
    clearContentLog();
  });
}

function viewSession()
{
  var caller = event.target.id;
  var $tds = $("#"+caller).parent().parent().find("td");
  var json = {
    id: $($tds[0]).text(),
    startTime: $($tds[1]).text(),
    endTime: $($tds[2]).text()
  }
  var resp = $.ajax({
    type:"POST",
    headers: {
      Accept: "text/plain; charset=utf-8",
      "Content-Type": "application/json; charset=utf-8"
    },
    url: "/generateSessionStats",
    data: JSON.stringify(json)
  })
  resp.done(function(returnedJson)
  {
    $("#tabs").tabs({disabled: []});//Enable disabled tab once session is seleted.
    populateAnalysisTabWithSessionData(returnedJson);
  });

}

function populateAnalysisTabWithSessionData(json)
{
    var content = $.parseJSON(json);
    sessionData = content;
    var overview = content.Overview;
    var timeline = content.Timeline;
    var programsUsedList = content.List_Of_Programs_In_Session;
    var timeSpentPerProgram = content.Time_Spent_Per_Program;

    populateAnalysisOverview(overview);
}

function populateAnalysisOverview(overview)
{
  $("#overviewStatsOut").html("<ul></ul>");
  $.each(overview, function(key, value)
  {
    if(key == "Total_Time_In_Session")
    {
      $("#overviewStatsOut ul").append("<li>"+key+" (HH:MM:SS): "+value+"</li>");
      return true;
    }
    $("#overviewStatsOut ul").append("<li>"+key+": "+value+"</li>");
  });
}

function generateSessionChart()
{
    $("#sessionChart").empty();

    var data = [];
    var ys = [];
    var xs = [];

    var chartType = $("#chartType").val();

    if(chartType == "Time Spent Per Program")
    {
      ys=['time'];
      xs = 'program';
      l = ['Time'];
      $.each(sessionData.Time_Spent_Per_Program, function(key, val)
      {
        item = {program: key, time: val};
        data.push(item);
      });
    }
    if(chartType == "Actions Per Program")
    {
      //Do actions per program... Will need editing of SessionAnalysis.py
      ys=['actions'];
      xs = 'program';
      l = ['Actions'];
      $.each(sessionData.Actions_Per_Program, function(key, val)
      {
        item = {program: key, actions: val};
        data.push(item);
      });
    }
    if(chartType == "Keypresses Per Program")
    {
      //Do keypresses per program... Will need editing of SessionAnalysis.py
      ys=['keypresses'];
      xs = 'program';
      l = ['Keypresses'];
      $.each(sessionData.Keypresses_Per_Program, function(key, val)
      {
        item = {program: key, keypresses: val};
        data.push(item);
      });
    }
    if(chartType == "Mouse-clicks Per Program")
    {
      //Do Mouse-clicks per program... Will need editing of SessionAnalysis.py
      ys=['mouseclicks'];
      xs = 'program';
      l = ['Mouse-Clicks'];
      $.each(sessionData.Mouseclicks_Per_Program, function(key, val)
      {
        item = {program: key, mouseclicks: val};
        data.push(item);
      });
    }

    new Morris.Bar({
      resize: true,
      // ID of the element in which to draw the chart.
      element: 'sessionChart',
      // Chart data records -- each entry in this array corresponds to a point on
      // the chart.
      data: data,
      // The name of the data record attribute that contains x-values.
      xkey: xs,
      // A list of names of data record attributes that contain y-values.
      ykeys: ys,
      // Labels for the ykeys -- will be displayed when you hover over the
      // chart.
      labels: l
    });
}



function getUsersList()
{
  $("#users").empty();
  var resp = $.ajax({
    type:"GET",
    url: "/getUsersList",
  })
  resp.done(function(returnedJson)
  {
      returnedJson = JSON.parse(returnedJson);

      for(var item in returnedJson)
        $("#users").append('<option> '+returnedJson[item]+'</option>');

  });
}

function loadUserData()
{
  var userID = parseInt($("#users").val());
  var json = {
    id: userID
  }
  var resp = $.ajax({
    type:"POST",
    headers: {
      Accept: "text/plain; charset=utf-8",
      "Content-Type": "application/json; charset=utf-8"
    },
    url: "/generateUserSessionStats",
    data: JSON.stringify(json)
  })
  resp.done(function(returnedJson)
  {
    userData = $.parseJSON(returnedJson);
    generateUserChart();
  });


}

function generateUserChart()
{
    $("#userChart").empty();

    var data = [];
    var ys = [];
    var xs = [];

    var chartType = $("#userChartType").val();

    if(chartType == "Time Spent Per Session")
    {
      ys=['timeSpent'];
      xs = 'sessionDate';
      l = ['Time Spent'];
      $.each(userData.Time_Spent_Per_Session, function(key, val)
      {
        item = {sessionDate: key, timeSpent: val};
        data.push(item);
      });
    }
    if(chartType == "Time Spent Per Day")
    {
      ys=['timeSpent'];
      xs = 'date';
      l = ['Time Spent'];
      $.each(userData.Time_Spent_Per_Day, function(key, val)
      {
        item = {date: key, timeSpent: val};
        data.push(item);
      });
    }
    if(chartType == "Time Spent Per Program")
    {
      ys=['timeSpent'];
      xs = 'program';
      l = ['Time Spent'];
      $.each(userData.Time_Spent_Per_Program, function(key, val)
      {
        item = {program: key, timeSpent: val};
        data.push(item);
      });
    }
    if(chartType == "Number Of Keystrokes Per Session")
    {
      ys=['keystrokes'];
      xs = 'sessionDate';
      l = ['Keystrokes'];
      $.each(userData.Number_Of_Keys_Per_Session, function(key, val)
      {
        item = {sessionDate: key, keystrokes: val};
        data.push(item);
      });
    }

    if(chartType == "Number Of Actions Per Session")
    {
      ys=['actions'];
      xs = 'sessionDate';
      l = ['Actions'];
      $.each(userData.Number_Of_Actions_Per_Session, function(key, val)
      {
        item = {sessionDate: key, actions: val};
        data.push(item);
      });
    }

    if(chartType == "Number Of Clicks Per Session")
    {
      ys=['mouseclicks'];
      xs = 'sessionDate';
      l = ['Mouse-Clicks'];
      $.each(userData.Number_Of_Click_Per_Session, function(key, val)
      {
        item = {sessionDate: key, mouseclicks: val};
        data.push(item);
      });
    }

    if(chartType == "Number Of Programs Used Per Session")
    {
      ys=['programsUsed'];
      xs = 'sessionDate';
      l = ['Number Of Programs'];
      $.each(userData.Number_Of_Programs_User_Per_Session, function(key, val)
      {
        item = {sessionDate: key, programsUsed: val};
        data.push(item);
      });
    }
    new Morris.Bar({
      resize: true,
      // ID of the element in which to draw the chart.
      element: 'userChart',
      // Chart data records -- each entry in this array corresponds to a point on
      // the chart.
      data: data,
      // The name of the data record attribute that contains x-values.
      xkey: xs,
      // A list of names of data record attributes that contain y-values.
      ykeys: ys,
      // Labels for the ykeys -- will be displayed when you hover over the
      // chart.
      labels: l
    });

}

function loadPopulationData()
{
  var resp = $.ajax({
    type:"GET",
    url: "/generatePopulationStats"
  })
  resp.done(function(returnedJson)
  {
    populationData = $.parseJSON(returnedJson);
    generatePopulationChart();
  });
}

function generatePopulationChart()
{
    $("#populationChart").empty();

    var data = [];
    var ys = [];
    var xs = [];

    var chartType = $("#populationChartType").val();

    if(chartType == "Average Time Per Session")
    {
      ys=['timeSpent'];
      xs = 'userID';
      l = ['Time Spent'];
      $.each(populationData.Average_Time_Per_Session, function(key, val)
      {
        item = {userID: key, timeSpent: val};
        data.push(item);
      });
    }
    if(chartType == "Average Time Per Day")
    {
      ys=['timeSpent'];
      xs = 'userID';
      l = ['Time Spent'];
      $.each(populationData.Average_Time_Per_Day, function(key, val)
      {
        item = {userID: key, timeSpent: val};
        data.push(item);
      });
    }
    if(chartType == "Average Actions Per Session")
    {
      ys=['actions'];
      xs = 'userID';
      l = ['Actions'];
      $.each(populationData.Average_Actions_Per_Session, function(key, val)
      {
        item = {userID: key, actions: val};
        data.push(item);
      });
    }
    if(chartType == "Average Keystrokes Per Session")
    {
      ys=['keystrokes'];
      xs = 'userID';
      l = ['Keystrokes'];
      $.each(populationData.Average_Keys_Per_Session, function(key, val)
      {
        item = {userID: key, keystrokes: val};
        data.push(item);
      });
    }

    if(chartType == "Average Clicks Per Session")
    {
      ys=['clicks'];
      xs = 'userID';
      l = ['Clicks'];
      $.each(populationData.Average_Click_Per_Session, function(key, val)
      {
        item = {userID: key, clicks: val};
        data.push(item);
      });
    }

    if(chartType == "Average Number Of Programs Used Per Session")
    {
      ys=['numProgs'];
      xs = 'userID';
      l = ['Number Of Programs'];
      $.each(populationData.Average_Number_Programs_Per_Session, function(key, val)
      {
        item = {userID: key, numProgs: val};
        data.push(item);
      });
    }

    new Morris.Line({
      resize: true,
      // ID of the element in which to draw the chart.
      element: 'populationChart',
      // Chart data records -- each entry in this array corresponds to a point on
      // the chart.
      data: data,
      // The name of the data record attribute that contains x-values.
      xkey: xs,
      // A list of names of data record attributes that contain y-values.
      ykeys: ys,
      // Labels for the ykeys -- will be displayed when you hover over the
      // chart.
      labels: l
    });

}

function generatePopulationChartChart()
{
    $("#populationChart").empty();

    var data = [];
    var ys = [];
    var xs = [];

    var chartType = $("#populationChartType").val();

    if(chartType == "Average Time Per Session")
    {
      ys=['timeSpent'];
      xs = 'userID';
      l = ['Time Spent'];
      $.each(populationData.Average_Time_Per_Session, function(key, val)
      {
        item = {userID: key, timeSpent: val};
        data.push(item);
      });
    }
    if(chartType == "Average Time Per Day")
    {
      ys=['timeSpent'];
      xs = 'userID';
      l = ['Time Spent'];
      $.each(populationData.Average_Time_Per_Day, function(key, val)
      {
        item = {userID: key, timeSpent: val};
        data.push(item);
      });
    }
    if(chartType == "Average Actions Per Session")
    {
      ys=['actions'];
      xs = 'userID';
      l = ['Actions'];
      $.each(populationData.Average_Actions_Per_Session, function(key, val)
      {
        item = {userID: key, actions: val};
        data.push(item);
      });
    }
    if(chartType == "Average Keystrokes Per Session")
    {
      ys=['keystrokes'];
      xs = 'userID';
      l = ['Keystrokes'];
      $.each(populationData.Average_Keys_Per_Session, function(key, val)
      {
        item = {userID: key, keystrokes: val};
        data.push(item);
      });
    }

    if(chartType == "Average Clicks Per Session")
    {
      ys=['clicks'];
      xs = 'userID';
      l = ['Clicks'];
      $.each(populationData.Average_Click_Per_Session, function(key, val)
      {
        item = {userID: key, clicks: val};
        data.push(item);
      });
    }

    if(chartType == "Average Number Of Programs Used Per Session")
    {
      ys=['numProgs'];
      xs = 'userID';
      l = ['Number Of Programs'];
      $.each(populationData.Average_Number_Programs_Per_Session, function(key, val)
      {
        item = {userID: key, numProgs: val};
        data.push(item);
      });
    }

    var myBarChart = new Chart(ctx,{type: 'bar', data : data, options: options});

}
