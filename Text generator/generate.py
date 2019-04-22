import argparse
import random
from collections import defaultdict


# преобразование из string в dictionary
def stringToDictionary(model):
    modelFile = open(model, mode='r', encoding='utf8')
    dictionary = defaultdict(dict)

    for line in modelFile:
        line = line.rstrip("\n")
        words = line.split(": ")
        first = words[0]
        words = words[1].split("; ")
        words.pop()

        for word in words:
            second = word.split(" - ")[0]
            dictionary[first][second] = word.split(" - ")[1]

    modelFile.close()
    return dictionary


# берем следующее слово:
def getNextWord(dictionary, currentWord):
    random.seed()
    nextWords = dictionary[currentWord]

    # если за этим словом нету других, то берем рандомно.
    if not dictionary[currentWord]:
        return findRandomSeed(dictionary)

    percentage = []
    count = []
    words = []

    for nextWord in nextWords:
        count.append(int(nextWords[nextWord]))
        words.append(nextWord)

    s = 0

    for elem in count:
        s += int(elem)

    for k in count:
        percentage.append(k / s)

    return str(random.choices(words, weights=percentage, k=1)[0])


# рандомный выбор слова из словаря
def findRandomSeed(dictionary):
    arr = list(dictionary.keys())
    return random.choice(arr)


# Главный метод
def generate(length, model, seed, outputFile):
    output = ""
    dictionary = stringToDictionary(model)
    currentWord = seed if seed else findRandomSeed(dictionary)

    for _ in range(length):
        output = '{0} {1}'.format(output, currentWord)
        nextWord = getNextWord(dictionary, currentWord)
        currentWord = nextWord

    output = output.lstrip(" ")

    if outputFile:
        with open(outputFile, "w", encoding="utf8") as file:
            file.write(output)
            file.close()

    else:
        print(output)


def createParser():
    parser = argparse.ArgumentParser(description='Enter "-h" for help.')
    parser.add_argument('-length', '--length', type=int, default=None, required=True, help='Length of generating text')
    parser.add_argument('-model', '--model', default=None, required=True, help='model location')
    parser.add_argument('-seed', '--seed', required=False, help='First word of generating text')
    parser.add_argument('-output', '--output', required=False, help='Output file')
    parcedArgs = parser.parse_args()
    return parcedArgs


def main():
    parcedArgs = createParser()
    generate(parcedArgs.length, parcedArgs.model, parcedArgs.seed, parcedArgs.output)


if __name__ == '__main__': main()

# ПРИМЕР:
# python generate.py --model model.txt --length 100 --output output.txt
