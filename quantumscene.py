from manim import *
from manim_slides import Slide, ThreeDSlide

# ========================
# Quantum Dark Theme Setup
# ========================

AUTHOR = "Michael Hartmann"
EVENT = "Augsburger Linux-Infotag 2026"

BACKGROUND_COLOR = "#0b0f1a"
TEXT_COLOR = "#e6edf3"
ACCENT_CYAN = "#00d4ff"
ACCENT_PURPLE = "#a78bfa"
ACCENT_RED = "#f43f5e"
ACCENT_BLUE= "#3f5af4"
ACCENT_YELLOW = PURE_YELLOW

__all__ = ["AUTHOR", "EVENT", "BACKGROUND_COLOR", "TEXT_COLOR", "ACCENT_CYAN", "ACCENT_PURPLE", "ACCENT_RED", "ACCENT_BLUE", "ACCENT_YELLOW", "QuantumScene", "QuantumScene3D"]

config.background_color = BACKGROUND_COLOR

class QuantumBaseScene():
    def format_slide(self, slide_number, color=TEXT_COLOR, buff=0.3, scale=0.4, opacity=0.7):
        page = Text(slide_number, color=TEXT_COLOR).scale(scale)
        page.set_opacity(opacity)
        page.to_edge(DR, buff=buff)

        lit = Text(EVENT, color=color).scale(scale)
        lit._do_not_fadeout = True
        lit.set_opacity(opacity)
        lit.to_edge(DOWN, buff=buff)

        if hasattr(self, "add_fixed_in_frame_mobjects"):
            self.add_fixed_in_frame_mobjects(lit,page)

        self.add(lit)
        self.play(FadeIn(page, shift=UP))

    def construct_title(self, title_text):
        title = Text(title_text, color=TEXT_COLOR).scale(1)
        title.to_edge(UP)
        if hasattr(self, "add_fixed_in_frame_mobjects"):
            self.add_fixed_in_frame_mobjects(title)
        self.play(FadeIn(title, shift=UP))
        return title

    def transition_next_slide(self, wait=True):
        if wait:
            self.next_slide(auto_next=True)

        animations = []
        for m in self.mobjects:
            if hasattr(m, "_do_not_fadeout"):
                continue
            animations.append(FadeOut(m, shift=DOWN))
        
        self.play(*animations)


class QuantumScene(QuantumBaseScene, Slide):
    pass

class QuantumScene3D(QuantumBaseScene, ThreeDSlide):
    pass