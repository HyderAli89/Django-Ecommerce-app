$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 2,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 4,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 6,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

$('.plus-cart').click(function(){
    console.log("Button CLick")
    var id=$(this).attr("pid").toString();
    var eml=this.parentNode.children[2] 
     $.ajax({
         type:"GET",
         url:"/pluscart",
         data:{
            prod_id:id
         },
         success:function(data){
            console.log("data = ",data);    
            eml.innerText=data.quantity 
            document.getElementById("amount").innerText=data.amount 
            document.getElementById("totalamount").innerText=data.totalamount
         }
     })
})

$('.minus-cart').click(function(){
    console.log("minus cart")
    var id=$(this).attr("pid").toString();
    var eml=this.parentNode.children[2] 
    $.ajax({
        type:"GET",
        url:"/minuscart",
        data:{
            prod_id:id
        },
        success:function(data){
            eml.innerText=data.quantity 
            document.getElementById("amount").innerText=data.amount 
            document.getElementById("totalamount").innerText=data.totalamount
        }
    })
})

// Attach the click event to elements with the "remove-cart" class
$('.remove-cart').click(function () {
    console.log("Removing item from cart");
    var id = $(this).attr("pid").toString();  // Get product ID from the "pid" attribute
    var element = this;  // Reference to the clicked "Remove item" link

    // Make AJAX request to remove item from cart
    $.ajax({
        type: "GET",
        url: "/removecart/",  // The URL for the remove cart endpoint
        data: {
            prod_id: id  // Pass the product ID to the backend
        },
        success: function (data) {
            if (data.error) {
                alert(data.error);  // Display error message if any
            } else {
                // Dynamically update the amount and total amount on the cart page
                document.getElementById("amount").innerText = data.amount;
                document.getElementById("totalamount").innerText = data.totalamount;
                element.parentNode.parentNode.parentNode.remove()
                // Optionally, remove the product row or item from the cart display
                // $(element).closest('.cart-item').remove();
            }
        },
        error: function (xhr, status, error) {
            console.error("Error removing item from cart:", error);
        }
    });
});



$('.plus-wishlist').click(function(){
    var id=$(this).attr("pid").toString();
    $.ajax({
        type:"GET",
        url:"/pluswishlist",
        data:{
            prod_id:id
        },
        success:function(data){
            //alert(data.message)
            window.location.href = `http://localhost:8000/product-detail/${id}`  // redirecting to  product page
        }
    })
})


$('.minus-wishlist').click(function(){
    var id=$(this).attr("pid").toString();
    $.ajax({
        type:"GET",
        url:"/minuswishlist",
        data:{
            prod_id:id
        },
        success:function(data){
            window.location.href = `http://localhost:8000/product-detail/${id}`
        }
    })
})


