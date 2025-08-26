import React, { createContext, useState, ReactNode } from "react";
import { Navigate, useLocation } from "react-router-dom";
import { getProperties } from "../services/api";
import Loading from "../components/spinner";

// Define the shape of the authentication context
interface AuthContextProps {
  isAuthenticated: boolean;
  setIsAuthenticated: React.Dispatch<React.SetStateAction<boolean>>;
  login: () => void;
  logout: () => void;
}

// Create the context with default values
const AuthContext = createContext<AuthContextProps>({
  isAuthenticated: false,
  setIsAuthenticated: () => { },
  login: () => { },
  logout: () => { },
});

// Create a provider component
export const AuthProvider: React.FC<{ children: ReactNode }> = ({
  children,
}) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const location = useLocation();


  React.useEffect(() => {
    (async () => {
      try {
        if (location.pathname === "/login") {
          return;
        }
        const property = await getProperties();
        console.log("property:", property);
        if (property) {
          setIsAuthenticated(true);
        }
      } catch {
        setIsAuthenticated(false);
      } finally {
        setIsLoading(false);
      }
    })()
  }, []);

  const login = () => {
    // Your login logic here
    setIsAuthenticated(true);
  };

  const logout = () => {
    // Your logout logic here
    setIsAuthenticated(false);
  };



  if (isLoading) {
    return <Loading />;
  }


  if (isAuthenticated && location.pathname === "/login") {
    return <Navigate to="/" state={{ from: location }} replace />;
  }

  //

  return <AuthContext.Provider
    value={{
      isAuthenticated,
      setIsAuthenticated,
      login,
      logout,
    }}
  >{children}</AuthContext.Provider>;
};

// Export the context for use in other components
export const useAuth = () => React.useContext(AuthContext);
