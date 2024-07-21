import requests
import hashlib
import sys

def get_password(query):
   url =' https://api.pwnedpasswords.com/range/'+query
   response = requests.get(url)
   if response.status_code != 200:
        raise RuntimeError(f'Error fetching {url}, status code: {response.status_code}')
   return response.text
# check relative pass from the tail and the count of hacked 
def check_password(all_hashes,tail_hash):
    splitted_hashes=(line.split(':') for line in all_hashes.splitlines())
    for hash,count in splitted_hashes:
        if(hash==tail_hash):
            return count
    return 0

    
def hash_password(password):
    # hashong my paswword
    hashed_password=hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first_letter,tail=hashed_password[:5],hashed_password[5:]
    results=get_password(first_letter)
    return check_password(results,tail)

 

def main(args):
    for password in args:
        count=hash_password(password)
        if(count):
            print(f'OOPS!!Your password been hacked {count} time')
        else:
            print("Congrats you're password never been hacked.Carry on!")

    return 'done'

def read_password(path):
    all_pass=[]
    with open(path,'r') as file:
        for line in file.read().splitlines():
            all_pass.append(line)
    return all_pass

if(__name__=='__main__'):
    # read password from the file ad pass them here
    file_path=input('Please enter the realtive file to the passwords to check:(please each password should be in a seperate line): ')
    passwords=read_password(file_path)
    main(passwords)