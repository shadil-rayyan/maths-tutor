###########################################################################
#    Maths-Tutor
#
#    Copyright (C) 2022-2023 Greeshna Sarath <greeshnamohan001@gmail.com>    
#    
#    This project is Supervised by Zendalona(2022-2023)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
###########################################################################
import os

data_dir = "D:\shadil\zendalona\maths-tutor"
locale_dir = "D:\shadil\zendalona\maths-tutor\locale"
app_name = "Maths-Tutor"

# Check if 'HOME' environment variable exists
if 'HOME' in os.environ:
    user_preferences_file_path = os.path.join(os.environ['HOME'], '.maths-tutor.cfg')
else:
    # Fallback to using the user's directory
    user_preferences_file_path = os.path.expanduser('~/.maths-tutor.cfg')

user_guide_file_path = os.path.join(data_dir, "user-manual.html")
