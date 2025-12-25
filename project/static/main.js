/*
// Legacy client-side cart logic - Disabled to prevent conflict with Django backend
const addToCartButtons = document.querySelectorAll('.productBtn');
const cartCountElement = document.getElementById('cart-count');


let cart = JSON.parse(localStorage.getItem('CART')) || [];
// updateCartCount(); 


addToCartButtons.forEach(btn => {
    btn.addEventListener('click', addToCart);
});


function addToCart(event) {
    const btn = event.target;

    const productCard = btn.parentElement;


    const productName = productCard.querySelector('.productName').innerText;

const productPrice = productCard
  .querySelector('.productPrice')
  .innerText
  .replace('$', '')
  .replace(',', '');
    const productImg = productCard.querySelector('.productImg').src;

    const product = {
        name: productName,
        price: parseFloat(productPrice),
        image: productImg,
        quantity: 1
    };


    const existingProductIndex = cart.findIndex(item => item.name === product.name);

    if (existingProductIndex > -1) {
        cart[existingProductIndex].quantity += 1;
    } else {
        cart.push(product);
    }


    localStorage.setItem('CART', JSON.stringify(cart));
    updateCartCount();
    alert(`${productName} added to cart!`);
}


function updateCartCount() {
    if (cartCountElement) {
        const totalCount = cart.reduce((total, item) => total + item.quantity, 0);
        cartCountElement.innerText = totalCount;
    }
}



const cartTableBody = document.getElementById('cart-table-body');
const cartTotalElement = document.getElementById('cart-total');
const cartSubtotalElement = document.getElementById('cart-subtotal');
const emptyMsg = document.getElementById('empty-cart-msg');

if (cartTableBody) {
    displayCart();
}

function displayCart() {
    cartTableBody.innerHTML = '';
    let total = 0;

    if (cart.length === 0) {
        if(emptyMsg) emptyMsg.style.display = 'block';
    } else {
        if(emptyMsg) emptyMsg.style.display = 'none';

        cart.forEach((item, index) => {
            const itemTotal = item.price * item.quantity;
            total += itemTotal;

            const row = document.createElement('tr');
            row.innerHTML = `
                <td>
                    <div style="display:flex; align-items:center; gap:10px;">
                        <img src="${item.image}" style="width:60px; height:60px; object-fit:contain;">
                        <p style="margin:0; font-weight:600;">${item.name}</p>
                    </div>
                </td>
                <td>$${item.price}</td>
                <td>
                    <input type="number" value="${item.quantity}" min="1"
                           style="width:50px; text-align:center;"
                           onchange="updateQuantity(${index}, this.value)">
                </td>
                <td>$${itemTotal}</td>
                <td>
                    <button onclick="removeItem(${index})" style="color:red; border:none; background:none; cursor:pointer; font-weight:bold;">X</button>
                </td>
            `;
            cartTableBody.appendChild(row);
        });
    }

    if(cartSubtotalElement) cartSubtotalElement.innerText = `$${total}`;
    if(cartTotalElement) cartTotalElement.innerText = `$${total}`;
}

function updateQuantity(index, newQty) {
    if (newQty < 1) return;
    cart[index].quantity = parseInt(newQty);
    localStorage.setItem('CART', JSON.stringify(cart));
    displayCart();
    updateCartCount();
}

function removeItem(index) {
    cart.splice(index, 1);
    localStorage.setItem('CART', JSON.stringify(cart));
    displayCart();
    updateCartCount();
}
*/