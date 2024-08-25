from pecab import PeCab
import os

def main():
    pecab = PeCab()

    morphs = pecab.morphs("아버지가방에들어가시다.")
    print(morphs)

    srcPath = os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
    print(srcPath)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()