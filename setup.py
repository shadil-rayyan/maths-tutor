##########################################################################
#    
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

from setuptools import setup, find_packages
import sys
import platform
from pathlib import Path

# Determine platform-specific directories
if sys.platform.startswith('linux'):
    share_dir = '/usr/share'
    bin_dir = '/usr/bin'
elif sys.platform == 'darwin':  # macOS
    share_dir = '/usr/local/share'
    bin_dir = '/usr/local/bin'
elif sys.platform == 'win32':  # Windows
    share_dir = 'D:\shadil\zendalona'
    bin_dir = 'C:/Program Files/MathsTutor'

# Define data files
data_files = [
    (f'{share_dir}/maths-tutor', ['icon.png']),
    ('zendalona/maths-tutor/lessons/',['lessons/add_simple.txt']),
      ('zendalona/maths-tutor/lessons/',['lessons/add_easy.txt']),
      ('zendalona/maths-tutor/lessons/',['lessons/add_med.txt']),
      ('zendalona/maths-tutor/lessons/',['lessons/add_hard.txt']),
      ('zendalona/maths-tutor/lessons/',['lessons/add_chlg.txt']),
      ('zendalona/maths-tutor/lessons/',['lessons/sub_simple.txt']),
      ('zendalona/maths-tutor/lessons/',['lessons/sub_easy.txt']),
      ('zendalona/maths-tutor/lessons/',['lessons/sub_med.txt']),
      ('zendalona/maths-tutor/lessons/',['lessons/sub_hard.txt']),
      ('zendalona/maths-tutor/lessons/',['lessons/sub_chlg.txt']),
      ('zendalona/maths-tutor/lessons/',['lessons/mul_simple.txt']),
      ('zendalona/maths-tutor/lessons/',['lessons/mul_easy.txt']),
      ('zendalona/maths-tutor/lessons/',['lessons/mul_med.txt']),
      ('zendalona/maths-tutor/lessons/',['lessons/mul_hard.txt']),
      ('zendalona/maths-tutor/lessons/',['lessons/mul_chlg.txt']),
      ('zendalona/maths-tutor/lessons/',['lessons/div_simple.txt']),
      ('zendalona/maths-tutor/lessons/',['lessons/div_easy.txt']),
      ('zendalona/maths-tutor/lessons/',['lessons/div_med.txt']),
      ('zendalona/maths-tutor/lessons/',['lessons/div_hard.txt']),
      ('zendalona/maths-tutor/lessons/',['lessons/div_chlg.txt']),
      ('zendalona/maths-tutor/lessons/',['lessons/per_simple.txt']),
      ('zendalona/maths-tutor/lessons/',['lessons/per_easy.txt']),
      ('zendalona/maths-tutor/lessons/',['lessons/per_med.txt']),


      ('zendalona/maths-tutor/images/',['images/excellent-1.gif']),
      ('zendalona/maths-tutor/images/',['images/excellent-2.gif']),
      ('zendalona/maths-tutor/images/',['images/excellent-3.gif']),
      ('zendalona/maths-tutor/images/',['images/finished-1.gif']),
      ('zendalona/maths-tutor/images/',['images/finished-2.gif']),
      ('zendalona/maths-tutor/images/',['images/finished-3.gif']),
      ('zendalona/maths-tutor/images/',['images/good-1.gif']),
      ('zendalona/maths-tutor/images/',['images/good-2.gif']),
      ('zendalona/maths-tutor/images/',['images/good-3.gif']),
      ('zendalona/maths-tutor/images/',['images/not-bad-1.gif']),
      ('zendalona/maths-tutor/images/',['images/not-bad-2.gif']),
      ('zendalona/maths-tutor/images/',['images/not-bad-3.gif']),
      ('zendalona/maths-tutor/images/',['images/okay-1.gif']),
      ('zendalona/maths-tutor/images/',['images/okay-2.gif']),
      ('zendalona/maths-tutor/images/',['images/okay-3.gif']),
      ('zendalona/maths-tutor/images/',['images/question-1.gif']),
      ('zendalona/maths-tutor/images/',['images/question-2.gif']),
      ('zendalona/maths-tutor/images/',['images/very-good-1.gif']),
      ('zendalona/maths-tutor/images/',['images/very-good-2.gif']),
      ('zendalona/maths-tutor/images/',['images/very-good-3.gif']),
      ('zendalona/maths-tutor/images/',['images/welcome-1.gif']),
      ('zendalona/maths-tutor/images/',['images/welcome-2.gif']),
      ('zendalona/maths-tutor/images/',['images/welcome-3.gif']),
      ('zendalona/maths-tutor/images/',['images/wrong-anwser-1.gif']),
      ('zendalona/maths-tutor/images/',['images/wrong-anwser-2.gif']),
      ('zendalona/maths-tutor/images/',['images/wrong-anwser-3.gif']),
      ('zendalona/maths-tutor/images/',['images/wrong-anwser-repeted-1.gif']),
      ('zendalona/maths-tutor/images/',['images/wrong-anwser-repeted-2.gif']),

      ('zendalona/maths-tutor/sounds/',['sounds/backgroundmusic.ogg']),
      ('zendalona/maths-tutor/sounds/',['sounds/coin.ogg']),
      ('zendalona/maths-tutor/sounds/',['sounds/excellent-1.ogg']),
      ('zendalona/maths-tutor/sounds/',['sounds/excellent-2.ogg']),
      ('zendalona/maths-tutor/sounds/',['sounds/excellent-3.ogg']),
      ('zendalona/maths-tutor/sounds/',['sounds/finished-1.ogg']),
      ('zendalona/maths-tutor/sounds/',['sounds/finished-2.ogg']),
      ('zendalona/maths-tutor/sounds/',['sounds/finished-3.ogg']),
      ('zendalona/maths-tutor/sounds/',['sounds/good-1.ogg']),
      ('zendalona/maths-tutor/sounds/',['sounds/good-2.ogg']),
      ('zendalona/maths-tutor/sounds/',['sounds/good-3.ogg']),
      ('zendalona/maths-tutor/sounds/',['sounds/not-bad-1.ogg']),
      ('zendalona/maths-tutor/sounds/',['sounds/not-bad-2.ogg']),
      ('zendalona/maths-tutor/sounds/',['sounds/not-bad-3.ogg']),
      ('zendalona/maths-tutor/sounds/',['sounds/okay-1.ogg']),
      ('zendalona/maths-tutor/sounds/',['sounds/okay-2.ogg']),
      ('zendalona/maths-tutor/sounds/',['sounds/okay-3.ogg']),
      ('zendalona/maths-tutor/sounds/',['sounds/question.ogg']),
      ('zendalona/maths-tutor/sounds/',['sounds/very-good-1.ogg']),
      ('zendalona/maths-tutor/sounds/',['sounds/very-good-2.ogg']),
      ('zendalona/maths-tutor/sounds/',['sounds/very-good-3.ogg']),
      ('zendalona/maths-tutor/sounds/',['sounds/welcome.ogg']),
      ('zendalona/maths-tutor/sounds/',['sounds/wrong-anwser-1.ogg']),
      ('zendalona/maths-tutor/sounds/',['sounds/wrong-anwser-2.ogg']),
      ('zendalona/maths-tutor/sounds/',['sounds/wrong-anwser-3.ogg']),
      ('zendalona/maths-tutor/sounds/',['sounds/wrong-anwser-repeted-1.ogg']),
      ('zendalona/maths-tutor/sounds/',['sounds/wrong-anwser-repeted-2.ogg']),
      ('zendalona/maths-tutor/sounds/',['sounds/wrong-anwser-repeted-3.ogg']),

      ('zendalona/locale/ml/LC_MESSAGES',['locale/ml/LC_MESSAGES/Maths-Tutor.mo']),
      ('zendalona/locale/en/LC_MESSAGES',['locale/en/LC_MESSAGES/Maths-Tutor.mo']),
      ('zendalona/locale/ta/LC_MESSAGES',['locale/ta/LC_MESSAGES/Maths-Tutor.mo']),
      ('zendalona/locale/hi/LC_MESSAGES',['locale/hi/LC_MESSAGES/Maths-Tutor.mo']),
      ('zendalona/locale/ar/LC_MESSAGES',['locale/ar/LC_MESSAGES/Maths-Tutor.mo']),
      ('zendalona/locale/sa/LC_MESSAGES',['locale/sa/LC_MESSAGES/Maths-Tutor.mo']),

      ('zendalona/maths-tutor/',['user-manual.html']),

      ('zendalona/applications/',['maths-tutor.desktop']),
      ('bin/',['maths-tutor'])]

setup(
    name='MathsTutor',
    version='1.0',
    description='Game for learning mathematical operations',
    author='Roopasree AP',
    author_email='roopasreeap@gmail.com',
    url='https://github.com/roopasreeap/Maths-Tutor',
    license='GPL-3',
    packages=find_packages(),
    data_files=data_files,
)
