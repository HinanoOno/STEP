def create_new_dictionary(data):
  new_dictionary = []
  for word in data:
    new_dictionary.append([''.join(sorted(word)), word])
  new_dictionary.sort(key=lambda x:x[0])
  return new_dictionary
    
def binary_search(A,x):
  left=-1
  right=len(A) 
  ans=[]

  while(right>=left):
    mid=(left+right)//2
    if(A[mid][0]==x):
      ans.append(A[mid])
      i,j=mid-1,mid+1
      while (A[i][0]==x):
        ans.append(A[i])
        i-=1
        
      while (A[j][0]==x):
        ans.append(A[j])
        j+=1
      return ans
    elif(A[mid][0]<x):
      left=mid+1
    else:
      right=mid-1

    
  return None


def main(random_word):
  file_path = 'words.txt'
  with open(file_path, 'r') as file:
    data = file.read().split()
    
  sorted_random_word = ''.join(sorted(random_word))
    
  new_dictionary = create_new_dictionary(data)

  anagram = binary_search(new_dictionary, sorted_random_word)
  
  if(not anagram):
    print("No anagram found")
  else:
    return [word[1] for word in anagram]
  

if __name__ == '__main__':
  random_word= input("Enter a word: ")
  main(random_word)