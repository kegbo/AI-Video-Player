import os
import struct
from typing import  Dict

def create_mp4l_file(sql_file: str, bin_folder: str, mp4_file: str, output_file: str):
    # Read SQL data
    with open(sql_file, 'rb') as sql:
        sql_data = sql.read()

    # Read bin files data along with their names
    bin_files_data: Dict[str, bytes] = {}
    for filename in os.listdir(bin_folder):
        bin_file_path = os.path.join(bin_folder, filename)
        with open(bin_file_path, 'rb') as bin_file:
            bin_files_data[bin_file_path] = bin_file.read()
            print(bin_file_path)
    
    

    # Read MP4 data
    with open(mp4_file, 'rb') as mp4:
        mp4_data = mp4.read()

    # Prepare header
    header = struct.pack('I', len(sql_data))
    header += struct.pack('I', len(mp4_data))
    header += struct.pack('I', len(bin_files_data))

    # Pack the data into the .mp4l file
    with open(output_file, 'wb') as mp4l_file:
        mp4l_file.write(header)
        mp4l_file.write(sql_data)
        mp4l_file.write(mp4_data)
        for filename, bin_data in bin_files_data.items():
            # Write the length of the filename and the filename itself
            mp4l_file.write(struct.pack('I', len(filename)))
            mp4l_file.write(filename.encode('utf-8'))
            # Write the length of the binary data and the binary data itself
            mp4l_file.write(struct.pack('I', len(bin_data)))
            mp4l_file.write(bin_data)

