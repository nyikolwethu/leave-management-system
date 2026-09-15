// Thin wrapper around Cognito's IDP JSON API (no SDK dependency) and
// the API Gateway endpoints for the leave management backend.

const Auth = {
  TOKEN_KEY: 'lm_id_token',
  GROUPS_KEY: 'lm_groups',
  SUB_KEY: 'lm_sub',

  async login(email, password) {
    const idpUrl = `https://cognito-idp.${window.APP_CONFIG.COGNITO_REGION}.amazonaws.com/`;
    const res = await fetch(idpUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-amz-json-1.1',
        'X-Amz-Target': 'AWSCognitoIdentityProviderService.InitiateAuth'
      },
      body: JSON.stringify({
        AuthFlow: 'USER_PASSWORD_AUTH',
        ClientId: window.APP_CONFIG.COGNITO_CLIENT_ID,
        AuthParameters: { USERNAME: email, PASSWORD: password }
      })
    });

    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.message || 'Login failed');
    }

    const idToken = data.AuthenticationResult.IdToken;
    const payload = JSON.parse(atob(idToken.split('.')[1]));

    localStorage.setItem(this.TOKEN_KEY, idToken);
    localStorage.setItem(this.GROUPS_KEY, JSON.stringify(payload['cognito:groups'] || []));
    localStorage.setItem(this.SUB_KEY, payload.sub);

    return { name: payload.email || email, groups: payload['cognito:groups'] || [], sub: payload.sub };
  },

  logout() {
    localStorage.removeItem(this.TOKEN_KEY);
    localStorage.removeItem(this.GROUPS_KEY);
    localStorage.removeItem(this.SUB_KEY);
  },

  getToken() {
    return localStorage.getItem(this.TOKEN_KEY);
  },

  getGroups() {
    return JSON.parse(localStorage.getItem(this.GROUPS_KEY) || '[]');
  },

  getSub() {
    return localStorage.getItem(this.SUB_KEY);
  },

  isLoggedIn() {
    return !!this.getToken();
  }
};

const Api = {
  async request(path, options = {}) {
    const res = await fetch(`${window.APP_CONFIG.API_BASE}${path}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${Auth.getToken()}`,
        ...(options.headers || {})
      }
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      throw new Error(data.error || `Request failed (${res.status})`);
    }
    return data;
  },

  getBalance(employeeId) {
    return this.request(`/employee/${employeeId}/balance`);
  },

  getHistory(employeeId) {
    return this.request(`/employee/${employeeId}/history`);
  },

  getPending(managerId) {
    return this.request(`/manager/${managerId}/pending`);
  },

  submitLeave(payload) {
    return this.request('/leave', { method: 'POST', body: JSON.stringify(payload) });
  },

  decideLeave(requestId, employeeId, status) {
    return this.request(`/leave/${requestId}`, {
      method: 'PUT',
      body: JSON.stringify({ employeeId, status })
    });
  }
};
