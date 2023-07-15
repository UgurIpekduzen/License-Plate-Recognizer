from UIScreens import UIScreens
import UISwitchers as uisw

def main():
    dbui = UIScreens()
    switcher = None
    while True:
        if dbui.strMenuName == "mainmenuscr":
            switcher = uisw.mainMenuSwitchers
            dbui.mainMenuScreen()
        # end if
        elif dbui.strMenuName == "insertionscr":
            switcher = uisw.insertionSwitchers
            dbui.insertionScreen()
        # end elif
        elif dbui.strMenuName == "deletionscr":
            switcher = uisw.deletionSwitchers
            dbui.deletionScreen()
        # end elif
        elif dbui.strMenuName == "selectionscr":
            switcher = uisw.selectionSwitchers
            dbui.selectionScreen()
        # end elif
        elif dbui.strMenuName == "deleteallscr":
            dbui.deleteAllScreen()
        # end elif
        elif dbui.strMenuName == "deleteonescr":
            dbui.deleteOneScreen()
        # end elif
        elif dbui.strMenuName == "selectallscr":
            dbui.selectAllScreen()
        # end elif
        elif dbui.strMenuName == "selectonescr":
            dbui.selectOneScreen()
        # end elif
        elif dbui.strMenuName == "updatescr":
            dbui.updateScreen()
        # end elif
        intSelectionScreen = int(input())
        dbui.strMenuName = uisw.switch(switcher, intSelectionScreen)
    # end while
# end function

if __name__ == "__main__":
    main()
#end if



