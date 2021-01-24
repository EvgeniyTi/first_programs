from tqdm import tqdm
import zipfile
import itertools

# Путь к архиву
path_file = 'secure.zip'
# Инициализация объекта файла Zip
zip_file = zipfile.ZipFile(path_file)

use = itertools.product('0123456789', repeat=5)
use_list = [''.join(i) for i in use]
wordlist = []
for j in use_list:
    wordlist.append(f'o_main_got{j}')

words = len(wordlist)

print("Total passwords to test:", words)
for word in tqdm(wordlist, total=words, unit=" word"):
    try:
        zip_file.extractall(pwd=word.encode('utf-8').strip())
    except:
        pass
    else:
        print("\nPassword found:" + '\033[32m', word.strip())
        exit(0)
print("\nPassword not found", '\033[91m' + "try other wordlist.")
