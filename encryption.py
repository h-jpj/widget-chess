#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Encryption module for Widget Chess.
Implements a simplified encryption for game state.
"""

import os
import json
import base64
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

import config

# Simplified encryption implementation
def get_encryption_key():
    """Get or create the encryption key.

    Returns:
        bytes: Encryption key
    """
    key_file = config.ENCRYPTION_KEYS_FILE

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(key_file), exist_ok=True)

    if os.path.exists(key_file):
        try:
            with open(key_file, 'r') as f:
                key_data = json.load(f)
                return base64.b64decode(key_data['key'])
        except Exception as e:
            print(f"Error loading encryption key: {e}")

    # Create a new key
    key = os.urandom(32)  # 256-bit key

    # Save the key
    try:
        with open(key_file, 'w') as f:
            json.dump({'key': base64.b64encode(key).decode('utf-8')}, f, indent=4)
    except Exception as e:
        print(f"Error saving encryption key: {e}")

    return key

def encrypt_data(plaintext):
    """Encrypt data using AES-CBC.

    Args:
        plaintext: String to encrypt

    Returns:
        dict: Encrypted data with metadata
    """
    # Get the encryption key
    key = get_encryption_key()

    # Generate a random IV
    iv = os.urandom(16)

    # Pad the plaintext
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plaintext.encode('utf-8')) + padder.finalize()

    # Encrypt the data
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    # Create a simple HMAC
    h = hashlib.sha256()
    h.update(key)
    h.update(ciphertext)
    hmac = h.digest()

    # Return the encrypted data with metadata
    return {
        'iv': base64.b64encode(iv).decode('utf-8'),
        'ciphertext': base64.b64encode(ciphertext).decode('utf-8'),
        'hmac': base64.b64encode(hmac).decode('utf-8')
    }

def decrypt_data(encrypted_data):
    """Decrypt data using AES-CBC.

    Args:
        encrypted_data: Dictionary containing encrypted data and metadata

    Returns:
        str: Decrypted plaintext
    """
    # Get the encryption key
    key = get_encryption_key()

    # Decode the encrypted data
    iv = base64.b64decode(encrypted_data['iv'])
    ciphertext = base64.b64decode(encrypted_data['ciphertext'])
    hmac = base64.b64decode(encrypted_data['hmac'])

    # Verify HMAC
    h = hashlib.sha256()
    h.update(key)
    h.update(ciphertext)
    calculated_hmac = h.digest()

    if not hmac == calculated_hmac:
        raise ValueError("HMAC verification failed. Data may have been tampered with.")

    # Decrypt the data
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    # Unpad the plaintext
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    return plaintext.decode('utf-8')
