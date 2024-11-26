import flet as ft
import math  # 数学関数を利用するためにインポート


class CalcButton(ft.ElevatedButton):
    def __init__(self, text, button_clicked, expand=1):
        super().__init__()
        self.text = text
        self.expand = expand
        self.on_click = button_clicked
        self.data = text


class DigitButton(CalcButton):
    def __init__(self, text, button_clicked, expand=1):
        CalcButton.__init__(self, text, button_clicked, expand)
        self.bgcolor = ft.colors.WHITE24
        self.color = ft.colors.WHITE


class ActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.colors.ORANGE
        self.color = ft.colors.WHITE


class ExtraActionButton(CalcButton):
    def __init__(self, text, button_clicked):
        CalcButton.__init__(self, text, button_clicked)
        self.bgcolor = ft.colors.BLUE_GREY_100
        self.color = ft.colors.BLACK


class CalculatorApp(ft.Container):
    def __init__(self):
        super().__init__()
        self.reset()

        self.result = ft.Text(value="0", color=ft.colors.WHITE, size=20)
        self.width = 350
        self.bgcolor = ft.colors.BLACK
        self.border_radius = ft.border_radius.all(20)
        self.padding = 20
        self.content = ft.Column(
            controls=[
                ft.Row(controls=[self.result], alignment="end"),
                ft.Row(
                    controls=[
                        ExtraActionButton(
                            text="AC", button_clicked=self.button_clicked
                        ),
                        ExtraActionButton(
                            text="+/-", button_clicked=self.button_clicked
                        ),
                        ExtraActionButton(text="%", button_clicked=self.button_clicked),
                        ActionButton(text="/", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="7", button_clicked=self.button_clicked),
                        DigitButton(text="8", button_clicked=self.button_clicked),
                        DigitButton(text="9", button_clicked=self.button_clicked),
                        ActionButton(text="*", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="4", button_clicked=self.button_clicked),
                        DigitButton(text="5", button_clicked=self.button_clicked),
                        DigitButton(text="6", button_clicked=self.button_clicked),
                        ActionButton(text="-", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(text="1", button_clicked=self.button_clicked),
                        DigitButton(text="2", button_clicked=self.button_clicked),
                        DigitButton(text="3", button_clicked=self.button_clicked),
                        ActionButton(text="+", button_clicked=self.button_clicked),
                    ]
                ),
                ft.Row(
                    controls=[
                        DigitButton(
                            text="0", expand=2, button_clicked=self.button_clicked
                        ),
                        DigitButton(text=".", button_clicked=self.button_clicked),
                        ActionButton(text="=", button_clicked=self.button_clicked),
                    ]
                ),
                # 特殊関数ボタンを配置
                ft.Row(
                    controls=[
                        ExtraActionButton(text="log10", button_clicked=self.button_clicked),
                        ExtraActionButton(text="ln", button_clicked=self.button_clicked),
                        ExtraActionButton(text="sin", button_clicked=self.button_clicked),
                        ExtraActionButton(text="cos", button_clicked=self.button_clicked),
                        ExtraActionButton(text="^", button_clicked=self.button_clicked),
                        ExtraActionButton(text="√", button_clicked=self.button_clicked),  # 平方根ボタン
                        ExtraActionButton(text="n!", button_clicked=self.button_clicked),  # 階乗ボタン
                    ]
                ),
            ]
        )

    def button_clicked(self, e):
        data = e.control.data
        print(f"Button clicked with data = {data}")
        try:
            if self.result.value == "Error" or data == "AC":
                self.result.value = "0"
                self.reset()

            elif data in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."):
                if self.result.value == "0" or self.new_operand:
                    self.result.value = data
                    self.new_operand = False
                else:
                    self.result.value += data

            elif data in ("+", "-", "*", "/"):
                self.operand1 = float(self.result.value)
                self.operator = data
                self.new_operand = True

            elif data == "^":  # x^y 演算子
                self.operand1 = float(self.result.value)
                self.operator = "^"
                self.new_operand = True

            elif data == "=":
                self.result.value = self.calculate(
                    self.operand1, float(self.result.value), self.operator
                )
                self.reset()

            elif data == "log10":  # 常用対数
                if float(self.result.value) > 0:
                    self.result.value = math.log10(float(self.result.value))
                else:
                    self.result.value = "Error"

            elif data == "ln":  # 自然対数
                if float(self.result.value) > 0:
                    self.result.value = math.log(float(self.result.value))
                else:
                    self.result.value = "Error"

            elif data == "sin":
                self.result.value = math.sin(math.radians(float(self.result.value)))
            elif data == "cos":
                self.result.value = math.cos(math.radians(float(self.result.value)))

            elif data == "√":  # 平方根
                if float(self.result.value) >= 0:
                    self.result.value = math.sqrt(float(self.result.value))
                else:
                    self.result.value = "Error"

            elif data == "n!":  # 階乗
                if float(self.result.value).is_integer() and float(self.result.value) >= 0:
                    self.result.value = math.factorial(int(float(self.result.value)))
                else:
                    self.result.value = "Error"

            elif data == "%":
                self.result.value = float(self.result.value) / 100

            elif data == "+/-":
                self.result.value = str(-float(self.result.value))

        except Exception as ex:
            print(f"Error: {ex}")
            self.result.value = "Error"

        self.update()

    def calculate(self, operand1, operand2, operator):
        try:
            if operator == "+":
                return operand1 + operand2
            elif operator == "-":
                return operand1 - operand2
            elif operator == "*":
                return operand1 * operand2
            elif operator == "/":
                if operand2 == 0:
                    return "Error"
                return operand1 / operand2
            elif operator == "^":  # x^y の計算
                return math.pow(operand1, operand2)
        except:
            return "Error"

    def reset(self):
        self.operator = "+"
        self.operand1 = 0
        self.new_operand = True


def main(page: ft.Page):
    page.title = "Calculator with Factorial"
    calc = CalculatorApp()
    page.add(calc)


ft.app(target=main)
