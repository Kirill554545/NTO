import random
import math
import tkinter as tk
import pymunk
import pymunk.pygame_util
from datetime import datetime

global hi
hi = 0
WIDTH = 800
HEIGHT = 600
initial_speeds = [-6, -5, -4, 4, 5, 6]
dx, dy = 0, 0
while dx == dy:
    dx, dy = random.choice(initial_speeds), random.choice(initial_speeds)
line_segments = []
coords = []
basket_segments = []

global sch1
sch1 = 0

global count
count = 0

global time_left
time_left = 60


def create_ball(space):
    mass = 1
    radius = 10
    inertia = pymunk.moment_for_circle(mass, 0, radius)
    body = pymunk.Body(mass, inertia)
    x = 50
    y = 50
    body.position = x, y
    shape = pymunk.Circle(body, radius)
    shape.elasticity = 1.0
    shape.friction = 0.0
    space.add(body, shape)
    return shape


def bounce(space, size):
    global dx, dy, line_segments
    ball_shape = space.shapes[0]
    if ball_shape.body.position.x <= 0 or ball_shape.body.position.x >= WIDTH:
        dx = -dx
    if ball_shape.body.position.y <= 0 or ball_shape.body.position.y >= HEIGHT:
        dy = -dy
    sch = 0
    for line in line_segments:
        if len(coords) > sch:
            coord = coords[sch]
        sch += 1
        closest_point = line.point_query(ball_shape.body.position)
        distance = math.sqrt((ball_shape.body.position.x - closest_point.point.x) ** 2 +
                             (ball_shape.body.position.y - closest_point.point.y) ** 2)
        if distance <= size:
            st = coord[0]
            end = coord[1]
            x, y = st[0], st[1]
            x1, y1 = end[0], end[1]

            if x1 - x != 0:
                angle = abs(math.atan((y - y1) / (x1 - x))) * 57.295779514719953173
            else:
                angle = 46
            if angle > 45:
                dx = -dx
            if angle <= 45:
                dy = -dy
    ball_shape.body.velocity = dx, dy


def draw_line(event):
    global start_x, start_y
    start_x, start_y = event.x, event.y


def release_line(event):
    global space, line_segments
    end_x, end_y = event.x, event.y
    static_body = space.static_body
    static_lines = [pymunk.Segment(static_body, (start_x, HEIGHT - start_y), (end_x, HEIGHT - end_y), 5)]
    canvas.create_line(start_x, start_y, end_x, end_y, fill="black")
    line = (start_x, HEIGHT - start_y), (end_x, HEIGHT - end_y)
    line_segments.append(static_lines[0])
    coords.append(line)

    for line in static_lines:
        line.elasticity = 1.0
        line.friction = 0.0
        line.color = (255, 255, 255)  # set line color to white
        space.add(line)


# Добавляем статичную корзинку
def create_basket():
    static_body1 = space.static_body
    basket_width = 150
    basket_height = 20
    basket_segment = pymunk.Segment(static_body1, (WIDTH - basket_width, basket_height), (WIDTH - 20, basket_height), 5)
    canvas.create_line(WIDTH - basket_width, HEIGHT - basket_height, WIDTH - 20, HEIGHT - basket_height, fill="black")
    line_segments.append(basket_segment)
    line = (WIDTH - basket_width, basket_height), (WIDTH - 20, basket_height)
    coords.append(line)
    basket_segments.append(basket_segment)
    basket_segment.elasticity = 1.0
    basket_segment.friction = 0.0
    basket_segment.color = (255, 255, 255)
    space.add(basket_segment)
    left = WIDTH - basket_width
    down = basket_height
    right = WIDTH - 20

    static_body1 = space.static_body
    basket_height = 20
    basket_height1 = 100
    basket_segment = pymunk.Segment(static_body1, (WIDTH - basket_width, basket_height),
                                    (WIDTH - basket_width, basket_height1), 5)
    canvas.create_line(WIDTH - basket_width, HEIGHT - basket_height, WIDTH - basket_width, HEIGHT - basket_height1,
                       fill="black")
    line_segments.append(basket_segment)
    line = (WIDTH - basket_width, basket_height), (WIDTH - basket_width, basket_height1)
    coords.append(line)
    basket_segments.append(basket_segment)
    basket_segment.elasticity = 1.0
    basket_segment.friction = 0.0
    basket_segment.color = (255, 255, 255)
    space.add(basket_segment)
    up = basket_height1

    static_body1 = space.static_body
    basket_width = 20
    basket_height = 20
    basket_height1 = 100
    basket_segment = pymunk.Segment(static_body1, (WIDTH - 20, basket_height),
                                    (WIDTH - 20, basket_height1), 5)
    canvas.create_line(WIDTH - basket_width, HEIGHT - basket_height, WIDTH - basket_width, HEIGHT - basket_height1,
                       fill="black")
    line_segments.append(basket_segment)
    line = (WIDTH - 20, basket_height), (WIDTH - 20, basket_height1)
    coords.append(line)
    basket_segments.append(basket_segment)
    basket_segment.elasticity = 1.0
    basket_segment.friction = 0.0
    basket_segment.color = (255, 255, 255)
    space.add(basket_segment)

    return (left, right, up, down)


def ball_in_basket(bx, by, left, right, up, down):
    if left <= bx <= right and down <= by <= up:
        print("Мячик в корзине!")
        return True


def main():
    current_time = datetime.now()
    elapsed_time = current_time - start_time
    global dx, dy, space, canvas, count
    root = tk.Tk()
    root.wm_title("Bouncing Ball")
    root.geometry("800x600")
    canvas = tk.Canvas(root, width=800, height=600, bg="white")
    canvas.pack(expand=True, fill=tk.BOTH)
    space = pymunk.Space()
    space.gravity = 0, 1000
    global ball_shape
    ball_shape = create_ball(space)

    left, right, up, down = create_basket()

    canvas.bind("<Button-1>", draw_line)
    canvas.bind("<ButtonRelease-1>", release_line)
    size = 10

    timer_label = tk.Label(root, text="Time left: 60 sec")
    timer_label.pack()

    counter_label = tk.Label(root, text="Balls in basket: 0")
    counter_label.pack()

    def update():
        global count
        space.step(1.5)
        bounce(space, size)
        ball_pos = ball_shape.body.position
        canvas.coords(my_ball, ball_pos.x - ball_shape.radius, HEIGHT - ball_pos.y - ball_shape.radius,
                      ball_pos.x + ball_shape.radius, HEIGHT - ball_pos.y + ball_shape.radius)
        root.after(20, update)  # Уменьшаем интервал до 20 миллисекунд для более быстрой отрисовки

        bx, by = ball_shape.body.position.x, ball_shape.body.position.y
        if ball_in_basket(bx, by, left, right, up, down):
            global hi
            if hi == 0:
                count += 1
                counter_label.config(text="Balls in basket: {}".format(count))
                hi = 1

    x = 50
    y = 50
    my_ball = canvas.create_oval(x - size, y - size, x + size, y + size, fill="red")
    update()
    root.mainloop()


if __name__ == '__main__':
    main()
