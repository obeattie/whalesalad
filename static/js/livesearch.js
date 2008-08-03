function doSearch() {
    
    var query = $('#searchForm input#s').attr('value');
    
    $('#resultsArea').load("/?s="+query+"&ajax=true #liveResults");

    $('.post').hide();
    $('.nextprevious').hide();
    $('.commentArea').hide();
    $('#resultsArea').show();
    $('#resultsArea').removeClass('searching');
    
}

$(document).ready(function() {
    
    $('#searchForm input#s').bind('keyup', function(event) {        
        setTimeout("doSearch()", 500);
        return false;
    });
    
    $('span.closeResults a').livequery('click', function(event) {
        $('#resultsArea').slideUp();
        $('.post').show();
        $('.nextprevious').show();
        $('.commentArea').show();
        return false;
    });
});