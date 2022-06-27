# import PIL
from turtle import width
from PIL import Image, ImageDraw, ImageFont, ImageOps
import random
import requests

# Heart icon attribution
# https://www.flaticon.com/authors/vlad-szirka


def generate_ship_image(user1, user2):
    # Read ship image template
    # Have tested 1920x1080px and 1200x600px images.
    image = Image.open("images/Ship_Background.jpg").convert("RGBA")
    width, height = image.size
    center_x = width // 2
    center_y = height // 2

    # Open, resize, and add heart icon to background template
    heart_icon = Image.open(
        "images/heart.png").resize((width // 3, width // 3))
    heart_location = center_x - \
        heart_icon.size[0] // 2, center_y - heart_icon.size[1] // 2
    image.alpha_composite(heart_icon, heart_location)

    # Initialise first font for love percentage
    font_colour = "#000000"
    stroke_fill = "#ffffff"
    font_size = round(center_y // 3.33)
    stroke_width = round(font_size * 0.02)

    draw = ImageDraw.Draw(image)

    # Generate ship % and draw onto the background
    love_value = random.randint(0, 100)
    font = ImageFont.truetype("arial.ttf", font_size)
    draw.text((center_x, center_y), str(love_value) + "%", fill=font_colour,
              font=font, anchor="mm", align="center", stroke_width=stroke_width, stroke_fill=stroke_fill)

    # Change font settings for user names
    font_colour = "#f9595f"  # Red for names
    stroke_fill = "#000000"
    font_size = round(font_size // 1.75)
    stroke_width = round(font_size * 0.02)
    font = ImageFont.truetype("arial.ttf", font_size)

    # Set the display names and draw them onto the background
    # TODO: Grab names for users here from arguments
    name_1 = "Jackyyy"
    name_2 = "the lempika"
    draw.text((center_x, center_y - (center_y // 1.33)), name_1, fill=font_colour,
              font=font, anchor="mm", align="center", stroke_width=stroke_width, stroke_fill=stroke_fill)
    draw.text((center_x, center_y + (center_y // 1.33)), name_2, fill=font_colour,
              font=font, anchor="mm", align="center", stroke_width=stroke_width, stroke_fill=stroke_fill)

    # Get and resize the user avatars
    avatar_dims = (width // 5, width // 5)

    # TODO: Get avatar from users
    # Method 1: Using URLS
    # Method 2: Local files
    avatar_1, avatar_2 = get_avatar_using_urls("user1", "user2", avatar_dims)

    # avatar_1 = Image.open("avatar.jpg").resize(avatar_dims)
    # avatar_2 = Image.open("avatar2.webp").resize(avatar_dims)

    # Create circle mask for circle avatars. Same size as avatars
    avatar_mask = Image.new("L", avatar_dims, 0)
    draw = ImageDraw.Draw(avatar_mask)
    draw.ellipse((0, 0) + avatar_dims, fill=255)
    avatar_1 = ImageOps.fit(
        avatar_1, avatar_mask.size, centering=(0.5, 0.5))
    avatar_1.putalpha(avatar_mask)
    avatar_2 = ImageOps.fit(
        avatar_2, avatar_mask.size, centering=(0.5, 0.5))
    avatar_2.putalpha(avatar_mask)

    # Draw resized avatars onto the image
    avatar_1_location = (center_x - round((center_x // 2.5)) -
                         (avatar_dims[0]), center_y - avatar_dims[0] // 2)
    avatar_2_location = (center_x + round((center_x // 2.5)),
                         center_y - avatar_dims[0] // 2)
    image.alpha_composite(avatar_1, avatar_1_location)
    image.alpha_composite(avatar_2, avatar_2_location)

    # Save and replace the final image
    image = image.convert("RGB")
    image.save("last_ship_export.jpg")
    image.show()


def get_avatar_using_urls(user1, user2, avatar_dims):
    # TODO: Change these links here to discord user's avatar image
    r = requests.get(
        "https://avatars.githubusercontent.com/u/43399028?s=96&v=4", stream=True)
    avatar_1 = Image.open(r.raw).resize(avatar_dims)

    r = requests.get(
        "https://cdn.discordapp.com/avatars/90651365012955136/62a5d2b43aeb461f0d10d081b1e71f99.webp", stream=True)
    avatar_2 = Image.open(r.raw).resize(avatar_dims)

    return avatar_1, avatar_2


# TODO: Change these to the pinged users
generate_ship_image("user1", "user2")
