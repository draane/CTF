from binascii import unhexlify

with open('input.txt', 'r') as fd:
    for line in fd:
        index = line.split("(")[1].split(",")[0]
        hex_str = line.split(" ")[2].split(")")[0].split("x")[1]

        result = unhexlify(hex_str)
        with open('files/file_' + index, 'wb') as new_file:
            new_file.write(result)
