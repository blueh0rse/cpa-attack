import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt
from anthony.aes import sub_bytes, add_round_key
from scipy.stats import pearsonr
from multiprocessing import Pool

def hamming_weight(n):
    count = 0
    while n:
        count += n & 1
        n >>= 1
    return count

def calc_weights():
    for key_guess in range(256):
        key_guess_matrix = np.full((4, 4), key_guess, dtype=np.uint8)
        for tnum, in_data in enumerate(plaintexts):
            in_matrix = np.asarray(in_data, dtype=np.uint8).reshape(4, 4)

            added_key = add_round_key(in_matrix, key_guess_matrix)
            sub_out = sub_bytes(added_key, False).flatten()

            for byte_index in range(sub_out.shape[0]):
                all_hamming_weights_per_box2[tnum][key_guess][byte_index] = hamming_weights[sub_out[byte_index]]

def multi(box: int):
    print(f'Started working on box {box}', flush=True)
    maxes = np.zeros(256, dtype=np.float64)
    for guess in range(256):
        guess_box_weights = all_hamming_weights_per_box2[:, guess, box]
        WxH = (all_traces[box].T * guess_box_weights).T
        EWxH = np.sum(WxH, axis=0)

        Ew = np.sum(all_traces[box], axis=0) # constant

        Eh = np.sum(guess_box_weights)

        Ew2 = np.sum(np.square(all_traces[box]), axis=0) # constant
        Ew_squared = np.square(Ew) # constant

        Eh2 = np.sum(np.square(guess_box_weights), axis=0)
        Eh_squared = np.square(Eh)

        top = (150 * EWxH) - (Eh * Ew)
        bottom = np.sqrt((150 * Ew2) - Ew_squared) * np.sqrt((150 * Eh2) - Eh_squared)
        maxes[guess] = np.max(top / bottom)
    return box, maxes

if __name__ == '__main__':
    workdir = "data/dataset1"
    num_traces = 150
    num_samples = 50000
    num_key_bytes = 16

    # all_traces = np.zeros((num_traces, num_samples*16), dtype=np.float64)
    all_traces = np.zeros((16, 150, 50000), dtype=np.float64)

    # Read the traces
    print('Loading traces...')
    for i in range(16):
        with open(f'data/dataset1/trace{i}.txt') as f:
            for t, line in enumerate(f):
                all_traces[i][t] = np.array(line.strip().split(), dtype=np.float64)
    # for i in range(num_key_bytes):
    #     filename = f'{workdir}/trace{i}.txt'
    #     with open(filename, 'r') as file:
    #         for j, line in enumerate(file):
    #             # Convert line to float values and store in array
    #             all_traces[j, 50000*i:50000*(i+1)] = np.array(line.strip().split(), dtype=np.float64)

    plaintexts = np.zeros((num_traces, num_key_bytes), dtype=int)

    # Read the plaintexts
    with open(f'{workdir}/cleartext.txt', 'r') as file:
        for i, line in enumerate(file):
            # Convert line to integer values and store in array
            plaintexts[i] = np.array(line.strip().split(), dtype=int)

    hamming_weights = np.array([hamming_weight(i) for i in range(256)])

    all_hamming_weights_per_box2 = np.zeros((150, 256, 16), dtype=np.uint8)
    coeff2 = np.zeros((16, 256))

    print('Weights...')
    calc_weights()

    # coeff2[0] = multi(0)[1]

    with Pool() as pool:
        for box, coeffs in pool.imap_unordered(multi, range(16)):
            print(f'finished box {box}', flush=True)
            coeff2[box] = coeffs

    np.set_printoptions(formatter={'hex':int})

    for box in range(16):
        print(np.argsort(coeff2[box, :])[-1])