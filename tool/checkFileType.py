import filetype,os

def main():
    path = R"C:\Users\Administrator\Documents\WeChat Files\wxid_pz4ntx0z1a3o22\\"
    list=os.walk(path)
    for a in list: print(a)
    kind=filetype.guess(R'C:\Users\Administrator\Documents\WeChat Files\wxid_pz4ntx0z1a3o22\FileStorage\Video\2022-01\613b34e3b3a29397a3ee2d18e5353250 - 副本.dat')
    if kind is None:
        print("unknow.")
        return
    print(f"extension:{kind.extension},type:{kind.mime}")

if __name__ == '__main__':
    main()

