echo @"
const API_BASE = 'https://YOUR-API-ID.execute-api.us-east-1.amazonaws.com/prod';
let cognitoToken = null; // Replace with Cognito login flow

function showPage(pageId) {
  document.querySelectorAll('.page').forEach(p => p.style.display = 'none');
  document.getElementById(pageId).style.display = 'block';
}

function login() {
  // Placeholder for Cognito Hosted UI redirect
  alert('Login with Cognito Hosted UI here');
}

async function submitLeave(payload) {
  const res = await fetch(`${API_BASE}/leave`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${cognitoToken}`
    },
    body: JSON.stringify(payload)
  });
  return res.json();
}
"@ > app.js
