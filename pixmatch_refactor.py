import streamlit as st
import os
import time as tm
import random
import base64
import json
from PIL import Image
from streamlit_autorefresh import st_autorefresh

# Set page configuration
st.set_page_config(page_title="PixMatch", page_icon="🕹️", layout="wide", initial_sidebar_state="expanded")

# Define paths based on the current drive
vDrive = os.path.splitdrive(os.getcwd())[0]
if vDrive == "C:":
    vpth = "C:/Users/Shawn/dev/utils/pixmatch/"   # Local developer's disc
else:
    vpth = "./"

# HTML templates for styling
# These are HTML templates used to style the appearance of elements in the app.
# They are used later in the code to format how buttons, emoji, and other components appear.
sbe = """<span style='font-size: 140px;
                      border-radius: 7px;
                      text-align: center;
                      display:inline;
                      padding-top: 3px;
                      padding-bottom: 3px;
                      padding-left: 0.4em;
                      padding-right: 0.4em;
                      '>
                      |fill_variable|
                      </span>"""

pressed_emoji = """<span style='font-size: 24px;
                                border-radius: 7px;
                                text-align: center;
                                display:inline;
                                padding-top: 3px;
                                padding-bottom: 3px;
                                padding-left: 0.2em;
                                padding-right: 0.2em;
                                '>
                                |fill_variable|
                                </span>"""

horizontal_bar = "<hr style='margin-top: 0; margin-bottom: 0; height: 1px; border: 1px solid #635985;'><br>"    # thin divider line
purple_btn_colour = """
                        <style>
                            div.stButton > button:first-child {background-color: #4b0082; color:#ffffff;}
                            div.stButton > button:hover {background-color: RGB(0,112,192); color:#ffffff;}
                            div.stButton > button:focus {background-color: RGB(47,117,181); color:#ffffff;}
                        </style>
                    """

# Initialize session state variables
mystate = st.session_state
if "expired_cells" not in mystate:
    mystate.expired_cells = []
if "myscore" not in mystate:
    mystate.myscore = 0
if "plyrbtns" not in mystate:
    mystate.plyrbtns = {}
if "sidebar_emoji" not in mystate:
    mystate.sidebar_emoji = ''
if "emoji_bank" not in mystate:
    mystate.emoji_bank = []
if "GameDetails" not in mystate:
    mystate.GameDetails = ['Medium', 6, 7, '']  # difficulty level, sec interval for autogen, total_cells_per_row_or_col, player name

# Common functions

# Function to reduce gap from the top of the page
def ReduceGapFromPageTop(wch_section='main page'):
    """
    Adjusts the gap from the top of the page to make the layout visually appealing.
    
    Args:
        wch_section (str): Specifies which section of the page to adjust. Options are 'main page', 'sidebar', or 'all'.
    """
    if wch_section == 'main page':
        st.markdown(" <style> div[class^='block-container'] { padding-top: 2rem; } </style> ", True) # main area
    elif wch_section == 'sidebar':
        st.markdown(" <style> div[class^='st-emotion-cache-10oheav'] { padding-top: 0rem; } </style> ", True) # sidebar
    elif wch_section == 'all':
        st.markdown(" <style> div[class^='block-container'] { padding-top: 2rem; } </style> ", True) # main area
        st.markdown(" <style> div[class^='st-emotion-cache-10oheav'] { padding-top: 0rem; } </style> ", True) # sidebar

# Function to manage leaderboard operations
def Leaderboard(what_to_do):
    """
    Manages leaderboard operations such as creation, writing, and reading.
    
    Args:
        what_to_do (str): Specifies the operation to perform on the leaderboard. Options are 'create', 'write', or 'read'.
    """
    if what_to_do == 'create':
        if mystate.GameDetails[3] != '':
            if os.path.isfile(vpth + 'leaderboard.json') == False:
                tmpdict = {}
                json.dump(tmpdict, open(vpth + 'leaderboard.json', 'w'))     # write file

    elif what_to_do == 'write':
        if mystate.GameDetails[3] != '':       # record in leaderboard only if player name is provided
            if os.path.isfile(vpth + 'leaderboard.json'):
                leaderboard = json.load(open(vpth + 'leaderboard.json'))    # read file
                leaderboard_dict_lngth = len(leaderboard)
                    
                leaderboard[str(leaderboard_dict_lngth + 1)] = {'NameCountry': mystate.GameDetails[3], 'HighestScore': mystate.myscore}
                leaderboard = dict(sorted(leaderboard.items(), key=lambda item: item[1]['HighestScore'], reverse=True))  # sort desc

                if len(leaderboard) > 10:           # keep only the top 10 scores
                    leaderboard = dict(list(leaderboard.items())[:10])
                json.dump(leaderboard, open(vpth + 'leaderboard.json', 'w'))     # write file

    elif what_to_do == 'read':
        if os.path.isfile(vpth + 'leaderboard.json'):
            leaderboard = json.load(open(vpth + 'leaderboard.json'))    # read file
            return leaderboard
    else:
        pass

# Class for Game Matrix
class GameMatrix:
    def __init__(self, row_col):
        """
        Initializes the game matrix with a specified number of rows and columns.
        
        Args:
            row_col (int): Number of rows and columns in the game matrix.
        """
        self.row_col = row_col
        self.game_cells = [[random.choice(mystate.emoji_bank) for j in range(row_col)] for i in range(row_col)]

    def display(self):
        """
        Displays the game matrix.
        """
        for rw in range(self.row_col):
            for col in range(self.row_col):
                if rw * self.row_col + col in mystate.expired_cells:
                    st.markdown(sbe.replace("|fill_variable|", "&#128683;"), unsafe_allow_html=True)
                else:
                    st.markdown(sbe.replace("|fill_variable|", self.game_cells[rw][col]), unsafe_allow_html=True)
            st.write("\n")  # add a line break after each row

    def auto_refresh(self, interval):
        """
        Sets up auto-refresh for the game matrix.
        
        Args:
            interval (int): Interval in seconds for auto-refreshing the game matrix.
        """
        st_autorefresh(interval * 1000)  # in milliseconds

# Class for Button Presses
class ButtonPress:
    def __init__(self):
        pass

    def game_refresh(self):
        """
        Updates the game matrix by expiring cells randomly upon button press.
        """
        self.cell_to_expire = random.randint(0, mystate.GameDetails[1] * mystate.GameDetails[1] - 1)
        mystate.expired_cells.append(self.cell_to_expire)
        self.old_cell = self.cell_to_expire
        self.new_cell = -1
        if self.old_cell != self.new_cell:     # if button was pressed before
            mystate.myscore += 1
            self.old_cell = self.new_cell

    def player_btn_display(self):
        """
        Displays the player's button choices.
        """
        self.choices = mystate.emoji_bank
        if mystate.GameDetails[3] != '':
            self.player_name = mystate.GameDetails[3].split(",")[0]
            self.player_country = mystate.GameDetails[3].split(",")[1]
        else:
            self.player_name = 'Anonymous'
            self.player_country = ''
        
        if mystate.GameDetails[0] == 'Easy':
            self.btn_rows = 6
            self.btn_cols = 4
        elif mystate.GameDetails[0] == 'Medium':
            self.btn_rows = 6
            self.btn_cols = 6
        else:
            self.btn_rows = 8
            self.btn_cols = 8

        self.plyrbtns_layout = st.empty()      # create an empty container for player buttons
        self.plyrbtns_layout.markdown("<h3 style='margin-bottom:0px;font-size: 30px;'>Your Button Choices</h3>", unsafe_allow_html=True)
        self.plyrbtns_layout.markdown("<p style='margin-top:0px;font-size: 12px;'><i>Note: Press 'Start' Button to Begin Playing</i></p>", unsafe_allow_html=True)
        
        self.b1, self.b2, self.b3, self.b4, self.b5, self.b6, self.b7, self.b8 = st.columns(self.btn_cols)
        with self.b1:
            if 0 in mystate.plyrbtns:
                st.markdown(pressed_emoji.replace("|fill_variable|", self.choices[mystate.plyrbtns[0]]), unsafe_allow_html=True)
            else:
                st.markdown(sbe.replace("|fill_variable|", self.choices[0]), unsafe_allow_html=True)
        with self.b2:
            if 1 in mystate.plyrbtns:
                st.markdown(pressed_emoji.replace("|fill_variable|", self.choices[mystate.plyrbtns[1]]), unsafe_allow_html=True)
            else:
                st.markdown(sbe.replace("|fill_variable|", self.choices[1]), unsafe_allow_html=True)
        with self.b3:
            if 2 in mystate.plyrbtns:
                st.markdown(pressed_emoji.replace("|fill_variable|", self.choices[mystate.plyrbtns[2]]), unsafe_allow_html=True)
            else:
                st.markdown(sbe.replace("|fill_variable|", self.choices[2]), unsafe_allow_html=True)
        with self.b4:
            if 3 in mystate.plyrbtns:
                st.markdown(pressed_emoji.replace("|fill_variable|", self.choices[mystate.plyrbtns[3]]), unsafe_allow_html=True)
            else:
                st.markdown(sbe.replace("|fill_variable|", self.choices[3]), unsafe_allow_html=True)
        with self.b5:
            if 4 in mystate.plyrbtns:
                st.markdown(pressed_emoji.replace("|fill_variable|", self.choices[mystate.plyrbtns[4]]), unsafe_allow_html=True)
            else:
                st.markdown(sbe.replace("|fill_variable|", self.choices[4]), unsafe_allow_html=True)
        with self.b6:
            if 5 in mystate.plyrbtns:
                st.markdown(pressed_emoji.replace("|fill_variable|", self.choices[mystate.plyrbtns[5]]), unsafe_allow_html=True)
            else:
                st.markdown(sbe.replace("|fill_variable|", self.choices[5]), unsafe_allow_html=True)
        with self.b7:
            if 6 in mystate.plyrbtns:
                st.markdown(pressed_emoji.replace("|fill_variable|", self.choices[mystate.plyrbtns[6]]), unsafe_allow_html=True)
            else:
                st.markdown(sbe.replace("|fill_variable|", self.choices[6]), unsafe_allow_html=True)
        with self.b8:
            if 7 in mystate.plyrbtns:
                st.markdown(pressed_emoji.replace("|fill_variable|", self.choices[mystate.plyrbtns[7]]), unsafe_allow_html=True)
            else:
                st.markdown(sbe.replace("|fill_variable|", self.choices[7]), unsafe_allow_html=True)

# Function to run the game
def run_game():
    """
    Runs the game by displaying the game matrix, player's button choices, and initiating the game logic.
    """
    ReduceGapFromPageTop('main page')  # reduce gap from top of page

    mystate.myscore = 0   # reset score
    mystate.expired_cells = []   # reset expired cells
    mystate.plyrbtns = {i: -1 for i in range(8)}    # reset player button presses

    Leaderboard('read')     # get current leaderboard

    # Initialize game matrix and button presses
    GameMatrix(mystate.GameDetails[1]).display()
    button_press = ButtonPress()

    # Display player button choices
    button_press.player_btn_display()

    # Timer
    tm.sleep(1)
    st.markdown(horizontal_bar, unsafe_allow_html=True)
    timer_txt = st.empty()
    for t in range(3, 0, -1):
        timer_txt.markdown(f"<h2 style='margin-bottom:0px;'>{t}</h2>", unsafe_allow_html=True)
        tm.sleep(1)  # wait for 1 second before displaying the next countdown number
