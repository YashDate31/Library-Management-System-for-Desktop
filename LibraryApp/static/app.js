const API_BASE = '/api';

// State
let currentUser = null;

// DOM Elements
const screens = {
    login: document.getElementById('login-screen'),
    dashboard: document.getElementById('dashboard-screen')
};

const loginBtn = document.getElementById('login-btn');
const enrollInput = document.getElementById('enrollment-input');
const passInput = document.getElementById('password-input');
const loginError = document.getElementById('login-error');
const logoutBtn = document.getElementById('logout-btn');

// Init
document.addEventListener('DOMContentLoaded', () => {
    checkSession();
    
    // Bind Tab Switching
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', (e) => switchTab(e.target.dataset.tab));
    });

    // Bind Search
    const searchInput = document.getElementById('catalog-search');
    let debounceTimer;
    searchInput.addEventListener('input', (e) => {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => loadCatalog(e.target.value), 500);
    });
});

// Navigation
function showScreen(screenName) {
    Object.values(screens).forEach(s => {
        s.classList.remove('active');
        s.style.display = 'none';
    });
    const s = screens[screenName];
    s.style.display = 'block';
    setTimeout(() => s.classList.add('active'), 10); // Trigger transition
}

function switchTab(tabId) {
    // Update buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.tab === tabId);
    });
    
    // Update content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(`tab-${tabId}`).classList.add('active');

    // Load data if needed
    if (tabId === 'catalog') loadCatalog();
    if (tabId === 'history') loadHistory();
}

// Authentication
function checkSession() {
    const stored = localStorage.getItem('library_user');
    if (stored) {
        currentUser = JSON.parse(stored);
        loadDashboard();
        showScreen('dashboard');
    } else {
        showScreen('login');
    }
}

loginBtn.addEventListener('click', async () => {
    const enrollment = enrollInput.value.trim();
    const password = passInput.value.trim();
    
    if (!enrollment) return showError('Please enter enrollment number');
    if (!password) return showError('Please enter password');
    
    loginBtn.innerHTML = '<i class="ri-loader-4-line"></i>';
    
    try {
        const res = await fetch(`${API_BASE}/login`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ 
                enrollment_no: enrollment,
                password: password
            })
        });
        const data = await res.json();
        
        if (data.success) {
            currentUser = data.student;
            localStorage.setItem('library_user', JSON.stringify(currentUser));
            loadDashboard();
            showScreen('dashboard');
        } else {
            showError(data.message);
        }
    } catch (e) {
        showError('Network error. Please try again.');
    } finally {
        loginBtn.innerHTML = '<span>Login</span><i class="ri-arrow-right-line"></i>';
    }
});

logoutBtn.addEventListener('click', () => {
    localStorage.removeItem('library_user');
    currentUser = null;
    enrollInput.value = '';
    showScreen('login');
});

function showError(msg) {
    loginError.textContent = msg;
    setTimeout(() => loginError.textContent = '', 3000);
}

// Data Loading
async function loadDashboard() {
    if (!currentUser) return;
    
    // Update Header
    document.getElementById('user-greeting').textContent = `Hi, ${currentUser.name.split(' ')[0]}`;
    document.getElementById('user-dept').textContent = currentUser.department || 'Student';
    
    try {
        const res = await fetch(`${API_BASE}/dashboard?enrollment_no=${currentUser.enrollment_no}`);
        const data = await res.json();
        
        // Update Stats
        document.getElementById('stat-borrowed').textContent = data.books_count;
        document.getElementById('stat-fine').textContent = `₹${data.total_fine}`;
        
        // Update List
        const listEl = document.getElementById('borrowed-list');
        listEl.innerHTML = '';
        
        if (data.borrowed_books.length === 0) {
            listEl.innerHTML = `
                <div class="empty-state">
                    <i class="ri-book-open-line"></i>
                    <p>No books borrowed currently</p>
                </div>
            `;
        } else {
            data.borrowed_books.forEach(book => {
                const statusClass = book.is_overdue ? 'overdue' : 'borrowed';
                const statusText = book.is_overdue ? `Overdue (₹${book.fine})` : `Due: ${book.due_date}`;
                
                listEl.innerHTML += `
                    <div class="book-card">
                        <div class="book-icon"><i class="ri-book-2-fill"></i></div>
                        <div class="book-info">
                            <h4 class="book-title">${book.title}</h4>
                            <p class="book-author">${book.author}</p>
                            <span class="tag ${statusClass}">${statusText}</span>
                        </div>
                    </div>
                `;
            });
        }
    } catch (e) {
        console.error(e);
    }
}

async function loadHistory() {
    const listEl = document.getElementById('history-list');
    listEl.innerHTML = '<div class="loading-spinner"><i class="ri-loader-4-line"></i></div>';
    
    try {
        const res = await fetch(`${API_BASE}/history?enrollment_no=${currentUser.enrollment_no}`);
        const history = await res.json();
        
        listEl.innerHTML = '';
        if (history.length === 0) {
            listEl.innerHTML = '<div class="empty-state">No history found</div>';
            return;
        }
        
        history.forEach(item => {
            const isReturn = item.status === 'returned';
            listEl.innerHTML += `
                <div class="history-item">
                    <span class="history-date">${item.borrow_date}</span>
                    <h4 class="history-title">${item.title}</h4>
                    <span class="tag ${isReturn ? 'returned' : 'borrowed'}">${item.status}</span>
                    ${isReturn ? `<span class="tag">Ret: ${item.return_date || 'N/A'}</span>` : ''}
                </div>
            `;
        });
    } catch (e) {
        listEl.innerHTML = '<p class="error-msg">Failed to load history</p>';
    }
}

async function loadCatalog(query = '') {
    const listEl = document.getElementById('catalog-list');
    listEl.innerHTML = '<div class="loading-spinner"><i class="ri-loader-4-line"></i></div>';
    
    try {
        const res = await fetch(`${API_BASE}/catalog?search=${encodeURIComponent(query)}`);
        const books = await res.json();
        
        listEl.innerHTML = '';
        if (books.length === 0) {
            listEl.innerHTML = '<div class="empty-state">No books found</div>';
            return;
        }
        
        books.forEach(book => {
            listEl.innerHTML += `
                <div class="book-card">
                    <div class="book-icon"><i class="ri-book-line"></i></div>
                    <div class="book-info">
                        <h4 class="book-title">${book.title}</h4>
                        <p class="book-author">${book.author}</p>
                        <span class="tag ${book.available ? 'avail' : 'out'}">
                            ${book.available ? 'Available' : 'Out of Stock'}
                        </span>
                    </div>
                </div>
            `;
        });
    } catch (e) {
        listEl.innerHTML = '<p class="error-msg">Failed to load catalog</p>';
    }
}
