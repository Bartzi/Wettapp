// javascript helper functions for bets/details.html


$(document).ready(function()
{
    $("#increase-div").mouseover(showIncrease);
    $("#increase-div").mouseout(hideIncrease);
    $(".increase.increase-button").click(increaseScore);
    $(".increase.increase-button").hide();  
})

function showIncrease()
{
   $(".increase.increase-button").show();  
}

function hideIncrease()
{
    $(".increase.increase-button").hide();    
}

function increaseScore()
{
    var queryString = "/bets/increase?bet=" + getBetId();
    $.get(queryString, function(data){
        var htmlString = "<strong>" + data + "</strong>";
        $(".increase.increase-score").html(htmlString);
    });
}

function getBetId()
{
    var url = document.location.href;
    var IdString = url.match(/\/\d+\//);
    return url.substr(IdString.index, IdString.lastIndex).match(/\d+/);
    
}