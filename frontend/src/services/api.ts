import axios from "axios";
import { toast } from "react-toastify";
const API_URL = "http://localhost:5000/api"; // Replace with your backend URL

// Create an Axios instance
const apiClient = axios.create({
  baseURL: API_URL,
  // You can add other configuration options here, like headers
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    // You can add custom logic before the request is sent
    // For example, add an authorization token to headers
    const token = localStorage.getItem("token");
    if (token) {
      console.log("token", token);
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    // Handle request error
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    // You can perform actions with the response data before returning it
    return response;
  },
  (error) => {
    console.error("error : ---->", error);
    const { response } = error;

    if (response?.status === 400) {
      const { errors } = response.data;

      for (const key in errors) {
        if (errors.hasOwnProperty(key)) {
          const element = errors[key];
          toast.error(element);
        }
      }
    } else if (response?.status === 500) {
      toast.error("Internal server error");
    } else if (response?.status === 401) {
      console.log("response", response);
      toast.error(
        response?.data?.message || response?.data?.error || "Unauthorized"
      );
    } else if (response?.status === 403) {
      toast.error("Forbidden");
    }

    // handle network error
    if (error.message && error.message.includes("Network Error")) {
      toast.error("Network error. Please check your internet connection.");
    }

    // Handle response error
    return Promise.reject(error);
  }
);

export interface Property {
  id: number;
  name: string;
  address: string;
  type: string;
  number_of_units: number;
  rental_cost: number;
  created_at: string;
  updated_at: string;
}

export interface Tenant {
  id: number;
  name: string;
  email: string;
  property_id: number;
  property?: Property;
  created_at: string;
  updated_at: string;
}

export interface Payment {
  id: number;
  tenant_id: number;
  tenant: Tenant;
  amount: number;
  date: string;
  settled: boolean;
  created_at: string;
  updated_at: string;
}

export const login = (email: string, password: string) =>
  apiClient.post<{
    token: string;
  }>("auth/login", { email, password });

export const getProperties = () => apiClient.get("/properties");
export const addProperty = (
  property: Omit<Property, "id" | "created_at" | "updated_at">
) => apiClient.post("/properties", property);
export const getTenants = () => apiClient.get("/tenants");
export const addTenant = (
  tenant: Omit<Tenant, "id" | "property" | "created_at" | "updated_at">
) => apiClient.post("/tenants", tenant);
export const getPayments = () => apiClient.get("/payments");
export const addPayment = (
  payment: Omit<Payment, "id" | "tenant" | "created_at" | "updated_at">
) => apiClient.post("/payments", payment);

export const deleteProperty = (id: number) =>
  apiClient.delete(`/properties/${id}`);
export const deleteTenant = (id: number) => apiClient.delete(`/tenants/${id}`);
export const deletePayment = (id: number) =>
  apiClient.delete(`/payments/${id}`);
export const setPaymentAsSettled = (payment: Payment) => {
  return apiClient.post(`/payments/${payment.id}`, {
    settled: true,
    amount: payment.amount,
    date: payment.date,
  });
};

export const updateProperty = (
  property: Omit<Property, "created_at" | "updated_at">
) => {
  const { id, ...rest } = property;
  return apiClient.post(`/properties/${property.id}`, {
    name: rest.name,
    address: rest.address,
    type: rest.type,
    number_of_units: rest.number_of_units,
    rental_cost: rest.rental_cost,
  });
};

export const updateTenant = (
  tenant: Omit<Tenant, "created_at" | "updated_at">
) => {
  const { id, ...rest } = tenant;
  return apiClient.post(`/tenants/${tenant.id}`, {
    name: rest.name,
    email: rest.email,
    property_id: rest.property_id,
  });
};

export const updatePayment = (
  payment: Omit<Payment, "created_at" | "updated_at">
) => {
  const { id, ...rest } = payment;
  return apiClient.post(`/payments/${payment.id}`, {
    tenant_id: rest.tenant_id,
    amount: rest.amount,
    date: rest.date,
    settled: rest.settled,
  });
};

export const fetcher = (url: string) =>
  apiClient.get(url).then((res) => res.data);
