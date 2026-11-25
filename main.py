import math
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

Window.clearcolor = (0.055, 0.06, 0.075, 1)


class AttendanceApp(App):
    def build(self):
        self.title = "Smart Attendance"
        self.future_present = 0
        self.future_absent = 0
        self.target = 75

        root = BoxLayout(orientation="vertical", padding=dp(14))
        # User-provided photo background with a dark overlay for readability.
        with root.canvas.before:
            Color(1, 1, 1, 1)
            self.background_rect = Rectangle(
                source="background.jpg", pos=root.pos, size=root.size
            )
            Color(0, 0, 0, 0.48)
            self.overlay_rect = Rectangle(pos=root.pos, size=root.size)
        root.bind(
            pos=self._update_background,
            size=self._update_background
        )
        scroll = ScrollView()
        content = BoxLayout(
            orientation="vertical", spacing=dp(10),
            size_hint_y=None, padding=[0, dp(5), 0, dp(18)]
        )
        content.bind(minimum_height=content.setter("height"))

        content.add_widget(self.label("SMART ATTENDANCE", 25, "#FFA726", 48))
        self.welcome = self.label("Your personal attendance calculator", 13, "#AAAAAA", 30)
        content.add_widget(self.welcome)

        content.add_widget(self.section("YOUR NAME"))
        self.name_input = self.input("Enter your name", text="")
        self.name_input.bind(text=self.update_name)
        content.add_widget(self.name_input)

        content.add_widget(self.section("CURRENT ATTENDANCE"))
        row = GridLayout(cols=2, spacing=dp(10), size_hint_y=None, height=dp(78))
        pbox = BoxLayout(orientation="vertical", spacing=dp(4))
        tbox = BoxLayout(orientation="vertical", spacing=dp(4))
        pbox.add_widget(self.label("Present days", 12, "#AAAAAA", 24))
        tbox.add_widget(self.label("Total working days", 12, "#AAAAAA", 24))
        self.present_input = self.input("Present days", "101")
        self.total_input = self.input("Total days", "131")
        self.present_input.input_filter = "int"
        self.total_input.input_filter = "int"
        pbox.add_widget(self.present_input)
        tbox.add_widget(self.total_input)
        row.add_widget(pbox)
        row.add_widget(tbox)
        content.add_widget(row)

        self.current_label = self.label("--", 32, "#55E889", 52)
        content.add_widget(self.current_label)
        content.add_widget(self.label("CURRENT ATTENDANCE", 10, "#AAAAAA", 22))

        content.add_widget(self.section("DAYS YOU WILL ATTEND"))
        self.attend_value = self.label("0 days", 17, "#55E889", 30)
        content.add_widget(self.attend_value)
        self.attend_slider = Slider(min=0, max=100, value=0, step=1)
        self.attend_slider.bind(value=self.on_attend)
        content.add_widget(self.attend_slider)

        content.add_widget(self.section("DAYS YOU WILL BE ABSENT"))
        self.absent_value = self.label("0 days", 17, "#FF6262", 30)
        content.add_widget(self.absent_value)
        self.absent_slider = Slider(min=0, max=100, value=0, step=1)
        self.absent_slider.bind(value=self.on_absent)
        content.add_widget(self.absent_slider)

        content.add_widget(self.section("PREDICTED ATTENDANCE"))
        self.future_label = self.label("--", 36, "#55E889", 55)
        content.add_widget(self.future_label)
        self.change_label = self.label("No change", 15, "#FFFFFF", 32)
        content.add_widget(self.change_label)
        self.status_label = self.label("--", 14, "#55E889", 30)
        content.add_widget(self.status_label)

        content.add_widget(self.section("FUTURE ATTENDANCE BREAKDOWN"))
        self.breakdown_label = self.label("--", 14, "#FFFFFF", 78)
        content.add_widget(self.breakdown_label)

        content.add_widget(self.section("ATTENDANCE TARGET"))
        target_row = GridLayout(cols=4, spacing=dp(5), size_hint_y=None, height=dp(44))
        for value in (75, 80, 85, 90):
            button = Button(
                text=f"{value}%", background_normal="",
                background_color=(0.16, 0.20, 0.27, 1)
            )
            button.bind(on_release=lambda instance, v=value: self.set_target(v))
            target_row.add_widget(button)
        content.add_widget(target_row)

        self.allowance_label = self.label("--", 15, "#55E889", 38)
        content.add_widget(self.allowance_label)
        self.needed_label = self.label("--", 14, "#58A6FF", 38)
        content.add_widget(self.needed_label)

        calc = Button(
            text="CALCULATE ATTENDANCE", size_hint_y=None, height=dp(50),
            background_normal="", background_color=(1, 0.60, 0.13, 1),
            color=(0, 0, 0, 1), bold=True
        )
        calc.bind(on_release=lambda *_: self.calculate())
        content.add_widget(calc)

        reset = Button(
            text="RESET SLIDERS", size_hint_y=None, height=dp(46),
            background_normal="", background_color=(0.20, 0.22, 0.26, 1)
        )
        reset.bind(on_release=lambda *_: self.reset_sliders())
        content.add_widget(reset)

        content.add_widget(self.label("Made with Python + Kivy", 11, "#888888", 30))
        scroll.add_widget(content)
        root.add_widget(scroll)

        self.present_input.bind(text=lambda *_: self.calculate())
        self.total_input.bind(text=lambda *_: self.calculate())
        Clock.schedule_once(lambda *_: self.calculate(), 0.3)
        return root


    def _update_background(self, instance, value):
        self.background_rect.pos = instance.pos
        self.background_rect.size = instance.size
        self.overlay_rect.pos = instance.pos
        self.overlay_rect.size = instance.size

    def label(self, text, size, color, height):
        return Label(
            text=text, font_size=dp(size), color=self.hex_color(color),
            size_hint_y=None, height=dp(height),
            halign="center", valign="middle"
        )

    def section(self, text):
        return self.label(text, 14, "#FFA726", 32)

    def input(self, hint, text=""):
        return TextInput(
            hint_text=hint, text=text, multiline=False,
            size_hint_y=None, height=dp(45),
            background_color=(0.15, 0.17, 0.20, 1),
            foreground_color=(1, 1, 1, 1),
            hint_text_color=(0.65, 0.65, 0.65, 1),
            cursor_color=(1, 1, 1, 1), padding=dp(10)
        )

    def hex_color(self, value):
        value = value.lstrip("#")
        return tuple(int(value[i:i+2], 16) / 255 for i in (0, 2, 4)) + (1,)

    def update_name(self, instance, value):
        self.welcome.text = f"Welcome, {value.strip()}!" if value.strip() else "Your personal attendance calculator"

    def on_attend(self, instance, value):
        self.future_present = int(value)
        self.attend_value.text = f"{self.future_present} days"
        self.calculate()

    def on_absent(self, instance, value):
        self.future_absent = int(value)
        self.absent_value.text = f"{self.future_absent} days"
        self.calculate()

    def set_target(self, value):
        self.target = value
        self.calculate()

    def calculate(self):
        try:
            p = int(self.present_input.text)
            t = int(self.total_input.text)
            if t <= 0 or p < 0 or p > t:
                raise ValueError

            fp, fa, target = self.future_present, self.future_absent, self.target
            current = 100 * p / t
            new_p = p + fp
            new_t = t + fp + fa
            predicted = 100 * new_p / new_t
            diff = predicted - current

            self.current_label.text = f"{current:.2f}%"
            self.future_label.text = f"{predicted:.2f}%"

            if diff > 0.001:
                self.change_label.text = f"▲ +{diff:.2f} percentage points"
                self.change_label.color = self.hex_color("#55E889")
            elif diff < -0.001:
                self.change_label.text = f"▼ {diff:.2f} percentage points"
                self.change_label.color = self.hex_color("#FF6262")
            else:
                self.change_label.text = "No change"
                self.change_label.color = self.hex_color("#FFFFFF")

            if predicted >= target:
                self.status_label.text = f"ON TRACK — at or above {target}%"
                self.status_label.color = self.hex_color("#55E889")
            else:
                self.status_label.text = f"BELOW TARGET — {target}%"
                self.status_label.color = self.hex_color("#FF6262")

            absent_total = t - p + fa
            self.breakdown_label.text = (
                f"Present: {new_p} days\n"
                f"Absent: {absent_total} days\n"
                f"Total: {new_t} days"
            )

            # Maximum additional absences while staying at or above target.
            remaining = math.floor((new_p * 100 / target) - new_t + 1e-10)
            self.allowance_label.text = (
                f"Additional absences before falling below {target}%: {max(0, remaining)}"
            )

            if predicted >= target:
                needed = 0
            elif target >= 100:
                needed = "Not reachable"
            else:
                needed = math.ceil((target * new_t - 100 * new_p) / (100 - target))
            self.needed_label.text = f"Consecutive present days to reach {target}%: {needed}"

        except (ValueError, ZeroDivisionError):
            self.current_label.text = "--"
            self.future_label.text = "--"
            self.change_label.text = "Enter valid present and total days"
            self.status_label.text = "Check your inputs"
            self.breakdown_label.text = "--"
            self.allowance_label.text = "--"
            self.needed_label.text = "--"

    def reset_sliders(self):
        self.attend_slider.value = 0
        self.absent_slider.value = 0
        self.future_present = 0
        self.future_absent = 0
        self.calculate()


if __name__ == "__main__":
    AttendanceApp().run()
