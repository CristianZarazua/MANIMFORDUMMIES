from manim import *

"""class PackedCircleEye(Scene):
    def construct(self):
        # 1. Crear los círculos que formarán el ojo
        #    Cada círculo tiene posición (x, y), radio y color.
        circles_data = [
            # Contorno del ojo (Círculos grandes)
            {"pos": [-1.5, 0.5, 0], "radius": 0.8, "color": BLUE_D},
            {"pos": [1.5, 0.5, 0], "radius": 0.8, "color": BLUE_D},
            {"pos": [-1.8, -0.2, 0], "radius": 0.6, "color": BLUE_D},
            {"pos": [1.8, -0.2, 0], "radius": 0.6, "color": BLUE_D},
            {"pos": [-1.0, -0.8, 0], "radius": 0.5, "color": BLUE_D},
            {"pos": [1.0, -0.8, 0], "radius": 0.5, "color": BLUE_D},
            
            # Iris (Círculos marrones de diferente tamaño y opacidad)
            {"pos": [-0.5, 0.0, 0], "radius": 0.7, "color": MAROON, "opacity": 1.0},
            {"pos": [0.5, 0.0, 0], "radius": 0.7, "color": MAROON, "opacity": 1.0},
            {"pos": [0.0, 0.2, 0], "radius": 0.6, "color": GOLD, "opacity": 0.7},
            {"pos": [-0.2, -0.3, 0], "radius": 0.4, "color": LIGHT_BROWN, "opacity": 0.9},
            {"pos": [0.3, -0.3, 0], "radius": 0.4, "color": LIGHT_BROWN, "opacity": 0.9},
            
            # Pupila (Círculos negros)
            {"pos": [-0.1, 0.1, 0], "radius": 0.3, "color": BLACK},
            {"pos": [0.1, -0.1, 0], "radius": 0.2, "color": BLACK},
            
            # Brillo (Círculos blancos)
            {"pos": [-0.3, 0.4, 0], "radius": 0.1, "color": WHITE},
            {"pos": [0.3, -0.3, 0], "radius": 0.05, "color": WHITE},
        ]

        # 2. Crear los objetos Circle de Manim
        circles = VGroup()
        for data in circles_data:
            c = Circle(
                radius=data["radius"],
                color=data["color"],
                fill_color=data["color"],
                fill_opacity=data.get("opacity", 1.0),
                stroke_width=2 if data["color"] == BLUE_D else 0
            )
            c.move_to(data["pos"])
            circles.add(c)

        # 3. Agregar un párpado (opcional)
        eyelid = Arc(
            radius=2.2, angle=PI, arc_center=ORIGIN, color=BLACK, stroke_width=8
        ).move_to([0, 1.2, 0])

        # 4. Animar la creación
        self.play(Create(circles), run_time=3)
        self.wait(0.5)
        self.play(Create(eyelid))
        self.wait(2) """

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
