import Layout from "./layout";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { BrowserRouter as Router, Routes, Route, useLocation, Navigate } from "react-router-dom";
import Dashboard from "./pages/home";
import PaymentPage from "./pages/payment";
import TenantPage from "./pages/tenant";
import PropertyPage from "./pages/property";
import SignIn from "./pages/signin";
import { AuthProvider, useAuth } from "./context/auth.context";
import React, { ReactElement } from "react";
import NotFoundPage from "./pages/not-found";
interface ProtectedRouteProps {
  element: ReactElement;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ element }) => {
  const { isAuthenticated } = useAuth();
  const location = useLocation();

  if (!isAuthenticated) {
    console.log("ProtectedRoute -> isAuthenticated", isAuthenticated);
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return element;
};

const App = () => {
  return (

    <Layout>
      <ToastContainer
        position="top-right"
        autoClose={5000}
        hideProgressBar={false}
        newestOnTop
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="light"
        stacked
      />
      <Router>
        <AuthProvider>
          <Routes>
            {/* <Route path="/" element={<Dashboard />} />
          <Route path="/properties" element={<PropertyPage />} />
          <Route path="/tenants" element={<TenantPage />} />
          <Route path="/payments" element={<PaymentPage />} /> */}
            <Route path="/login" element={<SignIn />} />
            <Route
              path="/"
              element={
                <ProtectedRoute element={<Dashboard />} />
              }
            />
            <Route
              path="/properties"
              element={
                <ProtectedRoute element={<PropertyPage />} />
              }
            />
            <Route
              path="/tenants"
              element={
                <ProtectedRoute element={<TenantPage />} />
              }
            />
            <Route
              path="/payments"
              element={
                <ProtectedRoute element={<PaymentPage />} />
              }
            />
            <Route path="*" element={<NotFoundPage />} />
          </Routes>
        </AuthProvider>
      </Router>
    </Layout>
  );
};

export default App;
