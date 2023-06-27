function CartUpdate() {
    let t_href = event.target.getAttribute('href');
    var href =  $(this).data("href");
    console.log(href)
        $.ajax(
            {
                url: href,

                success: function (data){
                    console.log(data.items)
                    $(".CartBlock-amount").text(data['cart_count']);
                    $(".CartBlock-price").text(data['cart_sum']);
                    $('.Cart').html(data.items)
                }
            }
        )
}

$(document).ready(function(){
    $('.Cart').on('click', 'button[type="button"]', CartUpdate)


}
)
function AddToCart(url) {

    $.ajax({
        url: url,
        success: (data) => {
            console.log(data.items)
            $("#modal_open").fadeIn(200);

            $(".CartBlock-amount").text(data['cart_count']);
            $(".CartBlock-price").text(data['cart_sum']);

            },

  });
}

$("body").click(function () {
    $("#modal_open").fadeOut(300);
});

$(".close").click(function () {
    $("#modal_open").fadeOut(300);
});
