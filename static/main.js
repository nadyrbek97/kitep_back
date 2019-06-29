// Enable Django CsRf-ready AJAX calls
// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
/// Default Django Configuration

// adding like
$("#book-like-form").submit(function (e) {
    e.preventDefault();

    console.log("form is working");
    let thisForm = $(this);
    let actionEndPoint = thisForm.attr("action") || window.location.href;
    let method = thisForm.attr("method");
    let formData = thisForm.serialize();
    console.log(thisForm.attr("action"));
    console.log(thisForm.attr("method"));

    $.ajax({
        url: actionEndPoint,
        method: method,
        data: formData,
        success: handleFormSuccess,
        error: handleFormError
    });

    function handleFormSuccess(data, textStatus, jqXHR) {

        console.log('success');
        console.log('addding like');
        console.log(data);
        let likeAmountText = $("#like-amount").text();
        let likeButtonText = $("#book-like-btn").text();
        console.log(likeAmountText);
        console.log(likeButtonText);
        console.log(data['is_liked']);
        addLike(data, likeAmountText);
    }

    function addLike(data, text) {
            if (data['is_liked'] === true){
                let amountInt = parseInt(text);
                amountInt += 1;
                $("#like-amount").html(amountInt.toString() + " <img src=\"https://img.icons8.com/material-rounded/24/000000/like.png\">");
                $("#book-like-btn").html("Unlike" + " <img src=\"https://img.icons8.com/metro/26/000000/thumbs-down.png\">")

            }
            else{
                let amountInt = parseInt(text);
                amountInt -= 1;
                $("#like-amount").html(amountInt.toString() + " <img src=\"https://img.icons8.com/material-rounded/24/000000/like.png\">");
                $("#book-like-btn").html("Like" + " <img class=\"like-image\" src=\"https://img.icons8.com/material-sharp/24/000000/facebook-like.png\">")

            }
        }

    function handleFormError(jqXHR, textStatus, errorThrown) {
        console.log(jqXHR);
        console.log(textStatus);
        console.log(errorThrown);
    }


});

// adding comment
$("#form-comment-post").submit(function (event) {

    event.preventDefault();
    console.log("Form is not working");
    let thisForm = $(this);
    let actionEndPoint = thisForm.attr("action") || window.location.href;
    let method = thisForm.attr("method");
    let formData = thisForm.serialize();
    console.log(thisForm.attr("action"), thisForm.attr("method"));

    $.ajax({
        url: actionEndPoint,
        method: method,
        data: formData,
        success: handleFormSuccess,
        error: handleFormError
    });

    function handleFormSuccess(data, textStatus, jqXHR) {
        console.log(data);
        console.log(textStatus);
        console.log(jqXHR);
        // adding new created innerHTML
        addComment(data['username'], data['body'], data['date']);
        alert("Your comment was successfully added");
        $("#form-comment-post")[0].reset(); // reset form data

    }

    function handleFormError(jqXHR, textStatus, errorThrown) {
        console.log(jqXHR);
        console.log(textStatus);
        console.log(errorThrown);
    }

    function addComment(username, body, date) {

        // change comment count
        let commentCount = $("#comment-count");
        // getting text using jquery
        let textCommentCount = commentCount.text();
        console.log(textCommentCount);
        // parse text to Integer and add 1
        let intCommentCount = parseInt(textCommentCount) + 1;
        console.log(intCommentCount);
        let countText = intCommentCount.toString();
        commentCount.text(countText);


        // ############### COMMENT SECTION DIV
        let commentSection = $("<div class='col-md-10'></div>");

        // ############### COMMENT SECTION ROW
        let commentSectionRow = $("<div class='row'></div>");

        // ################ COMMENT CARD BODY
        let commentCardBody = $("#comment-card-body");

        // ################ COMMENT CARD

        // ############### add username using jquery
        let s = $("<strong class='text-primary'></strong>");
        s.text(username + ": ");
        let a = $("<a class='float-left'></a>");
        a.append(s);
        let username_p = $("<p></p>");
        username_p.append(a);

        // ############### add clearfix div
        let clearfix_div = $("<div class='clearfix'></div>");

        // add body
        let body_p = $("<p class='ml-3 mt-3'></p>");
        body_p.text(body);

        // ############### add date paragraph

        let date_p = $("<p class='badge badge-primary text-wrap'></p>");
        date_p.text(date);


        // ############### add like and reply buttons

        // <i/>

        let reply_icon = $("<img src=\"https://img.icons8.com/android/24/000000/reply-arrow.png\">");

        let like_icon = $("<img class=\"like-image\" src=\"https://img.icons8.com/material-sharp/24/000000/facebook-like.png\">");

        // <a> </a>

        let reply_a = $("<a class='float-right btn btn-outline-primary text-white ml-2'></a>");

        let like_a = $("<a class='float-right btn btn-danger ml-2'></a>");

        // add <i/> to <a> </a>
        reply_a.append(reply_icon);
        like_a.append(like_icon);

        // <p> </p>
        let like_reply_p = $("<p></p>");

        // add everything to <p> </p>
        like_reply_p.append(reply_a);
        like_reply_p.append(like_a);

        // ############## add all to commentSection
        commentSection.append(username_p);
        commentSection.append(clearfix_div);
        commentSection.append(body_p);
        commentSection.append(date_p);
        commentSection.append(like_reply_p);

        // ############## add comment to the row
        // commentSectionRow.prepend(commentSection);
        // get last child of row section

        commentSectionRow.append(commentSection);

        commentCardBody.prepend(commentSectionRow);

        // commentCard.prepend(commentCardBody);

        console.log("adding innerHTML ... ")
    }

});
