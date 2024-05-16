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
        if not os.path.exists(self.key_file_path):
            self.create_and_save_keys()
        self.load_keys()
        self.eval = heaan.HomEvaluator(self.context, self.pk)
        self.dec = heaan.Decryptor(self.context)
        self.enc = heaan.Encryptor(self.context)

    def create_and_save_keys(self):
        self.sk = heaan.SecretKey(self.context)
        os.makedirs(self.key_file_path, mode=0o775, exist_ok=True)
        self.sk.save(os.path.join(self.key_file_path, "secretkey.bin"))

        key_generator = heaan.KeyGenerator(self.context, self.sk)
        key_generator.gen_common_keys()
        key_generator.save(self.key_file_path)

    def load_keys(self):
        self.sk = heaan.SecretKey(self.context, os.path.join(self.key_file_path, "secretkey.bin"))
        self.pk = heaan.KeyPack(self.context, self.key_file_path)
        self.pk.load_enc_key()
        self.pk.load_mult_key()

    def preprocess_card_number(self, card_number):
        number_list = [int(num) for num in card_number if num.isdigit()]
        card_num = number_list + [0] * (self.num_slots - len(number_list))
        card_num_msg = heaan.Message(self.log_slots)
        for i in range(self.num_slots):
            card_num_msg[i] = card_num[i]
        card_num_ctxt = heaan.Ciphertext(self.context)
        self.enc.encrypt(card_num_msg, self.pk, card_num_ctxt)
        return card_num_ctxt

    def preprocess_expiry_date(self, expiry_date):
        expiry_list = [int(digit) for digit in expiry_date if digit.isdigit()]
        result_list = [expiry_list[0] * 10, expiry_list[1] * 1, expiry_list[2] * 1000, expiry_list[3] * 100]
        valid_date = sum(result_list)
        valid_thru = [valid_date] + [0] * (self.num_slots - 1)
        valid_thru_msg = heaan.Message(self.log_slots)
        for i in range(self.num_slots):
            valid_thru_msg[i] = valid_thru[i]
        valid_thru_ctxt = heaan.Ciphertext(self.context)
        self.enc.encrypt(valid_thru_msg, self.pk, valid_thru_ctxt)
        return valid_thru_ctxt

    def validate_card_number(self, card_number):
        pattern = re.compile(r'^\d{4}-\d{4}-\d{4}-\d{4}$')
        return bool(re.match(pattern, card_number))

    def validate_expiry_date(self, expiry_date):
        pattern = re.compile(r'^\d{2}/\d{2}$')
        return bool(re.match(pattern, expiry_date))

    def decrypt_result(self, ctxt):
        result_message = heaan.Message(self.log_slots)
        self.dec.decrypt(ctxt, self.sk, result_message)
        return result_message

    def check_card_brand(self, card_num_ctxt):
        visa_num = [4] + [0] * (self.num_slots - 1)
        master_num = [5] + [0] * (self.num_slots - 1)
        domestic_num = [9] + [0] * (self.num_slots - 1)

        visa_num_msg = heaan.Message(self.log_slots)
        master_num_msg = heaan.Message(self.log_slots)
        domestic_num_msg = heaan.Message(self.log_slots)

        for i in range(self.num_slots):
            visa_num_msg[i] = visa_num[i]
            master_num_msg[i] = master_num[i]
            domestic_num_msg[i] = domestic_num[i]

        visa_num_ctxt = heaan.Ciphertext(self.context)
        master_num_ctxt = heaan.Ciphertext(self.context)
        domestic_num_ctxt = heaan.Ciphertext(self.context)

        self.enc.encrypt(visa_num_msg, self.pk, visa_num_ctxt)
        self.enc.encrypt(master_num_msg, self.pk, master_num_ctxt)
        self.enc.encrypt(domestic_num_msg, self.pk, domestic_num_ctxt)

        result_sub1 = heaan.Ciphertext(self.context)
        result_sub2 = heaan.Ciphertext(self.context)
        result_sub3 = heaan.Ciphertext(self.context)

        self.eval.sub(card_num_ctxt, visa_num_ctxt, result_sub1)
        self.eval.sub(card_num_ctxt, master_num_ctxt, result_sub2)
        self.eval.sub(card_num_ctxt, domestic_num_ctxt, result_sub3)

        result_discrete_equal_zero1 = heaan.Ciphertext(self.context)
        result_discrete_equal_zero2 = heaan.Ciphertext(self.context)
        result_discrete_equal_zero3 = heaan.Ciphertext
    
    def feat_msg_generate(self, feat):
      # Generate a message from the feature array
      feat_list = feat
      feat_padding = feat_list + (self.num_slots-len(feat_list))*[0]
      msg = heaan.Message(self.log_slots)
      for i in range(self.num_slots):
          msg[i] = feat_padding[i]

      return msg

    def encrypt(self, plaintext):
        """
        주어진 평문을 암호화합니다.
        
        Args:
            plaintext (list): 암호화할 평문의 리스트
            
        Returns:
            heaan.Ciphertext: 암호문
        """
        # 메시지 생성
        msg = heaan.Message(self.log_slots)
        for i, num in enumerate(plaintext):
            msg[i] = num

        # 암호문 생성
        ctxt = heaan.Ciphertext(self.context)
        self.enc.encrypt(msg, self.pk, ctxt)
        
        return ctxt
    
    def decrypt(self, ciphertext):
        """
        주어진 암호문을 복호화합니다.
        
        Args:
            ciphertext (heaan.Ciphertext): 복호화할 암호문
            
        Returns:
            list: 평문의 리스트
        """
        # 메시지 객체 생성
        msg = heaan.Message(self.log_slots)
        
        # 복호화
        self.dec.decrypt(ciphertext, self.sk, msg)
        
        # 평문으로 변환
        plaintext = [msg[i].real for i in range(self.num_slots)]
        
        return plaintext
