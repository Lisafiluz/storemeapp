function buy_cart() {
    let orders_id = [];
    index = 0
    $("#cart tr").each(function() {
        console.log(this);
        if (index !== 0) {
            orders_id.push($(this).attr("id"))
            $(this).remove()
        }
        index += 1; 
    });
    $("#totalPrice").html(parseFloat(0.00))
    console.log(orders_id);
    fetch('/buy/' + orders_id, 
        {method: 'POST'}
    )
    location.reload()
    //alert("your order is checked! you will get it soon as possible")
}