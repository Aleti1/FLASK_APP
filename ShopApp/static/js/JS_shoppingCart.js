

// **********************************************************************
// Shoping Cart functions!
// **********************************************************************

// cart : Array
// Item : Object/Class
// addItemToCart
// removeItemFromCart
// removeAll
// setCountForItem
// clearCart
// countCart
// totalCart
// listCart
// saveCart
// loadCart


var JS_shoppingCart = (function(){

    // ==========================================
    // ==========================================
    // ===== private methods and properties =====
    // ==========================================
    // ==========================================

    var cart = [];
    function Item( idProduct, name, price, count ) {
        this.idProduct = idProduct
        this.name = name
        this.price = price
        this.count = count
        this.total = 0.00
    }

    function saveCart() {
        localStorage.setItem( "ShopingCart", JSON.stringify( obj.listCart() ));
    }
        
    function loadCart() {
        cart = 'ShopingCart' in localStorage ? JSON.parse(localStorage.getItem( "ShopingCart" )) : [];
    }
    
    loadCart();

    // =========================================
    // =========================================
    // ===== public methods and properties =====
    // =========================================
    // =========================================

    var obj = {};
    obj.addItemToCart = function( idProduct, name, price, count ) {
        for ( var i = 0; i < cart.length; i++ ) {
            if(cart[i].idProduct == idProduct) {
                cart[i].count += count;
                saveCart();
                return;
            }
        }
        var item = new Item( idProduct, name, price, count );
        cart.push(item);
        saveCart();
    };

    obj.setCountForItem = function( idProduct, count ) {
        for ( var i = 0; i < cart.length; i++ ) { 
            if( cart[i].idProduct == idProduct ) {
                cart[i].count = count;
                break;
            }
        }
        saveCart();
    };

    obj.removeItemFromCart = function( idProduct ) {
        for ( var i = 0; i < cart.length; i++ ) {
            if( cart[i].idProduct == idProduct ) {
                cart[i].count -= 1;
                if(cart[i].count == 0) {
                    cart.splice(i, 1);  
                }
                break;
            }
        }
        saveCart();
    };

    obj.removeAll = function(idProduct) {
        for ( var i = 0; i < cart.length; i++ ) {
            if( cart[i].idProduct == idProduct ) {
                cart.splice(i, 1);
                break;  
            }
        }
        saveCart();
    }; 
    
    obj.clearCart = function() {
        cart = [];
        saveCart();
    }; 
    
    obj.countCart = function(){
        var total_count = 0
        for ( var i = 0; i < cart.length; i++ ) {
            total_count += cart[i].count;
        }
        return total_count;
    }; 

    obj.totalCart = function() {
        total_cost = 0;
        costPerProduct = 0;
        for ( var i = 0; i < cart.length; i++ ) {
            if(cart[i].idProduct) {
                costPerProduct = cart[i].price * cart[i].count;
            }
            total_cost += costPerProduct;
        }
        return total_cost.toFixed(2);
    }; 

    obj.listCart = function() {
        var cartCopy = [];
        for( var i in cart ) {
            var item = cart[i];
            var itemCopy = {};
            for ( var x in item ) {
                itemCopy[x] = item[x];
            }
            itemCopy.total = (item.price * item.count).toFixed(2);
            cartCopy.push(itemCopy);
        }
        return cartCopy;
    }; 

    return obj;
})();














    
 

