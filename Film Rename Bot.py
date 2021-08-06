import os
import re
import time
import Levenshtein

# Creator: Tobechukwu N. Njoku
# Last Update: 2021/08/06

regex_audio = re.compile(r'.*([2-7] [0-2][ ])')  # Using Regular expression to fix audio
regex_resolutions = re.compile(r'.*([1-2][0-9]{3}[p] )')  # Using Regular expression to find the resolution
regex_year = re.compile(r'.*( [1-2][0-9]{3} )')  # Using Regular expression to find the year
regex_anomaly = re.compile(r'.*([)] (.*.) [\[])')  # Using Regular expression to find the anomaly


def movie_rename(file_name):
    renaming_history_file_name = "Film Rename Bot History.txt"
    special_characters = (") [", "[", "]", "(", ")", ":", " - ", "-", "_", ".", "  ")
    distorted_data = {" A ": " a ", " Of ": " of ", " And ": " and ", " The ": " the ", "a K a": "A.K.A.",
                      "Dts HD": "DTS-HD", "WEB DL": "Web-DL", "Web DL": "Blu ray", "Blu-ray": "Web-DL", "ENGLISH": "Eng", "GERMAN": "Ger",
                      "FRENCH": "Fre", "ITALIAN": "Ita", "JAPANESE": "Jap", "KOREAN": "Kor", "RUSSIAN": "Rus",
                      "THAI": "Thai", "REMASTERED": "Remastered"}
    opening_bracket = special_characters[1]
    closing_bracket = special_characters[2]
    open_bracket_index = file_name.find(opening_bracket)
    closing_bracket_index = file_name.find(closing_bracket)

    try:
        open(renaming_history_file_name)
    except IOError:
        print("File not accessible or doesn't exist. \nCreating a new file.")
    finally:
        file = open(renaming_history_file_name, "a+")
        file.write("Input:  " + file_name + " \n")

    print("Input: " + file_name)

    file_name, file_extension = os.path.splitext(file_name)  # Remove and save the file extension.

    for x in special_characters:  # Replace certain characters with spaces.
        file_name = file_name.replace(x, " ")
    for key, value in distorted_data.items():  # Replaces broken metadata.
        file_name = file_name.replace(key, value)

    file_name = regular_expressions(file_name)
    file_name = sanitize_output(file_name)

    title = file_name[:open_bracket_index]
    metadata = file_name[open_bracket_index:]

    metadata = levenshtein_fuzzy_search(metadata)

    file_name = title + metadata + "]" + file_extension  # Re-attach the file extension to the finished name.
    file.write("Output: " + file_name + " \n")  # Writing the computed file name to the history file.
    file.close()
    print("Finished: " + file_name + "\n")  # Telling the user what the computed file name is.

    return file_name


def regular_expressions(file_name):
    audio_found = re.search(regex_audio, file_name)  # Search for broken audio format in file name.
    if audio_found:  # Fixing the naming of audio if it is found in a broken state.
        sound_format = audio_found.group(1).strip().replace(" ", ".")
        print("Found Sound Format: " + sound_format)
        file_name = file_name.replace(audio_found.group(1), sound_format + " ")
    else:
        print("Error: Sound format not found!")

    resolution_found = re.search(regex_resolutions, file_name)  # Search for resolution item in file name.
    if resolution_found:  # Putting a square bracket in front of the resolution if it is found.
        resolution = resolution_found.group(1).strip()
        print("Found Resolution: " + resolution)
        file_name = file_name.replace(resolution_found.group(1), "[" + resolution + " ")
    else:
        print("Error: Resolution not found!")

    year_found = re.search(regex_year, file_name)  # Search for year in file name.
    if year_found:  # Padding the year if it's found with parentheses.
        year = year_found.group(1).strip()
        print("Found Year: " + year)
        file_name = file_name.replace(year, " (" + year + ")")
    else:
        print("Error: Year not found!")

    anomaly_found = re.search(regex_anomaly, file_name)  # Search for misplaced item in file name.
    if anomaly_found:  # Moving any anomalies found between the year and start of metadata to the end.
        anomaly = anomaly_found.group(2)  # Group 1 = ")x[
        print("Found Anomaly: " + anomaly)  # Group 2 = "x"
        # print("Group 1 = " + anomaly_found.group(1) + "\nGroup 2 = " + anomaly_found.group(2))        # Print info.
        file_name = file_name.replace(anomaly_found.group(1), ") [").replace("]", "") + " " + anomaly
    else:
        print("Warning: Anomaly not found!")

    file_name = re.sub(r'(\s\s+)', ' ', file_name)  # Removing double spaces in the file name.

    return file_name


def sanitize_output(file_name):
    while file_name[-1] == " ":  # Removes trailing whitespaces.
        if file_name[-1].isalnum():
            break
        else:
            file_name = file_name[:-1]

    file_name = file_name.replace(")[", ") [")  # Adjusting the spacing between year and metadata.

    return file_name


def levenshtein_fuzzy_search(metadata):
    fuzzy_search_items = ['x265', 'St. ', '10bit', 'HDR', 'HMAX', 'HEVC', 'AAC', 'Atmos', 'DTS-HD', 'TrueHD', 'WebRip',
                          'Blu-ray', 'DC', 'eztv.re']
    space = " "

    input_data = metadata.split()  # Putting the file name into a list.

    for index, item in enumerate(input_data):
        for index2, item2 in enumerate(fuzzy_search_items):  # Nested for loop, to match all indexes between two lists.
            levenshtein_ratio = Levenshtein.ratio(input_data[index].lower(), fuzzy_search_items[index2].lower())

            if levenshtein_ratio > 0.7:  # Replace if the code if the match is good.
                input_data[index] = fuzzy_search_items[index2]
                print("Levenshtein Ratio", end=": ")
                print(levenshtein_ratio)
                print("Input", end=":  ")
                print(input_data[index])
                print("Output", end=": ")
                print(input_data[index])

    metadata = space.join(input_data)

    return metadata


def film_parsing():
    path = 'Films/'

    files = os.listdir(path)

    start_time = time.time()  # This will time how long it takes the code to execute.

    for index, file_name in enumerate(files):  # Move through all the files in the directory.
        os.rename(os.path.join(path, file_name), os.path.join(path, ''.join([str(movie_rename(file_name)), ])))

    end_time = time.time()
    duration = end_time - start_time

    print("Execution Duration", end=": ")
    print(duration, end=" seconds")  # Print the time duration of the code execution.

    exit()


film_parsing()
