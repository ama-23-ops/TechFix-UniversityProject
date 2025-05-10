// Fetch all products and display them in the table
async function fetchProducts() {
    const response = await fetch('/api/products');
    const data = await response.json();
    const productTable = document.getElementById('productTable').getElementsByTagName('tbody')[0];
    productTable.innerHTML = ''; // Clear existing rows

    data.products.forEach(product => {
        const row = productTable.insertRow();
        row.innerHTML = `
            <td>${product.id}</td>
            <td>${product.name}</td>
            <td>${product.price}</td>
            <td>${product.category}</td>
            <td>
                <button onclick="editProduct(${product.id})">Edit</button>
                <button onclick="deleteProduct(${product.id})">Delete</button>
            </td>
        `;
    });
}

// Add a new product
document.getElementById('productForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const product = {
        name: formData.get('name'),
        price: parseFloat(formData.get('price')),
        category: formData.get('category')
    };

    const response = await fetch('/api/products', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(product)
    });

    if (response.ok) {
        fetchProducts(); // Refresh the product list
        e.target.reset(); // Clear the form
    }
});

// Fetch products when the page loads
window.onload = fetchProducts;

// Fetch quotes and display results
document.getElementById('quotationForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const productId = document.getElementById('product_id').value;

    const response = await fetch('/api/quotations', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_id: productId })
    });

    const result = await response.json();
    document.getElementById('quotationResult').textContent = JSON.stringify(result, null, 2);
});

// Fetch and display inventory
async function fetchInventory() {
    const response = await fetch('/api/inventory');
    const data = await response.json();
    const inventoryTable = document.getElementById('inventoryTable').getElementsByTagName('tbody')[0];
    inventoryTable.innerHTML = ''; // Clear existing rows

    data.inventory.forEach(item => {
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

// Fetch and display suppliers
async function fetchSuppliers() {
    const response = await fetch('/api/suppliers');
    const data = await response.json();
    const supplierTable = document.getElementById('supplierTable').getElementsByTagName('tbody')[0];
    supplierTable.innerHTML = ''; // Clear existing rows

    data.suppliers.forEach(supplier => {
        const row = supplierTable.insertRow();
        row.innerHTML = `
            <td>${supplier.id}</td>
            <td>${supplier.name}</td>
            <td>${supplier.contact_email}</td>
            <td>${supplier.phone_number}</td>
            <td>${supplier.address}</td>
            <td>${supplier.contact_person}</td>
            <td>
                <button onclick="editSupplier(${supplier.id})">Edit</button>
                <button onclick="deleteSupplier(${supplier.id})">Delete</button>
            </td>
        `;
    });
}

// Fetch and display orders
async function fetchOrders() {
    const response = await fetch('/api/orders');
    const data = await response.json();
    const orderTable = document.getElementById('orderTable').getElementsByTagName('tbody')[0];
    orderTable.innerHTML = ''; // Clear existing rows

    data.orders.forEach(order => {
        const row = orderTable.insertRow();
        row.innerHTML = `
            <td>${order.id}</td>
            <td>${order.supplier_id}</td>
            <td>${order.product_id}</td>
            <td>${order.quantity}</td>
            <td>${order.total_price}</td>
            <td>${order.order_status}</td>
            <td>
                <button onclick="editOrder(${order.id})">Edit</button>
                <button onclick="deleteOrder(${order.id})">Delete</button>
            </td>
        `;
    });
}

// Fetch data when the page loads
window.onload = () => {
    if (window.location.pathname === '/inventory') fetchInventory();
    if (window.location.pathname === '/suppliers') fetchSuppliers();
    if (window.location.pathname === '/orders') fetchOrders();
};