def mainmenuscr():
    return "mainmenuscr"

def insertionscr():
    return "insertionscr"

def deletionscr():
    return "deletionscr"

def selectionscr():
    return "selectionscr"

def deleteallscr():
    return "deleteallscr"

def deleteonescr():
    return "deleteonescr"

def selectallscr():
    return "selectallscr"

def selectonescr():
    return "selectonescr"

def default():
    print("Hatalı giriş yaptınız lütfen tekrar deneyiniz:")

mainMenuSwitchers = {
    0: mainmenuscr,
    1: insertionscr,
    2: selectionscr,
    3: deletionscr,
}

insertionSwitchers = {
    0: mainmenuscr,
}

selectionSwitchers = {
    0: mainmenuscr,
    1: selectallscr,
    2: selectonescr,
    3: selectionscr
}

deletionSwitchers = {
    0: mainmenuscr,
    1: deleteallscr,
    2: deleteonescr,
    3: deletionscr
}

def switch(switcher, screenSelection):
    return switcher.get(screenSelection, default)()
