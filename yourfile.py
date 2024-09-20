from manimlib import *


class UpdatersExample(Scene):
    def construct(self):
        square = Square()
        square.set_fill(BLUE_E, 1)
        
        # 在所有帧上，构造函数 Brace（square， UP） 将
        # 被调用，mobject 大括号会将其数据设置为匹配
        # 新建对象的对象
        brace = always_redraw(Brace, square, UP)
        
        text, number = label = VGroup(
            Text("Width = "),
            DecimalNumber(
                0,
                show_ellipsis=True,
                num_decimal_places=2,
                include_sign=True,
            )
        )
        label.arrange(RIGHT)
        
        # 这确保了方法deicmal.next_to（square）
        # 在每一帧上被调用
        always(label.next_to, brace, UP)
        # 您也可以编写以下等效行
        # label.add_updater（lambda m： m.next_to（大括号， UP））
        
        # 如果参数本身可能会发生变化，你可以使用 f_always，
        # 其中的参数遵循初始 Mobject 方法
        # 应该是返回该方法参数的函数。
        # 以下行确保 decimal.set_value（square.get_y（））
        # 称为每帧
        f_always(number.set_value, square.get_width)
        # 你也可以写出以下等效的行
        # number.add_updater（lambda m： m.set_value（square.get_width（）））
        
        self.add(square, brace, label)
        
        # Notice that the brace and label track with the square
        self.play(
            square.animate.scale(2),
            rate_func=there_and_back,
            run_time=2,
        )
        self.wait()
        self.play(
            square.animate.set_width(5, stretch=True),
            run_time=3,
        )
        self.wait()
        self.play(
            square.animate.set_width(2),
            run_time=3
        )
        self.wait()
        
        # 一般来说，您可以随时调用Mobject.add_updater，然后传入
        # 您希望在每一帧上调用的函数。 函数
        # 应该接受一个参数，mobject 或两个参数，
        # mobject 和自上一帧以来的时间量。
        now = self.time
        w0 = square.get_width()
        square.add_updater(
            lambda m: m.set_width(w0 * math.cos(self.time - now))
        )
        self.wait(4 * PI)
