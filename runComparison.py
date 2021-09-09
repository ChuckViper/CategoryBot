import SrcCdeAnalysis
import webbrowser
from bs4 import BeautifulSoup
import urllib.request

def main():
    print()
    cat = input(SrcCdeAnalysis.chooseCat())
    catN = []
   
    if cat.find("dog") > -1:
        catN = SrcCdeAnalysis.catDog
    elif cat.find("travel") > -1:
        catN = SrcCdeAnalysis.catTravel
    elif cat.find("nature") > -1:
        catN = SrcCdeAnalysis.catNature

    SrcCdeAnalysis.searchCat(catN)

if __name__ == "__main__":
    main()