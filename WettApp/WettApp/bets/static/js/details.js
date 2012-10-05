// javascript helper functions for bets/details.html


jQuery(document).ready(function()
{
    jQuery("#increase-div").mouseover(showIncrease);
    jQuery("#increase-div").mouseout(hideIncrease);
    jQuery(".float-left.increase-button").click(increaseScore);
    jQuery(".float-left.increase-button").hide();  
    var csrftoken = getCookie('csrftoken');
    jQuery.ajaxSetup({
        crossDomain: false,
        beforeSend: function(xhr, settings)
        {
            if (!csrfSafeMethod(settings.type))
            {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
})

/*
 * this function has been taken from https://docs.djangoproject.com/en/dev/ref/contrib/csrf/
 */
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function showIncrease()
{
   jQuery(".float-left.increase-button").show();  
}

function hideIncrease()
{
    jQuery(".float-left.increase-button").hide();    
}

/*
 * this function has been taken from https://docs.djangoproject.com/en/dev/ref/contrib/csrf/
 */
function csrfSafeMethod(method)
{
    return (/^(GET|HEAD|OPTIONS|TRACE)$/).test(method);
}

function increaseScore()
{
    var opponentScoreId = jQuery(".float-left.increase-button").attr("data-score");
    var yourScoreId = jQuery(".your-points").attr("data-score");
    jQuery.post("/bets/increase/", { your_score_id: yourScoreId, opponent_score_id: opponentScoreId }, function(data){
        var htmlString = "<strong>" + data + "</strong>";
        jQuery(".float-left.increase-score").html(htmlString);
    });
}