/* Radio player JS control \o/ ~jaymz
   ----------------------------------

   Here we have the main player control for swaping out data and banners.
   The player template will output a hidden div containing the JSON data
   for loading into the main-show column. It all uses id's in the template.

   Because of all sorts of injection stuff we'll probably want to swap out
   the eval call for a JSON.parse() at some point with the right JS included.
*/

$('.showname').bind('click', function() {
    var showData = eval('('+$(this).next('.jsondata').html()+')');
    $('#ms-picture').attr('src', showData.picture);
    $('#ms-description').html(showData.description);
    $('#ms-show-title').html(showData.title);
    if(!showData.series_title) {
        $('#ms-series-title').html(showData.title);
    } else {
        $('#ms-series-title').html(showData.series_title);
    }
});