


from a6_include import *


class HashEntry:

    def __init__(self, key: str, value: object):
        """
        Initializes an entry for use in a hash map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.key = key
        self.value = value
        self.is_tombstone = False

    def __str__(self):
        """
        Overrides object's string method
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return f"K: {self.key} V: {self.value} TS: {self.is_tombstone}"


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses Quadratic Probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()

        for _ in range(capacity):
            self.buckets.append(None)

        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Overrides object's string method
        Return content of hash map in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            out += str(i) + ': ' + str(self.buckets[i]) + '\n'
        return out

    def clear(self) -> None:
        """
        It clear all buckets of the hash map. TODO: Write this implementation
        """
        for i in range(self.capacity):
            self.buckets.set_at_index(i, None)
        self.size = 0

    def get(self, key: str) -> object:
        """
        It gets the value from the hash map according to the given key. TODO: Write this implementation
        """
        # quadratic probing required
        ind=self.hash_function(key)%self.capacity # Initial target index
        # For probing iterations
        cur_ind=ind
        cur_entry=self.buckets.get_at_index(ind)
        iter_count=1
        while iter_count < self.capacity + 1: # Probing iterations
            if cur_entry == None or cur_entry.is_tombstone: # If it is None, go to next iteration
                cur_ind=(ind+iter_count**2)%self.capacity # quadratic probing
                cur_entry = self.buckets.get_at_index(cur_ind) # new target entry
                iter_count += 1
                continue
            if cur_entry.key==key: # If we find the key, return the corresponding value
                return cur_entry.value
            else: # If keys are not matched, go to next iteration
                cur_ind=(ind+iter_count**2)%self.capacity # quadratic probing
                cur_entry=self.buckets.get_at_index(cur_ind) # new target entry
                iter_count += 1
        return None

    def put(self, key: str, value: object) -> None:
        """
        It find the propoer place and puts the given key, value pair to this location. TODO: Write this implementation
        """
        # remember, if the load factor is greater than or equal to 0.5,
        # resize the table before putting the new key/value pair
        #
        # quadratic probing required
        if self.table_load() >= 0.5: # If the load factor is gt or eq to 0.5, doubles the capacity
            self.resize_table(2*self.capacity)
        ind=self.hash_function(key)%self.capacity # Initial target index
        # For probing iterations
        cur_ind=ind
        cur_entry = self.buckets.get_at_index(cur_ind) # new target entry
        iter_count=1
        if self.contains_key(key):
            while iter_count < self.capacity + 1: # Probing iterations
                if cur_entry != None and not cur_entry.is_tombstone and cur_entry.key == key: # We found the correct place, then overwrite the value
                    cur_entry.value = value
                    self.buckets.set_at_index(cur_ind, cur_entry)
                    return
                else:
                    cur_ind=(ind+iter_count**2)%self.capacity # quadratic probing
                    cur_entry = self.buckets.get_at_index(cur_ind) # new target entry
                    iter_count += 1
        else:
            while iter_count < self.capacity + 1:
                if cur_entry == None or cur_entry.is_tombstone: # We found the correct place, just put a new HashEntry
                    new_entry = HashEntry(key, value)
                    self.buckets.set_at_index(cur_ind, new_entry)
                    self.size += 1
                    return
                else:
                    cur_ind=(ind+iter_count**2)%self.capacity # quadratic probing
                    cur_entry = self.buckets.get_at_index(cur_ind) # new target entry
                    iter_count += 1
        
    def remove(self, key: str) -> None:
        """
        It removes key, value pair from the hash map according to the given key. TODO: Write this implementation
        """
        # quadratic probing required
        ind=self.hash_function(key)%self.capacity # Initial target index
        # For probing iterations
        cur_ind=ind
        cur_entry = self.buckets.get_at_index(cur_ind)
        iter_count=1
        while iter_count < self.capacity+1: # Probing iterations
            if cur_entry == None: # If it is None, go to next iteration
                cur_ind=(ind+iter_count**2)%self.capacity # quadratic probing
                cur_entry = self.buckets.get_at_index(cur_ind) # new target entry
                iter_count += 1
                continue
            if cur_entry.key==key and not cur_entry.is_tombstone: # If we find the key, remove this entry
                cur_entry.is_tombstone = True
                self.buckets.set_at_index(cur_ind, cur_entry)
                self.size-=1
                break
            else: # If keys are not matched, go to next iteration
                cur_ind=(ind+iter_count**2)%self.capacity # quadratic probing
                cur_entry = self.buckets.get_at_index(cur_ind) # new target entry
                iter_count += 1

    def contains_key(self, key: str) -> bool:
        """
        It checks if the given key in the hash map. TODO: Write this implementation
        """
        # quadratic probing required
        ind=self.hash_function(key)%self.capacity # Initial target index
        # For probing iterations
        cur_ind=ind
        cur_entry = self.buckets.get_at_index(cur_ind)
        iter_count=1
        while iter_count < self.capacity + 1: # Probing iterations
            if cur_entry == None or cur_entry.is_tombstone: # If it is None, go to next iteration
                cur_ind=(ind+iter_count**2)%self.capacity # quadratic probing
                cur_entry = self.buckets.get_at_index(cur_ind) # new target entry
                iter_count += 1
                continue
            if cur_entry.key==key and not cur_entry.is_tombstone: # If we find the key, return True
                return True
            else: # If keys are not matched, go to next iteration
                cur_ind=(ind+iter_count**2)%self.capacity # quadratic probing
                cur_entry = self.buckets.get_at_index(cur_ind) # new target entry
                iter_count += 1
        return False

    def empty_buckets(self) -> int:
        """
        If returns the count of the empty buckets. TODO: Write this implementation
        """
        count=0
        length=self.capacity
        for i in range(length): # Iterate over the bucket elements and check if it is empty
            if self.buckets.get_at_index(i)==None or self.buckets.get_at_index(i).is_tombstone:
                count+=1
        return count

    def table_load(self) -> float:
        """
        It returns the current load factor. TODO: Write this implementation
        """
        return self.size / self.capacity

    def resize_table(self, new_capacity: int) -> None:
        """
        It resizes the table with the given new capacity value. TODO: Write this implementation
        """
        # remember to rehash non-deleted entries into new table
        if new_capacity >= 1 and new_capacity >= self.size: # If new capacity is lt 0 or the current size, nothing happens
            old_keys = self.get_keys() # Get old keys
            old_values = DynamicArray()
            for i in range(old_keys.length()): # Find corresponding values
                key = old_keys.get_at_index(i)
                old_values.append(self.get(key))
            # Clean and change attributes
            self.capacity = new_capacity
            self.buckets = DynamicArray()
            for _ in range(self.capacity):
                self.buckets.append(None)
            self.size=0

            for i in range(old_keys.length()): # Put old entries one by one
                self.put(old_keys.get_at_index(i), old_values.get_at_index(i))

    def get_keys(self) -> DynamicArray:
        """
        It returns all keys in the hash map. TODO: Write this implementation
        """
        arr=DynamicArray()
        for i in range(self.buckets.length()): # Iterate over the buckets
            cur_entry = self.buckets.get_at_index(i)
            if cur_entry!=None and not cur_entry.is_tombstone:
                arr.append(cur_entry.key)
        return arr


if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    # this test assumes that put() has already been correctly implemented
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
