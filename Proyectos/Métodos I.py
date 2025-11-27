from manim import *
from numpy import *

class bienvenida(Scene):
    def construct(self):
        # Textos principales
        texto1 = Text("Métodos Numéricos I")
        texto2 = Text("Método de Newton-Raphson aplicado en")
        texto3 = Text("La ecuación de Colebrook-White")
        texto4 = Text("Por:")

        texto1.set_color(RED)
        texto2.set_color(ORANGE)
        texto3.set_color(YELLOW)
        texto4.set_color(GREEN)

        nombre1 = Tex(
            r"Cristian Michel Zarazua Castañeda",
            tex_environment="center"
        ).set_color(BLUE)

        nombre2 = Tex(
            r"Karla Fernanda Reyes Castañeda",
            tex_environment="center"
        ).set_color(PURPLE)

        nombre3 = Tex(
            r"Valeria Paola Gómez Hernández",
            tex_environment="center"
        ).set_color(PINK)

        texto_unificado = VGroup(nombre1, nombre2, nombre3)
        texto_unificado.arrange(DOWN, aligned_edge=ORIGIN)
        texto_unificado.move_to(ORIGIN)  # <-- CENTRADO EXACTO EN PANTALLA

        # Animaciones
        self.play(Write(texto1), run_time=3)
        self.wait(2)
        self.play(ReplacementTransform(texto1, texto2))
        self.wait()
        self.play(ReplacementTransform(texto2, texto3))
        self.wait()
        self.play(ReplacementTransform(texto3, texto4))
        self.wait()

        self.play(ReplacementTransform(texto4, texto_unificado))
        self.wait(3)
        self.play(FadeOut(texto_unificado), run_time=2)

class introd(Scene):
    def construct(self):
        # Aquí vamos a explicar el método de Newton-Raphson
        texto8 = Tex(
            r"Primero, ¿Qué es el método de Newton-Raphson?",
            tex_environment="center"
        )
        
        texto9 = Tex(
            r"El método de Newton-Raphson se trata de un procedimiento basado\\"
            r"en la derivada, para encontrar aproximaciones a las raíces de\\"
            r"una función real que sea derivable.",
            tex_environment="center"
        )

        texto10 = Tex(
            r"""
            Es muy útil en el análisis numérico, sobre todo para aproximar raíces de \\
            polinomios en los cuales los métodos convencionales no funcionan \\
            (por ejemplo: $x^{3} + 2x - 5 = 0$, $x^{5} - x + 1 = 0$) \\
            o para otro tipo de funciones, como por ejemplo: $2\cos{x} - x^{2} = 0$ \\
            o $x - \cos{x} = 0$.
            """,
            tex_environment="center"
        )

        texto11 = Tex(
            r"""
            Este método sirve inclusive para aproximar valores como por ejemplo: \\
            $\sqrt{3}, \ \sqrt[4]{3}, \ \sqrt[5]{247}, \pi$, encontrando de manera \\
            aproximada las raíces de las siguientes ecuaciones $x^{2} - 3 = 0,$ \\
            $x^{4} - 3 = 0, \ x^{5} - 247 = 0, \ \cos{x} + 1 = 0$, respectivamente. \\
            """,
            tex_environment="center"
        )

        # Posiciones
        texto8.move_to([0, 3, 0])
        texto9.move_to([0, 1.5, 0])
        texto10.move_to([0, -0.5, 0])
        texto11.move_to([0, -2.8, 0])

        texto8.scale(0.8)
        texto9.scale(0.8)
        texto10.scale(0.8)
        texto11.scale(0.8)
        texto8.set_color(RED)
        texto9.set_color(ORANGE)
        texto10.set_color(GOLD)
        texto11.set_color(YELLOW)

        # Animación
        self.play(Write(texto8))
        self.play(Write(texto9))
        self.play(Write(texto10))
        self.play(Write(texto11))
        self.wait(28)
        self.play(FadeOut(texto8, texto9, texto10, texto11), run_time=2)

class requisitos(Scene):
    def construct(self):
        # Aquí vamos a relacionarlo con Colebrook-White
        texto12 = Tex(
            r"Segundo, ¿Qué problema real se podría solucionar con este método?",
            tex_environment="center"
        )
        texto13 = Tex(
            r"""En nuestro ejercicio ficticio del problema del agua en la UNAM \\
            encontramos que la ecuación de Colebrook-White podría resolver esta \\
            incógnita, ya que esta ecuación es usada comúnmente en el sector \\
            hidráulico, ya que nos permite aproximar con gran precisión la \\
            rugosidad de las paredes de las tuberías, el diámetro del tubo y \\
            el consecuente desgaste que el uso constante genera.""",
            tex_environment="center"
        )

        texto14 = Tex(
            r"""Mencionamos mucho estas ecuaciones, pero ¿cuáles son?""",
            tex_environment="center"
        )

        # Posiciones
        texto12.move_to([0, 2, 0])
        texto13.move_to([0, 0, 0])
        texto14.move_to([0, -2, 0])

        # Escalas
        texto12.scale(0.8)
        texto13.scale(0.8)
        texto14.scale(0.8)
        texto12.set_color(BLUE)
        texto13.set_color(TEAL)
        texto14.set_color(GREEN)

        # Animación
        self.play(Write(texto12))
        self.play(Write(texto13))
        self.play(Write(texto14))
        self.wait(8)
        self.play(FadeOut(texto12), FadeOut(texto13), FadeOut(texto14), run_time=2)

class ecuaciones(Scene):
    # Aquí vamos a describir las ecuaciones que vamos a usar
    def construct(self):
        # Texto explicativo
        texto15 = Tex(
            r"""En primer lugar tenemos la forma general \\
             del método de Newton-Raphson""",tex_environment="center")

        # Ecuación
        ecuacion1 = MathTex(r"x_{1} = x_{0} - \frac{f(x_{0})}{f'(x_{0})}")

        texto16 = Tex(
            r"""Donde $x_{0}$ es el valor inicial, $f(x)$ es la función a \\
             evaluar y $f'(x)$ es la derivada de la función original.""",tex_environment="center")

        texto17 = Tex(
            r"""Luego tenemos la ecuación de Colebrook–White. En nuestro \\
             caso utilizaremos la versión empleada en hidráulica; no \\
             obstante también mencionaremos tanto la ecuación original \\
             como su forma adaptada a este campo. La versión más conocida \\ 
             es la siguiente:""",tex_environment="center")

        ecuacion2 = MathTex(r"\frac{1}{\sqrt{\lambda}} = -2 \log_{10} \left(\frac{k / D}{3.7} + \frac{2.51}{Re \sqrt{\lambda}}\right)")

        texto18 = Tex(
            r"""Donde $Re$ es el número de Reynolds, $k / D$ hace alusión a la \\
             rugosidad relativa y $\lambda$ representa el factor de fricción.""",tex_environment="center")


        texto19 = Tex(
            r"""En esta ocasión utilizaremos su versión reducida. El \\
             motivo y procedimiento para que se de esta reducción pueden \\
             consultarlo en las fuentes que dejaremos en el documento y \\
             a las cuales hemos hecho referencia previamente.""",tex_environment="center")

        ecuacion3 = MathTex(r"\frac{1}{\sqrt{\lambda}} = -2 \log_{10} \left(Re \sqrt{\lambda}\right) - 0.8")

        texto15.move_to([0, 1.5, 0])
        ecuacion1.move_to([0, 0, 0])
        texto16.move_to([0, -1.5, 0])
        texto17.move_to([0, 1.5, 0])
        ecuacion2.move_to([0, -1, 0])
        texto18.move_to([0, -2.5, 0])
        texto19.move_to([0, 0.5, 0])
        ecuacion3.move_to([0, -1.5, 0])
        texto15.set_color(PURPLE)
        ecuacion1.set_color(PINK)
        texto16.set_color(RED)
        texto17.set_color(ORANGE)
        ecuacion2.set_color(GOLD)
        texto18.set_color(YELLOW)
        texto19.set_color(GREEN)
        ecuacion3.set_color(BLUE)

        self.play(Write(texto15))
        self.play(Write(ecuacion1))
        self.play(Write(texto16))
        self.wait(6)
        self.play(ReplacementTransform(texto15, texto17))
        self.play(ReplacementTransform(ecuacion1, ecuacion2))
        self.play(ReplacementTransform(texto16, texto18))
        self.wait(6)
        self.play(FadeOut(texto18))
        self.play(ReplacementTransform(texto17, texto19))
        self.play(ReplacementTransform(ecuacion2, ecuacion3))
        self.wait(6)
        self.play(FadeOut(texto19), FadeOut(ecuacion3), run_time=2)

class aprox(Scene):
    def construct(self):
        # ---------------------------------------------------------
        # Textos introductorios sobre tuberías
        # ---------------------------------------------------------
        texto20 = Tex(
            r"""En el diseño de tuberías, el coeficiente de fricción $\lambda$ \\
            depende del diámetro interno $D$, la rugosidad del material $\varepsilon$ \\
            y el régimen de flujo turbulento. La ecuación que gobierna este \\
            comportamiento es la ecuación implícita de Colebrook-White.""",
            tex_environment="center"
        ).set_color(PINK)

        texto21 = Tex(
            r"""A continuación se resolverá la ecuación de Colebrook-White \\
             usando el método iterativo de Newton-Raphson. \\
             (Se hará de manera rápida por cuestiones de tiempo)""",
            tex_environment="center"
        ).set_color(PURPLE)

        # ---------------------------------------------------------
        # 1. Ecuación general de Colebrook–White
        # ---------------------------------------------------------
        eq1 = MathTex(
            r"\frac{1}{\sqrt{\lambda}} = -2 \log_{10}\left(",
            r"\frac{\varepsilon/D}{3.7} + \frac{2.51}{Re\sqrt{\lambda}}",
            r"\right)"
        ).set_color(BLUE)

        # ---------------------------------------------------------
        # 2. Reescritura como f(lam) = 0
        # ---------------------------------------------------------
        eq2 = MathTex(
            r"f(\lambda) = \frac{1}{\sqrt{\lambda}} + 2\log_{10}\left(",
            r"\frac{\varepsilon/D}{3.7} + \frac{2.51}{Re\sqrt{\lambda}}",
            r"\right) = 0"
        ).set_color(GREEN)

        # ---------------------------------------------------------
        # 3. Definición de A
        # ---------------------------------------------------------
        eqA = MathTex(
            r"A = \frac{\varepsilon/D}{3.7} + \frac{2.51}{Re\sqrt{\lambda}}"
        ).set_color(YELLOW)

        # ---------------------------------------------------------
        # 4. Derivada f'(lambda)
        # ---------------------------------------------------------
        eq3 = MathTex(
            r"f'(\lambda) = -\frac{1}{2\lambda^{3/2}}",
            r"- \frac{2.51}{Re\,\lambda^{3/2}\,A\,\ln(10)}"
        ).set_color(GOLD)

        # ---------------------------------------------------------
        # 5. Fórmula de Newton–Raphson
        # ---------------------------------------------------------
        eqNR = MathTex(
            r"\lambda_{n+1} = \lambda_n - \frac{f(\lambda_n)}{f'(\lambda_n)}"
        ).set_color(ORANGE)

        # ---------------------------------------------------------
        # 6. Cierre
        # ---------------------------------------------------------
        final_text = Tex(
            r"""Este método permite determinar el coeficiente de fricción $\lambda$ \\
            para cualquier tubería rugosa o lisa en régimen turbulento.""",
            tex_environment="center"
        ).set_color(RED)

        creditos = Tex(
            r"""Para poder visualizar con todos sus argumentos estás \\
             operaciones en nuestras fuentes.""",
            tex_environment="center"
        ).set_color(PINK)


        # ---------------------------------------------------------
        # Posiciones
        # ---------------------------------------------------------
        texto20.move_to([0, 0, 0])
        texto21.move_to([0, 1, 0])
        eq1.move_to([0, -1, 0])
        eq2.move_to([0, -1, 0])
        eqA.move_to([0, -1, 0])
        eq3.move_to([0, -1, 0])
        eqNR.move_to([0, -1, 0])
        final_text.move_to([0, 0, 0])
        creditos.move_to([0, 0, 0])

        # ---------------------------------------------------------
        # Animaciones (exactamente con tu estructura de transforms)
        # ---------------------------------------------------------
        self.play(Write(texto20))
        self.wait(2)
        self.play(ReplacementTransform(texto20, texto21))
        self.wait(3)

        self.play(Write(eq1))
        self.wait(4)

        self.play(ReplacementTransform(eq1, eq2))
        self.wait(4)

        self.play(ReplacementTransform(eq2, eqA))
        self.wait(4)

        self.play(ReplacementTransform(eqA, eq3))
        self.wait(4)

        self.play(ReplacementTransform(eq3, eqNR))
        self.wait(4)

        self.play(FadeOut(texto21))
        self.play(ReplacementTransform(eqNR, final_text))
        self.wait(4)
        self.play(ReplacementTransform(final_text, creditos))
        self.wait(4)
        self.play(FadeOut(creditos), run_time=2)    

class graf(Scene):
    def construct(self):
        niuton = Tex(
            r"""E igualmente vamos a visualizar un pequeño ejemplo de \\
            el método de Newton-Raphson.""",
            tex_environment="center"
        ).set_color(RED)

        ejem = Tex(
            r"""Vamos a trabajar con la ecuación \\
             $x^{3} - 2x - 5 = 0$""",
            tex_environment="center"
        ).set_color(ORANGE)

        niuton.move_to([0, 0, 0])
        ejem.move_to([0, 0, 0])

        self.play(Write(niuton), run_time=2)
        self.wait(4)
        self.play(ReplacementTransform(niuton, ejem))
        self.wait(4)
        self.play(FadeOut(ejem))
        self.wait(1)


        funsion = Tex(
            r"""Primero veamos gráficamente esta función \\
             y donde podría tener tu raíz.""",
            tex_environment="center"
        ).set_color(GOLD)

        # Crear ejes coordenados
        ejes = Axes(
            x_range=[-2, 3, 1],
            y_range=[-10, 10, 2],
            x_length=7,
            y_length=5,
            axis_config={"color": WHITE, "stroke_width": 2},
            tips=True,
            x_axis_config={
                "numbers_to_include": [-2, -1, 0, 1, 2, 3],
            },
            y_axis_config={
                "numbers_to_include": [-10, -5, 0, 5, 10],
            }
        )
        ejes.shift(DOWN * 0.5)
        
        # Etiquetas de los ejes
        etiqueta_x = ejes.get_x_axis_label("x")
        etiqueta_y = ejes.get_y_axis_label("y")
        
        # Definir la función
        def funcion(x):
            return x**3 - 2*x - 5
        
        # Crear la gráfica
        grafica = ejes.plot(
            funcion, 
            color=PINK, 
            stroke_width=4,
            x_range=[-2, 3],
            use_smoothing=True
        )
        
        # Nombre de la función
        nombre_grafica = MathTex("f(x) = x^3 - 2x - 5", font_size=30, color=PINK)
        nombre_grafica.move_to([1.3, 1, 0])
        funsion.move_to([-3, 3, 0])
        funsion.scale(0.7)
        
        # ANIMACIONES
        self.play(Write(funsion), run_time=2)
        self.play(Create(ejes))
        self.play(Write(etiqueta_x), Write(etiqueta_y))
        self.wait(2)
        
        self.play(Create(grafica), run_time=3)
        self.play(Write(nombre_grafica))
        self.wait(4)
        
        # Encerrar la raíz (sin mostrar el valor numérico)
        raiz_aproximada = 2.0946
        
        rais = Tex(
            r"""Podemos determinar gráficamente que la raíz está \\
             entre 2 y 3, entonces ya sabemos a que valor tiende \\
             la raíz y que al parecer no es racional ($f(x) = 0 \not\in \mathbb{Q}).$""",
            tex_environment="center"
        ).set_color(YELLOW).scale(0.5).move_to([-3, 3, 0])

        # Punto en la raíz
        punto_raiz = Dot(ejes.c2p(raiz_aproximada, 0), color=RED, radius=0.08)
        
        # Línea vertical hasta la curva
        linea_vertical = DashedLine(
            ejes.c2p(raiz_aproximada, 0),
            ejes.c2p(raiz_aproximada, funcion(raiz_aproximada)),
            color=RED,
            stroke_width=2
        )
        
        # Círculo destacando la raíz
        circulo_destacado = Circle(radius=0.2, color=GOLD, stroke_width=4)
        circulo_destacado.move_to(ejes.c2p(raiz_aproximada, 0))

        chamba = Tex(
            r"""Entonces con esto atajo visual ya sabemos \\
             por donde empezar...""",
            tex_environment="center"
        ).set_color(TEAL).scale(0.6).move_to([3, -3, 0])
        
        # Animación para encerrar la raíz
        self.play(Create(punto_raiz))
        self.play(Create(linea_vertical))
        self.play(Create(circulo_destacado))
        self.play(ReplacementTransform(funsion, rais), run_time=2)
        self.play(Write(chamba), run_time=2)
        self.wait(5)
        self.play(FadeOut(ejes, etiqueta_x, etiqueta_y, grafica, nombre_grafica, punto_raiz, linea_vertical, circulo_destacado, rais, chamba), run_time=2)

class rapson(Scene):
    def construct(self):
        shamba1 = Tex(
            r"""Disclaimer: \\
             Sabemos que nos brincamos varios pasos, \\
             pero el tiempo apremia.""",
            tex_environment="center"
        ).set_color(RED).move_to([0, 0, 0]).scale(1.5)

        shamba2 = Tex(
            r"""Primero, vamos a determinar la derivada de $f(x)$,""",
            tex_environment="center"
        ).set_color(GREEN).move_to([0, 0.5, 0])

        paso1 = MathTex(
            r"\text{Si } f(x) = x^{3} - 2x - 5 \text{ entonces } f'(x) = 3x^{2} - 2"
        ).set_color(BLUE).move_to([0, -0.5, 0])

        shamba3 = Tex(
            r"""Y sabiendo qué es y como se compone el método \\
             ($x_{n + 1} = x_{n} - \frac{f(x_{n})}{f'(x_{n})}$) vamos a \\
             definir nuestros parametros""",
            tex_environment="center"
        ).set_color(PURPLE).move_to([0, 0.5, 0])

        paso2 = MathTex(
            r"\text{Nuestro } x_{1} = 2 \text{ y con Tolerancia de } 10^{-4}"
        ).set_color(PINK).move_to([0, -1, 0])

        shamba4 = Tex(
            r"""Empezamos a evaluar en la fórmula,""",
            tex_environment="center"
        ).set_color(RED).move_to([0, 0, 0]).scale(1.5)

        hint1 = Tex(
            r"""Veamos que $f(x_{1}) = 2^{3} - 2(2) - 5 = -1$ \\
             y $f'(x_{1}) = 3(2)^{2} - 2 = 10$ entonces,""",
            tex_environment="center"
        ).set_color(ORANGE).move_to([0, 1, 0])

        paso3 = MathTex(
            r"x_{2} = 2 - \frac{-1}{10} = 2 + 0.1 = 2.1"
        ).set_color(GOLD).move_to([0, -0.5, 0])

        hint2 = Tex(
            r"""Ahora tenemos que $f(x_{2}) = 2.1^{3} - 2(2.1) - 5 = 0.061$ \\
             y $f'(x_{2}) = 3(2)^{2} - 2 = 11.23$ entonces,""",
            tex_environment="center"
        ).set_color(YELLOW).move_to([0, 1, 0])

        paso4 = MathTex(
            r"x_{3} = 2.1 - \frac{0.061}{11.23} = 2.1 - 0.00543= 2.0945"
        ).set_color(TEAL).move_to([0, -0.5, 0])


        hint3 = Tex(
            r"""Ahora tenemos que $f(x_{3}) = 2.0945^{3} - 2(2.0945) - 5 = -0.0005$ \\
             y $f'(x_{3}) = 3(2)^{3.0945} - 2 = 11.1607$ entonces,""",
            tex_environment="center"
        ).set_color(GREEN).move_to([0, 1, 0])

        paso5 = MathTex(
            r"x_{4} = 2.0945 - \frac{-0.0005}{11.1607} = 2.0945 + 0.00004= 2.09454"
        ).set_color(BLUE).move_to([0, -0.5, 0])

        hint4 = Tex(
            r"""Podemos hacer más iteraciones, pero llegaríamos a lo mismo \\
             y como nuestra $Tolerancia$ era de $10^{-4}$, podemos decir \\
             la raíz de nuestro polinomio redondeada a $2.09454$. \\
             (hasta creo que nos pasamos)""",
            tex_environment="center"
        ).set_color(PURPLE).move_to([0, 0, 0])

        self.play(Write(shamba1), run_time=2)
        self.wait(5)
        self.play(ReplacementTransform(shamba1, shamba2))
        self.play(Write(paso1))
        self.wait(5)
        self.play(ReplacementTransform(shamba2, shamba3))
        self.play(ReplacementTransform(paso1, paso2))
        self.wait(5)
        self.play(ReplacementTransform(shamba3, shamba4))
        self.play(FadeOut(paso2))
        self.wait(5)
        self.play(ReplacementTransform(shamba4, hint1))
        self.play(Write(paso3), run_time=2)
        self.wait(5)
        self.play(ReplacementTransform(hint1, hint2))
        self.play(ReplacementTransform(paso3, paso4))
        self.wait(5)
        self.play(ReplacementTransform(hint2, hint3))
        self.play(ReplacementTransform(paso4, paso5))
        self.wait(5)
        self.play(FadeOut(paso5))
        self.play(ReplacementTransform(hint3, hint4))
        self.wait(5)
        self.play(FadeOut(hint4), run_time=2)

                # Crear ejes coordenados
        ejes = Axes(
            x_range=[-2, 3, 1],
            y_range=[-10, 10, 2],
            x_length=7,
            y_length=5,
            axis_config={"color": WHITE, "stroke_width": 2},
            tips=True,
            x_axis_config={
                "numbers_to_include": [-2, -1, 0, 1, 2, 3],
            },
            y_axis_config={
                "numbers_to_include": [-10, -5, 0, 5, 10],
            }
        )
        ejes.shift(DOWN * 0.5)
        
        # Etiquetas de los ejes
        etiqueta_x = ejes.get_x_axis_label("x")
        etiqueta_y = ejes.get_y_axis_label("y")
        
        # Definir la función
        def funcion(x):
            return x**3 - 2*x - 5
        
        # Crear la gráfica
        grafica = ejes.plot(
            funcion, 
            color=PINK, 
            stroke_width=4,
            x_range=[-2, 3],
            use_smoothing=True
        )
        
        # Nombre de la función
        nombre_grafica = MathTex("f(x) = x^3 - 2x - 5", font_size=30, color=PINK)
        nombre_grafica.move_to([1.3, 1, 0])
        
        # ANIMACIONES
        self.play(Create(ejes))
        self.play(Write(etiqueta_x), Write(etiqueta_y))
        self.wait(2)
        
        self.play(Create(grafica), run_time=3)
        self.play(Write(nombre_grafica))
        self.wait(4)
        
        # Raíz numérica a 4 decimales
        raiz_aproximada = 2.09454
        
        # Etiqueta con el valor numérico de la raíz
        etiqueta_raiz_numerica = MathTex(f"x \\approx {raiz_aproximada:.4f}", font_size=20, color=RED)
        etiqueta_raiz_numerica.move_to([1.9, 0.1, 0])

        finale = Tex(
            r"""Finalmente, podríamos decir que ya sabemos \\
             (aunque sea superficialmente) qué es el método de Newton \\ 
             y como nos puede ayudar aquí; además de un pequeño ejemplo; \\
             así que solo nos queda agardecer por su atención y su tiempo.""",
            tex_environment="center"
        ).set_color(PINK).move_to([0, 0, 0])

        # Punto en la raíz
        punto_raiz = Dot(ejes.c2p(raiz_aproximada, 0), color=RED, radius=0.08)
        
        # Línea vertical hasta la curva
        linea_vertical = DashedLine(
            ejes.c2p(raiz_aproximada, 0),
            ejes.c2p(raiz_aproximada, funcion(raiz_aproximada)),
            color=RED,
            stroke_width=2
        )
        
        # Círculo destacando la raíz
        circulo_destacado = Circle(radius=0.2, color=GOLD, stroke_width=4)
        circulo_destacado.move_to(ejes.c2p(raiz_aproximada, 0))

        
        # Animación para encerrar la raíz
        self.play(Create(punto_raiz))
        self.play(Create(linea_vertical))
        self.play(Create(circulo_destacado))
        self.play(Write(etiqueta_raiz_numerica))
        self.wait(4)
        self.play(FadeOut(ejes, etiqueta_x, etiqueta_y, grafica, nombre_grafica, punto_raiz, linea_vertical, circulo_destacado, etiqueta_raiz_numerica), run_time=2)
        self.play(FadeIn(finale), run_time=2)
        self.wait(4)
        self.play(FadeOut(finale), run_time=2)


"""
Colores de manera gradiente:

1. BLACK, 2. BLUE, 3. TEAL, 4. GREEN, 5. YELLOW, 6. GOLD, 7. ORANGE, 8. RED, 9. PURPLE, 10. PINK,
11. GRAY, 12. DARK_GRAY, 13. LIGHT_GRAY, 14. WHITE
"""
