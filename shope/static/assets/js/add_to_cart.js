function AddToCart(url) {
    $.ajax({
    url: url,

    type: "GET",
        data: {
        quantity: 2,
        },
    dataType: "text",
    success: (data) => {

        $("#modal_open").fadeIn(200);
        let obj =$.parseJSON(data)
        $(".CartBlock-amount").text(obj['count']);
        $(".CartBlock-price").text(obj['amount']);
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
