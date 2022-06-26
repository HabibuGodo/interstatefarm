
! function($) {
    "use strict";

    var Adminto = function() {};

    //scroll
    Adminto.prototype.initSticky = function() {
        $("#sticky-nav").sticky({topSpacing: 0});
    },

    Adminto.prototype.initAnimatedScrollMenu = function() {
        $('.navbar-nav a').on('click', function(event) {
            var $anchor = $(this);
            $('html, body').stop().animate({
                scrollTop: $($anchor.attr('href')).offset().top - 0
            }, 1500, 'easeInOutExpo');
            event.preventDefault();
        });
    },

    Adminto.prototype.initScrollspy = function() {
        $(".navbar-nav").scrollspy({
            offset: 50
        });
    },

    Adminto.prototype.init = function() {
        this.initSticky();
        this.initAnimatedScrollMenu();
        this.initScrollspy();
    },
    //init
    $.Adminto = new Adminto, $.Adminto.Constructor = Adminto
}(window.jQuery),

//initializing
function($) {
    "use strict";
    $.Adminto.init();
}(window.jQuery);