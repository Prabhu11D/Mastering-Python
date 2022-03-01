const updateBtns = document.getElementsByClassName('update-cart');
console.log(updateBtns.length);

for (let i = 0; i < updateBtns.length; i++) {
  updateBtns[i].addEventListener('click', function () {
    let productId = this.dataset.product;
    let action = this.dataset.action;

    console.log("Product ID", productId, "Action", action);

    console.log("USER", user);
    if (user == "AnonymousUser") addCookieItem(productId, action);
    else updateUserOrder(productId, action);
  })
}

function updateUserOrder(productId, action) {
  console.log("User is logged in, sending data...");

  let url = '/update_item/';

  fetch(url, {
    method: "POST",
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken
    },
    body: JSON.stringify({ 'productId': productId, 'action': action })
  }).then(response => {
    return response.json();
  }).then(data => {
    console.log('Data', data);
    location.reload();
  }).catch(err => {
    console.log("Error", err);
  })
}

function addCookieItem(productId, action) {
  console.log('User is not authenticated')

  if (action == 'add') {
    if (cart[productId] == undefined) {
      cart[productId] = { 'quantity': 1 }

    } else {
      cart[productId]['quantity'] += 1
    }
  }

  if (action == 'remove') {
    cart[productId]['quantity'] -= 1

    if (cart[productId]['quantity'] <= 0) {
      console.log('Item should be deleted')
      delete cart[productId];
    }
  }
  console.log('CART:', cart)
  document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"

  location.reload()
}