// javascript helper functions for bets/details.html

var content;

function showIncrease(obj)
{
    content = obj.innerHTML;
    obj.innerHTML += "<div class='increase-button'><button type='button'><i class='icon-plus'></i></button></div>";
}

function hideIncrease(obj)
{
    obj.innerHTML = content;
}