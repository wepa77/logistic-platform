// src/api/auth.ts
import api from "./api";

export async function login(username: string, password: string) {
    const { data } = await api.post("/auth/token/", { username, password });
    localStorage.setItem("access_token", data.access);
    localStorage.setItem("refresh_token", data.refresh);
    return data;
}
