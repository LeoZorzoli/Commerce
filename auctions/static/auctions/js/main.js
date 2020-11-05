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
    newBid = $('#newBid').val()
    lastBid = $(`.lastBid${auction}`).val()
    message = $('#message')
    console.log(lastBid)

    if(newBid > 0 && newBid > lastBid){
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
            }
        });
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
