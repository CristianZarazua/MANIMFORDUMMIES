from manim import *

# ============================================================
# CLASE BASE: Fondo de cuaderno de cuadro (blanco con cuadrícula)
# ============================================================
class CuadernoScene(Scene):
    """Escena base: fondo blanco con cuadrícula tipo cuaderno de cuadro."""

    def setup(self):
        # Fondo blanco
        self.camera.background_color = WHITE

        # Cuadrícula tipo cuaderno (cuadros de 0.5 unidades)
        self.cuadricula = NumberPlane(
            x_range=[-8, 8, 0.5],
            y_range=[-5, 5, 0.5],
            background_line_style={
                "stroke_color": "#A8C4DC",   # azul grisáceo claro
                "stroke_width": 1,
                "stroke_opacity": 0.45,
            },
            axis_config={"stroke_opacity": 0},   # ocultar ejes
        )
        self.add(self.cuadricula)

        # Línea de margen roja (como en los cuadernos)
        self.margen = Line(
            start=[-6, -4, 0],
            end=[-6, 4, 0],
            color="#E88B8B",
            stroke_width=1.5,
            stroke_opacity=0.85,
        )
        self.add(self.margen)

    def titulo_diapositiva(self, texto):
        """Devuelve un VGroup con el título y su subrayado."""
        titulo = Text(
            texto,
            font_size=34,
            color="#1A3A5C",
            weight=BOLD,
        )
        titulo.to_edge(UP, buff=0.55)

        linea = Line(
            start=titulo.get_left() + DOWN * 0.15 + LEFT * 0.1,
            end=titulo.get_right() + DOWN * 0.15 + RIGHT * 0.1,
            color="#1A3A5C",
            stroke_width=2,
        )
        return VGroup(titulo, linea)


# ============================================================
# DIAPOSITIVA 1: PORTADA
# ============================================================
class D01_Portada(CuadernoScene):
    def construct(self):
        # ---------- 1. OBJETOS ----------
        titulo = Text(
            "Regla de los Signos",
            font_size=54, color="#1A3A5C", weight=BOLD,
        )
        titulo2 = Text(
            "de Descartes",
            font_size=54, color="#1A3A5C", weight=BOLD,
        )
        titulo_grupo = VGroup(titulo, titulo2).arrange(DOWN, center=True, buff=0.15)

        subtitulo = Tex(
            r"Una herramienta para determinar la naturaleza\\"
            r"de las raíces de un polinomio",
            tex_environment="center",
            font_size=35,
        )
        subtitulo.set_color("#4A6A8A")

        linea = Line(LEFT * 3.5, RIGHT * 3.5, color="#E88B8B", stroke_width=2)

        autor = Tex(
            r"Álgebra Superior $\cdot$ FES Acatlán - UNAM $\cdot$ Octubre 2026",
            tex_environment="center",
            font_size=30,
        )
        autor.set_color("#6A7A8A")

        polinomio = MathTex(
            r"f(t) = a_n t^n + a_{n-1} t^{n-1} + \cdots + a_1 t + a_0",
            color="#6A7A8A", font_size=60,
        )

        # ---------- 2. CONFIGURACIÓN (colores y posición) ----------
        # Título: arriba del centro
        titulo_grupo.move_to([0, 1.6, 0])

        # Subtítulo: debajo del título
        subtitulo.move_to([0, 0.2, 0])

        # Línea decorativa: debajo del subtítulo
        linea.move_to([0, -0.5, 0])

        # Autor: parte inferior de la pantalla
        autor.move_to([0, -3.2, 0])

        # Polinomio decorativo: muy abajo, como marca de agua
        polinomio.move_to([0, -1.8, 0])

        # ---------- 3. ANIMACIONES ----------
        # Aparece el título principal
        self.play(Write(titulo_grupo), run_time=2)
        self.wait(1)

        # Aparece el subtítulo
        self.play(FadeIn(subtitulo, shift=UP * 0.3), run_time=1)
        self.wait(1)

        # Aparece la línea decorativa
        self.play(Create(linea), run_time=0.8)
        self.wait(1)

        # Aparece la información del autor
        self.play(FadeIn(autor), run_time=1)
        self.wait(1)

        # Aparece el polinomio decorativo
        self.play(FadeIn(polinomio, scale=1.1), run_time=2)
        self.wait(30)

        # Desaparece todo
        self.play(FadeOut(titulo_grupo, subtitulo, linea, autor, polinomio), run_time=2)

# ============================================================
# ESCENA 2: RECORDATORIO — POLINOMIOS Y SUS RAÍCES
# ============================================================
class D02_Polinomios(CuadernoScene):
    def construct(self):
        # ---------- 1. OBJETOS ----------
        text1 = Text(
            "Regla de los Signos",
            font_size=42, color="#1A3A5C", weight=BOLD,
        )
        text2 = Text(
            "de Descartes",
            font_size=42, color="#1A3A5C", weight=BOLD,
        )
        texto_grupo1 = VGroup(text1, text2).arrange(DOWN, center=True, buff=0.15)

        subtitulo = Text(
            "Recordatorio: Polinomios y sus raíces",
            font_size=30, color="#1A3A5C", weight=BOLD,
        )

        definicion = Tex(
            r"Sea $k$ un campo. Un polinomio sobre $k$ es una función "
            r"$f: k \to k$ tal que:",
            tex_environment="center",
            font_size=40,
        )

        formula = MathTex(
            r"f(t) = a_n t^n + a_{n-1} t^{n-1} "
            r"+ \dots + a_1 t^{1} + a_0 t^{0}",
            font_size=55,
        )

        grado = Tex(
            r"\textbf{Grado:} mayor exponente de la variable "
            r"con coeficiente distinto de cero.",
            tex_environment="center",
            font_size=35,
        )

        raiz = MathTex(
            r"\alpha \in \mathbb{C} \text{ es raíz de } f "
            r"\iff f(\alpha) = 0",
            font_size=48,
        )

        # ---------- 2. CONFIGURACIÓN (colores y posición) ----------
        # Título: posición inicial (centro de la pantalla)
        texto_grupo1.move_to([0, 0, 0])

        # Título: versión final (esquina superior izquierda, más pequeño)
        texto_grupo1_final = texto_grupo1.copy().scale(0.6).move_to([-4.8, 3.5, 0])

        # Subtítulo de la escena
        subtitulo.move_to([0, 2.5, 0])

        # Definición
        definicion.move_to([0, 1.5, 0])
        definicion.set_color("#2A4A6A")

        # Fórmula general
        formula.move_to([0, 0.3, 0])
        formula.set_color("#1A3A5C")
        formula.set_color_by_tex("a_n t^n", RED)
        formula.set_color_by_tex("a_0", BLUE)

        # Grado
        grado.move_to([0, -1.2, 0])
        grado.set_color("#2A4A6A")

        # Raíz
        raiz.move_to([0, -2.6, 0])
        raiz.set_color("#2A4A6A")

        # ---------- 3. ANIMACIONES ----------
        # El título aparece grande en el centro
        self.play(Write(texto_grupo1), run_time=2)
        self.wait(2)

        # El título se encoge y se va a la esquina superior izquierda
        self.play(
            Transform(texto_grupo1, texto_grupo1_final),
            run_time=1.5,
        )
        self.wait(0.5)

        # Aparece el subtítulo de la escena
        self.play(Write(subtitulo), run_time=1.5)
        self.wait(1)

        # Aparece la definición de polinomio
        self.play(FadeIn(definicion, shift=DOWN * 0.3), run_time=1.5)
        self.wait(1)

        # Aparece la fórmula general
        self.play(Write(formula), run_time=2)
        self.wait(16.5)

        # Aparece la definición de grado
        self.play(FadeIn(grado, shift=DOWN * 0.3), run_time=1.5)
        self.wait(8)

        # Aparece la definición de raíz con su recuadro
        self.play(Write(raiz), run_time=2)
        caja_raiz = SurroundingRectangle(raiz, color="#E88B8B", buff=0.25)
        self.play(Create(caja_raiz), run_time=1)
        self.wait(17)

        # ---------- 4. CIERRE DE ESCENA ----------
        self.play(
            FadeOut(VGroup(
                texto_grupo1, subtitulo, definicion, formula,
                grado, raiz, caja_raiz,
            )),
            run_time=2,
        )

# ============================================================
# ESCENA 3: TIPOS DE RAÍCES
# ============================================================
class D03_TiposRaices(CuadernoScene):
    def construct(self):
        # ---------- 1. OBJETOS ----------
        text1 = Text("Los tipos", font_size=42, color="#1A3A5C", weight=BOLD)
        text2 = Text("de raíces",        font_size=42, color="#1A3A5C", weight=BOLD)
        texto_grupo1 = VGroup(text1, text2).arrange(DOWN, center=True, buff=0.15)

        subtitulo = Text(
            "¿Qué tipos de raíces puede tener un polinomio?",
            font_size=30, color="#1A3A5C", weight=BOLD,
        )

        reales = Tex(r"\textbf{1. Raíces reales}",
                     tex_environment="center", font_size=40)
        racionales = Tex(r"a) Racionales (ej. $4$, $\frac{1}{3}$, $-3$)",
                         tex_environment="center", font_size=40)
        irracionales = Tex(r"b) Irracionales (ej. $\sqrt{2}$, $\pi$, etc.)",
                           tex_environment="center", font_size=40)

        complejas = Tex(r"\textbf{2. Raíces complejas (ej. $\frac{1}{6} \pm \frac{\sqrt{86}}{6} i$)}",
                        tex_environment="center", font_size=40)

        nota = Tex(
            r"\textit{Las raíces reales también son complejas, "
            r"con parte imaginaria igual a cero.}",
            tex_environment="center", font_size=35,
        )

        # ---------- 2. CONFIGURACIÓN (colores y posición) ----------
        texto_grupo1.move_to([0, 0, 0])
        texto_grupo1_final = texto_grupo1.copy().scale(0.6).move_to([-4.8, 3.5, 0])

        subtitulo.move_to([0, 2.5, 0])

        # Bloque izquierdo (raíces reales) — acento TEAL
        reales.move_to([0, 1.5, 0])
        reales.set_color(TEAL)

        racionales.move_to([0, 0.5, 0])
        racionales.set_color("#2A4A6A")

        irracionales.move_to([0, -0.5, 0])
        irracionales.set_color("#2A4A6A")

        # Bloque derecho (raíces complejas) — acento RED
        complejas.move_to([0, -1.5, 0])
        complejas.set_color(RED)

        # Nota al pie — gris medio
        nota.move_to([0, -2.75, 0])
        nota.set_color("#6A7A8A")

        # ---------- 3. ANIMACIONES ----------
        self.play(Write(texto_grupo1), run_time=2)
        self.wait(5.5)

        self.play(Transform(texto_grupo1, texto_grupo1_final), run_time=1.5)
        self.wait(1)

        self.play(Write(subtitulo), run_time=1.5)
        self.wait(4)

        self.play(FadeIn(reales, shift=DOWN * 0.3), run_time=1.5)
        self.wait(4)

        self.play(FadeIn(racionales, shift=RIGHT * 0.3), run_time=1)
        self.wait(3)

        self.play(FadeIn(irracionales, shift=RIGHT * 0.3), run_time=1)
        self.wait(7)

        self.play(FadeIn(complejas, shift=DOWN * 0.3), run_time=1.5)
        self.wait(9)

        self.play(FadeIn(nota), run_time=1.5)
        self.wait(20)

        # ---------- 4. CIERRE ----------
        self.play(FadeOut(VGroup(texto_grupo1, subtitulo, reales, racionales,
                                 irracionales, complejas, nota)), run_time=3)

# ============================================================
# ESCENA 4: DOS TEOREMAS FUNDAMENTALES
# ============================================================
class D04_Teoremas(CuadernoScene):
    def construct(self):
        # ---------- 1. OBJETOS ----------
        text1 = Text("Antes de llegar", font_size=42, color="#1A3A5C", weight=BOLD)
        text2 = Text("a Descartes...",        font_size=42, color="#1A3A5C", weight=BOLD)
        texto_grupo1 = VGroup(text1, text2).arrange(DOWN, center=True, buff=0.15)

        subtitulo = Text(
            "Dos resultados que lo cambian todo",
            font_size=40, color="#1A3A5C", weight=BOLD,
        )

        tfa_titulo = Tex(r"\textbf{Teorema Fundamental del Álgebra}",
                         tex_environment="center", font_size=40)
        tfa_texto = Tex(
            r"Todo polinomio de grado $\geq 1$ sobre $\mathbb{C}$\\"
            r"tiene \textbf{al menos una raíz}.",
            tex_environment="center", font_size=40,
        )

        nraices_titulo = Tex(
            r"\textbf{Un polinomio de grado $n$ tiene exactamente $n$ raíces}",
            tex_environment="center", font_size=40,
        )
        nraices_texto = Tex(
            r"Contando cada raíz con su \textbf{multiplicidad}.",
            tex_environment="center", font_size=40,
        )

        # ---------- 2. CONFIGURACIÓN (colores y posición) ----------
        texto_grupo1.move_to([0, 0, 0])
        texto_grupo1_final = texto_grupo1.copy().scale(0.6).move_to([-4.8, 3.5, 0])

        subtitulo.move_to([0, 2.5, 0])

        # Bloque 1 — acento BLUE
        tfa_titulo.move_to([0, 1.3, 0])
        tfa_titulo.set_color(BLUE_D)

        tfa_texto.move_to([0, 0.2, 0])
        tfa_texto.set_color("#2A4A6A")

        # Bloque 2 — acento TEAL
        nraices_titulo.move_to([0, -1.2, 0])
        nraices_titulo.set_color(TEAL_D)

        nraices_texto.move_to([0, -2.2, 0])
        nraices_texto.set_color("#2A4A6A")

        # ---------- 3. ANIMACIONES ----------
        self.play(Write(texto_grupo1), run_time=2)
        self.wait(1.5)
        self.play(Transform(texto_grupo1, texto_grupo1_final), run_time=1.5)
        self.wait(1)

        self.play(Write(subtitulo), run_time=1)
        self.wait(0.5)

        # Bloque 1
        self.play(Write(tfa_titulo), run_time=1)
        self.wait(1)
        self.play(FadeIn(tfa_texto, shift=DOWN * 0.3), run_time=1.5)
        caja_tfa = SurroundingRectangle(tfa_texto, color=BLUE_D, buff=0.2)  # recuadro azul
        self.play(Create(caja_tfa), run_time=1)
        self.wait(18.5)

        # Bloque 2
        self.play(Write(nraices_titulo), run_time=1.8)
        self.wait(1.5)
        self.play(FadeIn(nraices_texto, shift=DOWN * 0.3), run_time=1.5)
        caja_n = SurroundingRectangle(nraices_texto, color=TEAL_D, buff=0.2)  # recuadro teal
        self.play(Create(caja_n), run_time=1)
        self.wait(24.2)

        # ---------- 4. CIERRE ----------
        self.play(FadeOut(VGroup(texto_grupo1, subtitulo, tfa_titulo, tfa_texto,
                                 caja_tfa, nraices_titulo, nraices_texto, caja_n)),
                  run_time=2)

# ============================================================
# ESCENA 5: EL PROBLEMA
# ============================================================
class D05_Problema(CuadernoScene):
    def construct(self):
        # ---------- 1. OBJETOS ----------
        text1 = Text("Entonces...", font_size=42, color="#1A3A5C", weight=BOLD)
        text2 = Text("El problema",        font_size=42, color="#1A3A5C", weight=BOLD)
        texto_grupo1 = VGroup(text1, text2).arrange(DOWN, center=True, buff=0.15)

        subtitulo = Text(
            "El problema: ¿cuántas raíces reales tiene?",
            font_size=30, color="#1A3A5C", weight=BOLD,
        )

        contexto = Tex(
            r"Un polinomio de grado $n$ tiene $n$ raíces complejas.\\"
            r"Pero ¿cuántas son \textbf{reales positivas} y "
            r"cuántas \textbf{reales negativas}?",
            tex_environment="center", font_size=40,
        )

        polinomio = MathTex(
            r"f(t) = t^5 - 3t^4 + 2t^3 - 5t^2 + t - 7",
            font_size=50,
        )

        pregunta = Tex(
            r"¿Existe una forma \textbf{rápida} de acotar el número\\"
            r"de raíces reales sin resolverlo?",
            tex_environment="center", font_size=40,
        )

        # ---------- 2. CONFIGURACIÓN (colores y posición) ----------
        texto_grupo1.move_to([0, 0, 0])
        texto_grupo1_final = texto_grupo1.copy().scale(0.6).move_to([-4.8, 3.5, 0])

        subtitulo.move_to([0, 2.5, 0])

        contexto.move_to([0, 1.3, 0])
        contexto.set_color("#2A4A6A")

        polinomio.move_to([0, -0.1, 0])
        polinomio.set_color("#1A3A5C")

        # Recuadro rojo suave alrededor del polinomio
        caja_pol = SurroundingRectangle(polinomio, color="#E88B8B", buff=0.25)

        pregunta.move_to([0, -1.9, 0])
        pregunta.set_color(RED_D)

        # ---------- 3. ANIMACIONES ----------
        self.play(Write(texto_grupo1), run_time=1)
        self.wait(1)
        self.play(Transform(texto_grupo1, texto_grupo1_final), run_time=1.5)
        self.wait(1)

        self.play(Write(subtitulo), run_time=1.5)
        self.wait(2)

        self.play(FadeIn(contexto, shift=DOWN * 0.3), run_time=1.5)
        self.wait(3)

        self.play(Write(polinomio), run_time=2)
        self.play(Create(caja_pol), run_time=1)
        self.wait(17)

        self.play(Write(pregunta), run_time=2)
        self.wait(18)

        # ---------- 4. CIERRE ----------
        self.play(FadeOut(VGroup(texto_grupo1, subtitulo, contexto, polinomio,
                                 caja_pol, pregunta)), run_time=2)

# ============================================================
# ESCENA 6: CAMBIO DE SIGNO
# ============================================================
class D06_CambioSigno(CuadernoScene):
    def construct(self):
        # ---------- 1. OBJETOS ----------
        text1 = Text("Conteo de cambio", font_size=42, color="#1A3A5C", weight=BOLD)
        text2 = Text("de signos",        font_size=42, color="#1A3A5C", weight=BOLD)
        texto_grupo1 = VGroup(text1, text2).arrange(DOWN, center=True, buff=0.15)

        subtitulo = Text(
            "Concepto clave: cambio de signo",
            font_size=30, color="#1A3A5C", weight=BOLD,
        )

        definicion = Tex(
            r"Hay un \textbf{cambio de signo} cuando dos términos "
            r"sucesivos\\ difieren en el signo de sus coeficientes.",
            tex_environment="center", font_size=40,
        )

        # Función auxiliar: construye el polinomio por piezas
        # para poder colorear cada término individualmente sin \textcolor.
        def make_polinomio(colores=None):
            partes = [
                r"f(t) = ",
                r"+t^4",
                r" - 3t^3",
                r" + 2t^2",
                r" + 5t",
                r" - 7",
            ]
            mob = MathTex(*partes, font_size=48)
            if colores is None:
                colores = [None] * len(partes)
            for i, c in enumerate(colores):
                mob[i].set_color(c if c is not None else "#1A3A5C")
            return mob

        # Polinomio base (todo en azul oscuro)
        ejemplo = make_polinomio()

        resultado = Tex(
            r"\textbf{Total: 3 cambios de signo}",
            tex_environment="center", font_size=40,
        )

        # ---------- 2. CONFIGURACIÓN ----------
        texto_grupo1.move_to([0, 0, 0])
        texto_grupo1_final = texto_grupo1.copy().scale(0.6).move_to([-4.8, 3.5, 0])

        subtitulo.move_to([0, 2.5, 0])

        definicion.move_to([0, 1.4, 0])
        definicion.set_color("#2A4A6A")

        ejemplo.move_to([0, 0.0, 0])

        resultado.move_to([0, -2.3, 0])
        resultado.set_color(RED_D)

        # ---------- 3. ANIMACIONES ----------
        self.play(Write(texto_grupo1), run_time=2)
        self.wait(1)
        self.play(Transform(texto_grupo1, texto_grupo1_final), run_time=1.5)
        self.wait(1)

        self.play(Write(subtitulo), run_time=1.5)
        self.wait(2)

        self.play(FadeIn(definicion, shift=DOWN * 0.3), run_time=1.5)
        self.wait(3)

        self.play(Write(ejemplo), run_time=2)
        self.wait(3)

        # Resaltado 1: +t^4 → -3t^3 (cambio) — ROJO
        res1 = make_polinomio([None, RED, RED, None, None, None])
        res1.move_to([0, 0.0, 0])
        self.play(Transform(ejemplo, res1), run_time=1.2)
        self.wait(1.5)

        # Resaltado 2: -3t^3 → +2t^2 (cambio) — NARANJA
        res2 = make_polinomio([None, None, ORANGE, ORANGE, None, None])
        res2.move_to([0, 0.0, 0])
        self.play(Transform(ejemplo, res2), run_time=1.2)
        self.wait(1.5)

        # Sin cambio: +2t^2 → +5t (mismo signo)
        res3 = make_polinomio()
        res3.move_to([0, 0.0, 0])
        self.play(Transform(ejemplo, res3), run_time=1.2)
        self.wait(1.5)

        # Resaltado 3: +5t → -7 (cambio) — TEAL
        res4 = make_polinomio([None, None, None, None, TEAL, TEAL])
        res4.move_to([0, 0.0, 0])
        self.play(Transform(ejemplo, res4), run_time=1.2)
        self.wait(2)

        self.play(Write(resultado), run_time=2)
        caja_res = SurroundingRectangle(resultado, color="#E88B8B", buff=0.25)
        self.play(Create(caja_res), run_time=1)
        self.wait(6.5)

        # ---------- 4. CIERRE ----------
        self.play(FadeOut(VGroup(texto_grupo1, subtitulo, definicion, ejemplo,
                                 resultado, caja_res)), run_time=2)

# ============================================================
# ESCENA 7: ENUNCIADO DE LA REGLA DE DESCARTES
# ============================================================
class D07_EnunciadoRegla(CuadernoScene):
    def construct(self):
        # ---------- 1. OBJETOS ----------
        text1 = Text("El enunciado", font_size=42, color="#1A3A5C", weight=BOLD)
        text2 = Text("y la regla",        font_size=42, color="#1A3A5C", weight=BOLD)
        texto_grupo1 = VGroup(text1, text2).arrange(DOWN, center=True, buff=0.15)

        subtitulo = Text(
            "Enunciado de la regla",
            font_size=30, color="#1A3A5C", weight=BOLD,
        )

        # Regla 1 — raíces positivas
        regla1_titulo = Tex(
            r"\textbf{1. Raíces positivas}",
            tex_environment="center", font_size=30,
        )
        regla1_texto = Tex(
            r"El número de raíces reales positivas de $f(t)$ es igual\\"
            r"al número de cambios de signo en $f(t)$, o menor\\"
            r"en una cantidad par.",
            tex_environment="center", font_size=26,
        )

        # Regla 2 — raíces negativas
        regla2_titulo = Tex(
            r"\textbf{2. Raíces negativas}",
            tex_environment="center", font_size=30,
        )
        regla2_texto = Tex(
            r"El número de raíces reales negativas de $f(t)$ es igual\\"
            r"al número de cambios de signo en $f(-t)$, o menor\\"
            r"en una cantidad par.",
            tex_environment="center", font_size=26,
        )

        # Nota
        nota = Tex(
            r"\textit{El polinomio debe estar ordenado en potencias "
            r"decrecientes y sin raíces nulas.}",
            tex_environment="center", font_size=35,
        )

        # ---------- 2. CONFIGURACIÓN ----------
        texto_grupo1.move_to([0, 0, 0])
        texto_grupo1_final = texto_grupo1.copy().scale(0.6).move_to([-4.8, 3.5, 0])

        subtitulo.move_to([0, 2.6, 0])

        # Regla 1 — acento BLUE
        regla1_titulo.move_to([-3.2, 0.6, 0])
        regla1_titulo.set_color(BLUE_D)

        regla1_texto.move_to([-3.2, -0.2, 0])
        regla1_texto.set_color("#2A4A6A")

        # Regla 2 — acento RED
        regla2_titulo.move_to([3.2, 0.6, 0])
        regla2_titulo.set_color(RED_D)

        regla2_texto.move_to([3.2, -0.2, 0])
        regla2_texto.set_color("#2A4A6A")

        # Nota al pie
        nota.move_to([0, -2.6, 0])
        nota.set_color("#6A7A8A")

        # ---------- 3. ANIMACIONES ----------
        self.play(Write(texto_grupo1), run_time=2)
        self.wait(1)
        self.play(Transform(texto_grupo1, texto_grupo1_final), run_time=1.5)
        self.wait(1)

        self.play(Write(subtitulo), run_time=1.5)
        self.wait(2)

        # Regla 1
        self.play(Write(regla1_titulo), run_time=1.5)
        self.wait(1)
        self.play(FadeIn(regla1_texto, shift=DOWN * 0.3), run_time=1.5)
        self.wait(15)

        # Regla 2
        self.play(Write(regla2_titulo), run_time=1.5)
        self.wait(1)
        self.play(FadeIn(regla2_texto, shift=DOWN * 0.3), run_time=1.5)
        self.wait(10)

        # Nota
        self.play(FadeIn(nota), run_time=1.5)
        self.wait(11.5)

        # ---------- 4. CIERRE ----------
        self.play(FadeOut(VGroup(texto_grupo1, subtitulo, regla1_titulo,
                                 regla1_texto, regla2_titulo, regla2_texto,
                                 nota)), run_time=2)

# ============================================================
# ESCENA 8: EJEMPLO 1 — RAÍCES POSITIVAS
# ============================================================
class D08_EjemploPositivas(CuadernoScene):
    def construct(self):
        # ---------- 1. OBJETOS ----------
        text1 = Text("Ejemplo", font_size=42, color="#1A3A5C", weight=BOLD)
        text2 = Text("# 1",        font_size=42, color="#1A3A5C", weight=BOLD)
        texto_grupo1 = VGroup(text1, text2).arrange(DOWN, center=True, buff=0.15)

        subtitulo = Text(
            "Raíces positivas",
            font_size=30, color="#1A3A5C", weight=BOLD,
        )

        polinomio = MathTex(
            r"P(t) = t^3 + t^2 - t - 1",
            font_size=52,
        )

        coefs = Tex(
            r"Coeficientes: $+1,\; +1,\; -1,\; -1$",
            tex_environment="center", font_size=40,
        )

        paso1 = Tex(
            r"$+1 \to +1$: no cambia",
            tex_environment="center", font_size=40,
        )
        paso2 = Tex(
            r"$+1 \to -1$: \textbf{sí cambia}",
            tex_environment="center", font_size=40,
        )
        paso3 = Tex(
            r"$-1 \to -1$: no cambia",
            tex_environment="center", font_size=40,
        )

        conclusion = Tex(
            r"\textbf{Exactamente 1 raíz real positiva}",
            tex_environment="center", font_size=40,
        )

        # ---------- 2. CONFIGURACIÓN ----------
        texto_grupo1.move_to([0, 0, 0])
        texto_grupo1_final = texto_grupo1.copy().scale(0.6).move_to([-4.8, 3.5, 0])

        subtitulo.move_to([0, 2.6, 0])

        polinomio.move_to([0, 1.5, 0])
        polinomio.set_color("#1A3A5C")

        coefs.move_to([0, 0.5, 0])
        coefs.set_color("#2A4A6A")

        # Los tres pasos en columna izquierda
        paso1.move_to([-3.0, -0.7, 0])
        paso1.set_color("#2A4A6A")

        paso2.move_to([-3.0, -1.5, 0])
        paso2.set_color(RED)   # resaltar el único cambio

        paso3.move_to([-3.0, -2.3, 0])
        paso3.set_color("#2A4A6A")

        # Conclusión en columna derecha
        conclusion.move_to([3.0, -1.5, 0])
        conclusion.set_color(TEAL_D)

        # ---------- 3. ANIMACIONES ----------
        self.play(Write(texto_grupo1), run_time=1)
        self.wait(1)
        self.play(Transform(texto_grupo1, texto_grupo1_final), run_time=1)
        self.wait(1)

        self.play(Write(subtitulo), run_time=0.5)
        self.wait(1)

        self.play(Write(polinomio), run_time=1)
        self.wait(2)

        self.play(FadeIn(coefs, shift=DOWN * 0.3), run_time=1.5)
        self.wait(3)

        self.play(FadeIn(paso1), run_time=1)
        self.wait(1.5)
        self.play(FadeIn(paso2), run_time=1)
        self.wait(2)
        self.play(FadeIn(paso3), run_time=1)
        self.wait(7)

        self.play(Write(conclusion), run_time=2)
        caja = SurroundingRectangle(conclusion, color="#E88B8B", buff=0.2)
        self.play(Create(caja), run_time=1)
        self.wait(16)

        # ---------- 4. CIERRE ----------
        self.play(FadeOut(VGroup(texto_grupo1, subtitulo, polinomio, coefs,
                                 paso1, paso2, paso3, conclusion, caja)),
                  run_time=2)

# ============================================================
# ESCENA 9: EJEMPLO 1 — RAÍCES NEGATIVAS
# ============================================================
class D09_EjemploNegativas(CuadernoScene):
    def construct(self):
        # ---------- 1. OBJETOS ----------
        text1 = Text("Ejemplo", font_size=42, color="#1A3A5C", weight=BOLD)
        text2 = Text("#2",        font_size=42, color="#1A3A5C", weight=BOLD)
        texto_grupo1 = VGroup(text1, text2).arrange(DOWN, center=True, buff=0.15)

        subtitulo = Text(
            "Raíces negativas",
            font_size=30, color="#1A3A5C", weight=BOLD,
        )

        original = MathTex(
            r"P(t) = t^3 + t^2 - t - 1",
            font_size=48,
        )

        sustitucion = MathTex(
            r"P(-t) = -t^3 + t^2 + t - 1",
            font_size=48,
        )

        coefs = Tex(
            r"Coeficientes de $P(-t)$: $-1,\; +1,\; +1,\; -1$",
            tex_environment="center", font_size=28,
        )

        pasos = VGroup(
            Tex(r"$-1 \to +1$: \textbf{sí cambia}", tex_environment="center", font_size=26),
            Tex(r"$+1 \to +1$: no cambia",         tex_environment="center", font_size=26),
            Tex(r"$+1 \to -1$: \textbf{sí cambia}", tex_environment="center", font_size=26),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)

        conclusion = Tex(
            r"\textbf{2 o 0 raíces reales negativas}",
            tex_environment="center", font_size=32,
        )

        # ---------- 2. CONFIGURACIÓN ----------
        texto_grupo1.move_to([0, 0, 0])
        texto_grupo1_final = texto_grupo1.copy().scale(0.6).move_to([-4.8, 3.5, 0])

        subtitulo.move_to([0, 2.6, 0])

        original.move_to([0, 1.7, 0])
        original.set_color("#1A3A5C")

        sustitucion.move_to([0, 0.7, 0])
        sustitucion.set_color(BLUE_D)   # azul porque es la sustitución

        coefs.move_to([0, -0.2, 0])
        coefs.set_color("#2A4A6A")

        pasos.move_to([-2.5, -1.6, 0])
        # los "sí cambia" en rojo, los "no cambia" en gris
        pasos[0].set_color(RED)
        pasos[1].set_color("#6A7A8A")
        pasos[2].set_color(RED)

        conclusion.move_to([2.8, -1.6, 0])
        conclusion.set_color(TEAL_D)

        # ---------- 3. ANIMACIONES ----------
        self.play(Write(texto_grupo1), run_time=2)
        self.wait(1)
        self.play(Transform(texto_grupo1, texto_grupo1_final), run_time=1.5)
        self.wait(1)

        self.play(Write(subtitulo), run_time=1.5)
        self.wait(2)

        self.play(Write(original), run_time=1.5)
        self.wait(2)

        # Transición: sustituir t por -t
        self.play(Transform(original, sustitucion), run_time=2)
        self.wait(17)

        self.play(FadeIn(coefs, shift=DOWN * 0.3), run_time=1.5)
        self.wait(4)

        self.play(FadeIn(pasos[0]), run_time=1)
        self.wait(2.5)
        self.play(FadeIn(pasos[1]), run_time=1)
        self.wait(2.5)
        self.play(FadeIn(pasos[2]), run_time=1)
        self.wait(4)

        self.play(Write(conclusion), run_time=2)
        caja = SurroundingRectangle(conclusion, color="#E88B8B", buff=0.2)
        self.play(Create(caja), run_time=1)
        self.wait(12)

        # ---------- 4. CIERRE ----------
        self.play(FadeOut(VGroup(texto_grupo1, subtitulo, original, coefs,
                                 pasos, conclusion, caja)), run_time=2)

# ============================================================
# ESCENA 10: VERIFICACIÓN GRÁFICA
# ============================================================
class D10_VerificacionGrafica(CuadernoScene):
    def construct(self):
        # ---------- 1. OBJETOS ----------
        text1 = Text("Comprobación", font_size=42, color="#1A3A5C", weight=BOLD)
        text2 = Text("mediante gráfica",        font_size=42, color="#1A3A5C", weight=BOLD)
        texto_grupo1 = VGroup(text1, text2).arrange(DOWN, center=True, buff=0.15)

        subtitulo = Text(
            "Verificación gráfica",
            font_size=30, color="#1A3A5C", weight=BOLD,
        )

        # Ejes
        ejes = Axes(
            x_range=[-6, 6, 1],
            y_range=[-6, 6, 1],
            x_length=5,
            y_length=4,
            axis_config={"color": "#6A7A8A", "include_numbers": True},
        )

        # Gráfica del polinomio
        grafica = ejes.plot(
            lambda t: t**3 + t**2 - t - 1,
            color="#1A3A5C",
            x_range=[-2, 2],
        )

        etiqueta_grafica = MathTex(
            r"P(t) = t^3 + t^2 - t - 1",
            font_size=36,
        )

        raiz_pos = Dot(
            ejes.c2p(1, 0),
            color=BLUE, radius=0.09,
        )
        raiz_neg = Dot(
            ejes.c2p(-1, 0),
            color=RED, radius=0.09,
        )

        etiqueta_pos = MathTex(r"t = 1", font_size=32, color=BLUE)
        etiqueta_neg = MathTex(r"t = -1 \; (\text{doble})", font_size=32, color=RED)

        conclusion = Tex(
            r"\textbf{1 positiva y 2 negativas (contando multiplicidad)}",
            tex_environment="center", font_size=28,
        )

        # ---------- 2. CONFIGURACIÓN ----------
        texto_grupo1.move_to([0, 0, 0])
        texto_grupo1_final = texto_grupo1.copy().scale(0.6).move_to([-4.8, 3.5, 0])

        subtitulo.move_to([-2, 2.6, 0])

        ejes.move_to([0.0, -0.05, 0])

        etiqueta_grafica.move_to([2.5, 1.0, 0])
        etiqueta_grafica.set_color("#1A3A5C")

        etiqueta_pos.next_to(raiz_pos, UP, buff=0.2).shift(RIGHT * 0.7)
        etiqueta_neg.next_to(raiz_neg, DOWN, buff=0.2).shift(LEFT * 1.5)

        conclusion.move_to([0, -2.5, 0])
        conclusion.set_color(TEAL_D)

        # ---------- 3. ANIMACIONES ----------
        self.play(Write(texto_grupo1), run_time=0.5)
        self.wait(0.5)
        self.play(Transform(texto_grupo1, texto_grupo1_final), run_time=0.5)
        self.wait(0.5)

        self.play(Write(subtitulo), run_time=0.5)
        self.wait(0.5)

        self.play(Create(ejes), run_time=1.5)
        self.wait(1)

        self.play(Create(grafica), run_time=2.5)
        self.wait(2)

        self.play(Write(etiqueta_grafica), run_time=1.5)
        self.wait(2)

        # Raíz positiva
        self.play(FadeIn(raiz_pos, scale=2), run_time=1)
        self.play(Write(etiqueta_pos), run_time=1)
        self.wait(5)

        # Raíz negativa
        self.play(FadeIn(raiz_neg, scale=2), run_time=1)
        self.play(Write(etiqueta_neg), run_time=1)
        self.wait(5)

        # Conclusión
        self.play(Write(conclusion), run_time=2)
        self.wait(14)

        # ---------- 4. CIERRE ----------
        self.play(FadeOut(VGroup(texto_grupo1, subtitulo, ejes, grafica,
                                 etiqueta_grafica, raiz_pos, raiz_neg,
                                 etiqueta_pos, etiqueta_neg, conclusion)),
                  run_time=2)

# ============================================================
# ESCENA 11: EJEMPLO 2 — MÚLTIPLES POSIBILIDADES
# ============================================================
class D11_Ejemplo2(CuadernoScene):
    def construct(self):
        # ---------- 1. OBJETOS ----------
        text1 = Text("Ejemplo", font_size=42, color="#1A3A5C", weight=BOLD)
        text2 = Text("particular",        font_size=42, color="#1A3A5C", weight=BOLD)
        texto_grupo1 = VGroup(text1, text2).arrange(DOWN, center=True, buff=0.15)

        subtitulo = Text(
            "Nuevo ejemplo: varias posibilidades",
            font_size=30, color="#1A3A5C", weight=BOLD,
        )

        original = MathTex(
            r"Q(t) = t^4 - 2t^3 - 3t^2 + 4t + 4",
            font_size=46,
        )

        pos_titulo = Tex(
            r"\textbf{Raíces positivas:} 2 cambios de signo",
            tex_environment="center", font_size=26,
        )
        pos_resultado = Tex(
            r"$\Rightarrow$ 2 o 0 raíces positivas",
            tex_environment="center", font_size=26,
        )

        neg_titulo = Tex(
            r"\textbf{Raíces negativas:} 2 cambios en $Q(-t)$",
            tex_environment="center", font_size=26,
        )
        neg_resultado = Tex(
            r"$\Rightarrow$ 2 o 0 raíces negativas",
            tex_environment="center", font_size=26,
        )

        # ---------- 2. CONFIGURACIÓN ----------
        texto_grupo1.move_to([0, 0, 0])
        texto_grupo1_final = texto_grupo1.copy().scale(0.6).move_to([-4.8, 3.5, 0])

        subtitulo.move_to([0, 2.6, 0])

        original.move_to([0, 1.6, 0])
        original.set_color("#1A3A5C")

        # Bloque positivo — azul
        pos_titulo.move_to([0, 0.4, 0])
        pos_titulo.set_color(BLUE_D)

        pos_resultado.move_to([0, -0.3, 0])
        pos_resultado.set_color(BLUE)

        # Bloque negativo — rojo
        neg_titulo.move_to([0, -1.3, 0])
        neg_titulo.set_color(RED_D)

        neg_resultado.move_to([0, -2.0, 0])
        neg_resultado.set_color(RED)

        # ---------- 3. ANIMACIONES ----------
        self.play(Write(texto_grupo1), run_time=2)
        self.wait(1)
        self.play(Transform(texto_grupo1, texto_grupo1_final), run_time=1.5)
        self.wait(1)

        self.play(Write(subtitulo), run_time=1.5)
        self.wait(2)

        self.play(Write(original), run_time=2)
        self.wait(22)

        self.play(FadeIn(pos_titulo, shift=DOWN * 0.3), run_time=1.5)
        self.wait(2)
        self.play(FadeIn(pos_resultado, shift=DOWN * 0.3), run_time=1.5)
        self.wait(12)

        self.play(FadeIn(neg_titulo, shift=DOWN * 0.3), run_time=1.5)
        self.wait(2)
        self.play(FadeIn(neg_resultado, shift=DOWN * 0.3), run_time=1.5)
        self.wait(12)

        # ---------- 4. CIERRE ----------
        self.play(FadeOut(VGroup(texto_grupo1, subtitulo, original,
                                 pos_titulo, pos_resultado,
                                 neg_titulo, neg_resultado)), run_time=2)

# ============================================================
# ESCENA 12: TABLA DE COMBINACIONES POSIBLES
# ============================================================
class D12_Tabla(CuadernoScene):
    def construct(self):
        # ---------- 1. OBJETOS ----------
        text1 = Text("Muestra de", font_size=42, color="#1A3A5C", weight=BOLD)
        text2 = Text("las posibles soluciones",        font_size=42, color="#1A3A5C", weight=BOLD)
        texto_grupo1 = VGroup(text1, text2).arrange(DOWN, center=True, buff=0.15)

        subtitulo = Text(
            "Todas las combinaciones posibles",
            font_size=30, color="#1A3A5C", weight=BOLD,
        )

        # Encabezados de la tabla
        encabezados = VGroup(
            Text("Positivas", font_size=22, color=WHITE, weight=BOLD),
            Text("Negativas", font_size=22, color=WHITE, weight=BOLD),
            Text("Complejas", font_size=22, color=WHITE, weight=BOLD),
            Text("Total",     font_size=22, color=WHITE, weight=BOLD),
        ).arrange(RIGHT, buff=1.2)
        caja_encabezado = SurroundingRectangle(
            encabezados, color=BLUE_D, fill_color=BLUE_D,
            fill_opacity=1, buff=0.15, corner_radius=0.05,
        )

        # Filas de datos
        filas = VGroup()
        datos = [("2", "2", "0", "4"),
                 ("2", "0", "2", "4"),
                 ("0", "2", "2", "4"),
                 ("0", "0", "4", "4")]
        for fila in datos:
            fila_grupo = VGroup(*[
                Text(celda, font_size=30, color="#2A4A6A")
                for celda in fila
            ]).arrange(RIGHT, buff=2)
            filas.add(fila_grupo)
        filas.arrange(DOWN, buff=0.25)

        nota = Tex(
            r"Las raíces complejas siempre vienen en pares.\\"
            r"Por eso la cantidad es par y la suma siempre es $n = 4$.",
            tex_environment="center", font_size=40,
        )

        # ---------- 2. CONFIGURACIÓN ----------
        texto_grupo1.move_to([0, 0, 0])
        texto_grupo1_final = texto_grupo1.copy().scale(0.6).move_to([-4.8, 3.5, 0])

        subtitulo.move_to([0, 2.6, 0])

        # Tabla: encabezado arriba y filas debajo
        caja_encabezado.move_to([0, 1.5, 0])
        encabezados.move_to(caja_encabezado.get_center())

        filas.move_to([0, 0.0, 0])

        nota.move_to([0, -2, 0])
        nota.set_color("#6A7A8A")

        # ---------- 3. ANIMACIONES ----------
        self.play(Write(texto_grupo1), run_time=2)
        self.wait(1)
        self.play(Transform(texto_grupo1, texto_grupo1_final), run_time=1.5)
        self.wait(1)

        self.play(Write(subtitulo), run_time=1.5)
        self.wait(2)

        # Encabezado
        self.play(FadeIn(caja_encabezado), FadeIn(encabezados), run_time=1.5)
        self.wait(1)

        # Filas una por una
        for fila in filas:
            self.play(FadeIn(fila, shift=DOWN * 0.2), run_time=0.8)
            self.wait(1)

        self.wait(2)

        # Nota final
        self.play(FadeIn(nota), run_time=1.5)
        self.wait(27)

        # ---------- 4. CIERRE ----------
        self.play(FadeOut(VGroup(texto_grupo1, subtitulo, caja_encabezado,
                                 encabezados, filas, nota)), run_time=2)

# ============================================================
# ESCENA 13: INTEGRACIÓN CON OTRAS TÉCNICAS
# ============================================================
class D13_Integracion(CuadernoScene):
    def construct(self):
        # ---------- 1. OBJETOS ----------
        text1 = Text("Integración con", font_size=42, color="#1A3A5C", weight=BOLD)
        text2 = Text("otros métodos",        font_size=42, color="#1A3A5C", weight=BOLD)
        texto_grupo1 = VGroup(text1, text2).arrange(DOWN, center=True, buff=0.15)

        subtitulo = Text(
            "Cómo se integra con otras técnicas",
            font_size=30, color="#1A3A5C", weight=BOLD,
        )

        pasos = VGroup(
            Tex(r"\textbf{1.} Usar Descartes para acotar positivas y negativas.",
                tex_environment="center", font_size=40),
            Tex(r"\textbf{2.} Enlistar las posibles raíces racionales.",
                tex_environment="center", font_size=40),
            Tex(r"\textbf{3.} Probar con división sintética.",
                tex_environment="center", font_size=40),
            Tex(r"\textbf{4.} Reducir el polinomio y repetir.",
                tex_environment="center", font_size=40),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)

        # ---------- 2. CONFIGURACIÓN ----------
        texto_grupo1.move_to([0, 0, 0])
        texto_grupo1_final = texto_grupo1.copy().scale(0.6).move_to([-4.8, 3.5, 0])

        subtitulo.move_to([0, 2.6, 0])

        pasos.move_to([0, 0.3, 0])

        # Colorear cada paso con un acento distinto
        pasos[0].set_color(BLUE_D)     # Descartes — azul
        pasos[1].set_color(TEAL_D)     # Racionales — teal
        pasos[2].set_color("#2A4A6A")  # División — gris azulado
        pasos[3].set_color(RED_D)      # Repetir — rojo

        # ---------- 3. ANIMACIONES ----------
        self.play(Write(texto_grupo1), run_time=2)
        self.wait(1)
        self.play(Transform(texto_grupo1, texto_grupo1_final), run_time=1.5)
        self.wait(1)

        self.play(Write(subtitulo), run_time=1.5)
        self.wait(6)

        for paso in pasos:
            self.play(FadeIn(paso, shift=RIGHT * 0.3), run_time=1)
            self.wait(4.5)

        self.wait(10)

        # ---------- 4. CIERRE ----------
        self.play(FadeOut(VGroup(texto_grupo1, subtitulo, pasos)), run_time=2)

# ============================================================
# ESCENA 14: CONCLUSIONES
# ============================================================
class D14_Conclusiones(CuadernoScene):
    def construct(self):
        # ---------- 1. OBJETOS ----------
        text1 = Text("Conclusión y comentarios", font_size=42, color="#1A3A5C", weight=BOLD)
        text2 = Text("finales",        font_size=42, color="#1A3A5C", weight=BOLD)
        texto_grupo1 = VGroup(text1, text2).arrange(DOWN, center=True, buff=0.15)

        subtitulo = Text(
            "Conclusiones",
            font_size=32, color="#1A3A5C", weight=BOLD,
        )

        puntos = VGroup(
            Tex(r"$\bullet$ Es una herramienta \textbf{rápida} y \textbf{sencilla}.",
                tex_environment="center", font_size=40),
            Tex(r"$\bullet$ \textbf{No da el número exacto}, sino las posibilidades.",
                tex_environment="center", font_size=40),
            Tex(r"$\bullet$ Es útil combinada con otras técnicas.",
                tex_environment="center", font_size=40),
            Tex(r"$\bullet$ Las raíces complejas vienen en pares.",
                tex_environment="center", font_size=40),
        ).arrange(DOWN, buff=0.45, aligned_edge=LEFT)

        # ---------- 2. CONFIGURACIÓN ----------
        texto_grupo1.move_to([0, 0, 0])
        texto_grupo1_final = texto_grupo1.copy().scale(0.6).move_to([-4.8, 3.5, 0])

        subtitulo.move_to([0, 2.6, 0])

        puntos.move_to([0, 0.2, 0])
        puntos.set_color("#2A4A6A")

        # ---------- 3. ANIMACIONES ----------
        self.play(Write(texto_grupo1), run_time=1)
        self.wait(0.5)
        self.play(Transform(texto_grupo1, texto_grupo1_final), run_time=0.5)
        self.wait(0.5)

        self.play(Write(subtitulo), run_time=1)
        self.wait(0.5)

        for punto in puntos:
            self.play(FadeIn(punto, shift=RIGHT * 0.3), run_time=1)
            self.wait(8)

        self.wait(2)

        # ---------- 4. CIERRE ----------
        self.play(FadeOut(VGroup(texto_grupo1, subtitulo, puntos)), run_time=2)
