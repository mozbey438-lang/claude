import { contextBridge, ipcRenderer } from "electron";

contextBridge.exposeInMainWorld("studio", {
  platform: process.platform,
  onBackendReady: (cb: () => void) => ipcRenderer.on("backend-ready", cb),
});
