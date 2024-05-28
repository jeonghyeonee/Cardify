import os
import re
from datetime import datetime
import piheaan as heaan
from piheaan.math import sort
from piheaan.math import approx
import math

class Heaan:
    def __init__(self, key_file_path="./keys", log_slots=15):
        self.context = heaan.make_context(heaan.ParameterPreset.FGb)
        heaan.make_bootstrappable(self.context)
        self.key_file_path = key_file_path
        self.log_slots = log_slots
        self.num_slots = 2 ** log_slots
        self.sk = None
        self.pk = None
        self.eval = None
        self.dec = None
        self.enc = None
        self.initialize()

    def initialize(self):
        """
        Initialize the HEAAN context and load or create keys.
        """
        if not os.path.exists(self.key_file_path):
            self.create_and_save_keys()
        self.load_keys()
        self.eval = heaan.HomEvaluator(self.context, self.pk)
        self.dec = heaan.Decryptor(self.context)
        self.enc = heaan.Encryptor(self.context)

    def create_and_save_keys(self):
        """
        Create and save the secret and public keys.
        """
        self.sk = heaan.SecretKey(self.context)
        os.makedirs(self.key_file_path, mode=0o775, exist_ok=True)
        self.sk.save(os.path.join(self.key_file_path, "secretkey.bin"))

        key_generator = heaan.KeyGenerator(self.context, self.sk)
        key_generator.gen_common_keys()
        key_generator.save(self.key_file_path)

    def load_keys(self):
        """
        Load the secret and public keys.
        """
        self.sk = heaan.SecretKey(self.context, os.path.join(self.key_file_path, "secretkey.bin"))
        self.pk = heaan.KeyPack(self.context, self.key_file_path)
        self.pk.load_enc_key()
        self.pk.load_mult_key()

    def feat_msg_generate(self, feat):
        """
        Generate a message from the feature array.
        """
        feat_list = feat
        feat_padding = feat_list + (self.num_slots - len(feat_list)) * [0]
        msg = heaan.Message(self.log_slots)
        for i in range(self.num_slots):
            msg[i] = feat_padding[i]
        return msg

    def encrypt(self, plaintext):
        """
        Encrypt the given plaintext.
        
        Args:
            plaintext (list): The list of plaintext values to encrypt.
            
        Returns:
            heaan.Ciphertext: The resulting ciphertext.
        """
        # Create the message
        msg = heaan.Message(self.log_slots)
        for i, num in enumerate(plaintext):
            msg[i] = num

        # Create the ciphertext
        ctxt = heaan.Ciphertext(self.context)
        self.enc.encrypt(msg, self.pk, ctxt)
        
        return ctxt
    
    def decrypt(self, ciphertext):
        """
        Decrypt the given ciphertext.
        
        Args:
            ciphertext (heaan.Ciphertext): The ciphertext to decrypt.
            
        Returns:
            list: The resulting plaintext values.
        """
        # Create the message object
        msg = heaan.Message(self.log_slots)
        
        # Decrypt
        self.dec.decrypt(ciphertext, self.sk, msg)
        
        # Convert to plaintext
        plaintext = [msg[i].real for i in range(self.num_slots)]
        
        return plaintext
    
    def division(self, divided, divider):
        """
        Perform encrypted division of 'divided' by 'divider'.
        
        Args:
            divided (heaan.Ciphertext): The dividend ciphertext.
            divider (int): The divisor value.
            
        Returns:
            heaan.Ciphertext: The quotient ciphertext.
            heaan.Ciphertext: The remainder ciphertext.
        """
        cnt = [0] * self.num_slots
        cnt_msg = heaan.Message(self.log_slots)
        for i in range(self.num_slots):
            cnt_msg[i] = cnt[i]
        cnt_ctxt = heaan.Ciphertext(self.context)

        self.enc.encrypt(cnt_msg, self.pk, cnt_ctxt)

        # For adding 1
        sig = [1] * self.num_slots

        sig_msg = heaan.Message(self.log_slots)
        for i in range(self.num_slots):
            sig_msg[i] = sig[i]
        sig_ctxt = heaan.Ciphertext(self.context)

        self.enc.encrypt(sig_msg, self.pk, sig_ctxt)

        # Encrypt divider (10)
        divider = [divider] * self.num_slots

        divider_msg = heaan.Message(self.log_slots)
        for i in range(self.num_slots):
            divider_msg[i] = divider[i]
        divider_ctxt = heaan.Ciphertext(self.context)

        self.enc.encrypt(divider_msg, self.pk, divider_ctxt)

        # Subtraction for division
        remain = heaan.Ciphertext(self.context)
        remain_msg = heaan.Message(self.log_slots)

        self.eval.sub(divided, divider_ctxt, remain)
        self.eval.add(cnt_ctxt, sig_ctxt, cnt_ctxt)
        self.dec.decrypt(remain, self.sk, remain_msg)

        while True:
            if remain_msg[0].real <= 0:
                break
            self.eval.sub(remain, divider_ctxt, remain)
            self.eval.add(cnt_ctxt, sig_ctxt, cnt_ctxt)
            self.dec.decrypt(remain, self.sk, remain_msg)
            
        return cnt_ctxt, remain
    
    def multiply(self, ctxt, factor):
        """
        Multiply the ciphertext by a given factor.
        
        Args:
            ctxt (heaan.Ciphertext): The ciphertext to multiply.
            factor (int): The factor to multiply by.
            
        Returns:
            heaan.Ciphertext: The resulting ciphertext.
        """
        result = heaan.Ciphertext(self.context)
        self.eval.mult(ctxt, factor, result)
        return result
    
    def subtract(self, ctxt1, ctxt2):
        """
        Subtract one ciphertext from another.
        
        Args:
            ctxt1 (heaan.Ciphertext): The first ciphertext.
            ctxt2 (heaan.Ciphertext): The second ciphertext.
            
        Returns:
            heaan.Ciphertext: The resulting ciphertext (ctxt1 - ctxt2).
        """
        result = heaan.Ciphertext(self.context)
        self.eval.sub(ctxt1, ctxt2, result)
        return result

    def addition(self, ctxt1, ctxt2):
        """
        Add two ciphertexts together.
        
        Args:
            ctxt1 (heaan.Ciphertext): The first ciphertext.
            ctxt2 (heaan.Ciphertext): The second ciphertext.
            
        Returns:
            heaan.Ciphertext: The resulting ciphertext (ctxt1 + ctxt2).
        """
        result = heaan.Ciphertext(self.context)
        self.eval.add(ctxt1, ctxt2, result)
        return result

    def equal_zero(self, ctxt):
        """
        Check if the ciphertext is approximately zero.
        
        Args:
            ctxt (heaan.Ciphertext): The ciphertext to check.
            
        Returns:
            bool: True if the ciphertext is approximately zero, otherwise False.
        """
        result = heaan.Ciphertext(self.context)
        approx.discrete_equal_zero(self.eval, ctxt, result)
        return result

    def left_rotate(self, ctxt, rotation_amount):
        """
        Rotate the ciphertext to the left by a given amount.
        
        Args:
            ctxt (heaan.Ciphertext): The ciphertext to rotate.
            rotation_amount (int): The amount to rotate.
            
        Returns:
            heaan.Ciphertext: The rotated ciphertext.
        """
        result = heaan.Ciphertext(self.context)
        self.eval.left_rotate(ctxt, rotation_amount, result)
        return result

    def right_rotate(self, ctxt, rotation_amount):
        """
        Rotate the ciphertext to the right.

        Args:
            ctxt (heaan.Ciphertext): The ciphertext to rotate.
            rotation_amount (int): The amount to rotate.

        Returns:
            heaan.Ciphertext: The rotated ciphertext.
        """
        result = heaan.Ciphertext(self.context)
        self.eval.right_rotate(ctxt, rotation_amount, result)
        return result
        
    def comparing(self, ctxt1, ctxt2):
        """
        Compare two ciphertexts to determine the relative size of their values in each slot.

        Args:
            ctxt1 (heaan.Ciphertext): The first ciphertext to compare.
            ctxt2 (heaan.Ciphertext): The second ciphertext to compare.

        Returns:
            float: Returns 1 if the value in each slot of ciphertext 1 is greater than that in ciphertext 2,
                0 if it is less, and 0.5 if they are equal.
        """
        result = heaan.Ciphertext(self.context)
        approx.compare(self.eval, ctxt1, ctxt2, result)
        return result

