import axios from "axios";

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api",
    // withCredentials cookie üçin, JWT-de zerur däl
});

// 👉 Her soragda Authorization başlyk goýmak
api.interceptors.request.use((config) => {
    const token = localStorage.getItem("access_token"); // token ady
    if (token) {
        config.headers = config.headers || {};
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export default api;

/* ---------------- USERS ---------------- */
export const getMe = () => api.get("/auth/me/");
export const getUsers = (params?: any) => api.get("/users/", { params });

/* ---------------- VEHICLES ---------------- */
export const getVehicles = (params?: any) => api.get("/vehicles/", { params });
export const createVehicle = (data: FormData) => api.post("/vehicles/", data);
export const updateVehicle = (id: number, data: FormData) =>
    api.put(`/vehicles/${id}/`, data);
export const deleteVehicleApi = (id: number) => api.delete(`/vehicles/${id}/`);

/* ---------------- CARGOS ---------------- */
export const getCargos = (params?: any) => api.get("/cargos/", { params });
export const createCargo = (data: any) => api.post("/cargos/", data);
export const updateCargo = (id: number, data: any) => api.put(`/cargos/${id}/`, data);
export const deleteCargo = (id: number) => api.delete(`/cargos/${id}/`);
/* ---------------- OFFERS ---------------- */
export const getOffers = (params?: any) => api.get("/offers/", { params });
export const createOffer = (data: any) => api.post("/offers/", data);
export const updateOffer = (id: number, data: any) => api.put(`/offers/${id}/`, data);
export const deleteOffer = (id: number) => api.delete(`/offers/${id}/`);

/* ---------------- SHIPMENTS ---------------- */
export const getShipments = (params?: any) => api.get("/shipments/", { params });
export const createShipment = (data: any) => api.post("/shipments/", data);
export const updateShipment = (id: number, data: any) => api.put(`/shipments/${id}/`, data);
export const deleteShipment = (id: number) => api.delete(`/shipments/${id}/`);

/* ---------------- REVIEWS ---------------- */
export const getReviews = (params?: any) => api.get("/reviews/", { params });
export const createReview = (data: any) => api.post("/reviews/", data);
export const updateReview = (id: number, data: any) => api.put(`/reviews/${id}/`, data);
export const deleteReview = (id: number) => api.delete(`/reviews/${id}/`);

/* ---------------- WALLET & TOPUPS ---------------- */
export const getWalletTransactions = (params?: any) =>
    api.get("/wallet/", { params });

export const getBalance = () => api.get("/topups/balance/");
export const createTopUp = (data: any) => api.post("/topups/", data);
