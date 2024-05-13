from collections import defaultdict

def create_dict_counter(data):
  new_dictionary = []
  for word in data:
    counter = defaultdict(int)
    for i in sorted(word):
      counter[i]+=1
    new_dictionary.append([counter,word])
  return new_dictionary

def is_subset(counter1,counter2):
  for key,value in counter1.items():
    if key not in counter2.keys() or counter2[key]<value:
      return False
  return True

def find_all_anagram(dictionary,input_word):
  result=[]
  counter = defaultdict(int)
  for i in sorted(input_word):
    counter[i]+=1
  
  for word in dictionary:
    if(is_subset(word[0],counter)):
      result.append(word[1])
  return result
      
def calculate_point(word):
  SCORES = [1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2, 2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4]
  score = 0
  for character in word:
    score += SCORES[ord(character) - ord('a')]
  return score
    
def find_maxpoint_anagram(anagrams):
  answer=0
  answer_word=""
  for anagram in anagrams:
    point = calculate_point(anagram)
    if(point>answer):
      answer = point
      answer_word = anagram
  return answer_word


def main():
  file_path = 'words.txt'
  with open(file_path, 'r') as file:
    data = file.read().split()
  
  test_path = 'large.txt'
  with open(test_path, 'r') as file:
    test_data = file.read().split()

  
  
  new_dictionary=create_dict_counter(data)
  
  test_anagrams=[]
  answer_anagrams=[]
  for data in test_data:
    anagrams = find_all_anagram(new_dictionary,data)
    test_anagrams.append(anagrams) 
   
  
  if(test_anagrams):
    for test_anagram in test_anagrams:
      answer_anagram=find_maxpoint_anagram(test_anagram)
      answer_anagrams.append(answer_anagram)
  else:
    print('Not Found an Anagram')
    return None

  output_path="output_large.txt"
  with open(output_path, mode='w') as file:
    file.write('\n'.join(answer_anagrams))

    
    

if __name__ == '__main__':
  main()