#####################################
import subprocess, os, requests     #
import tkinter as tk                #
from tkinter import messagebox      #
from bs4 import BeautifulSoup       #
from urllib.parse import urljoin    #
######################################

### [PGX] - NINGUN SITEMA ES SEGURO ###
ovpn = []

def descargar_clave():
 url = 'https://www.vpnbook.com/freevpn'
 r = requests.get(url)
 soup = BeautifulSoup(r.content, 'html.parser')
 imagenes = soup.find_all('img')
 imagenes_filtradas = [img for img in imagenes if img.get('src', '').startswith('password.php?t')]
 for img in imagenes_filtradas:
  url_imagen = urljoin(url, img['src'])
  print(f"Descargando desde: {url_imagen}")
  d = requests.get(url_imagen)
  contenido = d.content
  with open('vpn/clave.png', 'wb') as f:
     f.write(contenido)
 if os.path.exists('vpn/clave.png'):
  c='start vpn/clave.png'
  subprocess.run(c, shell=True)
 else:
    print("ERROR AL DESCARGAR")

def actualizar_vpn_actual():
 vpn_actual.set(f"Conectado a: {ovpn[0] if ovpn else 'Ninguna VPN'}")

def conectarme():
 command = 'taskkill /f /im openvpn.exe'
 subprocess.run(command, shell=True)
 if not ovpn:
  messagebox.showwarning("Advertencia", "No hay archivos .ovpn disponibles.")
  return
 global proceso
 vpn_conectar = ovpn[0]
 command = f'vpn\\OpenVPN\\bin\\openvpn.exe vpn\\OpenVPN\\bin\\{vpn_conectar}'
 proceso = subprocess.Popen(command, shell=True)
 actualizar_vpn_actual()

def conectarme_a_otro():
 if len(ovpn) > 1:
  command = 'taskkill /f /im openvpn.exe'
  subprocess.run(command, shell=True)
  ovpn.pop(0)
  conectarme()
 else:
  messagebox.showinfo("Info", "No hay más VPN disponibles para conectarse.")

def listar_archivos_vpn():
 global ovpn
 listar = os.listdir('vpn\\OpenVPN\\bin')
 for i in listar:
  if i.endswith('.ovpn'):
   ovpn.append(i)

def mostrar_modpass():
 input_frame.pack(pady=(10, 20))

def guardar_clave():
 nueva_clave = entry_clave.get()
 if nueva_clave:
  with open('vpn/OpenVPN/bin/uspass.txt', 'w') as f:
   f.write(f'vpnbook\n{nueva_clave}')
  messagebox.showinfo("Éxito", "La clave ha sido actualizada.")
  entry_clave.delete(0, tk.END)
 else:
  messagebox.showwarning("Advertencia", "Por favor, introduce una nueva clave.")

def detener():
 c1='taskkill /f /im openvpn.exe'
 c1='taskkill /f /im python.exe'
 subprocess.run(c1, shell=True)
 subprocess.run(c2, shell=True)
root = tk.Tk()
root.title("CONECTARME A VPN")
ancho_ventana = root.winfo_screenwidth()
alto_ventana = root.winfo_screenheight()
root.geometry(f"{ancho_ventana}x{alto_ventana}")
root.configure(bg="black")
vpn_actual = tk.StringVar()
vpn_actual.set("Conectado a: Ninguna VPN")
listar_archivos_vpn()
input_frame = tk.Frame(root, bg="black")
label_clave = tk.Label(input_frame, text="Nueva clave:", bg="black", fg="white")
label_clave.pack(side=tk.LEFT, padx=5)
entry_clave = tk.Entry(input_frame)
entry_clave.pack(side=tk.LEFT)
button_guardar = tk.Button(input_frame, text="Guardar", command=guardar_clave)
button_guardar.pack(side=tk.LEFT)
button_ancho = 30
button_conectar = tk.Button(root, text="CONECTARME A VPN", width=button_ancho, command=conectarme)
button_conectar.pack(pady=(50, 20))
button_otro = tk.Button(root, text="Conectarme a otro VPN", width=button_ancho, command=conectarme_a_otro)
button_otro.pack(pady=(10, 20))
button_modificar = tk.Button(root, text="Modificar clave de VPNBOOK", width=button_ancho, command=mostrar_modpass)
button_modificar.pack(pady=(10, 20))
button_otro = tk.Button(root, text="Descargar clave de VPNBOOK", width=button_ancho, command=descargar_clave)
button_otro.pack(pady=(10, 20))
vpnkill = tk.Button(root, text="FINALIZAR VPN", width=button_ancho, command=detener)
vpnkill.pack(pady=(10, 20))
label_vpn_actual = tk.Label(root, textvariable=vpn_actual, bg="black", fg="white")
label_vpn_actual.pack(pady=(10, 20))
root.mainloop()