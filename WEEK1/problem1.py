import sys
from typing import List
from typing import Union

WORDS_FILE_PATH = 'words.txt'

def load_data(file_path: str) -> List[str]:
  with open(file_path, 'r') as file:
    data = file.read().split()
  return data

def make_dictionary(data: List[str]) -> List[List[str]]:
  dictionary = []
  for word in data:
    dictionary.append([''.join(sorted(word)), word])
  dictionary.sort(key=lambda x:x[0])
  return dictionary

def anagrams_binary_search(A: List[List[str]], word: str) -> Union[List[List[str]], None]:
  left=0
  right=len(A)-1
  ans=[]

  while(right>=left):
    mid=(left+right)//2
    if(A[mid][0]==word):
      ans.append(A[mid])
      i,j=mid-1,mid+1
      while (A[i][0]==word):
        ans.append(A[i])
        i-=1
        
      while (A[j][0]==word):
        ans.append(A[j])
        j+=1
      return ans
    elif(A[mid][0]<word):
      left=mid+1
    else:
      right=mid-1
    
  return None


def main(input_word: str) -> Union[List[str], None]:
  words_data = load_data(WORDS_FILE_PATH)
  dictionary = make_dictionary(words_data)
    
  sorted_input_word = ''.join(sorted(input_word))
  anagrams = anagrams_binary_search(dictionary, sorted_input_word)
  
  if(not anagrams):
    print("No anagram found")
  else:
    for word in anagrams:
      print(word[1])
    return [word[1] for word in anagrams]

  return None

if __name__ == '__main__':
  if len(sys.argv) != 2:
    print(f"Usage: python {sys.argv[0]} <input_word>")
    sys.exit(1)
  main(sys.argv[1])