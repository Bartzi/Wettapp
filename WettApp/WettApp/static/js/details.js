// javascript helper functions for bets/details.html


$(document).ready(function()
{
    $("#increase-div").mouseover(showIncrease);
    $("#increase-div").mouseout(hideIncrease);
    $(".increase.increase-button").click(test);
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

function test()
{
    alert("test");
}