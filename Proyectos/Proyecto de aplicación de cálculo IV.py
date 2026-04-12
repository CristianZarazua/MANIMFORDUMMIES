from manim import *

class Inicio(Scene):
    def construct(self):
        # Creación del objeto Tex
        materia = Tex(
            r"Proyecto de aplicación\\Cálculo IV",
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
        texto_unificado.move_to([0, 0, 0])  # <-- Esto es para centrar en la pantalla, estos 5 textos unificados

        # Animaciones
        self.play(Write(materia))
        self.wait(5)
        self.play(ReplacementTransform(materia, por))
        self.wait(3)
        self.play(ReplacementTransform(por, texto_unificado))
        self.wait(8)
        self.play(FadeOut(texto_unificado), run_time=2)



""" 
# 1. Atardecer cálido (ideal para títulos principales)
GRADIENT_ATARDECER = [RED, ORANGE, YELLOW, "#FFD700"]

# 2. Océano profundo (para textos secundarios o subtítulos)
GRADIENT_OCEANO = ["#1A5F7A", "#22A39F", "#57C4AD", "#B5EAEA"]

# 3. Aurora boreal (muy estético para fondos o textos destacados)
GRADIENT_AURORA = ["#2E4C6D", "#396EB0", "#4E9F3D", "#D8E9A8"]

# 4. Cerezo en flor (para detalles o acentos románticos)
GRADIENT_CEREZO = ["#FFB7B2", "#FF9AA2", "#E2A9FF", "#C5A3FF"]

# 5. Cítrico refrescante (ideal para llamadas a la acción)
GRADIENT_CITRICO = ["#F4A261", "#E9C46A", "#2A9D8F", "#264653"]

# 6. Metálico elegante (escala de grises con un toque de color)
GRADIENT_METALICO = ["#CFD8DC", "#90A4AE", "#607D8B", "#455A64"]

# 7. Fuego y lava (para textos que quieren llamar la atención)
GRADIENT_FUEGO = [RED, "#FF4500", ORANGE, YELLOW]

# 8. Menta fresca (verde menta a azul cielo)
GRADIENT_MENTA = ["#98DDCA", "#D3E0EA", "#A2D5F2", "#79C2D0"]

# 9. Uva madura (morados intensos)
GRADIENT_UVA = [PURPLE, "#8A2BE2", "#9370DB", "#BA55D3"]

# 10. Arcoíris completo (para textos divertidos o infantiles)
GRADIENT_ARCOIRIS = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE] 
"""
