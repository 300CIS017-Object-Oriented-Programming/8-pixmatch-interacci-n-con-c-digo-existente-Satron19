import streamlit as st
import os
import time as tm
import random
import base64
import json
from PIL import Image
from streamlit_autorefresh import st_autorefresh

# General page attributes configuration
st.set_page_config(page_title="PixMatch", page_icon="🕹️", layout="wide", initial_sidebar_state="expanded")

# Get the disk drive where the current directory is located
vDrive = os.path.splitdrive(os.getcwd())[0]

# Set the local developer directory path
if vDrive == "C:":
    vpth = "C:/Users/Shawn/dev/utils/pixmatch/"   # local developer's disk
else:
    vpth = "./"

# Create a template for large text style
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

# Create a template for emoji style
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

# Thin horizontal divider
horizontal_bar = "<hr style='margin-top: 0; margin-bottom: 0; height: 1px; border: 1px solid #635985;'><br>"

# Style for purple button color
purple_btn_colour = """
                        <style>
                            div.stButton > button:first-child {background-color: #4b0082; color:#ffffff;}
                            div.stButton > button:hover {background-color: RGB(0,112,192); color:#ffffff;}
                            div.stButton > button:focus {background-color: RGB(47,117,181); color:#ffffff;}
                        </style>
                    """

# Session state
mystate = st.session_state

# Initialize session state keys if they don't exist
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
    mystate.GameDetails = ['Medium', 6, 7, '']  # Difficulty level, autogeneration interval in seconds, total cells per row or column, player name

# Common functions

def ReduceGapFromPageTop(wch_section='main page'):
    """
    Reduce the space from the top of the page by adjusting the padding of the specified section.
    """
    if wch_section == 'main page':
        # Main area
        st.markdown(" <style> div[class^='block-container'] { padding-top: 2rem; } </style> ", True)
    elif wch_section == 'sidebar':
        # Sidebar
        st.markdown(" <style> div[class^='st-emotion-cache-10oheav'] { padding-top: 0rem; } </style> ", True)
    elif wch_section == 'all':
        # Main area
        st.markdown(" <style> div[class^='block-container'] { padding-top: 2rem; } </style> ", True)
        # Sidebar
        st.markdown(" <style> div[class^='st-emotion-cache-10oheav'] { padding-top: 0rem; } </style> ", True)


def Leaderboard(what_to_do):
    """
    Manage the creation, writing, and reading of the leaderboard.
    Parameters:
        what_to_do: a string representing the action to perform ('create' to create, 'write' to write, 'read' to read).
    """
    if what_to_do == 'create':
        # Create a leaderboard file if it doesn't exist and the player name is available
        if mystate.GameDetails[3] != '':
            if os.path.isfile(vpth + 'leaderboard.json') == False:
                tmpdict = {}
                json.dump(tmpdict, open(vpth + 'leaderboard.json', 'w'))  # write file

    elif what_to_do == 'write':
        # Write to the leaderboard if the player name is available
        if mystate.GameDetails[3] != '':
            if os.path.isfile(vpth + 'leaderboard.json'):
                leaderboard = json.load(open(vpth + 'leaderboard.json'))  # read file
                leaderboard_dict_lngth = len(leaderboard)

                leaderboard[str(leaderboard_dict_lngth + 1)] = {'NameCountry': mystate.GameDetails[3],'HighestScore': mystate.myscore}
                leaderboard = dict(sorted(leaderboard.items(), key=lambda item: item[1]['HighestScore'], reverse=True))  # sort descending

                if len(leaderboard) > 4:
                    for i in range(len(leaderboard) - 4):
                        leaderboard.popitem()

                json.dump(leaderboard, open(vpth + 'leaderboard.json', 'w'))  # write to file

    elif what_to_do == 'read':
        # Read the leaderboard if the player name is available
        if mystate.GameDetails[3] != '':
            if os.path.isfile(vpth + 'leaderboard.json'):
                leaderboard = json.load(open(vpth + 'leaderboard.json'))  # read file

                leaderboard = dict(sorted(leaderboard.items(), key=lambda item: item[1]['HighestScore'], reverse=True))  # sort descending

                sc0, sc1, sc2, sc3, sc4 = st.columns((2, 3, 3, 3, 3))
                rknt = 0
                for vkey in leaderboard.keys():
                    if leaderboard[vkey]['NameCountry'] != '':
                        rknt += 1
                        if rknt == 1:
                            sc0.write('🏆 Past Winners:')
                            sc1.write(f"🥇 | {leaderboard[vkey]['NameCountry']}: :red[{leaderboard[vkey]['HighestScore']}]")
                        elif rknt == 2:
                            sc2.write(f"🥈 | {leaderboard[vkey]['NameCountry']}: :red[{leaderboard[vkey]['HighestScore']}]")
                        elif rknt == 3: sc3.write(f"🥉 | {leaderboard[vkey]['NameCountry']}: :red[{leaderboard[vkey]['HighestScore']}]")
                        elif rknt == 4:
                            sc4.write(f"🥉 | {leaderboard[vkey]['NameCountry']}: :red[{leaderboard[vkey]['HighestScore']}]")

def InitialPage():
    """
       Define the initial page of the Pix Match game.
    """
    with st.sidebar:
        st.subheader("🖼️ Pix Match:")
        st.markdown(horizontal_bar, True)

        # sidebarlogo = Image.open('sidebarlogo.jpg').resize((300, 420))
        sidebarlogo = Image.open('sidebarlogo.jpg').resize((300, 390))
        st.image(sidebarlogo, use_column_width='auto')
# ViewHelp
hlp_dtl = f"""<span style="font-size: 26px;">
<ol>
<li style="font-size:15px";>The game starts with (a) a sidebar picture and (b) an N x N grid of picture buttons, where N=6:Easy, N=7:Medium, N=8:Hard.</li>
<li style="font-size:15px";>You need to match the sidebar picture with a grid picture button by pressing the matching button as quickly as possible.</li>
<li style="font-size:15px";>Each correct picture match earns you <strong>+N</strong> points (where N=5:Easy, N=3:Medium, N=1:Hard); each incorrect picture match earns you <strong>-1</strong> point.</li>
<li style="font-size:15px";>The sidebar picture and the grid pictures will dynamically regenerate after a fixed interval (Easy=8 seconds, Medium=6 seconds, Hard=5 seconds). Each regeneration incurs a penalty of <strong>-1</strong> point.</li>
<li style="font-size:15px";>Each grid button can only be pressed once during the entire game.</li>
<li style="font-size:15px";>The game ends when all grid buttons are pressed.</li>
<li style="font-size:15px";>At the end of the game, if you have a positive score, you win; otherwise, you lose.</li>
</ol></span>""" 

sc1, sc2 = st.columns(2)
random.seed()
GameHelpImg = vpth + random.choice(["MainImg1.jpg", "MainImg2.jpg", "MainImg3.jpg", "MainImg4.jpg"])
GameHelpImg = Image.open(GameHelpImg).resize((550, 550))
sc2.image(GameHelpImg, use_column_width='auto')

sc1.subheader('Rules | Playing Instructions:')
sc1.markdown(horizontal_bar, True)
sc1.markdown(hlp_dtl, unsafe_allow_html=True)
st.markdown(horizontal_bar, True)

author_dtl = "<strong>Happy Playing: 😎 Shawn Pereira: shawnpereira1969@gmail.com</strong>"
st.markdown(author_dtl, unsafe_allow_html=True)

def ReadPictureFile(wch_fl):
    """
    Reads an image file and returns its base64 representation.
    """
    try:
        pxfl = f"{vpth}{wch_fl}"  # Get the full path of the image file.
        return base64.b64encode(open(pxfl, 'rb').read()).decode()  # Read the image file, encode it in base64, and return as a string.

    except:
        return ""  # Return an empty string if there's any error while reading the image file.


def PressedCheck(vcell):
    """
    Checks if a cell button has been pressed and performs corresponding actions.
    """
    if mystate.plyrbtns[vcell]['isPressed'] == False:  # Check if the cell button has not been pressed yet.
        mystate.plyrbtns[vcell]['isPressed'] = True  # Mark the cell button as pressed.
        mystate.expired_cells.append(vcell)  # Add the cell index to the list of expired cells.

        if mystate.plyrbtns[vcell][
            'eMoji'] == mystate.sidebar_emoji:  # Check if the button emoji matches the sidebar emoji.
            mystate.plyrbtns[vcell]['isTrueFalse'] = True  # Mark the result as true.
            mystate.myscore += 5  # Increase the score by 5 points.

            # Adjust the score based on the game difficulty.
            if mystate.GameDetails[0] == 'Easy':
                mystate.myscore += 5
            elif mystate.GameDetails[0] == 'Medium':
                mystate.myscore += 3
            elif mystate.GameDetails[0] == 'Hard':
                mystate.myscore += 1

        else:  # If the button emoji does not match the sidebar emoji.
            mystate.plyrbtns[vcell]['isTrueFalse'] = False  # Mark the result as false.
            mystate.myscore -= 1  # Decrease the score by 1 point.


def ResetBoard():
    """
    Resets the game board.
    """
    total_cells_per_row_or_col = mystate.GameDetails[2]  # Get the total number of cells per row or column.

    # Select a random emoji for the sidebar.
    sidebar_emoji_no = random.randint(1, len(mystate.emoji_bank)) - 1
    mystate.sidebar_emoji = mystate.emoji_bank[sidebar_emoji_no]

    sidebar_emoji_in_list = False  # Flag to check if the sidebar emoji is in the button emoji list.

    # Assign random emojis to buttons that have not been pressed yet.
    for vcell in range(1, ((total_cells_per_row_or_col ** 2) + 1)):
        rndm_no = random.randint(1, len(mystate.emoji_bank)) - 1
        if mystate.plyrbtns[vcell]['isPressed'] == False:
            vemoji = mystate.emoji_bank[rndm_no]
            mystate.plyrbtns[vcell]['eMoji'] = vemoji
            if vemoji == mystate.sidebar_emoji:
                sidebar_emoji_in_list = True

    # If the sidebar emoji is not in the button emoji list, randomly add it to a button.
    if sidebar_emoji_in_list == False:
        tlst = [x for x in range(1, ((total_cells_per_row_or_col ** 2) + 1))]
        flst = [x for x in tlst if x not in mystate.expired_cells]
        if len(flst) > 0:
            lptr = random.randint(0, (len(flst) - 1))
            lptr = flst[lptr]
            mystate.plyrbtns[lptr]['eMoji'] = mystate.sidebar_emoji
def PreNewGame():
    """
    Prepare the game for a new round.
    """
    total_cells_per_row_or_col = mystate.GameDetails[2]  # Get the total number of cells per row or column.
    # Reset the list of expired cells and the player's score.
    mystate.expired_cells = []
    mystate.myscore = 0
    # Define lists of emojis for each difficulty level.
    foxes = ['😺', '😸', '😹', '😻', '😼', '😽', '🙀', '😿', '😾']
    emojis = ['😃', '😄', '😁', '😆', '😅', '😂', '🤣', '😊', '😇', '🙂', '🙃', '😉', '😌', '😍', '🥰', '😘', '😗', '😙', '😚', '😋', '😛', '😝', '😜', '🤪', '🤨', '🧐', '🤓', '😎', '🤩', '🥳', '😏', '😒', '😞', '😔', '😟', '😕', '🙁', '☹️', '😣', '😖', '😫', '😩', '🥺', '😢', '😠', '😳', '😥', '😓', '🤗', '🤔', '🤭', '🤫', '🤥', '😶', '😐', '😑', '😬', '🙄', '😯', '😧', '😮', '😲', '🥱', '😴', '🤤', '😪', '😵', '🤐', '🥴', '🤒']
    humans = ['👶', '👧', '🧒', '👦', '👩', '🧑', '👨', '👩‍🦱', '👨‍🦱', '👩‍🦰', '‍👨', '👱', '👩', '👱', '👩‍', '👨‍🦳', '👩‍🦲', '👵', '🧓', '👴', '👲', '👳']
    foods = ['🍏', '🍎', '🍐', '🍊', '🍋', '🍌', '🍉', '🍇', '🍓', '🍈', '🍒', '🍑', '🥭', '🍍', '🥥', '🥝', '🍅', '🍆', '🥑', '🥦', '🥬', '🥒', '🌽', '🥕', '🧄', '🧅', '🥔', '🍠', '🥐', '🥯', '🍞', '🥖', '🥨', '🧀', '🥚', '🍳', '🧈', '🥞', '🧇', '🥓', '🥩', '🍗', '🍖', '🦴', '🌭', '🍔', '🍟', '🍕']
    clocks = ['🕓', '🕒', '🕑', '🕘', '🕛', '🕚', '🕖', '🕙', '🕔', '🕤', '🕠', '🕕', '🕣', '🕞', '🕟', '🕜', '🕢', '🕦']
    hands = ['🤚', '🖐', '✋', '🖖', '👌', '🤏', '✌️', '🤞', '🤟', '🤘', '🤙', '👈', '👉', '👆', '🖕', '👇', '☝️', '👍', '👎', '✊', '👊', '🤛', '🤜', '👏', '🙌', '🤲', '🤝', '🤚🏻', '🖐🏻', '✋🏻', '🖖🏻', '👌🏻', '🤏🏻', '✌🏻', '🤞🏻', '🤟🏻', '🤘🏻', '🤙🏻', '👈🏻', '👉🏻', '👆🏻', '🖕🏻', '👇🏻', '☝🏻', '👍🏻', '👎🏻', '✊🏻', '👊🏻', '🤛🏻', '🤜🏻', '👏🏻', '🙌🏻', '🤚🏽', '🖐🏽', '✋🏽', '🖖🏽', '👌🏽', '🤏🏽', '✌🏽', '🤞🏽', '🤟🏽', '🤘🏽', '🤙🏽', '👈🏽', '👉🏽', '👆🏽', '🖕🏽', '👇🏽', '☝🏽', '👍🏽', '👎🏽', '✊🏽', '👊🏽', '🤛🏽', '🤜🏽', '👏🏽', '🙌🏽']
    animals = ['🐶', '🐱', '🐭', '🐹', '🐰', '🦊', '🐻', '🐼', '🐨', '🐯', '🦁', '🐮', '🐷', '🐽', '🐸', '🐵', '🙈', '🙉', '🙊', '🐒', '🐔', '🐧', '🐦', '🐤', '🐣', '🐥', '🦆', '🦅', '🦉', '🦇', '🐺', '🐗', '🐴', '🦄', '🐝', '🐛', '🦋', '🐌', '🐞', '🐜', '🦟', '🦗', '🦂', '🐢', '🐍', '🦎', '🦖', '🦕', '🐙', '🦑', '🦐', '🦞', '🦀', '🐡', '🐠', '🐟', '🐬', '🐳', '🐋', '🦈', '🐊', '🐅', '🐆', '🦓', '🦍', '🦧', '🐘', '🦛', '🦏', '🐪', '🐫', '🦒', '🦘', '🐃', '🐂', '🐄', '🐎', '🐖', '🐏', '🐑', '🦙', '🐐', '🦌', '🐕', '🐩', '🦮', '🐕‍🦺', '🐈', '🐓', '🦃', '🦚', '🦜', '🦢', '🦩', '🐇', '🦝', '🦨', '🦦', '🦥', '🐁', '🐀', '🦔']
    vehicles = ['🚗', '🚕', '🚙', '🚌', '🚎', '🚓', '🚑', '🚒', '🚐', '🚚', '🚛', '🚜', '🦯', '🦽', '🦼', '🛴', '🚲', '🛵', '🛺', '🚔', '🚍', '🚘', '🚖', '🚡', '🚠', '🚟', '🚃', '🚋', '🚞', '🚝', '🚄', '🚅', '🚈', '🚂', '🚆', '🚇', '🚊', '🚉', '✈️', '🛫', '🛬', '💺', '🚀', '🛸', '🚁', '🛶', '⛵️', '🚤', '🛳', '⛴', '🚢']
    houses = ['🏠', '🏡', '🏘', '🏚', '🏗', '🏭', '🏢', '🏬', '🏣', '🏤', '🏥', '🏦', '🏨', '🏪', '🏫', '🏩', '💒', '🏛', '⛪️', '🕌', '🕍', '🛕']
    purple_signs = ['☮️', '✝️', '☪️', '☸️', '✡️', '🔯', '🕎', '☯️', '☦️', '🛐', '⛎', '♈️', '♉️', '♊️', '♋️', '♌️', '♍️', '♎️', '♏️', '♐️', '♑️', '♒️', '♓️', '🆔', '🈳']
    red_signs = ['🈶', '🈚️', '🈸', '🈺', '🈷️', '✴️', '🉐', '㊙️', '㊗️', '🈴', '🈵', '🈹', '🈲', '🅰️', '🅱️', '🆎', '🆑', '🅾️', '🆘', '🚼', '🛑', '⛔️', '📛', '🚫', '🚷', '🚯', '🚳', '🚱', '🔞', '📵', '🚭']
    blue_signs = ['🚾', '♿️', '🅿️', '🈂️', '🛂', '🛃', '🛄', '🛅', '🚹', '🚺', '🚻', '🚮', '🎦', '📶', '🈁', '🔣', '🔤', '🔡', '🔠', '🆖', '🆗', '🆙', '🆒', '🆕', '🆓', '0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟', '🔢', '⏏️', '▶️', '⏸', '⏯', '⏹', '⏺', '⏭', '⏮', '⏩', '⏪', '⏫', '⏬', '◀️', '🔼', '🔽', '➡️', '⬅️', '⬆️', '⬇️', '↗️', '↘️', '↙️', '↖️', '↪️', '↩️', '⤴️', '⤵️', '🔀', '🔁', '🔂', '🔄', '🔃', '➿', '🔚', '🔙', '🔛', '🔝', '🔜']
    moon = ['🌕', '🌔', '🌓', '🌗', '🌒', '🌖', '🌑', '🌜', '🌛', '🌙']

    random.seed()
    # Select a random emoji list depending on the difficulty level.
    if mystate.GameDetails[0] == 'Easy':
        emoji_group = random.choice(['foods', 'moon', 'animals'])
        mystate.emoji_bank = locals()[emoji_group]

    elif mystate.GameDetails[0] == 'Medium':
        emoji_group = random.choice(['foxes', 'emojis', 'humans', 'vehicles', 'houses', 'hands', 'purple_signs', 'red_signs', 'blue_signs'])
        mystate.emoji_bank = locals()[emoji_group]

    elif mystate.GameDetails[0] == 'Hard':
        emoji_group = random.choice(['foxes', 'emojis', 'humans', 'foods', 'clocks', 'hands', 'animals', 'vehicles', 'houses', 'purple_signs', 'red_signs', 'blue_signs', 'moon'])
        mystate.emoji_bank = locals()[emoji_group]
    # Reset the player's button dictionary.
    mystate.player_buttons = {}
    for cell in range(1, ((total_cells_per_row_or_col ** 2)+1)): mystate.player_buttons[cell] = {'isPressed': False, 'isTrueFalse': False, 'emoji': ''}

def ScoreEmoji():
    """
    Assigns an emoji based on the player's score.
    """
    if mystate.myscore == 0:  # If the score is zero.
        return '😐'  # Returns the neutral expression emoji.
    elif -5 <= mystate.myscore <= -1:  # If the score is between -5 and -1.
        return '😏'  # Returns the slightly negative expression emoji.
    elif -10 <= mystate.myscore <= -6:  # If the score is between -10 and -6.
        return '☹️'  # Returns the negative expression emoji.
    elif mystate.myscore <= -11:  # If the score is less than or equal to -11.
        return '😖'  # Returns the very negative expression emoji.
    elif 1 <= mystate.myscore <= 5:  # If the score is between 1 and 5.
        return '🙂'  # Returns the slightly positive expression emoji.
    elif 6 <= mystate.myscore <= 10:  # If the score is between 6 and 10.
        return '😊'  # Returns the positive expression emoji.
    elif mystate.myscore > 10:  # If the score is greater than 10.
        return '😁'  # Returns the very positive expression emoji.


def NewGame():
    ResetBoard()  # Resets the game board.
    total_cells_per_row_or_col = mystate.GameDetails[2]  # Gets the total number of cells per row or column.

    ReduceGapFromPageTop('sidebar')  # Reduces the space from the top of the page.
    with st.sidebar:
        st.subheader(f"🖼️ Pix Match: {mystate.GameDetails[0]}")  # Sidebar header with the selected difficulty level.
        st.markdown(horizontal_bar, True)  # Decorative horizontal line.

        st.markdown(sbe.replace('|fill_variable|', mystate.sidebar_emoji), True)  # Displays the sidebar emoji.

        aftimer = st_autorefresh(interval=(mystate.GameDetails[1] * 1000), key="aftmr")  # Automatically updates the timer in the sidebar.
        if aftimer > 0: mystate.myscore -= 1  # Reduces the score if the timer is running.

        st.info(f"{ScoreEmoji()} Score: {mystate.myscore} | Pending: {(total_cells_per_row_or_col ** 2) - len(mystate.expired_cells)}")

        st.markdown(horizontal_bar, True)
        if st.button(f"🔙 Return to Main Page", use_container_width=True):
            mystate.runpage = Main
            st.rerun()

    Leaderboard('read')
    st.subheader("Picture Positions:")
    st.markdown(horizontal_bar, True)

    # Set Board Defaults
    st.markdown("<style> div[class^='css-1vbkxwb'] > p { font-size: 1.5rem; } </style> ", unsafe_allow_html=True)  # Makes button face big
    errores = 0
    for i in range(1, (total_cells_per_row_or_col+1)):
        tlst = ([1] * total_cells_per_row_or_col) + [2]  
        globals()['cols' + str(i)] = st.columns(tlst)

    for vcell in range(1, (total_cells_per_row_or_col ** 2)+1):
        if errores == (total_cells_per_row_or_col ** 1)+1:
            mystate.runpage = Main
            st.rerun()
            break
        if 1 <= vcell <= (total_cells_per_row_or_col * 1):
            arr_ref = '1'
            mval = 0

        elif ((total_cells_per_row_or_col * 1)+1) <= vcell <= (total_cells_per_row_or_col * 2):
            arr_ref = '2'
            mval = (total_cells_per_row_or_col * 1)

        elif ((total_cells_per_row_or_col * 2)+1) <= vcell <= (total_cells_per_row_or_col * 3):
            arr_ref = '3'
            mval = (total_cells_per_row_or_col * 2)

        elif ((total_cells_per_row_or_col * 3)+1) <= vcell <= (total_cells_per_row_or_col * 4):
            arr_ref = '4'
            mval = (total_cells_per_row_or_col * 3)

        elif ((total_cells_per_row_or_col * 4)+1) <= vcell <= (total_cells_per_row_or_col * 5):
            arr_ref = '5'
            mval = (total_cells_per_row_or_col * 4)

        elif ((total_cells_per_row_or_col * 5)+1) <= vcell <= (total_cells_per_row_or_col * 6):
            arr_ref = '6'
            mval = (total_cells_per_row_or_col * 5)

        elif ((total_cells_per_row_or_col * 6)+1) <= vcell <= (total_cells_per_row_or_col * 7):
            arr_ref = '7'
            mval = (total_cells_per_row_or_col * 6)

        elif ((total_cells_per_row_or_col * 7)+1) <= vcell <= (total_cells_per_row_or_col * 8):
            arr_ref = '8'
            mval = (total_cells_per_row_or_col * 7)

        elif ((total_cells_per_row_or_col * 8)+1) <= vcell <= (total_cells_per_row_or_col * 9):
            arr_ref = '9'
            mval = (total_cells_per_row_or_col * 8)

        elif ((total_cells_per_row_or_col * 9)+1) <= vcell <= (total_cells_per_row_or_col * 10):
            arr_ref = '10'
            mval = (total_cells_per_row_or_col * 9)


        globals()['cols' + arr_ref][vcell-mval] = globals()['cols' + arr_ref][vcell-mval].empty()
        if mystate.plyrbtns[vcell]['isPressed'] == True:
            if mystate.plyrbtns[vcell]['isTrueFalse'] == True:
                globals()['cols' + arr_ref][vcell-mval].markdown(pressed_emoji.replace('|fill_variable|', '✅️'), True)

            elif mystate.plyrbtns[vcell]['isTrueFalse'] == False:
                globals()['cols' + arr_ref][vcell-mval].markdown(pressed_emoji.replace('|fill_variable|', '❌'), True)
                errores+=1

        else:
            vemoji = mystate.plyrbtns[vcell]['eMoji']
            globals()['cols' + arr_ref][vcell-mval].button(vemoji, on_click=PressedCheck, args=(vcell, ), key=f"B{vcell}")

    st.caption('') # Adds a vertical filler
    st.markdown(horizontal_bar, True) # Adds a horizontal bar

    if len(mystate.expired_cells) == (total_cells_per_row_or_col ** 2) :
        Leaderboard('write')

        if mystate.myscore > 0: st.balloons() # Displays balloons if the score is positive
        elif mystate.myscore <= 0: st.snow() # Displays snow if the score is non-positive

        tm.sleep(5)
        mystate.runpage = Main
        st.rerun()


def Main():
    """
    Main function that sets up the user interface and handles game actions.
    It configures the appearance of the user interface, including the width of the sidebar and the color of buttons.
    Also presents the initial page and provides options to select the game difficulty level and the player's name.
    Additionally, it allows starting a new game and updates the user interface accordingly.
    """

    st.markdown('<style>[data-testid="stSidebar"] > div:first-child {width: 310px;}</style>', unsafe_allow_html=True)  # Reduces the width of the sidebar
    st.markdown(purple_btn_colour, unsafe_allow_html=True)  # Sets the color of buttons to purple

    InitialPage()  # Displays the initial page

    with st.sidebar:
        # Allows the user to select the difficulty level and provide the player's name
        mystate.GameDetails[0] = st.radio('Difficulty Level:', options=('Easy', 'Medium', 'Hard'), index=1, horizontal=True)
        mystate.GameDetails[3] = st.text_input("Player Name, Country", placeholder='Shawn Pereira, India', help='Optional input only for Leaderboard')

        # Button to start a new game
        if st.button(f"🕹️ New Game", use_container_width=True):
            # Configures the game details based on the selected difficulty level
            if mystate.GameDetails[0] == 'Easy':
                mystate.GameDetails[1] = 8  # Time interval in seconds
                mystate.GameDetails[2] = 6  # Total cells per row or column

            elif mystate.GameDetails[0] == 'Medium':
                mystate.GameDetails[1] = 6  # Time interval in seconds
                mystate.GameDetails[2] = 7  # Total cells per row or column

            elif mystate.GameDetails[0] == 'Hard':
                mystate.GameDetails[1] = 5  # Time interval in seconds
                mystate.GameDetails[2] = 8  # Total cells per row or column

            Leaderboard('create')  # Creates the leaderboard table

            PreNewGame()  # Prepares the new game
            mystate.runpage = NewGame  # Sets the game page
            st.rerun()  # Restarts the user interface to start the new game

        st.markdown(horizontal_bar, True)  # Adds a dividing line in the sidebar


if 'runpage' not in mystate:
    mystate.runpage = Main  # Sets the main page as the default start page
mystate.runpage()  # Runs the active page, which can be Main or NewGame
