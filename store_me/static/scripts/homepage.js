let eventListeners = [];
//load_storage()
//  function load_storage() {
//      $("#cart_dropdown").html(localStorage.cart)
//  }


function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function show_cart() {
    $("#cart_dropdown").addClass("show");
    await sleep(1500);
    $("#cart_dropdown").removeClass("show");
}
document.querySelectorAll('.add_to_cart_btn').forEach(item => {
    item.addEventListener('click', event => {
        new_row = "<tr id=" + $(item).attr("id") + ">" + "<td>" + $('#cart tr').length + "</td>" 
                    + "<td>" + $(item).attr("productName") + "</td>"
                    + "<td>" + $(item).attr("price") + "</td>"
                    + "<td><button class='btn btn-outline-danger my-2 my-sm-0 del_btn' tr_id="+$(item).attr("id")+">Delete</button></td>" +
                "</tr>";
        $("#totalPrice").html(parseFloat(parseFloat($("#totalPrice").html()) + parseFloat($(item).attr("price"))).toFixed(2))
        $('#cart tr:last').after(new_row);
        show_cart()
        add_listeners() 
        // add_to_storage()
    })
});

function add_listeners() {
    document.querySelectorAll('.del_btn').forEach(item => {
        if (!eventListeners.includes(item)){
            eventListeners.push(item)
            item.addEventListener('click', event => {
                console.log(eventListeners);
                console.log(parseFloat($("#totalPrice").html()));
                console.log(parseFloat($("table #"+$(item).attr("tr_id")+" td:eq(2)").html()));
                $("#totalPrice").html(parseFloat(parseFloat($("#totalPrice").html()) - parseFloat($("table #"+$(item).attr("tr_id")+" td:eq(2)").html())).toFixed(2))
                $("table #"+$(item).attr("tr_id")).remove()
                //add_to_storage()
            })
        }
        
    })
}

// function add_to_storage() {
//     let table = {}
//     let index = 0
//     $("#cart tr").each(function() {
//        console.log(this);
//        table[this.id] this
//     });
//     console.log(table);
//     localStorage.setItem('testObject', JSON.stringify(testObject));
//     localStorage.setItem('cart', JSON.stringify(table));
// }