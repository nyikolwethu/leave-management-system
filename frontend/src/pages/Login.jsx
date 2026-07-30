import Button from "../components/Button/Button";

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

      <Button text="Sign In" type="submit" />
      </form>
    </div>
  );
}

export default Login;