# Matrices.py — Curso de Álgebra Superior: Matrices y Determinantes
import asyncio
import hashlib
import os
import tempfile
from pathlib import Path

from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.base import SpeechService
import edge_tts
from mutagen.mp3 import MP3


# ---------- Adaptador edge-tts para manim-voiceover ----------
class EdgeTTSService(SpeechService):
    def __init__(self, voice="es-MX-JorgeNeural", rate="+0%", volume="+0%", pitch="+0Hz", **kwargs):
        self.voice = voice
        self.rate = rate
        self.volume = volume
        self.pitch = pitch
        super().__init__(**kwargs)

    def generate_from_text(self, text, **kwargs):
        cache_dir = kwargs.get("cache_dir") or os.path.join(
            tempfile.gettempdir(), "manim_voiceover_edge_tts"
        )
        Path(cache_dir).mkdir(parents=True, exist_ok=True)
        text_hash = hashlib.md5(text.encode("utf-8")).hexdigest()[:16]
        audio_path = os.path.join(cache_dir, f"tts_{text_hash}.mp3")
        if not os.path.exists(audio_path):
            asyncio.run(self._generate_tts(text, audio_path))
        duration = MP3(audio_path).info.length
        return {
            "original_text": text,
            "generated_text": text,
            "original_audio": audio_path,
            "duration": duration,
        }

    async def _generate_tts(self, text, output_path):
        communicate = edge_tts.Communicate(
            text, voice=self.voice, rate=self.rate,
            volume=self.volume, pitch=self.pitch,
        )
        await communicate.save(output_path)

    def get_word_boundaries(self, json_path, **kwargs):
        return []


# ---------- Escena base con fondo de cuaderno + helper esperar ----------
class CuadernoScene(VoiceoverScene):
    def setup(self):
        super().setup()
        self.camera.background_color = WHITE
        self.cuadricula = NumberPlane(
            x_range=[-8, 8, 0.5], y_range=[-5, 5, 0.5],
            background_line_style={
                "stroke_color": "#A8C4DC", "stroke_width": 1, "stroke_opacity": 0.45,
            },
            axis_config={"stroke_opacity": 0},
        )
        self.add(self.cuadricula)
        self.margen = Line(
            start=[-6.2, -4, 0], end=[-6.2, 4, 0],
            color="#E88B8B", stroke_width=1.5, stroke_opacity=0.85,
        )
        self.add(self.margen)

    def esperar(self, duration):
        """wait seguro: solo espera si duration > 0."""
        if duration > 0.01:
            self.wait(duration)


# ---------- Escena 01: Portada ----------
class D01_Portada(CuadernoScene):
    def construct(self):
        titulo = Text("Álgebra Superior", font_size=42, color="#1A3A5C", weight=BOLD)
        titulo2 = Text("Matrices y Determinantes", font_size=42, color="#1A3A5C", weight=BOLD)
        titulo_grupo = VGroup(titulo, titulo2).arrange(DOWN, center=True, buff=0.15)
        titulo_grupo.scale_to_fit_width(12)

        linea = Line(LEFT * 4, RIGHT * 4, color="#E88B8B", stroke_width=2)

        matriz_deco = MathTex(
            r"A = \begin{bmatrix} a_{11} & a_{12} & a_{13} \\"
            r"a_{21} & a_{22} & a_{23} \\"
            r"a_{31} & a_{32} & a_{33} \end{bmatrix}",
            color="#6A7A8A", font_size=70,
        )

        titulo_grupo.move_to([0, 2.2, 0])
        linea.move_to([0, 0.9, 0])
        matriz_deco.move_to([0, -0.7, 0])

        self.set_speech_service(EdgeTTSService(voice="es-MX-JorgeNeural"))

        with self.voiceover(
            text="Bienvenidos a este material de Álgebra Superior. "
                 "El día de hoy vamos a meternos de lleno con las matrices "
                 "y los determinantes."
        ) as t:
            self.play(Write(titulo_grupo), run_time=min(t.duration, 2.5))
            self.esperar(t.duration - 2.5)

        with self.voiceover(
            text="Esto es material de la Universidad Nacional Autónoma de México, "
                 "de la Facultad de Estudios Superiores Acatlán, para la "
                 "Licenciatura en Matemáticas Aplicadas y Computación."
        ) as t:
            self.esperar(t.duration)

        with self.voiceover(
            text="La idea es ir paso a paso, con calma. Vamos a ver definiciones, "
                 "ejemplos, y bastantes trucos para que los cálculos no se hagan "
                 "tan pesados."
        ) as t:
            self.play(Create(linea), run_time=min(t.duration, 1))
            self.esperar(t.duration - 1)

        with self.voiceover(
            text="Fíjense en esta matriz de tres por tres que está aquí al centro. "
                 "Esa es la forma del corazón del tema. Todo lo que vamos a ver "
                 "gira alrededor de objetos como este."
        ) as t:
            self.play(FadeIn(matriz_deco), run_time=min(t.duration, 2))
            self.esperar(t.duration - 2)

        with self.voiceover(
            text="Así que acomódense, saquen papel y lápiz si pueden, y vamos "
                 "a empezar con todo."
        ) as t:
            self.esperar(t.duration)

        self.play(FadeOut(VGroup(titulo_grupo, linea, matriz_deco)), run_time=2)


# ---------- Escena 02a: ¿Qué es una matriz? ----------
class D02a_QueEsMatriz(CuadernoScene):
    def construct(self):
        titulo = Text("¿Qué es una matriz?", font_size=42, color="#1A3A5C", weight=BOLD)

        def_label = Text("Definición", font_size=26, color="#6A7A8A", weight=BOLD)

        definicion = Tex(
            r"Una matriz $A$ de orden $m \times n$ es un arreglo\\"
            r"rectangular de $m \cdot n$ n\'umeros, en $m$ filas\\"
            r"y $n$ columnas.",
            tex_environment="center", font_size=26,
        )
        definicion.set_color("#2A4A6A")

        notacion = MathTex(r"A = (a_{ij})_{m \times n}", font_size=48, color="#1A3A5C")

        indices_i = MathTex(r"i = 1,\, 2,\, \ldots,\, m", font_size=32, color="#4A6A8A")
        indices_j = MathTex(r"j = 1,\, 2,\, \ldots,\, n", font_size=32, color="#4A6A8A")
        indices_grupo = VGroup(indices_i, indices_j).arrange(RIGHT, buff=0.8)

        significado = Tex(
            r"$a_{ij}$ = entrada en la fila $i$, columna $j$",
            tex_environment="center", font_size=28,
        )
        significado.set_color("#4A6A8A")

        ejemplo = MathTex(
            r"A = \begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{bmatrix}",
            font_size=75, color="#2A4A6A",
        )

        entrada_label = MathTex(r"a_{23} = 6", font_size=40, color=RED)
        flecha = Arrow(
            start=RIGHT, end=LEFT, color=RED, stroke_width=3,
            max_tip_length_to_length_ratio=0.2,
        )
        recuadro_ejemplo = SurroundingRectangle(ejemplo, color="#E88B8B", buff=0.3)

        tipos_label = Text("Tipos especiales de matrices", font_size=28, color="#1A3A5C", weight=BOLD)
        tipos_l1 = Text("Nula  ·  Identidad  ·  Diagonal", font_size=26, color="#4A6A8A")
        tipos_l2 = Text("Triangular  ·  Transpuesta  ·  Simétrica", font_size=26, color="#4A6A8A")
        tipos_l3 = Text("Idempotente  ·  Ortogonal  ·  y más", font_size=26, color="#4A6A8A")
        tipos_grupo = VGroup(tipos_l1, tipos_l2, tipos_l3).arrange(DOWN, center=True, buff=0.18)

        titulo.move_to([0, 0, 0])
        titulo_final = titulo.copy().scale(0.7).move_to([0, 3.5, 0])
        def_label.move_to([-4.5, 2.7, 0])
        definicion.move_to([0, 1.8, 0])
        notacion.move_to([0, 0.5, 0])
        indices_grupo.move_to([0, -0.4, 0])
        significado.move_to([0, -1.2, 0])
        ejemplo.move_to([0, 0.0, 0])
        recuadro_ejemplo.move_to([0, 0.0, 0])
        entrada_label.move_to([3.8, -1.0, 0])
        flecha.put_start_and_end_on([2.6, -1.0, 0], [1.2, -0.35, 0])
        tipos_label.move_to([0, 2.6, 0])
        tipos_grupo.move_to([0, 1.0, 0])

        self.set_speech_service(EdgeTTSService(voice="es-MX-JorgeNeural"))

        with self.voiceover(text="Ok, vamos a ver qué es una matriz, pero de forma formal.") as t:
            self.play(Write(titulo), run_time=min(t.duration, 2))
            self.esperar(t.duration - 2)

        with self.voiceover(text="Empecemos con la definición.") as t:
            self.play(Transform(titulo, titulo_final), run_time=min(t.duration, 1.5))
            self.play(FadeIn(def_label), run_time=min(t.duration * 0.3, 0.6))
            self.esperar(t.duration - 2.1)

        with self.voiceover(
            text="Formalmente, una matriz A de orden m por n es un arreglo "
                 "rectangular de m por n números, organizados en m filas y n columnas."
        ) as t:
            self.play(FadeIn(definicion, shift=DOWN * 0.3), run_time=min(t.duration * 0.5, 2))
            self.esperar(t.duration - 2)

        with self.voiceover(
            text="A esto lo escribimos así: A igual a a sub i j, de orden m por n."
        ) as t:
            self.play(Write(notacion), run_time=min(t.duration * 0.6, 2))
            self.esperar(t.duration - 2)

        with self.voiceover(
            text="Donde i va desde uno hasta m, y j va desde uno hasta n. "
                 "Es decir, i recorre las filas y j recorre las columnas."
        ) as t:
            self.play(FadeIn(indices_grupo, shift=DOWN * 0.3), run_time=min(t.duration * 0.4, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="Entonces, a sub i j significa: la entrada que está en la fila i "
                 "y en la columna j. Esto lo vamos a usar todo el tiempo."
        ) as t:
            self.play(FadeIn(significado, shift=DOWN * 0.3), run_time=min(t.duration * 0.4, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="Veamos un ejemplo concreto. Esta es una matriz de dos por tres. "
                 "Tiene dos filas y tres columnas."
        ) as t:
            self.play(
                FadeOut(VGroup(def_label, definicion, notacion, indices_grupo, significado)),
                run_time=min(t.duration * 0.2, 1),
            )
            self.play(Write(ejemplo), run_time=min(t.duration * 0.4, 2))
            self.play(Create(recuadro_ejemplo), run_time=min(t.duration * 0.2, 1))
            self.esperar(t.duration - 4)

        with self.voiceover(
            text="Por ejemplo, la entrada a sub dos coma tres, es decir, fila dos, "
                 "columna tres, es el número seis."
        ) as t:
            self.play(FadeIn(entrada_label, shift=LEFT * 0.3), run_time=min(t.duration * 0.3, 1.2))
            self.play(GrowArrow(flecha), run_time=min(t.duration * 0.3, 1.2))
            self.esperar(t.duration - 2.4)

        with self.voiceover(
            text="Y ojo, existen muchísimos tipos especiales de matrices: la nula, "
                 "la identidad, la diagonal, la triangular, la transpuesta, la "
                 "simétrica, la idempotente, y varias más. Todas las iremos viendo."
        ) as t:
            self.play(
                FadeOut(VGroup(ejemplo, recuadro_ejemplo, entrada_label, flecha)),
                run_time=min(t.duration * 0.15, 1),
            )
            self.play(FadeIn(tipos_label), run_time=min(t.duration * 0.15, 1))
            self.play(FadeIn(tipos_grupo, shift=DOWN * 0.3), run_time=min(t.duration * 0.2, 1.2))
            self.esperar(t.duration - 3.2)

        self.play(FadeOut(VGroup(titulo, tipos_label, tipos_grupo)), run_time=2)


# ---------- Escena 03: Tipos de matrices ----------
class D03_TiposMatrices(CuadernoScene):
    def construct(self):
        titulo = Text("Tipos de matrices", font_size=42, color="#1A3A5C", weight=BOLD)

        cuad_nombre = Text("Matriz cuadrada", font_size=32, color="#1A3A5C", weight=BOLD)
        cuad_def = Tex(r"$m = n$: igual n\'umero de filas y columnas",
                       tex_environment="center", font_size=26)
        cuad_mat = Matrix([
            [r"a_{11}", r"a_{12}", r"a_{13}"],
            [r"a_{21}", r"a_{22}", r"a_{23}"],
            [r"a_{31}", r"a_{32}", r"a_{33}"],
        ], h_buff=1.2, v_buff=0.8)

        id_nombre = Text("Matriz identidad", font_size=32, color="#1A3A5C", weight=BOLD)
        id_simbolo = MathTex(r"I_n", font_size=38, color="#E88B8B")
        id_def = Tex(r"$I_{ij} = 1$ si $i = j$; \; $I_{ij} = 0$ si $i \neq j$",
                     tex_environment="center", font_size=24)
        id_mat = Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]], h_buff=1.0, v_buff=0.8)
        id_prop = Tex(r"$I_n \cdot A = A \cdot I_n = A$",
                      tex_environment="center", font_size=30)

        nul_nombre = Text("Matriz nula", font_size=32, color="#1A3A5C", weight=BOLD)
        nul_simbolo = MathTex(r"O", font_size=38, color="#E88B8B")
        nul_def = Tex(r"$O_{ij} = 0$ para todo $i$ y $j$",
                      tex_environment="center", font_size=24)
        nul_mat = Matrix([[0, 0, 0], [0, 0, 0], [0, 0, 0]], h_buff=1.0, v_buff=0.8)
        nul_prop = Tex(r"$A + O = O + A = A$",
                       tex_environment="center", font_size=30)

        diag_nombre = Text("Matriz diagonal", font_size=32, color="#1A3A5C", weight=BOLD)
        diag_def = Tex(r"$a_{ij} = 0$ siempre que $i \neq j$",
                       tex_environment="center", font_size=24)
        diag_mat = Matrix([[2, 0, 0], [0, 5, 0], [0, 0, -3]], h_buff=1.0, v_buff=0.8)
        diag_nota = Tex(r"$D = \mathrm{diag}(d_1, d_2, \ldots, d_n)$",
                        tex_environment="center", font_size=26)

        tsup_nombre = Text("Triangular superior", font_size=32, color="#1A3A5C", weight=BOLD)
        tsup_def = Tex(r"$a_{ij} = 0$ si $i > j$: ceros debajo de la diagonal",
                       tex_environment="center", font_size=24)
        tsup_mat = Matrix([[1, 2, 3], [0, 4, 5], [0, 0, 6]], h_buff=1.0, v_buff=0.8)

        tinf_nombre = Text("Triangular inferior", font_size=32, color="#1A3A5C", weight=BOLD)
        tinf_def = Tex(r"$a_{ij} = 0$ si $i < j$: ceros arriba de la diagonal",
                       tex_environment="center", font_size=24)
        tinf_mat = Matrix([[1, 0, 0], [2, 3, 0], [4, 5, 6]], h_buff=1.0, v_buff=0.8)

        trans_nombre = Text("Matriz transpuesta", font_size=32, color="#1A3A5C", weight=BOLD)
        trans_def = Tex(r"$(A^T)_{ij} = a_{ji}$: se intercambian filas por columnas",
                        tex_environment="center", font_size=24)
        trans_A = Matrix([[1, 2], [3, 4]], h_buff=1.0, v_buff=0.8)
        trans_At = Matrix([[1, 3], [2, 4]], h_buff=1.0, v_buff=0.8)
        trans_A_label = MathTex("A", font_size=36, color="#1A3A5C")
        trans_At_label = MathTex(r"A^T", font_size=36, color="#E88B8B")
        trans_arrow = MathTex(r"\longrightarrow", font_size=70, color="#E88B8B")

        sim_nombre = Text("Matriz simétrica", font_size=32, color="#1A3A5C", weight=BOLD)
        sim_def = Tex(r"$A = A^T$: coincide con su transpuesta",
                      tex_environment="center", font_size=24)
        sim_mat = Matrix([[1, 2, 3], [2, 4, 5], [3, 5, 6]], h_buff=1.0, v_buff=0.8)

        idem_nombre = Text("Matriz idempotente", font_size=32, color="#1A3A5C", weight=BOLD)
        idem_def = Tex(r"$A^2 = A$", tex_environment="center", font_size=40)
        idem_nota = Tex(r"Al multiplicarla por s\'i misma vuelve a dar $A$",
                        tex_environment="center", font_size=24)

        # --- Configuración ---
        titulo.move_to([0, 0, 0])
        titulo_final = titulo.copy().scale(0.7).move_to([0, 3.6, 0])

        cuad_nombre.move_to([0, 2.5, 0])
        cuad_def.move_to([0, 1.7, 0])
        cuad_def.set_color("#2A4A6A")
        cuad_mat.move_to([0, -0.1, 0])
        cuad_mat.set_color("#2A4A6A")
        cuad_diag_boxes = VGroup(*[
            SurroundingRectangle(cuad_mat.get_entries()[i], color="#E88B8B", buff=0.12)
            for i in [0, 4, 8]
        ])
        for b in cuad_diag_boxes:
            b.set_stroke(width=2.5)
        cuad_grupo = VGroup(cuad_mat, cuad_diag_boxes)

        id_nombre.move_to([-0.9, 2.5, 0])
        id_simbolo.move_to([1.1, 2.5, 0])
        id_def.move_to([0, 1.7, 0])
        id_def.set_color("#2A4A6A")
        id_mat.move_to([0, -0.1, 0])
        id_mat.set_color("#2A4A6A")
        for i in [1, 2, 3, 5, 6, 7]:
            id_mat.get_entries()[i].set_color("#6A7A8A")
        id_ones_boxes = VGroup(*[
            SurroundingRectangle(id_mat.get_entries()[i], color="#E88B8B", buff=0.12)
            for i in [0, 4, 8]
        ])
        for b in id_ones_boxes:
            b.set_stroke(width=2.5)
        id_grupo = VGroup(id_mat, id_ones_boxes)
        id_prop.move_to([0, -1.7, 0])
        id_prop.set_color("#2A4A6A")

        nul_nombre.move_to([-0.7, 2.5, 0])
        nul_simbolo.move_to([0.9, 2.5, 0])
        nul_def.move_to([0, 1.7, 0])
        nul_def.set_color("#2A4A6A")
        nul_mat.move_to([0, -0.1, 0])
        nul_mat.set_color("#6A7A8A")
        nul_prop.move_to([0, -1.7, 0])
        nul_prop.set_color("#2A4A6A")

        diag_nombre.move_to([0, 2.5, 0])
        diag_def.move_to([0, 1.7, 0])
        diag_def.set_color("#2A4A6A")
        diag_mat.move_to([0, -0.1, 0])
        diag_mat.set_color("#2A4A6A")
        for i in [1, 2, 3, 5, 6, 7]:
            diag_mat.get_entries()[i].set_color("#6A7A8A")
        diag_nota.move_to([0, -1.7, 0])
        diag_nota.set_color("#4A6A8A")

        tsup_nombre.move_to([0, 2.5, 0])
        tsup_def.move_to([0, 1.7, 0])
        tsup_def.set_color("#2A4A6A")
        tsup_mat.move_to([0, -0.1, 0])
        tsup_mat.set_color("#2A4A6A")
        for i in [3, 6, 7]:
            tsup_mat.get_entries()[i].set_color("#A8C4DC")

        tinf_nombre.move_to([0, 2.5, 0])
        tinf_def.move_to([0, 1.7, 0])
        tinf_def.set_color("#2A4A6A")
        tinf_mat.move_to([0, -0.1, 0])
        tinf_mat.set_color("#2A4A6A")
        for i in [1, 2, 5]:
            tinf_mat.get_entries()[i].set_color("#A8C4DC")

        trans_nombre.move_to([0, 2.5, 0])
        trans_def.move_to([0, 1.7, 0])
        trans_def.set_color("#2A4A6A")
        trans_A.move_to([-2.8, -0.2, 0])
        trans_A.set_color("#2A4A6A")
        trans_At.move_to([2.8, -0.2, 0])
        trans_At.set_color("#2A4A6A")
        trans_A_label.move_to([-2.8, 1.0, 0])
        trans_At_label.move_to([2.8, 1.0, 0])
        trans_arrow.move_to([0, -0.2, 0])

        sim_nombre.move_to([0, 2.5, 0])
        sim_def.move_to([0, 1.7, 0])
        sim_def.set_color("#2A4A6A")
        sim_mat.move_to([0, -0.1, 0])
        sim_mat.set_color("#2A4A6A")

        idem_nombre.move_to([0, 2.5, 0])
        idem_def.move_to([0, 0.5, 0])
        idem_def.set_color("#2A4A6A")
        idem_nota.move_to([0, -1.2, 0])
        idem_nota.set_color("#4A6A8A")

        # --- Animaciones ---
        self.set_speech_service(EdgeTTSService(voice="es-MX-JorgeNeural"))

        with self.voiceover(
            text="Ahora sí, vamos a ver todos los tipos especiales de matrices. "
                 "Los vamos a ver uno por uno, con su definición y con un ejemplo "
                 "para que quede clarísimo."
        ) as t:
            self.play(Write(titulo), run_time=min(t.duration, 2.5))
            self.esperar(t.duration - 2.5)

        with self.voiceover(text="Empecemos.") as t:
            self.play(Transform(titulo, titulo_final), run_time=min(t.duration, 1.5))
            self.esperar(t.duration - 1.5)

        # Cuadrada
        with self.voiceover(
            text="La matriz cuadrada. Es aquella que tiene el mismo número de filas "
                 "que de columnas, es decir, m igual a n."
        ) as t:
            self.play(FadeIn(cuad_nombre), run_time=min(t.duration * 0.25, 0.8))
            self.play(FadeIn(cuad_def, shift=DOWN * 0.3), run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 2.3)

        with self.voiceover(
            text="Aquí tienen un ejemplo de orden tres. Fíjense en los elementos "
                 "resaltados en rojo: son los de la diagonal principal, donde el "
                 "índice de fila y el de columna coinciden."
        ) as t:
            self.play(FadeIn(cuad_mat), run_time=min(t.duration * 0.3, 1.5))
            self.play(
                LaggedStart(*[Create(b) for b in cuad_diag_boxes], lag_ratio=0.3),
                run_time=min(t.duration * 0.4, 2),
            )
            self.esperar(t.duration - 3.5)

        with self.voiceover(text="Muy bien.") as t:
            self.play(FadeOut(VGroup(cuad_nombre, cuad_def, cuad_grupo)),
                      run_time=min(t.duration, 1.5))
            self.esperar(t.duration - 1.5)

        # Identidad
        with self.voiceover(
            text="La matriz identidad, que denotamos I sub n. Es una matriz cuadrada "
                 "donde todos los elementos de la diagonal son uno, y todos los de "
                 "afuera son cero."
        ) as t:
            self.play(FadeIn(id_nombre), FadeIn(id_simbolo), run_time=min(t.duration * 0.25, 1.0))
            self.play(FadeIn(id_def, shift=DOWN * 0.3), run_time=min(t.duration * 0.25, 1.2))
            self.play(FadeIn(id_mat), run_time=min(t.duration * 0.25, 1.2))
            self.esperar(t.duration - 3.4)

        with self.voiceover(
            text="Fíjense en la forma de escalera que hace. Es como el uno de la "
                 "multiplicación: si la multiplicas por cualquier matriz A del "
                 "mismo orden, te vuelve a dar A."
        ) as t:
            self.play(
                LaggedStart(*[Create(b) for b in id_ones_boxes], lag_ratio=0.3),
                run_time=min(t.duration * 0.4, 2),
            )
            self.play(FadeIn(id_prop, shift=DOWN * 0.3), run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 3.5)

        with self.voiceover(text="Siguiente.") as t:
            self.play(FadeOut(VGroup(id_nombre, id_simbolo, id_def, id_grupo, id_prop)),
                      run_time=min(t.duration, 1.5))
            self.esperar(t.duration - 1.5)

        # Nula
        with self.voiceover(
            text="La matriz nula, denotada O. Es aquella donde absolutamente todas "
                 "las entradas son cero."
        ) as t:
            self.play(FadeIn(nul_nombre), FadeIn(nul_simbolo), run_time=min(t.duration * 0.25, 1.0))
            self.play(FadeIn(nul_def, shift=DOWN * 0.3), run_time=min(t.duration * 0.25, 1.2))
            self.play(FadeIn(nul_mat), run_time=min(t.duration * 0.25, 1.2))
            self.esperar(t.duration - 3.4)

        with self.voiceover(
            text="Es el neutro aditivo: si le sumas la matriz nula a cualquier "
                 "matriz A, te vuelve a dar A."
        ) as t:
            self.play(FadeIn(nul_prop, shift=DOWN * 0.3), run_time=min(t.duration * 0.4, 1.8))
            self.esperar(t.duration - 1.8)

        with self.voiceover(text="Bien.") as t:
            self.play(FadeOut(VGroup(nul_nombre, nul_simbolo, nul_def, nul_mat, nul_prop)),
                      run_time=min(t.duration, 1.5))
            self.esperar(t.duration - 1.5)

        # Diagonal
        with self.voiceover(
            text="La matriz diagonal. Es una matriz cuadrada donde solo los "
                 "elementos de la diagonal principal pueden ser distintos de cero. "
                 "Todos los de afuera tienen que ser cero."
        ) as t:
            self.play(FadeIn(diag_nombre), run_time=min(t.duration * 0.2, 1.0))
            self.play(FadeIn(diag_def, shift=DOWN * 0.3), run_time=min(t.duration * 0.25, 1.2))
            self.play(FadeIn(diag_mat), run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 3.7)

        with self.voiceover(
            text="Fíjense que en la diagonal puede haber cualquier valor, no "
                 "necesariamente unos como en la identidad. Aquí tenemos dos, cinco "
                 "y menos tres. A este tipo de matrices también se les escribe "
                 "como diag de d uno hasta d n."
        ) as t:
            self.play(FadeIn(diag_nota, shift=DOWN * 0.3), run_time=min(t.duration * 0.25, 1.2))
            self.esperar(t.duration - 1.2)

        with self.voiceover(text="Vamos con las triangulares.") as t:
            self.play(FadeOut(VGroup(diag_nombre, diag_def, diag_mat, diag_nota)),
                      run_time=min(t.duration, 1.5))
            self.esperar(t.duration - 1.5)

        # Triangular superior
        with self.voiceover(
            text="La matriz triangular superior. Es una matriz cuadrada donde "
                 "todos los elementos debajo de la diagonal son cero. Es decir, "
                 "a sub i j es cero siempre que i sea mayor que j."
        ) as t:
            self.play(FadeIn(tsup_nombre), run_time=min(t.duration * 0.2, 1.0))
            self.play(FadeIn(tsup_def, shift=DOWN * 0.3), run_time=min(t.duration * 0.25, 1.2))
            self.play(FadeIn(tsup_mat), run_time=min(t.duration * 0.25, 1.2))
            self.esperar(t.duration - 3.4)

        with self.voiceover(
            text="Aquí pueden ver esos ceros, que los puse en un tono más clarito "
                 "para que se noten bien. Esa es la clave de la triangular superior: "
                 "todo lo de abajo se hace cero."
        ) as t:
            self.esperar(t.duration)

        with self.voiceover(text="Siguiente.") as t:
            self.play(FadeOut(VGroup(tsup_nombre, tsup_def, tsup_mat)),
                      run_time=min(t.duration, 1.5))
            self.esperar(t.duration - 1.5)

        # Triangular inferior
        with self.voiceover(
            text="La matriz triangular inferior es exactamente al revés: todos "
                 "los elementos arriba de la diagonal son cero. Es decir, a sub i j "
                 "es cero si i es menor que j."
        ) as t:
            self.play(FadeIn(tinf_nombre), run_time=min(t.duration * 0.2, 1.0))
            self.play(FadeIn(tinf_def, shift=DOWN * 0.3), run_time=min(t.duration * 0.25, 1.2))
            self.play(FadeIn(tinf_mat), run_time=min(t.duration * 0.25, 1.2))
            self.esperar(t.duration - 3.4)

        with self.voiceover(
            text="Igual, los ceros están marcados en azul claro, pero ahora arriba "
                 "de la diagonal."
        ) as t:
            self.esperar(t.duration)

        with self.voiceover(text="Muy bien.") as t:
            self.play(FadeOut(VGroup(tinf_nombre, tinf_def, tinf_mat)),
                      run_time=min(t.duration, 1.5))
            self.esperar(t.duration - 1.5)

        # Transpuesta
        with self.voiceover(
            text="Ahora la matriz transpuesta. Dada una matriz A, su transpuesta, "
                 "que escribimos A super T, se obtiene intercambiando filas por "
                 "columnas. Es decir, la entrada a sub i j de A transpuesta es "
                 "igual a la entrada a sub j i de A."
        ) as t:
            self.play(FadeIn(trans_nombre), run_time=min(t.duration * 0.15, 0.8))
            self.play(FadeIn(trans_def, shift=DOWN * 0.3), run_time=min(t.duration * 0.2, 1.0))
            self.esperar(t.duration - 1.8)

        with self.voiceover(
            text="Aquí tienen un ejemplo. A la izquierda está la matriz A, y a la "
                 "derecha su transpuesta. Fíjense cómo la primera fila de A se "
                 "convierte en la primera columna de A transpuesta, y la segunda "
                 "fila en la segunda columna."
        ) as t:
            self.play(FadeIn(trans_A), FadeIn(trans_A_label), run_time=min(t.duration * 0.2, 1.2))
            self.play(FadeIn(trans_arrow), run_time=min(t.duration * 0.15, 1.0))
            self.play(FadeIn(trans_At), FadeIn(trans_At_label), run_time=min(t.duration * 0.2, 1.2))
            self.esperar(t.duration - 3.4)

        with self.voiceover(
            text="Ojo: la transpuesta no requiere que la matriz sea cuadrada. Puede "
                 "ser rectangular sin problema."
        ) as t:
            self.esperar(t.duration)

        with self.voiceover(text="Bien.") as t:
            self.play(
                FadeOut(VGroup(trans_nombre, trans_def, trans_A, trans_A_label,
                               trans_At, trans_At_label, trans_arrow)),
                run_time=min(t.duration, 1.5),
            )
            self.esperar(t.duration - 1.5)

        # Simétrica
        with self.voiceover(
            text="La matriz simétrica. Una matriz cuadrada es simétrica si es igual "
                 "a su propia transpuesta. Es decir, A es igual a A super T. Eso "
                 "significa que a sub i j es igual a a sub j i para todo i y j."
        ) as t:
            self.play(FadeIn(sim_nombre), run_time=min(t.duration * 0.15, 0.8))
            self.play(FadeIn(sim_def, shift=DOWN * 0.3), run_time=min(t.duration * 0.2, 1.0))
            self.play(FadeIn(sim_mat), run_time=min(t.duration * 0.2, 1.2))
            self.esperar(t.duration - 3.0)

        with self.voiceover(
            text="Fíjense en el ejemplo. Si se paran en cualquier elemento y lo "
                 "reflejan respecto a la diagonal, encuentran exactamente el mismo "
                 "valor. La parte de arriba es un espejo de la de abajo. Por ejemplo, "
                 "el dos de hasta arriba a la derecha coincide con el dos de hasta "
                 "abajo a la izquierda."
        ) as t:
            self.esperar(t.duration)

        with self.voiceover(text="Siguiente.") as t:
            self.play(FadeOut(VGroup(sim_nombre, sim_def, sim_mat)),
                      run_time=min(t.duration, 1.5))
            self.esperar(t.duration - 1.5)

        # Idempotente
        with self.voiceover(
            text="Y por último, la matriz idempotente. Es una matriz que cumple "
                 "que A al cuadrado es igual a A. Es decir, si la multiplicas por "
                 "sí misma, te vuelve a dar la misma matriz."
        ) as t:
            self.play(FadeIn(idem_nombre), run_time=min(t.duration * 0.2, 1.0))
            self.play(FadeIn(idem_def, shift=DOWN * 0.3), run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 2.5)

        with self.voiceover(
            text="El ejemplo más sencillo es la identidad, porque I al cuadrado es "
                 "I. Pero hay muchísimas otras matrices que también cumplen esta "
                 "propiedad. Es un concepto importante en proyecciones y en álgebra "
                 "lineal aplicada."
        ) as t:
            self.play(FadeIn(idem_nota, shift=DOWN * 0.3), run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="Estos son los tipos más importantes. Hay otros, como las "
                 "ortogonales, las nilpotentes, las invertibles, y un largo etcétera. "
                 "Pero con estos ya tienen una base muy sólida para todo lo que viene."
        ) as t:
            self.play(FadeOut(VGroup(idem_nombre, idem_def, idem_nota)),
                      run_time=min(t.duration * 0.2, 1.0))
            self.esperar(t.duration - 1.0)

        self.play(FadeOut(titulo), run_time=2)

# ---------- Escena 04: Suma y resta de matrices ----------
class D04_SumaResta(CuadernoScene):
    def construct(self):
        # ---------- 1. OBJETOS ----------
        titulo = Text("Suma y resta de matrices", font_size=42, color="#1A3A5C", weight=BOLD)

        # ===== Bloque 1: condición =====
        cond_nombre = Text("Condición: mismo orden", font_size=30, color="#1A3A5C", weight=BOLD)
        cond_def = Tex(
            r"Para sumar o restar dos matrices, deben tener\\"
            r"el mismo n\'umero de filas y de columnas.",
            tex_environment="center", font_size=26,
        )
        cond_def.set_color("#2A4A6A")

        mat_2x2 = Matrix([[1, 2], [3, 4]], h_buff=0.7, v_buff=0.5)
        mat_2x2.set_color("#2A4A6A")
        mat_3x3 = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]], h_buff=0.7, v_buff=0.5)
        mat_3x3.set_color("#2A4A6A")

        orden_2 = MathTex(r"2 \times 2", font_size=30, color="#4A6A8A")
        orden_3 = MathTex(r"3 \times 3", font_size=30, color="#4A6A8A")
        x_roja = MathTex(r"\neq", font_size=50, color=RED)

        # ===== Bloque 2: definición suma =====
        sum_nombre = Text("Suma elemento a elemento", font_size=30, color="#1A3A5C", weight=BOLD)
        sum_def = Tex(
            r"$(A + B)_{ij} = a_{ij} + b_{ij}$",
            tex_environment="center", font_size=42,
        )
        sum_def.set_color("#1A3A5C")

        sum_nota = Tex(
            r"Cada entrada se suma con la que est\'a en la misma posici\'on",
            tex_environment="center", font_size=24,
        )
        sum_nota.set_color("#4A6A8A")

        # ===== Bloque 3: ejemplo suma =====
        A_s = Matrix([[2, 1], [0, 3]], h_buff=0.7, v_buff=0.5)
        B_s = Matrix([[1, 4], [2, -1]], h_buff=0.7, v_buff=0.5)
        C_s = Matrix([[3, 5], [2, 2]], h_buff=0.7, v_buff=0.5)
        A_s.set_color("#2A4A6A")
        B_s.set_color("#2A4A6A")
        C_s.set_color("#2A4A6A")

        sum_signo = MathTex("+", font_size=50, color="#1A3A5C")
        eq_signo = MathTex("=", font_size=50, color="#1A3A5C")

        label_A = MathTex("A", font_size=36, color="#1A3A5C")
        label_B = MathTex("B", font_size=36, color="#1A3A5C")
        label_C = MathTex("C", font_size=36, color="#1A3A5C")

        calc_s = MathTex(
            r"a_{11} + b_{11} = 2 + 1 = 3",
            font_size=32, color="#E88B8B",
        )

        # Resaltados de ejemplo (se crearán después de posicionar)
        # ===== Bloque 4: definición resta =====
        res_nombre = Text("Resta elemento a elemento", font_size=30, color="#1A3A5C", weight=BOLD).move_to([0, 0.5, 0])
        res_def = Tex(
            r"$(A - B)_{ij} = a_{ij} - b_{ij}$",
            tex_environment="center", font_size=42,
        )
        res_def.set_color("#1A3A5C")

        # ===== Bloque 5: ejemplo resta =====
        A_r = Matrix([[5, 2], [1, 4]], h_buff=0.7, v_buff=0.5)
        B_r = Matrix([[3, 1], [0, 2]], h_buff=0.7, v_buff=0.5)
        C_r = Matrix([[2, 1], [1, 2]], h_buff=0.7, v_buff=0.5)
        A_r.set_color("#2A4A6A")
        B_r.set_color("#2A4A6A")
        C_r.set_color("#2A4A6A")

        res_signo = MathTex("-", font_size=50, color="#1A3A5C")
        eq_signo_r = MathTex("=", font_size=50, color="#1A3A5C")

        label_A_r = MathTex("A", font_size=36, color="#1A3A5C")
        label_B_r = MathTex("B", font_size=36, color="#1A3A5C")
        label_C_r = MathTex("C", font_size=36, color="#1A3A5C")

        calc_r = MathTex(
            r"a_{11} - b_{11} = 5 - 3 = 2",
            font_size=32, color="#E88B8B",
        )

        # ===== Bloque 6: propiedades =====
        prop_nombre = Text("Propiedades", font_size=30, color="#1A3A5C", weight=BOLD)
        prop_c = Tex(r"Conmutativa: $A + B = B + A$",
                     tex_environment="center", font_size=26)
        prop_a = Tex(r"Asociativa: $(A + B) + C = A + (B + C)$",
                     tex_environment="center", font_size=26)
        prop_n = Tex(r"Neutro: $A + O = A$",
                     tex_environment="center", font_size=26)
        prop_i = Tex(r"Inverso: $A + (-A) = O$",
                     tex_environment="center", font_size=26)
        for p in [prop_c, prop_a, prop_n, prop_i]:
            p.set_color("#2A4A6A")
        props = VGroup(prop_c, prop_a, prop_n, prop_i).arrange(DOWN, center=True, buff=0.25)

        # ---------- 2. CONFIGURACIÓN ----------
        titulo.move_to([0, 0, 0])
        titulo_final = titulo.copy().scale(0.7).move_to([0, 3.6, 0])

        # Bloque 1
        cond_nombre.move_to([0, 2.6, 0])
        cond_def.move_to([0, 1.8, 0])
        mat_2x2.move_to([-3.0, -0.2, 0])
        orden_2.move_to([-3.0, -1.3, 0])
        x_roja.move_to([0, -0.2, 0])
        mat_3x3.move_to([3.0, -0.2, 0])
        orden_3.move_to([3.0, -1.4, 0])

        # Bloque 2
        sum_nombre.move_to([0, 2.6, 0])
        sum_def.move_to([0, 1.5, 0])
        sum_nota.move_to([0, 0.6, 0])

        # Bloque 3
        A_s.move_to([-3.4, -0.5, 0])
        sum_signo.move_to([-1.8, -0.5, 0])
        B_s.move_to([-0.2, -0.5, 0])
        eq_signo.move_to([1.5, -0.5, 0])
        C_s.move_to([3.2, -0.5, 0])
        label_A.move_to([-3.4, 0.6, 0])
        label_B.move_to([-0.2, 0.6, 0])
        label_C.move_to([3.2, 0.6, 0])
        calc_s.move_to([0, 1.6, 0])

        # Bloque 5
        A_r.move_to([-3.4, -0.5, 0])
        res_signo.move_to([-1.8, -0.5, 0])
        B_r.move_to([-0.2, -0.5, 0])
        eq_signo_r.move_to([1.5, -0.5, 0])
        C_r.move_to([3.2, -0.5, 0])
        label_A_r.move_to([-3.4, 0.6, 0])
        label_B_r.move_to([-0.2, 0.6, 0])
        label_C_r.move_to([3.2, 0.6, 0])
        calc_r.move_to([0, 1.6, 0])

        # Bloque 6
        prop_nombre.move_to([0, 2.6, 0])
        props.move_to([0, 0.6, 0])

        # ---------- 3. ANIMACIONES ----------
        self.set_speech_service(EdgeTTSService(voice="es-MX-JorgeNeural"))

        # ==== Intro ====
        with self.voiceover(
            text="Ahora vamos a ver cómo se suman y cómo se restan las matrices."
        ) as t:
            self.play(Write(titulo), run_time=min(t.duration, 2.5))
            self.esperar(t.duration - 2.5)

        with self.voiceover(text="Antes que nada, una condición fundamental.") as t:
            self.play(Transform(titulo, titulo_final), run_time=min(t.duration, 1.5))
            self.esperar(t.duration - 1.5)

        # ==== Bloque 1: condición ====
        with self.voiceover(
            text="Para poder sumar o restar dos matrices, necesitamos que tengan "
                 "exactamente el mismo orden. Es decir, el mismo número de filas "
                 "y el mismo número de columnas."
        ) as t:
            self.play(FadeIn(cond_nombre), run_time=min(t.duration * 0.2, 1.0))
            self.play(FadeIn(cond_def, shift=DOWN * 0.3), run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 2.5)

        with self.voiceover(
            text="Por ejemplo, no podemos sumar una matriz de dos por dos con una "
                 "de tres por tres. Simplemente no está definido, porque no hay "
                 "una correspondencia clara entre sus entradas."
        ) as t:
            self.play(FadeIn(mat_2x2), FadeIn(orden_2), run_time=min(t.duration * 0.15, 0.8))
            self.play(FadeIn(x_roja), run_time=min(t.duration * 0.1, 0.5))
            self.play(FadeIn(mat_3x3), FadeIn(orden_3), run_time=min(t.duration * 0.15, 0.8))
            self.esperar(t.duration - 2.6)

        with self.voiceover(text="Muy bien.") as t:
            self.play(FadeOut(VGroup(cond_nombre, cond_def, mat_2x2, mat_3x3,
                                     orden_2, orden_3, x_roja)),
                      run_time=min(t.duration, 1.5))
            self.esperar(t.duration - 1.5)

        # ==== Bloque 2: definición suma ====
        with self.voiceover(
            text="Bien, suponiendo que sí tienen el mismo orden, la suma se hace "
                 "elemento a elemento. Es decir, cada entrada de A se suma con la "
                 "entrada que está en la misma posición en B."
        ) as t:
            self.play(FadeIn(sum_nombre), run_time=min(t.duration * 0.2, 1.0))
            self.play(FadeIn(sum_def, shift=DOWN * 0.3), run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 2.5)

        with self.voiceover(
            text="Formalmente, la entrada i j de A más B es igual a la entrada i j "
                 "de A más la entrada i j de B."
        ) as t:
            self.play(FadeIn(sum_nota, shift=DOWN * 0.3), run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(text="Veamos un ejemplo.") as t:
            self.play(FadeOut(VGroup(sum_nombre, sum_def, sum_nota)),
                      run_time=min(t.duration, 1.5))
            self.esperar(t.duration - 1.5)

        # ==== Bloque 3: ejemplo suma ====
        with self.voiceover(
            text="Aquí tenemos dos matrices de dos por dos, A y B. Vamos a "
                 "sumarlas entrada por entrada."
        ) as t:
            self.play(FadeIn(label_A), FadeIn(A_s), run_time=min(t.duration * 0.15, 1.0))
            self.play(FadeIn(sum_signo), run_time=min(t.duration * 0.1, 0.5))
            self.play(FadeIn(label_B), FadeIn(B_s), run_time=min(t.duration * 0.15, 1.0))
            self.esperar(t.duration - 2.5)

        with self.voiceover(
            text="Por ejemplo, la entrada de arriba a la izquierda: a uno uno, que "
                 "es dos, más b uno uno, que es uno, nos da tres."
        ) as t:
            self.play(FadeIn(eq_signo), FadeIn(label_C), FadeIn(C_s),
                      run_time=min(t.duration * 0.15, 1.0))
            self.esperar(t.duration - 1.0)

        with self.voiceover(
            text="Y así con todas las demás entradas. Fila uno columna dos: uno "
                 "más cuatro es cinco. Fila dos columna uno: cero más dos es dos. "
                 "Y fila dos columna dos: tres más menos uno es dos."
        ) as t:
            # Resaltar a11, b11, c11
            rects = VGroup()
            for mat in [A_s, B_s, C_s]:
                rects.add(SurroundingRectangle(mat.get_entries()[0], color=RED, buff=0.1))
            self.play(FadeIn(calc_s), run_time=min(t.duration * 0.1, 0.8))
            self.play(*[Create(r) for r in rects], run_time=min(t.duration * 0.1, 0.8))
            self.esperar(t.duration * 0.2)

            # Recorrer las otras 3 entradas
            for idx in [1, 2, 3]:
                rects_new = VGroup()
                for mat in [A_s, B_s, C_s]:
                    rects_new.add(SurroundingRectangle(mat.get_entries()[idx],
                                                       color=RED, buff=0.1))
                self.play(
                    FadeOut(rects),
                    *[Create(r) for r in rects_new],
                    run_time=min(t.duration * 0.08, 0.5),
                )
                rects = rects_new
                self.esperar(t.duration * 0.1)

            self.play(FadeOut(rects), FadeOut(calc_s), run_time=0.5)
            self.esperar(t.duration * 0.1)

        with self.voiceover(text="Perfecto. Esa es la suma.") as t:
            self.play(
                FadeOut(VGroup(label_A, A_s, sum_signo, label_B, B_s,
                               eq_signo, label_C, C_s)),
                run_time=min(t.duration, 1.5),
            )
            self.esperar(t.duration - 1.5)

        # ==== Bloque 4: definición resta ====
        with self.voiceover(
            text="La resta funciona exactamente igual, pero restando las entradas "
                 "correspondientes. La entrada i j de A menos B es igual a la "
                 "entrada i j de A menos la entrada i j de B."
        ) as t:
            self.play(FadeIn(res_nombre), run_time=min(t.duration * 0.2, 1.0))
            self.play(FadeIn(res_def, shift=DOWN * 0.3), run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 2.5)

        with self.voiceover(text="Veamos un ejemplo rápido.") as t:
            self.play(FadeOut(VGroup(res_nombre, res_def)), run_time=min(t.duration, 1.0))
            self.esperar(t.duration - 1.0)

        # ==== Bloque 5: ejemplo resta ====
        with self.voiceover(
            text="Tenemos A y B de nuevo. Ahora restamos."
        ) as t:
            self.play(FadeIn(label_A_r), FadeIn(A_r), run_time=min(t.duration * 0.15, 0.8))
            self.play(FadeIn(res_signo), run_time=min(t.duration * 0.1, 0.5))
            self.play(FadeIn(label_B_r), FadeIn(B_r), run_time=min(t.duration * 0.15, 0.8))
            self.esperar(t.duration - 2.1)

        with self.voiceover(
            text="Por ejemplo, a uno uno menos b uno uno: cinco menos tres, es dos. "
                 "Y así con las demás entradas. El resultado es esta nueva matriz C."
        ) as t:
            self.play(FadeIn(eq_signo_r), FadeIn(label_C_r), FadeIn(C_r),
                      run_time=min(t.duration * 0.2, 1.2))
            rects_r = VGroup()
            for mat in [A_r, B_r, C_r]:
                rects_r.add(SurroundingRectangle(mat.get_entries()[0], color=RED, buff=0.1))
            self.play(FadeIn(calc_r), run_time=min(t.duration * 0.1, 0.8))
            self.play(*[Create(r) for r in rects_r], run_time=min(t.duration * 0.1, 0.8))
            self.esperar(t.duration * 0.3)
            self.play(FadeOut(rects_r), FadeOut(calc_r), run_time=0.5)

        with self.voiceover(text="Bien.") as t:
            self.play(
                FadeOut(VGroup(label_A_r, A_r, res_signo, label_B_r, B_r,
                               eq_signo_r, label_C_r, C_r)),
                run_time=min(t.duration, 1.5),
            )
            self.esperar(t.duration - 1.5)

        # ==== Bloque 6: propiedades ====
        with self.voiceover(
            text="La suma de matrices cumple varias propiedades muy parecidas a "
                 "las de los números. Es conmutativa, es decir, A más B es igual "
                 "a B más A."
        ) as t:
            self.play(FadeIn(prop_nombre), run_time=min(t.duration * 0.2, 1.0))
            self.play(FadeIn(prop_c, shift=DOWN * 0.3), run_time=min(t.duration * 0.3, 1.2))
            self.esperar(t.duration - 2.2)

        with self.voiceover(
            text="Es asociativa: da igual si sumas primero A con B, o B con C."
        ) as t:
            self.play(FadeIn(prop_a, shift=DOWN * 0.3), run_time=min(t.duration * 0.3, 1.2))
            self.esperar(t.duration - 1.2)

        with self.voiceover(
            text="Tiene un elemento neutro, que es la matriz nula: si le sumas la "
                 "matriz nula a cualquier matriz, te vuelve a dar la misma."
        ) as t:
            self.play(FadeIn(prop_n, shift=DOWN * 0.3), run_time=min(t.duration * 0.3, 1.2))
            self.esperar(t.duration - 1.2)

        with self.voiceover(
            text="Y cada matriz tiene un inverso aditivo: si le sumas su negativa, "
                 "te da la matriz nula."
        ) as t:
            self.play(FadeIn(prop_i, shift=DOWN * 0.3), run_time=min(t.duration * 0.3, 1.2))
            self.esperar(t.duration - 1.2)

        with self.voiceover(
            text="Estas propiedades nos van a servir mucho cuando empecemos a "
                 "resolver sistemas de ecuaciones."
        ) as t:
            self.esperar(t.duration)

        # ---------- 4. CIERRE ----------
        self.play(FadeOut(VGroup(titulo, prop_nombre, props)), run_time=2)


# ---------- Escena 05: Multiplicación por escalar ----------
class D05_MultiplicacionEscalar(CuadernoScene):
    def construct(self):
        # ---------- 1. OBJETOS ----------
        titulo = Text("Multiplicación por escalar", font_size=42, color="#1A3A5C", weight=BOLD)

        # ===== Bloque 1: definición =====
        def_nombre = Text("Definición", font_size=30, color="#1A3A5C", weight=BOLD)
        def_formula = MathTex(
            r"(\alpha A)_{ij} = \alpha \cdot a_{ij}",
            font_size=52, color="#1A3A5C",
        )
        def_nota = Tex(
            r"Cada entrada de $A$ se multiplica por el escalar $\alpha$",
            tex_environment="center", font_size=26,
        )
        def_nota.set_color("#4A6A8A")

        aclara = Text("α es un número real (escalar)", font_size=24, color="#6A7A8A", slant=ITALIC)

        # ===== Bloque 2: ejemplo =====
        ej_nombre = Text("Ejemplo", font_size=30, color="#1A3A5C", weight=BOLD)

        alpha = MathTex(r"3", font_size=50, color=RED)
        punto = MathTex(r"\cdot", font_size=50, color="#1A3A5C")

        A_mat = Matrix([[2, 1], [0, 3]], h_buff=0.7, v_buff=0.5)
        A_mat.set_color("#2A4A6A")
        label_A = MathTex("A", font_size=36, color="#1A3A5C")

        eq = MathTex("=", font_size=50, color="#1A3A5C")

        C_mat = Matrix([[6, 3], [0, 9]], h_buff=0.7, v_buff=0.5)
        C_mat.set_color("#2A4A6A")
        label_C = MathTex(r"3A", font_size=36, color="#E88B8B")

        calc = MathTex(r"3 \cdot 2 = 6", font_size=30, color=RED)

        # ===== Bloque 3: propiedades =====
        prop_nombre = Text("Propiedades", font_size=30, color="#1A3A5C", weight=BOLD)
        p1 = Tex(r"$\alpha(A + B) = \alpha A + \alpha B$",
                 tex_environment="center", font_size=28)
        p2 = Tex(r"$(\alpha + \beta)A = \alpha A + \beta A$",
                 tex_environment="center", font_size=28)
        p3 = Tex(r"$\alpha(\beta A) = (\alpha\beta)A$",
                 tex_environment="center", font_size=28)
        p4 = Tex(r"$1 \cdot A = A$",
                 tex_environment="center", font_size=28)
        for p in [p1, p2, p3, p4]:
            p.set_color("#2A4A6A")
        props = VGroup(p1, p2, p3, p4).arrange(DOWN, center=True, buff=0.28)

        # ===== Cierre nota =====
        nota_final = Tex(
            r"Multiplicar por escalar \textbf{escala} toda la matriz",
            tex_environment="center", font_size=28,
        )
        nota_final.set_color("#4A6A8A")

        # ---------- 2. CONFIGURACIÓN ----------
        titulo.move_to([0, 0, 0])
        titulo_final = titulo.copy().scale(0.7).move_to([0, 3.6, 0])

        # Bloque 1
        def_nombre.move_to([0, 2.6, 0])
        def_formula.move_to([0, 1.2, 0])
        def_nota.move_to([0, 0.0, 0])
        aclara.move_to([0, -0.9, 0])

        # Bloque 2
        ej_nombre.move_to([0, 2.6, 0])
        alpha.move_to([-4.5, -0.1, 0])
        punto.move_to([-3.4, -0.1, 0])
        label_A.move_to([-2.6, 0.9, 0])
        A_mat.move_to([-2.4, -0.1, 0])
        eq.move_to([-0.7, -0.1, 0])
        label_C.move_to([1.0, 0.9, 0])
        C_mat.move_to([1.2, -0.1, 0])
        calc.move_to([0, 1.7, 0])

        # Bloque 3
        prop_nombre.move_to([0, 2.6, 0])
        props.move_to([0, 0.6, 0])

        # Cierre
        nota_final.move_to([0, 0.0, 0])

        # ---------- 3. ANIMACIONES ----------
        self.set_speech_service(EdgeTTSService(voice="es-MX-JorgeNeural"))

        # ==== Intro ====
        with self.voiceover(
            text="Ahora vamos a ver la multiplicación de una matriz por un escalar."
        ) as t:
            self.play(Write(titulo), run_time=min(t.duration, 2.5))
            self.esperar(t.duration - 2.5)

        with self.voiceover(text="Empecemos con la definición.") as t:
            self.play(Transform(titulo, titulo_final), run_time=min(t.duration, 1.5))
            self.play(FadeIn(def_nombre), run_time=min(t.duration * 0.25, 0.8))
            self.esperar(t.duration - 2.3)

        # ==== Bloque 1: definición ====
        with self.voiceover(
            text="Dada una matriz A y un número real, que llamamos escalar y "
                 "denotamos con la letra griega alfa, el producto alfa por A se "
                 "calcula multiplicando cada entrada de A por ese escalar."
        ) as t:
            self.play(FadeIn(def_formula, shift=DOWN * 0.3), run_time=min(t.duration * 0.25, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="Formalmente, la entrada i j del producto es igual a alfa por "
                 "la entrada i j de A."
        ) as t:
            self.play(FadeIn(def_nota, shift=DOWN * 0.3), run_time=min(t.duration * 0.3, 1.2))
            self.esperar(t.duration - 1.2)

        with self.voiceover(
            text="Ojo, alfa puede ser cualquier número real: positivo, negativo, "
                 "cero, decimal, fracción. No tiene que ser entero."
        ) as t:
            self.play(FadeIn(aclara), run_time=min(t.duration * 0.2, 1.0))
            self.esperar(t.duration - 1.0)

        with self.voiceover(text="Veamos un ejemplo concreto.") as t:
            self.play(FadeOut(VGroup(def_nombre, def_formula, def_nota, aclara)),
                      run_time=min(t.duration, 1.5))
            self.esperar(t.duration - 1.5)

        # ==== Bloque 2: ejemplo ====
        with self.voiceover(
            text="Tenemos la matriz A igual a dos, uno, cero, tres. Y queremos "
                 "multiplicarla por el escalar tres."
        ) as t:
            self.play(FadeIn(ej_nombre), run_time=min(t.duration * 0.15, 0.8))
            self.play(FadeIn(label_A), FadeIn(A_mat), run_time=min(t.duration * 0.2, 1.2))
            self.esperar(t.duration - 2.0)

        with self.voiceover(
            text="Entonces, multiplicamos cada entrada por tres."
        ) as t:
            self.play(FadeIn(alpha), FadeIn(punto), run_time=min(t.duration * 0.2, 1.0))
            self.esperar(t.duration - 1.0)

        with self.voiceover(
            text="Fíjense: a uno uno, que es dos, por tres nos da seis."
        ) as t:
            r1 = SurroundingRectangle(A_mat.get_entries()[0], color=RED, buff=0.1)
            self.play(FadeIn(eq), FadeIn(label_C), FadeIn(C_mat),
                      run_time=min(t.duration * 0.15, 0.8))
            self.play(FadeIn(calc), run_time=min(t.duration * 0.1, 0.6))
            self.play(Create(r1), run_time=min(t.duration * 0.1, 0.6))
            self.esperar(t.duration - 2.0)

        with self.voiceover(
            text="a uno dos, que es uno, por tres nos da tres. a dos uno, que es "
                 "cero, por tres nos da cero. Y a dos dos, que es tres, por tres "
                 "nos da nueve."
        ) as t:
            # Recorrer las otras 3 entradas de A, resaltando
            rects = VGroup(r1)
            for idx in [1, 2, 3]:
                r_new = SurroundingRectangle(A_mat.get_entries()[idx],
                                             color=RED, buff=0.1)
                self.play(FadeOut(rects), Create(r_new),
                          run_time=min(t.duration * 0.1, 0.6))
                rects = VGroup(r_new)
                self.esperar(t.duration * 0.1)
            self.play(FadeOut(rects), FadeOut(calc), run_time=0.5)

        with self.voiceover(
            text="El resultado es esta nueva matriz: seis, tres, cero, nueve. "
                 "Como ven, cada entrada creció por un factor de tres."
        ) as t:
            self.esperar(t.duration)

        with self.voiceover(text="Siguiente.") as t:
            self.play(
                FadeOut(VGroup(alpha, punto, label_A, A_mat, eq, label_C, C_mat, ej_nombre)),
                run_time=min(t.duration, 1.5),
            )
            self.esperar(t.duration - 1.5)

        # ==== Bloque 3: propiedades ====
        with self.voiceover(
            text="El producto por escalar cumple varias propiedades muy cómodas."
        ) as t:
            self.play(FadeIn(prop_nombre), run_time=min(t.duration * 0.3, 1.0))
            self.esperar(t.duration - 1.0)

        with self.voiceover(
            text="Distribuye respecto a la suma de matrices: alfa por A más B es "
                 "igual a alfa A más alfa B."
        ) as t:
            self.play(FadeIn(p1, shift=DOWN * 0.3), run_time=min(t.duration * 0.3, 1.2))
            self.esperar(t.duration - 1.2)

        with self.voiceover(
            text="También distribuye respecto a la suma de escalares: alfa más "
                 "beta, todo por A, es igual a alfa A más beta A."
        ) as t:
            self.play(FadeIn(p2, shift=DOWN * 0.3), run_time=min(t.duration * 0.3, 1.2))
            self.esperar(t.duration - 1.2)

        with self.voiceover(
            text="Y es compatible con el producto de escalares: alfa por beta A "
                 "es igual a alfa beta, todo por A."
        ) as t:
            self.play(FadeIn(p3, shift=DOWN * 0.3), run_time=min(t.duration * 0.3, 1.2))
            self.esperar(t.duration - 1.2)

        with self.voiceover(
            text="Finalmente, multiplicar por uno deja la matriz igual: uno por A "
                 "es A."
        ) as t:
            self.play(FadeIn(p4, shift=DOWN * 0.3), run_time=min(t.duration * 0.3, 1.2))
            self.esperar(t.duration - 1.2)

        with self.voiceover(
            text="Estas propiedades nos van a permitir manipular expresiones con "
                 "matrices casi como si fueran números normales."
        ) as t:
            self.esperar(t.duration)

        # ---------- 4. CIERRE ----------
        self.play(FadeOut(VGroup(titulo, prop_nombre, props)), run_time=2)


# ---------- Escena 06: Multiplicación de matrices ----------
class D06_MultiplicacionMatrices(CuadernoScene):
    def construct(self):
        # ---------- 1. OBJETOS ----------
        titulo = Text("Multiplicación de matrices", font_size=42, color="#1A3A5C", weight=BOLD)

        # ===== Bloque 1: condición =====
        cond_nombre = Text("Condición de compatibilidad", font_size=30, color="#1A3A5C", weight=BOLD)
        cond_formula = Tex(
            r"$A_{m \times n} \cdot B_{n \times p} = C_{m \times p}$",
            tex_environment="center", font_size=40,
        )
        cond_formula.set_color("#1A3A5C")
        cond_nota = Tex(
            r"Las columnas de $A$ deben coincidir con las filas de $B$",
            tex_environment="center", font_size=26,
        )
        cond_nota.set_color("#4A6A8A")

        # Compatible
        comp_label = Text("Compatible", font_size=26, color=TEAL, weight=BOLD)
        comp_formula = MathTex(r"(2 \times \mathbf{3}) \cdot (\mathbf{3} \times 2)",
                               font_size=32, color="#2A4A6A")
        comp_res = MathTex(r"\Rightarrow 2 \times 2", font_size=32, color=TEAL)

        # Incompatible
        inc_label = Text("No compatible", font_size=26, color=RED, weight=BOLD)
        inc_formula = MathTex(r"(2 \times \mathbf{2}) \cdot (\mathbf{3} \times 2)",
                              font_size=32, color="#2A4A6A")
        inc_res = MathTex(r"\times", font_size=44, color=RED)

        # ===== Bloque 2: definición =====
        def_nombre = Text("Definición", font_size=30, color="#1A3A5C", weight=BOLD)
        def_formula = MathTex(
            r"c_{ij} = \sum_{k=1}^{n} a_{ik}\, b_{kj}",
            font_size=52, color="#1A3A5C",
        )
        def_nota = Tex(
            r"$c_{ij}$ = producto punto de la fila $i$ de $A$\\"
            r"con la columna $j$ de $B$",
            tex_environment="center", font_size=26,
        )
        def_nota.set_color("#4A6A8A")

        # ===== Bloque 3: ejemplo 2x2 =====
        ej_nombre = Text("Ejemplo paso a paso", font_size=30, color="#1A3A5C", weight=BOLD)

        A_mat = Matrix([[1, 2], [3, 4]], h_buff=0.7, v_buff=0.5)
        A_mat.set_color("#2A4A6A")
        label_A = MathTex("A", font_size=34, color="#1A3A5C")

        B_mat = Matrix([[5, 6], [7, 8]], h_buff=0.7, v_buff=0.5)
        B_mat.set_color("#2A4A6A")
        label_B = MathTex("B", font_size=34, color="#1A3A5C")

        C_mat = Matrix([[r"c_{11}", r"c_{12}"], [r"c_{21}", r"c_{22}"]],
                       h_buff=0.9, v_buff=0.6)
        C_mat.set_color("#1A3A5C")
        label_C = MathTex("C", font_size=34, color="#E88B8B")

        punto_op = MathTex(r"\cdot", font_size=44, color="#1A3A5C")
        eq_op = MathTex("=", font_size=44, color="#1A3A5C")

        # Cálculo detallado por entrada (se van mostrando uno a uno)
        calc11 = MathTex(r"c_{11} = (1)(5) + (2)(7) = 19",
                         font_size=28, color=RED)
        calc12 = MathTex(r"c_{12} = (1)(6) + (2)(8) = 22",
                         font_size=28, color=RED)
        calc21 = MathTex(r"c_{21} = (3)(5) + (4)(7) = 43",
                         font_size=28, color=RED)
        calc22 = MathTex(r"c_{22} = (3)(6) + (4)(8) = 50",
                         font_size=28, color=RED)

        # ===== Bloque 4: nota AB != BA =====
        nota_nombre = Text("Ojo con el orden", font_size=30, color="#1A3A5C", weight=BOLD)
        nota_formula = MathTex(r"A \cdot B \;\neq\; B \cdot A",
                               font_size=44, color="#1A3A5C")
        nota_expl = Tex(
            r"La multiplicaci\'on de matrices \textbf{no es conmutativa}",
            tex_environment="center", font_size=26,
        )
        nota_expl.set_color("#4A6A8A")
        nota_final = Tex(
            r"El orden de los factores \textbf{s\'i} altera el producto",
            tex_environment="center", font_size=26,
        )
        nota_final.set_color("#E88B8B")

        # ---------- 2. CONFIGURACIÓN ----------
        titulo.move_to([0, 0, 0])
        titulo_final = titulo.copy().scale(0.7).move_to([0, 3.6, 0])

        # Bloque 1
        cond_nombre.move_to([0, 2.6, 0])
        cond_formula.move_to([0, 1.5, 0])
        cond_nota.move_to([0, 0.6, 0])
        comp_label.move_to([-3.2, -0.7, 0])
        comp_formula.move_to([-3.2, -1.4, 0])
        comp_res.move_to([-3.2, -2.0, 0])
        inc_label.move_to([3.2, -0.7, 0])
        inc_formula.move_to([3.2, -1.4, 0])
        inc_res.move_to([3.2, -2.0, 0])

        # Bloque 2
        def_nombre.move_to([0, 2.6, 0])
        def_formula.move_to([0, 1.3, 0])
        def_nota.move_to([0, 0.0, 0])

        # Bloque 3
        ej_nombre.move_to([0, 2.6, 0])
        label_A.move_to([-5.0, -0.1, 0])
        A_mat.move_to([-4.8, -0.9, 0])
        punto_op.move_to([-3.0, -0.9, 0])
        label_B.move_to([-1.8, -0.1, 0])
        B_mat.move_to([-1.6, -0.9, 0])
        eq_op.move_to([0.2, -0.9, 0])
        label_C.move_to([1.6, -0.1, 0])
        C_mat.move_to([1.8, -0.9, 0])
        calc11.move_to([-3.2, 1.8, 0])
        calc12.move_to([3.2, 1.8, 0])
        calc21.move_to([-3.2, 1.1, 0])
        calc22.move_to([3.2, 1.1, 0])

        # Bloque 4
        nota_nombre.move_to([0, 2.6, 0])
        nota_formula.move_to([0, 1.0, 0])
        nota_expl.move_to([0, 0.0, 0])
        nota_final.move_to([0, -1.2, 0])

        # ---------- 3. ANIMACIONES ----------
        self.set_speech_service(EdgeTTSService(voice="es-MX-JorgeNeural"))

        # ==== Intro ====
        with self.voiceover(
            text="Ahora sí, llegamos al tema más importante de todo: la "
                 "multiplicación de matrices."
        ) as t:
            self.play(Write(titulo), run_time=min(t.duration, 2.5))
            self.esperar(t.duration - 2.5)

        with self.voiceover(text="Empecemos con la condición.") as t:
            self.play(Transform(titulo, titulo_final), run_time=min(t.duration, 1.5))
            self.play(FadeIn(cond_nombre), run_time=min(t.duration * 0.25, 0.8))
            self.esperar(t.duration - 2.3)

        # ==== Bloque 1: condición ====
        with self.voiceover(
            text="A diferencia de la suma, donde necesitábamos que las matrices "
                 "tuvieran el mismo orden, aquí la condición es distinta."
        ) as t:
            self.play(FadeIn(cond_formula, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="Si A es de orden m por n, y B es de orden n por p, entonces el "
                 "número de columnas de A, que es n, tiene que coincidir con el "
                 "número de filas de B, que también es n. El resultado C va a ser "
                 "de orden m por p."
        ) as t:
            self.play(FadeIn(cond_nota, shift=DOWN * 0.3), run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="Por ejemplo, una matriz de dos por tres sí se puede multiplicar "
                 "con una de tres por dos, porque el tres de en medio coincide. "
                 "Y el resultado va a ser de dos por dos."
        ) as t:
            self.play(FadeIn(comp_label), run_time=min(t.duration * 0.1, 0.6))
            self.play(FadeIn(comp_formula), run_time=min(t.duration * 0.1, 0.6))
            self.play(FadeIn(comp_res), run_time=min(t.duration * 0.1, 0.6))
            self.esperar(t.duration - 1.8)

        with self.voiceover(
            text="Pero una de dos por dos con una de tres por dos, no se puede, "
                 "porque el dos no coincide con el tres."
        ) as t:
            self.play(FadeIn(inc_label), run_time=min(t.duration * 0.1, 0.6))
            self.play(FadeIn(inc_formula), run_time=min(t.duration * 0.1, 0.6))
            self.play(FadeIn(inc_res), run_time=min(t.duration * 0.1, 0.6))
            self.esperar(t.duration - 1.8)

        with self.voiceover(text="Bien.") as t:
            self.play(FadeOut(VGroup(cond_nombre, cond_formula, cond_nota,
                                     comp_label, comp_formula, comp_res,
                                     inc_label, inc_formula, inc_res)),
                      run_time=min(t.duration, 1.5))
            self.esperar(t.duration - 1.5)

        # ==== Bloque 2: definición ====
        with self.voiceover(
            text="Suponiendo que son compatibles, ¿cómo se calcula cada entrada "
                 "del producto? La respuesta es con un producto punto entre una "
                 "fila y una columna."
        ) as t:
            self.play(FadeIn(def_nombre), run_time=min(t.duration * 0.2, 1.0))
            self.esperar(t.duration - 1.0)

        with self.voiceover(
            text="Formalmente, la entrada c sub i j es la suma desde k igual a uno "
                 "hasta n, de a sub i k por b sub k j."
        ) as t:
            self.play(FadeIn(def_formula, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.8))
            self.esperar(t.duration - 1.8)

        with self.voiceover(
            text="En palabras: tomamos la fila i de A, la columna j de B, "
                 "multiplicamos entrada por entrada, y sumamos todos esos productos."
        ) as t:
            self.play(FadeIn(def_nota, shift=DOWN * 0.3), run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(text="Veamos un ejemplo clarísimo.") as t:
            self.play(FadeOut(VGroup(def_nombre, def_formula, def_nota)),
                      run_time=min(t.duration, 1.5))
            self.esperar(t.duration - 1.5)

        # ==== Bloque 3: ejemplo ====
        with self.voiceover(
            text="Aquí tenemos dos matrices de dos por dos. A igual a uno, dos, "
                 "tres, cuatro. Y B igual a cinco, seis, siete, ocho. Como ambas "
                 "son de dos por dos, sí se pueden multiplicar, y el resultado va "
                 "a ser otra matriz de dos por dos."
        ) as t:
            self.play(FadeIn(ej_nombre), run_time=min(t.duration * 0.1, 0.6))
            self.play(FadeIn(label_A), FadeIn(A_mat), run_time=min(t.duration * 0.15, 1.0))
            self.play(FadeIn(punto_op), run_time=min(t.duration * 0.05, 0.4))
            self.play(FadeIn(label_B), FadeIn(B_mat), run_time=min(t.duration * 0.15, 1.0))
            self.play(FadeIn(eq_op), FadeIn(label_C), FadeIn(C_mat),
                      run_time=min(t.duration * 0.15, 1.0))
            self.esperar(t.duration - 4.0)

        # --- c11: fila 1 de A, columna 1 de B ---
        with self.voiceover(
            text="Para calcular c uno uno, tomamos la fila uno de A, que es uno y "
                 "dos, y la columna uno de B, que es cinco y siete. Multiplicamos: "
                 "uno por cinco es cinco, dos por siete es catorce. Sumamos y nos "
                 "da diecinueve."
        ) as t:
            fila_A_1 = SurroundingRectangle(
                VGroup(A_mat.get_entries()[0], A_mat.get_entries()[1]),
                color=RED, buff=0.12,
            )
            col_B_1 = SurroundingRectangle(
                VGroup(B_mat.get_entries()[0], B_mat.get_entries()[2]),
                color=TEAL, buff=0.12,
            )
            self.play(Create(fila_A_1), Create(col_B_1),
                      run_time=min(t.duration * 0.2, 1.5))
            self.play(FadeIn(calc11), run_time=min(t.duration * 0.15, 1.2))
            self.esperar(t.duration - 2.7)

        with self.voiceover(text="Muy bien.") as t:
            self.play(FadeOut(fila_A_1), FadeOut(col_B_1), FadeOut(calc11),
                      run_time=min(t.duration * 0.5, 1.0))
            self.esperar(t.duration - 1.0)

        # --- c12: fila 1 de A, columna 2 de B ---
        with self.voiceover(
            text="Para c uno dos, misma fila uno de A, pero ahora columna dos de B, "
                 "que es seis y ocho. Uno por seis es seis, dos por ocho es "
                 "dieciséis. Sumamos y nos da veintidós."
        ) as t:
            fila_A_1b = SurroundingRectangle(
                VGroup(A_mat.get_entries()[0], A_mat.get_entries()[1]),
                color=RED, buff=0.12,
            )
            col_B_2 = SurroundingRectangle(
                VGroup(B_mat.get_entries()[1], B_mat.get_entries()[3]),
                color=TEAL, buff=0.12,
            )
            self.play(Create(fila_A_1b), Create(col_B_2),
                      run_time=min(t.duration * 0.2, 1.5))
            self.play(FadeIn(calc12), run_time=min(t.duration * 0.15, 1.2))
            self.esperar(t.duration - 2.7)

        with self.voiceover(text="Bien.") as t:
            self.play(FadeOut(fila_A_1b), FadeOut(col_B_2), FadeOut(calc12),
                      run_time=min(t.duration * 0.5, 1.0))
            self.esperar(t.duration - 1.0)

        # --- c21: fila 2 de A, columna 1 de B ---
        with self.voiceover(
            text="Para c dos uno, ahora fila dos de A, que es tres y cuatro, con "
                 "columna uno de B. Tres por cinco es quince, cuatro por siete es "
                 "veintiocho. Total: cuarenta y tres."
        ) as t:
            fila_A_2 = SurroundingRectangle(
                VGroup(A_mat.get_entries()[2], A_mat.get_entries()[3]),
                color=RED, buff=0.12,
            )
            col_B_1b = SurroundingRectangle(
                VGroup(B_mat.get_entries()[0], B_mat.get_entries()[2]),
                color=TEAL, buff=0.12,
            )
            self.play(Create(fila_A_2), Create(col_B_1b),
                      run_time=min(t.duration * 0.2, 1.5))
            self.play(FadeIn(calc21), run_time=min(t.duration * 0.15, 1.2))
            self.esperar(t.duration - 2.7)

        with self.voiceover(text="Siguiente.") as t:
            self.play(FadeOut(fila_A_2), FadeOut(col_B_1b), FadeOut(calc21),
                      run_time=min(t.duration * 0.5, 1.0))
            self.esperar(t.duration - 1.0)

        # --- c22: fila 2 de A, columna 2 de B ---
        with self.voiceover(
            text="Y para c dos dos, fila dos de A con columna dos de B. Tres por "
                 "seis es dieciocho, cuatro por ocho es treinta y dos. Total: "
                 "cincuenta."
        ) as t:
            fila_A_2b = SurroundingRectangle(
                VGroup(A_mat.get_entries()[2], A_mat.get_entries()[3]),
                color=RED, buff=0.12,
            )
            col_B_2b = SurroundingRectangle(
                VGroup(B_mat.get_entries()[1], B_mat.get_entries()[3]),
                color=TEAL, buff=0.12,
            )
            self.play(Create(fila_A_2b), Create(col_B_2b),
                      run_time=min(t.duration * 0.2, 1.5))
            self.play(FadeIn(calc22), run_time=min(t.duration * 0.15, 1.2))
            self.esperar(t.duration - 2.7)

        with self.voiceover(
            text="Entonces, el producto C es la matriz: diecinueve, veintidós, "
                 "cuarenta y tres, cincuenta."
        ) as t:
            self.play(FadeOut(fila_A_2b), FadeOut(col_B_2b), FadeOut(calc22),
                      run_time=min(t.duration * 0.3, 1.0))
            # Reemplazar la C simbólica por la numérica
            C_num = Matrix([[19, 22], [43, 50]], h_buff=0.9, v_buff=0.6)
            C_num.set_color("#1A3A5C")
            C_num.move_to(C_mat.get_center())
            self.play(Transform(C_mat, C_num), run_time=min(t.duration * 0.5, 2))
            self.esperar(t.duration - 3.0)

        with self.voiceover(text="Perfecto.") as t:
            self.play(
                FadeOut(VGroup(ej_nombre, label_A, A_mat, punto_op, label_B, B_mat,
                               eq_op, label_C, C_mat)),
                run_time=min(t.duration, 1.5),
            )
            self.esperar(t.duration - 1.5)

        # ==== Bloque 4: AB != BA ====
        with self.voiceover(
            text="Ahora, un detalle muy importante. A diferencia de los números "
                 "reales, donde a por b es igual a b por a, con las matrices esto "
                 "NO siempre se cumple."
        ) as t:
            self.play(FadeIn(nota_nombre), run_time=min(t.duration * 0.15, 1.0))
            self.play(FadeIn(nota_formula, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 2.5)

        with self.voiceover(
            text="En general, A por B no es igual a B por A. La multiplicación de "
                 "matrices no es conmutativa. Y de hecho, a veces ni siquiera están "
                 "definidos los dos productos."
        ) as t:
            self.play(FadeIn(nota_expl, shift=DOWN * 0.3), run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="Así que mucho ojo con el orden de los factores. Aquí sí altera "
                 "el producto. Guárdense esta idea, porque es una de las grandes "
                 "diferencias con el álgebra de números normales."
        ) as t:
            self.play(FadeIn(nota_final, shift=DOWN * 0.3), run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        # ---------- 4. CIERRE ----------
        self.play(FadeOut(VGroup(titulo, nota_nombre, nota_formula, nota_expl, nota_final)),
                  run_time=2)

# ---------- Escena 07: Matriz transpuesta ----------
class D07_Transpuesta(CuadernoScene):
    def construct(self):
        # ---------- 1. OBJETOS ----------
        titulo = Text("Matriz transpuesta", font_size=42, color="#1A3A5C", weight=BOLD)

        # ===== Bloque 1: definición =====
        def_nombre = Text("Definición", font_size=30, color="#1A3A5C", weight=BOLD)
        def_formula = MathTex(
            r"(A^T)_{ij} = a_{ji}",
            font_size=54, color="#1A3A5C",
        )
        def_nota = Tex(
            r"La fila $i$ de $A^T$ es la columna $i$ de $A$\\"
            r"(y viceversa)",
            tex_environment="center", font_size=26,
        )
        def_nota.set_color("#4A6A8A")

        dims = Tex(
            r"Si $A$ es de orden $m \times n$, entonces $A^T$ es de $n \times m$",
            tex_environment="center", font_size=26,
        )
        dims.set_color("#2A4A6A")

        # ===== Bloque 2: ejemplo visual =====
        ej_nombre = Text("Ejemplo", font_size=30, color="#1A3A5C", weight=BOLD)

        A_mat = Matrix([[1, 2, 3], [4, 5, 6]], h_buff=0.7, v_buff=0.5)
        A_mat.set_color("#2A4A6A")
        label_A = MathTex("A", font_size=36, color="#1A3A5C")

        At_mat = Matrix([[1, 4], [2, 5], [3, 6]], h_buff=0.7, v_buff=0.5)
        At_mat.set_color("#2A4A6A")
        label_At = MathTex(r"A^T", font_size=36, color="#E88B8B")

        flecha = MathTex(r"\longrightarrow", font_size=80, color="#E88B8B")

        dim_label_A = MathTex(r"2 \times 3", font_size=26, color="#4A6A8A")
        dim_label_At = MathTex(r"3 \times 2", font_size=26, color="#4A6A8A")

        hint1 = Tex(r"Fila 1 de $A$ $\rightarrow$ Columna 1 de $A^T$",
                    tex_environment="center", font_size=24)
        hint1.set_color("#E88B8B")

        # ===== Bloque 3: propiedades =====
        prop_nombre = Text("Propiedades", font_size=30, color="#1A3A5C", weight=BOLD)
        p1 = Tex(r"$(A^T)^T = A$", tex_environment="center", font_size=30)
        p2 = Tex(r"$(A + B)^T = A^T + B^T$", tex_environment="center", font_size=30)
        p3 = Tex(r"$(\alpha A)^T = \alpha A^T$", tex_environment="center", font_size=30)
        p4 = Tex(r"$(AB)^T = B^T A^T$", tex_environment="center", font_size=30)
        for p in [p1, p2, p3, p4]:
            p.set_color("#2A4A6A")
        props = VGroup(p1, p2, p3, p4).arrange(DOWN, center=True, buff=0.25)

        # ===== Bloque 4: simétrica =====
        sim_nombre = Text("Caso especial: matriz simétrica", font_size=28,
                          color="#1A3A5C", weight=BOLD)
        sim_def = Tex(
            r"$A$ es \textbf{sim\'etrica} si $A = A^T$",
            tex_environment="center", font_size=28,
        )
        sim_def.set_color("#2A4A6A")
        sim_ej = Matrix([[1, 2, 3], [2, 4, 5], [3, 5, 6]],
                        h_buff=0.7, v_buff=0.5)
        sim_ej.set_color("#2A4A6A")
        sim_nota = Tex(
            r"La parte de arriba es espejo de la de abajo",
            tex_environment="center", font_size=24,
        )
        sim_nota.set_color("#4A6A8A")

        # ---------- 2. CONFIGURACIÓN ----------
        titulo.move_to([0, 0, 0])
        titulo_final = titulo.copy().scale(0.7).move_to([0, 3.6, 0])

        # Bloque 1
        def_nombre.move_to([0, 2.6, 0])
        def_formula.move_to([0, 1.3, 0])
        def_nota.move_to([0, 0.2, 0])
        dims.move_to([0, -1.0, 0])

        # Bloque 2
        ej_nombre.move_to([0, 2.6, 0])
        label_A.move_to([-3.7, 0.6, 0])
        A_mat.move_to([-3.7, -0.4, 0])
        dim_label_A.move_to([-3.7, -1.6, 0])
        flecha.move_to([0, -0.4, 0])
        label_At.move_to([3.0, 0.6, 0])
        At_mat.move_to([3.0, -0.6, 0])
        dim_label_At.move_to([3.0, -2.1, 0])
        hint1.move_to([0, 1.7, 0])

        # Bloque 3
        prop_nombre.move_to([0, 2.6, 0])
        props.move_to([0, 0.6, 0])

        # Bloque 4
        sim_nombre.move_to([0, 2.5, 0])
        sim_def.move_to([0, 1.7, 0])
        sim_ej.move_to([0, -0.1, 0])
        sim_nota.move_to([0, -1.7, 0])

        # ---------- 3. ANIMACIONES ----------
        self.set_speech_service(EdgeTTSService(voice="es-MX-JorgeNeural"))

        # ==== Intro ====
        with self.voiceover(
            text="Vamos ahora con la transpuesta. Es una operación muy sencilla "
                 "pero muy importante."
        ) as t:
            self.play(Write(titulo), run_time=min(t.duration, 2.5))
            self.esperar(t.duration - 2.5)

        with self.voiceover(text="Empecemos con la definición formal.") as t:
            self.play(Transform(titulo, titulo_final), run_time=min(t.duration, 1.5))
            self.play(FadeIn(def_nombre), run_time=min(t.duration * 0.25, 0.8))
            self.esperar(t.duration - 2.3)

        # ==== Bloque 1: definición ====
        with self.voiceover(
            text="Dada una matriz A, su transpuesta, que escribimos A super T, "
                 "es la matriz que se obtiene intercambiando filas por columnas."
        ) as t:
            self.play(FadeIn(def_formula, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="Formalmente, la entrada i j de A transpuesta es igual a la "
                 "entrada j i de A. Es decir, la fila i de A transpuesta es la "
                 "columna i de A, y viceversa."
        ) as t:
            self.play(FadeIn(def_nota, shift=DOWN * 0.3), run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="Esto tiene una consecuencia muy útil: si A es de orden m por n, "
                 "entonces A transpuesta es de orden n por m. Los órdenes se "
                 "intercambian."
        ) as t:
            self.play(FadeIn(dims, shift=DOWN * 0.3), run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(text="Veamos un ejemplo visual.") as t:
            self.play(FadeOut(VGroup(def_nombre, def_formula, def_nota, dims)),
                      run_time=min(t.duration, 1.5))
            self.esperar(t.duration - 1.5)

        # ==== Bloque 2: ejemplo visual ====
        with self.voiceover(
            text="Aquí tenemos una matriz A de dos por tres. Fíjense que tiene dos "
                 "filas y tres columnas."
        ) as t:
            self.play(FadeIn(ej_nombre), run_time=min(t.duration * 0.15, 0.8))
            self.play(FadeIn(label_A), FadeIn(A_mat),
                      run_time=min(t.duration * 0.2, 1.2))
            self.play(FadeIn(dim_label_A), run_time=min(t.duration * 0.1, 0.6))
            self.esperar(t.duration - 2.6)

        with self.voiceover(
            text="Al transponerla, las filas se convierten en columnas. Entonces "
                 "ahora vamos a tener tres filas y dos columnas: una matriz de tres "
                 "por dos."
        ) as t:
            self.play(FadeIn(flecha), run_time=min(t.duration * 0.15, 1.0))
            self.play(FadeIn(label_At), FadeIn(At_mat),
                      run_time=min(t.duration * 0.2, 1.2))
            self.play(FadeIn(dim_label_At), run_time=min(t.duration * 0.1, 0.6))
            self.esperar(t.duration - 2.8)

        with self.voiceover(
            text="Miren cómo funciona. La primera fila de A, que es uno, dos, tres, "
                 "se convierte en la primera columna de A transpuesta."
        ) as t:
            fila_A_1 = SurroundingRectangle(
                VGroup(A_mat.get_entries()[0], A_mat.get_entries()[1], A_mat.get_entries()[2]),
                color=RED, buff=0.12,
            )
            col_At_1 = SurroundingRectangle(
                VGroup(At_mat.get_entries()[0], At_mat.get_entries()[2], At_mat.get_entries()[4]),
                color=TEAL, buff=0.12,
            )
            self.play(FadeIn(hint1), run_time=min(t.duration * 0.1, 0.6))
            self.play(Create(fila_A_1), run_time=min(t.duration * 0.15, 1.0))
            self.play(Create(col_At_1), run_time=min(t.duration * 0.15, 1.0))
            self.esperar(t.duration - 2.6)

        with self.voiceover(
            text="Y la segunda fila de A, que es cuatro, cinco, seis, se convierte "
                 "en la segunda columna de A transpuesta."
        ) as t:
            fila_A_2 = SurroundingRectangle(
                VGroup(A_mat.get_entries()[3], A_mat.get_entries()[4], A_mat.get_entries()[5]),
                color=RED, buff=0.12,
            )
            col_At_2 = SurroundingRectangle(
                VGroup(At_mat.get_entries()[1], At_mat.get_entries()[3], At_mat.get_entries()[5]),
                color=TEAL, buff=0.12,
            )
            self.play(FadeOut(fila_A_1), FadeOut(col_At_1),
                      run_time=min(t.duration * 0.1, 0.6))
            self.play(Create(fila_A_2), run_time=min(t.duration * 0.15, 1.0))
            self.play(Create(col_At_2), run_time=min(t.duration * 0.15, 1.0))
            self.esperar(t.duration - 2.6)

        with self.voiceover(
            text="Eso es todo: filas que se vuelven columnas, columnas que se "
                 "vuelven filas. Y ojo, la transpuesta no requiere que la matriz "
                 "sea cuadrada; puede ser rectangular sin problema."
        ) as t:
            self.play(FadeOut(fila_A_2), FadeOut(col_At_2), FadeOut(hint1),
                      run_time=min(t.duration * 0.15, 1.0))
            self.esperar(t.duration - 1.0)

        with self.voiceover(text="Bien.") as t:
            self.play(
                FadeOut(VGroup(ej_nombre, label_A, A_mat, dim_label_A,
                               flecha, label_At, At_mat, dim_label_At)),
                run_time=min(t.duration, 1.5),
            )
            self.esperar(t.duration - 1.5)

        # ==== Bloque 3: propiedades ====
        with self.voiceover(
            text="La transpuesta cumple varias propiedades muy cómodas de recordar."
        ) as t:
            self.play(FadeIn(prop_nombre), run_time=min(t.duration * 0.3, 1.0))
            self.esperar(t.duration - 1.0)

        with self.voiceover(
            text="Primera: si transpones dos veces, vuelves a la matriz original. "
                 "A transpuesta, transpuesta, es A."
        ) as t:
            self.play(FadeIn(p1, shift=DOWN * 0.3), run_time=min(t.duration * 0.3, 1.2))
            self.esperar(t.duration - 1.2)

        with self.voiceover(
            text="Segunda: la transpuesta de una suma es la suma de las transpuestas."
        ) as t:
            self.play(FadeIn(p2, shift=DOWN * 0.3), run_time=min(t.duration * 0.3, 1.2))
            self.esperar(t.duration - 1.2)

        with self.voiceover(
            text="Tercera: la transpuesta saca los escalares sin problema. Alfa por "
                 "A, transpuesta, es alfa por A transpuesta."
        ) as t:
            self.play(FadeIn(p3, shift=DOWN * 0.3), run_time=min(t.duration * 0.3, 1.2))
            self.esperar(t.duration - 1.2)

        with self.voiceover(
            text="Y cuarta, que es la más importante y a veces se olvida: la "
                 "transpuesta de un producto A por B es igual a B transpuesta por "
                 "A transpuesta. Fíjense que se invierte el orden."
        ) as t:
            self.play(FadeIn(p4, shift=DOWN * 0.3), run_time=min(t.duration * 0.3, 1.2))
            self.esperar(t.duration - 1.2)

        with self.voiceover(
            text="Esta última la vamos a usar muchísimo cuando veamos matrices "
                 "ortogonales y transformaciones lineales."
        ) as t:
            self.esperar(t.duration)

        with self.voiceover(text="Por último, un caso especial.") as t:
            self.play(FadeOut(VGroup(prop_nombre, props)), run_time=min(t.duration, 1.5))
            self.esperar(t.duration - 1.5)

        # ==== Bloque 4: simétrica ====
        with self.voiceover(
            text="Hay matrices que son iguales a su propia transpuesta. A estas les "
                 "llamamos matrices simétricas."
        ) as t:
            self.play(FadeIn(sim_nombre), run_time=min(t.duration * 0.2, 1.0))
            self.play(FadeIn(sim_def, shift=DOWN * 0.3), run_time=min(t.duration * 0.3, 1.2))
            self.esperar(t.duration - 2.2)

        with self.voiceover(
            text="Fíjense en este ejemplo. Si se paran en cualquier elemento y lo "
                 "reflejan respecto a la diagonal, encuentran exactamente el mismo "
                 "valor. La parte de arriba es espejo de la de abajo."
        ) as t:
            self.play(FadeIn(sim_ej), run_time=min(t.duration * 0.2, 1.2))
            self.esperar(t.duration - 1.2)

        with self.voiceover(
            text="Las matrices simétricas aparecen muchísimo en física, en "
                 "estadística, en optimización. Son un objeto muy estudiado dentro "
                 "del álgebra lineal."
        ) as t:
            self.play(FadeIn(sim_nota, shift=DOWN * 0.3), run_time=min(t.duration * 0.3, 1.2))
            self.esperar(t.duration - 1.2)

        # ---------- 4. CIERRE ----------
        self.play(
            FadeOut(VGroup(titulo, sim_nombre, sim_def, sim_ej, sim_nota)),
            run_time=2,
        )

# ---------- Escena 08: Matriz inversa (Gauss-Jordan en detalle) ----------
class D08_MatrizInversa(CuadernoScene):
    def construct(self):
        # ---------- 1. OBJETOS ----------
        titulo = Text("Matriz inversa", font_size=42, color="#1A3A5C", weight=BOLD)

        # ===== Bloque 1: definición =====
        def_nombre = Text("Definición", font_size=30, color="#1A3A5C", weight=BOLD)
        def_formula = MathTex(
            r"A \cdot A^{-1} = A^{-1} \cdot A = I_n",
            font_size=48, color="#1A3A5C",
        )
        def_nota = Tex(
            r"Solo existe para matrices cuadradas con $\det(A) \neq 0$",
            tex_environment="center", font_size=26,
        )
        def_nota.set_color("#4A6A8A")

        # ===== Bloque 2: método de Gauss-Jordan =====
        gj_nombre = Text("Método de Gauss-Jordan", font_size=30, color="#1A3A5C", weight=BOLD)
        gj_idea = MathTex(
            r"[\,A \;|\; I\,] \;\longrightarrow\; [\,I \;|\; A^{-1}\,]",
            font_size=44, color="#1A3A5C",
        )
        gj_nota = Tex(
            r"Aplicamos operaciones elementales por fila hasta\\"
            r"convertir $A$ en la identidad",
            tex_environment="center", font_size=24,
        )
        gj_nota.set_color("#4A6A8A")

        # Operaciones elementales
        op_titulo = Text("Operaciones elementales por fila", font_size=28, color="#1A3A5C", weight=BOLD)
        op1 = Tex(r"1. Intercambiar dos filas: $R_i \leftrightarrow R_j$",
                  tex_environment="center", font_size=24)
        op2 = Tex(r"2. Multiplicar por escalar: $R_i \to k R_i$ \;(k $\neq$ 0)",
                  tex_environment="center", font_size=24)
        op3 = Tex(r"3. Sumar m\'ultiplo: $R_i \to R_i + k R_j$",
                  tex_environment="center", font_size=24)
        for o in [op1, op2, op3]:
            o.set_color("#2A4A6A")
        ops = VGroup(op1, op2, op3).arrange(DOWN, center=True, buff=0.28)

        # ===== Bloque 3: ejemplo 4x4 =====
        ej_nombre = Text("Ejemplo 4×4 paso a paso", font_size=30, color="#1A3A5C", weight=BOLD)
        operacion = MathTex(r"R_2 \to R_2 - R_1", font_size=32, color="#E88B8B")

        # Matrices [A | I] en cada estado (se crean como funciones)
        # Estado 0
        A_0 = Matrix([[1, 1, 0, 0], [1, 2, 1, 0], [0, 1, 2, 1], [0, 0, 1, 2]],
                     h_buff=0.45, v_buff=0.32)
        I_0 = Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
                     h_buff=0.45, v_buff=0.32)
        A_0.set_color("#2A4A6A")
        I_0.set_color("#2A4A6A")
        label_A = MathTex("A", font_size=30, color="#1A3A5C")
        label_I = MathTex("I", font_size=30, color="#1A3A5C")
        linea_v = Line([0, 1.4, 0], [0, -1.4, 0], color="#1A3A5C", stroke_width=2)

        # ===== Bloque 4: nota final =====
        nota_nombre = Text("¿Y el método del determinante?", font_size=30, color="#1A3A5C", weight=BOLD)
        nota_formula = MathTex(
            r"A^{-1} = \frac{1}{\det(A)} \cdot \mathrm{adj}(A)",
            font_size=44, color="#1A3A5C",
        )
        nota_texto = Tex(
            r"Es m\'as eficiente para matrices \textbf{2$\times$2 y 3$\times$3},\\"
            r"pero para matrices grandes Gauss-Jordan es superior",
            tex_environment="center", font_size=24,
        )
        nota_texto.set_color("#4A6A8A")
        nota_adelanto = Tex(
            r"Lo veremos a detalle cuando lleguemos\\"
            r"al tema de determinantes",
            tex_environment="center", font_size=24,
        )
        nota_adelanto.set_color("#E88B8B")

        # ---------- 2. CONFIGURACIÓN ----------
        titulo.move_to([0, 0, 0])
        titulo_final = titulo.copy().scale(0.7).move_to([0, 3.6, 0])

        # Bloque 1
        def_nombre.move_to([0, 2.6, 0])
        def_formula.move_to([0, 1.3, 0])
        def_nota.move_to([0, 0.2, 0])

        # Bloque 2
        gj_nombre.move_to([0, 2.6, 0])
        gj_idea.move_to([0, 1.3, 0])
        gj_nota.move_to([0, 0.2, 0])
        op_titulo.move_to([0, 2.6, 0])
        ops.move_to([0, 0.6, 0])

        # Bloque 3
        ej_nombre.move_to([0, 2.7, 0])
        operacion.move_to([0, 1.9, 0])
        A_0.move_to([-2.2, 0.0, 0])
        I_0.move_to([2.2, 0.0, 0])
        label_A.move_to([-2.2, 1.6, 0])
        label_I.move_to([2.2, 1.6, 0])
        linea_v.move_to([0, 0.0, 0])

        # Bloque 4
        nota_nombre.move_to([0, 2.5, 0])
        nota_formula.move_to([0, 1.2, 0])
        nota_texto.move_to([0, 0.0, 0])
        nota_adelanto.move_to([0, -1.3, 0])

        # ---------- 3. ANIMACIONES ----------
        self.set_speech_service(EdgeTTSService(voice="es-MX-JorgeNeural"))

        # ==== Intro + definición ====
        with self.voiceover(
            text="Vamos ahora con la matriz inversa. Este es uno de los conceptos "
                 "más importantes del álgebra lineal, porque nos permite, entre "
                 "otras cosas, resolver sistemas de ecuaciones de forma elegante."
        ) as t:
            self.play(Write(titulo), run_time=min(t.duration, 2.5))
            self.esperar(t.duration - 2.5)

        with self.voiceover(text="Empecemos con la definición.") as t:
            self.play(Transform(titulo, titulo_final), run_time=min(t.duration, 1.5))
            self.play(FadeIn(def_nombre), run_time=min(t.duration * 0.25, 0.8))
            self.esperar(t.duration - 2.3)

        with self.voiceover(
            text="Dada una matriz cuadrada A, su inversa, que escribimos A elevada "
                 "a menos uno, es otra matriz que cumple que al multiplicarla por A, "
                 "ya sea por izquierda o por derecha, nos da la identidad."
        ) as t:
            self.play(FadeIn(def_formula, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="Es importante saber que la inversa no siempre existe. Para que "
                 "exista, la matriz tiene que ser cuadrada y su determinante tiene "
                 "que ser distinto de cero. El determinante lo vamos a estudiar más "
                 "adelante, pero guárdenlo por ahora: si el determinante es cero, la "
                 "matriz no tiene inversa."
        ) as t:
            self.play(FadeIn(def_nota, shift=DOWN * 0.3), run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(text="Muy bien. Ahora, ¿cómo se calcula la inversa?") as t:
            self.play(FadeOut(VGroup(def_nombre, def_formula, def_nota)),
                      run_time=min(t.duration, 1.5))
            self.esperar(t.duration - 1.5)

        # ==== Gauss-Jordan: idea ====
        with self.voiceover(
            text="Existen varios métodos, pero el más importante, el más general y "
                 "el más usado en la práctica, es el método de Gauss-Jordan."
        ) as t:
            self.play(FadeIn(gj_nombre), run_time=min(t.duration * 0.2, 1.0))
            self.esperar(t.duration - 1.0)

        with self.voiceover(
            text="La idea es esta: tomamos la matriz A, y a su derecha le pegamos la "
                 "matriz identidad del mismo orden. Así formamos una matriz aumentada, "
                 "que escribimos entre corchetes como A, una barra vertical, e I."
        ) as t:
            self.play(FadeIn(gj_idea, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.8))
            self.esperar(t.duration - 1.8)

        with self.voiceover(
            text="Luego aplicamos operaciones elementales por fila, que son "
                 "transformaciones permitidas, hasta que la parte izquierda se "
                 "convierta en la identidad. En ese momento, la parte derecha se "
                 "habrá transformado automáticamente en la inversa de A."
        ) as t:
            self.play(FadeIn(gj_nota, shift=DOWN * 0.3), run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(text="Vamos a ver cuáles son esas operaciones elementales.") as t:
            self.play(FadeOut(VGroup(gj_nombre, gj_idea, gj_nota)),
                      run_time=min(t.duration, 1.5))
            self.esperar(t.duration - 1.5)

        # ==== Operaciones elementales ====
        with self.voiceover(
            text="Hay tres operaciones elementales por fila que podemos hacer."
        ) as t:
            self.play(FadeIn(op_titulo), run_time=min(t.duration * 0.25, 1.0))
            self.esperar(t.duration - 1.0)

        with self.voiceover(
            text="Primera: intercambiar dos filas. Esto lo escribimos como R sub i "
                 "se intercambia con R sub j."
        ) as t:
            self.play(FadeIn(op1, shift=DOWN * 0.3), run_time=min(t.duration * 0.3, 1.2))
            self.esperar(t.duration - 1.2)

        with self.voiceover(
            text="Segunda: multiplicar una fila por un escalar distinto de cero. "
                 "Aquí es importante que sea distinto de cero, porque si multiplicamos "
                 "por cero, perdemos información y ya no podemos deshacer la operación."
        ) as t:
            self.play(FadeIn(op2, shift=DOWN * 0.3), run_time=min(t.duration * 0.3, 1.2))
            self.esperar(t.duration - 1.2)

        with self.voiceover(
            text="Y tercera: sumarle a una fila un múltiplo de otra fila. Estas tres "
                 "operaciones son las únicas que vamos a usar, y son reversibles: "
                 "siempre podemos deshacerlas."
        ) as t:
            self.play(FadeIn(op3, shift=DOWN * 0.3), run_time=min(t.duration * 0.3, 1.2))
            self.esperar(t.duration - 1.2)

        with self.voiceover(
            text="Ahora sí, veamos un ejemplo completo. Voy a usar una matriz de "
                 "cuatro por cuatro, para que vean que el método escala bien y no se "
                 "limita a matrices pequeñitas."
        ) as t:
            self.play(FadeOut(VGroup(op_titulo, ops)), run_time=min(t.duration * 0.5, 1.5))
            self.esperar(t.duration - 1.5)

        # ==== Ejemplo 4x4 ====
        with self.voiceover(
            text="Aquí tienen la matriz A, que es una matriz tridiagonal: unos en la "
                 "diagonal, unos en las dos diagonales vecinas, y ceros en el resto. "
                 "Y a su derecha tienen la identidad. Juntas forman la matriz aumentada."
        ) as t:
            self.play(FadeIn(ej_nombre), run_time=min(t.duration * 0.1, 0.6))
            self.play(FadeIn(label_A), FadeIn(A_0), run_time=min(t.duration * 0.15, 1.0))
            self.play(FadeIn(label_I), FadeIn(I_0), run_time=min(t.duration * 0.15, 1.0))
            self.play(FadeIn(linea_v), run_time=min(t.duration * 0.1, 0.5))
            self.esperar(t.duration - 3.1)

        # --- Estado 1: R2 - R1 → R2 ---
        with self.voiceover(
            text="Paso uno. Queremos eliminar el uno que está debajo del pivote de la "
                 "primera columna. Entonces le restamos a la fila dos la fila uno. "
                 "En la parte de A, la nueva fila dos queda: cero, uno, uno, cero. "
                 "Y en la parte de la identidad: menos uno, uno, cero, cero."
        ) as t:
            self.play(FadeIn(operacion), run_time=min(t.duration * 0.1, 0.5))
            A_1 = Matrix([[1, 1, 0, 0], [0, 1, 1, 0], [0, 1, 2, 1], [0, 0, 1, 2]],
                         h_buff=0.45, v_buff=0.32)
            I_1 = Matrix([[1, 0, 0, 0], [-1, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
                         h_buff=0.45, v_buff=0.32)
            A_1.set_color("#2A4A6A")
            I_1.set_color("#2A4A6A")
            A_1.move_to(A_0.get_center())
            I_1.move_to(I_0.get_center())
            r_fila = SurroundingRectangle(
                VGroup(*[A_0.get_entries()[4 + k] for k in range(4)]),
                color=RED, buff=0.08,
            )
            self.play(Create(r_fila), run_time=min(t.duration * 0.1, 0.6))
            self.play(ReplacementTransform(A_0, A_1),
                      ReplacementTransform(I_0, I_1),
                      run_time=min(t.duration * 0.3, 2))
            self.play(FadeOut(r_fila), run_time=0.4)
            self.esperar(t.duration - 3.5)
            A_0, I_0 = A_1, I_1

        with self.voiceover(text="Siguiente.") as t:
            self.play(FadeOut(operacion), run_time=0.5)
            operacion = MathTex(r"R_3 \to R_3 - R_2", font_size=32, color="#E88B8B")
            operacion.move_to([0, 1.9, 0])
            self.esperar(t.duration - 0.5)

        # --- Estado 2: R3 - R2 → R3 ---
        with self.voiceover(
            text="Paso dos. Ahora eliminamos el uno de la tercera fila, segunda "
                 "columna. Restamos fila tres menos fila dos. La nueva fila tres en "
                 "A queda: cero, cero, uno, uno. Y en la identidad: uno, menos uno, "
                 "uno, cero."
        ) as t:
            self.play(FadeIn(operacion), run_time=0.5)
            A_2 = Matrix([[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1], [0, 0, 1, 2]],
                         h_buff=0.45, v_buff=0.32)
            I_2 = Matrix([[1, 0, 0, 0], [-1, 1, 0, 0], [1, -1, 1, 0], [0, 0, 0, 1]],
                         h_buff=0.45, v_buff=0.32)
            A_2.set_color("#2A4A6A")
            I_2.set_color("#2A4A6A")
            A_2.move_to(A_0.get_center())
            I_2.move_to(I_0.get_center())
            r_fila = SurroundingRectangle(
                VGroup(*[A_0.get_entries()[8 + k] for k in range(4)]),
                color=RED, buff=0.08,
            )
            self.play(Create(r_fila), run_time=0.6)
            self.play(ReplacementTransform(A_0, A_2),
                      ReplacementTransform(I_0, I_2),
                      run_time=min(t.duration * 0.3, 2))
            self.play(FadeOut(r_fila), run_time=0.4)
            self.esperar(t.duration - 3.5)
            A_0, I_0 = A_2, I_2

        with self.voiceover(text="Bien.") as t:
            self.play(FadeOut(operacion), run_time=0.5)
            operacion = MathTex(r"R_4 \to R_4 - R_3", font_size=32, color="#E88B8B")
            operacion.move_to([0, 1.9, 0])
            self.esperar(t.duration - 0.5)

        # --- Estado 3: R4 - R3 → R4 ---
        with self.voiceover(
            text="Paso tres. Eliminamos el uno de la cuarta fila, tercera columna, "
                 "restando fila cuatro menos fila tres. En A: cero, cero, cero, uno. "
                 "En la identidad: menos uno, uno, menos uno, uno. Con esto terminamos "
                 "la fase hacia abajo."
        ) as t:
            self.play(FadeIn(operacion), run_time=0.5)
            A_3 = Matrix([[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1], [0, 0, 0, 1]],
                         h_buff=0.45, v_buff=0.32)
            I_3 = Matrix([[1, 0, 0, 0], [-1, 1, 0, 0], [1, -1, 1, 0], [-1, 1, -1, 1]],
                         h_buff=0.45, v_buff=0.32)
            A_3.set_color("#2A4A6A")
            I_3.set_color("#2A4A6A")
            A_3.move_to(A_0.get_center())
            I_3.move_to(I_0.get_center())
            r_fila = SurroundingRectangle(
                VGroup(*[A_0.get_entries()[12 + k] for k in range(4)]),
                color=RED, buff=0.08,
            )
            self.play(Create(r_fila), run_time=0.6)
            self.play(ReplacementTransform(A_0, A_3),
                      ReplacementTransform(I_0, I_3),
                      run_time=min(t.duration * 0.3, 2))
            self.play(FadeOut(r_fila), run_time=0.4)
            self.esperar(t.duration - 3.5)
            A_0, I_0 = A_3, I_3

        with self.voiceover(text="Ahora vamos hacia arriba.") as t:
            self.play(FadeOut(operacion), run_time=0.5)
            operacion = MathTex(r"R_3 \to R_3 - R_4", font_size=32, color="#E88B8B")
            operacion.move_to([0, 1.9, 0])
            self.esperar(t.duration - 0.5)

        # --- Estado 4: R3 - R4 → R3 ---
        with self.voiceover(
            text="Paso cuatro. Ahora eliminamos hacia arriba. Quitamos el uno de la "
                 "tercera fila, cuarta columna, restando fila tres menos fila cuatro. "
                 "En A: cero, cero, uno, cero. En la identidad: dos, menos dos, dos, "
                 "menos uno."
        ) as t:
            self.play(FadeIn(operacion), run_time=0.5)
            A_4 = Matrix([[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
                         h_buff=0.45, v_buff=0.32)
            I_4 = Matrix([[1, 0, 0, 0], [-1, 1, 0, 0], [2, -2, 2, -1], [-1, 1, -1, 1]],
                         h_buff=0.45, v_buff=0.32)
            A_4.set_color("#2A4A6A")
            I_4.set_color("#2A4A6A")
            A_4.move_to(A_0.get_center())
            I_4.move_to(I_0.get_center())
            r_fila = SurroundingRectangle(
                VGroup(*[A_0.get_entries()[8 + k] for k in range(4)]),
                color=RED, buff=0.08,
            )
            self.play(Create(r_fila), run_time=0.6)
            self.play(ReplacementTransform(A_0, A_4),
                      ReplacementTransform(I_0, I_4),
                      run_time=min(t.duration * 0.3, 2))
            self.play(FadeOut(r_fila), run_time=0.4)
            self.esperar(t.duration - 3.5)
            A_0, I_0 = A_4, I_4

        with self.voiceover(text="Siguiente.") as t:
            self.play(FadeOut(operacion), run_time=0.5)
            operacion = MathTex(r"R_2 \to R_2 - R_3", font_size=32, color="#E88B8B")
            operacion.move_to([0, 1.9, 0])
            self.esperar(t.duration - 0.5)

        # --- Estado 5: R2 - R3 → R2 ---
        with self.voiceover(
            text="Paso cinco. Eliminamos el uno de la segunda fila, tercera columna. "
                 "Restamos fila dos menos fila tres. En A: cero, uno, cero, cero. "
                 "En la identidad: menos tres, tres, menos dos, uno."
        ) as t:
            self.play(FadeIn(operacion), run_time=0.5)
            A_5 = Matrix([[1, 1, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
                         h_buff=0.45, v_buff=0.32)
            I_5 = Matrix([[1, 0, 0, 0], [-3, 3, -2, 1], [2, -2, 2, -1], [-1, 1, -1, 1]],
                         h_buff=0.45, v_buff=0.32)
            A_5.set_color("#2A4A6A")
            I_5.set_color("#2A4A6A")
            A_5.move_to(A_0.get_center())
            I_5.move_to(I_0.get_center())
            r_fila = SurroundingRectangle(
                VGroup(*[A_0.get_entries()[4 + k] for k in range(4)]),
                color=RED, buff=0.08,
            )
            self.play(Create(r_fila), run_time=0.6)
            self.play(ReplacementTransform(A_0, A_5),
                      ReplacementTransform(I_0, I_5),
                      run_time=min(t.duration * 0.3, 2))
            self.play(FadeOut(r_fila), run_time=0.4)
            self.esperar(t.duration - 3.5)
            A_0, I_0 = A_5, I_5

        with self.voiceover(text="Último paso.") as t:
            self.play(FadeOut(operacion), run_time=0.5)
            operacion = MathTex(r"R_1 \to R_1 - R_2", font_size=32, color="#E88B8B")
            operacion.move_to([0, 1.9, 0])
            self.esperar(t.duration - 0.5)

        # --- Estado 6: R1 - R2 → R1 ---
        with self.voiceover(
            text="Paso seis, el último. Eliminamos el uno de la primera fila, segunda "
                 "columna, restando fila uno menos fila dos. En A: uno, cero, cero, "
                 "cero. En la identidad: cuatro, menos tres, dos, menos uno. ¡Y listo!"
        ) as t:
            self.play(FadeIn(operacion), run_time=0.5)
            A_6 = Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
                         h_buff=0.45, v_buff=0.32)
            I_6 = Matrix([[4, -3, 2, -1], [-3, 3, -2, 1], [2, -2, 2, -1], [-1, 1, -1, 1]],
                         h_buff=0.45, v_buff=0.32)
            A_6.set_color("#2A4A5C")
            I_6.set_color("#E88B8B")
            A_6.move_to(A_0.get_center())
            I_6.move_to(I_0.get_center())
            r_fila = SurroundingRectangle(
                VGroup(*[A_0.get_entries()[0 + k] for k in range(4)]),
                color=RED, buff=0.08,
            )
            self.play(Create(r_fila), run_time=0.6)
            self.play(ReplacementTransform(A_0, A_6),
                      ReplacementTransform(I_0, I_6),
                      run_time=min(t.duration * 0.3, 2))
            self.play(FadeOut(r_fila), run_time=0.4)
            self.esperar(t.duration - 3.5)
            A_0, I_0 = A_6, I_6

        with self.voiceover(
            text="A la izquierda ya tenemos la identidad, y a la derecha, en rojo, "
                 "está la inversa de A. Pueden verificar que A por esta matriz da la "
                 "identidad. Y ojo, todos los números quedaron enteros, sin "
                 "fracciones, lo cual es una suerte del ejemplo que elegí."
        ) as t:
            self.play(FadeOut(operacion), run_time=0.5)
            self.esperar(t.duration - 0.5)

        with self.voiceover(
            text="El método de Gauss-Jordan es muy poderoso: funciona para cualquier "
                 "matriz invertible, sin importar el tamaño. Puede ser 2 por 2, 3 por "
                 "3, 10 por 10, o más. Solo hay que tener paciencia y orden con las "
                 "operaciones."
        ) as t:
            self.play(
                FadeOut(VGroup(ej_nombre, label_A, label_I, A_0, I_0, linea_v)),
                run_time=min(t.duration * 0.4, 1.5),
            )
            self.esperar(t.duration - 1.5)

        # ==== Bloque 4: nota final sobre el determinante ====
        with self.voiceover(
            text="Antes de cerrar, un comentario importante. Existe otro método para "
                 "calcular la inversa, usando determinantes y lo que se llama la "
                 "matriz adjunta. La fórmula es: A inversa es igual a uno sobre el "
                 "determinante de A, por la adjunta de A."
        ) as t:
            self.play(FadeIn(nota_nombre), run_time=min(t.duration * 0.15, 0.8))
            self.play(FadeIn(nota_formula, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 2.3)

        with self.voiceover(
            text="Este método es muy eficiente para matrices pequeñas, de dos por dos "
                 "o de tres por tres, porque los cálculos son pocos. Pero para "
                 "matrices grandes, como la de cuatro por cuatro que acabamos de ver, "
                 "el método del determinante se vuelve impráctico, porque hay que "
                 "calcular muchísimos cofactores. En esos casos, Gauss-Jordan es "
                 "mucho más eficiente."
        ) as t:
            self.play(FadeIn(nota_texto, shift=DOWN * 0.3), run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="Así que ya lo saben: para matrices chiquitas, el método del "
                 "determinante es elegante y rápido. Para matrices grandes, "
                 "Gauss-Jordan es el camino. Vamos a ver el método del determinante "
                 "con todo detalle más adelante, cuando lleguemos al tema de "
                 "determinantes, que es justo el siguiente bloque."
        ) as t:
            self.play(FadeIn(nota_adelanto, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        # ---------- 4. CIERRE ----------
        self.play(
            FadeOut(VGroup(titulo, nota_nombre, nota_formula, nota_texto, nota_adelanto)),
            run_time=2,
        )

# ---------- Escena 09a: Determinante de 2x2 ----------
class D09a_Determinante2x2(CuadernoScene):
    def construct(self):
        # ---------- 1. OBJETOS ----------
        titulo = Text("Determinante de 2×2", font_size=42, color="#1A3A5C", weight=BOLD)

        # ===== Bloque 1: definición =====
        def_nombre = Text("Definición", font_size=30, color="#1A3A5C", weight=BOLD)
        def_texto = Tex(
            r"El \textbf{determinante} es un n\'umero asociado\\"
            r"a toda matriz cuadrada.",
            tex_environment="center", font_size=26,
        )
        def_texto.set_color("#2A4A6A")
        def_notacion = Tex(
            r"Se denota $\det(A)$ o tambi\'en $|A|$",
            tex_environment="center", font_size=26,
        )
        def_notacion.set_color("#4A6A8A")

        # ===== Bloque 2: fórmula general =====
        form_nombre = Text("Fórmula para 2×2", font_size=30, color="#1A3A5C", weight=BOLD)
        form_mat = Matrix([[r"a", r"b"], [r"c", r"d"]], h_buff=1.2, v_buff=0.8)
        form_mat.set_color("#2A4A6A")
        form_eq = MathTex(r"\det(A) = ad - bc", font_size=52, color="#1A3A5C")
        form_hint = Tex(
            r"Producto de la diagonal principal menos producto de la diagonal secundaria",
            tex_environment="center", font_size=22,
        )
        form_hint.set_color("#6A7A8A")

        # ===== Bloque 3: ejemplo numérico =====
        ej_nombre = Text("Ejemplo", font_size=30, color="#1A3A5C", weight=BOLD)
        ej_A = Matrix([[2, 1], [1, 2]], h_buff=1.2, v_buff=0.8)
        ej_A.set_color("#2A4A6A")
        ej_label = MathTex("A =", font_size=36, color="#1A3A5C")

        calc_principal = MathTex(r"(2)(2) = 4", font_size=32, color=RED)
        calc_secundaria = MathTex(r"(1)(1) = 1", font_size=32, color=BLUE)
        calc_total = MathTex(r"\det(A) = 4 - 1 = 3", font_size=40, color=TEAL)

        # ===== Bloque 4: interpretación geométrica =====
        geo_nombre = Text("Interpretación geométrica", font_size=30, color="#1A3A5C", weight=BOLD)
        geo_texto = Tex(
            r"El valor absoluto del determinante es\\"
            r"el \textbf{área} del paralelogramo formado\\"
            r"por los vectores columna de $A$",
            tex_environment="center", font_size=24,
        )
        geo_texto.set_color("#2A4A6A")
        geo_formula = MathTex(r"|\det(A)| = \text{Área}", font_size=36, color="#1A3A5C")

        # Vectores y paralelogramo (se configuran abajo)
        # Para A = [[2,1],[1,2]], los vectores columna son (2,1) y (1,2)
        origen_pt = np.array([-3.0, -1.8, 0])
        v1_pt = np.array([2.0, 1.0, 0])
        v2_pt = np.array([1.0, 2.0, 0])

        flecha_v1 = Arrow(
            start=origen_pt, end=origen_pt + v1_pt,
            color=RED, stroke_width=4, buff=0,
            max_tip_length_to_length_ratio=0.15,
        )
        flecha_v2 = Arrow(
            start=origen_pt, end=origen_pt + v2_pt,
            color=BLUE, stroke_width=4, buff=0,
            max_tip_length_to_length_ratio=0.15,
        )
        label_v1 = MathTex(r"\vec{v}_1", font_size=30, color=RED)
        label_v2 = MathTex(r"\vec{v}_2", font_size=30, color=BLUE)

        paralelogramo = Polygon(
            origen_pt,
            origen_pt + v1_pt,
            origen_pt + v1_pt + v2_pt,
            origen_pt + v2_pt,
            color=TEAL, stroke_width=2, fill_color=TEAL, fill_opacity=0.25,
        )

        area_label = MathTex(r"\text{Área} = 3", font_size=32, color=TEAL)

        # ===== Bloque 5: caso det = 0 =====
        cero_nombre = Text("Caso especial: determinante cero", font_size=28,
                          color="#1A3A5C", weight=BOLD)
        cero_texto = Tex(
            r"Si $\det(A) = 0$, los vectores columna son\\"
            r"\textbf{linealmente dependientes} (colineales)",
            tex_environment="center", font_size=24,
        )
        cero_texto.set_color("#2A4A6A")
        cero_mat = Matrix([[1, 2], [2, 4]], h_buff=1.2, v_buff=0.8)
        cero_mat.set_color("#2A4A6A")
        cero_calc = MathTex(r"\det = (1)(4) - (2)(2) = 0", font_size=32, color=RED)

        cero_origen = np.array([-3.0, -1.8, 0])
        cero_v1 = np.array([1.0, 2.0, 0])
        cero_v2 = np.array([2.0, 4.0, 0])
        cero_flecha_v1 = Arrow(
            start=cero_origen, end=cero_origen + cero_v1,
            color=RED, stroke_width=4, buff=0,
            max_tip_length_to_length_ratio=0.15,
        )
        cero_flecha_v2 = Arrow(
            start=cero_origen, end=cero_origen + cero_v2,
            color=BLUE, stroke_width=4, buff=0,
            max_tip_length_to_length_ratio=0.15,
        )
        cero_area = MathTex(r"\text{Área} = 0", font_size=32, color=RED)

        cero_conclusion = Tex(
            r"La matriz es \textbf{singular}: no tiene inversa",
            tex_environment="center", font_size=26,
        )
        cero_conclusion.set_color("#E88B8B")

        # ---------- 2. CONFIGURACIÓN ----------
        titulo.move_to([0, 0, 0])
        titulo_final = titulo.copy().scale(0.7).move_to([0, 3.6, 0])

        # Bloque 1
        def_nombre.move_to([0, 2.6, 0])
        def_texto.move_to([0, 1.4, 0])
        def_notacion.move_to([0, 0.2, 0])

        # Bloque 2
        form_nombre.move_to([0, 2.6, 0])
        form_mat.move_to([-2.5, 0.8, 0])
        form_eq.move_to([2.3, 0.8, 0])
        form_hint.move_to([0, -0.6, 0])

        # Bloque 3
        ej_nombre.move_to([0, 2.6, 0])
        ej_label.move_to([-3.0, 1.0, 0])
        ej_A.move_to([-1.8, 1.0, 0])
        calc_principal.move_to([2.8, 1.5, 0])
        calc_secundaria.move_to([2.8, 0.7, 0])
        calc_total.move_to([0, -0.7, 0])

        # Bloque 4
        geo_nombre.move_to([0, 2.6, 0])
        geo_texto.move_to([2.2, 1.4, 0])
        geo_formula.move_to([2.2, -0.4, 0])
        label_v1.move_to(origen_pt + v1_pt + np.array([0.4, 0.1, 0]))
        label_v2.move_to(origen_pt + v2_pt + np.array([0.3, -0.3, 0]))
        area_label.move_to(origen_pt + (v1_pt + v2_pt) / 2 + np.array([0.5, 0.3, 0]))

        # Bloque 5
        cero_nombre.move_to([0, 2.6, 0])
        cero_texto.move_to([2.2, 1.4, 0])
        cero_mat.move_to([-3.4, 0.6, 0])
        cero_calc.move_to([2.2, 0.4, 0])
        cero_area.move_to(cero_origen + cero_v1 * 0.5 + np.array([-1.0, 0.4, 0]))
        cero_conclusion.move_to([0, -1.4, 0])

        # ---------- 3. ANIMACIONES ----------
        self.set_speech_service(EdgeTTSService(voice="es-MX-JorgeNeural"))

        # ==== Intro + definición ====
        with self.voiceover(
            text="Muy bien, ahora entramos al tema de determinantes. Este es uno de "
                 "los conceptos más importantes de todo el álgebra lineal."
        ) as t:
            self.play(Write(titulo), run_time=min(t.duration, 2.5))
            self.esperar(t.duration - 2.5)

        with self.voiceover(text="Empecemos con la definición.") as t:
            self.play(Transform(titulo, titulo_final), run_time=min(t.duration, 1.5))
            self.play(FadeIn(def_nombre), run_time=min(t.duration * 0.25, 0.8))
            self.esperar(t.duration - 2.3)

        with self.voiceover(
            text="El determinante es un número que se asocia a toda matriz cuadrada. "
                 "Es decir, solo tiene sentido para matrices que tienen el mismo "
                 "número de filas que de columnas."
        ) as t:
            self.play(FadeIn(def_texto, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="Se denota de dos formas: det de A, o también con dos barras "
                 "verticales alrededor de la matriz, como el valor absoluto, pero no "
                 "es lo mismo: aquí son barras de determinante."
        ) as t:
            self.play(FadeIn(def_notacion, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(text="Vamos con la fórmula para el caso 2 por 2.") as t:
            self.play(FadeOut(VGroup(def_nombre, def_texto, def_notacion)),
                      run_time=min(t.duration, 1.5))
            self.esperar(t.duration - 1.5)

        # ==== Bloque 2: fórmula ====
        with self.voiceover(
            text="Si tenemos una matriz de dos por dos, con entradas a, b, c, d, "
                 "el determinante se calcula como a por d, menos b por c."
        ) as t:
            self.play(FadeIn(form_nombre), run_time=min(t.duration * 0.15, 0.8))
            self.play(FadeIn(form_mat), run_time=min(t.duration * 0.2, 1.2))
            self.play(FadeIn(form_eq), run_time=min(t.duration * 0.2, 1.2))
            self.esperar(t.duration - 3.2)

        with self.voiceover(
            text="En palabras: producto de la diagonal principal, menos producto de "
                 "la diagonal secundaria."
        ) as t:
            self.play(FadeIn(form_hint, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        # Resaltar diagonal principal (a, d) y secundaria (b, c)
        with self.voiceover(text="Fíjense en las dos diagonales.") as t:
            diag_principal = Line(
                form_mat.get_entries()[0].get_center(),
                form_mat.get_entries()[3].get_center(),
                color=RED, stroke_width=3,
            )
            diag_secundaria = Line(
                form_mat.get_entries()[1].get_center(),
                form_mat.get_entries()[2].get_center(),
                color=BLUE, stroke_width=3,
            )
            self.play(Create(diag_principal), run_time=min(t.duration * 0.3, 1.0))
            self.play(Create(diag_secundaria), run_time=min(t.duration * 0.3, 1.0))
            self.esperar(t.duration - 2.0)

        with self.voiceover(text="La roja suma, la azul resta.") as t:
            self.esperar(t.duration)

        with self.voiceover(text="Veamos un ejemplo.") as t:
            self.play(FadeOut(VGroup(form_nombre, form_mat, form_eq, form_hint,
                                     diag_principal, diag_secundaria)),
                      run_time=min(t.duration, 1.5))
            self.esperar(t.duration - 1.5)

        # ==== Bloque 3: ejemplo ====
        with self.voiceover(
            text="Aquí tenemos la matriz A, con entradas dos, uno, uno, dos. Vamos a "
                 "calcular su determinante."
        ) as t:
            self.play(FadeIn(ej_nombre), run_time=min(t.duration * 0.15, 0.8))
            self.play(FadeIn(ej_label), FadeIn(ej_A), run_time=min(t.duration * 0.2, 1.2))
            self.esperar(t.duration - 2.0)

        with self.voiceover(
            text="La diagonal principal: dos por dos, igual a cuatro."
        ) as t:
            r_a = SurroundingRectangle(ej_A.get_entries()[0], color=RED, buff=0.1)
            r_d = SurroundingRectangle(ej_A.get_entries()[3], color=RED, buff=0.1)
            self.play(Create(r_a), Create(r_d), run_time=min(t.duration * 0.2, 1.2))
            self.play(FadeIn(calc_principal), run_time=min(t.duration * 0.2, 1.0))
            self.esperar(t.duration - 2.2)
            self.play(FadeOut(r_a), FadeOut(r_d), run_time=0.5)

        with self.voiceover(
            text="La diagonal secundaria: uno por uno, igual a uno."
        ) as t:
            r_b = SurroundingRectangle(ej_A.get_entries()[1], color=BLUE, buff=0.1)
            r_c = SurroundingRectangle(ej_A.get_entries()[2], color=BLUE, buff=0.1)
            self.play(Create(r_b), Create(r_c), run_time=min(t.duration * 0.2, 1.2))
            self.play(FadeIn(calc_secundaria), run_time=min(t.duration * 0.2, 1.0))
            self.esperar(t.duration - 2.2)
            self.play(FadeOut(r_b), FadeOut(r_c), run_time=0.5)

        with self.voiceover(
            text="Entonces, el determinante es cuatro menos uno, igual a tres."
        ) as t:
            self.play(FadeIn(calc_total, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.4, 1.8))
            self.esperar(t.duration - 1.8)

        with self.voiceover(
            text="Perfecto, el determinante de esta matriz es tres."
        ) as t:
            self.play(
                FadeOut(VGroup(ej_nombre, ej_label, ej_A,
                               calc_principal, calc_secundaria, calc_total)),
                run_time=min(t.duration, 1.5),
            )
            self.esperar(t.duration - 1.5)

        # ==== Bloque 4: interpretación geométrica ====
        with self.voiceover(
            text="Ahora, ¿qué significa geométricamente este número tres? Pues "
                 "resulta que el valor absoluto del determinante es exactamente el "
                 "área del paralelogramo que forman los vectores columna de la matriz."
        ) as t:
            self.play(FadeIn(geo_nombre), run_time=min(t.duration * 0.1, 0.6))
            self.play(FadeIn(geo_texto, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 2.1)

        with self.voiceover(
            text="Los vectores columna de nuestra matriz A son: el vector v uno, que "
                 "es dos coma uno, y el vector v dos, que es uno coma dos."
        ) as t:
            self.play(Create(flecha_v1), run_time=min(t.duration * 0.15, 1.0))
            self.play(FadeIn(label_v1), run_time=min(t.duration * 0.1, 0.6))
            self.play(Create(flecha_v2), run_time=min(t.duration * 0.15, 1.0))
            self.play(FadeIn(label_v2), run_time=min(t.duration * 0.1, 0.6))
            self.esperar(t.duration - 3.2)

        with self.voiceover(
            text="Si los dibujamos desde el mismo origen, forman un paralelogramo. Y "
                 "el área de ese paralelogramo es exactamente el valor absoluto del "
                 "determinante, o sea tres."
        ) as t:
            self.play(Create(paralelogramo), run_time=min(t.duration * 0.3, 1.8))
            self.play(FadeIn(geo_formula), run_time=min(t.duration * 0.2, 1.0))
            self.play(FadeIn(area_label), run_time=min(t.duration * 0.15, 0.8))
            self.esperar(t.duration - 3.6)

        with self.voiceover(text="Eso es muy importante.") as t:
            self.esperar(t.duration)

        with self.voiceover(
            text="Ahora, ¿qué pasa si el determinante es cero? Vamos a verlo."
        ) as t:
            self.play(
                FadeOut(VGroup(geo_nombre, geo_texto, geo_formula,
                               flecha_v1, flecha_v2, label_v1, label_v2,
                               paralelogramo, area_label)),
                run_time=min(t.duration, 1.5),
            )
            self.esperar(t.duration - 1.5)

        # ==== Bloque 5: caso det = 0 ====
        with self.voiceover(
            text="Consideremos esta otra matriz, con entradas uno, dos, dos, cuatro. "
                 "Si calculamos el determinante: uno por cuatro, cuatro, menos dos por "
                 "dos, cuatro. Cuatro menos cuatro es cero."
        ) as t:
            self.play(FadeIn(cero_nombre), run_time=min(t.duration * 0.1, 0.6))
            self.play(FadeIn(cero_mat), run_time=min(t.duration * 0.15, 1.0))
            self.play(FadeIn(cero_calc, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.8))
            self.esperar(t.duration - 3.4)

        with self.voiceover(
            text="¿Qué significa esto geométricamente? Los vectores columna son uno "
                 "coma dos, y dos coma cuatro. Pero fíjense: el segundo vector es "
                 "exactamente el doble del primero. Son colineales."
        ) as t:
            self.play(Create(cero_flecha_v1), run_time=min(t.duration * 0.15, 1.0))
            self.play(Create(cero_flecha_v2), run_time=min(t.duration * 0.15, 1.0))
            self.esperar(t.duration - 2.0)

        with self.voiceover(
            text="Entonces, el paralelogramo no es un paralelogramo de verdad: es "
                 "solo una línea. Su área es cero. Y eso coincide con el determinante."
        ) as t:
            self.play(FadeIn(cero_area), run_time=min(t.duration * 0.2, 1.0))
            self.esperar(t.duration - 1.0)

        with self.voiceover(
            text="Cuando esto pasa, decimos que la matriz es singular, y no tiene "
                 "inversa. Es decir, la condición det distinto de cero que "
                 "mencionamos en la escena de la inversa, ahora ya sabemos de dónde "
                 "viene: el determinante mide si los vectores columna son linealmente "
                 "independientes o no."
        ) as t:
            self.play(FadeIn(cero_conclusion, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="Así que ya lo saben: el determinante es un número muy importante, "
                 "con una interpretación geométrica muy clara: mide áreas en el caso "
                 "de dos por dos, y volúmenes en dimensiones más altas. Y cuando vale "
                 "cero, algo se degenera."
        ) as t:
            self.esperar(t.duration)

        # ---------- 4. CIERRE ----------
        self.play(
            FadeOut(VGroup(titulo, cero_nombre, cero_mat, cero_calc,
                           cero_flecha_v1, cero_flecha_v2, cero_area,
                           cero_conclusion)),
            run_time=2,
        )

# ---------- Escena 09b: Determinante de 3x3 (Regla de Sarrus) ----------
class D09b_Determinante3x3(CuadernoScene):
    def construct(self):
        # ---------- 1. OBJETOS ----------
        titulo = Text("Determinante de 3×3", font_size=42, color="#1A3A5C", weight=BOLD)

        # ===== Bloque 1: intro =====
        intro_nombre = Text("Regla de Sarrus", font_size=30, color="#1A3A5C", weight=BOLD)
        intro_texto = Tex(
            r"Para 3$\times$3 no hay una f\'ormula tan simple\\"
            r"como $ad - bc$. Usamos la \textbf{regla de Sarrus}.",
            tex_environment="center", font_size=26,
        )
        intro_texto.set_color("#2A4A6A")

        pasos_label = Text("¿Cómo funciona?", font_size=26, color="#6A7A8A", weight=BOLD)
        paso1 = Tex(r"1. Copiamos las dos primeras columnas a la derecha",
                    tex_environment="center", font_size=24)
        paso2 = Tex(r"2. Trazamos 3 diagonales descendentes (suman)",
                    tex_environment="center", font_size=24)
        paso3 = Tex(r"3. Trazamos 3 diagonales ascendentes (restan)",
                    tex_environment="center", font_size=24)
        for p in [paso1, paso2, paso3]:
            p.set_color("#2A4A6A")
        pasos = VGroup(paso1, paso2, paso3).arrange(DOWN, center=True, buff=0.25)

        # ===== Bloque 2: matriz extendida =====
        ej_nombre = Text("Ejemplo", font_size=30, color="#1A3A5C", weight=BOLD)

        mat_ext = Matrix([
            [1, 2, 3, 1, 2],
            [4, 5, 6, 4, 5],
            [7, 8, 10, 7, 8],
        ], h_buff=0.55, v_buff=0.4)
        mat_ext.set_color("#2A4A6A")

        # Columnas 4 y 5 en gris claro (son copias)
        for i in [3, 4, 8, 9, 13, 14]:
            mat_ext.get_entries()[i].set_color("#B0B0B0")

        # Productos positivos
        prod_pos_1 = MathTex(r"(1)(5)(10) = 50", font_size=26, color=RED)
        prod_pos_2 = MathTex(r"(2)(6)(7) = 84", font_size=26, color=RED)
        prod_pos_3 = MathTex(r"(3)(4)(8) = 96", font_size=26, color=RED)
        prods_pos = VGroup(prod_pos_1, prod_pos_2, prod_pos_3).arrange(RIGHT, buff=0.8)

        suma_pos = MathTex(r"50 + 84 + 96 = 230", font_size=34, color=RED)

        # Productos negativos
        prod_neg_1 = MathTex(r"(3)(5)(7) = 105", font_size=26, color=BLUE)
        prod_neg_2 = MathTex(r"(1)(6)(8) = 48", font_size=26, color=BLUE)
        prod_neg_3 = MathTex(r"(2)(4)(10) = 80", font_size=26, color=BLUE)
        prods_neg = VGroup(prod_neg_1, prod_neg_2, prod_neg_3).arrange(RIGHT, buff=0.8)

        suma_neg = MathTex(r"105 + 48 + 80 = 233", font_size=34, color=BLUE)

        # Resultado final
        resultado = MathTex(r"\det(A) = 230 - 233 = -3", font_size=42, color=TEAL)

        # ===== Bloque 3: interpretación 3D =====
        geo_nombre = Text("Interpretación geométrica", font_size=30, color="#1A3A5C", weight=BOLD)
        geo_formula = MathTex(r"|\det(A)| = \text{Volumen del paralelep\'ipedo}",
                              font_size=36, color="#1A3A5C")
        geo_nota = Tex(
            r"Formado por los 3 vectores columna de la matriz",
            tex_environment="center", font_size=24,
        )
        geo_nota.set_color("#4A6A8A")

        # ===== Bloque 4: advertencia =====
        adv_nombre = Text("Ojo con el tamaño", font_size=30, color="#1A3A5C", weight=BOLD)
        adv_texto = Tex(
            r"La regla de Sarrus \textbf{solo funciona para 3$\times$3}.\\"
            r"Para matrices m\'as grandes necesitamos\\"
            r"otro m\'etodo: los \textbf{cofactores}.",
            tex_environment="center", font_size=26,
        )
        adv_texto.set_color("#2A4A6A")
        adv_prox = Tex(r"Eso lo veremos a continuaci\'on",
                       tex_environment="center", font_size=24)
        adv_prox.set_color("#E88B8B")

        # ---------- 2. CONFIGURACIÓN ----------
        titulo.move_to([0, 0, 0])
        titulo_final = titulo.copy().scale(0.7).move_to([0, 3.6, 0])

        # Bloque 1
        intro_nombre.move_to([0, 2.6, 0])
        intro_texto.move_to([0, 1.6, 0])
        pasos_label.move_to([-4.0, 0.4, 0])
        pasos.move_to([0.8, -0.2, 0])

        # Bloque 2
        ej_nombre.move_to([0, 2.6, 0])
        mat_ext.move_to([0, 1.4, 0])
        prods_pos.move_to([0, -0.4, 0])
        suma_pos.move_to([0, -1.2, 0])
        prods_neg.move_to([0, -0.4, 0])
        suma_neg.move_to([0, -1.2, 0])
        resultado.move_to([0, 0.0, 0])

        # Bloque 3
        geo_nombre.move_to([0, 2.4, 0])
        geo_formula.move_to([0, 1.0, 0])
        geo_nota.move_to([0, -0.2, 0])

        # Bloque 4
        adv_nombre.move_to([0, 2.4, 0])
        adv_texto.move_to([0, 0.8, 0])
        adv_prox.move_to([0, -1.0, 0])

        # ---------- 3. ANIMACIONES ----------
        self.set_speech_service(EdgeTTSService(voice="es-MX-JorgeNeural"))

        # ==== Intro ====
        with self.voiceover(
            text="Muy bien, ahora el caso 3 por 3. Para 2 por 2 teníamos la fórmula "
                 "sencilla a d menos b c, pero para 3 por 3 no hay una fórmula tan "
                 "simple. En su lugar, usamos la regla de Sarrus."
        ) as t:
            self.play(Write(titulo), run_time=min(t.duration, 2.5))
            self.esperar(t.duration - 2.5)

        with self.voiceover(text="¿Cómo funciona la regla de Sarrus?") as t:
            self.play(Transform(titulo, titulo_final), run_time=min(t.duration, 1.5))
            self.play(FadeIn(intro_nombre), run_time=min(t.duration * 0.2, 0.8))
            self.esperar(t.duration - 2.3)

        with self.voiceover(
            text="El procedimiento tiene tres pasos."
        ) as t:
            self.play(FadeIn(intro_texto, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.2, 1.2))
            self.play(FadeIn(pasos_label), run_time=min(t.duration * 0.1, 0.6))
            self.esperar(t.duration - 1.8)

        with self.voiceover(
            text="Paso uno: copiamos las dos primeras columnas a la derecha de la "
                 "matriz. Es decir, la matriz se extiende y queda de tres por cinco."
        ) as t:
            self.play(FadeIn(paso1, shift=DOWN * 0.3), run_time=min(t.duration * 0.3, 1.2))
            self.esperar(t.duration - 1.2)

        with self.voiceover(
            text="Paso dos: trazamos tres diagonales descendentes, que van de "
                 "izquierda a derecha y hacia abajo. Los productos de esas diagonales "
                 "suman."
        ) as t:
            self.play(FadeIn(paso2, shift=DOWN * 0.3), run_time=min(t.duration * 0.3, 1.2))
            self.esperar(t.duration - 1.2)

        with self.voiceover(
            text="Paso tres: trazamos tres diagonales ascendentes, que van hacia "
                 "arriba. Esos productos restan."
        ) as t:
            self.play(FadeIn(paso3, shift=DOWN * 0.3), run_time=min(t.duration * 0.3, 1.2))
            self.esperar(t.duration - 1.2)

        with self.voiceover(text="Veamos un ejemplo completo.") as t:
            self.play(FadeOut(VGroup(intro_nombre, intro_texto, pasos_label, pasos)),
                      run_time=min(t.duration, 1.5))
            self.esperar(t.duration - 1.5)

        # ==== Matriz extendida ====
        with self.voiceover(
            text="Aquí tenemos nuestra matriz de tres por tres. La extendemos "
                 "copiando las dos primeras columnas a la derecha. Fíjense que las "
                 "columnas copiadas están en un tono más clarito, para distinguirlas "
                 "de las originales."
        ) as t:
            self.play(FadeIn(ej_nombre), run_time=min(t.duration * 0.1, 0.6))
            self.play(Write(mat_ext), run_time=min(t.duration * 0.4, 2.5))
            self.esperar(t.duration - 3.1)

        # ==== Diagonales descendentes (positivas) ====
        with self.voiceover(
            text="Empecemos con las diagonales descendentes. Son tres, y sus "
                 "productos van a sumar."
        ) as t:
            # Diagonal 1 (roja): 0 -> 6 -> 12
            d1 = Line(
                mat_ext.get_entries()[0].get_center(),
                mat_ext.get_entries()[12].get_center(),
                color=RED, stroke_width=2.5,
            )
            self.play(Create(d1), run_time=min(t.duration * 0.2, 1.2))
            self.esperar(t.duration - 1.2)

        with self.voiceover(
            text="Primera diagonal: uno por cinco por diez, igual a cincuenta."
        ) as t:
            self.play(FadeIn(prod_pos_1), run_time=min(t.duration * 0.4, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="Segunda diagonal: dos por seis por siete, igual a ochenta y cuatro."
        ) as t:
            d2 = Line(
                mat_ext.get_entries()[1].get_center(),
                mat_ext.get_entries()[13].get_center(),
                color=RED, stroke_width=2.5,
            )
            self.play(Create(d2), run_time=min(t.duration * 0.2, 1.0))
            self.play(FadeIn(prod_pos_2), run_time=min(t.duration * 0.3, 1.2))
            self.esperar(t.duration - 2.2)

        with self.voiceover(
            text="Tercera diagonal: tres por cuatro por ocho, igual a noventa y seis."
        ) as t:
            d3 = Line(
                mat_ext.get_entries()[2].get_center(),
                mat_ext.get_entries()[14].get_center(),
                color=RED, stroke_width=2.5,
            )
            self.play(Create(d3), run_time=min(t.duration * 0.2, 1.0))
            self.play(FadeIn(prod_pos_3), run_time=min(t.duration * 0.3, 1.2))
            self.esperar(t.duration - 2.2)

        with self.voiceover(
            text="Sumamos los tres productos positivos: cincuenta más ochenta y "
                 "cuatro más noventa y seis, es doscientos treinta."
        ) as t:
            self.play(FadeIn(suma_pos, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.4, 1.8))
            self.esperar(t.duration - 1.8)

        # ==== Diagonales ascendentes (negativas) ====
        with self.voiceover(
            text="Ahora vamos con las diagonales ascendentes. Estas van hacia arriba, "
                 "y sus productos restan."
        ) as t:
            self.play(FadeOut(d1), FadeOut(d2), FadeOut(d3),
                      FadeOut(prods_pos), FadeOut(suma_pos),
                      run_time=min(t.duration * 0.3, 1.2))
            self.esperar(t.duration - 1.2)

        with self.voiceover(
            text="Primera diagonal ascendente: tres por cinco por siete, igual a "
                 "ciento cinco."
        ) as t:
            a1 = Line(
                mat_ext.get_entries()[10].get_center(),
                mat_ext.get_entries()[2].get_center(),
                color=BLUE, stroke_width=2.5,
            )
            self.play(Create(a1), run_time=min(t.duration * 0.2, 1.2))
            self.play(FadeIn(prod_neg_1), run_time=min(t.duration * 0.3, 1.2))
            self.esperar(t.duration - 2.4)

        with self.voiceover(
            text="Segunda: uno por seis por ocho, igual a cuarenta y ocho."
        ) as t:
            a2 = Line(
                mat_ext.get_entries()[11].get_center(),
                mat_ext.get_entries()[3].get_center(),
                color=BLUE, stroke_width=2.5,
            )
            self.play(Create(a2), run_time=min(t.duration * 0.2, 1.0))
            self.play(FadeIn(prod_neg_2), run_time=min(t.duration * 0.3, 1.2))
            self.esperar(t.duration - 2.2)

        with self.voiceover(
            text="Tercera: dos por cuatro por diez, igual a ochenta."
        ) as t:
            a3 = Line(
                mat_ext.get_entries()[12].get_center(),
                mat_ext.get_entries()[4].get_center(),
                color=BLUE, stroke_width=2.5,
            )
            self.play(Create(a3), run_time=min(t.duration * 0.2, 1.0))
            self.play(FadeIn(prod_neg_3), run_time=min(t.duration * 0.3, 1.2))
            self.esperar(t.duration - 2.2)

        with self.voiceover(
            text="Sumamos estos tres productos negativos: ciento cinco más cuarenta "
                 "y ocho más ochenta, es doscientos treinta y tres."
        ) as t:
            self.play(FadeIn(suma_neg, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.4, 1.8))
            self.esperar(t.duration - 1.8)

        # ==== Resultado final ====
        with self.voiceover(
            text="Entonces, el determinante es la diferencia: doscientos treinta "
                 "menos doscientos treinta y tres, igual a menos tres."
        ) as t:
            self.play(
                FadeOut(mat_ext), FadeOut(a1), FadeOut(a2), FadeOut(a3),
                FadeOut(prods_neg), FadeOut(suma_neg), FadeOut(ej_nombre),
                run_time=min(t.duration * 0.3, 1.2),
            )
            self.play(FadeIn(resultado, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.4, 2.0))
            self.esperar(t.duration - 3.2)

        with self.voiceover(
            text="Perfecto. El determinante de esta matriz es menos tres. Un número "
                 "negativo, lo cual es completamente normal. El signo no importa para "
                 "el área o el volumen, solo nos dice orientación."
        ) as t:
            self.esperar(t.duration)

        with self.voiceover(text="Bien, ahora la interpretación geométrica.") as t:
            self.play(FadeOut(resultado), run_time=min(t.duration, 1.5))
            self.esperar(t.duration - 1.5)

        # ==== Interpretación 3D ====
        with self.voiceover(
            text="Al igual que en el caso 2 por 2, donde el determinante medía el "
                 "área de un paralelogramo, en el caso 3 por 3 el valor absoluto del "
                 "determinante mide el volumen de un paralelepípedo."
        ) as t:
            self.play(FadeIn(geo_nombre), run_time=min(t.duration * 0.15, 0.8))
            self.play(FadeIn(geo_formula, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 2.3)

        with self.voiceover(
            text="Este paralelepípedo está formado por los tres vectores columna de "
                 "la matriz. Si los tres vectores son linealmente independientes, el "
                 "volumen es distinto de cero y el determinante también. Si son "
                 "dependientes, todo se aplana, el volumen es cero, y el determinante "
                 "también es cero."
        ) as t:
            self.play(FadeIn(geo_nota, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="Es la misma idea que en 2D, solo que ahora en tres dimensiones: el "
                 "determinante mide cómo se estiran o se aplastan los vectores."
        ) as t:
            self.esperar(t.duration)

        with self.voiceover(text="Antes de cerrar, una advertencia importante.") as t:
            self.play(FadeOut(VGroup(geo_nombre, geo_formula, geo_nota)),
                      run_time=min(t.duration, 1.5))
            self.esperar(t.duration - 1.5)

        # ==== Advertencia ====
        with self.voiceover(
            text="La regla de Sarrus solo funciona para matrices de tres por tres. No "
                 "se puede aplicar a matrices de cuatro por cuatro, cinco por cinco, o "
                 "más grandes. Para esos casos necesitamos otro método."
        ) as t:
            self.play(FadeIn(adv_nombre), run_time=min(t.duration * 0.15, 0.8))
            self.play(FadeIn(adv_texto, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 2.3)

        with self.voiceover(
            text="Ese método se llama expansión por cofactores, y es lo que vamos a "
                 "ver a continuación."
        ) as t:
            self.play(FadeIn(adv_prox, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="Así que ya lo saben: Sarrus es muy cómoda para 3 por 3, pero tiene "
                 "sus límites. Vamos con los cofactores."
        ) as t:
            self.esperar(t.duration)

        # ---------- 4. CIERRE ----------
        self.play(
            FadeOut(VGroup(titulo, adv_nombre, adv_texto, adv_prox)),
            run_time=2,
        )

# ---------- Escena 10: Determinantes por cofactores ----------
class D10_Cofactores(CuadernoScene):
    def construct(self):
        # ---------- 1. OBJETOS ----------
        titulo = Text("Determinantes por cofactores", font_size=42, color="#1A3A5C", weight=BOLD)

        # ===== Bloque 1: menor complementario =====
        menor_nombre = Text("Menor complementario Mᵢⱼ", font_size=28, color="#1A3A5C", weight=BOLD)
        menor_def = Tex(
            r"El \textbf{menor} $M_{ij}$ es el determinante de la\\"
            r"submatriz que queda al eliminar la fila $i$\\"
            r"y la columna $j$.",
            tex_environment="center", font_size=24,
        )
        menor_def.set_color("#2A4A6A")

        # Matriz 3x3 para mostrar el menor
        mat_A = Matrix([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 10],
        ], h_buff=1.0, v_buff=0.7)
        mat_A.set_color("#2A4A6A")
        mat_label = MathTex("A =", font_size=34, color="#1A3A5C")

        # Tachado para M_11: eliminar fila 1 y columna 1
        tacha_fila1 = Line(
            mat_A.get_entries()[0].get_center() + np.array([-0.5, 0, 0]),
            mat_A.get_entries()[2].get_center() + np.array([0.4, 0, 0]),
            color=RED, stroke_width=5,
        ).move_to([-2, 0.2, 0])
        tacha_col1 = Line(
            mat_A.get_entries()[0].get_center() + np.array([0, 0.4, 0]),
            mat_A.get_entries()[6].get_center() + np.array([0, -0.4, 0]),
            color=RED, stroke_width=5,
        ).move_to([-2.75,-0.5,0])

        submat_label = Tex(r"Submatriz de $M_{11}$:",
                          tex_environment="center", font_size=24)
        submat_label.set_color("#6A7A8A")

        submat = Matrix([[5, 6], [8, 10]], h_buff=1.0, v_buff=0.7)
        submat.set_color("#2A4A6A")

        menor_calc = MathTex(r"M_{11} = (5)(10) - (6)(8) = 2",
                            font_size=30, color=TEAL)

        # ===== Bloque 2: cofactor =====
        cof_nombre = Text("Cofactor Cᵢⱼ", font_size=28, color="#1A3A5C", weight=BOLD)
        cof_formula = MathTex(
            r"C_{ij} = (-1)^{i+j} \cdot M_{ij}",
            font_size=44, color="#1A3A5C",
        )
        cof_nota = Tex(
            r"El cofactor es el menor con un \textbf{signo}\\" 
            r"seg\'un la posici\'on $(i,j)$",
            tex_environment="center", font_size=24,
        )
        cof_nota.set_color("#4A6A8A")

        # Tabla de signos
        tabla_label = Text("Tabla de signos de (-1)^(i+j)", font_size=26,
                          color="#1A3A5C", weight=BOLD)
        signos_pos = MathTex(r"+", font_size=48, color=TEAL)
        signos_neg = MathTex(r"-", font_size=48, color=RED)
        signos_11 = signos_pos.copy()
        signos_12 = signos_neg.copy()
        signos_13 = signos_pos.copy()
        signos_21 = signos_neg.copy()
        signos_22 = signos_pos.copy()
        signos_23 = signos_neg.copy()
        signos_31 = signos_pos.copy()
        signos_32 = signos_neg.copy()
        signos_33 = signos_pos.copy()

        signos_fila1 = VGroup(signos_11, signos_12, signos_13).arrange(RIGHT, buff=1.2)
        signos_fila2 = VGroup(signos_21, signos_22, signos_23).arrange(RIGHT, buff=1.2)
        signos_fila3 = VGroup(signos_31, signos_32, signos_33).arrange(RIGHT, buff=1.2)
        tabla_signos = VGroup(signos_fila1, signos_fila2, signos_fila3).arrange(DOWN, buff=0.3)

        # ===== Bloque 3: fórmula de expansión =====
        exp_nombre = Text("Expansión por cofactores", font_size=28,
                          color="#1A3A5C", weight=BOLD)
        exp_formula = MathTex(
            r"\det(A) = \sum_{j=1}^{n} a_{ij} \cdot C_{ij}",
            font_size=42, color="#1A3A5C",
        )
        exp_nota = Tex(
            r"Elegimos una fila $i$ y sumamos: cada entrada\\"
            r"por su cofactor correspondiente",
            tex_environment="center", font_size=24,
        )
        exp_nota.set_color("#4A6A8A")
        exp_hint = Tex(
            r"Tambi\'en se puede expandir por una columna",
            tex_environment="center", font_size=22,
        )
        exp_hint.set_color("#6A7A8A")

        # ===== Bloque 4: ejemplo paso a paso =====
        ej_nombre = Text("Ejemplo por la primera fila", font_size=28,
                        color="#1A3A5C", weight=BOLD)

        mat_ej = Matrix([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 10],
        ], h_buff=0.7, v_buff=0.5)
        mat_ej.set_color("#2A4A6A")

        formula_desc = MathTex(
            r"\det(A) = a_{11}C_{11} + a_{12}C_{12} + a_{13}C_{13}",
            font_size=30, color="#1A3A5C",
        )

        calc_C11 = MathTex(
            r"C_{11} = (+1)\, M_{11} = +2",
            font_size=26, color=TEAL,
        )
        calc_C12 = MathTex(
            r"C_{12} = (-1)\, M_{12} = -(-2) = +2",
            font_size=26, color=RED,
        )
        calc_C13 = MathTex(
            r"C_{13} = (+1)\, M_{13} = +(-3) = -3",
            font_size=26, color=TEAL,
        )

        calc_total_1 = MathTex(
            r"\det(A) = (1)(2) + (2)(2) + (3)(-3)",
            font_size=30, color="#1A3A5C",
        )
        calc_total_2 = MathTex(
            r"\det(A) = 2 + 4 - 9 = -3",
            font_size=34, color=TEAL,
        )

        verificacion = Tex(
            r"\checkmark{} Coincide con la regla de Sarrus",
            tex_environment="center", font_size=26,
        )
        verificacion.set_color(TEAL)

        # ===== Bloque 5: ventaja =====
        vent_nombre = Text("¿Por qué usar cofactores?", font_size=28,
                          color="#1A3A5C", weight=BOLD)
        vent_texto = Tex(
            r"Funciona para \textbf{cualquier orden} $n \geq 3$.\\"
            r"Sarrus solo sirve para 3$\times$3.\\"
            r"Los cofactores, combinados con propiedades,\\"
            r"son la base del m\'etodo general.",
            tex_environment="center", font_size=24,
        )
        vent_texto.set_color("#2A4A6A")
        vent_tip = Tex(
            r"Truco: expandir por la fila o columna con m\'as ceros",
            tex_environment="center", font_size=22,
        )
        vent_tip.set_color("#E88B8B")

        # ---------- 2. CONFIGURACIÓN ----------
        titulo.move_to([0, 0, 0])
        titulo_final = titulo.copy().scale(0.7).move_to([0, 3.6, 0])

        # Bloque 1
        menor_nombre.move_to([0, 2.6, 0])
        menor_def.move_to([0, 1.5, 0])
        mat_label.move_to([-3.4, -0.5, 0])
        mat_A.move_to([-1.8, -0.5, 0])
        submat_label.move_to([2.8, 0.2, 0])
        submat.move_to([2.8, -0.6, 0])
        menor_calc.move_to([0, -1.8, 0])

        # Bloque 2
        cof_nombre.move_to([0, 2.6, 0])
        cof_formula.move_to([0, 1.5, 0])
        cof_nota.move_to([0, 0.6, 0])
        tabla_label.move_to([0, -0.3, 0])
        tabla_signos.move_to([0, -1.4, 0])

        # Bloque 3
        exp_nombre.move_to([0, 2.6, 0])
        exp_formula.move_to([0, 1.5, 0])
        exp_nota.move_to([0, 0.4, 0])
        exp_hint.move_to([0, -0.6, 0])

        # Bloque 4
        ej_nombre.move_to([0, 2.6, 0])
        mat_ej.move_to([-4.2, 0.6, 0])
        formula_desc.move_to([1.5, 1.5, 0])
        calc_C11.move_to([1.5, 0.7, 0])
        calc_C12.move_to([1.5, 0.0, 0])
        calc_C13.move_to([1.5, -0.7, 0])
        calc_total_1.move_to([0, -1.4, 0])
        calc_total_2.move_to([0, -1.4, 0])
        verificacion.move_to([0, -2.0, 0])

        # Bloque 5
        vent_nombre.move_to([0, 2.4, 0])
        vent_texto.move_to([0, 0.8, 0])
        vent_tip.move_to([0, -1.4, 0])

        # ---------- 3. ANIMACIONES ----------
        self.set_speech_service(EdgeTTSService(voice="es-MX-JorgeNeural"))

        # ==== Intro ====
        with self.voiceover(
            text="Ya vimos que para matrices de dos por dos hay una fórmula directa, "
                 "y para tres por tres está la regla de Sarrus. Pero, ¿qué pasa con "
                 "matrices más grandes, de cuatro por cuatro en adelante? Para eso "
                 "existe un método general: la expansión por cofactores."
        ) as t:
            self.play(Write(titulo), run_time=min(t.duration, 2.5))
            self.esperar(t.duration - 2.5)

        with self.voiceover(text="Empecemos por el concepto de menor.") as t:
            self.play(Transform(titulo, titulo_final), run_time=min(t.duration, 1.5))
            self.play(FadeIn(menor_nombre), run_time=min(t.duration * 0.25, 0.8))
            self.esperar(t.duration - 2.3)

        # ==== Bloque 1: menor ====
        with self.voiceover(
            text="Dada una matriz cuadrada A, el menor complementario, que escribimos "
                 "M sub i j, es el determinante de la submatriz que queda al eliminar "
                 "la fila i y la columna j."
        ) as t:
            self.play(FadeIn(menor_def, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="Veámoslo con un ejemplo. Aquí tenemos nuestra matriz A, de tres por "
                 "tres. Vamos a calcular el menor M uno uno: eliminamos la fila uno y "
                 "la columna uno."
        ) as t:
            self.play(FadeIn(mat_label), FadeIn(mat_A), run_time=min(t.duration * 0.2, 1.2))
            self.play(Create(tacha_fila1), run_time=min(t.duration * 0.15, 0.8))
            self.play(Create(tacha_col1), run_time=min(t.duration * 0.15, 0.8))
            self.esperar(t.duration - 2.8)

        with self.voiceover(
            text="Lo que queda es esta submatriz de dos por dos: cinco, seis, ocho, "
                 "diez. Y el menor es el determinante de esa submatriz: cinco por "
                 "diez, cincuenta, menos seis por ocho, cuarenta y ocho, igual a dos."
        ) as t:
            self.play(FadeIn(submat_label), FadeIn(submat),
                      run_time=min(t.duration * 0.2, 1.2))
            self.play(FadeIn(menor_calc, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 2.7)

        with self.voiceover(text="Bien, eso es el menor. Ahora el cofactor.") as t:
            self.play(FadeOut(VGroup(menor_nombre, menor_def, mat_label, mat_A,
                                     tacha_fila1, tacha_col1,
                                     submat_label, submat, menor_calc)),
                      run_time=min(t.duration, 1.5))
            self.esperar(t.duration - 1.5)

        # ==== Bloque 2: cofactor ====
        with self.voiceover(
            text="El cofactor es muy parecido al menor, pero con un signo que depende "
                 "de la posición. Se define como C sub i j igual a menos uno elevado a "
                 "i más j, por el menor M sub i j."
        ) as t:
            self.play(FadeIn(cof_nombre), run_time=min(t.duration * 0.15, 0.8))
            self.play(FadeIn(cof_formula, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 2.3)

        with self.voiceover(
            text="El factor menos uno elevado a i más j solo puede valer más uno o "
                 "menos uno, dependiendo de si i más j es par o impar. Esto genera un "
                 "patrón de signos que se alterna, como un tablero de ajedrez."
        ) as t:
            self.play(FadeIn(cof_nota, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="Esta es la tabla de signos para el caso tres por tres. Arriba a la "
                 "izquierda empieza con más, luego menos, más. La siguiente fila al "
                 "revés: menos, más, menos. Y la última: más, menos, más."
        ) as t:
            self.play(FadeIn(tabla_label), run_time=min(t.duration * 0.1, 0.6))
            self.play(FadeIn(signos_fila1), run_time=min(t.duration * 0.15, 1.0))
            self.play(FadeIn(signos_fila2), run_time=min(t.duration * 0.15, 1.0))
            self.play(FadeIn(signos_fila3), run_time=min(t.duration * 0.15, 1.0))
            self.esperar(t.duration - 3.6)

        with self.voiceover(
            text="Así que el cofactor es simplemente el menor con el signo que le "
                 "corresponde según su posición."
        ) as t:
            self.esperar(t.duration)

        with self.voiceover(text="Ahora, la fórmula de expansión.") as t:
            self.play(FadeOut(VGroup(cof_nombre, cof_formula, cof_nota,
                                     tabla_label, tabla_signos)),
                      run_time=min(t.duration, 1.5))
            self.esperar(t.duration - 1.5)

        # ==== Bloque 3: expansión ====
        with self.voiceover(
            text="La idea es esta: elegimos una fila cualquiera de la matriz, y el "
                 "determinante se calcula como la suma de cada entrada de esa fila, "
                 "multiplicada por su cofactor correspondiente."
        ) as t:
            self.play(FadeIn(exp_nombre), run_time=min(t.duration * 0.15, 0.8))
            self.play(FadeIn(exp_formula, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 2.3)

        with self.voiceover(
            text="Formalmente, si elegimos la fila i, el determinante es la suma "
                 "desde j igual a uno hasta n, de a sub i j por C sub i j."
        ) as t:
            self.play(FadeIn(exp_nota, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="Y algo muy útil: también podemos expandir por una columna en lugar "
                 "de una fila. El resultado va a ser el mismo. Esto nos da flexibilidad "
                 "para elegir la fila o columna que nos convenga más."
        ) as t:
            self.play(FadeIn(exp_hint, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(text="Veamos un ejemplo completo.") as t:
            self.play(FadeOut(VGroup(exp_nombre, exp_formula, exp_nota, exp_hint)),
                      run_time=min(t.duration, 1.5))
            self.esperar(t.duration - 1.5)

        # ==== Bloque 4: ejemplo ====
        with self.voiceover(
            text="Vamos a usar la misma matriz del ejemplo anterior. Y vamos a "
                 "expandir por la primera fila."
        ) as t:
            self.play(FadeIn(ej_nombre), run_time=min(t.duration * 0.1, 0.6))
            self.play(FadeIn(mat_ej), run_time=min(t.duration * 0.2, 1.2))
            self.play(FadeIn(formula_desc, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.2, 1.2))
            self.esperar(t.duration - 3.0)

        with self.voiceover(
            text="La fórmula queda: a uno uno por C uno uno, más a uno dos por C uno "
                 "dos, más a uno tres por C uno tres."
        ) as t:
            self.esperar(t.duration)

        # Resaltar fila 1
        with self.voiceover(text="Fíjense que solo usamos la primera fila.") as t:
            r_fila = SurroundingRectangle(
                VGroup(mat_ej.get_entries()[0],
                       mat_ej.get_entries()[1],
                       mat_ej.get_entries()[2]),
                color=RED, buff=0.12,
            )
            self.play(Create(r_fila), run_time=min(t.duration * 0.3, 1.2))
            self.esperar(t.duration - 1.2)

        with self.voiceover(text="Para el primer cofactor, C uno uno.") as t:
            self.play(FadeOut(r_fila), run_time=0.5)
            r_11 = SurroundingRectangle(mat_ej.get_entries()[0], color=RED, buff=0.1)
            self.play(Create(r_11), run_time=min(t.duration * 0.15, 0.8))
            self.esperar(t.duration - 1.3)

        with self.voiceover(
            text="La posición uno uno tiene signo más, y el menor M uno uno ya lo "
                 "calculamos: es dos. Entonces C uno uno es más dos."
        ) as t:
            self.play(FadeIn(calc_C11), run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(text="Para C uno dos.") as t:
            self.play(FadeOut(r_11), run_time=0.4)
            r_12 = SurroundingRectangle(mat_ej.get_entries()[1], color=RED, buff=0.1)
            self.play(Create(r_12), run_time=min(t.duration * 0.15, 0.8))
            self.esperar(t.duration - 1.2)

        with self.voiceover(
            text="La posición uno dos tiene signo menos. El menor M uno dos es: la "
                 "submatriz que queda al eliminar fila uno y columna dos es cuatro, "
                 "seis, siete, diez. Su determinante es cuatro por diez, cuarenta, "
                 "menos seis por siete, cuarenta y dos, igual a menos dos. Entonces C "
                 "uno dos es menos, por menos dos, que es más dos."
        ) as t:
            self.play(FadeIn(calc_C12), run_time=min(t.duration * 0.4, 2.0))
            self.esperar(t.duration - 2.0)

        with self.voiceover(text="Para C uno tres.") as t:
            self.play(FadeOut(r_12), run_time=0.4)
            r_13 = SurroundingRectangle(mat_ej.get_entries()[2], color=RED, buff=0.1)
            self.play(Create(r_13), run_time=min(t.duration * 0.15, 0.8))
            self.esperar(t.duration - 1.2)

        with self.voiceover(
            text="La posición uno tres tiene signo más. El menor M uno tres es: cuatro, "
                 "cinco, siete, ocho. Determinante: cuatro por ocho, treinta y dos, "
                 "menos cinco por siete, treinta y cinco, igual a menos tres. Entonces "
                 "C uno tres es más, por menos tres, que es menos tres."
        ) as t:
            self.play(FadeIn(calc_C13), run_time=min(t.duration * 0.4, 2.0))
            self.esperar(t.duration - 2.0)

        with self.voiceover(
            text="Ahora armamos la suma: uno por más dos, más dos por más dos, más "
                 "tres por menos tres. Esto es dos más cuatro menos nueve."
        ) as t:
            self.play(FadeOut(r_13), run_time=0.4)
            self.play(FadeIn(calc_total_1, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.8))
            self.esperar(t.duration - 2.2)

        with self.voiceover(
            text="Y el resultado es menos tres. ¡Exactamente lo mismo que nos dio con "
                 "la regla de Sarrus!"
        ) as t:
            self.play(ReplacementTransform(calc_total_1, calc_total_2),
                      run_time=min(t.duration * 0.4, 1.8))
            self.play(FadeIn(verificacion, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.2))
            self.esperar(t.duration - 3.0)

        with self.voiceover(text="Bien.") as t:
            self.play(
                FadeOut(VGroup(ej_nombre, mat_ej, formula_desc,
                               calc_C11, calc_C12, calc_C13,
                               calc_total_2, verificacion)),
                run_time=min(t.duration, 1.5),
            )
            self.esperar(t.duration - 1.5)

        # ==== Bloque 5: ventaja ====
        with self.voiceover(
            text="¿Por qué usar cofactores si Sarrus es más rápida para tres por "
                 "tres? Porque los cofactores funcionan para cualquier orden. Para "
                 "cuatro por cuatro, cinco por cinco, o cualquier tamaño. Sarrus, en "
                 "cambio, está limitada al tres por tres."
        ) as t:
            self.play(FadeIn(vent_nombre), run_time=min(t.duration * 0.15, 0.8))
            self.play(FadeIn(vent_texto, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 2.3)

        with self.voiceover(
            text="Además, combinada con otras propiedades que vamos a ver en la "
                 "siguiente escena, la expansión por cofactores es la base del método "
                 "general para calcular determinantes en cualquier dimensión."
        ) as t:
            self.esperar(t.duration)

        with self.voiceover(
            text="Un truco muy útil: si tienes que expandir, elige la fila o columna "
                 "que tenga más ceros. Porque los ceros aportan cero a la suma, y te "
                 "ahorras calcular ese cofactor. Esto puede reducir muchísimo el trabajo."
        ) as t:
            self.play(FadeIn(vent_tip, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="Y esa es la clave del método: no es que sea siempre la vía más "
                 "rápida, es que es la vía general. Combinado con propiedades, se "
                 "vuelve muy eficiente."
        ) as t:
            self.esperar(t.duration)

        # ---------- 4. CIERRE ----------
        self.play(FadeOut(VGroup(titulo, vent_nombre, vent_texto, vent_tip)),
                  run_time=2)

# ---------- Escena 11: Propiedades de los determinantes ----------
class D11_PropiedadesDeterminantes(CuadernoScene):
    def construct(self):
        # ============================================================
        # 1. OBJETOS
        # ============================================================
        titulo = Text("Propiedades de los determinantes", font_size=42, color="#1A3A5C", weight=BOLD)

        # ===== Propiedad 1 =====
        p1_nombre = Text("1. Determinante del producto", font_size=28, color="#1A3A5C", weight=BOLD)
        p1_formula = MathTex(r"\det(AB) = \det(A) \cdot \det(B)", font_size=44, color="#1A3A5C")

        A1 = Matrix([[1, 2], [3, 4]], h_buff=0.6, v_buff=0.4)
        B1 = Matrix([[5, 6], [7, 8]], h_buff=0.6, v_buff=0.4)
        AB1 = Matrix([[19, 22], [43, 50]], h_buff=0.6, v_buff=0.4)
        for m in [A1, B1, AB1]:
            m.set_color("#2A4A6A")

        A1_label = MathTex("A", font_size=32, color="#1A3A5C")
        B1_label = MathTex("B", font_size=32, color="#1A3A5C")
        AB1_label = MathTex("AB", font_size=32, color="#E88B8B")
        op_dot = MathTex(r"\cdot", font_size=36, color="#1A3A5C")
        op_eq = MathTex("=", font_size=36, color="#1A3A5C")

        det_A1 = MathTex(r"\det(A) = -2", font_size=26, color=RED)
        det_B1 = MathTex(r"\det(B) = -2", font_size=26, color=RED)
        det_AB1 = MathTex(r"\det(AB) = 4", font_size=26, color=TEAL)
        p1_verif = MathTex(r"(-2)(-2) = 4 \;\checkmark", font_size=30, color=TEAL)

        # ===== Propiedad 2 =====
        p2_nombre = Text("2. Determinante de la transpuesta", font_size=28, color="#1A3A5C", weight=BOLD)
        p2_formula = MathTex(r"\det(A^T) = \det(A)", font_size=44, color="#1A3A5C")

        A2 = Matrix([[1, 2], [3, 4]], h_buff=0.6, v_buff=0.4)
        At2 = Matrix([[1, 3], [2, 4]], h_buff=0.6, v_buff=0.4)
        A2.set_color("#2A4A6A"); At2.set_color("#2A4A6A")

        A2_label = MathTex("A", font_size=32, color="#1A3A5C")
        At2_label = MathTex(r"A^T", font_size=32, color="#E88B8B")
        arrow2 = MathTex(r"\longrightarrow", font_size=60, color="#E88B8B")

        det_A2 = MathTex(r"\det(A) = -2", font_size=26, color=RED)
        det_At2 = MathTex(r"\det(A^T) = -2", font_size=26, color=TEAL)
        p2_verif = MathTex(r"-2 = -2 \;\checkmark", font_size=30, color=TEAL)

        # ===== Propiedad 3 =====
        p3_nombre = Text("3. Fila múltiplo de otra", font_size=28, color="#1A3A5C", weight=BOLD)
        p3_formula = Tex(r"Si una fila es m\'ultiplo de otra, entonces $\det(A) = 0$",
                         tex_environment="center", font_size=26)
        p3_formula.set_color("#2A4A6A")

        A3 = Matrix([[1, 2], [2, 4]], h_buff=0.7, v_buff=0.5)
        A3.set_color("#2A4A6A")

        p3_expl = Tex(r"Fila 2 = 2 $\times$ Fila 1", tex_environment="center", font_size=24)
        p3_expl.set_color("#4A6A8A")
        p3_calc = MathTex(r"\det = (1)(4) - (2)(2) = 0", font_size=30, color=RED)
        p3_verif = Tex(r"Los vectores fila son \textbf{linealmente dependientes}",
                       tex_environment="center", font_size=24)
        p3_verif.set_color("#E88B8B")

        # ===== Propiedad 4 =====
        p4_nombre = Text("4. Intercambio de filas", font_size=28, color="#1A3A5C", weight=BOLD)
        p4_formula = Tex(r"Al intercambiar dos filas, $\det$ cambia de signo",
                         tex_environment="center", font_size=26)
        p4_formula.set_color("#2A4A6A")

        A4 = Matrix([[1, 2], [3, 4]], h_buff=0.7, v_buff=0.5)
        A4s = Matrix([[3, 4], [1, 2]], h_buff=0.7, v_buff=0.5)
        A4.set_color("#2A4A6A"); A4s.set_color("#2A4A6A")

        A4_label = MathTex("A", font_size=32, color="#1A3A5C")
        A4s_label = MathTex(r"A'", font_size=32, color="#E88B8B")
        arrow4 = MathTex(r"\longrightarrow", font_size=60, color="#E88B8B")

        det_A4 = MathTex(r"\det(A) = -2", font_size=26, color=RED)
        det_A4s = MathTex(r"\det(A') = 2", font_size=26, color=TEAL)
        p4_verif = MathTex(r"\det(A') = -\det(A) \;\checkmark", font_size=30, color=TEAL)

        # ===== Propiedad 5 =====
        p5_nombre = Text("5. Matriz triangular", font_size=28, color="#1A3A5C", weight=BOLD)
        p5_formula = Tex(r"Si $A$ es triangular, $\det(A)$ = producto de la diagonal",
                         tex_environment="center", font_size=26)
        p5_formula.set_color("#2A4A6A")

        T5 = Matrix([[2, 5, 1], [0, 3, 4], [0, 0, 5]], h_buff=0.7, v_buff=0.5)
        T5.set_color("#2A4A6A")

        p5_calc = MathTex(r"\det(T) = (2)(3)(5) = 30", font_size=32, color=TEAL)
        p5_nota = Tex(r"Tambi\'en vale para matrices diagonales",
                      tex_environment="center", font_size=24)
        p5_nota.set_color("#6A7A8A")

        # ============================================================
        # 2. CONFIGURACIÓN (colores y posición) — TODO SE MUEVE AQUÍ
        # ============================================================
        titulo.move_to([0, 0, 0])
        titulo_final = titulo.copy().scale(0.7).move_to([0, 3.6, 0])

        # P1
        p1_nombre.move_to([0, 2.6, 0])
        p1_formula.move_to([0, 1.9, 0])
        A1_label.move_to([-4.3, 1.4, 0]); A1.move_to([-4.3, 0.5, 0])
        op_dot.move_to([-2.2, 0.5, 0])
        B1_label.move_to([-0.9, 1.4, 0]); B1.move_to([-0.9, 0.5, 0])
        op_eq.move_to([1.1, 0.5, 0])
        AB1_label.move_to([2.6, 1.4, 0]); AB1.move_to([2.6, 0.5, 0])
        det_A1.move_to([-4.3, -0.5, 0])
        det_B1.move_to([-0.9, -0.5, 0])
        det_AB1.move_to([2.6, -0.5, 0])
        p1_verif.move_to([0, -1.5, 0])

        # P2
        p2_nombre.move_to([0, 2.6, 0])
        p2_formula.move_to([0, 1.8, 0])
        A2_label.move_to([-3.0, 1.2, 0]); A2.move_to([-3.0, 0.3, 0])
        arrow2.move_to([0, 0.3, 0])
        At2_label.move_to([3.0, 1.2, 0]); At2.move_to([3.0, 0.3, 0])
        det_A2.move_to([-3.0, -0.9, 0])
        det_At2.move_to([3.0, -0.9, 0])
        p2_verif.move_to([0, -1.7, 0])

        # P3
        p3_nombre.move_to([0, 2.6, 0])
        p3_formula.move_to([0, 1.7, 0])
        A3.move_to([0, 0.3, 0])   # ← A3 se mueve ANTES de crear rectángulos
        p3_expl.move_to([0, -0.8, 0])
        p3_calc.move_to([0, -1.5, 0])
        p3_verif.move_to([0, -2.1, 0])

        # P4
        p4_nombre.move_to([0, 2.6, 0])
        p4_formula.move_to([0, 1.7, 0])
        A4_label.move_to([-3.0, 1.2, 0]); A4.move_to([-3.0, 0.3, 0])
        arrow4.move_to([0, 0.3, 0])
        A4s_label.move_to([3.0, 1.2, 0]); A4s.move_to([3.0, 0.3, 0])
        det_A4.move_to([-3.0, -0.9, 0])
        det_A4s.move_to([3.0, -0.9, 0])
        p4_verif.move_to([0, -1.7, 0])

        # P5
        p5_nombre.move_to([0, 2.6, 0])
        p5_formula.move_to([0, 1.7, 0])
        T5.move_to([0, 0.3, 0])   # ← T5 se mueve ANTES de crear diag5
        p5_calc.move_to([0, -1.4, 0])
        p5_nota.move_to([0, -2.0, 0])

        # ============================================================
        # 2b. RECTÁNGULOS (SE CREAN DESPUÉS DE POSICIONAR LAS MATRICES)
        # ============================================================
        # P3: fila 1 en rojo, fila 2 en azul
        r_fila1 = SurroundingRectangle(
            VGroup(A3.get_entries()[0], A3.get_entries()[1]),
            color=RED, buff=0.1,
        )
        r_fila2 = SurroundingRectangle(
            VGroup(A3.get_entries()[2], A3.get_entries()[3]),
            color=BLUE, buff=0.1,
        )
        for r in [r_fila1, r_fila2]:
            r.set_stroke(width=2.5)

        # P5: diagonal principal resaltada
        diag5 = VGroup(*[
            SurroundingRectangle(T5.get_entries()[i], color="#E88B8B", buff=0.12)
            for i in [0, 4, 8]
        ])
        for b in diag5:
            b.set_stroke(width=2.5)

        # ============================================================
        # 3. ANIMACIONES
        # ============================================================
        self.set_speech_service(EdgeTTSService(voice="es-MX-JorgeNeural"))

        with self.voiceover(
            text="Ahora vamos a ver las propiedades más importantes de los "
                 "determinantes. Estas propiedades nos van a permitir calcular "
                 "determinantes de forma más rápida, y también entender mejor qué "
                 "significan."
        ) as t:
            self.play(Write(titulo), run_time=min(t.duration, 2.5))
            self.esperar(t.duration - 2.5)

        with self.voiceover(text="Empecemos con la primera.") as t:
            self.play(Transform(titulo, titulo_final), run_time=min(t.duration, 1.5))
            self.esperar(t.duration - 1.5)

        # ==== PROPIEDAD 1 ====
        with self.voiceover(
            text="Propiedad uno: el determinante de un producto es el producto de "
                 "los determinantes. Es decir, det de A por B es igual a det de A, "
                 "por det de B."
        ) as t:
            self.play(FadeIn(p1_nombre), run_time=min(t.duration * 0.15, 0.8))
            self.play(FadeIn(p1_formula, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 2.3)

        with self.voiceover(
            text="Veamos un ejemplo. Tomamos A, con determinante menos dos, y B, "
                 "también con determinante menos dos. Multiplicamos A por B y "
                 "obtenemos esta matriz, cuyo determinante es cuatro."
        ) as t:
            self.play(FadeIn(A1_label), FadeIn(A1), run_time=min(t.duration * 0.08, 0.6))
            self.play(FadeIn(op_dot), run_time=min(t.duration * 0.04, 0.4))
            self.play(FadeIn(B1_label), FadeIn(B1), run_time=min(t.duration * 0.08, 0.6))
            self.play(FadeIn(op_eq), run_time=min(t.duration * 0.04, 0.4))
            self.play(FadeIn(AB1_label), FadeIn(AB1), run_time=min(t.duration * 0.08, 0.6))
            self.play(FadeIn(det_A1), FadeIn(det_B1), FadeIn(det_AB1),
                      run_time=min(t.duration * 0.08, 0.6))
            self.esperar(t.duration - 3.8)

        with self.voiceover(
            text="Y efectivamente, menos dos por menos dos es cuatro. Se cumple."
        ) as t:
            self.play(FadeIn(p1_verif, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(text="Bien.") as t:
            self.play(FadeOut(VGroup(p1_nombre, p1_formula,
                                     A1_label, A1, op_dot, B1_label, B1,
                                     op_eq, AB1_label, AB1,
                                     det_A1, det_B1, det_AB1, p1_verif)),
                      run_time=min(t.duration, 1.5))
            self.esperar(t.duration - 1.5)

        # ==== PROPIEDAD 2 ====
        with self.voiceover(
            text="Propiedad dos: el determinante de la transpuesta es igual al "
                 "determinante de la matriz original. Det de A transpuesta es igual "
                 "a det de A."
        ) as t:
            self.play(FadeIn(p2_nombre), run_time=min(t.duration * 0.15, 0.8))
            self.play(FadeIn(p2_formula, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 2.3)

        with self.voiceover(
            text="Por ejemplo, si A es uno, dos, tres, cuatro, su transpuesta es uno, "
                 "tres, dos, cuatro. Calculamos ambos determinantes: A da uno por "
                 "cuatro, menos dos por tres, igual a menos dos. Y A transpuesta da "
                 "uno por cuatro, menos tres por dos, también menos dos. Son iguales."
        ) as t:
            self.play(FadeIn(A2_label), FadeIn(A2), run_time=min(t.duration * 0.08, 0.6))
            self.play(FadeIn(arrow2), run_time=min(t.duration * 0.04, 0.5))
            self.play(FadeIn(At2_label), FadeIn(At2), run_time=min(t.duration * 0.08, 0.6))
            self.play(FadeIn(det_A2), FadeIn(det_At2),
                      run_time=min(t.duration * 0.08, 0.7))
            self.esperar(t.duration - 2.4)

        with self.voiceover(
            text="Esto es muy útil: si una matriz es más fácil de transponer que de "
                 "calcular directamente, podemos aprovechar esta propiedad."
        ) as t:
            self.play(FadeIn(p2_verif, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(text="Siguiente.") as t:
            self.play(FadeOut(VGroup(p2_nombre, p2_formula,
                                     A2_label, A2, arrow2, At2_label, At2,
                                     det_A2, det_At2, p2_verif)),
                      run_time=min(t.duration, 1.5))
            self.esperar(t.duration - 1.5)

        # ==== PROPIEDAD 3 ====
        with self.voiceover(
            text="Propiedad tres: si una fila es múltiplo de otra, entonces el "
                 "determinante es cero."
        ) as t:
            self.play(FadeIn(p3_nombre), run_time=min(t.duration * 0.2, 0.8))
            self.play(FadeIn(p3_formula, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 2.3)

        with self.voiceover(
            text="Aquí tenemos una matriz donde la segunda fila es exactamente el "
                 "doble de la primera: dos, cuatro, contra uno, dos."
        ) as t:
            self.play(FadeIn(A3), run_time=min(t.duration * 0.2, 1.0))
            self.play(Create(r_fila1), Create(r_fila2),
                      run_time=min(t.duration * 0.3, 1.5))
            self.play(FadeIn(p3_expl, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.2, 1.0))
            self.esperar(t.duration - 3.5)

        with self.voiceover(
            text="Si calculamos el determinante: uno por cuatro, cuatro, menos dos "
                 "por dos, cuatro. Cuatro menos cuatro, cero."
        ) as t:
            self.play(FadeIn(p3_calc, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="Esto tiene todo el sentido geométrico: los dos vectores fila son "
                 "paralelos, forman un paralelogramo degenerado de área cero."
        ) as t:
            self.play(FadeIn(p3_verif, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(text="Bien.") as t:
            self.play(FadeOut(VGroup(p3_nombre, p3_formula, A3,
                                     r_fila1, r_fila2, p3_expl, p3_calc, p3_verif)),
                      run_time=min(t.duration, 1.5))
            self.esperar(t.duration - 1.5)

        # ==== PROPIEDAD 4 ====
        with self.voiceover(
            text="Propiedad cuatro: si intercambiamos dos filas, el determinante "
                 "cambia de signo. Lo que antes era positivo, ahora es negativo. Y "
                 "viceversa."
        ) as t:
            self.play(FadeIn(p4_nombre), run_time=min(t.duration * 0.15, 0.8))
            self.play(FadeIn(p4_formula, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 2.3)

        with self.voiceover(
            text="Tenemos A, con determinante menos dos. Si intercambiamos sus dos "
                 "filas, obtenemos A prima, y su determinante es ahora más dos. "
                 "Exactamente el negativo del anterior."
        ) as t:
            self.play(FadeIn(A4_label), FadeIn(A4), run_time=min(t.duration * 0.08, 0.6))
            self.play(FadeIn(arrow4), run_time=min(t.duration * 0.04, 0.5))
            self.play(FadeIn(A4s_label), FadeIn(A4s),
                      run_time=min(t.duration * 0.08, 0.6))
            self.play(FadeIn(det_A4), FadeIn(det_A4s),
                      run_time=min(t.duration * 0.08, 0.7))
            self.esperar(t.duration - 2.4)

        with self.voiceover(
            text="Esto es muy útil cuando hacemos eliminación gaussiana: cada vez "
                 "que intercambiamos filas, sabemos que el determinante cambia de "
                 "signo."
        ) as t:
            self.play(FadeIn(p4_verif, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(text="Última propiedad.") as t:
            self.play(FadeOut(VGroup(p4_nombre, p4_formula,
                                     A4_label, A4, arrow4, A4s_label, A4s,
                                     det_A4, det_A4s, p4_verif)),
                      run_time=min(t.duration, 1.5))
            self.esperar(t.duration - 1.5)

        # ==== PROPIEDAD 5 ====
        with self.voiceover(
            text="Propiedad cinco, y esta es de las más prácticas: si la matriz es "
                 "triangular, ya sea superior o inferior, su determinante es "
                 "simplemente el producto de los elementos de la diagonal principal."
        ) as t:
            self.play(FadeIn(p5_nombre), run_time=min(t.duration * 0.15, 0.8))
            self.play(FadeIn(p5_formula, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 2.3)

        with self.voiceover(
            text="Aquí tenemos una matriz triangular superior: todos los elementos "
                 "debajo de la diagonal son cero. Entonces el determinante es "
                 "simplemente dos por tres por cinco, igual a treinta."
        ) as t:
            self.play(FadeIn(T5), run_time=min(t.duration * 0.2, 1.2))
            self.play(
                LaggedStart(*[Create(b) for b in diag5], lag_ratio=0.3),
                run_time=min(t.duration * 0.3, 1.8),
            )
            self.esperar(t.duration - 3.0)

        with self.voiceover(
            text="No hace falta hacer ninguna expansión por cofactores, ningún "
                 "cálculo complicado. Solo multiplicar la diagonal. Y esto es "
                 "importantísimo, porque cuando hagamos eliminación gaussiana, vamos "
                 "a transformar la matriz en triangular, y luego podremos leer el "
                 "determinante directamente."
        ) as t:
            self.play(FadeIn(p5_calc, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.2, 1.2))
            self.esperar(t.duration - 1.2)

        with self.voiceover(
            text="Y ojo, esto también aplica para matrices diagonales, porque una "
                 "matriz diagonal es un caso particular de triangular: tiene ceros "
                 "en todo lo que no es la diagonal."
        ) as t:
            self.play(FadeIn(p5_nota, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="Estas cinco propiedades son las más usadas en la práctica. Con "
                 "ellas, combinadas con la expansión por cofactores, podemos "
                 "calcular determinantes de cualquier tamaño de forma eficiente. "
                 "Y además, nos dan intuición sobre qué significan geométricamente "
                 "los determinantes."
        ) as t:
            self.esperar(t.duration)

        # ============================================================
        # 4. CIERRE
        # ============================================================
        self.play(FadeOut(VGroup(titulo, p5_nombre, p5_formula, T5, diag5,
                                 p5_calc, p5_nota)),
                  run_time=2)

# ---------- Escena 12: Regla de Cramer ----------
class D12_ReglaCramer(CuadernoScene):
    def construct(self):
        # ============================================================
        # 1. OBJETOS
        # ============================================================
        titulo = Text("Regla de Cramer", font_size=42, color="#1A3A5C", weight=BOLD)

        # ===== Bloque 1: idea general =====
        idea_nombre = Text("Idea general", font_size=30, color="#1A3A5C", weight=BOLD)
        sistema_gen = MathTex(r"A\vec{x} = \vec{b}", font_size=52, color="#1A3A5C")
        condicion = Tex(
            r"Sistema de $n$ ecuaciones con $n$ inc\'ognitas,\\"
            r"con $\det(A) \neq 0$ (soluci\'on \'unica)",
            tex_environment="center", font_size=24,
        )
        condicion.set_color("#2A4A6A")

        formula_cramer = MathTex(r"x_i = \frac{\det(A_i)}{\det(A)}", font_size=54, color="#1A3A5C")
        formula_nota = Tex(
            r"$A_i$ = matriz $A$ con la columna $i$ reemplazada por $\vec{b}$",
            tex_environment="center", font_size=24,
        )
        formula_nota.set_color("#4A6A8A")
        formula_hint = Tex(
            r"Una f\'ormula directa para cada inc\'ognita",
            tex_environment="center", font_size=22,
        )
        formula_hint.set_color("#6A7A8A")

        # ===== Bloque 2: ejemplo 2x2 =====
        ej_nombre = Text("Ejemplo 2×2", font_size=30, color="#1A3A5C", weight=BOLD)
        ec1 = MathTex(r"2x + y = 5", font_size=34, color="#2A4A6A")
        ec2 = MathTex(r"x + 3y = 10", font_size=34, color="#2A4A6A")
        sistema_2x2 = VGroup(ec1, ec2).arrange(DOWN, aligned_edge=LEFT, buff=0.25)

        forma_mat = MathTex(
            r"\begin{bmatrix} 2 & 1 \\ 1 & 3 \end{bmatrix}"
            r"\begin{bmatrix} x \\ y \end{bmatrix}"
            r" = "
            r"\begin{bmatrix} 5 \\ 10 \end{bmatrix}",
            font_size=42, color="#2A4A6A",
        )

        det_sist_label = MathTex(r"\det(A) =", font_size=34, color="#1A3A5C")
        det_sist = MathTex(r"(2)(3) - (1)(1) = 6 - 1 = 5", font_size=30, color=TEAL)

        reemplazo_x_label = Tex(
            r"Para $x$: reemplazamos la columna de $x$ por $\vec{b}$",
            tex_environment="center", font_size=26,
        )
        reemplazo_x_label.set_color("#4A6A8A")

        A_x = Matrix([[5, 1], [10, 3]], h_buff=0.8, v_buff=0.5)
        A_x.set_color("#2A4A6A")
        det_Ax = MathTex(r"\det(A_x) = (5)(3) - (1)(10) = 15 - 10 = 5",
                         font_size=28, color=TEAL)
        x_calc = MathTex(r"x = \frac{\det(A_x)}{\det(A)} = \frac{5}{5} = 1",
                         font_size=36, color=TEAL)

        reemplazo_y_label = Tex(
            r"Para $y$: reemplazamos la columna de $y$ por $\vec{b}$",
            tex_environment="center", font_size=26,
        )
        reemplazo_y_label.set_color("#4A6A8A")

        A_y = Matrix([[2, 5], [1, 10]], h_buff=0.8, v_buff=0.5)
        A_y.set_color("#2A4A6A")
        det_Ay = MathTex(r"\det(A_y) = (2)(10) - (5)(1) = 20 - 5 = 15",
                         font_size=28, color=TEAL)
        y_calc = MathTex(r"y = \frac{\det(A_y)}{\det(A)} = \frac{15}{5} = 3",
                         font_size=36, color=TEAL)

        solucion = MathTex(r"x = 1, \quad y = 3", font_size=42, color=TEAL)
        verificacion = Tex(
            r"Verificaci\'on: \quad $2(1) + 3 = 5 \;\checkmark$ \qquad $1 + 3(3) = 10 \;\checkmark$",
            tex_environment="center", font_size=24,
        )
        verificacion.set_color(TEAL)

        # ===== Bloque 3: ejemplo 3x3 breve =====
        ej3_nombre = Text("Ejemplo 3×3 (breve)", font_size=30, color="#1A3A5C", weight=BOLD)
        sistema_3x3 = MathTex(
            r"\begin{cases} x + y + z = 6 \\ x - y + z = 2 \\ 2x + y - z = 1 \end{cases}",
            font_size=32, color="#2A4A6A",
        )
        det3_A = MathTex(r"\det(A) = 6 \;\neq 0", font_size=32, color=TEAL)
        dets3 = MathTex(
            r"\det(A_x) = 6, \quad \det(A_y) = 12, \quad \det(A_z) = 18",
            font_size=28, color="#2A4A6A",
        )
        solucion3 = MathTex(
            r"x = \frac{6}{6} = 1, \quad y = \frac{12}{6} = 2, \quad z = \frac{18}{6} = 3",
            font_size=30, color=TEAL,
        )
        nota3 = Tex(
            r"Mismo procedimiento, un poco m\'as de c\'alculo",
            tex_environment="center", font_size=22,
        )
        nota3.set_color("#6A7A8A")

        advertencia = Tex(
            r"Cramer es pr\'actico para sistemas peque\~nos (2$\times$2, 3$\times$3).\\"
            r"Para sistemas grandes, \textbf{Gauss} es mejor.",
            tex_environment="center", font_size=26,
        )
        advertencia.set_color("#E88B8B")

        # ============================================================
        # 2. CONFIGURACIÓN
        # ============================================================
        titulo.move_to([0, 0, 0])
        titulo_final = titulo.copy().scale(0.7).move_to([0, 3.6, 0])

        # B1
        idea_nombre.move_to([0, 2.6, 0])
        sistema_gen.move_to([0, 1.7, 0])
        condicion.move_to([0, 0.8, 0])
        formula_cramer.move_to([0, -0.3, 0])
        formula_nota.move_to([0, -1.3, 0])
        formula_hint.move_to([0, -2.0, 0])

        # B2
        ej_nombre.move_to([0, 2.6, 0])
        sistema_2x2.move_to([-3.5, 1.4, 0])
        forma_mat.move_to([2.5, 1.4, 0])
        det_sist_label.move_to([-3.5, 0.3, 0])
        det_sist.move_to([-3.5, -0.4, 0])

        reemplazo_x_label.move_to([0, 2.6, 0])
        A_x.move_to([0, 1.3, 0])
        det_Ax.move_to([0, 0.0, 0])
        x_calc.move_to([0, -1.0, 0])

        reemplazo_y_label.move_to([0, 2.6, 0])
        A_y.move_to([0, 1.3, 0])
        det_Ay.move_to([0, 0.0, 0])
        y_calc.move_to([0, -1.0, 0])

        solucion.move_to([0, 0.8, 0])
        verificacion.move_to([0, -0.2, 0])

        # B3
        ej3_nombre.move_to([0, 2.6, 0])
        sistema_3x3.move_to([0, 1.4, 0])
        det3_A.move_to([0, 0.2, 0])
        dets3.move_to([0, -0.6, 0])
        solucion3.move_to([0, -1.4, 0])
        nota3.move_to([0, -2.0, 0])

        advertencia.move_to([0, 0.2, 0])

        # Colorear columnas reemplazadas (después de mover las matrices)
        A_x.get_entries()[0].set_color(RED)   # 5
        A_x.get_entries()[2].set_color(RED)   # 10
        A_y.get_entries()[1].set_color(RED)   # 5
        A_y.get_entries()[3].set_color(RED)   # 10

        # ============================================================
        # 3. ANIMACIONES
        # ============================================================
        self.set_speech_service(EdgeTTSService(voice="es-MX-JorgeNeural"))

        # ==== Intro ====
        with self.voiceover(
            text="Ahora vamos a ver la regla de Cramer. Es un método elegante para "
                 "resolver sistemas de ecuaciones lineales, aunque con limitaciones "
                 "que vamos a comentar al final."
        ) as t:
            self.play(Write(titulo), run_time=min(t.duration, 2.5))
            self.esperar(t.duration - 2.5)

        with self.voiceover(text="Empecemos con la idea general.") as t:
            self.play(Transform(titulo, titulo_final), run_time=min(t.duration, 1.5))
            self.play(FadeIn(idea_nombre), run_time=min(t.duration * 0.2, 0.8))
            self.esperar(t.duration - 2.3)

        # ==== Bloque 1 ====
        with self.voiceover(
            text="Partimos de un sistema de n ecuaciones con n incógnitas, escrito "
                 "en forma matricial como A por x igual a b. Donde A es la matriz de "
                 "coeficientes, x es el vector de incógnitas, y b es el vector de "
                 "términos independientes."
        ) as t:
            self.play(FadeIn(sistema_gen, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="La regla de Cramer solo aplica cuando el determinante de A es "
                 "distinto de cero. En ese caso, el sistema tiene solución única."
        ) as t:
            self.play(FadeIn(condicion, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="Y la fórmula es esta: la incógnita x sub i es igual al determinante "
                 "de A sub i, dividido entre el determinante de A."
        ) as t:
            self.play(FadeIn(formula_cramer, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.8))
            self.esperar(t.duration - 1.8)

        with self.voiceover(
            text="Pero, ¿qué es A sub i? Es la matriz A, pero con la columna i "
                 "reemplazada por el vector b. Es decir, para cada incógnita, "
                 "sustituimos la columna correspondiente por los términos "
                 "independientes, calculamos su determinante, y dividimos entre el "
                 "determinante original."
        ) as t:
            self.play(FadeIn(formula_nota, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.play(FadeIn(formula_hint, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.2))
            self.esperar(t.duration - 2.7)

        with self.voiceover(text="Veamos un ejemplo concreto.") as t:
            self.play(FadeOut(VGroup(idea_nombre, sistema_gen, condicion,
                                     formula_cramer, formula_nota, formula_hint)),
                      run_time=min(t.duration, 1.5))
            self.esperar(t.duration - 1.5)

        # ==== Bloque 2: ejemplo 2x2 ====
        with self.voiceover(
            text="Aquí tenemos un sistema de dos ecuaciones con dos incógnitas: dos "
                 "x más y igual a cinco, y x más tres y igual a diez."
        ) as t:
            self.play(FadeIn(ej_nombre), run_time=min(t.duration * 0.15, 0.8))
            self.play(FadeIn(ec1), run_time=min(t.duration * 0.1, 0.6))
            self.play(FadeIn(ec2), run_time=min(t.duration * 0.1, 0.6))
            self.esperar(t.duration - 2.0)

        with self.voiceover(
            text="En forma matricial, esto queda: la matriz A con entradas dos, uno, "
                 "uno, tres. El vector x con x e y. Y el vector b con cinco y diez."
        ) as t:
            self.play(FadeIn(forma_mat, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="Primero calculamos el determinante de A: dos por tres, seis, menos "
                 "uno por uno, uno. Da cinco. Como es distinto de cero, podemos usar "
                 "Cramer."
        ) as t:
            self.play(FadeIn(det_sist_label), run_time=min(t.duration * 0.1, 0.6))
            self.play(FadeIn(det_sist), run_time=min(t.duration * 0.15, 1.0))
            self.esperar(t.duration - 1.6)

        with self.voiceover(text="Ahora, para obtener x.") as t:
            self.play(FadeOut(VGroup(ej_nombre, ec1, ec2, sistema_2x2,
                                     forma_mat, det_sist_label, det_sist)),
                      run_time=min(t.duration, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="Reemplazamos la columna de x, es decir la primera columna, por el "
                 "vector b. Nos queda la matriz cinco, uno, diez, tres. Fíjense que "
                 "la columna reemplazada está en rojo."
        ) as t:
            self.play(FadeIn(reemplazo_x_label), run_time=min(t.duration * 0.2, 0.8))
            self.play(FadeIn(A_x), run_time=min(t.duration * 0.2, 1.2))
            self.esperar(t.duration - 2.0)

        with self.voiceover(
            text="Su determinante es: cinco por tres, quince, menos uno por diez, "
                 "diez. Quince menos diez, cinco."
        ) as t:
            self.play(FadeIn(det_Ax), run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="Y entonces x es igual a det de A sub x, entre det de A. Es decir, "
                 "cinco entre cinco, igual a uno."
        ) as t:
            self.play(FadeIn(x_calc, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(text="Ahora para y.") as t:
            self.play(FadeOut(VGroup(reemplazo_x_label, A_x, det_Ax, x_calc)),
                      run_time=min(t.duration, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="Reemplazamos la columna de y, es decir la segunda columna, por el "
                 "vector b. Nos queda dos, cinco, uno, diez. De nuevo, la columna "
                 "reemplazada está en rojo."
        ) as t:
            self.play(FadeIn(reemplazo_y_label), run_time=min(t.duration * 0.2, 0.8))
            self.play(FadeIn(A_y), run_time=min(t.duration * 0.2, 1.2))
            self.esperar(t.duration - 2.0)

        with self.voiceover(
            text="Su determinante: dos por diez, veinte, menos cinco por uno, cinco. "
                 "Veinte menos cinco, quince."
        ) as t:
            self.play(FadeIn(det_Ay), run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="Entonces y es quince entre cinco, igual a tres."
        ) as t:
            self.play(FadeIn(y_calc, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="Y verificamos: dos por uno más tres es cinco, y uno más tres por "
                 "tres es diez. Se cumple el sistema."
        ) as t:
            self.play(FadeOut(VGroup(reemplazo_y_label, A_y, det_Ay, y_calc)),
                      run_time=min(t.duration * 0.2, 1.0))
            self.play(FadeIn(solucion, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.2, 1.2))
            self.play(FadeIn(verificacion, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.2, 1.2))
            self.esperar(t.duration - 3.4)

        with self.voiceover(text="Perfecto.") as t:
            self.play(FadeOut(VGroup(solucion, verificacion)),
                      run_time=min(t.duration, 1.2))
            self.esperar(t.duration - 1.2)

        # ==== Bloque 3: ejemplo 3x3 ====
        with self.voiceover(
            text="Veamos ahora un ejemplo de tres por tres, pero más breve para no "
                 "repetir todo el cálculo con detalle."
        ) as t:
            self.play(FadeIn(ej3_nombre), run_time=min(t.duration * 0.2, 0.8))
            self.esperar(t.duration - 0.8)

        with self.voiceover(
            text="Tenemos este sistema de tres ecuaciones con tres incógnitas."
        ) as t:
            self.play(FadeIn(sistema_3x3), run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="Calculando el determinante de la matriz A, obtenemos seis. Distinto "
                 "de cero, entonces aplica Cramer."
        ) as t:
            self.play(FadeIn(det3_A, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.2))
            self.esperar(t.duration - 1.2)

        with self.voiceover(
            text="Reemplazando cada columna por el vector b, obtenemos los "
                 "determinantes: seis, doce, y dieciocho, para x, y, z "
                 "respectivamente."
        ) as t:
            self.play(FadeIn(dets3, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="Y entonces las soluciones son: x igual a uno, y igual a dos, z "
                 "igual a tres. Si sustituyen, verán que cumplen las tres ecuaciones."
        ) as t:
            self.play(FadeIn(solucion3, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.8))
            self.esperar(t.duration - 1.8)

        with self.voiceover(
            text="El procedimiento es exactamente el mismo que en dos por dos, solo "
                 "que con más determinantes que calcular."
        ) as t:
            self.play(FadeIn(nota3, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.2))
            self.esperar(t.duration - 1.2)

        with self.voiceover(
            text="Pero ojo, aquí hay algo importante. Cramer es muy práctico para "
                 "sistemas pequeños, de dos por dos o de tres por tres. Pero para "
                 "sistemas más grandes, se vuelve muy caro, porque hay que calcular "
                 "n más uno determinantes. Para esos casos, el método de Gauss es "
                 "mucho más eficiente."
        ) as t:
            self.play(FadeOut(VGroup(ej3_nombre, sistema_3x3, det3_A, dets3,
                                     solucion3, nota3)),
                      run_time=min(t.duration * 0.2, 1.0))
            self.play(FadeIn(advertencia, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 2.5)

        with self.voiceover(
            text="Eso sí, cuando el sistema es pequeño, Cramer es elegante y directo. "
                 "Y además, nos da una fórmula explícita para cada incógnita, lo cual "
                 "es útil en demostraciones teóricas. Pero en la práctica, para "
                 "sistemas grandes, Gauss se lleva la corona."
        ) as t:
            self.esperar(t.duration)

        # ============================================================
        # 4. CIERRE
        # ============================================================
        self.play(FadeOut(VGroup(titulo, advertencia)), run_time=2)

# ---------- Escena 13: Eliminación de Gauss ----------
class D13_EliminacionGauss(CuadernoScene):
    def construct(self):
        # ============================================================
        # 1. OBJETOS
        # ============================================================
        titulo = Text("Eliminación de Gauss", font_size=42, color="#1A3A5C", weight=BOLD)

        # ===== Bloque 1: idea general =====
        idea_nombre = Text("¿Qué es la eliminación de Gauss?", font_size=28,
                          color="#1A3A5C", weight=BOLD)
        idea_texto = Tex(
            r"Es un m\'etodo para resolver sistemas lineales\\"
            r"transformando la matriz aumentada en una\\"
            r"\textbf{forma escalonada} mediante operaciones\\"
            r"elementales por fila.",
            tex_environment="center", font_size=24,
        )
        idea_texto.set_color("#2A4A6A")

        ops_nombre = Text("Operaciones elementales", font_size=26,
                         color="#1A3A5C", weight=BOLD)
        op1 = Tex(r"1. Intercambiar dos filas: $R_i \leftrightarrow R_j$",
                  tex_environment="center", font_size=22)
        op2 = Tex(r"2. Multiplicar por escalar: $R_i \to k R_i$",
                  tex_environment="center", font_size=22)
        op3 = Tex(r"3. Sumar m\'ultiplo: $R_i \to R_i + k R_j$",
                  tex_environment="center", font_size=22)
        for o in [op1, op2, op3]:
            o.set_color("#2A4A6A")
        ops_grupo = VGroup(op1, op2, op3).arrange(DOWN, center=True, buff=0.22)

        # ===== Bloque 2: forma escalonada =====
        esc_nombre = Text("Forma escalonada", font_size=28, color="#1A3A5C", weight=BOLD)
        esc_texto = Tex(
            r"Una matriz est\'a en forma escalonada si:\\"
            r"1. La primera entrada no nula de cada fila est\'a a la\\"
            r"derecha de la anterior.\\"
            r"2. Las filas de puros ceros van al final.",
            tex_environment="center", font_size=22,
        )
        esc_texto.set_color("#2A4A6A")

        esc_ej = Matrix([[1, 2, 3], [0, 1, 4], [0, 0, 5]],
                        h_buff=0.7, v_buff=0.5)
        esc_ej.set_color("#2A4A6A")
        esc_label = MathTex(r"\text{Escalonada}", font_size=22, color=TEAL)

        no_esc_ej = Matrix([[1, 2, 3], [0, 0, 0], [0, 1, 4]],
                          h_buff=0.7, v_buff=0.5)
        no_esc_ej.set_color("#2A4A6A")
        no_esc_label = MathTex(r"\text{NO escalonada}", font_size=22, color=RED)

        # ===== Bloque 3: sistema aumentado =====
        sis_nombre = Text("Sistema aumentado", font_size=28, color="#1A3A5C", weight=BOLD)
        sis_ec1 = MathTex(r"x + y + z = 6", font_size=30, color="#2A4A6A")
        sis_ec2 = MathTex(r"2x + 3y + z = 11", font_size=30, color="#2A4A6A")
        sis_ec3 = MathTex(r"x - y + 2z = 5", font_size=30, color="#2A4A6A")
        sistema = VGroup(sis_ec1, sis_ec2, sis_ec3).arrange(DOWN, aligned_edge=LEFT, buff=0.2)

        aumentada_label = MathTex(r"\longrightarrow", font_size=60, color="#E88B8B")

        # ===== Bloque 4: matriz aumentada [A | b] paso a paso =====
        ej_nombre = Text("Eliminación paso a paso", font_size=28, color="#1A3A5C", weight=BOLD)
        operacion = MathTex(r"R_2 \to R_2 - 2R_1", font_size=32, color="#E88B8B")

        A_0 = Matrix([[1, 1, 1], [2, 3, 1], [1, -1, 2]],
                     h_buff=0.55, v_buff=0.4)
        b_0 = Matrix([[6], [11], [5]], h_buff=0.5, v_buff=0.4)
        A_0.set_color("#2A4A6A")
        b_0.set_color("#2A4A6A")
        label_A = MathTex("A", font_size=28, color="#1A3A5C")
        label_b = MathTex(r"\vec{b}", font_size=28, color="#1A3A5C")
        linea_v = Line([0, 0.9, 0], [0, -0.9, 0], color="#1A3A5C", stroke_width=2)

        # ===== Bloque 5: sustitución hacia atrás =====
        back_nombre = Text("Sustitución hacia atrás", font_size=28, color="#1A3A5C", weight=BOLD)
        back_paso1 = MathTex(r"z = 3", font_size=36, color=TEAL)
        back_paso2 = MathTex(r"y - z = -1 \;\Rightarrow\; y = 2", font_size=32, color=TEAL)
        back_paso3 = MathTex(r"x + y + z = 6 \;\Rightarrow\; x = 1", font_size=32, color=TEAL)

        solucion_final = MathTex(r"x = 1, \quad y = 2, \quad z = 3",
                                 font_size=44, color=TEAL)
        verificacion = Tex(
            r"Verificaci\'on en las 3 ecuaciones $\;\checkmark$",
            tex_environment="center", font_size=24,
        )
        verificacion.set_color(TEAL)

        # ============================================================
        # 2. CONFIGURACIÓN
        # ============================================================
        titulo.move_to([0, 0, 0])
        titulo_final = titulo.copy().scale(0.7).move_to([0, 3.6, 0])

        # B1
        idea_nombre.move_to([0, 2.6, 0])
        idea_texto.move_to([0, 1.4, 0])
        ops_nombre.move_to([0, 0.0, 0])
        ops_grupo.move_to([0, -1.1, 0])

        # B2
        esc_nombre.move_to([0, 2.6, 0])
        esc_texto.move_to([-2.8, 1.4, 0])
        esc_ej.move_to([3.3, 1.4, 0])
        esc_label.move_to([3.3, 0.4, 0])
        no_esc_ej.move_to([3.3, -0.6, 0])
        no_esc_label.move_to([3.3, -1.6, 0])

        # B3
        sis_nombre.move_to([0, 2.6, 0])
        sistema.move_to([-3.5, 1.2, 0])
        aumentada_label.move_to([0.8, 1.2, 0])

        # B4
        ej_nombre.move_to([0, 2.6, 0])
        operacion.move_to([0, 1.9, 0])
        A_0.move_to([-1.4, 0.2, 0])
        b_0.move_to([1.4, 0.2, 0])
        label_A.move_to([-1.4, 1.3, 0])
        label_b.move_to([1.4, 1.3, 0])
        linea_v.move_to([0, 0.2, 0])

        # B5
        back_nombre.move_to([0, 2.6, 0])
        back_paso1.move_to([0, 1.5, 0])
        back_paso2.move_to([0, 0.5, 0])
        back_paso3.move_to([0, -0.5, 0])
        solucion_final.move_to([0, 0.8, 0])
        verificacion.move_to([0, -0.4, 0])

        # ============================================================
        # 3. ANIMACIONES
        # ============================================================
        self.set_speech_service(EdgeTTSService(voice="es-MX-JorgeNeural"))

        # ==== Intro ====
        with self.voiceover(
            text="Ahora vamos a ver el método de eliminación de Gauss, que es "
                 "probablemente el método más importante para resolver sistemas de "
                 "ecuaciones lineales. Es la base de casi todo lo que se hace en "
                 "cómputo científico."
        ) as t:
            self.play(Write(titulo), run_time=min(t.duration, 2.5))
            self.esperar(t.duration - 2.5)

        with self.voiceover(text="Empecemos con la idea general.") as t:
            self.play(Transform(titulo, titulo_final), run_time=min(t.duration, 1.5))
            self.play(FadeIn(idea_nombre), run_time=min(t.duration * 0.2, 0.8))
            self.esperar(t.duration - 2.3)

        # ==== Bloque 1: idea + operaciones ====
        with self.voiceover(
            text="La idea es esta: tomamos el sistema, lo escribimos como una matriz "
                 "aumentada, y mediante operaciones elementales por fila lo "
                 "transformamos en una forma triangular, que se llama forma "
                 "escalonada. Una vez ahí, es muy fácil resolver."
        ) as t:
            self.play(FadeIn(idea_texto, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="Las operaciones elementales son tres, las mismas que vimos con "
                 "Gauss-Jordan: intercambiar filas, multiplicar por un escalar, y "
                 "sumarle a una fila un múltiplo de otra."
        ) as t:
            self.play(FadeIn(ops_nombre), run_time=min(t.duration * 0.15, 0.7))
            self.play(FadeIn(op1, shift=DOWN * 0.3), run_time=min(t.duration * 0.15, 0.8))
            self.play(FadeIn(op2, shift=DOWN * 0.3), run_time=min(t.duration * 0.15, 0.8))
            self.play(FadeIn(op3, shift=DOWN * 0.3), run_time=min(t.duration * 0.15, 0.8))
            self.esperar(t.duration - 3.1)

        with self.voiceover(text="¿Y qué es la forma escalonada?") as t:
            self.play(FadeOut(VGroup(idea_nombre, idea_texto, ops_nombre, ops_grupo)),
                      run_time=min(t.duration, 1.5))
            self.esperar(t.duration - 1.5)

        # ==== Bloque 2: forma escalonada ====
        with self.voiceover(
            text="Una matriz está en forma escalonada si se cumplen dos condiciones. "
                 "Primera: la primera entrada no nula de cada fila está más a la "
                 "derecha que la de la fila anterior."
        ) as t:
            self.play(FadeIn(esc_nombre), run_time=min(t.duration * 0.15, 0.8))
            self.play(FadeIn(esc_texto, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 2.3)

        with self.voiceover(
            text="Y segunda: las filas de puros ceros van al final."
        ) as t:
            self.esperar(t.duration)

        with self.voiceover(
            text="Por ejemplo, esta matriz sí está en forma escalonada. El pivote de "
                 "la primera fila está en la columna uno, el de la segunda en la "
                 "columna dos, y el de la tercera en la columna tres. Va bajando en "
                 "escalera."
        ) as t:
            self.play(FadeIn(esc_ej), run_time=min(t.duration * 0.2, 1.2))
            self.play(FadeIn(esc_label, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.15, 0.8))
            self.esperar(t.duration - 2.0)

        with self.voiceover(
            text="En cambio, esta otra no lo está, porque el pivote de la tercera "
                 "fila está a la izquierda del de la segunda, y además hay una fila "
                 "de ceros antes de la última."
        ) as t:
            self.play(FadeIn(no_esc_ej), run_time=min(t.duration * 0.2, 1.2))
            self.play(FadeIn(no_esc_label, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.15, 0.8))
            self.esperar(t.duration - 2.0)

        with self.voiceover(text="Bien, ahora el ejemplo completo.") as t:
            self.play(FadeOut(VGroup(esc_nombre, esc_texto, esc_ej, esc_label,
                                     no_esc_ej, no_esc_label)),
                      run_time=min(t.duration, 1.5))
            self.esperar(t.duration - 1.5)

        # ==== Bloque 3: sistema aumentado ====
        with self.voiceover(
            text="Aquí tenemos un sistema de tres ecuaciones con tres incógnitas. La "
                 "solución es x igual a uno, y igual a dos, z igual a tres, pero "
                 "todavía no lo sabemos. Vamos a descubrirlo con Gauss."
        ) as t:
            self.play(FadeIn(sis_nombre), run_time=min(t.duration * 0.15, 0.8))
            self.play(FadeIn(sis_ec1), run_time=min(t.duration * 0.08, 0.5))
            self.play(FadeIn(sis_ec2), run_time=min(t.duration * 0.08, 0.5))
            self.play(FadeIn(sis_ec3), run_time=min(t.duration * 0.08, 0.5))
            self.esperar(t.duration - 2.3)

        with self.voiceover(
            text="El primer paso es escribir la matriz aumentada. Ponemos los "
                 "coeficientes de las incógnitas a la izquierda, y los términos "
                 "independientes a la derecha, separados por una línea vertical."
        ) as t:
            self.play(FadeIn(aumentada_label), run_time=min(t.duration * 0.1, 0.6))
            self.esperar(t.duration - 0.6)

        with self.voiceover(text="Veamos el proceso paso a paso.") as t:
            self.play(FadeOut(VGroup(sis_nombre, sistema, aumentada_label)),
                      run_time=min(t.duration, 1.2))
            self.play(FadeIn(ej_nombre), FadeIn(label_A), FadeIn(label_b),
                      run_time=min(t.duration * 0.2, 0.8))
            self.esperar(t.duration - 2.0)

        # ==== Bloque 4: eliminación ====
        with self.voiceover(
            text="Aquí está nuestra matriz aumentada. A la izquierda los coeficientes, "
                 "a la derecha los términos independientes. El pivote de la primera "
                 "fila es uno, y queremos eliminar los elementos debajo de él."
        ) as t:
            self.play(FadeIn(A_0), FadeIn(b_0), FadeIn(linea_v),
                      run_time=min(t.duration * 0.3, 1.8))
            self.esperar(t.duration - 1.8)

        # ---- Paso 1: R2 - 2R1 → R2 ----
        with self.voiceover(
            text="Paso uno: eliminamos el dos de la segunda fila. Restamos dos veces "
                 "la fila uno a la fila dos. La nueva fila dos en A queda: cero, uno, "
                 "menos uno. Y en b: menos uno."
        ) as t:
            self.play(FadeIn(operacion), run_time=min(t.duration * 0.1, 0.5))
            A_1 = Matrix([[1, 1, 1], [0, 1, -1], [1, -1, 2]],
                         h_buff=0.55, v_buff=0.4)
            b_1 = Matrix([[6], [-1], [5]], h_buff=0.5, v_buff=0.4)
            A_1.set_color("#2A4A6A"); b_1.set_color("#2A4A6A")
            A_1.move_to(A_0.get_center()); b_1.move_to(b_0.get_center())
            r_fila = SurroundingRectangle(
                VGroup(*[A_0.get_entries()[3 + k] for k in range(3)]),
                color=RED, buff=0.08,
            )
            self.play(Create(r_fila), run_time=min(t.duration * 0.08, 0.5))
            self.play(ReplacementTransform(A_0, A_1),
                      ReplacementTransform(b_0, b_1),
                      run_time=min(t.duration * 0.3, 2))
            self.play(FadeOut(r_fila), run_time=0.4)
            self.esperar(t.duration - 3.4)
            A_0, b_0 = A_1, b_1

        with self.voiceover(text="Siguiente.") as t:
            self.play(FadeOut(operacion), run_time=0.5)
            operacion = MathTex(r"R_3 \to R_3 - R_1", font_size=32, color="#E88B8B")
            operacion.move_to([0, 1.9, 0])
            self.esperar(t.duration - 0.5)

        # ---- Paso 2: R3 - R1 → R3 ----
        with self.voiceover(
            text="Paso dos: eliminamos el uno de la tercera fila. Restamos fila uno a "
                 "fila tres. Nueva fila tres en A: cero, menos dos, uno. En b: menos "
                 "uno."
        ) as t:
            self.play(FadeIn(operacion), run_time=0.5)
            A_2 = Matrix([[1, 1, 1], [0, 1, -1], [0, -2, 1]],
                         h_buff=0.55, v_buff=0.4)
            b_2 = Matrix([[6], [-1], [-1]], h_buff=0.5, v_buff=0.4)
            A_2.set_color("#2A4A6A"); b_2.set_color("#2A4A6A")
            A_2.move_to(A_0.get_center()); b_2.move_to(b_0.get_center())
            r_fila = SurroundingRectangle(
                VGroup(*[A_0.get_entries()[6 + k] for k in range(3)]),
                color=RED, buff=0.08,
            )
            self.play(Create(r_fila), run_time=0.5)
            self.play(ReplacementTransform(A_0, A_2),
                      ReplacementTransform(b_0, b_2),
                      run_time=min(t.duration * 0.3, 2))
            self.play(FadeOut(r_fila), run_time=0.4)
            self.esperar(t.duration - 3.4)
            A_0, b_0 = A_2, b_2

        with self.voiceover(text="Bien.") as t:
            self.play(FadeOut(operacion), run_time=0.5)
            operacion = MathTex(r"R_3 \to R_3 + 2R_2", font_size=32, color="#E88B8B")
            operacion.move_to([0, 1.9, 0])
            self.esperar(t.duration - 0.5)

        # ---- Paso 3: R3 + 2R2 → R3 ----
        with self.voiceover(
            text="Paso tres: ahora eliminamos el menos dos de la tercera fila. Le "
                 "sumamos dos veces la fila dos. Nueva fila tres en A: cero, cero, "
                 "menos uno. En b: menos tres."
        ) as t:
            self.play(FadeIn(operacion), run_time=0.5)
            A_3 = Matrix([[1, 1, 1], [0, 1, -1], [0, 0, -1]],
                         h_buff=0.55, v_buff=0.4)
            b_3 = Matrix([[6], [-1], [-3]], h_buff=0.5, v_buff=0.4)
            A_3.set_color("#2A4A6A"); b_3.set_color("#2A4A6A")
            A_3.move_to(A_0.get_center()); b_3.move_to(b_0.get_center())
            r_fila = SurroundingRectangle(
                VGroup(*[A_0.get_entries()[6 + k] for k in range(3)]),
                color=RED, buff=0.08,
            )
            self.play(Create(r_fila), run_time=0.5)
            self.play(ReplacementTransform(A_0, A_3),
                      ReplacementTransform(b_0, b_3),
                      run_time=min(t.duration * 0.3, 2))
            self.play(FadeOut(r_fila), run_time=0.4)
            self.esperar(t.duration - 3.4)
            A_0, b_0 = A_3, b_3

        with self.voiceover(text="Último paso de eliminación.") as t:
            self.play(FadeOut(operacion), run_time=0.5)
            operacion = MathTex(r"R_3 \to -R_3", font_size=32, color="#E88B8B")
            operacion.move_to([0, 1.9, 0])
            self.esperar(t.duration - 0.5)

        # ---- Paso 4: -R3 → R3 ----
        with self.voiceover(
            text="Paso cuatro: multiplicamos la fila tres por menos uno, para que el "
                 "pivote quede positivo. Nueva fila tres en A: cero, cero, uno. En b: "
                 "tres."
        ) as t:
            self.play(FadeIn(operacion), run_time=0.5)
            A_4 = Matrix([[1, 1, 1], [0, 1, -1], [0, 0, 1]],
                         h_buff=0.55, v_buff=0.4)
            b_4 = Matrix([[6], [-1], [3]], h_buff=0.5, v_buff=0.4)
            A_4.set_color("#2A4A5C"); b_4.set_color("#E88B8B")
            A_4.move_to(A_0.get_center()); b_4.move_to(b_0.get_center())
            r_fila = SurroundingRectangle(
                VGroup(*[A_0.get_entries()[6 + k] for k in range(3)]),
                color=RED, buff=0.08,
            )
            self.play(Create(r_fila), run_time=0.5)
            self.play(ReplacementTransform(A_0, A_4),
                      ReplacementTransform(b_0, b_4),
                      run_time=min(t.duration * 0.3, 2))
            self.play(FadeOut(r_fila), run_time=0.4)
            self.esperar(t.duration - 3.4)
            A_0, b_0 = A_4, b_4

        with self.voiceover(
            text="Perfecto. La matriz ya está en forma escalonada: los pivotes van en "
                 "escalera: uno, uno, uno. Ahora podemos resolver con sustitución "
                 "hacia atrás."
        ) as t:
            self.play(FadeOut(operacion), run_time=0.5)
            self.esperar(t.duration - 0.5)

        with self.voiceover(text="Vamos a resolver.") as t:
            self.play(FadeOut(VGroup(ej_nombre, label_A, label_b, A_0, b_0, linea_v)),
                      run_time=min(t.duration, 1.5))
            self.play(FadeIn(back_nombre), run_time=min(t.duration * 0.2, 0.8))
            self.esperar(t.duration - 2.3)

        # ==== Bloque 5: sustitución hacia atrás ====
        with self.voiceover(
            text="La tercera fila nos dice directamente: z es igual a tres."
        ) as t:
            self.play(FadeIn(back_paso1, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="La segunda fila es: y menos z igual a menos uno. Como z ya vale "
                 "tres, entonces y menos tres es menos uno, y por lo tanto y es dos."
        ) as t:
            self.play(FadeIn(back_paso2, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="La primera fila es: x más y más z igual a seis. Sustituyendo, x más "
                 "dos más tres es seis, entonces x es uno."
        ) as t:
            self.play(FadeIn(back_paso3, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="La solución es x igual a uno, y igual a dos, z igual a tres. Y si "
                 "verifican en el sistema original, van a ver que se cumplen las tres "
                 "ecuaciones."
        ) as t:
            self.play(FadeOut(VGroup(back_paso1, back_paso2, back_paso3)),
                      run_time=min(t.duration * 0.2, 0.8))
            self.play(FadeIn(solucion_final, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.play(FadeIn(verificacion, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.2, 1.0))
            self.esperar(t.duration - 3.3)

        with self.voiceover(
            text="Y este es el método de Gauss. Es el más usado en la práctica, "
                 "porque es sistemático y eficiente. Funciona para cualquier tamaño de "
                 "sistema. Las operaciones son las mismas, solo hay más pasos. En la "
                 "siguiente escena vamos a ver una variante: Gauss-Jordan, que sigue "
                 "un poco más allá y elimina también hacia arriba."
        ) as t:
            self.esperar(t.duration)

        # ============================================================
        # 4. CIERRE
        # ============================================================
        self.play(FadeOut(VGroup(titulo, back_nombre, solucion_final, verificacion)),
                  run_time=2)


# ---------- Escena 14: Gauss-Jordan ----------
class D14_GaussJordan(CuadernoScene):
    def construct(self):
        # ============================================================
        # 1. OBJETOS
        # ============================================================
        titulo = Text("Gauss-Jordan", font_size=42, color="#1A3A5C", weight=BOLD)

        # ===== Bloque 1: diferencia con Gauss =====
        dif_nombre = Text("La diferencia con Gauss", font_size=28, color="#1A3A5C", weight=BOLD)
        dif_texto = Tex(
            r"Gauss se detiene en la \textbf{forma escalonada}.\\"
            r"Gauss-Jordan contin\'ua eliminando hacia arriba\\"
            r"hasta llegar a la \textbf{forma escalonada reducida}.",
            tex_environment="center", font_size=24,
        )
        dif_texto.set_color("#2A4A6A")

        ref_label = Text("Forma escalonada (Gauss)", font_size=22, color="#4A6A8A", weight=BOLD)
        ref_mat = Matrix([[1, 1, 1], [0, 1, -1], [0, 0, 1]],
                         h_buff=0.6, v_buff=0.4)
        ref_mat.set_color("#2A4A6A")

        flecha_dif = MathTex(r"\longrightarrow", font_size=60, color="#E88B8B")

        rref_label = Text("Forma reducida (Gauss-Jordan)", font_size=22,
                         color="#4A6A8A", weight=BOLD)
        rref_mat = Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                          h_buff=0.6, v_buff=0.4)
        rref_mat.set_color("#2A4A6A")

        # ===== Bloque 2: qué es la forma escalonada reducida =====
        rref_nombre = Text("Forma escalonada reducida", font_size=28,
                          color="#1A3A5C", weight=BOLD)
        rref_texto = Tex(
            r"Adem\'as de estar escalonada, cumple:\\"
            r"1. Cada pivote vale exactamente 1.\\"
            r"2. En cada columna pivote, todos los dem\'as\\"
            r"   elementos son cero.",
            tex_environment="center", font_size=22,
        )
        rref_texto.set_color("#2A4A6A")

        # ===== Bloque 3: ejemplo paso a paso =====
        ej_nombre = Text("Continuando el ejemplo anterior", font_size=28,
                        color="#1A3A5C", weight=BOLD)
        operacion = MathTex(r"R_2 \to R_2 + R_3", font_size=32, color="#E88B8B")

        A_0 = Matrix([[1, 1, 1], [0, 1, -1], [0, 0, 1]],
                     h_buff=0.55, v_buff=0.4)
        b_0 = Matrix([[6], [-1], [3]], h_buff=0.5, v_buff=0.4)
        A_0.set_color("#2A4A6A"); b_0.set_color("#2A4A6A")
        label_A = MathTex("A", font_size=28, color="#1A3A5C")
        label_b = MathTex(r"\vec{b}", font_size=28, color="#1A3A5C")
        linea_v = Line([0, 0.9, 0], [0, -0.9, 0], color="#1A3A5C", stroke_width=2)

        # ===== Bloque 4: ventaja =====
        vent_nombre = Text("¿Cuándo usar Gauss-Jordan?", font_size=28,
                          color="#1A3A5C", weight=BOLD)
        vent_texto = Tex(
            r"\textbf{Ventaja:} la soluci\'on se lee directamente,\\"
            r"sin sustituci\'on hacia atr\'as.\\"
            r"\textbf{Desventaja:} requiere m\'as operaciones.",
            tex_environment="center", font_size=24,
        )
        vent_texto.set_color("#2A4A6A")
        vent_tip = Tex(
            r"\'Util cuando hay que resolver muchos sistemas\\"
            r"con la misma matriz $A$",
            tex_environment="center", font_size=22,
        )
        vent_tip.set_color("#E88B8B")

        # ============================================================
        # 2. CONFIGURACIÓN
        # ============================================================
        titulo.move_to([0, 0, 0])
        titulo_final = titulo.copy().scale(0.7).move_to([0, 3.6, 0])

        # B1
        dif_nombre.move_to([0, 2.6, 0])
        dif_texto.move_to([0, 1.5, 0])
        ref_label.move_to([-3.5, 0.2, 0])
        ref_mat.move_to([-3.5, -0.6, 0])
        flecha_dif.move_to([0, -0.6, 0])
        rref_label.move_to([3.5, 0.2, 0])
        rref_mat.move_to([3.5, -0.6, 0])

        # B2
        rref_nombre.move_to([0, 2.6, 0])
        rref_texto.move_to([0, 1.0, 0])

        # B3
        ej_nombre.move_to([0, 2.6, 0])
        operacion.move_to([0, 1.9, 0])
        A_0.move_to([-1.4, 0.2, 0])
        b_0.move_to([1.4, 0.2, 0])
        label_A.move_to([-1.4, 1.3, 0])
        label_b.move_to([1.4, 1.3, 0])
        linea_v.move_to([0, 0.2, 0])

        # B4
        vent_nombre.move_to([0, 2.4, 0])
        vent_texto.move_to([0, 0.8, 0])
        vent_tip.move_to([0, -1.0, 0])

        # ============================================================
        # 3. ANIMACIONES
        # ============================================================
        self.set_speech_service(EdgeTTSService(voice="es-MX-JorgeNeural"))

        # ==== Intro ====
        with self.voiceover(
            text="Muy bien, ahora vamos con Gauss-Jordan. Ya conocen el método de "
                 "Gauss, ahora vamos a ver su versión extendida. La idea es simple: "
                 "Gauss se queda a medio camino, y Gauss-Jordan va hasta el final."
        ) as t:
            self.play(Write(titulo), run_time=min(t.duration, 2.5))
            self.esperar(t.duration - 2.5)

        with self.voiceover(text="Veamos la diferencia.") as t:
            self.play(Transform(titulo, titulo_final), run_time=min(t.duration, 1.5))
            self.play(FadeIn(dif_nombre), run_time=min(t.duration * 0.2, 0.8))
            self.esperar(t.duration - 2.3)

        # ==== Bloque 1: diferencia ====
        with self.voiceover(
            text="Gauss se detiene cuando llega a la forma escalonada: una matriz "
                 "triangular superior, donde los pivotes van en escalera. Con eso ya "
                 "podemos resolver por sustitución hacia atrás, como vimos en la "
                 "escena anterior."
        ) as t:
            self.play(FadeIn(dif_texto, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="Gauss-Jordan va un paso más allá: sigue eliminando también hacia "
                 "arriba, hasta que la matriz de coeficientes se convierte en la "
                 "identidad. Es decir, llega a la forma escalonada reducida."
        ) as t:
            self.play(FadeIn(ref_label), FadeIn(ref_mat),
                      run_time=min(t.duration * 0.15, 1.0))
            self.play(FadeIn(flecha_dif), run_time=min(t.duration * 0.1, 0.6))
            self.play(FadeIn(rref_label), FadeIn(rref_mat),
                      run_time=min(t.duration * 0.15, 1.0))
            self.esperar(t.duration - 2.6)

        with self.voiceover(
            text="Cuando la matriz queda así, la solución del sistema ya está en la "
                 "última columna. No hace falta sustituir hacia atrás."
        ) as t:
            self.esperar(t.duration)

        with self.voiceover(text="¿Qué es exactamente la forma reducida?") as t:
            self.play(FadeOut(VGroup(dif_nombre, dif_texto, ref_label, ref_mat,
                                     flecha_dif, rref_label, rref_mat)),
                      run_time=min(t.duration, 1.5))
            self.play(FadeIn(rref_nombre), run_time=min(t.duration * 0.2, 0.8))
            self.esperar(t.duration - 2.3)

        # ==== Bloque 2: RREF ====
        with self.voiceover(
            text="La forma escalonada reducida cumple todo lo de la forma escalonada, "
                 "y además dos condiciones extra. Primera: cada pivote vale exactamente "
                 "uno. Y segunda: en cada columna pivote, todos los demás elementos son "
                 "cero, arriba y abajo del pivote."
        ) as t:
            self.play(FadeIn(rref_texto, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.8))
            self.esperar(t.duration - 1.8)

        with self.voiceover(
            text="Esto significa que en cada columna pivote hay un uno y puros ceros. "
                 "Nada más. Es la forma más limpia que puede tener una matriz."
        ) as t:
            self.esperar(t.duration)

        with self.voiceover(text="Veamos cómo se llega a ella.") as t:
            self.play(FadeOut(VGroup(rref_nombre, rref_texto)),
                      run_time=min(t.duration, 1.5))
            self.play(FadeIn(ej_nombre), FadeIn(label_A), FadeIn(label_b),
                      run_time=min(t.duration * 0.2, 0.8))
            self.esperar(t.duration - 2.3)

        # ==== Bloque 3: ejemplo ====
        with self.voiceover(
            text="Vamos a continuar con el mismo sistema de la escena anterior. Gauss "
                 "nos dejó la matriz en esta forma triangular: pivotes uno, uno, uno, "
                 "y debajo de la diagonal puros ceros. Pero arriba de la diagonal "
                 "todavía hay elementos distintos de cero."
        ) as t:
            self.play(FadeIn(A_0), FadeIn(b_0), FadeIn(linea_v),
                      run_time=min(t.duration * 0.3, 1.8))
            self.esperar(t.duration - 1.8)

        with self.voiceover(
            text="Gauss-Jordan va a eliminar esos elementos uno por uno, empezando por "
                 "los de arriba y yendo hacia arriba."
        ) as t:
            self.esperar(t.duration)

        # ---- Paso 1: R2 + R3 → R2 ----
        with self.voiceover(
            text="Paso uno: eliminamos el menos uno que está en la segunda fila, "
                 "tercera columna. Sumamos fila dos más fila tres. La nueva fila dos "
                 "en A: cero, uno, cero. En b: dos."
        ) as t:
            self.play(FadeIn(operacion), run_time=0.5)
            A_1 = Matrix([[1, 1, 1], [0, 1, 0], [0, 0, 1]],
                         h_buff=0.55, v_buff=0.4)
            b_1 = Matrix([[6], [2], [3]], h_buff=0.5, v_buff=0.4)
            A_1.set_color("#2A4A6A"); b_1.set_color("#2A4A6A")
            A_1.move_to(A_0.get_center()); b_1.move_to(b_0.get_center())
            r_fila = SurroundingRectangle(
                VGroup(*[A_0.get_entries()[3 + k] for k in range(3)]),
                color=RED, buff=0.08,
            )
            self.play(Create(r_fila), run_time=0.5)
            self.play(ReplacementTransform(A_0, A_1),
                      ReplacementTransform(b_0, b_1),
                      run_time=min(t.duration * 0.3, 2))
            self.play(FadeOut(r_fila), run_time=0.4)
            self.esperar(t.duration - 3.4)
            A_0, b_0 = A_1, b_1

        with self.voiceover(text="Siguiente.") as t:
            self.play(FadeOut(operacion), run_time=0.5)
            operacion = MathTex(r"R_1 \to R_1 - R_3", font_size=32, color="#E88B8B")
            operacion.move_to([0, 1.9, 0])
            self.esperar(t.duration - 0.5)

        # ---- Paso 2: R1 - R3 → R1 ----
        with self.voiceover(
            text="Paso dos: eliminamos el uno de la primera fila, tercera columna. "
                 "Restamos fila uno menos fila tres. La nueva fila uno en A: uno, uno, "
                 "cero. En b: tres."
        ) as t:
            self.play(FadeIn(operacion), run_time=0.5)
            A_2 = Matrix([[1, 1, 0], [0, 1, 0], [0, 0, 1]],
                         h_buff=0.55, v_buff=0.4)
            b_2 = Matrix([[3], [2], [3]], h_buff=0.5, v_buff=0.4)
            A_2.set_color("#2A4A6A"); b_2.set_color("#2A4A6A")
            A_2.move_to(A_0.get_center()); b_2.move_to(b_0.get_center())
            r_fila = SurroundingRectangle(
                VGroup(*[A_0.get_entries()[0 + k] for k in range(3)]),
                color=RED, buff=0.08,
            )
            self.play(Create(r_fila), run_time=0.5)
            self.play(ReplacementTransform(A_0, A_2),
                      ReplacementTransform(b_0, b_2),
                      run_time=min(t.duration * 0.3, 2))
            self.play(FadeOut(r_fila), run_time=0.4)
            self.esperar(t.duration - 3.4)
            A_0, b_0 = A_2, b_2

        with self.voiceover(text="Último paso.") as t:
            self.play(FadeOut(operacion), run_time=0.5)
            operacion = MathTex(r"R_1 \to R_1 - R_2", font_size=32, color="#E88B8B")
            operacion.move_to([0, 1.9, 0])
            self.esperar(t.duration - 0.5)

        # ---- Paso 3: R1 - R2 → R1 ----
        with self.voiceover(
            text="Paso tres: eliminamos el uno de la primera fila, segunda columna. "
                 "Restamos fila uno menos fila dos. La nueva fila uno en A: uno, cero, "
                 "cero. En b: uno."
        ) as t:
            self.play(FadeIn(operacion), run_time=0.5)
            A_3 = Matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                         h_buff=0.55, v_buff=0.4)
            b_3 = Matrix([[1], [2], [3]], h_buff=0.5, v_buff=0.4)
            A_3.set_color("#2A4A5C"); b_3.set_color("#E88B8B")
            A_3.move_to(A_0.get_center()); b_3.move_to(b_0.get_center())
            r_fila = SurroundingRectangle(
                VGroup(*[A_0.get_entries()[0 + k] for k in range(3)]),
                color=RED, buff=0.08,
            )
            self.play(Create(r_fila), run_time=0.5)
            self.play(ReplacementTransform(A_0, A_3),
                      ReplacementTransform(b_0, b_3),
                      run_time=min(t.duration * 0.3, 2))
            self.play(FadeOut(r_fila), run_time=0.4)
            self.esperar(t.duration - 3.4)
            A_0, b_0 = A_3, b_3

        with self.voiceover(
            text="¡Y listo! A la izquierda tenemos la identidad. Y a la derecha, en "
                 "rojo, tenemos directamente la solución del sistema: x igual a uno, "
                 "y igual a dos, z igual a tres."
        ) as t:
            self.play(FadeOut(operacion), run_time=0.5)
            self.esperar(t.duration - 0.5)

        with self.voiceover(
            text="Como ven, en Gauss-Jordan no hace falta sustituir hacia atrás. La "
                 "solución aparece directamente en la última columna. Esa es la gran "
                 "ventaja."
        ) as t:
            self.esperar(t.duration)

        with self.voiceover(text="Bien.") as t:
            self.play(FadeOut(VGroup(ej_nombre, label_A, label_b, A_0, b_0, linea_v)),
                      run_time=min(t.duration, 1.5))
            self.play(FadeIn(vent_nombre), run_time=min(t.duration * 0.2, 0.8))
            self.esperar(t.duration - 2.3)

        # ==== Bloque 4: ventaja ====
        with self.voiceover(
            text="Entonces, ¿cuándo usar Gauss-Jordan y cuándo Gauss? La ventaja de "
                 "Gauss-Jordan es que la solución se lee directamente, sin sustitución "
                 "hacia atrás. Eso es muy cómodo cuando ya tienes la matriz en forma "
                 "reducida."
        ) as t:
            self.play(FadeIn(vent_texto, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="La desventaja es que requiere más operaciones. Porque además de "
                 "eliminar hacia abajo, como Gauss, también hay que eliminar hacia "
                 "arriba. Eso significa más cálculos."
        ) as t:
            self.esperar(t.duration)

        with self.voiceover(
            text="Entonces, Gauss es más eficiente cuando solo necesitas resolver un "
                 "sistema. Pero Gauss-Jordan es muy útil cuando tienes que resolver "
                 "muchos sistemas con la misma matriz A, porque una vez que la reduces "
                 "a la identidad, cualquier vector b nuevo te da la solución "
                 "directamente."
        ) as t:
            self.play(FadeIn(vent_tip, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="Y de hecho, Gauss-Jordan es el método que se usa internamente para "
                 "calcular inversas, como vimos en la escena ocho. Porque para "
                 "calcular la inversa, lo que hacemos es exactamente esto: reducir A a "
                 "la identidad mientras aplicamos las mismas operaciones a la identidad "
                 "de la derecha."
        ) as t:
            self.esperar(t.duration)

        with self.voiceover(
            text="Así que ya lo saben: Gauss y Gauss-Jordan son dos versiones del mismo "
                 "método. Gauss se queda en la forma triangular y usa sustitución hacia "
                 "atrás. Gauss-Jordan va hasta la forma reducida y da la solución "
                 "directa. Los dos son importantes, y cada uno tiene su lugar."
        ) as t:
            self.esperar(t.duration)

        # ============================================================
        # 4. CIERRE
        # ============================================================
        self.play(FadeOut(VGroup(titulo, vent_nombre, vent_texto, vent_tip)),
                  run_time=2)

# ---------- Escena 15: Clasificación de sistemas ----------
class D15_ClasificacionSistemas(CuadernoScene):
    def construct(self):
        # ============================================================
        # 1. OBJETOS
        # ============================================================
        titulo = Text("Clasificación de sistemas", font_size=42, color="#1A3A5C", weight=BOLD)

        # ===== Bloque 1: los tres tipos =====
        intro_nombre = Text("Tres tipos de sistemas", font_size=28, color="#1A3A5C", weight=BOLD)

        tipo1 = Tex(r"1. \textbf{Compatible determinado}: soluci\'on \'unica",
                    tex_environment="center", font_size=24)
        tipo2 = Tex(r"2. \textbf{Compatible indeterminado}: infinitas soluciones",
                    tex_environment="center", font_size=24)
        tipo3 = Tex(r"3. \textbf{Incompatible}: sin soluci\'on",
                    tex_environment="center", font_size=24)
        for tt in [tipo1, tipo2, tipo3]:
            tt.set_color("#2A4A6A")
        tipos_grupo = VGroup(tipo1, tipo2, tipo3).arrange(DOWN, center=True, buff=0.3)

        criterio = Tex(
            r"La forma escalonada de la matriz aumentada\\"
            r"nos dice cu\'al es el caso, sin resolverlo.",
            tex_environment="center", font_size=22,
        )
        criterio.set_color("#6A7A8A")

        # ===== Bloque 2: DETERMINADO =====
        det_nombre = Text("1. Compatible determinado", font_size=28,
                        color="#1A3A5C", weight=BOLD)
        det_cond = Tex(r"Tantas ecuaciones independientes como inc\'ognitas",
                       tex_environment="center", font_size=22)
        det_cond.set_color("#4A6A8A")

        det_sis_1 = MathTex(r"x + y = 3", font_size=28, color="#2A4A6A")
        det_sis_2 = MathTex(r"x - y = 1", font_size=28, color="#2A4A6A")
        det_sistema = VGroup(det_sis_1, det_sis_2).arrange(DOWN, aligned_edge=LEFT, buff=0.25)

        det_flecha = MathTex(r"\longrightarrow", font_size=44, color="#E88B8B")

        det_A = Matrix([[1, 0], [0, 1]], h_buff=0.5, v_buff=0.4)
        det_b = Matrix([[2], [1]], h_buff=0.4, v_buff=0.4)
        det_A.set_color("#2A4A6A")
        det_b.set_color("#2A4A6A")

        det_concl = Tex(r"La soluci\'on se lee directo: $x=2,\; y=1$",
                       tex_environment="center", font_size=24)
        det_concl.set_color(TEAL)

        # ===== Bloque 3: INDETERMINADO =====
        ind_nombre = Text("2. Compatible indeterminado", font_size=28,
                         color="#1A3A5C", weight=BOLD)
        ind_cond = Tex(r"Aparece una fila de ceros $\Rightarrow$ variable libre",
                      tex_environment="center", font_size=22)
        ind_cond.set_color("#4A6A8A")

        ind_sis_1 = MathTex(r"x + y + z = 3", font_size=24, color="#2A4A6A")
        ind_sis_2 = MathTex(r"2x + 2y + 2z = 6", font_size=24, color="#2A4A6A")
        ind_sistema = VGroup(ind_sis_1, ind_sis_2).arrange(DOWN, aligned_edge=LEFT, buff=0.2)

        ind_flecha = MathTex(r"\longrightarrow", font_size=40, color="#E88B8B")

        ind_A = Matrix([[1, 1, 1], [0, 0, 0]], h_buff=0.35, v_buff=0.4)
        ind_b = Matrix([[3], [0]], h_buff=0.4, v_buff=0.4)
        ind_A.set_color("#2A4A6A")
        ind_b.set_color("#2A4A6A")

        ind_concl_1 = Tex(r"La fila de ceros no aporta informaci\'on",
                         tex_environment="center", font_size=22)
        ind_concl_1.set_color("#4A6A8A")
        ind_concl_2 = Tex(r"$z$ es libre: infinitas soluciones",
                         tex_environment="center", font_size=24)
        ind_concl_2.set_color(TEAL)
        ind_concl = VGroup(ind_concl_1, ind_concl_2).arrange(DOWN, buff=0.15)

        # ===== Bloque 4: INCOMPATIBLE =====
        inc_nombre = Text("3. Incompatible", font_size=28,
                        color="#1A3A5C", weight=BOLD)
        inc_cond = Tex(r"Aparece una fila del tipo $[0\; 0\; \cdots\; 0 \;|\; c]$ con $c \neq 0$",
                      tex_environment="center", font_size=22)
        inc_cond.set_color("#4A6A8A")

        inc_sis_1 = MathTex(r"x + y = 2", font_size=28, color="#2A4A6A")
        inc_sis_2 = MathTex(r"x + y = 5", font_size=28, color="#2A4A6A")
        inc_sistema = VGroup(inc_sis_1, inc_sis_2).arrange(DOWN, aligned_edge=LEFT, buff=0.25)

        inc_flecha = MathTex(r"\longrightarrow", font_size=44, color="#E88B8B")

        inc_A = Matrix([[1, 1], [0, 0]], h_buff=0.5, v_buff=0.4)
        inc_b = Matrix([[2], [3]], h_buff=0.4, v_buff=0.4)
        inc_A.set_color("#2A4A6A")
        inc_b.set_color("#2A4A6A")

        inc_concl_1 = Tex(r"La segunda fila dice: $0 = 3$",
                         tex_environment="center", font_size=22)
        inc_concl_1.set_color("#4A6A8A")
        inc_concl_2 = Tex(r"Imposible: el sistema no tiene soluci\'on",
                         tex_environment="center", font_size=24)
        inc_concl_2.set_color(RED)
        inc_concl = VGroup(inc_concl_1, inc_concl_2).arrange(DOWN, buff=0.15)

        # ===== Bloque 5: tabla resumen =====
        res_nombre = Text("Resumen: cómo identificarlos", font_size=28,
                        color="#1A3A5C", weight=BOLD)

        res_row1 = Tex(r"\textbf{Determinado}: \quad pivotes en todas las columnas",
                      tex_environment="center", font_size=22)
        res_row2 = Tex(r"\textbf{Indeterminado}: \quad alguna fila $[0 \cdots 0 \,|\, 0]$",
                      tex_environment="center", font_size=22)
        res_row3 = Tex(r"\textbf{Incompatible}: \quad alguna fila $[0 \cdots 0 \,|\, c]$, $c \neq 0$",
                      tex_environment="center", font_size=22)
        res_row1.set_color(TEAL)
        res_row2.set_color("#1A3A5C")
        res_row3.set_color(RED)
        res_grupo = VGroup(res_row1, res_row2, res_row3).arrange(DOWN, aligned_edge=LEFT, buff=0.3)

        res_nota = Tex(
            r"Esto se ve \textbf{directamente} en la forma escalonada.",
            tex_environment="center", font_size=22,
        )
        res_nota.set_color("#6A7A8A")

        # ============================================================
        # 2. CONFIGURACIÓN
        # ============================================================
        titulo.move_to([0, 0, 0])
        titulo_final = titulo.copy().scale(0.7).move_to([0, 3.6, 0])

        # B1
        intro_nombre.move_to([0, 2.6, 0])
        tipos_grupo.move_to([0, 1.2, 0])
        criterio.move_to([0, -1.0, 0])

        # ---- B2: DETERMINADO ----
        det_nombre.move_to([0, 2.6, 0])
        det_cond.move_to([0, 1.9, 0])
        det_sistema.move_to([-3.8, 0.4, 0])
        det_flecha.move_to([-1.2, 0.4, 0])
        det_A.move_to([1.0, 0.4, 0])
        det_b.move_to([2.6, 0.4, 0])
        det_concl.move_to([0, -1.4, 0])

        # ---- B3: INDETERMINADO ----
        ind_nombre.move_to([0, 2.6, 0])
        ind_cond.move_to([0, 1.9, 0])
        ind_sistema.move_to([-4.0, 0.4, 0])
        ind_flecha.move_to([-1.2, 0.4, 0])
        ind_A.move_to([0.5, 0.4, 0])
        ind_b.move_to([2.5, 0.4, 0])
        ind_concl.move_to([0, -1.5, 0])

        # ---- B4: INCOMPATIBLE ----
        inc_nombre.move_to([0, 2.6, 0])
        inc_cond.move_to([0, 1.9, 0])
        inc_sistema.move_to([-3.8, 0.4, 0])
        inc_flecha.move_to([-1.2, 0.4, 0])
        inc_A.move_to([1.0, 0.4, 0])
        inc_b.move_to([2.4, 0.4, 0])
        inc_concl.move_to([0, -1.5, 0])

        # ---- B5: RESUMEN ----
        res_nombre.move_to([0, 2.6, 0])
        res_grupo.move_to([0, 0.6, 0])
        res_nota.move_to([0, -1.4, 0])

        # ============================================================
        # 2b. LÍNEAS AUMENTADAS (auto-calculadas, DESPUÉS de mover A y b)
        # ============================================================
        def linea_aumentada(mat_A, mat_b, pad=0.12):
            """Línea vertical entre los bordes reales de A y b."""
            x = (mat_A.get_right()[0] + mat_b.get_left()[0]) / 2
            y_top = max(mat_A.get_top()[1], mat_b.get_top()[1]) + pad
            y_bot = min(mat_A.get_bottom()[1], mat_b.get_bottom()[1]) - pad
            return Line([x, y_top, 0], [x, y_bot, 0],
                        color="#1A3A5C", stroke_width=2)

        det_linea = linea_aumentada(det_A, det_b)
        ind_linea = linea_aumentada(ind_A, ind_b)
        inc_linea = linea_aumentada(inc_A, inc_b)

        # ============================================================
        # 3. ANIMACIONES
        # ============================================================
        self.set_speech_service(EdgeTTSService(voice="es-MX-JorgeNeural"))

        # ==== Intro ====
        with self.voiceover(
            text="Ahora vamos a cerrar el bloque de sistemas con un tema muy "
                 "importante: cómo clasificar un sistema según la cantidad de "
                 "soluciones que tiene."
        ) as t:
            self.play(Write(titulo), run_time=min(t.duration, 2.5))
            self.esperar(t.duration - 2.5)

        with self.voiceover(text="Básicamente, hay tres tipos.") as t:
            self.play(Transform(titulo, titulo_final), run_time=min(t.duration, 1.5))
            self.play(FadeIn(intro_nombre), run_time=min(t.duration * 0.15, 0.8))
            self.esperar(t.duration - 2.3)

        # ==== Bloque 1 ====
        with self.voiceover(
            text="El primero es el sistema compatible determinado: tiene solución "
                 "única. El segundo es el compatible indeterminado: tiene infinitas "
                 "soluciones. Y el tercero es el incompatible: no tiene ninguna "
                 "solución."
        ) as t:
            self.play(FadeIn(tipo1, shift=DOWN * 0.3), run_time=min(t.duration * 0.15, 1.0))
            self.play(FadeIn(tipo2, shift=DOWN * 0.3), run_time=min(t.duration * 0.15, 1.0))
            self.play(FadeIn(tipo3, shift=DOWN * 0.3), run_time=min(t.duration * 0.15, 1.0))
            self.esperar(t.duration - 3.0)

        with self.voiceover(
            text="Lo bueno es que no hace falta resolver el sistema para saber de qué "
                 "tipo es. Basta con mirar la forma escalonada de la matriz aumentada. "
                 "Vamos a ver un ejemplo de cada uno."
        ) as t:
            self.play(FadeIn(criterio, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(text="Empecemos con el determinado.") as t:
            self.play(FadeOut(VGroup(intro_nombre, tipos_grupo, criterio)),
                      run_time=min(t.duration, 1.5))
            self.play(FadeIn(det_nombre), run_time=min(t.duration * 0.15, 0.8))
            self.esperar(t.duration - 2.3)

        # ==== Bloque 2: DETERMINADO ====
        with self.voiceover(
            text="Sistema compatible determinado. Tenemos dos ecuaciones con dos "
                 "incógnitas: x más y igual a tres, y x menos y igual a uno. Son dos "
                 "ecuaciones independientes."
        ) as t:
            self.play(FadeIn(det_cond, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.2, 1.0))
            self.play(FadeIn(det_sis_1), run_time=min(t.duration * 0.1, 0.6))
            self.play(FadeIn(det_sis_2), run_time=min(t.duration * 0.1, 0.6))
            self.esperar(t.duration - 2.2)

        with self.voiceover(
            text="Al escribir la matriz aumentada y reducirla, obtenemos la "
                 "identidad a la izquierda. Eso significa que los pivotes cubren todas "
                 "las columnas, y la solución se lee directamente."
        ) as t:
            self.play(FadeIn(det_flecha), run_time=min(t.duration * 0.1, 0.6))
            self.play(FadeIn(det_A), run_time=min(t.duration * 0.12, 0.8))
            self.play(FadeIn(det_linea), FadeIn(det_b),
                      run_time=min(t.duration * 0.15, 1.0))
            self.esperar(t.duration - 2.4)

        with self.voiceover(
            text="En este caso, x igual a dos, y igual a uno. Solución única."
        ) as t:
            self.play(FadeIn(det_concl, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(text="Ahora el indeterminado.") as t:
            self.play(FadeOut(VGroup(det_nombre, det_cond, det_sistema, det_flecha,
                                     det_A, det_linea, det_b, det_concl)),
                      run_time=min(t.duration, 1.5))
            self.play(FadeIn(ind_nombre), run_time=min(t.duration * 0.15, 0.8))
            self.esperar(t.duration - 2.3)

        # ==== Bloque 3: INDETERMINADO ====
        with self.voiceover(
            text="Sistema compatible indeterminado. Aquí tenemos dos ecuaciones con "
                 "tres incógnitas: x más y más z igual a tres, y dos x más dos y más "
                 "dos z igual a seis. Pero ojo, la segunda ecuación es simplemente el "
                 "doble de la primera."
        ) as t:
            self.play(FadeIn(ind_cond, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.2, 1.0))
            self.play(FadeIn(ind_sis_1), run_time=min(t.duration * 0.08, 0.5))
            self.play(FadeIn(ind_sis_2), run_time=min(t.duration * 0.08, 0.5))
            self.esperar(t.duration - 2.0)

        with self.voiceover(
            text="Al reducir la matriz aumentada, la segunda fila se convierte en puros "
                 "ceros, incluyendo el término independiente. Es decir, cero igual a "
                 "cero. Esa fila no aporta información nueva."
        ) as t:
            self.play(FadeIn(ind_flecha), run_time=min(t.duration * 0.08, 0.5))
            self.play(FadeIn(ind_A), run_time=min(t.duration * 0.12, 0.8))
            self.play(FadeIn(ind_linea), FadeIn(ind_b),
                      run_time=min(t.duration * 0.15, 1.0))
            self.esperar(t.duration - 2.3)

        with self.voiceover(
            text="Entonces nos queda una sola ecuación con tres incógnitas. Eso "
                 "significa que dos incógnitas quedan libres. Podemos darles el valor "
                 "que queramos, y siempre habrá solución. Por eso hay infinitas "
                 "soluciones."
        ) as t:
            self.play(FadeIn(ind_concl, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(text="Y por último, el incompatible.") as t:
            self.play(FadeOut(VGroup(ind_nombre, ind_cond, ind_sistema, ind_flecha,
                                     ind_A, ind_linea, ind_b, ind_concl)),
                      run_time=min(t.duration, 1.5))
            self.play(FadeIn(inc_nombre), run_time=min(t.duration * 0.15, 0.8))
            self.esperar(t.duration - 2.3)

        # ==== Bloque 4: INCOMPATIBLE ====
        with self.voiceover(
            text="Sistema incompatible. Tenemos x más y igual a dos, y x más y igual a "
                 "cinco. A simple vista ya se ve raro: la misma combinación x más y no "
                 "puede valer dos y cinco al mismo tiempo."
        ) as t:
            self.play(FadeIn(inc_cond, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.15, 0.8))
            self.play(FadeIn(inc_sis_1), run_time=min(t.duration * 0.1, 0.5))
            self.play(FadeIn(inc_sis_2), run_time=min(t.duration * 0.1, 0.5))
            self.esperar(t.duration - 1.8)

        with self.voiceover(
            text="Al reducir, la segunda fila se convierte en ceros en la parte de A, "
                 "pero el término independiente queda tres. Es decir, cero igual a tres. "
                 "Eso es imposible, y significa que el sistema no tiene solución."
        ) as t:
            self.play(FadeIn(inc_flecha), run_time=min(t.duration * 0.08, 0.5))
            self.play(FadeIn(inc_A), run_time=min(t.duration * 0.12, 0.8))
            self.play(FadeIn(inc_linea), FadeIn(inc_b),
                      run_time=min(t.duration * 0.15, 1.0))
            self.esperar(t.duration - 2.3)

        with self.voiceover(
            text="Y fíjense que la diferencia con el caso anterior es solo el término "
                 "independiente. Si la fila de ceros termina en cero, es indeterminado. "
                 "Si termina en un número distinto de cero, es incompatible."
        ) as t:
            self.play(FadeIn(inc_concl, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(text="Bien. Vamos a resumir todo esto.") as t:
            self.play(FadeOut(VGroup(inc_nombre, inc_cond, inc_sistema, inc_flecha,
                                     inc_A, inc_linea, inc_b, inc_concl)),
                      run_time=min(t.duration, 1.5))
            self.play(FadeIn(res_nombre), run_time=min(t.duration * 0.15, 0.8))
            self.esperar(t.duration - 2.3)

        # ==== Bloque 5: tabla resumen ====
        with self.voiceover(
            text="Recapitulando. Determinado: hay pivotes en todas las columnas de la "
                 "parte de A, sin filas de ceros. La solución es única."
        ) as t:
            self.play(FadeIn(res_row1, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="Indeterminado: aparece al menos una fila de ceros, incluyendo el "
                 "término independiente. Hay variables libres, y por lo tanto infinitas "
                 "soluciones."
        ) as t:
            self.play(FadeIn(res_row2, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="E incompatible: aparece una fila con ceros en la parte de A pero un "
                 "número distinto de cero en el término independiente. Cero igual a "
                 "algo distinto de cero, imposible. Sin solución."
        ) as t:
            self.play(FadeIn(res_row3, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="Y todo esto se puede saber viendo únicamente la forma escalonada de "
                 "la matriz aumentada. No hace falta resolver el sistema completo, ni "
                 "sustituir nada. Con un vistazo, ya sabemos qué tipo de sistema "
                 "tenemos."
        ) as t:
            self.play(FadeIn(res_nota, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="Con esto cerramos el bloque de sistemas de ecuaciones. Ya saben "
                 "resolverlos con Gauss, con Gauss-Jordan, con Cramer, y ahora también "
                 "saben clasificarlos. Esa es una caja de herramientas bastante completa."
        ) as t:
            self.esperar(t.duration)

        # ============================================================
        # 4. CIERRE
        # ============================================================
        self.play(FadeOut(VGroup(titulo, res_nombre, res_grupo, res_nota)),
                  run_time=2)

# ---------- Escena 16: Conclusiones ----------
class D16_Conclusiones(CuadernoScene):
    def construct(self):
        # ============================================================
        # 1. OBJETOS
        # ============================================================
        titulo = Text("Conclusiones", font_size=42, color="#1A3A5C", weight=BOLD)

        # ===== Bloque 1: recapitulación =====
        recap_nombre = Text("Lo que aprendimos", font_size=30, color="#1A3A5C", weight=BOLD)

        # 4 pilares: matriz bullet + título + subtemas
        pilar1_b = MathTex(r"\bullet", font_size=36, color="#E88B8B")
        pilar1_t = Text("Matrices", font_size=26, color="#1A3A5C", weight=BOLD)
        pilar1_s = Text("definición, tipos, suma, escalar, producto, transpuesta",
                        font_size=18, color="#4A6A8A")
        pilar1 = VGroup(pilar1_b, pilar1_t, pilar1_s)

        pilar2_b = MathTex(r"\bullet", font_size=36, color="#E88B8B")
        pilar2_t = Text("Inversa", font_size=26, color="#1A3A5C", weight=BOLD)
        pilar2_s = Text("Gauss-Jordan, condición det ≠ 0",
                        font_size=18, color="#4A6A8A")
        pilar2 = VGroup(pilar2_b, pilar2_t, pilar2_s)

        pilar3_b = MathTex(r"\bullet", font_size=36, color="#E88B8B")
        pilar3_t = Text("Determinantes", font_size=26, color="#1A3A5C", weight=BOLD)
        pilar3_s = Text("2×2, Sarrus, cofactores, propiedades",
                        font_size=18, color="#4A6A8A")
        pilar3 = VGroup(pilar3_b, pilar3_t, pilar3_s)

        pilar4_b = MathTex(r"\bullet", font_size=36, color="#E88B8B")
        pilar4_t = Text("Sistemas lineales", font_size=26, color="#1A3A5C", weight=BOLD)
        pilar4_s = Text("Cramer, Gauss, Gauss-Jordan, clasificación",
                        font_size=18, color="#4A6A8A")
        pilar4 = VGroup(pilar4_b, pilar4_t, pilar4_s)

        pilares = VGroup(pilar1, pilar2, pilar3, pilar4)

        # ===== Bloque 2: aplicaciones =====
        app_nombre = Text("¿Para qué sirve todo esto?", font_size=30,
                        color="#1A3A5C", weight=BOLD)

        app1_t = Text("Ingeniería", font_size=24, color="#1A3A5C", weight=BOLD)
        app1_s = Text("Estructuras, circuitos, control", font_size=18, color="#4A6A8A")
        app1 = VGroup(app1_t, app1_s).arrange(DOWN, buff=0.1)

        app2_t = Text("Física", font_size=24, color="#1A3A5C", weight=BOLD)
        app2_s = Text("Mecánica cuántica, relatividad", font_size=18, color="#4A6A8A")
        app2 = VGroup(app2_t, app2_s).arrange(DOWN, buff=0.1)

        app3_t = Text("Computación", font_size=24, color="#1A3A5C", weight=BOLD)
        app3_s = Text("Gráficos 3D, machine learning", font_size=18, color="#4A6A8A")
        app3 = VGroup(app3_t, app3_s).arrange(DOWN, buff=0.1)

        app4_t = Text("Optimización", font_size=24, color="#1A3A5C", weight=BOLD)
        app4_s = Text("Economía, logística, IA", font_size=18, color="#4A6A8A")
        app4 = VGroup(app4_t, app4_s).arrange(DOWN, buff=0.1)

        # Cajas alrededor de cada aplicación
        # (se crean después de posicionar, en sección 2b)
        # ===== Bloque 3: cierre =====
        cierre_t = Text("Fin del curso", font_size=48, color="#1A3A5C", weight=BOLD)
        cierre_s = Text("Gracias por acompañarme en este recorrido",
                        font_size=28, color="#4A6A8A")
        cierre_linea = Line(LEFT * 3, RIGHT * 3, color="#E88B8B", stroke_width=2)

        # ============================================================
        # 2. CONFIGURACIÓN
        # ============================================================
        titulo.move_to([0, 0, 0])
        titulo_final = titulo.copy().scale(0.7).move_to([0, 3.6, 0])

        # B1: recap
        recap_nombre.move_to([0, 2.6, 0])
        # Cada pilar: bullet a la izquierda, título al centro-izq, subtemas abajo
        for i, pilar in enumerate(pilares):
            y = 1.6 - i * 0.9
            b, t, s = pilar
            b.move_to([-5.6, y, 0])
            t.move_to([-4.8 + t.width / 2, y, 0])
            s.move_to([-4.8 + s.width / 2, y - 0.38, 0])

        # B2: apps en 2x2
        app_nombre.move_to([0, 2.6, 0])
        app1.move_to([-3.3, 0.9, 0])
        app2.move_to([3.3, 0.9, 0])
        app3.move_to([-3.3, -0.5, 0])
        app4.move_to([3.3, -0.5, 0])

        # B3: cierre
        cierre_t.move_to([0, 1.0, 0])
        cierre_linea.move_to([0, 0.2, 0])
        cierre_s.move_to([0, -0.8, 0])

        # ============================================================
        # 2b. CAJAS (creadas DESPUÉS de posicionar)
        # ============================================================
        cajas_apps = VGroup()
        for app in [app1, app2, app3, app4]:
            caja = SurroundingRectangle(app, color="#E88B8B", buff=0.25)
            caja.set_stroke(width=1.5)
            cajas_apps.add(caja)

        # ============================================================
        # 3. ANIMACIONES
        # ============================================================
        self.set_speech_service(EdgeTTSService(voice="es-MX-JorgeNeural"))

        # ==== Intro ====
        with self.voiceover(
            text="Bueno, hemos llegado al final de este curso de Álgebra Superior. "
                 "Vamos a hacer un repaso rápido de todo lo que vimos."
        ) as t:
            self.play(Write(titulo), run_time=min(t.duration, 2.5))
            self.esperar(t.duration - 2.5)

        with self.voiceover(text="Empecemos por los cuatro grandes pilares.") as t:
            self.play(Transform(titulo, titulo_final), run_time=min(t.duration, 1.5))
            self.play(FadeIn(recap_nombre), run_time=min(t.duration * 0.2, 0.8))
            self.esperar(t.duration - 2.3)

        # ==== Bloque 1: recap de pilares ====
        with self.voiceover(
            text="Primero, las matrices. Vimos qué son, cómo se clasifican, y todas "
                 "las operaciones básicas: suma, resta, multiplicación por escalar, "
                 "producto de matrices, y transpuesta."
        ) as t:
            self.play(FadeIn(pilar1_b), FadeIn(pilar1_t),
                      run_time=min(t.duration * 0.15, 0.8))
            self.play(FadeIn(pilar1_s, shift=DOWN * 0.2),
                      run_time=min(t.duration * 0.25, 1.2))
            self.esperar(t.duration - 2.0)

        with self.voiceover(
            text="Después, la inversa. Aprendimos a calcularla con el método de "
                 "Gauss-Jordan, y entendimos que solo existe cuando el determinante es "
                 "distinto de cero."
        ) as t:
            self.play(FadeIn(pilar2_b), FadeIn(pilar2_t),
                      run_time=min(t.duration * 0.15, 0.8))
            self.play(FadeIn(pilar2_s, shift=DOWN * 0.2),
                      run_time=min(t.duration * 0.25, 1.2))
            self.esperar(t.duration - 2.0)

        with self.voiceover(
            text="Luego, los determinantes. Vimos cómo calcularlos para dos por dos, "
                 "para tres por tres con la regla de Sarrus, y para cualquier tamaño "
                 "con expansión por cofactores. Y repasamos sus propiedades más útiles."
        ) as t:
            self.play(FadeIn(pilar3_b), FadeIn(pilar3_t),
                      run_time=min(t.duration * 0.15, 0.8))
            self.play(FadeIn(pilar3_s, shift=DOWN * 0.2),
                      run_time=min(t.duration * 0.25, 1.2))
            self.esperar(t.duration - 2.0)

        with self.voiceover(
            text="Y por último, los sistemas lineales. Los resolvimos por varios "
                 "métodos: Cramer, eliminación de Gauss, Gauss-Jordan. Y aprendimos a "
                 "clasificarlos según la cantidad de soluciones."
        ) as t:
            self.play(FadeIn(pilar4_b), FadeIn(pilar4_t),
                      run_time=min(t.duration * 0.15, 0.8))
            self.play(FadeIn(pilar4_s, shift=DOWN * 0.2),
                      run_time=min(t.duration * 0.25, 1.2))
            self.esperar(t.duration - 2.0)

        with self.voiceover(
            text="Eso es una caja de herramientas bastante completa. Cuatro bloques "
                 "que se conectan entre sí."
        ) as t:
            self.esperar(t.duration)

        with self.voiceover(text="Ahora, ¿para qué sirve todo esto?") as t:
            self.play(FadeOut(VGroup(recap_nombre, pilares)),
                      run_time=min(t.duration, 1.5))
            self.play(FadeIn(app_nombre), run_time=min(t.duration * 0.2, 0.8))
            self.esperar(t.duration - 2.3)

        # ==== Bloque 2: aplicaciones ====
        with self.voiceover(
            text="Las matrices y los determinantes están en todos lados. En "
                 "ingeniería, por ejemplo, se usan para analizar estructuras, "
                 "resolver circuitos eléctricos, y diseñar sistemas de control."
        ) as t:
            self.play(FadeIn(app1), Create(cajas_apps[0]),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="En física, aparecen en la mecánica cuántica, en la relatividad, y en "
                 "prácticamente cualquier área que involucre sistemas de ecuaciones."
        ) as t:
            self.play(FadeIn(app2), Create(cajas_apps[1]),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="En computación, son la base de los gráficos 3D, del machine learning, "
                 "del procesamiento de imágenes, y de muchísimos algoritmos."
        ) as t:
            self.play(FadeIn(app3), Create(cajas_apps[2]),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="Y en optimización, que se aplica en economía, en logística, en "
                 "inteligencia artificial, los sistemas lineales son el punto de "
                 "partida de casi todo."
        ) as t:
            self.play(FadeIn(app4), Create(cajas_apps[3]),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="Así que aunque a veces parezca abstracto, todo esto tiene aplicaciones "
                 "muy concretas y muy importantes. Están en el corazón de la tecnología "
                 "moderna."
        ) as t:
            self.esperar(t.duration)

        # ==== Bloque 3: cierre ====
        with self.voiceover(text="Bueno, es hora de cerrar.") as t:
            self.play(
                FadeOut(VGroup(app_nombre, app1, app2, app3, app4, cajas_apps)),
                run_time=min(t.duration, 1.5),
            )
            self.esperar(t.duration - 1.5)

        with self.voiceover(
            text="Con esto terminamos este recorrido por las matrices y los "
                 "determinantes. Espero que les haya servido, y que ahora vean estos "
                 "conceptos con más claridad que al principio."
        ) as t:
            self.play(Write(cierre_t), run_time=min(t.duration * 0.4, 2.5))
            self.esperar(t.duration - 2.5)

        with self.voiceover(
            text="La práctica es clave. Resuelvan ejercicios, jueguen con matrices, "
                 "calculen determinantes a mano. Cuanto más lo hagan, más natural se "
                 "les va a hacer. Esto no se aprende solo leyendo, se aprende haciendo."
        ) as t:
            self.play(Create(cierre_linea), run_time=min(t.duration * 0.2, 1.0))
            self.esperar(t.duration - 1.0)

        with self.voiceover(
            text="Si este material les sirvió, compártanlo con quienes lo necesiten. Y "
                 "nos vemos en el siguiente tema. Muchas gracias, y hasta luego."
        ) as t:
            self.play(FadeIn(cierre_s, shift=DOWN * 0.3),
                      run_time=min(t.duration * 0.3, 1.5))
            self.esperar(t.duration - 1.5)

        # ---------- 4. CIERRE ----------
        self.play(
            FadeOut(VGroup(titulo, cierre_t, cierre_linea, cierre_s)),
            run_time=2,
        )
