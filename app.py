import flet as ft 

def main(page: ft.Page):
    page.title="ventana"
    page.theme_mode=ft.ThemeMode.DARK 
    page.window.width=370
    page.window.height=600
    page.window.min_width=370
    page.window.min_height=600
    page.window.resizable=False

    grid =ft.GridView(runs_count=8, max_extent=40, spacing=2, run_spacing=2,height=334, width=334)

    pixels = []
    
    def cerrar_alerta(e):
        alerta.open = False
        page.update()
        
    alerta = ft.AlertDialog(
        title=ft.Text("⚠️ Advertencia", color=ft.Colors.YELLOW, weight=ft.FontWeight.BOLD),    
       
        content=ft.Text("El texto ingresado contiene caracteres inválidos.\nUse únicamente números hexadecimales quevan de\n (0-9) y letras de la A a la F."),
        actions=[
            ft.TextButton("Aceptar", on_click=cerrar_alerta)
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
    page.overlay.append(alerta)

    def actualizar_hex():
        bin_value = "".join(["1" if p.bgcolor == "yellow" else "0" for p in pixels])
        hex_value = hex(int(bin_value, 2))[2:].upper().zfill(16)
        output_hex.value = hex_value
        page.update()
    
    def toggle_pixels(e):
        btn = e.control
        btn.bgcolor = "yellow" if btn.bgcolor == "black" else "black"
        actualizar_hex()
        page.update()
        
    for fila in range(8):
        for columna in range(8):
            btn = ft.Container(
                width=40,
                height=40,
                bgcolor="black",
                on_click=toggle_pixels
            )
            pixels.append(btn)
            grid.controls.append(btn)            
        
    input_hex = ft.TextField(label="Codigo Hex", width=200,max_length=16)   
    output_hex = ft.Text(value="0000000000000000", size=20)

    def cargar_hex(e):
        
        texto_usuario = input_hex.value.strip().upper()
        
        if len(texto_usuario) <= 16 and all(c in "0123456789ABCDEF" for c in texto_usuario):
            try:
                hex_value = texto_usuario.zfill(16)
                
                bin_value = bin(int(hex_value, 16))[2:].zfill(64)
                for i, bit in enumerate(bin_value):
                    pixels[i].bgcolor = "yellow" if bit == '1' else "black"
                    
                output_hex.value = hex_value
                page.update()
            except ValueError:
                alerta.open = True 
                page.update()
        else:
            
            alerta.open = True 
            page.update()

    boton_cargar = ft.ElevatedButton("Cargar Hex", on_click=cargar_hex)        
    page.add(ft.Column([
            grid,
            ft.Row([input_hex, boton_cargar], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([ft.Text("Hex actual: "), output_hex], alignment=ft.MainAxisAlignment.CENTER)
        ], alignment=ft.MainAxisAlignment.START, spacing=20)
    )
    
ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=8000)
