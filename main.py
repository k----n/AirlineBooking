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
import setup
import database
import login
import menu

def main():
    connection_url = "@gwynne.cs.ualberta.ca:1521/CRS"
    database_spec = "table_definitions.sql"
    drop_tables = "drop_tables.sql"

    # connect to database
    connection = database.connect(connection_url)

    # mode 0 to ignore, 1 for fresh setup
    setup.createTable(0, connection, database_spec, drop_tables)

    while True:
        # login screen
        user = login.login(connection)
        option = ""

        while option != 2:
            # main menu
            option = menu.main(user)
            database.process(option, connection, user)

        database.process(option, connection, user)


if __name__ == "__main__":
    main()
