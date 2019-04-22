import argparse
import sys
import os
import glob
import re
from collections import defaultdict


# Конвертирует словарь в строку (запись)
def dictionaryToString(dictionary):
    string = ""

    for word1 in dictionary:
        string = '{0}{1}: '.format(string, word1)
        for word2 in dictionary[word1]:
            string = '{0}{1} - {2} '.format(string, word2, str(dictionary[word1][word2]))
        string = '{0}\n'.format(string)

    return string


# Обрабатывает нужным образом строку в файле и
# Берет последнее слово в файле
def process(dictionary, line, lc):
    words = re.sub(r'([^\s\w]|_)+', '', line)

    if lc:
        words = words.lower()

    words = re.sub('\t+', '', words)
    words = re.sub('\n+', '', words)
    words = re.sub(' +', ' ', words)
    words = words.strip()
    words = words.split()

    for i in range(len(words) - 1):
        dictionary[words[i]][words[i + 1]] += 1

    return dictionary, words[len(words) - 1] if len(words) >= 1 else ""


# Считывание с stdin
def parseFromStdin(inputDir, lc):
    dictionary = defaultdict(lambda: defaultdict(int))

    prevWord = ""

    for line in sys.stdin:
        if line == "/exit\n":
            break

        dictionary, prevWord = process(dictionary, '{0} {1}'.format(prevWord, line), lc)

    return dictionary


# Считывание с файла
def parseFromFile(inputDir, lc):
    dictionary = defaultdict(lambda: defaultdict(int))

    # Выбираем все .txt файлы из директории inputDir
    for file in glob.glob(inputDir + "/*.txt"):
        fin = open(file, "r", encoding="utf-8")
        line = "1"
        prevWord = ""

        while line:
            line = fin.readline()
            dictionary, prevWord = process(dictionary, '{0} {1}'.format(prevWord, line), lc)

    return dictionary


# Запись в stdin
def printModelToStdin(dictionary):
    print(dictionaryToString(dictionary))


# Запись в файл
def printModelToFile(dictionary, model):
    with open(model, "w", encoding='UTF-8') as file:
        file.write(dictionaryToString(dictionary))
        file.close()


def createParser():
    parser = argparse.ArgumentParser(description='Enter "-h" for help.')
    parser.add_argument('-input_dir', '--input_dir', required=True, help='Directory with source files.')
    parser.add_argument('-model', '--model', default=None, required=True, help='Directory, which will be used as a destination folder for model file.')
    parser.add_argument('-lc', '--lc', action="store_true", required=False, help='Ignore cases in input files.')
    return parser.parse_args()


# main
def main():
    parcedArgs = createParser()

    if parcedArgs.input_dir:
        dictionary = parseFromFile(parcedArgs.input_dir, parcedArgs.lc)

    else:
        print("Reading input from stdin:\nTo exit - enter '/exit'")
        dictionary = parseFromStdin(parcedArgs.input_dir, parcedArgs.lc)

    if parcedArgs.model:
        printModelToFile(dictionary, parcedArgs.model)

    else:
        printModelToStdin(dictionary)


if __name__ == '__main__': main()

# ПРИМЕР:
# python train.py --lc --model model.txt --input_dir inp
