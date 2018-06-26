import os


def GetWorkingDirectory():
    return os.path.dirname(os.path.abspath(__file__))
    # Gets the working directory - avoids any issues that may occur


def CheckDirectoryExists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def DirectoryCheck(directory):
    here = GetWorkingDirectory()
    CheckDirectoryExists(here + "/input")
    CheckDirectoryExists(here + "/output")
    # Checks to see if there is an input and output, if not, it creates them


def GetInputFiles():
    return os.listdir(GetWorkingDirectory() + "/input")


def GetUserInputs():
    while True:
        try:
            backgroundHeight = int(
                input(
                    "\nPlease enter the height (in pixels) "
                    "for your edited images: "
                )
            )
            if backgroundHeight > 10000 or backgroundHeight < 1:
                raise ValueError

            backgroundWidth = int(
                input(
                    "Please enter the width (in pixels) "
                    "for your edited images: "
                )
            )
            if backgroundWidth > 10000 or backgroundWidth < 1:
                raise ValueError

            tolerance = float(
                input(
                    "\n(Recommened 0.8 for most images)"
                    "\n(Increase if not detecting edges)"
                    "\n(Decrease if detecting too far away from object"
                    "\nPlease enter a tolerance between 0 and 1: "
                )
            )
            if tolerance > 1 or tolerance < 0:
                raise ValueError

            borderPercentage = float(
                input(
                    "\n(Recommended 0.05 for most images)"
                    "\n(Increase if you find objects strechting)"
                    "\nPlease enter a border percentage between 0 and 1: "
                )
            )
            if borderPercentage > 1 or borderPercentage < 0:
                raise ValueError

            print("\n")
            break
        except ValueError:
            print("\nOops! That was not a valid number. Try again...")
            # Throws an error if the user did not enter an integer
    return backgroundHeight, backgroundWidth, tolerance, borderPercentage


def CheckImageExists(directory, debug=True):
        if (
            os.path.exists(directory) and
            (
                (
                    directory.endswith(".jpg") or
                    directory.endswith(".jpeg") or
                    directory.endswith(".png")
                )
            )
        ):
            return True
        else:
            if debug:
                print(
                    directory +
                    " cannot be found or the image "
                    "is not in the JPEG or PNG format!"
                )
            return False
