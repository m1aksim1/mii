import math
from bitarray import bitarray

class BloomFilter: #реализация фильтра блуума
    def __init__(self, items_count, fp_prob):
        self.fp_prob = fp_prob
        self.size = self.get_size(items_count, fp_prob)
        self.hash_count = self.get_hash_count(self.size, items_count)
        self.bit_array = [0] * self.size

    def add(self, item):
        for i in range(self.hash_count):
            digest = hash(item+str(i)) % self.size
            self.bit_array[digest] = 1

    def check(self, item):
        for i in range(self.hash_count):
            digest = hash(item+str(i)) % self.size
            if self.bit_array[digest] == 0:
                return False
        return True

    @staticmethod
    def get_size(n, p):
        m = -(n * math.log(p)) / (math.log(2) ** 2)
        return int(m)

    @staticmethod
    def get_hash_count(m, n):
        k = (m / n) * math.log(2)
        return int(k)