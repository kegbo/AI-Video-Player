import os
import struct

def ensure_directories_exist(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def read_mp4l_file(input_file: str, output_folder: str):
    with open(input_file, 'rb') as mp4l_file:
        # Read header
        sql_length, mp4_length, num_bin_files = struct.unpack('III', mp4l_file.read(12))

        # Read SQL data
        sql_data = mp4l_file.read(sql_length)

        # Read MP4 data
        mp4_data = mp4l_file.read(mp4_length)

               # Write SQL data to file
        sql_file_path = os.path.join(output_folder, "chroma.sqlite3")
        with open(sql_file_path, 'wb') as sql_file:
            sql_file.write(sql_data)

        # Write MP4 data to file
        mp4_file_path = os.path.join(output_folder, "video.mp4")
        with open(mp4_file_path, 'wb') as mp4_file:
            mp4_file.write(mp4_data)

        

        # Read and create bin files
        for _ in range(num_bin_files):
            # Read filename
            filename_length = struct.unpack('I', mp4l_file.read(4))[0]
            filename = mp4l_file.read(filename_length).decode('utf-8')

            # Read binary data
            bin_file_data_length = struct.unpack('I', mp4l_file.read(4))[0]
            bin_file_data = mp4l_file.read(bin_file_data_length)

            # Write binary data to file
            output_path = os.path.join(output_folder, filename)
            ensure_directories_exist(output_path)
            with open(output_path, 'wb') as output_file:
                output_file.write(bin_file_data)

    return mp4_file_path


