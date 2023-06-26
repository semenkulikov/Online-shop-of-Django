window.onload = function (){
    $('.Cart').on('click', 'button[class="Amount-remove"]', function () {
            let t_href = event.target;

        $.ajax(
            {

                url: t_href.name,
                success: function (data){
                    console.log(data)
                    $('.Cart').html(data.items)
                }
            }

        )
        }
    )

    $('.Cart').on('click', 'button[class="Amount-add"]', function () {
            let t_href = event.target;

        $.ajax(
            {

                url: t_href.name,
                success: function (data){
                    console.log(data)
                    $('.Cart').html(data.items)
                }
            }

        )
        }
    )


}