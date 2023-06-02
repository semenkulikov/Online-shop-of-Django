function AddToCart(url) {
    let quantity = 1
    if (document.getElementById("amount")) {
        quantity = document.getElementById("amount").value;
    }

    $.ajax({
    url: url,
    type: "GET",
    data:
        {
            'quantity': quantity
        },
    dataType: "text",
    success: (data) => {
        console.log(url)
        $("#modal_open").fadeIn(200);
        let obj =$.parseJSON(data)
        $(".CartBlock-amount").text(obj['cart_count']);
        $(".CartBlock-price").text(obj['cart_sum']);
        document.getElementById("amount").value = 1;
        },
     error: (error) => {
      console.log(error);
    }
  });
}

$("body").click(function () {
    $("#modal_open").fadeOut(300);
});

$(".close").click(function () {
    $("#modal_open").fadeOut(300);
});
