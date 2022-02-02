# def NAME(self, query):
#   do stuff
#   return htmlFileIndex


def homePage(self, query):
    if query:
        if query["auth"]:
            if query["auth"]=="69":
                return 0
            else:
                return 1
        else:
            return 1
    else:
        return 1

def exitPage(self, query):
    if query:
        if query["auth"]:
            if query["auth"]=="420":
                return 0
            else:
                return 1
        else:
            return 1
    else:
        return 1