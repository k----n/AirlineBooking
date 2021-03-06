#
#   Copyright 2015 Kalvin Eng
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
import os

def main(user):
    clearScreen()
    if user.agent:
        print(
                "Main Menu\n" +
                "-------------------------\n" +
                "Select an option:\n" +
                "0 - Search/Book a flight\n" +
                "1 - List existing booking(s)\n" +
                "2 - Logout\n" +
                "3 - Record flight departure\n" +
                "4 - Record flight arrival\n" +
                "-------------------------\n")
        entries = [x for x in range(5)]
        while True:
            option = input("Option: ")

            if option == "0":
                return 0

            elif option == "1":
                return 1

            elif option == "2":
                return 2

            elif option == "3":
                return 3

            elif option == "4":
                return 4

            elif option not in entries:
                print("Invalid input, try again\n")
    else:
        print(
            "Main Menu\n" +
            "-------------------------\n" +
            "Select an option:\n" +
            "0 - Search/Book a flight\n" +
            "1 - List existing booking(s)\n" +
            "2 - Logout\n" +
            "-------------------------\n")
        entries = [x for x in range(3)]
        while True:
            option = input("Option: ")

            if option == "0":
                return 0

            elif option == "1":
                return 1

            elif option == "2":
                return 2

            elif option not in entries:
                print("Invalid input, try again\n")


def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')

