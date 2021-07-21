# class for the hashtable used to hold and retrieve package objects

class HashTable:

    # constuctor
    def __init__(self, capacity):
        self.table = []
        for i in range(capacity):
            self.table.append([])
    # insert method
    def insert(self, key, item):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # update if key is present
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True
        # if key is not present, item is appended to bucket list
        key_value = [key, item]
        bucket_list.append(key_value)
        return True

    # searches for key and returns item
    def lookup(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # searches for key
        for kv in bucket_list:
            if kv[0] == key:
                return kv[1] # returns value
        return None # returns None if key is not found

    # removes item based on key
    def remove(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                bucket_list.remove(kv[0], kv[1])



