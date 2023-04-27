import binascii
import firebase_admin
from firebase_admin import credentials, db
from PIL import Image
import os
import time

from PIL import Image

# Define a function to convert a hex string to an image and save it to a specified path
def hex_to_image(hex_string, image_path):
    # Set the width and height of the image
    width = 267
    height = 178
    # Create a new image with the specified width and height
    image = Image.new("RGB", (width, height))
    # Load the pixels of the image
    pixels = image.load()
    # Split the hex string into 6-character-long color codes
    hex_string = [hex_string[i:i+6] for i in range(0, len(hex_string), 6)]
    # Initialize a variable to keep track of the index in the hex string
    hex_index = 0
    # Iterate through the rows of the image
    for y in range(height):
        # Iterate through the columns of the image
        for x in range(width):
            # Convert the color code to RGB values
            r, g, b = int(hex_string[hex_index][0:2], 16), int(hex_string[hex_index][2:4], 16), int(hex_string[hex_index][4:6], 16)
            # Set the pixel color at the current position
            pixels[x, y] = (r, g, b)
            # Increment the hex string index
            hex_index += 1
    # Save the image to the specified path
    image.save(image_path)


# Obtain the Firebase credentials from the JSON file
cred = credentials.Certificate(r"C:\Users\isaia\OneDrive\Desktop\School\Spring 2023\ECEN 403\Capstone Project\Database Connection\serviceAccountKey.json")

# Initialize the Firebase app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://iot-pet-based-tracker-database-default-rtdb.firebaseio.com/'
})

start_time = time.time()

# Get a reference to the 'Image' node in the Firebase Realtime Database
image_ref = db.reference('Image')
# Retrieve the image dictionary from the database
image_dict = image_ref.get()
# Get the hex string of the image from the dictionary
hex_str = image_dict.get('img_hex')

# Use the hex_to_image function to convert the hex string to a JPEG file and save it to the Images folder
hex_to_image(hex_str, "Images/2_pulled.jpeg")

# Calculate and print the total time taken for the operation
print("--- Total time: %s seconds ---" % (time.time() - start_time))
