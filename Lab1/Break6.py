import hashlib
import subprocess
import time

# directory: /home/cse/Lab1/Q6/

def format_data(salted_pws):
  user_salt_dict = {}
  user_pw_dict = {}
  for line in salted_pws:
    user, salt, password  = line.split(",")
    user_salt_dict[user] = salt
    user_pw_dict[user] = password
  return user_salt_dict, user_pw_dict


def my_hash(password):
  sha256 = hashlib.sha256()
  sha256.update(password.encode())
  string_hash = sha256.hexdigest()
  return string_hash


def login(username, password):
  result = subprocess.run(["python3", "Login.pyc", username, password], capture_output=True, text=True, cwd = "/home/cse/Lab1/Q6/")
  if result.stdout == "Login successful.\n":
    print(result.stdout.strip())
    print(f"Username '{username}': Password '{password}'")
    end = time.time()
    print(f"Time taken to find gang member: {end - start}")
    print()
    return True
  return False


def find_password(user, passwords, user_salt_dict, user_pw_dict, output_file):
  target_pw = user_pw_dict[user]
  salt = user_salt_dict[user]
  for password in passwords:
    for digit in range(10):
      new_pw = str(salt) + password + str(digit)
      new_pw1 = password + str(digit)
      print(f'Attempting: {new_pw}')
      hashed_pw = my_hash(new_pw)
      if hashed_pw == target_pw:
        if login(user, new_pw1):
          with open(output_file, "a") as f:
            f.write(f"Username: {user}, Password: {new_pw1}\n")
          return True
  return False


def intersection(lst1, lst2):
  return list(set(lst1) & set(lst2))


if __name__ == "__main__":
  start = time.time()
  print("Running Program")
  print("Searching for passwords...")
  print(f"\nProgram start time: {start - start}")

  with open('/home/cse/Lab1/Q6/PwnedPWs100k') as f:
    passwords = [line.rstrip('\n') for line in f]
  f.close()
  
  with open('/home/cse/Lab1/Q6/SaltedPWs') as f:
    salted_pws = [line.rstrip('\n') for line in f]
  f.close()
  
  with open('/home/cse/Lab1/Q6/gang') as f:
    gang = [line.rstrip('\n') for line in f]
  f.close()
  
  user_salt_dict = {}
  user_pw_dict = {}
  for line in salted_pws:
    user, salt, password  = line.split(",")
    user_salt_dict[user] = salt
    user_pw_dict[user] = password

  gang_members = list(user_salt_dict.keys())
  login_status = False

  the_gang = intersection(gang_members, gang)
 
  output_file = "/home/cse/Lab1/Q6/discovered_passwords.txt"
  with open(output_file, "w") as f:
    f.write("Discovered Passwords:\n")


  for member in the_gang:
    if find_password(member, passwords, user_salt_dict, user_pw_dict, output_file):
      login_status = True
      break

  if not login_status:
    print("No Successful Login Attempts")

  end = time.time()
  print(f"\nProgram End Time: {end - start}")
