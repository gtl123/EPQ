import time
from turtle import Turtle, Screen, colormode, update
from PIL import Image


# Function to get the color of each pixel
def get_pixel_color(image_path, size=(100, 100)):
    # Open the image
    with Image.open(image_path) as img:
        # Resize the image if it's too large
        img = img.resize(tuple(size))  # Example resize, adjust as needed

        # Get the size of the image
        width, height = img.size

        # Create a list to store the colors
        colors = [(0, 0, 0)]
        meta = [0]

        # Go through each pixel
        for y in range(height):
            for x in range(width):
                # Get the color of the pixel (excluding the alpha channel if present)
                color = img.getpixel((x, y))[:3]
                # Append the color to the list
                if color == colors[-1]:
                    meta[-1] += 1
                else:
                    meta.append(1)
                    colors.append(color)

        return colors, width, height, meta


# Function to draw pixels with Turtle
def draw_pixels(colors, width, height, skip, meta):

    # Create a turtle object
    pixel_turtle = Turtle()
    pixel_turtle.speed('fastest')
    # Draw each pixel
    pixel_index = 1
    ox, oy = (0 % width), (height - (0 // width)-1)
    for index in range(0, len(colors), skip):
        pixel_index += meta[index]
        # Calculate the position
        x = pixel_index % width
        y = height - (pixel_index // width)-1 # Subtract y from height to flip the image
        # Move the turtle to the position
        if y == oy:
            pixel_turtle.pencolor(colors[index])
            pixel_turtle.goto(x, y)
        else:
            pixel_turtle.pencolor(colors[index])
            pixel_turtle.goto(ox+1, oy)
            for i in range((y-oy)-1):
                pixel_turtle.goto(0, oy+i)
                pixel_turtle.goto(width, oy+i)
            pixel_turtle.goto(0, y-oy)
            pixel_turtle.goto(x, y)
        ox, oy = x, y

    # Hide the turtle cursor
    pixel_turtle.hideturtle()
    # Update the screen once after all drawing commands
    update()


# Set up the screen
screen = Screen()
colormode(255)
# Turn off the animation and set the tracer to 0
screen.tracer(0, 0)
# Replace 'path_to_image.png' with your image file path
image_path = 'water.bmp'
colors, img_width, img_height, meta = get_pixel_color(image_path, (50, 50))
print("PRE TEX LOAD COMPLETE")
t = time.process_time_ns()
draw_pixels(colors, img_width, img_height, 1, meta)
print(f"Process took {(time.process_time_ns()-t)/1000000}ms")
# Keep the window open
screen.mainloop()