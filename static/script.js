// Global Application State
let allExpenses = [];
let expenseToDeleteId = null;

// DOM Elements
const expenseForm = document.getElementById('expense-form');
const expenseIdInput = document.getElementById('expense-id');
const titleInput = document.getElementById('title');
const amountInput = document.getElementById('amount');
const categoryInput = document.getElementById('category');
const dateInput = document.getElementById('date');
const paymentMethodInput = document.getElementById('payment-method');
const notesInput = document.getElementById('notes');

const formHeading = document.getElementById('form-heading');
const submitBtnText = document.getElementById('submit-btn-text');
const cancelEditBtn = document.getElementById('cancel-edit-btn');

const searchInput = document.getElementById('search-input');
const filterCategorySelect = document.getElementById('filter-category');

const expenseListBody = document.getElementById('expense-list');
const emptyState = document.getElementById('empty-state');
const emptyStateText = document.getElementById('empty-state-text');

const totalSpentEl = document.getElementById('total-spent');
const totalCountEl = document.getElementById('total-count');
const avgExpenseEl = document.getElementById('avg-expense');

const deleteModal = document.getElementById('delete-modal');
const deleteItemTitleEl = document.getElementById('delete-item-title');
const confirmDeleteBtn = document.getElementById('confirm-delete-btn');
const toastContainer = document.getElementById('toast-container');

// Initialize Application
document.addEventListener('DOMContentLoaded', () => {
    // Set default date to today
    const today = new Date().toISOString().split('T')[0];
    dateInput.value = today;

    // Fetch initial expenses from API
    fetchExpenses();
});

// Toast Notification Helper
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    
    const iconClass = type === 'success' ? 'fa-circle-check' : 'fa-circle-exclamation';
    toast.innerHTML = `<i class="fa-solid ${iconClass}"></i> <span>${escapeHtml(message)}</span>`;
    
    toastContainer.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transition = 'opacity 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3500);
}

// Fetch All Expenses from Flask API
async function fetchExpenses() {
    try {
        const response = await fetch('/api/expenses');
        if (!response.ok) {
            throw new Error(`Failed to fetch expenses (${response.status})`);
        }
        allExpenses = await response.json();
        updateDashboard(allExpenses);
        handleSearchFilter();
    } catch (error) {
        console.error('Error fetching expenses:', error);
        showToast('Could not load expenses from server', 'error');
    }
}

// Recalculate and Render Dashboard Metrics
function updateDashboard(expenses) {
    const totalCount = expenses.length;
    const totalSpent = expenses.reduce((sum, exp) => sum + Number(exp.amount), 0);
    const avgExpense = totalCount > 0 ? totalSpent / totalCount : 0;

    totalSpentEl.textContent = `₹${totalSpent.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    totalCountEl.textContent = totalCount;
    avgExpenseEl.textContent = `₹${avgExpense.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
}

// Render Expenses into Table
function renderExpenses(expensesToDisplay) {
    expenseListBody.innerHTML = '';

    if (expensesToDisplay.length === 0) {
        emptyState.classList.remove('hidden');
        if (allExpenses.length === 0) {
            emptyStateText.textContent = "No expenses recorded yet. Add your first expense above!";
        } else {
            emptyStateText.textContent = "No expenses match your search or category filter.";
        }
        return;
    }

    emptyState.classList.add('hidden');

    expensesToDisplay.forEach(expense => {
        const tr = document.createElement('tr');
        
        const formattedAmount = `₹${Number(expense.amount).toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
        const formattedDate = formatDateDisplay(expense.date);
        const categoryBadge = getCategoryBadgeHTML(expense.category);

        tr.innerHTML = `
            <td><strong>${escapeHtml(expense.title)}</strong></td>
            <td class="amount-text">${formattedAmount}</td>
            <td>${categoryBadge}</td>
            <td>${formattedDate}</td>
            <td><i class="fa-solid fa-credit-card"></i> ${escapeHtml(expense.payment_method)}</td>
            <td>${expense.notes ? escapeHtml(expense.notes) : '<span style="color: var(--text-dark);">-</span>'}</td>
            <td class="text-center">
                <div class="actions-cell">
                    <button class="btn-action btn-edit" title="Edit Expense" onclick="startEditExpense(${expense.id})">
                        <i class="fa-solid fa-pen"></i>
                    </button>
                    <button class="btn-action btn-delete" title="Delete Expense" onclick="openDeleteModal(${expense.id}, '${escapeHtml(expense.title).replace(/'/g, "\\'")}')">
                        <i class="fa-solid fa-trash"></i>
                    </button>
                </div>
            </td>
        `;
        expenseListBody.appendChild(tr);
    });
}

// Category Badge Helper
function getCategoryBadgeHTML(category) {
    const catLower = category.toLowerCase();
    let badgeClass = `badge-${catLower}`;
    let iconClass = 'fa-tag';

    switch (category) {
        case 'Food': iconClass = 'fa-utensils'; break;
        case 'Travel': iconClass = 'fa-plane-departure'; break;
        case 'Education': iconClass = 'fa-graduation-cap'; break;
        case 'Shopping': iconClass = 'fa-bag-shopping'; break;
        case 'Bills': iconClass = 'fa-file-invoice-dollar'; break;
        case 'Entertainment': iconClass = 'fa-film'; break;
        case 'Health': iconClass = 'fa-heart-pulse'; break;
        default: iconClass = 'fa-layer-group'; break;
    }

    return `<span class="category-badge ${badgeClass}"><i class="fa-solid ${iconClass}"></i> ${escapeHtml(category)}</span>`;
}

// Client Side Form Validation
function validateForm() {
    let isValid = true;
    clearFieldErrors();

    const title = titleInput.value.trim();
    const amount = amountInput.value.trim();
    const category = categoryInput.value;
    const date = dateInput.value;
    const paymentMethod = paymentMethodInput.value;

    if (!title) {
        showFieldError('title', 'Title is required');
        isValid = false;
    }

    if (!amount) {
        showFieldError('amount', 'Amount is required');
        isValid = false;
    } else {
        const numAmount = parseFloat(amount);
        if (isNaN(numAmount) || numAmount <= 0) {
            showFieldError('amount', 'Amount must be a number greater than 0');
            isValid = false;
        }
    }

    if (!category) {
        showFieldError('category', 'Category is required');
        isValid = false;
    }

    if (!date) {
        showFieldError('date', 'Date is required');
        isValid = false;
    }

    if (!paymentMethod) {
        showFieldError('payment-method', 'Payment method is required');
        isValid = false;
    }

    return isValid;
}

function showFieldError(fieldId, message) {
    const field = document.getElementById(fieldId);
    const errorEl = document.getElementById(`${fieldId}-error`);
    if (field) field.classList.add('is-invalid');
    if (errorEl) errorEl.textContent = message;
}

function clearFieldErrors() {
    ['title', 'amount', 'category', 'date', 'payment-method'].forEach(fieldId => {
        const field = document.getElementById(fieldId);
        const errorEl = document.getElementById(`${fieldId}-error`);
        if (field) field.classList.remove('is-invalid');
        if (errorEl) errorEl.textContent = '';
    });
}

// Form Submit Handler (CREATE & UPDATE)
async function handleFormSubmit(event) {
    event.preventDefault();

    if (!validateForm()) return;

    const expenseId = expenseIdInput.value;
    const payload = {
        title: titleInput.value.trim(),
        amount: parseFloat(amountInput.value),
        category: categoryInput.value,
        date: dateInput.value,
        payment_method: paymentMethodInput.value,
        notes: notesInput.value.trim()
    };

    try {
        let url = '/api/expenses';
        let method = 'POST';

        if (expenseId) {
            url = `/api/expenses/${expenseId}`;
            method = 'PUT';
        }

        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const result = await response.json();

        if (!response.ok) {
            showToast(result.error || 'Operation failed', 'error');
            return;
        }

        showToast(expenseId ? 'Expense updated successfully!' : 'Expense added successfully!', 'success');
        resetForm();
        fetchExpenses();

    } catch (error) {
        console.error('Error saving expense:', error);
        showToast('Network error, failed to save expense.', 'error');
    }
}

// Populate Form for Editing (UPDATE)
function startEditExpense(id) {
    const expense = allExpenses.find(e => e.id === id);
    if (!expense) return;

    expenseIdInput.value = expense.id;
    titleInput.value = expense.title;
    amountInput.value = expense.amount;
    categoryInput.value = expense.category;
    dateInput.value = expense.date;
    paymentMethodInput.value = expense.payment_method;
    notesInput.value = expense.notes || '';

    formHeading.innerHTML = `<i class="fa-solid fa-pen-to-square"></i> Edit Expense`;
    submitBtnText.textContent = 'Update Expense';
    cancelEditBtn.classList.remove('hidden');

    clearFieldErrors();

    // Scroll smoothly to form
    document.querySelector('.form-card').scrollIntoView({ behavior: 'smooth' });
}

// Reset Form to Initial State
function resetForm() {
    expenseForm.reset();
    expenseIdInput.value = '';
    
    // Default to today date
    const today = new Date().toISOString().split('T')[0];
    dateInput.value = today;

    formHeading.innerHTML = `<i class="fa-solid fa-circle-plus"></i> Add Expense`;
    submitBtnText.textContent = 'Add Expense';
    cancelEditBtn.classList.add('hidden');

    clearFieldErrors();
}

// Delete Confirmation Modal Flow (DELETE)
function openDeleteModal(id, title) {
    expenseToDeleteId = id;
    deleteItemTitleEl.textContent = `"${title}"`;
    deleteModal.classList.remove('hidden');

    confirmDeleteBtn.onclick = () => confirmDeleteExpense(id);
}

function closeDeleteModal() {
    expenseToDeleteId = null;
    deleteModal.classList.add('hidden');
}

async function confirmDeleteExpense(id) {
    if (!id) return;

    try {
        const response = await fetch(`/api/expenses/${id}`, {
            method: 'DELETE'
        });

        const result = await response.json();

        if (!response.ok) {
            showToast(result.error || 'Failed to delete expense', 'error');
        } else {
            showToast('Expense deleted successfully', 'success');
            // If editing the item being deleted, reset form
            if (expenseIdInput.value == id) {
                resetForm();
            }
            fetchExpenses();
        }
    } catch (error) {
        console.error('Error deleting expense:', error);
        showToast('Network error, could not delete expense', 'error');
    } finally {
        closeDeleteModal();
    }
}

// Dynamic Search and Category Filter
function handleSearchFilter() {
    const query = searchInput.value.toLowerCase().trim();
    const selectedCategory = filterCategorySelect.value;

    const filtered = allExpenses.filter(exp => {
        const matchesTitle = exp.title.toLowerCase().includes(query);
        const matchesCategory = (selectedCategory === 'ALL') || (exp.category === selectedCategory);
        return matchesTitle && matchesCategory;
    });

    renderExpenses(filtered);
}

// Helper Utilities
function formatDateDisplay(dateStr) {
    if (!dateStr) return '';
    const parts = dateStr.split('-');
    if (parts.length !== 3) return dateStr;
    const dateObj = new Date(parts[0], parts[1] - 1, parts[2]);
    return dateObj.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}

function escapeHtml(str) {
    if (typeof str !== 'string') return str;
    return str.replace(/[&<>"']/g, function (match) {
        return {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#39;'
        }[match];
    });
}
