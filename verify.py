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
import time


def char20(input):
    try:
        if len(input) > 20 or len(input) == 0:
            return False
        else:
            return True

    except:
        return False


def char4(input):
    try:
        if len(input) > 4 or len(input) == 0:
            return False
        else:
            return True

    except:
        return False


def rowSelection(entry, max):
    try:
        if 1 <= int(entry) <= max and max!=0:
            return True
        else:
            return False
    except:
        return False


def isTimeFormat(input):
    try:
        time.strptime(input, '%H:%M')
        return True
    except ValueError:
        return False

def isDateFormat(input):
    try:
        time.strptime(input, '%d-%m-%Y')
        return True
    except ValueError:
        return False