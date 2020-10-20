$(document).on('submit', '#addToWatchlist', function(e){
    e.preventDefault();

    $.ajax({
        type:'POST',
        url: $(this).attr('action'),
        data: $(this).serialize(),
        success:function(){
            watchlist = $('#watchListTotal')
            actualValue = watchlist.html()
            watchlist.text(parseInt(actualValue) + 1)
            form = $('#addToWatchlist')
            form.remove()
        }
    })
});

$(document).on('submit', '#addBid', function(e){
    e.preventDefault();
    auction = $(this).data("auction")
    newBid = $('#newBid').val()
    lastBid = $(`.lastBid${auction}`).val()

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
    }
})

$(document).on('submit', '#addComment', function(e){
    e.preventDefault();
    commentsList = $('#commentsList')
    commentToAdd = $('#commentToAdd').val()
    comentsListHtml = commentsList.html()
    
    $.ajax({
        type:'POST',
        url: $(this).attr('action'),
        data: $(this).serialize(),
        success: function() {
            console.log('created comment')
            commentsList.html(comentsListHtml + `<li>${commentToAdd}</li>`)
            $('#commentToAdd').val('')
        }
    });
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
