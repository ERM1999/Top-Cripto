import threading
import json
import flet as ft
from kafka import KafkaConsumer
from collections import deque

class AppCripto:
    def __init__(self, pagina: ft.Page):
        # Guardado de la referencia de la página de Flet
        self.pagina = pagina

        # Paleta cromática para toda la interfaz
        self.color_fondo = "#020617"
        self.color_tarjeta = "#1e293b"
        self.color_acento = "#22c55e"

        # Configuración dimensional y visual de la ventana de la aplicación
        self.pagina.bgcolor = self.color_fondo
        self.pagina.window_width = 360
        self.pagina.window_height = 700

        # Estructuras de control de datos históricos y récords financieros
        # Uso de deque con maxlen=12 para optimizar la gestión de puntos del gráfico
        self.puntos_grafico = deque(maxlen=12)
        self.contador_tiempo = 0
        self.record_historico = 69000.00  # Umbral para batir récord

        # Diccionarios de estilos para limpiar condicionales anidados
        self.TENDENCIA_ESTILOS = {
            "Alcista": {
                "color": "green",
                "icon": ft.icons.TRENDING_UP,
                "linea_color": "green"
            },
            "Bajista": {
                "color": "red",
                "icon": ft.icons.TRENDING_DOWN,
                "linea_color": "red"
            }
        }

        self.VOLATILIDAD_ESTILOS = {
            "Alta": {
                "color": "red",
                "icon": ft.icons.WARNING_ROUNDED
            },
            "Media": {
                "color": "orange",
                "icon": ft.icons.EQUALIZER
            },
            "Baja": {
                "color": "green",
                "icon": ft.icons.TRENDING_FLAT
            }
        }
  
        # pagina principal -  valores por defecto antes de que se actualicen con kafka
        self.texto_precio = ft.Text("€67,500", size=38, weight="bold", color="white")
        self.texto_cambio = ft.Text("+1.8% (24h)", size=16, weight="bold", color="greenaccent")
        self.texto_situacion = ft.Text("Esperando datos en tiempo real de Kafka...", color="white")

        # pagina analisis - valores por defecto antes de que se actualicen con kafki
        self.texto_capitalizacion = ft.Text("Cargando...", color=self.color_acento, weight="bold")
        self.texto_volumen = ft.Text("Cargando...", color="white", weight="bold")
        self.texto_record = ft.Text("€69,000", size=20, color="white", weight="bold")
        self.texto_tendencia = ft.Text("Analizando...", color="green", weight="bold")
        self.texto_volatilidad = ft.Text("Analizando...", color="orange", weight="bold")
        
        # indicadores gráficos dinámicos que cambiarán según el mercado
        self.icono_tendencia = ft.Icon(ft.icons.TIPS_AND_UPDATES, color="green")
        self.icono_volatilidad = ft.Icon(ft.icons.EQUALIZER, color="orange")

        # grafico
        self.linea_datos = ft.LineChartData(
            data_points=list(self.puntos_grafico),
            stroke_width=3,
            color=self.color_acento,
            curved=True,
            below_line_bgcolor=ft.colors.with_opacity(0.1, self.color_acento),
        )

        self.grafico_precios = ft.LineChart(
            data_series=[self.linea_datos],
            border=ft.Border(bottom=ft.BorderSide(1, "grey")),
            horizontal_grid_lines=ft.ChartGridLines(interval=50, color="#ffffff11"),
            left_axis=ft.ChartAxis(visible=False), # Oculto los ejes por estetica
            bottom_axis=ft.ChartAxis(visible=False),
            height=120,
            expand=True
        )

   
       # Home
        self.vista_principal = ft.Container(
            expand=True,
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO, spacing=15,
                controls=[
                    # cabecera con imagen de fondo y máscara de contraste 
                    ft.Container(
                        height=300, border_radius=20, clip_behavior="antiAlias",
                        content=ft.Stack(
                            expand=True,
                            controls=[
                                ft.Image(src="assets/fondo.jpg", width=self.pagina.window_width, height=300, fit="cover"),
                                
                                # Capa oscura para que el texto blanco resalte
                                ft.Container(expand=True, bgcolor="#000000aa"), 
                                
                                ft.Container(
                                    padding=20, alignment=ft.Alignment(-1, -0.2),
                                    content=ft.Column(
                                        spacing=8,
                                        controls=[
                                            ft.Text("Top crypto", color="white", size=20, weight="bold"), 
                                            self.texto_precio, 
                                            
                                            # Pastilla/Botón financiero con fondo oscuro para aislar la letra de la imagen
                                            ft.Container(
                                                content=self.texto_cambio,
                                                bgcolor="#1e293b", 
                                                padding=ft.padding.symmetric(vertical=6, horizontal=12),
                                                border_radius=8
                                            )
                                        ]
                                    )
                                ),
                            ]
                        )
                    ),
                    
                    # 2. Panel secundario de máximos y mínimos diarios
                    ft.Container(
                        padding=15, border_radius=12, bgcolor=self.color_tarjeta,
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Column(controls=[ft.Text("Máx 24h", color="grey", weight="bold"), ft.Text("€68,200", color="white", weight="bold")]),
                                ft.Column(controls=[ft.Text("Mín 24h", color="grey", weight="bold"), ft.Text("€66,300", color="white", weight="bold")]),
                            ]
                        )
                    ),
                    
                    # 3. Bloque de noticias contextuales procesadas sintácticamente por el Productor
                    ft.Container(
                        padding=15, border_radius=12, bgcolor=self.color_tarjeta,
                        content=ft.Column(
                            spacing=8,
                            controls=[ft.Text("Situación actual", color="grey", weight="bold"), self.texto_situacion]
                        )
                    ),
                ]
            )
        )

        # ESTADÍSTICAS DINÁMICAS DESDE KAFKA
        self.vista_estadisticas = ft.Container(
            expand=True, padding=20,
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO, spacing=20,
                controls=[
                    ft.Text("Estadísticas", size=26, color="white"),
                    # Datos directos extraídos de la API
                    ft.Row(
                        spacing=15,
                        controls=[
                            ft.Container(expand=True, padding=15, border_radius=12, bgcolor=self.color_tarjeta, content=ft.Column(controls=[ft.Text("Capitalización", color="grey"), self.texto_capitalizacion])),
                            ft.Container(expand=True, padding=15, border_radius=12, bgcolor=self.color_tarjeta, content=ft.Column(controls=[ft.Text("Volumen 24h", color="grey"), self.texto_volumen])),
                        ]
                    ),
                    # Constantes de mercado
                    ft.Row(
                        spacing=15,
                        controls=[
                            ft.Container(expand=True, padding=15, border_radius=12, bgcolor=self.color_tarjeta, content=ft.Column(controls=[ft.Text("Posición", color="grey"), ft.Text("#1", color="white", weight="bold")])),
                            ft.Container(expand=True, padding=15, border_radius=12, bgcolor=self.color_tarjeta, content=ft.Column(controls=[ft.Text("Suministro", color="grey"), ft.Text("19.6M BTC", color="white", weight="bold")])),
                        ]
                    ),
                    # Tarjeta del Máximo Histórico con evaluación interactiva de superación
                    ft.Container(padding=20, border_radius=15, bgcolor=self.color_tarjeta, content=ft.Column(spacing=8, controls=[ft.Text("Máximo histórico (ATH)", color="grey"), self.texto_record])),
                    # Fila analítica: Algoritmos computados por el productor
                    ft.Row(
                        spacing=15,
                        controls=[
                            ft.Container(expand=True, padding=15, border_radius=12, bgcolor=self.color_tarjeta, content=ft.Column(controls=[self.icono_tendencia, ft.Text("Tendencia", color="grey"), self.texto_tendencia])),
                            ft.Container(expand=True, padding=15, border_radius=12, bgcolor=self.color_tarjeta, content=ft.Column(controls=[self.icono_volatilidad, ft.Text("Volatilidad", color="grey"), self.texto_volatilidad])),
                        ]
                    ),
                    # Contenedor del gráfico dinámico alimentado por el Stream de Kafka
                    ft.Container(
                        padding=15, border_radius=12, bgcolor=self.color_tarjeta,
                        content=ft.Column(
                            spacing=10,
                            controls=[
                                ft.Text("Evolución del precio (Tiempo real)", color="grey"),
                                ft.Container(content=self.grafico_precios, padding=10),
                            ]
                        )
                    ),
                ]
            )
        )

        # GUÍA AL USUARIO)
        # ---------- PANTALLA 3: MÓDULO EDUCATIVO (GUÍA AL USUARIO) ----------
        self.vista_guia = ft.Container(
            expand=True, padding=20,
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO, spacing=15,
                controls=[
                    ft.Text("Guía Crypto", size=26, color="white", weight="bold"),
                    ft.Text("📊 ¿Qué significan los datos analíticos?", color=self.color_acento, size=16, weight="bold"),
                    
                    # Explicación: Capitalización
                    ft.Container(
                        padding=15, border_radius=12, bgcolor=self.color_tarjeta, 
                        content=ft.Column(
                            spacing=5,
                            controls=[
                                ft.Row([ft.Icon(ft.icons.ACCOUNT_BALANCE_WALLET, color=self.color_acento, size=18), ft.Text("Capitalización de Mercado", color="white", weight="bold")]),
                                ft.Text("Es el valor total en euros de todos los Bitcoins que existen en circulación. Se calcula multiplicando el precio actual por el suministro disponible. Indica el tamaño real del mercado.")
                            ]
                        )
                    ),
                    
                    # Explicación: Volumen 24h
                    ft.Container(
                        padding=15, border_radius=12, bgcolor=self.color_tarjeta, 
                        content=ft.Column(
                            spacing=5,
                            controls=[
                                ft.Row([ft.Icon(ft.icons.INSERT_CHART_OUTLINED, color="blue", size=18), ft.Text("Volumen (24h)", color="white", weight="bold")]),
                                ft.Text("Mide la cantidad total de dinero que se ha movido en compras y ventas de Bitcoin durante el último día. Un volumen alto significa que hay mucho interés y liquidez.")
                            ]
                        )
                    ),

                    # Explicación: Tendencia
                    ft.Container(
                        padding=15, border_radius=12, bgcolor=self.color_tarjeta, 
                        content=ft.Column(
                            spacing=5,
                            controls=[
                                ft.Row([ft.Icon(ft.icons.TRENDING_UP, color="green", size=18), ft.Text("Tendencia (Alcista / Bajista)", color="white", weight="bold")]),
                                ft.Text("El sistema evalúa el porcentaje de cambio diario. Si el precio ha subido respecto al día anterior la tendencia es Alcista (Verde); si ha bajado, es Bajista (Rojo).")
                            ]
                        )
                    ),

                    # Explicación: Volatilidad
                    ft.Container(
                        padding=15, border_radius=12, bgcolor=self.color_tarjeta, 
                        content=ft.Column(
                            spacing=5,
                            controls=[
                                ft.Row([ft.Icon(ft.icons.WARNING_ROUNDED, color="orange", size=18), ft.Text("Volatilidad (Alta / Media / Baja)", color="white", weight="bold")]),
                                ft.Text("Mide la fuerza y velocidad con la que cambia el precio. Nuestro algoritmo local la clasifica como 'Alta' si el precio varía más de un 3% en el día, 'Media' entre 1-3% y 'Baja' si es menor.")
                            ]
                        )
                    ),

                    # Explicación: Máximo Histórico (ATH)
                    ft.Container(
                        padding=15, border_radius=12, bgcolor=self.color_tarjeta, 
                        content=ft.Column(
                            spacing=5,
                            controls=[
                                ft.Row([ft.Icon(ft.icons.STAR, color="gold", size=18), ft.Text("Máximo Histórico (ATH)", color="white", weight="bold")]),
                                ft.Text("Representa el precio más alto jamás alcanzado por Bitcoin. La aplicación controla este valor en tiempo real: si el flujo de Kafka supera el récord actual, se actualiza automáticamente.")
                            ]
                        )
                    ),
                ]
            )
        )

        # NAVBAR
        self.barra_navegacion = ft.Container(
            bgcolor=self.color_tarjeta, height=60, border_radius=30, margin=ft.Margin(10, 5, 10, 15),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                controls=[
                    ft.IconButton(icon=ft.icons.HOME, icon_color="white", data="1", on_click=self.cambiar_vista),
                    ft.IconButton(icon="bar_chart_rounded", icon_color="white", data="2", on_click=self.cambiar_vista),
                    ft.IconButton(icon=ft.icons.INFO, icon_color="white", data="3", on_click=self.cambiar_vista),
                ]
            )
        )

        # Definición del área de contenido inicial y renderizado general de la escena
        self.area_contenido = ft.Container(expand=True, animate_opacity=ft.Animation(300, "ease"), content=self.vista_principal)
        self.pagina.add(ft.Column(expand=True, controls=[self.area_contenido, self.barra_navegacion]))

        # Inicialización del hilo de ejecución secundario para evitar el bloqueo de la UI al escuchar Kafka
        self.hilo_kafka = threading.Thread(target=self.escuchar_kafka, daemon=True)
        self.hilo_kafka.start()

    def cambiar_vista(self, evento):
        # Efecto visual de transición 
        self.area_contenido.opacity = 0
        self.pagina.update()
        
        if evento.control.data == "1": self.area_contenido.content = self.vista_principal
        elif evento.control.data == "2": self.area_contenido.content = self.vista_estadisticas
        elif evento.control.data == "3": self.area_contenido.content = self.vista_guia
        
        self.area_contenido.opacity = 1
        self.pagina.update()

   
    # CONSUMIDOR DE KAFKA:
   
    def escuchar_kafka(self):
        try:
            # consumidor conectado al clúster local de Docker
            consumidor = KafkaConsumer(
                'precios-crypto',
                bootstrap_servers=['localhost:9092'],
                value_deserializer=lambda datos: json.loads(datos.decode('utf-8')),
                auto_offset_reset='latest' # Escuchamos siempre la información más reciente
            )
            
            # Bucle infinito de captura de mensajes en streaming
            for mensaje in consumidor:
                datos_nuevos = mensaje.value
                precio_numerico = datos_nuevos["precio_num"]
                
            
                # actualizacion en home
                
                self.texto_precio.value = datos_nuevos["precio"]
                nuevo_cambio = datos_nuevos["cambio"]
                self.texto_cambio.value = f"{nuevo_cambio} (24h)"
                self.texto_situacion.value = datos_nuevos["mensaje"]
                
                # Control colores según el rendimiento del precio
                if "-" in nuevo_cambio:
                    self.texto_cambio.color = "red"
                else:
                    self.texto_cambio.color = "lightgreen"
                
               
                # actualizacion en estadisticas
                
        
                self.texto_capitalizacion.value = datos_nuevos["capitalizacion"]
                self.texto_volumen.value = datos_nuevos["volumen"]
                
                #  si se supera el récord histórico global o no
                if precio_numerico > self.record_historico:
                    self.record_historico = precio_numerico
                    self.texto_record.value = f"€{round(self.record_historico, 2):,}"
                    self.texto_record.color = "gold" # Alerta dorada indicando hito financiero batido en directo
                
                # Volcado de analíticas operacionales computadas en origen
                nueva_tendencia = datos_nuevos["tendencia"]
                nueva_volatilidad = datos_nuevos["volatilidad"]
                
                self.texto_tendencia.value = nueva_tendencia
                self.texto_volatilidad.value = nueva_volatilidad
                
                # Adaptación de estilos visuales e iconos según la dirección del mercado usando diccionario
                if nueva_tendencia in self.TENDENCIA_ESTILOS:
                    estilos_tendencia = self.TENDENCIA_ESTILOS[nueva_tendencia]
                    self.texto_tendencia.color = estilos_tendencia["color"]
                    self.icono_tendencia.icon = estilos_tendencia["icon"]
                    self.icono_tendencia.icon_color = estilos_tendencia["color"]
                    self.linea_datos.color = estilos_tendencia["linea_color"]
                    
                # Clasificación visual y nivelación de la volatilidad del mercado usando diccionario
                if nueva_volatilidad in self.VOLATILIDAD_ESTILOS:
                    estilos_volatilidad = self.VOLATILIDAD_ESTILOS[nueva_volatilidad]
                    self.texto_volatilidad.color = estilos_volatilidad["color"]
                    self.icono_volatilidad.icon = estilos_volatilidad["icon"]
                    self.icono_volatilidad.icon_color = estilos_volatilidad["color"]

                # Actualizacion de la gráfica con deque automático
                self.contador_tiempo += 1
                self.puntos_grafico.append(ft.LineChartDataPoint(self.contador_tiempo, precio_numerico))
                self.linea_datos.data_points = list(self.puntos_grafico)
                
                # Consolidamos las actualizaciones modificadas en la UI mediante un renderizado unificado
                self.pagina.update()
                
        except Exception as error:
            print(f" [CONSUMIDOR] Error crítico leyendo Kafka: {error}")

def lanzar_aplicacion(pagina: ft.Page):
    AppCripto(pagina)

# Punto de entrada principal de la ejecución de Flet
ft.app(target=lanzar_aplicacion)
