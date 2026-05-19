import { app, BrowserWindow, Tray, Menu, nativeImage } from "electron";
import { spawn, ChildProcess } from "child_process";
import * as path from "path";
import * as os from "os";

let win: BrowserWindow | null = null;
let tray: Tray | null = null;
let backend: ChildProcess | null = null;

const isDev = process.env.NODE_ENV === "development";
const FRONTEND_URL = isDev ? "http://localhost:5173" : `file://${path.join(__dirname, "../frontend/dist/index.html")}`;
const BACKEND_PORT = 8000;

function startBackend() {
  const isWin = os.platform() === "win32";
  const python = isWin ? "wsl" : "python3";
  const args = isWin
    ? ["python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", String(BACKEND_PORT)]
    : ["-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", String(BACKEND_PORT)];

  backend = spawn(python, args, {
    cwd: isWin ? undefined : path.join(__dirname, "../backend"),
    env: { ...process.env },
  });

  backend.stdout?.on("data", (d) => console.log("[backend]", d.toString()));
  backend.stderr?.on("data", (d) => console.error("[backend]", d.toString()));
}

function createWindow() {
  win = new BrowserWindow({
    width: 1400,
    height: 900,
    minWidth: 1024,
    minHeight: 700,
    titleBarStyle: "hiddenInset",
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      contextIsolation: true,
    },
  });

  win.loadURL(FRONTEND_URL);
  if (isDev) win.webContents.openDevTools();
}

function createTray() {
  const icon = nativeImage.createEmpty();
  tray = new Tray(icon);
  tray.setContextMenu(
    Menu.buildFromTemplate([
      { label: "Aç", click: () => win?.show() },
      { label: "Çıkış", click: () => app.quit() },
    ])
  );
}

app.whenReady().then(() => {
  startBackend();
  setTimeout(createWindow, 2000); // backend başlamasını bekle
  createTray();
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});

app.on("quit", () => {
  backend?.kill();
});
