import { useState, useEffect } from "react";
import "./App.css";
import "@fortawesome/fontawesome-free/css/all.min.css";

// API base URL - Deployed backend with local fallback
const API_URL = "https://backend-authentication-otp.onrender.com/docs";

interface UserInfo {
  user_id: number;
  username: string;
  email: string;
  phone_number: string | null;
}

function App() {
  const [page, setPage] = useState<
    "login" | "otp-select" | "otp-verify" | "success"
  >("login");
  const [userInfo, setUserInfo] = useState<UserInfo | null>(null);
  const [otpCode, setOtpCode] = useState<string>("");
  const [selectedCountryCode, setSelectedCountryCode] = useState("+1");
  const [error, setError] = useState("");
  const [countryCodes, setCountryCodes] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  // Fetch country codes on component mount
  useEffect(() => {
    fetchCountries();
  }, []);

  const fetchCountries = async () => {
    try {
      const response = await fetch(`${API_URL}/countries`);
      const data = await response.json();
      setCountryCodes(data);
      if (data.length > 0) {
        setSelectedCountryCode(data[0].code);
      }
    } catch (err) {
      console.error("Failed to fetch countries:", err);
      // Fallback to basic list
      setCountryCodes([
        { code: "+1", name: "US/Canada" },
        { code: "+254", name: "Kenya" },
      ]);
    }
  };

  // Login form state
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [isRegistering, setIsRegistering] = useState(false);

  // Password visibility states
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  // Phone validation state
  const [phoneError, setPhoneError] = useState("");
  const [countrySearch, setCountrySearch] = useState("");

  // OTP selection state
  const [deliveryMethod, setDeliveryMethod] = useState<"email" | "sms">(
    "email",
  );

  // Phone validation function
  const validatePhoneNumber = (_countryCode: string, phoneNumber: string) => {
    // Basic validation - check if phone number has reasonable length
    if (phoneNumber.length < 7) {
      setPhoneError("Phone number too short");
      return false;
    }

    if (phoneNumber.length > 15) {
      setPhoneError("Phone number too long");
      return false;
    }

    setPhoneError("");
    return true;
  };

  // Filter countries based on search
  const filteredCountries = countryCodes.filter(
    (country: any) =>
      country.name.toLowerCase().includes(countrySearch.toLowerCase()) ||
      country.code.includes(countrySearch),
  );

  // Handle country selection with auto-populate
  const handleCountryChange = (countryCode: string) => {
    setSelectedCountryCode(countryCode);

    // Auto-populate phone field with country code
    if (phone) {
      // Extract the actual phone number (remove any existing country codes)
      let phoneNumber = phone;

      // Remove common country codes from the beginning
      const commonCodes = [
        "+",
        "1",
        "44",
        "254",
        "255",
        "256",
        "91",
        "86",
        "81",
        "49",
        "33",
        "27",
        "234",
      ];
      for (const code of commonCodes) {
        if (phoneNumber.startsWith(code)) {
          phoneNumber = phoneNumber.substring(code.length);
          break;
        }
      }

      // Set the new phone with selected country code
      setPhone(countryCode + phoneNumber);
    } else {
      // If phone is empty, just set the country code
      setPhone(countryCode);
    }

    // Clear any phone errors when changing country
    setPhoneError("");
  };

  // Handle registration
  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    if (password.length < 6) {
      setError("Password must be at least 6 characters");
      return;
    }

    if (username.length < 3) {
      setError("Username must be at least 3 characters");
      return;
    }

    try {
      const response = await fetch(`${API_URL}/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username,
          email,
          phone_number: phone, // Phone now includes country code
          password,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.detail || "Registration failed");
        return;
      }

      // Auto-login after registration
      setUserInfo({
        user_id: data.user_id,
        username,
        email,
        phone_number: phone,
      });
      setPage("otp-select");
    } catch (err) {
      setError("Failed to connect to server");
    }
  };

  // Handle login (first step)
  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    try {
      const response = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.detail || "Login failed");
        return;
      }

      setUserInfo(data);
      setPage("otp-select");
    } catch (err) {
      setError("Failed to connect to server");
    }
  };

  // Handle OTP generation
  const handleGenerateOTP = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (!userInfo) return;

    setIsLoading(true);

    // Show immediate feedback
    setError(
      `Sending OTP via ${deliveryMethod === "email" ? "Email" : "SMS"}...`,
    );

    try {
      const response = await fetch(`${API_URL}/generate-otp`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: userInfo.user_id,
          delivery_method: deliveryMethod,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.detail || "Failed to generate OTP");
        setIsLoading(false);
        return;
      }

      // Clear the sending message
      setError("");

      // Auto-navigate to OTP verification after 1 second
      setTimeout(() => {
        setOtpCode(data.otp_code);
        setPage("otp-verify");
        setIsLoading(false);
      }, 1000);
    } catch (err) {
      setError("Failed to connect to server");
      setIsLoading(false);
    }
  };

  // Handle OTP verification
  const handleVerifyOTP = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (!userInfo) return;

    setIsLoading(true);

    try {
      const response = await fetch(`${API_URL}/verify-otp`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: userInfo.user_id,
          otp_code: otpCode,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.detail || "Invalid OTP code");
        setIsLoading(false);
        return;
      }

      setPage("success");
      setIsLoading(false);
    } catch (err) {
      setError("Failed to connect to server");
      setIsLoading(false);
    }
  };

  // Go back to login
  const handleLogout = () => {
    setPage("login");
    setUserInfo(null);
    setOtpCode("");
    setUsername("");
    setEmail("");
    setPhone("");
    setPassword("");
    setConfirmPassword("");
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>OTP Authentication System</h1>
        {page === "success" && (
          <button onClick={handleLogout} className="logout-btn">
            Logout
          </button>
        )}
      </header>

      <main className="app-main">
        {page === "login" && (
          <div className="login-container">
            <div className="form-toggle">
              <button
                className={!isRegistering ? "active" : ""}
                onClick={() => setIsRegistering(false)}
              >
                Login
              </button>
              <button
                className={isRegistering ? "active" : ""}
                onClick={() => setIsRegistering(true)}
              >
                Register
              </button>
            </div>

            {isRegistering ? (
              <form onSubmit={handleRegister} className="auth-form">
                <h2>Create Account</h2>

                <div className="form-group">
                  <label htmlFor="username">Username</label>
                  <input
                    type="text"
                    id="username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                    minLength={3}
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="email">Email</label>
                  <input
                    type="email"
                    id="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="phone">Phone Number</label>
                  <div className="phone-input-group">
                    <div className="country-select-wrapper">
                      <input
                        type="text"
                        placeholder="Search country (e.g., United, +1, Kenya)..."
                        value={countrySearch}
                        onChange={(e) => setCountrySearch(e.target.value)}
                        className="country-search"
                      />
                      <select
                        value={selectedCountryCode}
                        onChange={(e) => handleCountryChange(e.target.value)}
                        className="country-select"
                      >
                        {filteredCountries.map((c: any) => (
                          <option key={c.code} value={c.code}>
                            {c.code} - {c.name}
                          </option>
                        ))}
                      </select>
                    </div>
                    <input
                      type="tel"
                      id="phone"
                      value={phone}
                      onChange={(e) => {
                        const newPhone = e.target.value;
                        setPhone(newPhone);

                        // Extract country code from the beginning for validation
                        const countryCode = selectedCountryCode;
                        const phoneNumber = newPhone.startsWith(countryCode)
                          ? newPhone.substring(countryCode.length)
                          : newPhone;

                        validatePhoneNumber(countryCode, phoneNumber);
                      }}
                      placeholder={`${selectedCountryCode}123456789`}
                      required
                      className={phoneError ? "phone-input-error" : ""}
                    />
                  </div>
                  {phoneError && (
                    <div className="phone-error">{phoneError}</div>
                  )}
                  <div className="phone-hint">
                    <small>
                      Format: {selectedCountryCode} followed by your phone
                      number
                    </small>
                  </div>
                </div>

                <div className="form-group">
                  <label htmlFor="password">Password</label>
                  <div className="password-input-wrapper">
                    <input
                      type={showPassword ? "text" : "password"}
                      id="password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      required
                      minLength={6}
                    />
                    <button
                      type="button"
                      className="password-toggle"
                      onClick={() => setShowPassword(!showPassword)}
                    >
                      <i
                        className={`fas ${showPassword ? "fa-eye-slash" : "fa-eye"}`}
                      ></i>
                    </button>
                  </div>
                </div>

                <div className="form-group">
                  <label htmlFor="confirmPassword">Confirm Password</label>
                  <div className="password-input-wrapper">
                    <input
                      type={showConfirmPassword ? "text" : "password"}
                      id="confirmPassword"
                      value={confirmPassword}
                      onChange={(e) => setConfirmPassword(e.target.value)}
                      required
                    />
                    <button
                      type="button"
                      className="password-toggle"
                      onClick={() =>
                        setShowConfirmPassword(!showConfirmPassword)
                      }
                    >
                      <i
                        className={`fas ${showConfirmPassword ? "fa-eye-slash" : "fa-eye"}`}
                      ></i>
                    </button>
                  </div>
                </div>

                {error && <div className="error-message">{error}</div>}

                <button type="submit" className="submit-btn">
                  Register
                </button>
              </form>
            ) : (
              <form onSubmit={handleLogin} className="auth-form">
                <h2>Welcome Back</h2>

                <div className="form-group">
                  <label htmlFor="email">Email</label>
                  <input
                    type="email"
                    id="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="password">Password</label>
                  <div className="password-input-wrapper">
                    <input
                      type={showPassword ? "text" : "password"}
                      id="password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      required
                    />
                    <button
                      type="button"
                      className="password-toggle"
                      onClick={() => setShowPassword(!showPassword)}
                    >
                      <i
                        className={`fas ${showPassword ? "fa-eye-slash" : "fa-eye"}`}
                      ></i>
                    </button>
                  </div>
                </div>

                {error && <div className="error-message">{error}</div>}

                <button type="submit" className="submit-btn">
                  Login
                </button>
              </form>
            )}
          </div>
        )}

        {page === "otp-select" && userInfo && (
          <div className="otp-select-container">
            <h2>Choose OTP Delivery Method</h2>
            <p className="user-welcome">Welcome, {userInfo.username}!</p>

            <div className="delivery-options">
              <button
                className={deliveryMethod === "email" ? "selected" : ""}
                onClick={() => setDeliveryMethod("email")}
              >
                <span className="method-icon">
                  <i className="fas fa-envelope"></i>
                </span>
                <span className="method-label">Email</span>
                <span className="method-detail">{userInfo.email}</span>
              </button>

              <button
                className={deliveryMethod === "sms" ? "selected" : ""}
                onClick={() => setDeliveryMethod("sms")}
              >
                <span className="method-icon">
                  <i className="fas fa-sms"></i>
                </span>
                <span className="method-label">SMS</span>
                <span className="method-detail">{userInfo.phone_number}</span>
              </button>
            </div>

            {error && <div className="error-message">{error}</div>}

            <button
              onClick={handleGenerateOTP}
              className="submit-btn"
              disabled={isLoading}
            >
              {isLoading ? (
                <>
                  <i className="fas fa-spinner fa-spin"></i> Sending...
                </>
              ) : (
                <>Send OTP via {deliveryMethod === "email" ? "Email" : "SMS"}</>
              )}
            </button>
          </div>
        )}

        {page === "otp-verify" && userInfo && (
          <div className="otp-verify-container">
            <h2>Enter OTP Code</h2>
            <p className="otp-instructions">
              Your OTP has been sent via {deliveryMethod}. For demo purposes,
              the code is displayed below.
            </p>

            <div className="otp-display">
              <span className="otp-code">{otpCode}</span>
            </div>

            <form onSubmit={handleVerifyOTP} className="otp-form">
              <div className="form-group">
                <label htmlFor="otp">Enter OTP Code</label>
                <input
                  type="text"
                  id="otp"
                  value={otpCode}
                  onChange={(e) => setOtpCode(e.target.value)}
                  required
                  maxLength={6}
                  placeholder="Enter 6-digit code"
                />
              </div>

              {error && <div className="error-message">{error}</div>}

              <button type="submit" className="submit-btn" disabled={isLoading}>
                {isLoading ? (
                  <>
                    <i className="fas fa-spinner fa-spin"></i> Verifying...
                  </>
                ) : (
                  "Verify & Login"
                )}
              </button>
            </form>

            <button className="back-btn" onClick={() => setPage("otp-select")}>
              Back
            </button>
          </div>
        )}

        {page === "success" && userInfo && (
          <div className="success-container">
            <div className="success-icon">
              <i className="fas fa-check"></i>
            </div>
            <h2>Login Successful!</h2>
            <p className="success-message">
              Thanks for logging in, {userInfo.username}!
            </p>
            <p className="success-wish">Have an amazing day!</p>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
