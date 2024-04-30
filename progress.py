import piheaan as heaan
from piheaan.math import sort
from piheaan.math import approx # for piheaan math function
import math
import numpy as np
import pandas as pd
import os
import re
from datetime import datetime

# set parameter
params = heaan.ParameterPreset.FGb
context = heaan.make_context(params) # context has paramter information
heaan.make_bootstrappable(context) # make parameter bootstrapable

# create and save keys
key_file_path = "./keys"
sk = heaan.SecretKey(context) # create secret key
os.makedirs(key_file_path, mode=0o775, exist_ok=True)
sk.save(key_file_path+"/secretkey.bin") # save secret key


key_generator = heaan.KeyGenerator(context, sk) # create public key
key_generator.gen_common_keys()
key_generator.save(key_file_path+"/") # save public key

# load secret key and public key
# When a key is created, it can be used again to save a new key without creating a new one
key_file_path = "./keys"

sk = heaan.SecretKey(context,key_file_path+"/secretkey.bin") # load secret key
pk = heaan.KeyPack(context, key_file_path+"/") # load public key
pk.load_enc_key()
pk.load_mult_key()

eval = heaan.HomEvaluator(context,pk) # to load piheaan basic function
dec = heaan.Decryptor(context) # for decrypt
enc = heaan.Encryptor(context) # for encrypt

log_slots = 15
num_slots = 2**log_slots

def validate_card_number(card_number):
    # 카드 번호 패턴 정의
    pattern = re.compile(r'^\d{4}-\d{4}-\d{4}-\d{4}$')

    # 입력된 카드 번호가 패턴과 일치하는지 확인
    if not re.match(pattern, card_number):
        return False
    else:
        return True

# 사용자로부터 카드 번호 입력 받기
card_number = input("카드 번호를 입력하세요 (형식: xxxx-xxxx-xxxx-xxxx): ")

def validate_expiry_date(expiry_date):
    # 유효기간 패턴 정의 (mm/yy)
    pattern = re.compile(r'^\d{2}/\d{2}$')

    # 입력된 유효기간이 패턴과 일치하는지 확인
    if not re.match(pattern, expiry_date):
        return False
    else:
        return True

# 사용자로부터 유효기간 입력 받기
expiry_date = input("카드 유효기간을 mm/yy 형태로 입력하세요: ")

# 입력된 카드 번호의 유효성 검사

if validate_card_number(card_number):
    print("입력한 카드 번호:", card_number)
else:
    print("올바른 형식의 카드 번호를 입력하세요.")

# 입력된 유효기간의 유효성 검사
if validate_expiry_date(expiry_date):
    print("입력한 유효기간:", expiry_date)
else:
    print("올바른 형식의 유효기간을 입력하세요.")


number_list = [int(num) for num in card_number if num.isdigit()]
# print(number_list)

# 입력된 문자열을 한 글자씩 분리하여 각 자리수를 리스트에 저장합니다.
expiry_list = [int(digit) for digit in expiry_date if digit.isdigit()]

# print(expiry_list)

card_num = number_list + [0]*(num_slots-16)
# print(len(card_num))
# print(card_num)

# 카드 번호 암호화
card_num_msg = heaan.Message(log_slots)
for i in range(num_slots):
    card_num_msg[i] = card_num[i]
card_num_ctxt = heaan.Ciphertext(context)

enc.encrypt(card_num_msg, pk, card_num_ctxt)

# 유효기간 암호화
result_list = [expiry_list[0] * 10,
               expiry_list[1] * 1,
               expiry_list[2] * 1000,
               expiry_list[3] * 100]
# print(result_list)
valid_date = sum(result_list)

valid_thru = [valid_date] + [0] * (num_slots-1)
# print(len(valid_thru))

valid_thru_msg = heaan.Message(log_slots)
for i in range(num_slots):
    valid_thru_msg[i] = valid_thru[i]
valid_thru_ctxt = heaan.Ciphertext(context)

enc.encrypt(valid_thru_msg, pk, valid_thru_ctxt)


# print(valid_date)

# Master, Visa, Domestic Card Brand 확인 (1)
# 암호문 3개, 뺄셈 3번, equalzero 3번
visa_num = [4] + [0]*(num_slots-1)
master_num = [5] + [0]*(num_slots-1)
domestic_num = [9] + [0]*(num_slots-1)

visa_num_msg = heaan.Message(log_slots)
for i in range(num_slots):
    visa_num_msg[i] = visa_num[i]
visa_num_ctxt = heaan.Ciphertext(context)
enc.encrypt(visa_num_msg, pk, visa_num_ctxt)

master_num_msg = heaan.Message(log_slots)
for i in range(num_slots):
    master_num_msg[i] = master_num[i]
master_num_ctxt = heaan.Ciphertext(context)
enc.encrypt(master_num_msg, pk, master_num_ctxt)

domestic_num_msg = heaan.Message(log_slots)
for i in range(num_slots):
    domestic_num_msg[i] = domestic_num[i]
domestic_num_ctxt = heaan.Ciphertext(context)
enc.encrypt(domestic_num_msg, pk, domestic_num_ctxt)

# Check the Visa Card
result_sub1 = heaan.Ciphertext(context)

eval.sub(card_num_ctxt,visa_num_ctxt,result_sub1)

result_sub_message1 = heaan.Message(log_slots)
dec.decrypt(result_sub1, sk, result_sub_message1)

# print("(ciphertext + message) : ", result_sub_message1)

# Check the Master Card
result_sub2 = heaan.Ciphertext(context)

eval.sub(card_num_ctxt,master_num_ctxt,result_sub2)

result_sub_message2 = heaan.Message(log_slots)
dec.decrypt(result_sub2, sk, result_sub_message2)

# print("(ciphertext + message) : ", result_sub_message2)

# Check the Domestic Card
result_sub3 = heaan.Ciphertext(context)

eval.sub(card_num_ctxt,domestic_num_ctxt,result_sub3)

result_sub_message3 = heaan.Message(log_slots)
dec.decrypt(result_sub3, sk, result_sub_message3)

# print("(ciphertext + message) : ", result_sub_message3)

# using equal zero
# Visa Card
result_discrete_equal_zero1 = heaan.Ciphertext(context)
approx.discrete_equal_zero(eval, result_sub1, result_discrete_equal_zero1)

result_discrete_equal_zero_message1 = heaan.Message(log_slots)

dec.decrypt(result_discrete_equal_zero1, sk, result_discrete_equal_zero_message1)
# print(result_discrete_equal_zero_message1)

# Master Card
result_discrete_equal_zero2 = heaan.Ciphertext(context)
approx.discrete_equal_zero(eval, result_sub2, result_discrete_equal_zero2)

result_discrete_equal_zero_message2 = heaan.Message(log_slots)

dec.decrypt(result_discrete_equal_zero2, sk, result_discrete_equal_zero_message2)
# print(result_discrete_equal_zero_message2)

# Domestic Card
result_discrete_equal_zero3 = heaan.Ciphertext(context)
approx.discrete_equal_zero(eval, result_sub3, result_discrete_equal_zero3)

result_discrete_equal_zero_message3 = heaan.Message(log_slots)

dec.decrypt(result_discrete_equal_zero3, sk, result_discrete_equal_zero_message3)
# print(result_discrete_equal_zero_message3)

# Result
print("=======================================================================================")
print("Method 1")
if round(result_discrete_equal_zero_message1[0].real, 2) == 1:
    print("visa")
elif round(result_discrete_equal_zero_message2[0].real, 2) == 1:
    print("master")
elif round(result_discrete_equal_zero_message3[0].real, 2) == 1:
    print("domestic")
else:
    print("잘못된 카드 번호입니다. 다시 입력하세요.")


# Master, Visa, Domestic Card Brand 확인 (2)
# 암호문 1개, Rotation, 뺄셈
bin_num = [4] + [0]*(15) + [5] + [0]*(15) + [9] + [0]*(num_slots-33)

bin_num_msg = heaan.Message(log_slots)
for i in range(num_slots):
    bin_num_msg[i] = bin_num[i]
bin_num_ctxt = heaan.Ciphertext(context)
enc.encrypt(bin_num_msg, pk, bin_num_ctxt)

# Visa Card
result_sub1 = heaan.Ciphertext(context)

eval.sub(card_num_ctxt,bin_num_ctxt,result_sub1)

result_sub_message1 = heaan.Message(log_slots)
dec.decrypt(result_sub1, sk, result_sub_message1)

# print("(ciphertext + message) : ", result_sub_message1)

# Rotating 1: To check the Master Card
result_left_rot1 = heaan.Ciphertext(context)

# left_rotate
eval.left_rotate(bin_num_ctxt,16, result_left_rot1)

result_left_rot_message1 = heaan.Message(log_slots)
dec.decrypt(result_left_rot1, sk, result_left_rot_message1)
# print("left_rotate : ", result_left_rot_message1)
# print()

result_sub2 = heaan.Ciphertext(context)

eval.sub(card_num_ctxt,result_left_rot1,result_sub2)

result_sub_message2 = heaan.Message(log_slots)
dec.decrypt(result_sub1, sk, result_sub_message2)

# print("(ciphertext + message) : ", result_sub_message2)

# Rotating 2: To check the domestic card
result_left_rot2 = heaan.Ciphertext(context)

# left_rotate
eval.left_rotate(bin_num_ctxt,32, result_left_rot2)

result_left_rot_message2 = heaan.Message(log_slots)
dec.decrypt(result_left_rot2, sk, result_left_rot_message2)
# print("left_rotate : ", result_left_rot_message2)
# print()

result_sub3 = heaan.Ciphertext(context)

eval.sub(card_num_ctxt,result_left_rot2,result_sub3)

result_sub_message3 = heaan.Message(log_slots)
dec.decrypt(result_sub2, sk, result_sub_message2)

# print("(ciphertext + message) : ", result_sub_message3)

# equal zero
# visa Card
result_discrete_equal_zero1 = heaan.Ciphertext(context)
approx.discrete_equal_zero(eval, result_sub1, result_discrete_equal_zero1)

result_discrete_equal_zero_message1 = heaan.Message(log_slots)

dec.decrypt(result_discrete_equal_zero1, sk, result_discrete_equal_zero_message1)
# print(result_discrete_equal_zero_message1)

# Master Card
result_discrete_equal_zero2 = heaan.Ciphertext(context)
approx.discrete_equal_zero(eval, result_sub2, result_discrete_equal_zero2)

result_discrete_equal_zero_message2 = heaan.Message(log_slots)

dec.decrypt(result_discrete_equal_zero2, sk, result_discrete_equal_zero_message2)
# print(result_discrete_equal_zero_message2)

# Domestic
result_discrete_equal_zero3 = heaan.Ciphertext(context)
approx.discrete_equal_zero(eval, result_sub3, result_discrete_equal_zero3)

result_discrete_equal_zero_message3 = heaan.Message(log_slots)

dec.decrypt(result_discrete_equal_zero3, sk, result_discrete_equal_zero_message3)
# print(result_discrete_equal_zero_message3)

# Result
# print("-------------------------------------------------------------------------------------")
print("Method 2")
if round(result_discrete_equal_zero_message1[0].real, 2) == 1:
    print("visa")
elif round(result_discrete_equal_zero_message2[0].real, 2) == 1:
    print("master")
elif round(result_discrete_equal_zero_message3[0].real, 2) == 1:
    print("domestic")
else:
    print("잘못된 카드 번호입니다. 다시 입력하세요.")

# 카드 유효기간 검증
date = [int(datetime.today().strftime("%y%m"))] + [0]*(num_slots-1)

# print(date)
# print(valid_thru)

date_num_msg = heaan.Message(log_slots)
for i in range(num_slots):
    date_num_msg[i] = date[i]
date_num_ctxt = heaan.Ciphertext(context)
enc.encrypt(date_num_msg, pk, date_num_ctxt)

result_sub1 = heaan.Ciphertext(context)

eval.sub(valid_thru_ctxt,date_num_ctxt,result_sub1)

result_sub_message1 = heaan.Message(log_slots)
dec.decrypt(result_sub1, sk, result_sub_message1)

# print("(ciphertext + message) : ", result_sub_message1)

if round(result_sub_message1[0].real, 2) >= 0:
  print("valid")
else:
  print("Not Valid")