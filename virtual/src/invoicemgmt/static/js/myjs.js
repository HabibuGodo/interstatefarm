// WEBSITE =============================================================
// FOR PARTNERS SLIDING ****************************
$(document).ready(function () {
    $(".owl-carousel").owlCarousel({
        items: 4,
        itemsDesktop: [1000, 3],
        itemsDesktopSmall: [900, 3],
        itemsTablet: [600, 2],
        autoPlay: 4000,
        itemsMobile: false,
        loop: true,
        margin: 10,
        responsiveClass: true,
        pagination: false,
        responsive: {
            0: {
                items: 1
            },
            480: {
                items: 2
            },
            768: {
                items: 4
            }
        }
    });

});

// FOR NUMBER CAOUNT IN SPANNING AREAS ************
$(document).ready(function () {
    $('#value1,#value2,#value3').each(function () {
        $(this).prop('Counter', 100).animate({
            Counter: $(this).text()
        }, {
            duration: 500,
            easing: 'swing',
            step: function (now) {
                $(this).text(Math.ceil(now));
            }
        });
    });

});


// CUSTOMER =============================================================

// ORDER INFO *************************** 
$(document).ready(function () {
    $("#beans_90g, #ground_90g,#beans_250g, #ground_250g,#beans_400g, #ground_400g,#beans_750g, #ground_750g,#beans_1kg, #ground_1kg").keyup(function () {

        var gram_90_beans = $("#beans_90g").val() * 0.09;
        var gram_90_ground = $("#ground_90g").val() * 0.09;
        var gram_250_beans = $("#beans_250g").val() * 0.25;
        var gram_250_ground = $("#ground_250g").val() * 0.25;
        var gram_400_beans = $("#beans_400g").val() * 0.4;
        var gram_400_ground = $("#ground_400g").val() * 0.4;
        var gram_750_beans = $("#beans_750g").val() * 0.75;
        var gram_750_ground = $("#ground_750g").val() * 0.75;
        var kilogram_1_beans = $("#beans_1kg").val() * 1;
        var kilogram_1_ground = $("#ground_1kg").val() * 1;

        var total_beans = gram_90_beans + gram_250_beans + gram_400_beans + gram_750_beans + kilogram_1_beans;
        var total_ground = gram_90_ground + gram_250_ground + gram_400_ground + gram_750_ground + kilogram_1_ground;
        var total_kilo = total_beans + total_ground;

        if (total_kilo < 10) {
            // RETAIL SALE TZS
            var gram_90_beans_amount = $("#beans_90g").val() * 5900;
            var gram_90_ground_amount = $("#ground_90g").val() * 5900;
            var gram_250_beans_amount = $("#beans_250g").val() * 10050;
            var gram_250_ground_amount = $("#ground_250g").val() * 10050;
            var gram_400_beans_amount = $("#beans_400g").val() * 13500;
            var gram_400_ground_amount = $("#ground_400g").val() * 13500;
            var gram_750_beans_amount = $("#beans_750g").val() * 25950;
            var gram_750_ground_amount = $("#ground_750g").val() * 25950;
            var kilogram_1_beans_amount = $("#beans_1kg").val() * 29500;
            var kilogram_1_ground_amount = $("#ground_1kg").val() * 29500;

            // RETAIL SALE USD
            var gram_90_beans_amount_usd = $("#beans_90g").val() * 2.7;
            var gram_90_ground_amount_usd = $("#ground_90g").val() * 2.7;
            var gram_250_beans_amount_usd = $("#beans_250g").val() * 4.9;
            var gram_250_ground_amount_usd = $("#ground_250g").val() * 4.9;
            var gram_400_beans_amount_usd = $("#beans_400g").val() * 7.7;
            var gram_400_ground_amount_usd = $("#ground_400g").val() * 7.7;
            var gram_750_beans_amount_usd = $("#beans_750g").val() * 11.7;
            var gram_750_ground_amount_usd = $("#ground_750g").val() * 11.7;
            var kilogram_1_beans_amount_usd = $("#beans_1kg").val() * 13.5;
            var kilogram_1_ground_amount_usd = $("#ground_1kg").val() * 13.5;

        } else {
            // WHOLE SALE 
            var gram_90_beans_amount = $("#beans_90g").val() * 3300;
            var gram_90_ground_amount = $("#ground_90g").val() * 3300;
            var gram_250_beans_amount = $("#beans_250g").val() * 7700;
            var gram_250_ground_amount = $("#ground_250g").val() * 7700;
            var gram_400_beans_amount = $("#beans_400g").val() * 11800;
            var gram_400_ground_amount = $("#ground_400g").val() * 11800;
            var gram_750_beans_amount = $("#beans_750g").val() * 20650;
            var gram_750_ground_amount = $("#ground_750g").val() * 20650;
            var kilogram_1_beans_amount = $("#beans_1kg").val() * 25000;
            var kilogram_1_ground_amount = $("#ground_1kg").val() * 25000;

            

            // WHOLE SALE USD
            var gram_90_beans_amount_usd = $("#beans_90g").val() * 1.5;
            var gram_90_ground_amount_usd = $("#ground_90g").val() * 1.5;
            var gram_250_beans_amount_usd = $("#beans_250g").val() * 3.6;
            var gram_250_ground_amount_usd = $("#ground_250g").val() * 3.6;
            var gram_400_beans_amount_usd = $("#beans_400g").val() * 6.1;
            var gram_400_ground_amount_usd = $("#ground_400g").val() * 6.1;
            var gram_750_beans_amount_usd = $("#beans_750g").val() * 9.5
            var gram_750_ground_amount_usd = $("#ground_750g").val() * 9.5;
            var kilogram_1_beans_amount_usd = $("#beans_1kg").val() * 11.5;
            var kilogram_1_ground_amount_usd = $("#ground_1kg").val() * 11.5;

        }


        var amount_tzs = gram_90_beans_amount + gram_90_ground_amount +
            gram_250_beans_amount + gram_250_ground_amount +
            gram_400_beans_amount + gram_400_ground_amount +
            gram_750_beans_amount + gram_750_ground_amount +
            kilogram_1_beans_amount + kilogram_1_ground_amount;

        var amount_usd = gram_90_beans_amount_usd + gram_90_ground_amount_usd +
            gram_250_beans_amount_usd + gram_250_ground_amount_usd +
            gram_400_beans_amount_usd + gram_400_ground_amount_usd +
            gram_750_beans_amount_usd + gram_750_ground_amount_usd +
            kilogram_1_beans_amount_usd + kilogram_1_ground_amount_usd;

        var amount_vat_tzs = (18 / 100) * amount_tzs;
        var amount_vat_usd = (18 / 100) * amount_usd;
        var amount_sub_total_tzs = amount_tzs - amount_vat_tzs;
        var amount_sub_total_usd = amount_usd - amount_vat_usd;


        // ASSIGNING VALUE TO FIELDS 
        $("#beans_total").val(total_beans.toFixed(2));
        $("#ground_total").val(total_ground.toFixed(2));
        $("#total_kgs").val(total_kilo.toFixed(2));
        $("#total_amount_tzs").val(amount_tzs.toFixed(2));
        $("#total_amount_usd").val(amount_usd.toFixed(2));
        $("#amount_vat_tzs").val(amount_vat_tzs.toFixed(2));
        $("#amount_vat_usd").val(amount_vat_usd.toFixed(2));
        $("#amount_sub_total_tzs").val(amount_sub_total_tzs.toFixed(2));
        $("#amount_sub_total_usd").val(amount_sub_total_usd.toFixed(2));

    });
});


// STAFF =============================================================

$(document).ready(function () {

    $("#line5_product, #line6_product,#line7_product,#line8_product").hide();
    $('#more-line').click(function () {
        $('#line5_product,#line6_product,#line7_product,#line8_product').finish().show(200);
        $("#more-line").hide();
    });
    $("#product_quantity1, #product_price1,#product_quantity2, #product_price2,#product_quantity3, #product_price3,#product_quantity4, #product_price4,#product_quantity5, #product_price5,#product_quantity6, #product_price6,#product_quantity7, #product_price7,#product_quantity8, #product_price8, #discount_rate").keyup(function () {
        // LINE 1
        var product_quantity1 = $("#product_quantity1").val();
        var product_price1 = $("#product_price1").val();
        var line1_total = product_quantity1 * product_price1;

        // LINE 2
        var product_quantity2 = $("#product_quantity2").val();
        var product_price2 = $("#product_price2").val();
        var line2_total = product_quantity2 * product_price2;

        // LINE 3
        var product_quantity3 = $("#product_quantity3").val();
        var product_price3 = $("#product_price3").val();
        var line3_total = product_quantity3 * product_price3;

        // LINE 4
        var product_quantity4 = $("#product_quantity4").val();
        var product_price4 = $("#product_price4").val();
        var line4_total = product_quantity4 * product_price4;

        // LINE 5
        var product_quantity5 = $("#product_quantity5").val();
        var product_price5 = $("#product_price5").val();
        var line5_total = product_quantity5 * product_price5;

        // LINE 6
        var product_quantity6 = $("#product_quantity6").val();
        var product_price6 = $("#product_price6").val();
        var line6_total = product_quantity6 * product_price6;

        // LINE 7
        var product_quantity7 = $("#product_quantity7").val();
        var product_price7 = $("#product_price7").val();
        var line7_total = product_quantity7 * product_price7;

        // LINE 8
        var product_quantity8 = $("#product_quantity8").val();
        var product_price8 = $("#product_price8").val();
        var line8_total = product_quantity8 * product_price8;


        //  TOTAL PRICE  
        var total_price = line1_total + line2_total + line3_total + line4_total + line5_total + line6_total + line7_total + line8_total;
        var tax_total = ((18 / 100) * total_price);
        var sub_total = total_price - tax_total;
        var discount = ($("#discount_rate").val() / 100) * total_price;
        var total_after = total_price - discount

        // ASSIGNING VALUE TO FIELDS 
        $("#product_total_price1").val(line1_total);
        $("#product_total_price2").val(line2_total);
        $("#product_total_price3").val(line3_total);
        $("#product_total_price4").val(line4_total);
        $("#product_total_price5").val(line5_total);
        $("#product_total_price6").val(line6_total);
        $("#product_total_price7").val(line7_total);
        $("#product_total_price8").val(line8_total);



        $("#total").val(total_after);
        $("#discount").val(discount);
        $("#sub_total").val(sub_total);
        $("#tax").val(tax_total);

    })


    $(".table").paging({ limit: 15 });

    // Data Picker Initialization
    $('.datepicker').datepicker();
});

//CANCEL BUTTON;

$(document).ready(function () {
    $('#btn-cancel').on('clock', ".cancel-order" , function (e) {
       e.preventDefault();
       var $this = $(this);
       let cancelData = $this.parents('').find('td').eq(0).text();

       return false;
    });

});




function showModel() {
   
   $("#myModal").modal('show');l
};



