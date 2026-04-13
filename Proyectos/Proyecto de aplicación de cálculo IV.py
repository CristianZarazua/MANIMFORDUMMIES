from manim import *

class Inicio(Scene):
    def construct(self):
        # Creación del objeto Tex
        materia = Tex(
            r"Proyecto de aplicación\\Cálculo IV\\Proyección de Mercator y el Jacobiano",
            tex_environment="center"
        )

        por = Tex(
            r"Presentado por:",
            tex_environment="center"
        )

        nombre1 = Tex(
            r"Cristian Michel Zarazua Castañeda",
            tex_environment="center"
        ).set_color_by_gradient("#2E4C6D", "#396EB0", "#4E9F3D", "#D8E9A8").scale(1.5)

        nombre2 = Tex(
            r"Oswaldo Díaz Díaz",
            tex_environment="center"
        ).set_color_by_gradient("#FFB7B2", "#FF9AA2", "#E2A9FF", "#C5A3FF").scale(1.5)

        nombre3 = Tex(
            r"Nombre 3",
            tex_environment="center"
        ).set_color_by_gradient("#F4A261", "#E9C46A", "#2A9D8F", "#264653").scale(1.5)

        nombre4 = Tex(
            r"Nombre 4",
            tex_environment="center"
        ).set_color_by_gradient("#CFD8DC", "#90A4AE", "#607D8B", "#455A64").scale(1.5)

        nombre5 = Tex(
            r"María del Carmen Ramírez Torres",
            tex_environment="center"
        ).set_color_by_gradient(RED, "#FF4500", ORANGE, YELLOW).scale(1.5)

        # Modificaciones de posición, color y tamaño
        materia.move_to([0, 0, 0]).scale(1.5).set_color_by_gradient(RED, ORANGE, YELLOW, "#FFD700")
        por.move_to([0, 0, 0]).scale(1.5).set_color_by_gradient("#1A5F7A", "#22A39F", "#57C4AD", "#B5EAEA")
        
        # Modificaciones de textos unidos
        texto_unificado = VGroup(nombre1, nombre2, nombre3, nombre4, nombre5)
        texto_unificado.arrange(DOWN, aligned_edge=ORIGIN)
        texto_unificado.move_to([0, 0, 0])  # <-- CENTRADO EXACTO EN PANTALLA

        # Animaciones
        self.play(Write(materia))
        self.wait(5)
        self.play(ReplacementTransform(materia, por))
        self.wait(3)
        self.play(ReplacementTransform(por, texto_unificado))
        self.wait(8)
        self.play(FadeOut(texto_unificado), run_time=2)

class Introduccion(Scene):
    def construct(self):
        # Creación del objeto Tex
        testo1 = Tex(
            r"1. ¿Por qué Groelandia se ve\\tan grande en nuestros mapas?",
            tex_environment="center"
        )

        testo2 = Tex(
            r"Cuando miramos un mapa del mundo, estamos\\acostumbrados a ver a Groenlandia casi del tamaño\\de África. Pero en la realidad... África es catorce\\veces más grande.\\¿Por qué nuestros mapas mienten de esa forma?",
            tex_environment="center"
        )

        testo3 = Tex(
            r"La respuesta está en un problema matemático\\irresoluble: no se puede aplanar una esfera sin\\estirar o romper algo. En 1569, Gerardus Mercator creó\\un mapa que resolvía un problema de navegación, pero\\a costa de distorsionar las áreas cerca de los polos.",
            tex_environment="center"
        )

        testo4 = Tex(
            r"En esta animación vamos a visualizar esa\\distorsión usando una herramienta del cálculo\\multivariable llamada el Jacobiano. Veremos cómo este\\número nos dice, punto por punto, cuánto ha estirado\\el mapa la realidad.",
            tex_environment="center"
        )

        # Modificaciones de posición, color y tamaño
        testo1.move_to([0, 0, 0]).scale(1.5).set_color_by_gradient("#98DDCA", "#D3E0EA", "#A2D5F2", "#79C2D0")
        testo2.move_to([0, 0, 0]).scale(1).set_color_by_gradient(PURPLE, "#8A2BE2", "#9370DB", "#BA55D3")
        testo3.move_to([0, 0, 0]).scale(1).set_color_by_gradient(RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE)
        testo4.move_to([0, 0, 0]).scale(1).set_color_by_gradient(RED, ORANGE, YELLOW, "#FFD700")

        # Animaciones
        self.play(Write(testo1),run_time=3)
        self.wait(5)
        self.play(testo1.animate.scale(0.5).to_corner(UP + LEFT, buff=0.3),run_time=2)
        self.play(Write(testo2), run_time=4.5)
        self.wait(15)
        self.play(ReplacementTransform(testo2, testo3), run_time=2)
        self.wait(15)
        self.play(ReplacementTransform(testo3, testo4), run_time=2)
        self.wait(15)
        self.play(FadeOut(testo1, testo4), run_time=2)

class Visualizacion(ThreeDScene):
    def construct(self):
        # ==============================================================
        # 1. DEFINICIÓN DE OBJETOS / CONTENIDO
        # ==============================================================

        # --- Título de la sección ---
        titulo_seccion = Tex(
            r"1. Visualización",
            tex_environment="center"
        )

        # --- Esfera terrestre (sólida) ---
        esfera = Sphere(
            radius=2.0,
            resolution=(32, 32),
            fill_color=BLUE_C,
            fill_opacity=0.85,
            stroke_width=2,
            stroke_color=WHITE
        )

        # --- Líneas de latitud y longitud en la ESFERA ---
        lineas_esfera = VGroup()

        # Paralelos (círculos horizontales)
        for lat in np.linspace(-1, 1, 7)[1:-1]:
            circulo = Circle(
                radius=2.0 * np.sqrt(1 - lat**2),
                color=GRAY_B,
                stroke_width=1
            )
            circulo.shift(2.0 * lat * OUT)
            lineas_esfera.add(circulo)

        # Meridianos (elipses verticales rotadas)
        for lon in np.linspace(0, PI, 6)[1:-1]:
            elipse = Circle(
                radius=2.0,
                color=GRAY_B,
                stroke_width=1
            )
            elipse.apply_matrix([
                [np.cos(lon), -np.sin(lon), 0],
                [np.sin(lon),  np.cos(lon), 0],
                [0, 0, 1]
            ])
            lineas_esfera.add(elipse)

        # Agrupamos esfera y líneas para manipularlas juntas
        globo_terraqueo = VGroup(esfera, lineas_esfera)

        # --- Líneas correspondientes en el MAPA DE MERCATOR ---
        lineas_mapa = VGroup()

        # Meridianos en el mapa (líneas verticales rectas)
        # La longitud λ se mapea a x = λ (escalada)
        longitudes = np.linspace(-PI, PI, 13)[1:-1]  # Evitamos extremos para no amontonar
        for lon in longitudes:
            x = lon * 1.5  # Factor de escala horizontal
            linea = Line(
                start=[x, -3.5, 0],
                end=[x, 3.5, 0],
                color=GRAY_B,
                stroke_width=1
            )
            lineas_mapa.add(linea)

        # Paralelos en el mapa (líneas horizontales según y = ln(tan(π/4 + φ/2)))
        latitudes = np.linspace(-1.3, 1.3, 9)[1:-1]  # φ en radianes aprox
        for phi in latitudes:
            y_centro = np.log(np.tan(np.pi/4 + phi/2)) * 1.5  # Factor de escala vertical
            # Limitamos y para que no se dispare en los polos
            if abs(y_centro) > 4.0:
                continue
            # Cada paralelo es una línea horizontal que va de x=-π*1.5 a x=π*1.5
            paralelo = Line(
                start=[-PI*1.5, y_centro, 0],
                end=[PI*1.5, y_centro, 0],
                color=GRAY_B,
                stroke_width=1
            )
            lineas_mapa.add(paralelo)

        # Grupo completo del mapa (solo líneas, sin superficie)
        mapa_mercator = VGroup(lineas_mapa)

        # --- Textos informativos (HUD) ---
        etiqueta_radio = Tex(
            r"\text{Radio} = R",  # Editar texto
            font_size=30,
            color=YELLOW
        )

        texto_intro_deformacion = Text(
            "Editar texto: explicación de la proyección",  # Editar texto
            font_size=28,
            color=WHITE
        )

        # CORRECCIÓN: MathTex para ecuación matemática pura
        ecuacion_mercator = MathTex(
            r"x = \lambda,\quad y = \ln\left[\tan\left(\frac{\pi}{4}+\frac{\phi}{2}\right)\right]",
            font_size=36,
            color=TEAL
        )

        texto_jacobiano = Text(
            "Editar texto: el Jacobiano mide la distorsión de área",  # Editar texto
            font_size=28,
            color=YELLOW
        )

        # ==============================================================
        # 2. CONFIGURACIÓN DE PROPIEDADES (Color, posición, tamaño...)
        # ==============================================================

        # --- Título ---
        titulo_seccion.move_to([0, 0, 0])
        titulo_seccion.scale(1.5)
        titulo_seccion.set_color_by_gradient(
            "#98DDCA", "#D3E0EA", "#A2D5F2", "#79C2D0"
        )

        # --- Globo terráqueo ---
        globo_terraqueo.shift(IN * 0.5)

        # --- Mapa de Mercator (lo posicionamos en el centro, pero aparecerá después) ---
        mapa_mercator.move_to([0, 0, 0])
        mapa_mercator.shift(IN * 0.5)

        # --- Textos fijos ---
        etiqueta_radio.to_corner(DOWN + RIGHT, buff=0.4)
        texto_intro_deformacion.to_corner(UP + RIGHT, buff=0.4)
        ecuacion_mercator.to_edge(DOWN, buff=0.8)
        texto_jacobiano.next_to(ecuacion_mercator, UP, buff=0.2)

        # ==============================================================
        # 3. SECUENCIA DE ANIMACIONES (Aparición, movimiento, salida)
        # ==============================================================

        # --- Fase 1: Título ---
        self.play(Write(titulo_seccion), run_time=3)
        self.wait(1)
        self.play(
            titulo_seccion.animate.scale(0.5 / 1.5).to_corner(UP + LEFT, buff=0.3),
            run_time=2
        )
        self.wait(0.5)

        # --- Fase 2: Cámara 3D y aparición del globo ---
        self.set_camera_orientation(phi=70 * DEGREES, theta=-30 * DEGREES)
        self.camera.frame_center = [0, 0, 0.5]

        self.add_fixed_in_frame_mobjects(
            etiqueta_radio, texto_intro_deformacion,
            ecuacion_mercator, texto_jacobiano
        )
        # Inicialmente ocultamos los textos de deformación
        texto_intro_deformacion.set_opacity(0)
        ecuacion_mercator.set_opacity(0)
        texto_jacobiano.set_opacity(0)

        self.play(
            GrowFromCenter(globo_terraqueo),
            FadeIn(etiqueta_radio, shift=UP * 0.2),
            run_time=2
        )
        self.wait(1)

        # --- Fase 3: Rotación del globo ---
        self.play(
            Rotate(globo_terraqueo, angle=2 * PI, axis=UP, rate_func=linear),
            run_time=12
        )
        self.wait(2)

        # --- Fase 4: Preparación para la deformación ---
        # Mostramos el texto introductorio
        self.play(FadeIn(texto_intro_deformacion, shift=DOWN * 0.3), run_time=1.5)
        self.wait(2)

        # Ocultamos etiqueta de radio (ya no es relevante)
        self.play(FadeOut(etiqueta_radio), run_time=1)

        # --- Fase 5: Deformación de la esfera al mapa ---
        # La esfera sólida se desvanece para dejar solo las líneas
        self.play(FadeOut(esfera), run_time=1.5)

        # Transformamos las líneas de la esfera a las líneas del mapa
        self.play(
            Transform(lineas_esfera, lineas_mapa, replace_mobject_with_target_in_scene=True),
            run_time=5,
            rate_func=smooth
        )
        self.wait(1)

        # Mostramos la ecuación de Mercator
        self.play(Write(ecuacion_mercator), run_time=2)
        self.wait(2)

        # Mostramos texto sobre Jacobiano
        self.play(FadeIn(texto_jacobiano, shift=UP * 0.2), run_time=1.5)
        self.wait(3)

        # --- Fase 6: Rotación de cámara para apreciar el mapa 2D ---
        self.move_camera(phi=0 * DEGREES, theta=-90 * DEGREES, run_time=3)
        self.wait(2)

        # --- Fase 7: FadeOut final de todos los elementos ---
        self.play(
            FadeOut(VGroup(
                titulo_seccion, lineas_esfera,  # lineas_esfera ahora es el mapa
                texto_intro_deformacion, ecuacion_mercator, texto_jacobiano
            )),
            run_time=2
        )
        self.wait(1)
