
(function() {
    'use strict';
    window.addEventListener('load', function() {
      // Fetch all the forms we want to apply custom Bootstrap validation styles to
      var forms = document.getElementsByClassName('needs-validation');
      // Loop over them and prevent submission
      var validation = Array.prototype.filter.call(forms, function(form) {
        form.addEventListener('submit', function(event) {
          if (form.checkValidity() === false) {
            event.preventDefault();
            event.stopPropagation();
          }
          form.classList.add('was-validated');
        }, false);
      });
    }, false);
  })();

$(document).on('submit', '#addToWatchlist', function(e){
    e.preventDefault();

    if ($('#button-auction').hasClass('added')){
        $.ajax({
            type:'POST',
            url: $(this).attr('action'),
            data: $(this).serialize(),
            success:function(){
                watchlist = $('#watchListTotal')
                actualValue = watchlist.html()
                watchlist.text(parseInt(actualValue) - 1)
                $('#heart').css("color", "white")
                $('#button-auction').removeClass('added')
            }
        })
    } else{
        $.ajax({
            type:'POST',
            url: $(this).attr('action'),
            data: $(this).serialize(),
            success:function(){
                watchlist = $('#watchListTotal')
                actualValue = watchlist.html()
                watchlist.text(parseInt(actualValue) + 1)
                $('#heart').css("color", "red")
                $('#button-auction').addClass('added')
            }
        })
    }
});

$(document).on('submit', '#addBid', function(e){
    e.preventDefault();
    auction = $(this).data("auction")
    lastBid = $(this).data("lastbid")
    startingBid = $(this).data("startingbid")
    newBid = $('#newBid').val()
    message = $('#message')

    if(lastBid == 'None'){
        lastBid = 0
    } else{
        lastBid = parseInt(lastBid)
    }

    newBid = parseInt(newBid)
    startingBid = parseInt(startingBid)
    
    console.log(lastBid,startingBid)

    if(newBid > 0 && newBid > lastBid && newBid > startingBid){
        $.ajax({
            type:'POST',
            url: $(this).attr('action'),
            data: $(this).serialize(),
            success: function() {
                $(`.lastBid${auction}`).val(newBid)
                $(`.lastBid${auction}`).html(`Current Bid: ${newBid}`)
                totalValue = $('#smallTotalBid').html()
                $('#smallTotalBid').html(parseInt(totalValue) + 1)
                $('#yourLastBid').html('Your bid is the current bid.')
                $('#newBid').val('')
                message.remove()
            }
        });
    } else if (newBid === lastBid || newBid === startingBid) {
        message.html('Your bid is equal than the current bid')
    } else {
        message.html('Your bid is lower than the current bid')
    }
})

$(document).on('submit', '#deleteFromWatchlist', function(e){
    e.preventDefault();
    auctionId = $(this).data('auction')
    auction = $(`#auction${auctionId}`)
    watchlist = $('#watchListTotal')

    $.ajax({
        type:'POST',
        url: $(this).attr('action'),
        data: $(this).serialize(),
        success: function() {
            console.log('deleted')
            auction.remove()
            watchlist = $('#watchListTotal')
            actualValue = watchlist.html()
            watchlist.text(parseInt(actualValue) - 1)
        }
    })
})

$(document).on('submit', '#deleteComment', function(e){
    e.preventDefault();
    commentId = $(this).data('comment')
    comment = $(`#comment${commentId}`)

    $.ajax({
        type:'POST',
        url: $(this).attr('action'),
        data: $(this).serialize(),
        success: function() {
            console.log('deleted')
            comment.remove()
        }
    })

})

function toggleVisibilityPassword(id, button){
    var password = document.getElementById(id)
    var button = document.getElementById(button)
  
    if(password.type === "password"){
      password.type = "text";
      button.setAttribute('class', "fa fa-eye-slash")
  
    } else {
      password.type = "password"
      button.setAttribute('class', "fa fa-eye")
    }
}