function Login() {
  return (
    <div>
      <h1>Leave Management System</h1>

      <h2>Login</h2>

      <form>
        <div>
          <label>Email</label>
          <br />
          <input type="email" placeholder="Enter your email" />
        </div>

        <br />

        <div>
          <label>Password</label>
          <br />
          <input type="password" placeholder="Enter your password" />
        </div>

        <br />

        <button type="submit">Sign In</button>
      </form>
    </div>
  );
}

export default Login;