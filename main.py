import threading
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pyModbusTCP.client import ModbusClient

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label  # Corregido aquí

# --- 1. CONFIGURACIÓN DE LA API FASTAPI ---
app_api = FastAPI()

app_api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PLC_IP = "186.73.22.69"
PLC_PORT = 502

@app_api.get("/api/bombas-status")
def get_bombas_status():
    client = ModbusClient(host=PLC_IP, port=PLC_PORT, timeout=2, auto_open=True, auto_close=True)
    try:
        arranque = client.read_coils(24, 3)  # %M24, %M25, %M26[cite: 1]
        manual = client.read_coils(105, 3)    # %M105, %M106, %M107[cite: 1]
        auto = client.read_coils(214, 3)      # %M214, %M215, %M216[cite: 1]
        
        if not arranque or not manual or not auto:
            return {"error": "No se pudo leer el PLC Schneider"}

        def obtener_modo(is_auto, is_manual):
            if is_auto: return "AUTOMÁTICO"
            if is_manual: return "MANUAL"
            return "DESACTIVADO"

        return {
            "bomba_1": {"arrancada": arranque[0], "modo": obtener_modo(auto[0], manual[0])},
            "bomba_2": {"arrancada": arranque[1], "modo": obtener_modo(auto[1], manual[1])},
            "bomba_3": {"arrancada": arranque[2], "modo": obtener_modo(auto[2], manual[2])}
        }
    except Exception as e:
        return {"error": str(e)}

# --- 2. CONTROL DEL SERVIDOR EN HILO SEPARADO ---
server_thread = None
server_instance = None
is_running = False

def run_server():
    global server_instance, is_running
    is_running = True
    config = uvicorn.Config(app_api, host="127.0.0.1", port=8000, log_level="info")
    server_instance = uvicorn.Server(config)
    # Ejecutamos el servidor de forma asíncrona controlada
    server_instance.run()

# --- 3. INTERFAZ GRÁFICA EN KIVY ---
class PLCControlApp(App):
    def build(self):
        self.title = "Control Servidor PLC"
        self.layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        
        # Etiqueta de estatus corregida (Label)
        self.status_label = Label(
            text="Servidor API: DETENIDO", 
            font_size=18, 
            halign="center", 
            valign="middle"
        )
        self.layout.add_widget(self.status_label)
        
        self.btn_toggle = Button(
            text="ENCENDER SERVIDOR API", 
            font_size=16, 
            background_color=(0.1, 0.6, 0.2, 1)
        )
        self.btn_toggle.bind(on_press=self.toggle_server)
        self.layout.add_widget(self.btn_toggle)
        
        return self.layout

    def toggle_server(self, instance):
        global server_thread, server_instance, is_running
        if not is_running:
            # Iniciar servidor en hilo secundario
            server_thread = threading.Thread(target=run_server, daemon=True)
            server_thread.start()
            self.status_label.text = "Servidor API: EJECUTÁNDOSE\n(http://127.0.0.1:8000)"
            self.btn_toggle.text = "APAGAR SERVIDOR API"
            self.btn_toggle.background_color = (0.8, 0.2, 0.2, 1)
        else:
            # Apagar el servidor uvicorn
            if server_instance:
                server_instance.should_exit = True
            is_running = False
            self.status_label.text = "Servidor API: DETENIDO"
            self.btn_toggle.text = "ENCENDER SERVIDOR API"
            self.btn_toggle.background_color = (0.1, 0.6, 0.2, 1)

if __name__ == '__main__':
    PLCControlApp().run()