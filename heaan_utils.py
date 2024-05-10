import piheaan as heaan
from piheaan.math import sort
from piheaan.math import approx # for piheaan math function
import os
import math


class Heaan:
    def __init__(self) -> None:
        # set parameter
        self.params = heaan.ParameterPreset.FGb
        # context has paramter information
        self.context = heaan.make_context(self.params)
        self.key_file_path = "./keys"
        self.eval = None
        self.dec = None
        self.enc = None
        self.sk = None
        self.pk = None
        self.log_slots = 15
        self.num_slots = 2**self.log_slots


    def heaan_initilize(self):
        # log_slots is used for the number of slots per ciphertext
            # It depends on the parameter used (ParameterPreset)
            # The number '15' is the value for maximum number of slots,
            # but you can also use a smaller number (ex. 2, 3, 5, 7 ...)
            # The actual number of slots in the ciphertext is calculated as below.

        
        heaan.make_bootstrappable(self.context) # make parameter bootstrapable

        # # create and save secret keys
        # self.sk = heaan.SecretKey(self.context) # create secret key

        # # create and save public keys
        # key_generator = heaan.KeyGenerator(self.context, self.sk) # create public key
        # key_generator.gen_common_keys()
        # key_generator.save(self.key_file_path+"/") # save public key
        
        # load secret key and public key
        # When a key is created, it can be used again to save a new key without creating a new one
        self.sk = heaan.SecretKey(self.context, self.key_file_path+"/secretkey.bin") # load secret key
        self.pk = heaan.KeyPack(self.context, self.key_file_path+"/") # load public key
        self.pk.load_enc_key()
        self.pk.load_mult_key()
        # Create evaluators and decryptor
        self.eval = heaan.HomEvaluator(self.context, self.pk) # to load piheaan basic function
        self.dec = heaan.Decryptor(self.context) # for self.decrypt
        self.enc = heaan.Encryptor(self.context) # for self.encrypt

        ctxt1 = heaan.Ciphertext(self.context)
        ctxt2 = heaan.Ciphertext(self.context)

        return ctxt1, ctxt2
      

    def encrypt(self, msg, ctxt):
        self.enc.encrypt(msg, self.pk, ctxt)


    def decrypt(self, msg, ctxt):
        # Decrypt the ciphertext using the secret key
        self.dec.decrypt(msg, self.sk, ctxt)

