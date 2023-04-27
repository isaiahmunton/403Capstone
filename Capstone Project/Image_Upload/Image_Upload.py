import binascii
import firebase_admin
from firebase_admin import credentials, db
from PIL import Image
import time

# Define a function to convert an image to a hex string
def image_to_hex(image_path):
    # Open the image at the specified path
    with Image.open(image_path) as image:
        # Get the width and height of the image
        width, height = image.size
        # Check if the image size is 267x178, otherwise raise a ValueError
        if width != 267 or height != 178:
            raise ValueError("Image size is not 267x178")
        # Initialize an empty hex string
        hex_string = ""
        # Load the pixels of the image
        pixels = image.load()
        # Iterate through the rows of the image
        for y in range(height):
            # Iterate through the columns of the image
            for x in range(width):
                # Get the RGB values of the pixel at the current position
                r, g, b = pixels[x, y]
                # Append the RGB values as a hex string to the hex_string variable
                hex_string += f"{r:02x}{g:02x}{b:02x}"
        # Return the hex string
        return hex_string

# Obtain the Firebase credentials from the JSON file
cred = credentials.Certificate(r"C:\Users\isaia\OneDrive\Desktop\School\Spring 2023\ECEN 403\Capstone Project\Database Connection\serviceAccountKey.json")

# Initialize the Firebase app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://iot-pet-based-tracker-database-default-rtdb.firebaseio.com/'
})

start_time = time.time()

# Use the image_to_hex function to convert the image at the specified path to a hex string
hex_str = image_to_hex("Images/2.jpeg")

# Get a reference to the 'Image' node in the Firebase Realtime Database
image_ref = db.reference('Image')
# Set the hex-encoded image data in the database under the 'img_hex' key
image_ref.set({
    'img_hex': hex_str
})

# Calculate and print the total time taken for the operation
print("--- Total time: %s seconds ---" % (time.time() - start_time))
