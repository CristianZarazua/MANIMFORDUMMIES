from manim import *

class Inicio(Scene):
    def construct(self):
        # Creación del objeto Tex
        materia = Tex(
            r"Cálculo IV",
            tex_environment="center"
        )

        por = Tex(
            r"Presentado por:",
            tex_environment="center"
        )

        nombre1 = Tex(
            r"Cristian Michel Zarazua Castañeda",
            tex_environment="center"
        ).set_color(BLUE).scale(1.5)

        nombre2 = Tex(
            r"Oswaldo Díaz Díaz",
            tex_environment="center"
        ).set_color(PURPLE).scale(1.5)

        nombre3 = Tex(
            r"Nombre 3",
            tex_environment="center"
        ).set_color(PINK).scale(1.5)

        nombre4 = Tex(
            r"Nombre 4",
            tex_environment="center"
        ).set_color(RED).scale(1.5)

        nombre5 = Tex(
            r"María del Carmen Ramírez Torres",
            tex_environment="center"
        ).set_color(ORANGE).scale(1.5)

        # Modificaciones de posición, color y tamaño
        materia.move_to([0, 0, 0]).scale(1.5).set_color_by_gradient(RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE)
        por.move_to([0, 0, 0]).scale(1.5).set_color_by_gradient(RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE)
        
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
