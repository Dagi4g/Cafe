
// Store all selected items with their quantities
let orderItems = [];

// ===========================================
// 1. SELECT BUTTON HANDLER
// ===========================================

document.addEventListener("DOMContentLoaded",function(){
    document.querySelectorAll('.select-btn').forEach(button => {
        button.addEventListener('click', function() {
            // Find the parent menu item
            const menuItem = this.closest('.menu-item');

            // Hide this select button
            this.classList.add('hidden');

            // Show the quantity panel for this item
            const quantityPanel = menuItem.querySelector('.quantity-panel');
            quantityPanel.classList.remove('hidden');

            // Reset quantity to 1
            const quantitySpan = quantityPanel.querySelector('.quantity');
            quantitySpan.textContent = '1';

            // Update item total
            updateItemTotal(menuItem);

            // Add to order items (or update if already exists)
            addToOrder(menuItem);
        });
    });


    // ===========================================
    // 2. QUANTITY BUTTON HANDLERS
    // ===========================================
    document.querySelectorAll('.qty-btn').forEach(button => {
        button.addEventListener('click', function() {
            // Find the quantity panel and menu item
            const quantityPanel = this.closest('.quantity-panel');
            const menuItem = quantityPanel.closest('.menu-item');
            const quantitySpan = quantityPanel.querySelector('.quantity');

            // Get current quantity
            let quantity = parseInt(quantitySpan.textContent);

            // Increase or decrease
            if (this.dataset.action === 'increase') {
                quantity += 1;
            } else if (this.dataset.action === 'decrease' && quantity > 1) {
                quantity -= 1;
            }

            // Update display
            quantitySpan.textContent = quantity;

            // Update the item total
            updateItemTotal(menuItem);

            // Update in orderItems array
            updateOrderItem(menuItem);
        });
    });

    // ===========================================
    // 4. ORDER BUTTON HANDLER
    // ===========================================
    // Get DOM elements
    const totalDisplay = document.getElementById('totalDisplay');
    const orderBtn = document.getElementById('orderBtn');


    orderBtn.addEventListener('click', function() {
        if (orderItems.length === 0) {
            alert('Please select items to order');
            return;
        }

        // Show what's being ordered
        console.log('Order items:', orderItems);

        // Calculate total again just to be sure
        const total = orderItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);
        console.log('Total:', total);

        // Here you'll send to Django
        // fetch('/api/create-order/', {
        //     method: 'POST',
        //     headers: {'Content-Type': 'application/json'},
        //     body: JSON.stringify({items: orderItems, total: total})
        // });

        alert('Order placed! Total: ' + total + ' Birr');
    });


});

// ===========================================
// 3. HELPER FUNCTIONS
// ===========================================

// Update the per-item total display
function updateItemTotal(menuItem) {
    const price = parseFloat(menuItem.dataset.price);
    const quantity = parseInt(menuItem.querySelector('.quantity').textContent);
    const itemTotal = price * quantity;

    const itemTotalSpan = menuItem.querySelector('.item-total');
    itemTotalSpan.textContent = itemTotal + ' Birr';
}

// Add item to order array
function addToOrder(menuItem) {
    const id = menuItem.dataset.id;
    const price = parseFloat(menuItem.dataset.price);
    const name = menuItem.querySelector('.food-name').textContent;
    const quantity = parseInt(menuItem.querySelector('.quantity').textContent);

    // Check if already in order
    const existingIndex = orderItems.findIndex(item => item.id === id);

    if (existingIndex === -1) {
        // Add new
        orderItems.push({
            id: id,
            name: name,
            price: price,
            quantity: quantity
        });
    } else {
        // Update existing
        orderItems[existingIndex].quantity = quantity;
    }

    updateGrandTotal();
}

// Update item in order array (when quantity changes)
function updateOrderItem(menuItem) {
    const id = menuItem.dataset.id;
    const quantity = parseInt(menuItem.querySelector('.quantity').textContent);

    const existingItem = orderItems.find(item => item.id === id);
    if (existingItem) {
        existingItem.quantity = quantity;
    }

    updateGrandTotal();
}

// Calculate and display grand total
function updateGrandTotal() {
    const total = orderItems.reduce((sum, item) => {
        return sum + (item.price * item.quantity);
    }, 0);

    totalDisplay.textContent = total + ' Birr';
}


