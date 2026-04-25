import random
import itertools
from math import sin, cos

from manim import *

from quantumscene import *

def get_not_gate() -> VGroup:
    # Triangle (gate body)
    triangle = Polygon(
        LEFT*0.7 + DOWN * 0.5,
        LEFT*0.7 + UP * 0.5,
        RIGHT * 0.2,
    ).set_color(WHITE)

    # Inversion bubble
    bubble = Circle(radius=0.15).set_color(WHITE)
    bubble.move_to(triangle.get_right()+(bubble.get_right()-bubble.get_left())/2)
    # Input and output wires
    wire_in = Line(triangle.get_left()+LEFT, triangle.get_left())
    wire_out = Line(bubble.get_right(), bubble.get_right()+RIGHT)
    not_gate = VGroup(triangle, bubble, wire_in, wire_out)
    return not_gate

def get_single_qubit_gate(text) -> VGroup:
    box = Square(side_length=0.8)
    label = MathTex(text)
    label.move_to(box.get_center())
    wire1 = Line(box.get_left()+LEFT, box.get_left())
    wire2 = Line(box.get_right(), box.get_right()+RIGHT)
    return VGroup(box, label, wire1, wire2)

def get_xgate() -> VGroup:
    return get_single_qubit_gate("X")

def get_hadamard() -> VGroup:
    return get_single_qubit_gate("H")

def get_cnot() -> VGroup:
    dot1 = Circle(0.2, color=WHITE).set_fill(WHITE, opacity=1)
    dot2 = Circle(0.3, color=WHITE).next_to(dot1, DOWN, buff=1)
    wire1 = Line(dot1.get_left()+LEFT, dot1.get_right()+RIGHT)
    wire2 = Line(dot2.get_left()+LEFT, dot2.get_right()+RIGHT)
    wire3 = Line(dot2.get_bottom(), dot1.get_top())

    return VGroup(wire1, wire2, wire3, dot1, dot2)


class MeasurementSymbol(VGroup):
    def __init__(
        self,
        radius=0.5,
        needle_length=0.8,
        tick_count=5,
        **kwargs
    ):
        super().__init__(**kwargs)

        # Semi-circle (meter)
        arc = Arc(
            radius=radius,
            start_angle=0,
            angle=PI
        )

        # Tick marks
        ticks = VGroup()
        for angle in np.linspace(0, PI, tick_count):
            direction = np.array([np.cos(angle), np.sin(angle), 0])
            tick = Line(
                radius * 0.85 * direction,
                radius * direction,
            )
            ticks.add(tick)

        # Needle (store as attribute for animation later)
        self.needle = Arrow(
            start=ORIGIN,
            end=needle_length * UP,
            buff=0,
            stroke_width=4,
            color=ACCENT_YELLOW
        )

        dot = Dot()

        # Assemble
        self.add(dot, arc, ticks, self.needle)

        # Center nicely
        self.move_to(ORIGIN)

    def set_value(self, value):
        """
        Rotate needle based on value in [0,1]
        """
        angle = PI*(1-value)
        self.needle.set_angle(angle)
        return self

# ========================
# Example 1: Title Slide
# ========================

class TitleSlide(QuantumScene):
    def construct(self):
        title = Text("Quantencomputer", color=TEXT_COLOR).scale(1.7).shift(2*UP)

        subtitle1 = Text("Funktionsweise, Anwendungen", color=TEXT_COLOR).scale(1)
        subtitle2 = Text("und Grenzen", color=TEXT_COLOR).scale(1)

        event = Text(EVENT, color=ACCENT_PURPLE).scale(0.6)
        author = Text(AUTHOR, color=TEXT_COLOR).scale(0.6)

        subtitle1.next_to(title, DOWN)
        subtitle2.next_to(subtitle1, DOWN)

        event.next_to(subtitle2, 5*DOWN)
        author.next_to(event, 2*DOWN)

        title_orig = title.copy()
        title_highlighted = title.copy().scale(1.2)
        title_highlighted.set_color(PURE_YELLOW)
        title_orig = title.copy()

        author_orig = author.copy()
        author_highlighted = author.copy().scale(1.2)
        author_highlighted.set_color(PURE_YELLOW)

        self.play(FadeIn(title, shift=UP))
        self.wait(1)
        self.play(FadeIn(VGroup(subtitle1, subtitle2), shift=UP))
        self.play(FadeIn(event, shift=DOWN))
        self.wait(1)
        self.play(FadeIn(author, shift=UP))
        self.next_slide()

        self.play(Transform(title,title_highlighted))
        self.next_slide()
        self.play(AnimationGroup(Transform(title,title_orig), Transform(author, author_highlighted)))

        self.transition_next_slide()


class Overview(QuantumScene):
    def construct(self):
        self.format_slide("1")
        self.construct_title("Übersicht")

        texts = VGroup(
            Text("Klassische Computer"),
            Text("Qubit"),
            Text("Quantengatter"),
            Text("Quantenalgorithmen"),
            Text("Stand der Technik"),
        ).scale(0.7)

        texts.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        self.play(FadeIn(texts, shift=DOWN))

        self.next_slide()

        transformations = []
        for elem in texts:
            elem_orig = elem.copy()
            copy = elem.copy().scale(1.2)
            copy.set_color(PURE_YELLOW)

            transformations.extend((Transform(elem, copy), Transform(elem, elem_orig)))


        self.play(transformations[0])
        self.next_slide()

        t = tuple(itertools.batched(transformations[1:-1], 2))
        for k,(t1,t2) in enumerate(t):
            self.play(t1,t2)
            if k < (len(t)-1):
                self.next_slide()
            else:
                self.next_slide(auto_next=True)

        #self.play(transformations[-1])

        self.transition_next_slide(wait=True)


class HalfAdderSVGMobject(SVGMobject):
    def __init__(self):
        super().__init__("images/Half_Adder.svg", color=TEXT_COLOR)
        self.add(Text("A").scale(0.5).move_to(1.7*LEFT+0.8*UP))
        self.add(Text("B").scale(0.5).move_to(1.7*LEFT+0.35*UP))

        self.add(Text("S").scale(0.5).move_to(1.7*RIGHT+0.55*UP))
        self.add(Text("C").scale(0.5).move_to(1.7*RIGHT-0.6*UP))

    def set_state(self, color_inputA, color_inputB, color_outputA, color_outputB):
        self[1] .set_color(color_inputA) # input A
        self[5] .set_color(color_inputA) # input A
        self[9] .set_color(color_inputA) # input A
        self[11].set_color(color_inputA) # input A

        self[2] .set_color(color_inputB) # input B
        self[6] .set_color(color_inputB) # input B
        self[10].set_color(color_inputB) # input B
        self[12].set_color(color_inputB) # input B

        self[4] .set_color(color_outputA) # output A
        self[13].set_color(color_outputA) # output A

        self[0] .set_color(color_outputB) # output B
        self[14].set_color(color_outputB) # output B

    def copy_state(self, color_inputA, color_inputB, color_outputA, color_outputB):
        copy = self.copy()
        copy.set_state(color_inputA, color_inputB, color_outputA, color_outputB)
        return copy

class ClassicalComputing(QuantumScene):
    def construct(self):
        self.format_slide("2")

        self.construct_title("Klassischer Computer")

        text0_big = Text("Was braucht man, um einen Computer zu bauen?", color=ACCENT_CYAN)#.scale(0.7)#.to_edge(UP).shift(1.5*DOWN)
        text0 = text0_big.copy().scale(0.8).shift(2*UP+LEFT)

        or_gate = VGroup(
            or_text := Text("OR-Gatter"),
            svg_or := SVGMobject("images/or.svg", color=WHITE).scale(0.8).next_to(or_text, 1.7*DOWN),
            or_A := Text("A").next_to(svg_or, LEFT).shift(0.5*UP+0.1*RIGHT),
            or_B := Text("B").next_to(or_A, 2*DOWN),
            or_Q := Text("C").next_to(svg_or, 0.9*RIGHT),
        ).scale(0.5)

        nand_gate = VGroup(
            nand_text := Text("NAND-Gatter"),
            svg_nand := SVGMobject("images/nand.svg", color=WHITE).scale(0.8).next_to(nand_text, 1.7*DOWN),
            nand_A := Text("A").next_to(svg_nand, LEFT).shift(0.5*UP+0.1*RIGHT),
            nand_B := Text("B").next_to(nand_A, 2*DOWN),
            nand_Q := Text("C").next_to(svg_nand, 0.9*RIGHT),
        ).scale(0.5).next_to(or_gate)

        texts = VGroup(
            Text("1. Darstellung von Bits"),
            Text("2. Logikgatter"),
            Text("3. Taktsignal")
        ).scale(0.6)

        texts.arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(text0, 2*DOWN).shift(3*LEFT)

        self.play(FadeIn(text0_big, shift=UP))
        self.next_slide()
        self.play(Transform(text0_big, text0))
        self.play(FadeIn(texts, shift=UP))
        self.next_slide()

        orig0 = texts[0].copy()
        copy0 = texts[0].copy().scale(1.2)
        copy0.set_color(PURE_YELLOW)
        self.play(Transform(texts[0], copy0))

        texts_bits = VGroup(
            Text("Zwei unterscheidbare Zustände"),
            Text(r"  • Spannung (ICs)"),
            Text(r"  • Magnetisierung (HDDs)"),
            Text(r"  • Ladung (DRAMs)"),
            Text(r"  • …"),
        ).scale(0.5)
        texts_bits.arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(texts, RIGHT, aligned_edge=UP).shift(RIGHT)

        self.play(FadeIn(texts_bits, shift=UP))
        self.next_slide()

        orig1 = texts[1].copy()
        copy1 = texts[1].copy().scale(1.2)
        copy1.set_color(PURE_YELLOW)
        self.play(FadeOut(texts_bits, shift=DOWN))
        self.play(Transform(texts[0], orig0), Transform(texts[1], copy1))
        #self.play(AnimationGroup(Transform(text0_big, text0), FadeIn(texts, shift=UP), lag_ratio=0.2))

        nand_gate.next_to(texts, RIGHT, aligned_edge=UP).shift(RIGHT)
        or_gate.next_to(nand_gate, RIGHT, aligned_edge=UP).shift(RIGHT)

        table_nand = Table(
            [
                [Text("0", color=PURE_RED), Text("1", color=PURE_GREEN)],
                [Text("1", color=PURE_GREEN), Text("1", color=PURE_GREEN)],
                [Text("0", color=PURE_RED), Text("1", color=PURE_GREEN)],
                [Text("1", color=PURE_GREEN), Text("0", color=PURE_RED)],
            ],
            row_labels=[Text("0", color=PURE_RED), Text("0", color=PURE_RED), Text("1", color=PURE_GREEN), Text("1", color=PURE_GREEN)],
            col_labels=[Text("B"), Text("C")],
            top_left_entry = Text("A"),
            element_to_mobject=lambda x: x
        ).scale(0.45).next_to(nand_gate, 2*DOWN)

        table_or = Table(
            [
                [Text("0", color=PURE_RED), Text("0", color=PURE_RED)],
                [Text("1", color=PURE_GREEN), Text("1", color=PURE_GREEN)],
                [Text("0", color=PURE_RED), Text("1", color=PURE_GREEN)],
                [Text("1", color=PURE_GREEN), Text("1", color=PURE_GREEN)],
            ],
            row_labels=[Text("0", color=PURE_RED), Text("0", color=PURE_RED), Text("1", color=PURE_GREEN), Text("1", color=PURE_GREEN)],
            col_labels=[Text("B"), Text("C")],
            top_left_entry = Text("A"),
            element_to_mobject=lambda x: x
        ).scale(0.45).next_to(or_gate, 2*DOWN)

        self.play(FadeIn(nand_gate, shift=UP))
        self.next_slide()
        self.play(FadeIn(table_nand, shift=UP))
        self.next_slide()
        self.play(FadeIn(or_gate, shift=UP))
        self.next_slide()
        self.play(FadeIn(table_or, shift=UP))
        self.next_slide()
        self.play(FadeOut(nand_gate, shift=DOWN), FadeOut(table_nand, shift=DOWN), FadeOut(or_gate, shift=DOWN), FadeOut(table_or, shift=DOWN))


        false = PURE_RED
        true = PURE_GREEN

        adder0 = HalfAdderSVGMobject()

        table = Table(
            [
                [Text("0", color=BACKGROUND_COLOR), Text("0", color=BACKGROUND_COLOR), Text("0", color=BACKGROUND_COLOR)],
                [Text("1", color=BACKGROUND_COLOR), Text("1", color=BACKGROUND_COLOR), Text("0", color=BACKGROUND_COLOR)],
                [Text("0", color=BACKGROUND_COLOR), Text("1", color=BACKGROUND_COLOR), Text("0", color=BACKGROUND_COLOR)],
                [Text("1", color=BACKGROUND_COLOR), Text("0", color=BACKGROUND_COLOR), Text("1", color=BACKGROUND_COLOR)],
            ],
            row_labels=[Text("0", color=BACKGROUND_COLOR), Text("0", color=BACKGROUND_COLOR), Text("1", color=BACKGROUND_COLOR), Text("1", color=BACKGROUND_COLOR)],
            col_labels=[Text("B"), Text("S"), Text("C")],
            top_left_entry = Text("A"),
            element_to_mobject=lambda x: x
        )

        table.scale(0.6)

        group = VGroup(table, adder0)
        group.arrange(LEFT, aligned_edge=ORIGIN, buff=0.5).shift(1.75*RIGHT+0.5*DOWN)

        self.play(FadeIn(adder0, shift=UP))
        self.next_slide()
        self.play(FadeIn(table, shift=UP))
        #self.play(FadeIn(adder0), FadeIn(table))

        adders = [
            adder0.copy_state(false, false, false, false),
            adder0.copy_state(false, true,  true, false),
            adder0.copy_state(true,  false, true, false),
            adder0.copy_state(true,  true,  false, true),
        ]

        adder_last = adder0
        for j in range(1,5):
            adder = adders[j-1]
            self.play(Transform(adder_last, adder))
            last = adder

            elems = [table.get_columns()[k][j] for k in range(4)]
            self.play(
                AnimationGroup(
                    e.animate.set_color(true if e.text == "1" else false) for e in (elems[0], elems[1])
                )
            )
            self.play(
                AnimationGroup(
                    e.animate.set_color(true if e.text == "1" else false) for e in (elems[2], elems[3])
                )
            )
            self.next_slide()


        self.next_slide()
        sumtext = Text("A + B = S + C").next_to(group, 2*DOWN)
        self.play(FadeIn(sumtext), shift=UP)
        self.next_slide()
        self.play(FadeOut(sumtext, shift=DOWN), FadeOut(group, shift=DOWN))

        group2 = VGroup(
            Text("1. Logikgater (AND, OR, NOT, XOR …)"),
            Text("2. Schaltnetz (Addierer, Multiplexer)"),
            Text("3. Speicher (Latches, Flip-Flops)"),
            Text("4. Register / RAM"),
            Text("5. Zustandsautomat"),
            Text("6. Datenpfad und Steuerwerk"),
            Text("7. Arithmetisch-logische Einheit"),
            Text("8. CPU"),
        ).scale(0.5)
        group2.arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(texts, RIGHT, aligned_edge=UP).shift(RIGHT)
        self.play(FadeIn(group2, shift=UP))

        computer = Text("→ Computer", color=ACCENT_PURPLE).scale(0.8).next_to(group2, DR).shift(LEFT + 0.7*UP)
        self.next_slide()
        self.play(FadeIn(computer, shift=UP))

        self.next_slide()

        self.play(FadeOut(computer, shift=DOWN), FadeOut(group2, shift=DOWN))

        orig2 = texts[2].copy()
        copy2 = texts[2].copy().scale(1.2)
        copy2.set_color(PURE_YELLOW)
        self.play(Transform(texts[1], orig1), Transform(texts[2], copy2))
        self.next_slide()

        self.play(Transform(texts[2], orig2))
        self.play(FadeOut(texts, shift=DOWN), FadeOut(text0_big, shift=DOWN))

        z1 = ImageMobject("images/z1.jpg").scale(0.7).shift(2*LEFT)
        cpu = ImageMobject("images/cpu.jpg").scale(0.17).next_to(z1, RIGHT, aligned_edge=ORIGIN)
        
        self.play(FadeIn(z1, shift=UP), FadeIn(cpu, shift=UP))
        self.transition_next_slide()


class QubitSuperposition(QuantumScene):
    def construct(self):
        self.format_slide("3")
        self.construct_title("Qubit")

        def get_formula(alpha, beta, color_superposition, color_alpha, color_beta):
                formula = MathTex(
                    r"\lvert \Psi \rangle", # 0 
                    "=",                    # 1
                    rf"{alpha}",            # 2
                    r"\lvert 0 \rangle",    # 3
                    r"+",                   # 4
                    rf"{beta}",             # 5
                    r"\lvert 1 \rangle",    # 6
                )
                formula[0].set_color(color_superposition)
                formula[2].set_color(color_alpha)   # alpha
                formula[3].set_color(color_alpha)   # |0⟩ term
                formula[5].set_color(color_beta)    # beta
                formula[6].set_color(color_beta)    # |1⟩ term
                formula.scale(1.5).align_on_border(UP).shift(1.5*DOWN)
                return formula

        tracker = ValueTracker(0)
        def f():
            alpha = tracker.get_value()
            beta = 1-alpha #sqrt(1-alpha**2)
            c1 = ManimColor.from_hsv((0, 1, alpha))
            c2 = ManimColor.from_hsv((0.66, 1, beta))
            c3 = ManimColor.from_hsv((0.66 * beta, 1., 1.))
            return get_formula(f"{alpha**2:.3f}", f"{1-alpha**2:.3f}", c3, c1, c2)

    
        formula0 = get_formula(r"\alpha", r"\beta", ACCENT_YELLOW, ACCENT_RED, ACCENT_BLUE)

        formula = always_redraw(f)

        self.play(FadeIn(formula0, shift=UP))
        self.next_slide()

        qubit_state = Text("Qubit-Zustand").scale(0.8).set_color(ACCENT_YELLOW)
        zero_state = Text("0-Zustand").scale(0.8).set_color(ACCENT_RED)
        weights = Text("Gewichte").scale(0.8)
        for j in range(4):
             weights[j].set_color(ACCENT_RED)
             weights[4+j].set_color(ACCENT_BLUE)
        one_state = Text("1-Zustand").scale(0.8).set_color(ACCENT_BLUE)

        group = VGroup(qubit_state, zero_state, weights, one_state).arrange(RIGHT, buff=0.4)

        arrow_zero_state = Arrow(
            zero_state.get_top(),   # start at right edge of text1
            formula0[3].get_bottom(),    # end at left edge of text2
            buff=0.2             # small spacing so it doesn't overlap
        ).set_color(ACCENT_RED)
        arrow_one_state = Arrow(
            one_state.get_top(),   # start at right edge of text1
            formula0[6].get_bottom(),    # end at left edge of text2
            buff=0.2             # small spacing so it doesn't overlap
        ).set_color(ACCENT_BLUE)
        arrow_weights1 = Arrow(
            weights.get_top(),   # start at right edge of text1
            formula0[2].get_bottom(),    # end at left edge of text2
            buff=0.2             # small spacing so it doesn't overlap
        ).set_color(ACCENT_RED)
        arrow_weights2 = Arrow(
            weights.get_top(),   # start at right edge of text1
            formula0[5].get_bottom(),    # end at left edge of text2
            buff=0.2             # small spacing so it doesn't overlap
        ).set_color(ACCENT_BLUE)
        arrow_qubit = Arrow(
            qubit_state.get_top(),   # start at right edge of text1
            formula0[0].get_bottom(),    # end at left edge of text2
            buff=0.2             # small spacing so it doesn't overlap
        ).set_color(ACCENT_YELLOW)


        self.play(FadeIn(one_state, shift=UP), FadeIn(arrow_zero_state, shift=UP), FadeIn(zero_state, shift=UP), FadeIn(arrow_one_state, shift=UP))
        self.next_slide()
        self.play(FadeIn(weights, shift=UP), FadeIn(arrow_weights1, shift=UP), FadeIn(arrow_weights2, shift=UP))
        self.next_slide()
        self.play(FadeIn(qubit_state, shift=UP), FadeIn(arrow_qubit, shift=UP))
        self.next_slide()
        self.play(
             FadeOut(qubit_state, shift=DOWN), FadeOut(arrow_qubit, shift=DOWN),
             FadeOut(weights, shift=DOWN), FadeOut(arrow_weights1, shift=DOWN), FadeOut(arrow_weights2, shift=DOWN),
             FadeOut(zero_state, shift=DOWN), FadeOut(arrow_zero_state, shift=DOWN),
             FadeOut(one_state, shift=DOWN), FadeOut(arrow_one_state, shift=DOWN),    
        )

        formula_0bit = get_formula(r"1", r"0", ACCENT_YELLOW, ACCENT_RED, ACCENT_BLUE)
        formula_1bit = get_formula(r"0", r"1", ACCENT_YELLOW, ACCENT_RED, ACCENT_BLUE)
        formula_01bit = get_formula(r"0.7071", r"0.7071", ACCENT_YELLOW, ACCENT_RED, ACCENT_BLUE)

        self.play(ReplacementTransform(formula0, formula_0bit))
        self.next_slide()
        self.play(ReplacementTransform(formula_0bit, formula_1bit))
        self.next_slide()
        self.play(ReplacementTransform(formula_1bit, formula_01bit))
        self.next_slide()
        self.play(ReplacementTransform(formula_01bit, formula))

        def colors():
            alpha = tracker.get_value()
            beta = 1-alpha #sqrt(1-alpha**2)

            c1 = ManimColor.from_hsv((0, 1, alpha))
            c2 = ManimColor.from_hsv((0.66, 1, beta))
            c3 = ManimColor.from_hsv((0.66 * beta, 1., 1.))

            return c1,c2,c3

        c1 = lambda: colors()[0]
        c2 = lambda: colors()[1]
        c3 = lambda: colors()[2]

        circle1 = Circle(color=c1(), fill_opacity=1)            
        circle2 = Circle(color=c2(), fill_opacity=1).shift(LEFT)
        un = Intersection(circle1, circle2, fill_color=c3(), fill_opacity=1)

        circle1.add_updater(lambda x: x.set_color(c1()))
        circle2.add_updater(lambda x: x.set_color(c2()))
        un.add_updater(lambda x: x.set_color(c3()))

        circles = VGroup(circle1, circle2, un).shift(DOWN).scale(1.5)
        self.play(FadeIn(circles, shift=UP))
        self.next_slide(loop=True)

        self.play(tracker.animate.set_value(1), rate_func=linear, run_time=10)
        self.wait(1)
        self.play(tracker.animate.set_value(0), rate_func=linear, run_time=10)
        self.wait(4)
        self.next_slide()

        tracker2 = ValueTracker(-1)
        
        def get_formula2():
             value = tracker2.get_value()
             if value < 0:
                  return get_formula(r"\alpha", r"\beta", ACCENT_YELLOW, ACCENT_RED, ACCENT_BLUE)
             else:
                  alpha = cos(value)
                  beta = sin(value)
                  return get_formula(f"{alpha:.3f}", f"{beta:.3f}", ACCENT_YELLOW, ACCENT_RED, ACCENT_BLUE)


        formula2 = always_redraw(get_formula2)
        self.play(FadeOut(circles, shift=DOWN), ReplacementTransform(formula, formula2))

        modulus = MathTex(r"|\alpha|^2", "+", r"|\beta|^2", "= 1").scale(1.2).next_to(formula2, direction=DOWN, buff=1)
        modulus[0].set_color(ACCENT_RED)
        modulus[2].set_color(ACCENT_BLUE)

        self.play(FadeIn(modulus, shift=UP))
        self.next_slide()
        self.play(FadeOut(modulus, shift=DOWN))

        radius = 1.5
        circle = Circle(color=ACCENT_PURPLE, fill_opacity=0).shift(1.2*DOWN).scale(radius)

        circle_ketp0 = MathTex(r"|0\rangle").scale(0.7).next_to(circle.get_right(), RIGHT)
        circle_ketm0 = MathTex(r"-|0\rangle").scale(0.7).next_to(circle.get_left(), LEFT, aligned_edge=RIGHT)
        circle_ketp1 = MathTex(r"|1\rangle").scale(0.7).next_to(circle.get_top(), UP)
        circle_ketm1 = MathTex(r"-|1\rangle").scale(0.7).next_to(circle.get_bottom(), DOWN, aligned_edge=UP)

        self.play(
            FadeIn(circle, shift=UP),
            FadeIn(circle_ketp0, shift=UP), FadeIn(circle_ketm0, shift=UP),
            FadeIn(circle_ketp1, shift=UP), FadeIn(circle_ketm1, shift=UP)
        )

        def get_arrow():
            value = tracker2.get_value()
            value = value if value >= 0 else 0
            return Arrow(
                circle.get_center(),   # start at right edge of text1
                circle.get_center()+radius*(cos(value)*RIGHT + sin(value)*UP),    # end at left edge of text2
                buff=0.0             # small spacing so it doesn't overlap
            ).set_color(ACCENT_YELLOW)

        arrow = always_redraw(get_arrow)
        self.play(FadeIn(arrow, shift=UP))

        self.next_slide(loop=True)
        tracker2.set_value(0)
        self.play(tracker2.animate.set_value(2*PI), rate_func=linear, run_time=12)

        self.transition_next_slide()


class QubitMeasurement(QuantumScene):
    def construct(self):
        self.format_slide("4")
        self.construct_title("Messung")

        def get_formula(alpha, beta, color_superposition, color_alpha, color_beta):
                formula = MathTex(
                    r"\lvert \Psi \rangle", # 0 
                    "=",                    # 1
                    rf"{alpha}",            # 2
                    r"\lvert 0 \rangle",    # 3
                    r"+",                   # 4
                    rf"{beta}",             # 5
                    r"\lvert 1 \rangle",    # 6
                )
                formula[0].set_color(color_superposition)
                formula[2].set_color(color_alpha)   # alpha
                formula[3].set_color(color_alpha)   # |0⟩ term
                formula[5].set_color(color_beta)    # beta
                formula[6].set_color(color_beta)    # |1⟩ term
                formula.scale(1.5).align_on_border(UP).shift(1.5*DOWN)
                return formula

        formula = get_formula(r"0.8", r"0.6", ACCENT_YELLOW, ACCENT_RED, ACCENT_BLUE)
        
        group1 = VGroup(
            arrow0 := Arrow(buff=4),
            p0 := MathTex(r"36\%").next_to(arrow0.get_top(), UP, buff=0)
        ).rotate(-45*DEGREES).set_color(ACCENT_BLUE).move_to(formula.get_left()+1.2*DOWN+RIGHT+0.4*RIGHT)

        group0 = VGroup(
            arrow1 := Arrow(buff=4),
            p1 := MathTex(r"64\%").next_to(arrow1.get_bottom(), DOWN, buff=0).rotate(180*DEGREES)
        ).rotate(-135*DEGREES).set_color(ACCENT_RED).move_to(formula.get_left()+1.2*DOWN+LEFT+0.4*RIGHT)

        text0 = VGroup(
             Text("Messung: 0", font_size=32),
             mathtex0 := MathTex(r"|\Psi\rangle", "=", r"|0\rangle")
        ).arrange(DOWN).next_to(arrow1.get_tip(), DOWN)
        mathtex0[0].set_color(ACCENT_YELLOW)
        mathtex0[2].set_color(ACCENT_RED)

        text1 = VGroup(
             Text("Messung: 1", font_size=32),
             mathtex1 := MathTex(r"|\Psi\rangle", "=", r"|1\rangle")
        ).arrange(DOWN).next_to(arrow0.get_tip(), DOWN)
        mathtex1[0].set_color(ACCENT_YELLOW)
        mathtex1[2].set_color(ACCENT_BLUE)

        
        #p12 = MathTex(r"p(", r"|1\rangle", r")=", r"36\%").scale(1.5).next_to(p0, DOWN)

        #self.add(formula, group0, group1, text0, text1)

        self.play(FadeIn(formula, shift=UP))
        self.next_slide()
        self.play(FadeIn(group0, shift=UP), FadeIn(text0, shift=UP))
        self.next_slide()
        self.play(FadeIn(group1, shift=UP), FadeIn(text1, shift=UP))
        self.next_slide()

        self.play(FadeOut(group0, shift=DOWN), FadeOut(text0, shift=DOWN), FadeOut(group1, shift=DOWN), FadeOut(text1, shift=DOWN))


        p0 = MathTex(r"p(", r"|0\rangle", r")=|", r"\alpha", r"|^2").scale(1.5).next_to(formula, DOWN, buff=1)
        p1 = MathTex(r"p(", r"|1\rangle", r")=|", r"\beta",  r"|^2").scale(1.5).next_to(p0, DOWN)

        for idx in (1,3):
            p0[idx].set_color(ACCENT_RED)
            p1[idx].set_color(ACCENT_BLUE)

            #p02[idx].set_color(ACCENT_RED)
            #p12[idx].set_color(ACCENT_BLUE)

        measurement = MeasurementSymbol().scale(1.5).shift(2*LEFT+DOWN)
        measurement.set_value(0.7)
        self.play(FadeIn(measurement, shift=UP))


        zero = Text("0").move_to(measurement.get_center())
        one = Text("1").move_to(measurement.get_center())

        zero_fixed = Text("0").shift(2*RIGHT)
        num0 = DecimalNumber(0, num_decimal_places=1, unit=r"\%").scale(1.5).next_to(zero_fixed, RIGHT, buff=1).set_color(ACCENT_RED)
        one_fixed = Text("1").next_to(zero_fixed, DOWN, buff=1)
        num1 = DecimalNumber(0, num_decimal_places=1, unit=r"\%").scale(1.5).next_to(one_fixed, RIGHT, buff=1).set_color(ACCENT_BLUE)

        self.play(FadeIn(zero_fixed, shift=UP), FadeIn(one_fixed, shift=UP), FadeIn(num0, shift=UP), FadeIn(num1, shift=UP))
        #self.wait(1)

        
        random.seed(2026_05_02)
        zeros = 0
        for j in range(100):
            total = j+1

            if random.random() < 0.64:
                zeros += 1
                copy = zero.copy()
                end_pos = zero_fixed.get_center()
            else:
                copy = one.copy()
                end_pos = one_fixed.get_center()
            self.play(Wiggle(measurement), run_time=0.6)
            self.play(
                AnimationGroup(
                    FadeIn(copy),
                    copy.animate.move_to(end_pos)
                ),
                run_time=0.5
            )

            num0.set_value(zeros/total*100)
            num1.set_value((total-zeros)/total*100)
            self.remove(copy)

        self.transition_next_slide()


class QubitBloch(QuantumScene3D):
    def construct(self):
        # Set camera angle
        self.set_camera_orientation(phi=70 * DEGREES, theta=45 * DEGREES)

        self.construct_title("Bloch-Kugel")
        self.format_slide("5")

        # Create sphere
        sphere = Surface(
            lambda u, v: np.array([
                np.cos(u) * np.sin(v),
                np.sin(u) * np.sin(v),
                np.cos(v)
            ]),
            u_range=[0, 2 * PI],
            v_range=[0, PI],
            resolution=(32, 16),
            fill_opacity=0.2,
        ).scale(1.5)

        # Axes
        #axes = ThreeDAxes(z_length=6, y_length=6, x_length=6)
        axes = ThreeDAxes(z_length=4.5)


        # Tracker for angles
        #theta_tracker = ValueTracker(0.1)
        #phi_tracker = ValueTracker(0.1)
        time_tracker = ValueTracker(0.)

        def get_theta_phi() -> tuple[float,float]:
            t = time_tracker.get_value()
            theta = t*2*PI if t < 0.5 else 2*PI*(1-t)
            return theta, t*20
    
        get_theta = lambda: get_theta_phi()[0]
        get_phi = lambda: get_theta_phi()[1]

        p0 = lambda: cos(get_theta()/2)**2
        p1 = lambda: sin(get_theta()/2)**2

        # State vector (Bloch vector)
        def get_vector():
            theta = get_theta()
            phi = get_phi()

            x = np.sin(theta) * np.cos(phi)
            y = np.sin(theta) * np.sin(phi)
            z = np.cos(theta)

            return Arrow3D(
                start=[0, 0, 0],
                end=[x*1.5, y*1.5, z*1.5],
                color=YELLOW
            )#.scale(1.5)

        vector = always_redraw(get_vector)

        # Labels
        ket0 = MathTex(r"|0\rangle").move_to([0.5, 0, 2])
        ket1 = MathTex(r"|1\rangle").move_to([0.5, 0, -2])
        self.add_fixed_orientation_mobjects(ket0, ket1)


        # Add objects
        #self.play(FadeIn(axes, shift=UP), FadeIn(sphere, shift=UP), FadeIn(ket0, shift=UP), FadeIn(ket1, shift=UP), FadeIn(vector, shift=UP))
        self.play(FadeIn(sphere, shift=UP), FadeIn(ket0, shift=UP), FadeIn(ket1, shift=UP), FadeIn(vector, shift=UP))

        # Ambient camera rotation
        self.begin_ambient_camera_rotation(rate=0.2)

        def get_formula():
            theta, phi = get_theta_phi()

            alpha = np.cos(theta/2)
            beta = np.exp(1j*phi)*sin(theta/2)
            beta_r = np.real(beta)
            beta_i = np.imag(beta)

            tex = MathTex(
                r"\lvert \Psi \rangle",           # 0 
                "=",                              # 1
                rf"{alpha:.3f}",                  # 2
                r"\lvert 0 \rangle",              # 3
                r"+",                             # 4
                rf"({beta_r:+.3f}{beta_i:+.3f}i)", # 5
                r"\lvert 1 \rangle",              # 6
            )
            tex[0].set_color(ACCENT_YELLOW)
            tex[2].set_color(ACCENT_RED)   # alpha
            tex[3].set_color(ACCENT_RED)   # |0⟩ term
            tex[5].set_color(ACCENT_BLUE)  # beta
            tex[6].set_color(ACCENT_BLUE)  # |1⟩ term

            tex.shift(3*RIGHT+2.7*DOWN)

            return tex


        formula = always_redraw(get_formula)
        self.add_fixed_in_frame_mobjects(formula)

        p0_value = DecimalNumber(0, num_decimal_places=2, unit=r"\%").set_color(ACCENT_RED)
        p1_value = DecimalNumber(0, num_decimal_places=2, unit=r"\%").set_color(ACCENT_BLUE)

        def update_p0(mob, dt):
            mob.set_value(p0() * 100)
            self.add_fixed_in_frame_mobjects(mob)

        def update_p1(mob, dt):
            mob.set_value(p1() * 100)
            self.add_fixed_in_frame_mobjects(mob)


        self.add_fixed_in_frame_mobjects(p0_value, p1_value)

        p0_value.add_updater(update_p0)
        p1_value.add_updater(update_p1)

        p0_value.to_corner(UL).shift(DOWN * 2)
        p1_value.next_to(p0_value, DOWN, aligned_edge=LEFT)

        self.add(p0_value, p1_value)

        self.play(FadeIn(formula, shift=UP))
        self.next_slide(loop=True)

        # Animate the qubit state
        self.play(
            time_tracker.animate.set_value(1),
            run_time=25,
            rate_func=linear
        )

        self.transition_next_slide()

class QubitEntanglement(QuantumScene):
    def construct(self):
        self.format_slide("6")
        self.construct_title("Verschränkung")

        formula1 = MathTex(
            r"\lvert \Psi \rangle",           # 0 
            "=",                              # 1

            r"\alpha\lvert",                  # 2
            r"0",                             # 3
            r"0",                             # 4

            r"\rangle +\beta\lvert",          # 5
            r"0",                             # 6
            r"1",                             # 7

            r"\rangle + \gamma\lvert",        # 8
            r"1",                             # 9
            r"0",                             # 10

            r"\rangle + \delta\lvert",        # 11
            r"1",                             # 12
            r"1",                             # 13
            r"\rangle"                        # 14
        )
        formula1.scale(1.3)
        formula1[0].set_color(ACCENT_YELLOW)
        for j in (3,6,9,12):
            formula1[j].set_color(ACCENT_RED)
            formula1[j+1].set_color(ACCENT_BLUE)
        

        qubit1 = Text("Qubit 1").scale(0.8).set_color(ACCENT_RED).next_to(formula1.get_top(), UP, buff=1.5).shift(.7*RIGHT)
        qubit2 = Text("Qubit 2").scale(0.8).set_color(ACCENT_BLUE).next_to(formula1.get_bottom(), DOWN, buff=1.5).shift(.7*RIGHT)

        arrows1 = []
        arrows2 = []
        for j in (3,6,9,12):
            arrow1 = Arrow(start=qubit1.get_bottom(), end=formula1[j].get_top()).set_color(ACCENT_RED)
            arrows1.append(arrow1)

            arrow2 = Arrow(start=qubit2.get_top(), end=formula1[j+1].get_bottom()).set_color(ACCENT_BLUE)
            arrows2.append(arrow2)


        self.play(FadeIn(formula1, shift=UP))
        self.next_slide()
        self.play(FadeIn(qubit1, shift=UP), *[FadeIn(e, shift=UP) for e in arrows1])
        self.next_slide()
        self.play(FadeIn(qubit2, shift=UP), *[FadeIn(e, shift=UP) for e in arrows2])
        self.next_slide()
        self.play(FadeOut(qubit1, shift=DOWN), FadeOut(qubit2, shift=DOWN), *[FadeOut(e, shift=DOWN) for e in arrows1], *[FadeOut(e, shift=DOWN) for e in arrows2])

        self.play(formula1.animate.shift(1.5*UP))
        
        formula2 = MathTex(r"\lvert\Psi\rangle", r"= \frac{1}{\sqrt 2}\Big(", r"\lvert", "0", "1", r"\rangle + \lvert", "1", "0", r"\rangle\Big)").move_to(formula1.get_center())
        formula2[0].set_color(ACCENT_YELLOW)
        for j in (3, 6):
            formula2[j].set_color(ACCENT_RED)
            formula2[j+1].set_color(ACCENT_BLUE)

        self.play(ReplacementTransform(formula1, formula2))

        def get_vector(start, length, text, angle, scale=0.6):
            flip = abs(angle) > PI/2
            rotate = PI if flip else 0
            arrange = UP if flip else DOWN
            group = VGroup(
                Text(text).rotate(rotate).scale(scale),
                Arrow(start, start+length*RIGHT),
            ).arrange(arrange, buff=0.05).rotate(angle, about_point=start).set_color(ACCENT_PURPLE)
            group.shift(start-group[1].get_start())
            return group

        v1 = get_vector(formula2.get_bottom(), 2.5, "50%", -40*DEGREES).shift(0.3*RIGHT)
        v2 = get_vector(formula2.get_bottom(), 2.5, "50%", -140*DEGREES).shift(0.3*LEFT)

        m1 = MathTex("0", r"\,\,", r"\lvert", "0", "1", r"\rangle").next_to(v1[1].get_end(), DOWN)
        m1[0].set_color(ACCENT_RED)
        m1[3].set_color(ACCENT_RED)
        m1[4].set_color(ACCENT_BLUE)
        m2 = MathTex("1", r"\,\,", r"\lvert", "1", "0", r"\rangle").next_to(v2[1].get_end(), DOWN)
        m2[0].set_color(ACCENT_RED)
        m2[3].set_color(ACCENT_RED)
        m2[4].set_color(ACCENT_BLUE)

        arrow3 = Arrow(start=m1.get_bottom(), end=m1.get_bottom()+1.5*DOWN).set_color(PURPLE)
        text3 = Text("100%").scale(0.6).next_to(arrow3, RIGHT).set_color(PURPLE)
        arrow4 = Arrow(start=m2.get_bottom(), end=m2.get_bottom()+1.5*DOWN).set_color(PURPLE)
        text4 = Text("100%").scale(0.6).next_to(arrow4, LEFT).set_color(PURPLE)

        final1 = MathTex("0", "1", r"\,\,", r"\lvert", "0", "1", r"\rangle").next_to(arrow3, DOWN)
        final1[0].set_color(ACCENT_RED)
        final1[1].set_color(ACCENT_BLUE)
        final1[4].set_color(ACCENT_RED)
        final1[5].set_color(ACCENT_BLUE)
        final2 = MathTex("1", "0", r"\,\,", r"\lvert", "1", "0", r"\rangle").next_to(arrow4, DOWN)
        final2[0].set_color(ACCENT_RED)
        final2[1].set_color(ACCENT_BLUE)
        final2[4].set_color(ACCENT_RED)
        final2[5].set_color(ACCENT_BLUE)


        self.next_slide()
        self.play(FadeIn(v2,shift=UP), FadeIn(m2, shift=UP))
        self.next_slide()
        self.play(FadeIn(arrow4,shift=UP), FadeIn(text4, shift=UP), FadeIn(final2, shift=UP))
        self.next_slide()

        self.play(FadeIn(v1,shift=UP), FadeIn(m1, shift=UP))
        self.next_slide()
        self.play(FadeIn(arrow3,shift=UP), FadeIn(text3, shift=UP), FadeIn(final1, shift=UP))
        self.next_slide()

        self.play(FadeOut(e, shift=DOWN) for e in (formula2, v2, m2, arrow4, text4, v1, m1, arrow3, text3, final1, final2))

        envelop1 = SVGMobject("images/envelop.svg").scale(0.6).shift(2*LEFT+1*UP)
        envelop2 = envelop1.copy().next_to(envelop1, RIGHT, buff=2)
        self.play(FadeIn(envelop1, shift=UP), FadeIn(envelop2, shift=UP))
        self.next_slide()
        
        zero = Text("0", color=ACCENT_RED).scale(1.5).next_to(envelop1, UP)
        one  = Text("1", color=ACCENT_BLUE).scale(1.5).next_to(envelop2, UP)
        #one = Text("1", color=ACCENT_BLUE).move_to(envelop2.center())
        self.play(FadeIn(zero), FadeIn(one))
        self.next_slide()

        self.play(zero.animate.move_to(envelop1.get_center()), one.animate.move_to(envelop2.get_center()))
        self.wait(0.5)
        self.play(FadeOut(zero), FadeOut(one))

        center = 0.5*(envelop1.get_center() + envelop2.get_center())
        self.play(envelop1.animate.move_to(center), envelop2.animate.move_to(center))
        self.wait(0.5)
        self.play(envelop1.animate.shift(2*LEFT), envelop2.animate.shift(2*RIGHT))

        self.next_slide()
        one2 = Text("1", color=ACCENT_BLUE).scale(1.5).next_to(envelop1.get_center(), ORIGIN)
        self.play(FadeIn(one2))
        self.next_slide()
        zero2 = Text("0", color=ACCENT_RED).scale(1.5).next_to(envelop2.get_center(), ORIGIN)
        self.play(FadeIn(zero2))
        self.next_slide()

        self.play(FadeOut(one2), FadeOut(zero2))
        self.play(FadeOut(envelop1, shift=DOWN), FadeOut(envelop2, shift=DOWN))

        texts = VGroup(
            Text("• Qubit 1 und Qubit 2 sind korreliert"),
            Text("• Messung von Qubit 1 bestimmt Wert von Qubit 2 instatan"),
            Text("• Vor der Messung haben die Qubit keine eindeutigen Werte"),
            Text("• Korrelation stärker als klassisch möglich"),
            Text("• Überlichtschnelle Kommunikation nicht möglich"),
        ).scale(0.7)

        texts.arrange(DOWN, aligned_edge=LEFT, buff=0.5)

        for j,text in enumerate(texts):
            if j:
                self.next_slide()
            self.play(FadeIn(text, shift=UP))

        self.transition_next_slide()

class QubitSummary(QuantumScene):
    def construct(self):
        self.format_slide("7")
        self.construct_title("Qubit - Zusammenfassung")

        texts = VGroup(
            Text("• 0, 1 oder Überlagerung beider Zustände"),
            Text("• prinzipiell mehr Information als klassisches Bit"),
            Text("• Messung zerstört Zustand und liefert eindeutiges Ergebnis (0 oder 1)"),
            Text("• Qubits können nicht kopiert werden"),
            Text("• Qubits können verschränkt sein → Korrelation"),
        ).scale(0.7)

        texts.arrange(DOWN, aligned_edge=LEFT, buff=0.5)

        for text in texts:
            self.next_slide()
            self.play(FadeIn(text, shift=UP))

        self.transition_next_slide(wait=True)

class Gates(QuantumScene):
    def construct(self):
        self.format_slide("8")
        self.construct_title("Quanten-Gatter")

        ket0 = MathTex(r"\lvert0\rangle")
        ket1 = MathTex(r"\lvert1\rangle")

        # Gate box
        xgate = get_xgate().scale(1.5).align_on_border(LEFT).shift(2*RIGHT+UP)

        ket_in  = ket0.copy()
        ket_out = ket1.copy()

        ket_in.next_to(xgate[0], LEFT,  aligned_edge=UP, buff=0.5).shift(0.3*UP).set_color(ACCENT_RED)
        ket_out.next_to(xgate[0], RIGHT, aligned_edge=UP, buff=0.5).shift(0.3*UP).set_color(ACCENT_BLUE)

        self.play(FadeIn(xgate, shift=UP))
        self.play(FadeIn(ket_in, shift=UP), FadeIn(ket_out, shift=UP))
        self.next_slide()

        ket_in2 = ket1.copy().move_to(ket_in).set_color(ACCENT_RED)
        ket_out2 = ket0.copy().move_to(ket_out).set_color(ACCENT_BLUE)
        self.play(ReplacementTransform(ket_in, ket_in2), ReplacementTransform(ket_out, ket_out2))
        self.next_slide()

        table = MathTable(
            [[r"\mathrm{Eingang}", r"\mathrm{Ausgang}"],
            [r"\lvert0\rangle", r"\lvert1\rangle"],
            [r"\lvert1\rangle", r"\lvert0\rangle"]],
        ).next_to(xgate, RIGHT, buff=1)
        table[0][2].set_color(ACCENT_RED)
        table[0][4].set_color(ACCENT_RED)
        table[0][3].set_color(ACCENT_BLUE)
        table[0][5].set_color(ACCENT_BLUE)
        table.scale(0.8)
        self.play(FadeIn(table, shift=UP))


        not_gate = get_not_gate().next_to(xgate, DOWN, buff=1)
        text_not = Text("Not-Gatter").scale(0.7).next_to(not_gate, DOWN)


        formula = MathTex(r"X\Big(\alpha\lvert 0\rangle+\beta\lvert 1\rangle\Big) = \beta\lvert 0\rangle+\alpha\lvert 1\rangle").next_to(table, DOWN, buff=1)
        self.next_slide()
        self.play(FadeIn(formula, shift=UP))
        self.next_slide()
        self.play(FadeIn(not_gate, shift=UP), FadeIn(text_not, shift=UP))
        self.next_slide()

        fadeout = [formula, not_gate, text_not, table, ket_in2, ket_out2]
        self.play(*[FadeOut(e, shift=DOWN) for e in fadeout])

        xgate2 = xgate.copy().scale(0.5).shift(1.5*UP+2.5*LEFT)
        self.play(ReplacementTransform(xgate, xgate2))

        hadamard = get_hadamard().scale(1.5).align_on_border(LEFT).shift(2*RIGHT)
        self.play(FadeIn(hadamard, shift=UP))
        ket_in  = ket0.copy().next_to(hadamard[0], LEFT,  aligned_edge=UP, buff=0.5).shift(0.3*UP).set_color(ACCENT_RED)
        ket_out = MathTex(r"\frac{1}{\sqrt{2}}\big(\lvert 0\rangle + \lvert 1\rangle\big)").next_to(hadamard[0], RIGHT, aligned_edge=UP, buff=0.2).shift(0.6*UP).set_color(ACCENT_BLUE).scale(0.8)

        self.play(FadeIn(ket_in, shift=UP), FadeIn(ket_out, shift=UP))
        self.next_slide()
        ket_in2  = ket1.copy().next_to(hadamard[0], LEFT,  aligned_edge=UP, buff=0.5).shift(0.3*UP).set_color(ACCENT_RED)
        ket_out2 = MathTex(r"\frac{1}{\sqrt{2}}\big(\lvert 0\rangle - \lvert 1\rangle\big)").next_to(hadamard[0], RIGHT, aligned_edge=UP, buff=0.2).shift(0.6*UP).set_color(ACCENT_BLUE).scale(0.8)

        self.play(ReplacementTransform(ket_in, ket_in2), ReplacementTransform(ket_out, ket_out2))
        table = MathTable(
            [[r"\mathrm{Eingang}", r"\mathrm{Ausgang}"],
            [r"\lvert0\rangle", r"\frac{1}{\sqrt{2}}\big(\lvert 0\rangle + \lvert 1\rangle\big)"],
            [r"\lvert1\rangle", r"\frac{1}{\sqrt{2}}\big(\lvert 0\rangle - \lvert 1\rangle\big)"]],
        ).next_to(hadamard, RIGHT, buff=1)
        table[0][2].set_color(ACCENT_RED)
        table[0][4].set_color(ACCENT_RED)
        table[0][3].set_color(ACCENT_BLUE).scale(0.8)
        table[0][5].set_color(ACCENT_BLUE).scale(0.8)
        table.scale(0.8)
        self.play(FadeIn(table, shift=UP))
        self.next_slide()

        fadeout = [table, ket_in2, ket_out2]
        self.play(*[FadeOut(e, shift=DOWN) for e in fadeout])

        hadamard2 = hadamard.copy().scale(0.5).next_to(xgate2, DOWN, buff=0.2)
        self.play(ReplacementTransform(hadamard, hadamard2))

        cnot = get_cnot().shift(2*LEFT)

        ket_in1_1  = ket0.copy().move_to(cnot.get_corner(LEFT+UP)).shift(0.4*LEFT).set_color(ACCENT_RED)
        ket_in2_1  = ket0.copy().move_to(cnot.get_corner(LEFT+DOWN)).shift(0.4*LEFT).set_color(ACCENT_RED)
        ket_out1_1 = ket0.copy().move_to(cnot.get_corner(RIGHT+UP)).shift(0.4*RIGHT).set_color(ACCENT_BLUE)
        ket_out2_1 = ket0.copy().move_to(cnot.get_corner(RIGHT+DOWN)).shift(0.4*RIGHT).set_color(ACCENT_BLUE)

        ket_in1_2  = ket0.copy().move_to(cnot.get_corner(LEFT+UP)).shift(0.4*LEFT).set_color(ACCENT_RED)
        ket_in2_2  = ket1.copy().move_to(cnot.get_corner(LEFT+DOWN)).shift(0.4*LEFT).set_color(ACCENT_RED)
        ket_out1_2 = ket0.copy().move_to(cnot.get_corner(RIGHT+UP)).shift(0.4*RIGHT).set_color(ACCENT_BLUE)
        ket_out2_2 = ket1.copy().move_to(cnot.get_corner(RIGHT+DOWN)).shift(0.4*RIGHT).set_color(ACCENT_BLUE)

        ket_in1_3  = ket1.copy().move_to(cnot.get_corner(LEFT+UP)).shift(0.4*LEFT).set_color(ACCENT_RED)
        ket_in2_3  = ket0.copy().move_to(cnot.get_corner(LEFT+DOWN)).shift(0.4*LEFT).set_color(ACCENT_RED)
        ket_out1_3 = ket1.copy().move_to(cnot.get_corner(RIGHT+UP)).shift(0.4*RIGHT).set_color(ACCENT_BLUE)
        ket_out2_3 = ket1.copy().move_to(cnot.get_corner(RIGHT+DOWN)).shift(0.4*RIGHT).set_color(ACCENT_BLUE)

        ket_in1_4  = ket0.copy().move_to(cnot.get_corner(LEFT+UP)).shift(0.4*LEFT).set_color(ACCENT_RED)
        ket_in2_4  = ket1.copy().move_to(cnot.get_corner(LEFT+DOWN)).shift(0.4*LEFT).set_color(ACCENT_RED)
        ket_out1_4 = ket1.copy().move_to(cnot.get_corner(RIGHT+UP)).shift(0.4*RIGHT).set_color(ACCENT_BLUE)
        ket_out2_4 = ket0.copy().move_to(cnot.get_corner(RIGHT+DOWN)).shift(0.4*RIGHT).set_color(ACCENT_BLUE)


        self.play(FadeIn(cnot, shift=UP))
        self.play(FadeIn(ket_in1_1, shift=UP), FadeIn(ket_in2_1, shift=UP), FadeIn(ket_out1_1, shift=UP), FadeIn(ket_out2_1, shift=UP))
        self.next_slide()
        self.play(ReplacementTransform(ket_in1_1, ket_in1_2), ReplacementTransform(ket_in2_1, ket_in2_2), ReplacementTransform(ket_out1_1, ket_out1_2), ReplacementTransform(ket_out2_1, ket_out2_2))
        self.next_slide()
        self.play(ReplacementTransform(ket_in1_2, ket_in1_3), ReplacementTransform(ket_in2_2, ket_in2_3), ReplacementTransform(ket_out1_2, ket_out1_3), ReplacementTransform(ket_out2_2, ket_out2_3))
        self.next_slide()
        self.play(ReplacementTransform(ket_in1_3, ket_in1_4), ReplacementTransform(ket_in2_3, ket_in2_4), ReplacementTransform(ket_out1_3, ket_out1_4), ReplacementTransform(ket_out2_3, ket_out2_4))
        self.next_slide()

        table = MathTable(
            [[r"\mathrm{Eingang}", r"\mathrm{Ausgang}"],
            [r"\lvert00\rangle", r"\lvert00\rangle"],
            [r"\lvert01\rangle", r"\lvert01\rangle"],
            [r"\lvert10\rangle", r"\lvert11\rangle"],
            [r"\lvert11\rangle", r"\lvert10\rangle"]],
        ).next_to(cnot, RIGHT, buff=1)
        table[0][2].set_color(ACCENT_RED)
        table[0][4].set_color(ACCENT_RED)
        table[0][6].set_color(ACCENT_RED)
        table[0][8].set_color(ACCENT_RED)
        table[0][3].set_color(ACCENT_BLUE)
        table[0][5].set_color(ACCENT_BLUE)
        table[0][7].set_color(ACCENT_BLUE)
        table[0][9].set_color(ACCENT_BLUE)
        table.scale(0.8)

        self.play(FadeIn(table, shift=UP))
        self.next_slide()
        self.play(*[FadeOut(e, shift=DOWN) for e in (table, ket_in1_4, ket_in2_4, ket_out1_4, ket_out2_4)])
        cnot2 = cnot.copy().scale(0.5).next_to(hadamard2, DOWN, buff=0.2)
        self.play(ReplacementTransform(cnot, cnot2))

        texts = VGroup(
            Text("Quanten-Gatter…").set_color(ACCENT_YELLOW),
            Text("• …operieren auf Qubits"),
            Text("• …entsprechen Rotationen"),
            Text("• …sind deterministisch, Messung nicht-deterministisch"),
            Text("• …sind reversibel"),
            Text("• …nutzen Überlagerung für Parallelisierung"),
            Text("• …können Verschränkung erzeugen und nutzen"),
        ).scale(0.55).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(cnot2, RIGHT, buff=1).shift(DOWN)

        for j,text in enumerate(texts):
            if j > 1:
                self.next_slide()
            self.play(FadeIn(text, shift=UP))

        self.transition_next_slide(wait=True)


class Algorithms(QuantumScene):
    def construct(self):
        self.format_slide("9")
        self.construct_title("Quantenalgorithmen")

        circuit = SVGMobject("images/grover_circuit.svg", color=WHITE, stroke_color=WHITE, fill_color=WHITE, stroke_width=0.5).scale_to_fit_width(11)
        self.play(FadeIn(circuit, shift=UP))
        self.next_slide()
        self.play(FadeOut(circuit, shift=DOWN))

        texts = VGroup(
            Text("• Quanten-Optimierungsalgorithmen"),
            Text("• QPE (Quantum Phase Estimation) → Eigenwerte eines unitären Operators"),
            Text("• VQE (Variational quantum eigensolver) → Grundzustand"),
            Text("• Harrow–Hassidim–Lloyd (HHL) Algorithmus → schnelle lineare Algebra"),
            Text("• Quantenfouriertransformation"),
            Text("• Grovers Algorithmus → schnelle Suche"),
            Text("• Shors Algorithmus → Primzahlzerlegung"),
        ).scale(0.55).arrange(DOWN, aligned_edge=LEFT, buff=0.4)

        buff = 0.2
        scale = 0.45
        accent_color = ACCENT_YELLOW

        for text in texts:
            self.play(FadeIn(text, shift=UP))
            self.next_slide()
        self.play(*[FadeOut(text, shift=DOWN) for text in texts])

        group1 = VGroup(
            Text("Chemie und Materialwissenschaften").set_color(accent_color),
            Text("• Medikamentenforschung"),
            Text("• Bessere Baterien"),
            Text("• Neue Materialien wie Supraleiter"),
        ).scale(scale).arrange(DOWN, aligned_edge=LEFT, buff=buff)

        group2 = VGroup(
            Text("Optimierungsprobleme").set_color(accent_color),
            Text("• Logistik"),
            Text("• Lieferketten"),
            Text("• Portfoliomanagement"),
        ).scale(scale).arrange(DOWN, aligned_edge=LEFT, buff=buff)

        group3 = VGroup(
            Text("Kryptographie & Verschlüsselung").set_color(accent_color),
            Text("• Brechen von bestehender Verschlüsselung"),
            Text("• Quantenschlüsselaustausch"),
        ).scale(scale).arrange(DOWN, aligned_edge=LEFT, buff=buff)

        group4 = VGroup(
            Text("Maschinelles Lernen & Datenanalyse").set_color(accent_color),
            Text("• schnelle Lineare Algebra"),
        ).scale(scale).arrange(DOWN, aligned_edge=LEFT, buff=buff)

        group5 = VGroup(
            Text("Simulation physikalischer Systeme").set_color(accent_color),
            Text("• Hochenergiephysik"),
            Text("• Klimamodellierung"),
            Text("• Fusionsforschung"),
        ).scale(scale).arrange(DOWN, aligned_edge=LEFT, buff=buff)

        group6 = VGroup(
            Text("Medizin & Biologie").set_color(accent_color),
            Text("• Proteinfaltung"),
            Text("• Vorhersage von Molekularbindungen"),
        ).scale(scale).arrange(DOWN, aligned_edge=LEFT, buff=buff)

        group7 = VGroup(
            Text("Suchprobleme").set_color(accent_color),
            Text("• schnellere Brute-Force-Suche"),
        ).scale(scale).arrange(DOWN, aligned_edge=LEFT, buff=buff)


        # HHL https://en.wikipedia.org/wiki/HHL_algorithm
        # given Ax=b, estimate xTMx for Hermition matrix M

        #self.add(texts)

        group1.shift(4*LEFT).shift(1.7*UP)
        group2.next_to(group1, DOWN, aligned_edge=LEFT, buff=0.45)
        group3.next_to(group2, DOWN, aligned_edge=LEFT, buff=0.45)
        
        group4.next_to(group1, RIGHT, aligned_edge=UP, buff=2)
        group5.next_to(group4, DOWN, aligned_edge=LEFT, buff=0.45)
        group6.next_to(group5, DOWN, aligned_edge=LEFT, buff=0.45)
        group7.next_to(group6, DOWN, aligned_edge=LEFT, buff=0.45)

        groups = (group1, group2, group3, group4, group5, group6, group7)
        for g in groups:
            self.play(FadeIn(g,shift=UP))
            self.next_slide()
        
        self.play(FadeOut(g, shift=DOWN) for g in groups)


        # linear search
        # Data
        values = [3, 7, 2, 4, 9, 5, 8]
        target = 5

        # Create boxes with numbers
        boxes = VGroup()
        for v in values:
            box = Square(side_length=1)
            num = Text(str(v)).scale(0.6)
            num.move_to(box.get_center())
            boxes.add(VGroup(box, num))

        boxes.arrange(RIGHT, buff=0.3)

        # Target display
        target_text = Text(f"Lineare Suche − gesucht: {target}").scale(0.7).to_corner(UL).shift(1.2*DOWN)

        self.play(FadeIn(boxes), FadeIn(target_text))

        # Arrow pointer
        pointer = Arrow(0.1*UP, DOWN, buff=0.1).next_to(boxes[0], UP)

        self.play(FadeIn(pointer))
        self.next_slide(loop=True, auto_next=True)

        # Linear search loop
        for i, box in enumerate(boxes):
            # Move pointer
            if i > 0:
                self.play(pointer.animate.next_to(box, UP), run_time=0.5)

            # Highlight current box
            #self.play(box[0].animate.set_fill(YELLOW), run_time=0.5)

            # Check condition
            if values[i] == target:
                # Found!
                self.play(
                    box[0].animate.set_fill(GREEN, opacity=0.7),
                    Flash(box[0], color=GREEN),
                )
                break
            else:
                # Not found, mark red briefly
                self.play(box[0].animate.set_fill(RED, opacity=0.5), run_time=0.5)
                self.play(box[0].animate.set_fill(opacity=0), run_time=0.5)

        self.next_slide()
        self.play(*[FadeOut(e, shift=DOWN) for e in (pointer, boxes, target_text)])

        group = VGroup(
            Text("• Klassischer Computer: Lineare Suche benötigt ≈N/2 Operationen"),
            Text("• Grovers Algorithmus: (π/4)√N Operationen"),
            Text("• 1 Milliarde Elemente: nur ≈25'000 Operationen"),
            Text("• Anwendung für Brute-Force-Suche"),
        ).scale(0.7).arrange(DOWN, aligned_edge=LEFT).to_edge(UP).shift(2*DOWN)

        for text in group:
            self.play(FadeIn(text, shift=UP))
            self.next_slide()
        
        
        self.play(FadeOut(group, shift=DOWN))


        aymmetric_text = Text("Asymmetrische Kryptographie").set_color(ACCENT_YELLOW).scale(0.45).to_corner(UL).shift(DOWN)
        aymmetric_group = VGroup(
            Text("• Verschiedene Schlüssel für Ver- und Entschlüsseln"),
            Text("• Authentifizierung → Identitätsnachweis"),
            Text("• Schlüsselaustausch → Sicherer Austausch eines Geheimnisses"),
            Text("• Beispiele: RSA, DSA, Diffie-Hellman"),
        ).scale(0.35).arrange(DOWN, aligned_edge=LEFT, buff=0.17).next_to(aymmetric_text, DOWN, aligned_edge=LEFT)

        symmetric_text = Text("Symmetrische Kryptographie").set_color(ACCENT_YELLOW).scale(0.45).next_to(aymmetric_group, DOWN, aligned_edge=LEFT, buff=0.35)
        symmetric_group = VGroup(
            Text("• Ein Schlüssel für Ver- und Entschlüsselung von Daten"),
            Text("• Beispiele: AES, Blowfish"),
        ).scale(0.35).arrange(DOWN, aligned_edge=LEFT, buff=0.17).next_to(symmetric_text, DOWN, aligned_edge=LEFT)

        usecase_text = Text("Beispiel: Besuch Webseite").set_color(ACCENT_YELLOW).scale(0.45).next_to(symmetric_group, DOWN, aligned_edge=LEFT, buff=0.35)
        usecase_group = VGroup(
            Text("1. Server schickt Zertifikat"),
            Text("2. Browser überprüft Zertifikat und damit Identität des Servers"),
            Text("3. Schlüsselaustausch → Browser und Server haben ein gemeinsames Passwort"),
            Text("4. Weitere Kommunikation nutzt Passwort zum Ver-/Entschlüsseln"),
        ).scale(0.35).arrange(DOWN, aligned_edge=LEFT, buff=0.17).next_to(usecase_text, DOWN, aligned_edge=LEFT)


        grovers = VGroup(
            Text("Grovers: Effizientes Brute-Force").set_color(ACCENT_RED),
            Text("• klassisch: AES-256 2^256 Operationen"),
            Text("• Grovers: AES-256 2^128 Operationen"),
            Text("• kein großes Problem, evtl. längere Schlüssel"),
        ).scale(0.35).arrange(DOWN, aligned_edge=LEFT, buff=0.17).next_to(symmetric_text, aligned_edge=UP).shift(3*RIGHT+0.2*DOWN)

        shor = VGroup(
            Text("Shor-Algorithmus").set_color(ACCENT_RED),
            Text("• bricht asymmetrische Kryptosysteme wie DSA oder RSA"),
            Text("• asymmetrische post-Quantum Kryptopgrahie existiert"),
            Text("• DSA, RSA, eliptische Kurven & CO müssen ersetzt werden"),
        ).scale(0.35).arrange(DOWN, aligned_edge=LEFT, buff=0.17).next_to(aymmetric_text, aligned_edge=UP).move_to(grovers, aligned_edge=LEFT).shift(2*UP)

        self.play(FadeIn(aymmetric_text, shift=UP), FadeIn(aymmetric_group, shift=UP))
        self.next_slide()
        self.play(FadeIn(symmetric_text, shift=UP), FadeIn(symmetric_group, shift=UP))
        self.next_slide()
        self.play(FadeIn(usecase_text, shift=UP), FadeIn(usecase_group, shift=UP))
        self.next_slide()

        self.play(FadeOut(usecase_text, shift=DOWN), FadeOut(usecase_group, shift=DOWN))
        self.play(FadeIn(shor, shift=UP))
        self.next_slide()
        self.play(FadeIn(grovers, shift=UP))
        self.next_slide()

        self.play(*[FadeOut(e, shift=DOWN) for e in (aymmetric_text, aymmetric_group, symmetric_text, symmetric_group, grovers, shor)])

        google = ImageMobject("images/google.png").to_corner(UP).shift(3*LEFT)
        cloudfare = ImageMobject("images/cloudfare.png").next_to(google, RIGHT)
        openssl = ImageMobject("images/openssl.png").next_to(cloudfare, DOWN, buff=0.6).shift(1.6*LEFT)

        group = Group(google, cloudfare, openssl).shift(0.8*DOWN)

        self.play(FadeIn(group, shift=UP))

        self.transition_next_slide()

class StateOfTheArt(QuantumScene):
    def construct(self):
        self.format_slide("10")
        self.construct_title("Stand der Technik")

        texts = VGroup(
            Text("DiVincenzos Kriterien:").set_color(PURE_YELLOW),
            Text("• Skalierbares System mit Qubits"),
            Text("• Initialisierung von Qubits"),
            Text("• Lange Kohärenzzeit"),
            Text("• Universeller Satz an Quanten-Gatter"),
            Text("• Möglichkeit Qubits zu messen"),
        ).scale(0.55).arrange(DOWN, aligned_edge=LEFT, buff=0.5)#shift(DOWN)

        for t in texts:
            self.play(FadeIn(t, shift=UP))
            self.next_slide()
        
        self.play(FadeOut(texts, shift=DOWN))

        buff = 0.18
        scale = 0.32
        accent_color = ACCENT_YELLOW

        group1 = VGroup(
            Text("Supraleitende Qubits").set_color(accent_color),
            Text("+ Schnelle Gatter"),
            Text("+ Reife Fertigungstechnologie"),
            Text("- Sehr tiefe Temperaturen"),
            Text("- Kurze Kohärenzzeiten"),
            Text("- Begrenzte Konnektivität"),
            Text("IBM, Google, Rigetti, Amazon")
        ).scale(scale).arrange(DOWN, aligned_edge=LEFT, buff=buff)


        group2 = VGroup(
            Text("Gefangene Ionen").set_color(accent_color),
            Text("+ Hohe Genauigkeit, lange Kohärenzzeiten"),
            Text("+ Vollständige Konnektivität"),
            Text("+ Moderate Temperaturen"),
            Text("- Langsame Gatter"),
            Text("- Schwierigere Skalierbarkeit"),
            Text("IonQ, Quantinuum")
        ).scale(scale).arrange(DOWN, aligned_edge=LEFT, buff=buff)

        group3 = VGroup(
            Text("Photonische Quantencomputer").set_color(accent_color),
            Text("+ Betrieb bei Raumtemperatur"),
            Text("+ Gute Skalierungsmöglichkeiten"),
            Text("- Photonenverluste und Rauschen"),
            Text("- Schwierige Erzeugung einzelner Photonen"),
            Text("Firmen: PsiQuantum, Xanadu, Quandela")
        ).scale(scale).arrange(DOWN, aligned_edge=LEFT, buff=buff)

        group4 = VGroup(
            Text("Neutrale Atome").set_color(accent_color),
            Text("+ Sehr gut skalierbare Gitterstrukturen"),
            Text("+ Betrieb bei Raumtemperatur"),
            Text("- Noch geringere Genauigkeit als Ionen"),
            Text("- Weniger ausgereift"),
            Text("QuEra, Atom Computing, Infleqtion")
        ).scale(scale).arrange(DOWN, aligned_edge=LEFT, buff=buff)

        group5 = VGroup(
            Text("Spin-Qubits").set_color(accent_color),
            Text("+ Großes Skalierungspotenzial"),
            Text("+ Sehr kompakte Qubits"),
            Text("+ Integration mit klassischer Elektronik möglich"),
            Text("- Hohe Anforderungen an die Fertigung"),
            Text("- Begrenzte Kohärenzzeiten"),
            Text("Intel, IBM, Silicon Quantum Computing")
        ).scale(scale).arrange(DOWN, aligned_edge=LEFT, buff=buff)

        groups = (group1, group2, group3, group4, group5)
        for group in groups:
            for j,elem in enumerate(group):
                if j== 0:
                    elem.scale(1.1)
                    continue
                #elem.shift(0.2*RIGHT)
                if elem.text.startswith("+"):
                    elem.set_color(GREEN)
                elif elem.text.startswith("-"):
                    elem.set_color(RED)
        
        group1.to_corner(UL).shift(.9*DOWN)
        group2.move_to(group1, aligned_edge=UP).shift(4.5*RIGHT)
        group3.move_to(group1, aligned_edge=UP).shift(9*RIGHT)

        group4.next_to(group1, DOWN, aligned_edge=LEFT, buff=1)
        group5.move_to(group4, aligned_edge=UP).shift(4.5*RIGHT)


        for group in groups:
            self.play(FadeIn(group, shift=UP))
            self.next_slide()
        
        self.play(*[FadeOut(group, shift=UP) for group in groups])


        image = ImageMobject("images/scatter.png")
        source = Text("Olivier Ezratty, Understanding Quantum Technologies, 8th edition").scale(0.3)
        source.next_to(image, DOWN)
        scatter = Group(image, source).scale(0.9).shift(0.2*DOWN)

        self.play(FadeIn(scatter, shift=UP))

        self.transition_next_slide()


class Summary(QuantumScene):
    def construct(self):
        self.format_slide("11")
        title = self.construct_title("Zusammenfassung")

        texts = VGroup(
            Text("• Quantencomputer sind effizienter für einige Probleme…"),
            Text("• …dank Überlagerung und Verschränkung"),
            Text("• Quantencomputer werden leistungsstärker"),
            Text("• Quantenalgorithmen könnten einige Bereiche revolutionieren"),
            Text("• Quantencomputer werden klassische Computer nicht ersetzen"),
        ).scale(0.55).arrange(DOWN, aligned_edge=LEFT, buff=0.4)

        for text in texts:
            self.play(FadeIn(text, shift=UP))
            self.next_slide()

        self.play(FadeOut(texts, shift=DOWN), FadeOut(title, shift=DOWN))

        thankyou = Text("Vielen Dank für die Aufmerksamkeit!", color=ACCENT_YELLOW).shift(UP)
        questions = Text("Fragen?", color=ACCENT_PURPLE).next_to(thankyou, DOWN, buff=1)
        self.play(FadeIn(thankyou, shift=UP))
        self.play(FadeIn(questions, shift=UP))

        self.play(
            thankyou.animate.scale(1.05),
            rate_func=there_and_back,
            run_time=2
        )