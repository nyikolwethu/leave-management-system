
import "./Button.css";

function Button({ text, type = "button", onClick }) {
  return (
    <button
      className="primary-button"
      type={type}
      onClick={onClick}
    >
      {text}
    </button>
  );
}

export default Button;