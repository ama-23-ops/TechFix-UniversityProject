// static/js/techfix.js
document.addEventListener('DOMContentLoaded', function () {
    const path = window.location.pathname;

    if (path === '/techfix/products') {
        setupProductsPage();
    } else if (path === '/techfix/inventory') {
        setupInventoryPage();
    } else if (path === '/techfix/quotations') {
        setupQuotationsPage();
    } else if (path === '/techfix/orders') {
        setupOrdersPage();
    }
});

// --- Products (TechFix) ---
function setupProductsPage() {
    fetchProducts();
}

async function fetchProducts() {
    try {
        const response = await fetch('/techfix/products/api');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        populateProductTable(data.products);
    } catch (error) {
        console.error('Could not fetch products:', error);
        alert('Could not fetch products. Check console for details.');
    }
}

function populateProductTable(products) {
    const productTable = document.getElementById('productTable')?.querySelector('tbody');
    if (!productTable) return;

    productTable.innerHTML = ''; // Clear existing rows
    products.forEach(product => {
        const row = productTable.insertRow();
        row.innerHTML = `
            <td>${product.id}</td>
            <td>${product.name}</td>
            <td>${product.description}</td>
            <td>${product.price}</td>
            <td>${product.category}</td>
        `;
    });
}

// --- Inventory (TechFix) ---
function setupInventoryPage() {
    fetchInventory();
}

async function fetchInventory() {
    try {
        const response = await fetch('/techfix/inventory/api');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        populateInventoryTable(data.inventory);
    } catch (error) {
        console.error('Could not fetch inventory:', error);
        alert('Could not fetch inventory. Check console for details.');
    }
}

function populateInventoryTable(inventory) {
    const inventoryTable = document.getElementById('inventoryTable')?.querySelector('tbody');
    if (!inventoryTable) return;

    inventoryTable.innerHTML = ''; // Clear existing rows
    inventory.forEach(item => {
        const row = inventoryTable.insertRow();
        row.innerHTML = `
            <td>${item.id}</td>
            <td>${item.supplier_id}</td>
            <td>${item.product_id}</td>
            <td>${item.stock_quantity}</td>
            <td>${item.updated_at}</td>
        `;
    });
}

// --- Quotations (TechFix) ---
function setupQuotationsPage() {
    fetchProductsForQuotation();
    fetchQuotations();
}

// Fetch products when the page loads
document.addEventListener('DOMContentLoaded', function () {
    fetchProductsForQuotation();
});

async function fetchProductsForQuotation() {
    try {
        const response = await fetch('/techfix/quotations/api/products');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        console.log("Fetched products data:", data);  // Log the fetched data
        populateProductTableForQuotation(data.products);
    } catch (error) {
        console.error('Could not fetch products:', error);
        alert('Could not fetch products. Check console for details.');
    }
}

function populateProductTableForQuotation(products) {
    const productList = document.getElementById('product-list');
    if (!productList) {
        console.error('Product list container not found');
        return;
    }

    productList.innerHTML = ''; // Clear existing rows
    products.forEach(product => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${product.name}</td>
            <td>${product.description}</td>
            <td>${product.price}</td>
            <td><input type="number" id="quantity-${product.id}" min="1"></td>
        `;
        productList.appendChild(row);
    });
}

document.getElementById('request-quotation-btn').addEventListener('click', function () {
    const products = [];
    const rows = document.querySelectorAll('#product-list tr');
    rows.forEach(row => {
        const productId = row.querySelector('input').id.replace('quantity-', '');
        const quantity = parseFloat(row.querySelector('input').value);  // Convert to number
        if (quantity > 0) {
            products.push({
                product_id: productId,
                quantity: quantity
            });
        }
    });

    // Validate input
    if (products.length === 0) {
        alert("Please select at least one product and specify quantities.");
        return;
    }

    // Send quotation request to the backend
    fetch('/techfix/quotations/request', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            product_ids: products.map(p => p.product_id),
            quantities: products.map(p => p.quantity),
            supplier_id: 1  
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        alert(data.message || "Quotation request sent successfully");
        fetchQuotations();  // Refresh the quotations list
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to send quotation request. Check console for details.');
    });
});

async function fetchQuotations() {
    try {
        const response = await fetch('/techfix/quotations/api');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        populateQuotationTable(data.quotations);
    } catch (error) {
        console.error('Could not fetch quotations:', error);
        alert('Could not fetch quotations. Check console for details.');
    }
}

function populateQuotationTable(quotations) {
    const quotationTableBody = document.getElementById('quotationTable')?.querySelector('tbody');
    if (!quotationTableBody) return;

    quotationTableBody.innerHTML = ''; // Clear existing rows
    quotations.forEach(quotation => {
        const row = quotationTableBody.insertRow();
        row.innerHTML = `
            <td>${quotation.supplier_id}</td>
            <td>${quotation.id}</td>
            <td>${quotation.date_created}</td>
            <td>${quotation.status}</td>
            <td>
                <button onclick="requestQuotation(${quotation.id})">Request Quote</button>
            </td>
        `;
    });
}

// --- Orders (TechFix) ---
function setupOrdersPage() {
    fetchOrders();
}

async function fetchOrders(searchTerm = '') {
    try {
        let url = '/techfix/orders/api';
        if (searchTerm) {
            url += `?search_term=${searchTerm}`;
        }

        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        populateOrderTable(data.orders);
    } catch (error) {
        console.error('Could not fetch orders:', error);
        alert('Could not fetch orders. Check console for details.');
    }
}

function populateOrderTable(orders) {
    const orderTable = document.getElementById('orderTable')?.querySelector('tbody');
    if (!orderTable) return;

    orderTable.innerHTML = ''; // Clear existing rows
    orders.forEach(order => {
        const row = orderTable.insertRow();
        row.innerHTML = `
            <td>${order.id}</td>
            <td>${order.supplier_id}</td>
            <td>${order.date_created}</td>
            <td>${order.status}</td>
            <td>
                <button onclick="updateOrderQuantity(${order.id})">Update Quantity</button>
                <input type="number" id="quantity_${order.id}" value="1">
                <button onclick="confirmOrder(${order.id})">Confirm Order</button>
            </td>
        `;
    });
}

async function updateOrderQuantity(orderId) {
    const quantity = document.getElementById(`quantity_${orderId}`).value;

    try {
        const response = await fetch(`/techfix/orders/${orderId}/update_quantity`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ quantity: parseInt(quantity) })
        });

        if (!response.ok) {
            const errorText = await response.json();
            console.error('Failed to update order quantity:', errorText);
            alert('Failed to update order quantity: ' + (errorText.error || 'Unknown error'));
            return;
        }

        console.log('Order quantity updated successfully!');
        fetchOrders();
    } catch (error) {
        console.error('Failed to update order quantity:', error);
        alert('Failed to update order quantity. Check console for details.');
    }
}

async function confirmOrder(orderId) {
    try {
        const response = await fetch(`/techfix/orders/${orderId}/confirm`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });

        if (!response.ok) {
            const errorText = await response.json();
            console.error('Failed to confirm order:', errorText);
            alert('Failed to confirm order: ' + (errorText.error || 'Unknown error'));
            return;
        }

        console.log('Order confirmed successfully!');
        fetchOrders();
    } catch (error) {
        console.error('Failed to confirm order:', error);
        alert('Failed to confirm order. Check console for details.');
    }
}