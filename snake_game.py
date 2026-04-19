"""A simple Snake game implemented with Python's built-in turtle module.

Run:
    python3 snake_game.py
"""

from __future__ import annotations

import random
import time
import turtle

# Window/game settings
WIDTH = 600
HEIGHT = 600
STEP = 20
START_DELAY = 0.12
SPEEDUP_FACTOR = 0.98
MIN_DELAY = 0.05


class SnakeGame:
    def __init__(self) -> None:
        self.screen = turtle.Screen()
        self.screen.title("Snake Game")
        self.screen.bgcolor("black")
        self.screen.setup(width=WIDTH, height=HEIGHT)
        self.screen.tracer(0)

        self.head = self._make_segment("lime")
        self.head.goto(0, 0)
        self.head.direction = "stop"

        self.segments: list[turtle.Turtle] = []

        self.food = self._make_segment("red", shape="circle")
        self._reposition_food()

        self.score = 0
        self.high_score = 0
        self.delay = START_DELAY

        self.pen = turtle.Turtle()
        self.pen.hideturtle()
        self.pen.color("white")
        self.pen.penup()
        self.pen.goto(0, HEIGHT // 2 - 40)
        self._draw_score()

        self._bind_keys()

    @staticmethod
    def _make_segment(color: str, shape: str = "square") -> turtle.Turtle:
        part = turtle.Turtle()
        part.speed(0)
        part.shape(shape)
        part.color(color)
        part.penup()
        return part

    def _bind_keys(self) -> None:
        self.screen.listen()
        self.screen.onkeypress(lambda: self._set_direction("up"), "Up")
        self.screen.onkeypress(lambda: self._set_direction("down"), "Down")
        self.screen.onkeypress(lambda: self._set_direction("left"), "Left")
        self.screen.onkeypress(lambda: self._set_direction("right"), "Right")
        self.screen.onkeypress(self._restart, "r")
        self.screen.onkeypress(self._quit, "q")

    def _set_direction(self, direction: str) -> None:
        opposites = {
            "up": "down",
            "down": "up",
            "left": "right",
            "right": "left",
        }
        if self.head.direction != opposites.get(direction):
            self.head.direction = direction

    def _move(self) -> None:
        x, y = self.head.xcor(), self.head.ycor()
        if self.head.direction == "up":
            self.head.sety(y + STEP)
        elif self.head.direction == "down":
            self.head.sety(y - STEP)
        elif self.head.direction == "left":
            self.head.setx(x - STEP)
        elif self.head.direction == "right":
            self.head.setx(x + STEP)

    def _reposition_food(self) -> None:
        max_x = (WIDTH // 2 - STEP) // STEP
        max_y = (HEIGHT // 2 - STEP) // STEP
        fx = random.randint(-max_x, max_x) * STEP
        fy = random.randint(-max_y, max_y) * STEP
        self.food.goto(fx, fy)

    def _draw_score(self) -> None:
        self.pen.clear()
        text = (
            f"Score: {self.score}    High Score: {self.high_score}    "
            "Controls: arrows | R restart | Q quit"
        )
        self.pen.write(text, align="center", font=("Courier", 14, "normal"))

    def _reset_round(self) -> None:
        time.sleep(0.4)
        self.head.goto(0, 0)
        self.head.direction = "stop"

        for segment in self.segments:
            segment.goto(1000, 1000)
        self.segments.clear()

        self.score = 0
        self.delay = START_DELAY
        self._reposition_food()
        self._draw_score()

    def _restart(self) -> None:
        self._reset_round()

    def _quit(self) -> None:
        self.screen.bye()

    def _wall_collision(self) -> bool:
        half_w, half_h = WIDTH // 2, HEIGHT // 2
        return (
            self.head.xcor() >= half_w
            or self.head.xcor() <= -half_w
            or self.head.ycor() >= half_h
            or self.head.ycor() <= -half_h
        )

    def _self_collision(self) -> bool:
        return any(self.head.distance(segment) < 10 for segment in self.segments)

    def _eat_food(self) -> None:
        if self.head.distance(self.food) < 15:
            self._reposition_food()

            new_segment = self._make_segment("grey")
            self.segments.append(new_segment)

            self.score += 10
            if self.score > self.high_score:
                self.high_score = self.score

            self.delay = max(MIN_DELAY, self.delay * SPEEDUP_FACTOR)
            self._draw_score()

    def _follow_head(self) -> None:
        for idx in range(len(self.segments) - 1, 0, -1):
            x = self.segments[idx - 1].xcor()
            y = self.segments[idx - 1].ycor()
            self.segments[idx].goto(x, y)

        if self.segments:
            self.segments[0].goto(self.head.xcor(), self.head.ycor())

    def run(self) -> None:
        while True:
            self.screen.update()

            if self._wall_collision() or self._self_collision():
                self._reset_round()

            self._eat_food()
            self._follow_head()
            self._move()

            time.sleep(self.delay)


def main() -> None:
    game = SnakeGame()
    game.run()


if __name__ == "__main__":
    main()
