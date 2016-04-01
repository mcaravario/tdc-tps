import os.path
import argparse
import string

# verifies that testname parameter is valid
def check_testname_ok(f):
  if '/' in f or '.' in f:
    raise argparse.ArgumentTypeError('''Invalid testname.
    Please, don't use "/" nor "." in your testname.
    Valid testnames, ie: "shopping1", "trabajo5", "casa2", etc.''')

# check if a filepath is a file
def check_filepath_isfile(f):
  global parser
  if not os.path.isfile(f):
    raise argparse.ArgumentTypeError('File %s does not exists'%f)

# to check pcap input
def file_pcap(f):
  check_testname_ok(f)
  y = '../output/'+f+'.pcap'
  check_filepath_isfile(y)
  return y

# to check json input
def file_json_s(f):
  check_testname_ok(f)
  y = '../output/'+f+'-s.json'
  check_filepath_isfile(y)
  return y
def file_json_s1(f):
  check_testname_ok(f)
  y = '../output/'+f+'-s1.json'
  check_filepath_isfile(y)
  return y

# given a file path, replaces the extension
def replace_ext(file,newext):
  root,ext = os.path.splitext(file)
  return root+"."+newext

# given a file path, returns a png filepath
def output_testtype_ext(file,testtype,newext):
  root,ext = os.path.splitext(file)
  return root+"-"+testtype+"."+newext


# check sudo
def check_sudo():
  if os.getuid() != 0:
    raise RuntimeError("You need to run this script with sudo!")

def make_unused_letter():
    unused_letters = list(string.ascii_uppercase)
    unused_letters.reverse()
    def unused_letter():
        return unused_letters.pop()
    return unused_letter

unused_letter = make_unused_letter()
          
