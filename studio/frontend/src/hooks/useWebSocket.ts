import { useEffect, useRef, useCallback } from "react";
import { WS_URL } from "../api/client";

type Handler = (event: { type: string; data: unknown }) => void;

export function useWebSocket(onMessage: Handler) {
  const ws = useRef<WebSocket | null>(null);

  const connect = useCallback(() => {
    ws.current = new WebSocket(WS_URL);
    ws.current.onmessage = (e) => {
      try {
        onMessage(JSON.parse(e.data));
      } catch {}
    };
    ws.current.onclose = () => setTimeout(connect, 2000);
  }, [onMessage]);

  useEffect(() => {
    connect();
    return () => ws.current?.close();
  }, [connect]);
}
