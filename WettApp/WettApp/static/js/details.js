// javascript helper functions for bets/details.html

var content;

function saveInnerHtml()
{
    content = document.getElementById("increase-div").innerHTML;
}

window.onload = saveInnerHtml;

function showIncrease(obj)
{
    if (document.getElementById("script-div"))
    {
        return;
    }
    var newDiv = document.createElement("div");
    var classAttribute = document.createAttribute("class");
    classAttribute.nodeValue = "increase";
    var idAttribute = document.createAttribute("id");
    idAttribute.nodeValue = "script-div";
    newDiv.setAttributeNode(classAttribute);
    newDiv.setAttributeNode(idAttribute);
    newDiv.innerHTML = "<i class='icon-plus'></i>"

    obj.appendChild(newDiv);
}

function hideIncrease(obj)
{
    var divToRemove = document.getElementById("script-div");
    obj.removeChild(divToRemove);    
}