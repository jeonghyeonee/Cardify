from heaan_utils import Heaan
import time
from card_validity import check_card_brand_method1, check_card_brand_method2, check_card_brand_method3

he = Heaan()

def measure_time(func, *args):
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    return result, end_time - start_time

def test_efficiency():
    times = {}
    for brand, ctxt in encrypted_test_cards.items():
        method1_times = []
        method2_times = []
        method3_times = []
        cnt = 0
        for _ in range(100):
            cnt += 1
            print(brand+" cnt", cnt)
            _, time1 = measure_time(check_card_brand_method1, ctxt)
            _, time2 = measure_time(check_card_brand_method2, ctxt)
            _, time3 = measure_time(check_card_brand_method3, ctxt)
            method1_times.append(time1)
            method2_times.append(time2)
            method3_times.append(time3)
        avg_time1 = sum(method1_times) / len(method1_times)
        avg_time2 = sum(method2_times) / len(method2_times)
        avg_time3 = sum(method3_times) / len(method3_times)
        times[brand] = (avg_time1, avg_time2, avg_time3)
    return times

# Sample card numbers for testing
# Assuming ctxt values are encrypted representations of these numbers
# The actual ctxt values should be created by using he.encrypt() on these numbers
test_card_numbers = {
    'visa': [4] + [1]*15,
    'master': [5] + [2]*15,
    'domestic': [9] + [3]*15,
    'invalid': [0] + [4]*15
}

# Encrypt test card numbers
encrypted_test_cards = {k: he.encrypt(he.feat_msg_generate(v)) for k, v in test_card_numbers.items()}

efficiency_results = test_efficiency()
for card, times in efficiency_results.items():
    print(f"Card: {card}, \nMethod1 Average Time: {times[0]}, \nMethod2 Average Time: {times[1]}, \nMethod3 Average Time: {times[2]}")
