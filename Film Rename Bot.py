import re
import os
import time

# Creator: Tobechukwu N. Njoku
# Last Update: 2021/07/31

regex_audio = re.compile(r'.*([2-7] [0-2][ ])')       # Using Regular expression to fix audio
regex_year = re.compile(r'.*( [1-2][0-9]{3} )')     # Using Regular expression to find the year
regex_anomaly = re.compile(r'.*([)](.*.)[\[])')     # Using Regular expression to find the anomaly
regex_resolutions = re.compile(r'.*([1-2][0-9]{3}[p] )')     # Using Regular expression to find the resolution


def movie_rename(file_name):
    renaming_history_file_name = "Film Rename Bot History.txt"
    special_characters = ("(", ")", "[", "]", "  ", ":", "_", ".", "-")
    # opening_bracket = special_characters[3]
    # closing_bracket = special_characters[4]

    try:
        open(renaming_history_file_name)
    except IOError:
        print("File not accessible or doesn't exist")
    finally:
        file = open(renaming_history_file_name, "a+")
        file.write(file_name + " \n")
    file.close()

    print("Input: " + file_name)

    file_name, file_extension = os.path.splitext(file_name)     # Remove and save file extension.

    for x in special_characters:        # Remove certain characters
        file_name = file_name.replace(x, " ")

    file_name = file_name.replace(" A ", " a ").replace(" Of ", " of ").replace(" And ", " and ")\
        .replace(" The ", " the ").replace("X26", "x26").replace("H26", "x26").replace("Im ", "I'm ")\
        .replace("St ", "St. ").replace("WEB DL ", "Web-DL ").replace("BluRay ", "Blu-ray ")\
        .replace("Blu ray ", "Blu-ray ").replace("eztv re", "eztv.re")

    audio_found = re.search(regex_audio, file_name)     # Search for broken audio format in file name.
    resolution_found = re.search(regex_resolutions, file_name)     # Search for resolution item in file name.
    year_discovered = re.search(regex_year, file_name)      # Search for year in file name.
    anomaly_found = re.search(regex_anomaly, file_name)     # Search for misplaced item in file name.

    if audio_found:     # Fixing the naming of audio if it is found in a broken state.
        sound_format = audio_found.group(1).strip().replace(" ", ".")
        print("Found Sound Format: " + sound_format)
        file_name = file_name.replace(audio_found.group(1), sound_format + " ")

    if resolution_found:        # Putting a square bracket in front of the resolution if it is found.
        resolution = resolution_found.group(1).strip()
        print("Found Resolution: " + resolution)
        file_name = file_name.replace(resolution_found.group(1), "[" + resolution + " ")

    if year_discovered:     # Padding the year if it's found with parentheses.
        year = year_discovered.group(1).strip()
        print("Found Year: " + year)
        file_name = file_name.replace(year_discovered.group(1), " (" + year + ")")

    if anomaly_found:       # Removing any anomalies found between the year and start of metadata.
        anomaly = anomaly_found.group(2)
        print("Found Anomaly: " + anomaly)
        file_name = file_name.replace(anomaly_found.group(1), ") [") + " " + anomaly

    while file_name[-1] == " ":     # Remove trailing whitespaces.
        if file_name[-1].isalpha():
            break
        file_name = file_name[:-1]

    while "  " in file_name:        # Removing double spaces in the file name.
        if "  " not in file_name:
            break

    file_name = file_name.replace(")[", ") [")      # Adjusting the spacing between year and metadata.

    file_name += "]" + file_extension       # Re-attach the file extension to the finished name.

    # open_bracket_index = file_name.index(opening_bracket)
    # closing_bracket_index = file_name.index(closing_bracket)
    # file_name_copy = file_name
    print("Finished: " + file_name + "\n")
    return file_name


def film_parsing():
    path = 'Films/'
    files = os.listdir(path)

    start_time = time.time()        # This will time how long it takes the code to execute.

    for index, file_name in enumerate(files):
        os.rename(os.path.join(path, file_name), os.path.join(path, ''.join([str(movie_rename(file_name)), ])))

    end_time = time.time()
    print(end_time - start_time)        # Print the time duration of the code execution.
    exit()


film_parsing()