import sys
from collections import defaultdict
from typing import List, Dict, Tuple

WORDS_FILE_PATH = "words.txt"


def load_data(file_path: str) -> List[str]:
    with open(file_path, "r") as file:
        data = file.read().split()
    return data

def output_data(file_path: str, data: List[str]):
    with open(file_path, mode="w") as file:
        file.write("\n".join(data))
    return None

def calculate_point(word: str) -> int:
    SCORES = [1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2, 2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4]
    score = 0
    for character in word:
        score += SCORES[ord(character) - ord("a")]
    return score

def make_dictionary(data: List[str]) -> List[Tuple[Dict[str, int], str, int]]:
    dictionary = []
    for word in data:
        counter: Dict[str, int] = defaultdict(int)
        for i in word:
            counter[i] += 1
        point = calculate_point(word)
        dictionary.append((counter, word, point))
    dictionary.sort(key=lambda x:x[2],reverse=True)
   
    return dictionary

def find_anagrams(dictionary: List, input_word: str) -> str:
    counter: Dict[str, int] = defaultdict(int)
    for i in sorted(input_word):
        counter[i] += 1
    for word in dictionary:
        if is_subset(word[0], counter):
            return word[1]
    return ""  

def is_subset(counter1: dict, counter2: dict) -> bool:
    for key, value in counter1.items():
        if key not in counter2.keys() or counter2[key] < value:
            return False
    return True

def main(input_path: str):
    words_data = load_data(WORDS_FILE_PATH)
    input_data = load_data(input_path)
    
    dictionary = make_dictionary(words_data)

    anagrams=[]
    for data in input_data:
        anagrams.append(find_anagrams(dictionary,data))
    
    if(anagrams==[]):
        print("Not Found an Anagram")
        return None

    output_data(f"output_{input_path}", anagrams)

if __name__ == "__main__":
    main(sys.argv[1])
