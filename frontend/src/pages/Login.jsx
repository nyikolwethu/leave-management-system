import "./Login.css";
import Button from "../components/Button/Button";

function Login() {
  return (
    <div className="login-page">
      <div className="login-card">
        <h1>🌸 Leave Management System</h1>

        <p className="subtitle">
          Welcome Back
        </p>

        <form>
          <label>Email</label>

          <input
            type="email"
            placeholder="Enter your email"
          />

          <label>Password</label>

          <input
            type="password"
            placeholder="Enter your password"
          />

          <Button
            text="Sign In"
            type="submit"
          />
        </form>
      </div>
    </div>
  );
}

export default Login;