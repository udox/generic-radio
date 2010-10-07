/* Radio player JS control \o/ ~jaymz
   ----------------------------------

   Here we have the main player control for swaping out data and banners.
   The player template will output a hidden div containing the JSON data
   for loading into the main-show column. It all uses id's in the template.

   Because of all sorts of injection stuff we'll probably want to swap out
   the eval call for a JSON.parse() at some point with the right JS included.
*/

$(document).ready(function() {

    // Grab the first banner that is on the page - should be the skin banner
    var defaultSponsorImage = $('#sponsor-banner').attr('src');
    var defaultSponsorUrl = $('#sponsor-link').attr('href');
    
    $('.radio-hidden').hide(); // Hide anything on load that's not needed
    $('#embed-info').hide();

    $('.showname').bind('click', function() {
        $('#embed-info').fadeOut();
        var showData = eval('('+$(this).next('.jsondata').html()+')');
        $('#ms-picture').attr('src', showData.picture);

        if(showData.sponsor_image) {
            $('#sponsor-banner').attr('src', showData.sponsor_image);
            $('#sponsor-link').attr('href', showData.sponsor_url);
        } else {
            $('#sponsor-banner').attr('src', defaultSponsorImage);
            $('#sponsor-link').attr('href', defaultSponsorUrl);
        }

        $('#ms-description').html(showData.description);
        
        if(showData.subtitle) {
            $('#ms-show-title').html(showData.subtitle);
        } else {
            $('#ms-show-title').html(showData.title);
        }
        if(!showData.series_title) {
            $('#ms-series-title').html(showData.title);
        } else {
            $('#ms-series-title').html(showData.series_title);
        }
        $.get(showData.flash_player_url, function(data) {
            $('#ms-player').html(data);
        });
        
        $('#ms-embed').attr('href', showData.embed_url);
        $('#ms-download').attr('href', showData.download_url);
        
        if(showData.download) {
            $('.download-icon').show();
            $('#ms-download').show();
        } else {
            $('.download-icon').hide();
            $('#ms-download').hide();
        }
        
    });

    $('#ms-embed').bind('click', function(e) {
        e.preventDefault();
        $('#embed-info').fadeIn();
        $.get($(this).attr('href'), function(data) {
            $('#show-embedcode').val(data);
        });
    });

});