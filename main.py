import flet as ft

class AppCripto:
    def __init__(self, page: ft.Page):

        self.page = page

        # colores
        self.color_fondo = "#020617"
        self.container_color = "#1e293b"
        self.accent_color = "#22c55e"

        self.page.bgcolor = self.color_fondo
        self.page.window_width = 360
        self.page.window_height = 700

        # ---------- CONTAINER 1 (HOME) ----------
        self.container_1 = ft.Container(
    expand=True,
    content=ft.Column(
        scroll=ft.ScrollMode.AUTO,
        spacing=15,
        controls=[

            # -------- PORTADA --------
            ft.Container(
                height=300,
                border_radius=20,
                clip_behavior="antiAlias",
                content=ft.Stack(
                    expand=True,
                    controls=[

                        # Imagen de fondo
                        ft.Image(
                            src="assets/fondo.jpg",
                            width=self.page.window_width,
                            height=300,
                            fit="cover",
                        ),

                        # Capa oscura
                        ft.Container(
                            expand=True,
                            bgcolor="#00000066",
                        ),

                        # DATOS PRINCIPALES
                        ft.Container(
                            padding=15,
                            alignment=ft.Alignment(-1, -0.3),
                            content=ft.Column(
                                spacing=5,
                                controls=[
                                    ft.Text("Top crypto", color="white", size=18),
                                    ft.Text("€67,500", size=36, weight="bold", color="white"),
                                    ft.Text("+1.8% (24h)", color="lightgreen"),
                                ]
                            )
                        ),
                    ]
                )
            ),

            # -------- MAX / MIN --------
            ft.Container(
                padding=15,
                border_radius=12,
                bgcolor=self.container_color,
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text("Máx 24h", color="grey"),
                                ft.Text("€68,200", color="white"),
                            ]
                        ),
                        ft.Column(
                            controls=[
                                ft.Text("Mín 24h", color="grey"),
                                ft.Text("€66,300", color="white"),
                            ]
                        ),
                    ]
                )
            ),

            # -------- SITUACIÓN --------
            ft.Container(
                padding=15,
                border_radius=12,
                bgcolor=self.container_color,
                content=ft.Column(
                    spacing=8,
                    controls=[
                        ft.Text("Situación actual", color="grey"),
                        ft.Text(
                            "Bitcoin mantiene una tendencia alcista leve con estabilidad en el mercado en las últimas 24 horas.",
                            color="white",
                        ),
                    ]
                )
            ),

            
        ]
    )
)




        # ---------- CONTAINER 2 ----------
        self.container_2 = ft.Container(
    expand=True,
    padding=20,
    content=ft.Column(
        scroll=ft.ScrollMode.AUTO,
        spacing=20,
        controls=[

            ft.Text("Estadísticas", size=26, color="white"),

            # -------- PRIMER GRID --------
            ft.Row(
                spacing=15,
                controls=[

                    ft.Container(
                        expand=True,
                        padding=15,
                        border_radius=12,
                        bgcolor=self.container_color,
                        content=ft.Column(
                            controls=[
                                ft.Text("Capitalización", color="grey"),
                                ft.Text("1.3T €", color=self.accent_color),
                            ]
                        )
                    ),

                    ft.Container(
                        expand=True,
                        padding=15,
                        border_radius=12,
                        bgcolor=self.container_color,
                        content=ft.Column(
                            controls=[
                                ft.Text("Volumen 24h", color="grey"),
                                ft.Text("2.1B €", color="white"),
                            ]
                        )
                    ),
                ]
            ),

            # -------- SEGUNDO GRID --------
            ft.Row(
                spacing=15,
                controls=[

                    ft.Container(
                        expand=True,
                        padding=15,
                        border_radius=12,
                        bgcolor=self.container_color,
                        content=ft.Column(
                            controls=[
                                ft.Text("Posición", color="grey"),
                                ft.Text("#1", color="white"),
                            ]
                        )
                    ),

                    ft.Container(
                        expand=True,
                        padding=15,
                        border_radius=12,
                        bgcolor=self.container_color,
                        content=ft.Column(
                            controls=[
                                ft.Text("Suministro", color="grey"),
                                ft.Text("19.6M BTC", color="white"),
                            ]
                        )
                    ),
                ]
            ),

            # -------- ATH --------
            ft.Container(
                padding=20,
                border_radius=15,
                bgcolor=self.container_color,
                content=ft.Column(
                    spacing=8,
                    controls=[
                        ft.Text("Máximo histórico (ATH)", color="grey"),
                        ft.Text("€69,000", size=20, color="white"),
                    ]
                )
            ),

            # -------- TREND / VOLATILITY --------
            ft.Row(
                spacing=15,
                controls=[

                    ft.Container(
                        expand=True,
                        padding=15,
                        border_radius=12,
                        bgcolor=self.container_color,
                        content=ft.Column(
                            controls=[
                                ft.Icon("home", color="green"),
                                ft.Text("Tendencia", color="grey"),
                                ft.Text("Alcista", color="green"),
                            ]
                        )
                    ),

                    ft.Container(
                        expand=True,
                        padding=15,
                        border_radius=12,
                        bgcolor=self.container_color,
                        content=ft.Column(
                            controls=[
                                ft.Icon("warning", color="orange"),
                                ft.Text("Volatilidad", color="grey"),
                                ft.Text("Media", color="orange"),
                            ]
                        )
                    ),
                ]
            ),

            # -------- BLOQUE EXTRA (SCROLL) --------
            ft.Container(
                padding=15,
                border_radius=12,
                bgcolor=self.container_color,
                content=ft.Column(
                    spacing=10,
                    controls=[
                        ft.Text("Evolución del precio (24h)", color="grey"),

                        ft.Text(
                            "Aquí se mostrará un gráfico de la evolución del precio en tiempo real.",
                            color="white"
                        ),

                        ft.Text(
                            "📈 Gráfico en desarrollo…",
                            color=self.accent_color
                        ),
                    ]
                )
            ),
        ]
    )
)



        # ---------- CONTAINER 3 (GUÍA) ----------
        self.container_3 = ft.Container(
    expand=True,
    padding=20,
    content=ft.Column(
        scroll=ft.ScrollMode.AUTO,
        spacing=20,
        controls=[

            ft.Text("Guía Crypto", size=26, color="white"),

            ft.Text("📊 ¿Qué significan los datos?", color=self.accent_color),

            ft.Text(
                "Esta sección explica los indicadores que aparecen en la aplicación para ayudarte a entender mejor la información.",
                color="white"
            ),

            # -------- CAPITALIZACIÓN --------
            ft.Container(
                padding=15,
                border_radius=12,
                bgcolor=self.container_color,
                content=ft.Column(
                    controls=[
                        ft.Text("Capitalización", color="grey"),
                        ft.Text(
                            "Es el valor total de la criptomoneda. Se calcula multiplicando el precio por el número de monedas en circulación.",
                            color="white"
                        ),
                    ]
                )
            ),

            # -------- VOLUMEN --------
            ft.Container(
                padding=15,
                border_radius=12,
                bgcolor=self.container_color,
                content=ft.Column(
                    controls=[
                        ft.Text("Volumen 24h", color="grey"),
                        ft.Text(
                            "Cantidad de dinero que se ha movido en las últimas 24 horas.",
                            color="white"
                        ),
                    ]
                )
            ),

            # -------- POSICIÓN --------
            ft.Container(
                padding=15,
                border_radius=12,
                bgcolor=self.container_color,
                content=ft.Column(
                    controls=[
                        ft.Text("Posición", color="grey"),
                        ft.Text(
                            "Lugar que ocupa la criptomoneda en el ranking global.",
                            color="white"
                        ),
                    ]
                )
            ),

            # -------- SUMINISTRO --------
            ft.Container(
                padding=15,
                border_radius=12,
                bgcolor=self.container_color,
                content=ft.Column(
                    controls=[
                        ft.Text("Suministro", color="grey"),
                        ft.Text(
                            "Cantidad de monedas disponibles en circulación.",
                            color="white"
                        ),
                    ]
                )
            ),

            # -------- MÁX HISTÓRICO --------
            ft.Container(
                padding=15,
                border_radius=12,
                bgcolor=self.container_color,
                content=ft.Column(
                    controls=[
                        ft.Text("Máximo histórico (ATH)", color="grey"),
                        ft.Text(
                            "Precio más alto alcanzado por la criptomoneda.",
                            color="white"
                        ),
                    ]
                )
            ),

            # -------- MÁX / MÍN 24H --------
            ft.Container(
                padding=15,
                border_radius=12,
                bgcolor=self.container_color,
                content=ft.Column(
                    controls=[
                        ft.Text("Máx 24h", color="grey"),
                        ft.Text(
                            "Precio más alto en las últimas 24 horas.",
                            color="white"
                        ),
                    ]
                )
            ),

            ft.Container(
                padding=15,
                border_radius=12,
                bgcolor=self.container_color,
                content=ft.Column(
                    controls=[
                        ft.Text("Mín 24h", color="grey"),
                        ft.Text(
                            "Precio más bajo en las últimas 24 horas.",
                            color="white"
                        ),
                    ]
                )
            ),

            # -------- TENDENCIA --------
            ft.Container(
                padding=15,
                border_radius=12,
                bgcolor=self.container_color,
                content=ft.Column(
                    controls=[
                        ft.Text("Tendencia", color="grey"),
                        ft.Text(
                            "Indica si el mercado está subiendo o bajando.",
                            color="white"
                        ),
                    ]
                )
            ),

            # -------- VOLATILIDAD --------
            ft.Container(
                padding=15,
                border_radius=12,
                bgcolor=self.container_color,
                content=ft.Column(
                    controls=[
                        ft.Text("Volatilidad", color="grey"),
                        ft.Text(
                            "Indica cuánto varía el precio en poco tiempo.",
                            color="white"
                        ),
                    ]
                )
            ),

        ]
    )
)


        # ---------- NAVBAR ----------
        self.nav = ft.Container(
            bgcolor=self.container_color,
            height=60,
            border_radius=30,
            margin=ft.Margin(10, 5, 10, 15),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                controls=[
                    ft.IconButton(icon=ft.icons.HOME, icon_color="white", data="1", on_click=self.change_page),
                    ft.IconButton(icon=ft.icons.BAR_CHART, icon_color="white", data="2", on_click=self.change_page),
                    ft.IconButton(icon=ft.icons.INFO, icon_color="white", data="3", on_click=self.change_page),

                ]
            )
        )

        # ---------- LAYOUT ----------
        self.content_area = ft.Container(
            expand=True,
            animate_opacity=ft.Animation(300, "ease"),
            content=self.container_1
        )

        self.page.add(
            ft.Column(
                expand=True,
                controls=[
                    self.content_area,
                    self.nav
                ]
            )
        )

    # ---------- CAMBIO DE PANTALLA ----------
    def change_page(self, e):

        self.content_area.opacity = 0
        self.page.update()

        if e.control.data == "1":
            self.content_area.content = self.container_1
        elif e.control.data == "2":
            self.content_area.content = self.container_2
        elif e.control.data == "3":
            self.content_area.content = self.container_3

        self.content_area.opacity = 1
        self.page.update()


def main(page: ft.Page):
    AppCripto(page)


ft.app(target=main)
