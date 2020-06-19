import re
import sys
# import ast
# from analyzer import *
from fingerprint import Fingerprint


# Setup the winnowing function by removing all common characters and retrieving the k-gram hashes
def winnow_setup(text, k, w):
    # text to lowercase and remove all non-alphanumerics for text
    text = text.lower()
    # text = re.sub(r'\W+', '', text) this is for plain text
    text = re.sub(r'\s+', '', text)
    # retrieve the k-gram hashes
    hashes = compute_hash(text, k)
    # return the output of the winnow function
    return winnow(w, hashes)


# Algorithm taken from 'Winnowing: Local Algorithms for Document Fingerprinting'
def winnow(w, hashes):
    recorded = {}
    h2 = hashes.copy()
    # create the window of size 4
    h = [sys.maxsize for i in range(0, w)]
    r = 0
    minimum = 0
    global_pos = 0
    # loop through the hashes to find the minimum hash in every window
    for i in range(0, len(hashes)):
        r = (r + 1) % w
        h[r] = h2.pop(0)
        # if the minimum is the current index, check entire window for the minimum
        if minimum == r:
            for ind in scan_left_ind(r, w):
                if h[ind] < h[minimum]:
                    minimum = ind
            recorded = record(recorded, h[minimum], global_pos, w)
        else:  # check if the current index is the new minimum
            if h[r] < h[minimum]:
                minimum = r
                recorded = record(recorded, h[minimum], global_pos, w)
        global_pos += 1
    return recorded


# record the current hash and the its positioning
def record(recorded, minimum, global_pos, w):
    # determine if there is another hash in the same window already
    if global_pos < w and len(recorded) > 0:
        for rec in recorded.copy():
            # if there is, determine the true minimum and record it
            if minimum < rec:
                recorded.pop(rec)
                recorded[minimum] = [global_pos]
    else:
        if minimum in recorded:
            recorded[minimum] = recorded[minimum] + [global_pos]
        else:
            recorded[minimum] = [global_pos]
    return recorded


# create an array starting at the rightmost index of the current window
# continue until you hit the current index, r
def scan_left_ind(r, w):
    inds = []
    step = (r - 1) % w
    for i in range(0,4):
        inds.append(step)
        step = (step - 1 + w) % w
    return inds


# compute the k-gram hashes through a rolling hash function
def compute_hash(s, k):
    # setup the compute hash function
    ints = compute_ints(s)
    p = 31
    m = 10 ** 9 + 9
    # compute the p_pow values
    p_pow = compute_p_pow(k, p, m)
    final_pow = p_pow[k - 1]
    # compute the initial hash value
    hashes = [sum([num * power % m for num, power in zip(ints[0:k], p_pow)])]
    for i in range(0, len(s) - k):
        # compute the next hash value through the previous one
        hashes.append(int((hashes[i] - ints[i]) / p % m + (ints[k + i] * final_pow) % m))
    return hashes


# return the modified int value for the characters in the text
def compute_ints(s):
    ints = []
    for ch in s:
        ints.append(ord(ch) - ord('a') + 1)
    return ints


# compute the p_pow values
def compute_p_pow(k, p, m):
    p_pow = [1]
    for i in range(1, k):
        p_pow.append((p_pow[i-1] * p) % m)
    return p_pow


def get_substring(pos, k, text):
    i = 0
    spaces_pos = []
    newlines_pos = []
    for ch in text:
        if ch == ' ':
            spaces_pos.append(i)
        if ch == '\n':
            newlines_pos.append(i)
        i += 1
    for space_pos in spaces_pos + newlines_pos:
        if space_pos <= pos:
            pos += 1
        if pos < space_pos <= pos + k:
            k += 1
    return text[pos:pos+k]


def compare_files(student_file_loc, base_file_loc, k, w):
    student_file = open(student_file_loc, "r")
    student_txt = student_file.read()
    student_fingerprints = winnow_setup(student_txt, k, w)
    num_std_fps = 0
    for val in student_fingerprints.values():
        for _ in val:
            num_std_fps += 1

    base_file = open(base_file_loc, "r")
    base_txt = base_file.read()
    base_fingerprints = winnow_setup(base_txt, k, w)

    common = []
    num_common_fps = 0
    for fp in list(student_fingerprints.keys()):
        if fp in list(base_fingerprints.keys()):
            common.append(fp)
            for _ in student_fingerprints[fp]:
                num_common_fps += 1

    similarity = num_common_fps / num_std_fps
    plagiarized = "plagiarized" if similarity >= 0.25 else "not plagiarized"
    print("The student file is {:.2%} similar to the base file.\n".format(similarity) +
          "The student file was likely {}.".format(plagiarized))
    res = str("The student file is {:.2%} similar to the base file.\n".format(similarity) +
            "The student file was likely {}.".format(plagiarized))
    return res


def get_common_fingerprints(student_file_loc, base_file_loc, k, w):
    student_file = open(student_file_loc, "r")
    student_txt = student_file.read()
    student_fingerprints = winnow_setup(student_txt, k, w)

    base_file = open(base_file_loc, "r")
    base_txt = base_file.read()
    base_fingerprints = winnow_setup(base_txt, k, w)

    student_common = []
    base_common = []
    for fp in list(student_fingerprints.keys()):
        if fp in list(base_fingerprints.keys()):
            substr = get_substring(student_fingerprints[fp][0], k, student_txt)
            # for each position add an object
            for pos in student_fingerprints[fp]:
                sfp = Fingerprint(fp, pos, substr)
                student_common.append(sfp)
            # for each position add an object
            for pos in base_fingerprints[fp]:
                bfp = Fingerprint(fp, pos, substr)
                base_common.append(bfp)

    return student_common, base_common


"""def get_python(file):
    with open("test.py", "r") as source:
        # print(source.read())
        tree = ast.parse(source.read(), "test.py")

    for node in ast.walk(tree):
        print(node)

    v = PyAnalyzer()
    v.visit(tree)"""


def main():
    compare_files("text_test.txt", "test2.txt", 10, 4)
    get_common_fingerprints("text_test.txt", "test2.txt", 10, 4)
    # get_python('test.py')


if __name__ == "__main__":
    main()