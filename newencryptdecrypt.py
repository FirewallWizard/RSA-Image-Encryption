import tkinter as tk
from tkinter import filedialog
from PIL import Image
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Generate RSA keys
key = RSA.generate(2048)
private_key = key.export_key()
public_key = key.publickey().export_key()

# Define encryption and decryption functions
def encrypt_image(path):
    # Load public key
    public_key = RSA.import_key(open('public_key.pem').read())

    # Load image file and convert to byte array
    with open(path, 'rb') as f:
        image_data = f.read()
    image_data = bytearray(image_data)

    # Encrypt the byte array using RSA encryption
    block_size = public_key.size_in_bytes() - 42
    cipher = PKCS1_OAEP.new(public_key)
    encrypted_blocks = []
    for i in range(0, len(image_data), block_size):
        block = image_data[i:i+block_size]
        encrypted_block = cipher.encrypt(block)
        encrypted_blocks.append(encrypted_block)
    encrypted_data = b''.join(encrypted_blocks)

    # Save the encrypted data to a file
    with open('encrypted_image.jpg', 'wb') as f:
        f.write(encrypted_data)

def decrypt_image(path):
    # Load private key
    private_key = RSA.import_key(open('private_key.pem').read())

    # Load encrypted image file and convert to byte array
    with open(path, 'rb') as f:
        encrypted_data = f.read()
    encrypted_data = bytearray(encrypted_data)

    # Decrypt the byte array using RSA decryption
    block_size = private_key.size_in_bytes()
    cipher = PKCS1_OAEP.new(private_key)
    decrypted_blocks = []
    for i in range(0, len(encrypted_data), block_size):
        block = encrypted_data[i:i+block_size]
        decrypted_block = cipher.decrypt(block)
        decrypted_blocks.append(decrypted_block)
    decrypted_data = b''.join(decrypted_blocks)

    # Save the decrypted data to a file
    with open('decrypted_image.jpg', 'wb') as f:
        f.write(decrypted_data)

# Create the root window
root = tk.Tk()
root.title("Image Encryption and Decryption with RSA")

# Add a label widget
label = tk.Label(root, text="Select an image to encrypt or decrypt:")
label.pack()

# Add a button widget to select an image file
def select_file():
    path = filedialog.askopenfilename()
    file_entry.delete(0, tk.END)
    file_entry.insert(0, path)
file_button = tk.Button(root, text="Select file", command=select_file)
file_button.pack()

# Add an entry widget to display the selected file path
file_entry = tk.Entry(root)
file_entry.pack()

# Add a button widget to encrypt the selected image file
def encrypt_file():
    path = file_entry.get()
    encrypt_image(path)
    label.config(text="Image is encrypted!")
encrypt_button = tk.Button(root, text="Encrypt", command=encrypt_file)
encrypt_button.pack()

# Add a button widget to decrypt the selected image file
def decrypt_file():
    path = file_entry.get()
    decrypt_image(path)
    label.config(text="Image is decrypted!")
decrypt_button = tk.Button(root, text="Decrypt", command=decrypt_file)
decrypt_button.pack()

# Run the main event loop
root.mainloop()