import tkinter as tk
import pandas as pd
from tkinter import filedialog
from datetime import datetime

ventana = tk.Tk()
ventana.title("Seguimiento de Gastos")

# Establecer tamaño de la ventana
ventana.geometry("500x500")

frame_entrada = tk.Frame(ventana, pady=10)
frame_entrada.pack()

mes_etiqueta = tk.Label(frame_entrada, text="Mes:")
mes_etiqueta.grid(row=0, column=0, padx=10)
mes_entrada = tk.Entry(frame_entrada)
mes_entrada.grid(row=0, column=1)

sueldo_etiqueta = tk.Label(frame_entrada, text="Sueldo:")
sueldo_etiqueta.grid(row=1, column=0, padx=10)
sueldo_entrada = tk.Entry(frame_entrada)
sueldo_entrada.grid(row=1, column=1)

gasto_etiqueta = tk.Label(frame_entrada, text="Cuenta a Pagar:")
gasto_etiqueta.grid(row=2, column=0, padx=10)
entrada_gasto = tk.Entry(frame_entrada)
entrada_gasto.grid(row=2, column=1)

valor_etiqueta = tk.Label(frame_entrada, text="Valor:")
valor_etiqueta.grid(row=3, column=0, padx=10)
entrada_valor = tk.Entry(frame_entrada)
entrada_valor.grid(row=3, column=1)

ruta_excel_etiqueta = tk.Label(frame_entrada, text="Ruta del archivo Excel:")
ruta_excel_etiqueta.grid(row=4, column=0, padx=10)
ruta_excel_entrada = tk.Entry(frame_entrada)
ruta_excel_entrada.grid(row=4, column=1)

lista_gastos = tk.Listbox(ventana)
lista_gastos.pack(pady=10)

suma_gastos = 0   # Variable global para almacenar el total de gastos
lista_gastos_data = []   # Lista para almacenar las tuplas de gasto y valor

def agregar_gasto():
    gasto = entrada_gasto.get()
    valor = entrada_valor.get()
    lista_gastos_data.append((gasto, float(valor)))  # Convertir el valor a número
    lista_gastos.insert(tk.END, f"{gasto}: {valor}")
    global suma_gastos
    suma_gastos += float(valor)
    actualizar_totales()
    entrada_gasto.delete(0, tk.END)
    entrada_valor.delete(0, tk.END)

def borrar_gasto():
    seleccion = lista_gastos.curselection()
    if seleccion:
        gasto, valor = lista_gastos_data.pop(seleccion[0])
        lista_gastos.delete(seleccion[0])
        global suma_gastos
        suma_gastos -= valor
        actualizar_totales()

def actualizar_totales():
    total_gastos = sum([valor for _, valor in lista_gastos_data])
    sueldo = float(sueldo_entrada.get())
    sueldo_restante = sueldo - total_gastos
    etiqueta_total_gastos.config(text=f"Total de Gastos: {total_gastos}")
    etiqueta_sueldo_restante.config(text=f"Sueldo Restante: {sueldo_restante}")

def exportar_a_excel():
    try:
        gastos = [gasto for gasto, _ in lista_gastos_data]
        valores = [valor for _, valor in lista_gastos_data]
        mes = mes_entrada.get()
        fecha_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        ruta_excel = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")], initialfile=f"datos_{fecha_actual}.xlsx")

        if ruta_excel:
            print("Exportando datos a Excel...")
            print("Gastos:", gastos)
            print("Valores:", valores)

            # Crear dataframe para gastos y valores
            data_gastos_valores = {
                "Gasto": gastos,
                "Valor": valores
            }
            df_gastos_valores = pd.DataFrame(data_gastos_valores)

            # Crear dataframe para el resto de los datos
            data_resto = {
                "Sueldo": float(sueldo_entrada.get()),
                "Total Gastos": suma_gastos,
                "Sueldo Restante": float(sueldo_entrada.get()) - suma_gastos,
                "Mes": mes
            }
            df_resto = pd.DataFrame(data_resto, index=[0])

            # Crear archivo de Excel y exportar los dataframes en una misma hoja
            with pd.ExcelWriter(ruta_excel) as writer:
                df_gastos_valores.to_excel(writer, sheet_name="Datos", index=False)
                df_resto.to_excel(writer, sheet_name="Datos", startrow=len(df_gastos_valores)+2, index=False)

            print("Datos exportados exitosamente a Excel.")

    except ValueError:
        print("Error: El campo 'Valor' debe contener solo valores numéricos.")

agregar_boton = tk.Button(ventana, text="Agregar Gasto", command=agregar_gasto)
agregar_boton.pack(pady=10)

borrar_boton = tk.Button(ventana, text="Borrar Gasto", command=borrar_gasto)
borrar_boton.pack(pady=10)

exportar_boton = tk.Button(ventana, text="Exportar a Excel", command=exportar_a_excel)
exportar_boton.pack(pady=10)

etiqueta_total_gastos = tk.Label(ventana, text="Total de Gastos: 0")
etiqueta_total_gastos.pack()

etiqueta_sueldo_restante = tk.Label(ventana, text="Sueldo Restante: 0")
etiqueta_sueldo_restante.pack()

ventana.mainloop()