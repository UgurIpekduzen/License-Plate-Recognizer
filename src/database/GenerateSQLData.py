from UIScreens import UIScreens
import UISwitchers as uisw

def main():
    dbui = UIScreens()
    switcher = None
    while True:
        if dbui.strMenuName is "mainmenuscr":
            switcher = uisw.mainMenuSwitchers
            dbui.mainMenuScreen()
        # end if
        elif dbui.strMenuName is "insertionscr":
            switcher = uisw.insertionSwitchers
            dbui.insertionScreen()
        # end elif
        elif dbui.strMenuName is "deletionscr":
            switcher = uisw.deletionSwitchers
            dbui.deletionScreen()
        # end elif
        elif dbui.strMenuName is "selectionscr":
            switcher = uisw.selectionSwitchers
            dbui.selectionScreen()
        # end elif
        elif dbui.strMenuName is "deleteallscr":
            dbui.deleteAllScreen()
        # end elif
        elif dbui.strMenuName is "deleteonescr":
            dbui.deleteOneScreen()
        # end elif
        elif dbui.strMenuName is "selectallscr":
            dbui.selectAllScreen()
        # end elif
        elif dbui.strMenuName is "selectonescr":
            dbui.selectOneScreen()
        # end elif
        intSelectionScreen = int(input())
        dbui.strMenuName = uisw.switch(switcher, intSelectionScreen)

    # end while
# end function

if __name__ == "__main__":
    main()
#end if



