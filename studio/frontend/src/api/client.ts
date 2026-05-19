import axios from "axios";

export const api = axios.create({
  baseURL: "http://localhost:8000",
  timeout: 30000,
});

export const WS_URL = "ws://localhost:8000/ws";
