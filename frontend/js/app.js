const state = {
  employeeId: null,
  isManager: false
};

function $(id) { return document.getElementById(id); }

function showView(viewId) {
  document.querySelectorAll('.view').forEach(v => v.classList.add('hidden'));
  $(viewId).classList.remove('hidden');
}

function showTab(tabName) {
  document.querySelectorAll('.tab-panel').forEach(p => p.classList.add('hidden'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  $(tabName).classList.remove('hidden');
  document.querySelector(`.tab-btn[data-tab="${tabName}"]`).classList.add('active');

  if (tabName === 'dashboard') loadDashboard();
  if (tabName === 'history') loadHistory();
  if (tabName === 'inbox') loadInbox();
}

async function loadDashboard() {
  try {
    const data = await Api.getBalance(state.employeeId);
    const balances = data.leaveBalance || {};
    $('balanceCards').innerHTML = Object.entries(balances).map(([type, amount]) => `
      <div class="balance-card">
        <div class="num">${amount}</div>
        <div class="label">${type}</div>
      </div>
    `).join('') || '<p class="muted">No balance data available.</p>';
  } catch (e) {
    $('balanceCards').innerHTML = `<p class="error">${e.message}</p>`;
  }
}

async function loadHistory() {
  const tbody = $('historyBody');
  tbody.innerHTML = '<tr><td colspan="6">Loading...</td></tr>';
  try {
    const data = await Api.getHistory(state.employeeId);
    const rows = data.requests || [];
    tbody.innerHTML = rows.length ? rows.map(r => `
      <tr>
        <td>${r.leaveType}</td>
        <td>${r.startDate}</td>
        <td>${r.endDate}</td>
        <td>${r.numDays ?? '-'}</td>
        <td class="status-${(r.status || '').toLowerCase()}">${r.status}</td>
        <td>${new Date(r.submittedAt).toLocaleString()}</td>
      </tr>
    `).join('') : '<tr><td colspan="6" class="muted">No requests yet.</td></tr>';
  } catch (e) {
    tbody.innerHTML = `<tr><td colspan="6" class="error">${e.message}</td></tr>`;
  }
}

async function loadInbox() {
  const tbody = $('inboxBody');
  tbody.innerHTML = '<tr><td colspan="7">Loading...</td></tr>';
  try {
    const data = await Api.getPending(state.employeeId);
    const rows = data.pendingRequests || [];
    tbody.innerHTML = rows.length ? rows.map(r => `
      <tr data-request-id="${r.requestId}" data-employee-id="${r.employeeId}">
        <td>${r.employeeId}</td>
        <td>${r.leaveType}</td>
        <td>${r.startDate}</td>
        <td>${r.endDate}</td>
        <td>${r.numDays ?? '-'}</td>
        <td>${r.reason || ''}</td>
        <td>
          <button class="action-btn approve-btn" data-action="APPROVED">Approve</button>
          <button class="action-btn reject-btn" data-action="REJECTED">Reject</button>
        </td>
      </tr>
    `).join('') : '<tr><td colspan="7" class="muted">No pending requests.</td></tr>';

    tbody.querySelectorAll('button[data-action]').forEach(btn => {
      btn.addEventListener('click', async (e) => {
        const row = e.target.closest('tr');
        const requestId = row.dataset.requestId;
        const employeeId = row.dataset.employeeId;
        try {
          await Api.decideLeave(requestId, employeeId, e.target.dataset.action);
          loadInbox();
        } catch (err) {
          alert(err.message);
        }
      });
    });
  } catch (e) {
    tbody.innerHTML = `<tr><td colspan="7" class="error">${e.message}</td></tr>`;
  }
}

function initApp(user) {
  state.employeeId = user.sub;
  state.isManager = (user.groups || []).includes('Managers');

  $('userInfo').classList.remove('hidden');
  $('userName').textContent = user.name;
  if (state.isManager) {
    document.querySelector('.manager-only').classList.remove('hidden');
  }

  showView('appView');
  showTab('dashboard');
}

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => showTab(btn.dataset.tab));
  });

  $('loginBtn').addEventListener('click', async () => {
    const email = $('loginEmail').value.trim();
    const password = $('loginPassword').value;
    $('loginError').classList.add('hidden');
    try {
      const user = await Auth.login(email, password);
      initApp(user);
    } catch (e) {
      $('loginError').textContent = e.message;
      $('loginError').classList.remove('hidden');
    }
  });

  $('logoutBtn').addEventListener('click', () => {
    Auth.logout();
    showView('loginView');
  });

  $('submitLeaveBtn').addEventListener('click', async () => {
    const msg = $('submitMessage');
    msg.classList.add('hidden');
    try {
      const result = await Api.submitLeave({
        employeeId: state.employeeId,
        leaveType: $('leaveType').value,
        startDate: $('startDate').value,
        endDate: $('endDate').value,
        reason: $('reason').value
      });
      msg.className = 'success-msg';
      msg.textContent = `Request submitted (ID: ${result.requestId}), status: ${result.status}`;
      msg.classList.remove('hidden');
    } catch (e) {
      msg.className = 'error';
      msg.textContent = e.message;
      msg.classList.remove('hidden');
    }
  });

  // Restore session if a token is already stored
  if (Auth.isLoggedIn()) {
    const groups = Auth.getGroups();
    initApp({ name: 'You', groups, sub: Auth.getSub() });
  } else {
    showView('loginView');
  }
});
