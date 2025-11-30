import rusty_pstore

def main():
    print('CREATING DEFAULT ADMIN')
    rusty_pstore.init_pass_file('YWRtaW4=', 'password') # admin, password

if __name__ == '__main__':
    main()