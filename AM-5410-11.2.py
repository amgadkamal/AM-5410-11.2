""" LZW Python compression code to compress the text of Alice in Wonderland"""
"""Using code from https://rosettacode.org/wiki/LZW_compression#Python"""

import pickle

def compress(uncompressed):
    """Compress a string to a list of output symbols."""
    # Build the dictionary.
    dict_size = 256
    dictionary = dict((chr(i), i) for i in range(dict_size))
    # in Python 3: dictionary = {chr(i): i for i in range(dict_size)}

    w = ""
    result = []
    for c in uncompressed:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            # Add wc to the dictionary.
            dictionary[wc] = dict_size
            dict_size += 1
            w = c

    # Output the code for w.
    if w:
        result.append(dictionary[w])
    return result
#end def compress

def decompress(compressed):
    """Decompress a list of output ks to a string."""
    from io import StringIO

    # Build the dictionary.
    dict_size = 256
    dictionary = dict((i, chr(i)) for i in range(dict_size))
    # in Python 3: dictionary = {i: chr(i) for i in range(dict_size)}

    # use StringIO, otherwise this becomes O(N^2)
    # due to string concatenation in a loop
    result = StringIO()
    w = chr(compressed.pop(0))
    result.write(w)
    for k in compressed:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + w[0]
        else:
            raise ValueError('Bad compressed k: %s' % k)
        result.write(entry)

        # Add w+entry[0] to the dictionary.
        dictionary[dict_size] = w + entry[0]
        dict_size += 1
        w = entry
    return result.getvalue()
#end def decompress

#function of openining file for reading
def process_file(fname,enc):
    with open(fname, 'r', encoding=enc) as file:
        data = file.read()
    return data
#end def process_file

#function for ave the compressed text to a file using pickle.
def save_file(fname,compressed_data):
    with open(fname, 'wb') as save_:
        pickle.dump(compressed_data, save_)
#end def save_file

#funtion to read in the compressed file
def read_compressed(fname):
    with open(fname, 'rb') as read_:
        a=pickle.load(read_)
    return a
#def read_compressed

def main():

    data_=process_file('alice.txt','utf-8') # process the text file
    compressed = compress(data_) # compress the data
    save_file('save.pickle',compressed) # save the compressed data
    read_compressed_data=read_compressed('save.pickle') # read the compressed data file
    decode_data=decompress(read_compressed_data) # decode the compressed data
    print(decode_data[:45]) # print the first 45 characters
if __name__ == '__main__':
    main()









