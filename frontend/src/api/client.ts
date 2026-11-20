import axios, { type AxiosInstance } from "axios";

// Ключ, под которым JWT access token хранится в localStorage.
const TOKEN_STORAGE_KEY = "access_token";

// Базовый URL берётся из переменной окружения Next.js.
// NEXT_PUBLIC_* доступна и на клиенте, и на сервере.
const baseURL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export const apiClient: AxiosInstance = axios.create({
  baseURL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Подставляем Bearer-токен в каждый запрос, если он есть.
// Проверка на window нужна, чтобы не падать при серверном рендере.
apiClient.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = window.localStorage.getItem(TOKEN_STORAGE_KEY);
    if (token) {
      config.headers = config.headers ?? {};
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

export { TOKEN_STORAGE_KEY };
export default apiClient;
