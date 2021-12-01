

INPUT_PATH = '/home/hamz/Part Time/widya-wicara-diarization/fine-tuning/Widya/WDY-DZ.train.uem'
OUTPUT_PATH = '/home/hamz/Part Time/widya-wicara-diarization/fine-tuning/Widya/WDY-DZ.train-Fix.uem'
if __name__ == "__main__":
    with open(INPUT_PATH, 'r') as file:
        lines = file.readlines()
    
    with open(OUTPUT_PATH, 'w') as out:
        for line in lines:
            temp = line.split()
            out.writelines("{} 1 {} {}".format(temp[0],temp[1],temp[2]))
            out.writelines("\n")
            print(temp)