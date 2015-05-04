$(document).ready( function(){
    $('.pull-me').click( function() {
        $('.panel').slideToggle('slow');
    });
});
/*
$(document).ready(function() {
   $('.nav').mouseenter(function() {
       $(this).animate({
           height: '+=10px'
       });
   });
   $('.nav').mouseleave(function() {
       $(this).animate({
           height: '-=10px'
       }); 
   });
   $('.nav').click(function() {
       $(this).toggle(1000);
   }); 
});
*/