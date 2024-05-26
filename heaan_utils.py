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
    
    def division(self, divided, divider):
        cnt = [0] * self.num_slots
        cnt_msg = heaan.Message(self.log_slots)
        for i in range(self.num_slots):
            cnt_msg[i] = cnt[i]
        cnt_ctxt = heaan.Ciphertext(self.context)

        self.enc.encrypt(cnt_msg, self.pk, cnt_ctxt)

        # 1을 더해주기 위함
        sig = [1] * self.num_slots

        sig_msg = heaan.Message(self.log_slots)
        for i in range(self.num_slots):
            sig_msg[i] = sig[i]
        sig_ctxt = heaan.Ciphertext(self.context)

        self.enc.encrypt(sig_msg, self.pk, sig_ctxt)

        # divider(10) encryption
        divider = [divider] * self.num_slots

        divider_msg = heaan.Message(self.log_slots)
        for i in range(self.num_slots):
            divider_msg[i] = divider[i]
        divider_ctxt = heaan.Ciphertext(self.context)

        self.enc.encrypt(divider_msg, self.pk, divider_ctxt)

        # 나눗셈 연산을 위한 빼기
        # 나머지 선언
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

            # print("in while remain", remain)
            # self.dec.decrypt(cnt_ctxt, self.sk, cnt_msg)
            # self.dec.decrypt(divided_list, self.sk, divided_msg)
            # print("utils remain:", remain)
            
        return cnt_ctxt, remain
    

    def multiply(self, ctxt, factor):
        """
        암호문을 주어진 상수로 곱합니다.

        Args:
            ctxt (heaan.Ciphertext): 곱할 암호문
            factor (int): 곱할 상수

        Returns:
            heaan.Ciphertext: 곱셈 결과 암호문
        """
        result = heaan.Ciphertext(self.context)
        self.eval.mult(ctxt, factor, result)

        return result
    
    def subtract(self, ctxt1, ctxt2):
        """
        주어진 두 암호문을 뺀 결과를 반환합니다.
        
        Args:
            ctxt1 (heaan.Ciphertext): 암호문 1
            ctxt2 (heaan.Ciphertext): 암호문 2
            
        Returns:
            heaan.Ciphertext: ctxt1 - ctxt2의 결과 암호문
        """
        result = heaan.Ciphertext(self.context)
        self.eval.sub(ctxt1, ctxt2, result)
        return result

    def addition(self, ctxt1, ctxt2):
        """
        주어진 두 암호문을 더한 결과를 반환합니다.
        
        Args:
            context (heaan.Context): HEAAN 암호 시스템의 컨텍스트
            ctxt1 (heaan.Ciphertext): 암호문 1
            ctxt2 (heaan.Ciphertext): 암호문 2
            
        Returns:
            heaan.Ciphertext: ctxt1 + ctxt2의 결과 암호문
        """
        result = heaan.Ciphertext(self.context)
        self.eval.add(ctxt1, ctxt2, result)
        return result

    def equal_zero(self, ctxt):
        """
        암호문이 0에 근접하는지 확인합니다.

        Args:
            context (piheaan.Context): 암호 연산에 필요한 맥락 정보가 포함된 객체
            evaluator (piheaan.HomEvaluator): 암호 연산을 수행하는 evaluator 객체
            ciphertext (piheaan.Ciphertext): 확인할 암호문

        Returns:
            bool: 암호문이 0에 근접하면 True, 그렇지 않으면 False
        """
        result = heaan.Ciphertext(self.context)
        
        approx.discrete_equal_zero(self.eval, ctxt, result)
        
        return result

    def left_rotate(self, ctxt, rotation_amount):
        """
        암호문을 왼쪽으로 회전합니다.

        Args:
            ctxt (piheaan.Ciphertext): 회전할 암호문
            rotation_amount (int): 회전할 양

        Returns:
            piheaan.Ciphertext: 왼쪽으로 회전된 암호문
        """
        result = heaan.Ciphertext(self.context)
        self.eval.left_rotate(ctxt, rotation_amount, result)
        return result

    def right_rotate(self, ctxt, rotation_amount):
        """
        암호문을 오른쪽으로 회전합니다.

        Args:
            ctxt (piheaan.Ciphertext): 회전할 암호문
            rotation_amount (int): 회전할 양

        Returns:
            piheaan.Ciphertext: 오른쪽으로 회전된 암호문
        """
        result = heaan.Ciphertext(self.context)
        self.eval.right_rotate(ctxt, rotation_amount, result)
        return result
    
    def comparing(self, ctxt1, ctxt2):
        """
        두 개의 암호문을 비교하여 각 슬롯의 값이 크기를 비교합니다.

        Args:
            ctxt1 (piheaan.Ciphertext): 비교할 암호문 1
            ctxt2 (piheaan.Ciphertext): 비교할 암호문 2

        Returns:
            float: 암호문 1의 각 슬롯의 값이 암호문 2의 각 슬롯의 값보다 크면 1, 작으면 0, 동일하면 0.5를 반환합니다.
        """
        result = heaan.Ciphertext(self.context)
        approx.compare(self.eval, ctxt1, ctxt2, result)
        return result

