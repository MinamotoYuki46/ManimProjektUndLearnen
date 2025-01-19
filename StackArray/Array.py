from manim import *

class Array(Scene):
    def construct(self):
        cell = Rectangle(
                color=WHITE, 
                width=1, 
                height=1, 
                stroke_width=2)
        
        array = VGroup(*[cell.copy().shift(RIGHT * i) for i in range(10)])

        arrow = Arrow(start=DOWN, end=UP, color=RED).scale(0.5)
        arrow.move_to(array[0].get_bottom() + DOWN * 0.5)
        top_text = Text("top", font_size=24, color=RED).next_to(arrow, DOWN, buff=0.2)

        ptr_top = VGroup(arrow, top_text)

        stack_elements = [15, 6, 2, 9]
        top = len(stack_elements) - 1

        array.move_to(ORIGIN)

        # Title
        text_label = Text("Stack (with array approach)", font_size=48)
        text_label.move_to(UP * 2)
        self.play(FadeIn(text_label))
        self.wait(1)

        for i, cell in enumerate(array):
            cell.set_fill(BLUE, opacity=0.5)
        self.play(Create(array))
        self.wait(1)


        index_indicators = VGroup()
        for i, cell in enumerate(array):
            index_indicator = MathTex(f"{i}")
            index_indicator.next_to(cell, UP, buff=0.1)
            index_indicators.add(index_indicator)
        self.play(FadeIn(index_indicators))
        self.wait(1)

        ptr_top.move_to(array[0].get_bottom() + DOWN * 0.5 + LEFT * 0.5)
        self.play(FadeIn(ptr_top))
        self.wait(1)

        cell_values = VGroup()  

        def stack_load():
            for i, cell in enumerate(array):
                if i < len(stack_elements):
                    value = MathTex(str(stack_elements[i]))
                    value.move_to(cell.get_center())
                    cell_values.add(value)  # Track values
                    self.play(ptr_top.animate.move_to(cell.get_bottom() + DOWN * 0.5))
                    self.add(value)
                    self.play(cell.animate.set_fill(YELLOW, opacity=0.5))
                    

        def stack_push(value):
            nonlocal top
            top += 1
            stack_elements.append(value)

            update_command_screen(command_text, f"push({value})")

            cell = array[top]
            arrow_target = array[top].get_bottom() + DOWN * 0.5

            if len(cell_values) > top:
                existing_value = cell_values[top]
                new_value = MathTex(str(value))
                new_value.move_to(cell.get_center())
                self.play(ptr_top.animate.move_to(arrow_target))
                self.play(cell.animate.set_fill(YELLOW, opacity=0.5)) 
                self.play(
                    existing_value.animate.scale(0.5).move_to(new_value.get_center()),
                    Transform(existing_value, new_value) 
                )  
                cell_values[top] = new_value
            else:
                new_value = MathTex(str(value))
                new_value.move_to(cell.get_center())
                cell_values.add(new_value)
                self.play(ptr_top.animate.move_to(arrow_target))
                self.add(new_value)
                self.play(cell.animate.set_fill(YELLOW, opacity=0.5)) 

        def stack_pop():
            nonlocal top
            if top < 0:
                return
            stack_elements.pop()

            update_command_screen(command_text, f"pop()")

            top -= 1

            arrow_target = array[top].get_bottom() + DOWN * 0.5 if top >= 0 else arrow.get_start()
            self.play(ptr_top.animate.move_to(arrow_target))
            self.play(array[top + 1].animate.set_fill(BLUE, opacity=0.5))
        
        def create_command_screen():
            screen_box = Rectangle(width=6, height=2, color=WHITE, fill_color=BLACK, fill_opacity=0.7)
            screen_box.move_to(DOWN * 3)  
            command_text = MathTex(f"\\texttt{{-}}", font_size=24, color=WHITE)
            command_text.move_to(screen_box.get_center())  
            return screen_box, command_text
    
        def update_command_screen(command_text, command):
            new_command_text = MathTex(f"\\texttt{{Current Command: {command}}}", font_size=24, color=WHITE)
            new_command_text.move_to(command_text.get_center())  

            self.play(Transform(command_text, new_command_text))

        command_screen, command_text = create_command_screen()

        self.add(command_screen)
        self.add(command_text)
        
        update_command_screen(command_text, f"loading stack...")
        stack_load()
        self.wait(1) 

        stack_push(17)
        self.wait(1)

        stack_push(3)
        self.wait(1)

        stack_pop()
        self.wait(1)

        stack_pop()
        self.wait(1)

        stack_push(4)
        self.wait(1)
