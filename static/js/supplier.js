// static/js/supplier.js
document.addEventListener('DOMContentLoaded', function () {
    const path = window.location.pathname;

    if (path === '/supplier/products') {
        setupProductsPage();
    } else if (path === '/supplier/quotations') {
        setupQuotationsPage();
    } else if (path === '/supplier/inventory') {
        setupInventoryPage();
    } else if (path === '/supplier/orders') {
        setupOrdersPage();
    }
});

// --- Products (Supplier) ---
function setupProductsPage() {
    fetchProducts();

    const addProductForm = document.getElementById('addProductForm');
    if (addProductForm) {
        addProductForm.addEventListener('submit', handleAddProduct);
    }

    const editProductForm = document.getElementById('editProductForm');
    if (editProductForm) {
        editProductForm.addEventListener('submit', handleEditProduct);
    }
}

async function fetchProducts() {
    try {
        const response = await fetch('/supplier/products/api');
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
            <td>
                <button onclick="editProduct(${product.id}, '${product.name}', '${product.description}', ${product.price}, '${product.category}')">Edit</button>
                <button onclick="deleteProduct(${product.id})">Delete</button>
            </td>
        `;
    });
}

async function handleAddProduct(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const product = {
        name: formData.get('name'),
        description: formData.get('description'),
        price: parseFloat(formData.get('price')),
        category: formData.get('category')
    };

    try {
        const response = await fetch('/supplier/products/add', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(product)
        });

        if (!response.ok) {
            const errorText = await response.json();
            console.error('Failed to add product:', errorText);
            alert('Failed to add product: ' + (errorText.error || 'Unknown error'));
            return;
        }

        console.log('Product added successfully!');
        e.target.reset();
        fetchProducts();
    } catch (error) {
        console.error('Failed to add product:', error);
        alert('Failed to add product. Check console for details.');
    }
}

async function handleEditProduct(e) {
    e.preventDefault();
    const productId = document.getElementById('edit_product_id').value;
    const formData = new FormData(e.target);
    const product = {
        name: formData.get('name'),
        description: formData.get('description'),
        price: parseFloat(formData.get('price')),
        category: formData.get('category')
    };

    try {
        const response = await fetch(`/supplier/products/${productId}/update`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(product)
        });

        if (!response.ok) {
            const errorText = await response.json();
            console.error('Failed to update product:', errorText);
            alert('Failed to update product: ' + (errorText.error || 'Unknown error'));
            return;
        }

        console.log('Product updated successfully!');
        hideEditForm();
        e.target.reset();
        fetchProducts();
    } catch (error) {
        console.error('Failed to update product:', error);
        alert('Failed to update product. Check console for details.');
    }
}

function hideEditForm() {
    document.getElementById('editProductForm').style.display = 'none';
    document.getElementById('addProductForm').style.display = 'block';
}

// --- Inventory (Supplier) ---
function setupInventoryPage() {
    fetchInventory();

    const inventoryForm = document.getElementById('inventoryForm');
    if (inventoryForm) {
        inventoryForm.addEventListener('submit', handleAddInventoryItem);
    }
}

async function fetchInventory() {
    try {
        const response = await fetch('/supplier/inventory/api');
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
            <td>${item.product_id}</td>
            <td>${item.stock_quantity}</td>
            <td>${item.updated_at}</td>
        `;
    });
}

async function handleAddInventoryItem(e) {
    e.preventDefault();
    const formData = new FormData(e.target);
    const inventoryItem = {
        product_id: parseInt(formData.get('product_id')),
        stock_quantity: parseInt(formData.get('stock_quantity'))
    };

    try {
        const response = await fetch('/supplier/inventory/add', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(inventoryItem)
        });

        if (!response.ok) {
            const errorData = await response.json();
            console.error('Failed to add inventory item:', errorData);
            alert('Failed to add inventory: ' + (errorData.error || 'Unknown error'));
            return;
        }

        console.log('Inventory item added successfully!');
        fetchInventory();
        e.target.reset();
    } catch (error) {
        console.error('Failed to add inventory item:', error);
        alert('Failed to add inventory. Check console for details.');
    }
}

// --- Quotations (Supplier) ---
function setupQuotationsPage() {
    fetchQuotations();
}

async function fetchQuotations() {
    try {
        const response = await fetch('/supplier/quotations/api');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        populateQuotationTable(data);
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
            <td>${quotation.id}</td>
            <td>${quotation.techfix_id}</td>
            <td>${quotation.date_created}</td>
            <td>${quotation.status}</td>
            <td>
                <select class="status" data-quotation-id="${quotation.id}">
                    <option value="Pending" ${quotation.status === 'Pending' ? 'selected' : ''}>Pending</option>
                    <option value="Accepted" ${quotation.status === 'Accepted' ? 'selected' : ''}>Accepted</option>
                    <option value="Rejected" ${quotation.status === 'Rejected' ? 'selected' : ''}>Rejected</option>
                </select>
                <button onclick="updateQuotationStatus(${quotation.id})">Update</button>
            </td>
        `;
    });
}

async function updateQuotationStatus(quotationId) {
    const statusSelect = document.querySelector(`.status[data-quotation-id="${quotationId}"]`);
    const newStatus = statusSelect.value;

    try {
        const response = await fetch(`/supplier/quotations/${quotationId}/update_status`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: newStatus })
        });

        if (!response.ok) {
            const errorText = await response.json();
            console.error('Failed to update quotation status:', errorText);
            alert('Failed to update quotation status: ' + (errorText.error || 'Unknown error'));
            return;
        }

        console.log('Quotation status updated successfully!');
        fetchQuotations();
    } catch (error) {
        console.error('Failed to update quotation status:', error);
        alert('Failed to update quotation status. Check console for details.');
    }
}

// --- Orders (Supplier) ---
function setupOrdersPage() {
    fetchOrders();
}

async function fetchOrders() {
    try {
        const response = await fetch('/supplier/orders/api');
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
    const orderTableBody = document.getElementById('orderTable')?.querySelector('tbody');
    if (!orderTableBody) return;

    orderTableBody.innerHTML = ''; // Clear existing rows
    orders.forEach(order => {
        const row = orderTableBody.insertRow();
        row.innerHTML = `
            <td>${order.id}</td>
            <td>${order.techfix_id}</td>
            <td>${order.date_created}</td>
            <td>${order.status}</td>
            <td>
                <select class="status" data-order-id="${order.id}">
                    <option value="Pending" ${order.status === 'Pending' ? 'selected' : ''}>Pending</option>
                    <option value="Accepted" ${order.status === 'Accepted' ? 'selected' : ''}>Accepted</option>
                    <option value="Shipped" ${order.status === 'Shipped' ? 'selected' : ''}>Shipped</option>
                    <option value="Delivered" ${order.status === 'Delivered' ? 'selected' : ''}>Delivered</option>
                    <option value="Cancelled" ${order.status === 'Cancelled' ? 'selected' : ''}>Cancelled</option>
                </select>
                <button onclick="updateOrderStatus(${order.id})">Update</button>
            </td>
        `;
    });
}

async function updateOrderStatus(orderId) {
    const statusSelect = document.querySelector(`.status[data-order-id="${orderId}"]`);
    const newStatus = statusSelect.value;

    try {
        const response = await fetch(`/supplier/orders/${orderId}/update_status`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: newStatus })
        });

        if (!response.ok) {
            const errorText = await response.json();
            console.error('Failed to update order status:', errorText);
            alert('Failed to update order status: ' + (errorText.error || 'Unknown error'));
            return;
        }

        console.log('Order status updated successfully!');
        fetchOrders();
    } catch (error) {
        console.error('Failed to update order status:', error);
        alert('Failed to update order status. Check console for details.');
    }
}

// --- Delete Product (Supplier) ---
async function deleteProduct(productId) {
    try {
        const response = await fetch(`/supplier/products/${productId}/delete`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
        });

        if (response.ok) {
            console.log("Product deleted successfully!");
            fetchProducts(); // Refresh the product list
        } else {
            const errorText = await response.json();
            console.error('Error deleting product:', errorText);
            alert('Error deleting product: ' + (errorText.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error deleting product:', error);
        alert('Error deleting product. See console for details.');
    }
}

// --- Edit Product (Supplier) ---
async function editProduct(productId, name, description, price, category) {
    const editProductForm = document.getElementById('editProductForm');
    const addProductForm = document.getElementById('addProductForm');

    // Populate the edit form with existing data
    document.getElementById('edit_product_id').value = productId;
    document.getElementById('edit_product_name').value = name;
    document.getElementById('edit_product_description').value = description;
    document.getElementById('edit_product_price').value = price;
    document.getElementById('edit_product_category').value = category;

    // Show the edit form and hide the add form
    editProductForm.style.display = 'block';
    addProductForm.style.display = 'none';
}

// --- Cancel Edit (Supplier) ---
function cancelEdit() {
    const editProductForm = document.getElementById('editProductForm');
    const addProductForm = document.getElementById('addProductForm');

    // Hide the edit form and show the add form
    editProductForm.style.display = 'none';
    addProductForm.style.display = 'block';
}