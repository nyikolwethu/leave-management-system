import React, { createContext, useState, useEffect } from "react";
import UserPool from "../services/auth";

export const AuthContext = createContext();

const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const currentUser = UserPool.getCurrentUser();
    if (currentUser) {
      currentUser.getSession((err, session) => {
        if (!err && session.isValid()) {
          setUser(currentUser);
        }
      });
    }
  }, []);

  return (
    <AuthContext.Provider value={{ user, setUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;
