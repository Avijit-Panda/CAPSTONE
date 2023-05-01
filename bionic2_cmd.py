def bold_part_word(word, start_index, end_index):
    bold_part = "\033[1m" + word[start_index:end_index+1] + "\033[0m"
    normal_part = word[:start_index] + word[end_index+1:]
    return  bold_part + normal_part

word = input('paste').split()

for i in word:
    n=len(i)
    new_word = bold_part_word(i, 0, int(n//2))
    print(new_word,end=' ')