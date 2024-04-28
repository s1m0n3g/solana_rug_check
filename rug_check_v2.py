import pyperclip
import webbrowser
from termcolor import colored
import os
import re
import time
import sys

# Set error color for better visibility
error_color = 'red'
ok_color = 'green'

# List to store sites
sites = ["rugcheck", "solsniffer", "dexscreener", "birdeye"]

# Set to store unique codes, not URLs
opened_codes = set()

# Dictionary to store last copied time for each code
last_copied_time = {}

# Variable to track clipboard error
clipboard_error_shown = False

# Add this variable to store the timestamp of the last warning
last_warning_time = {}

def setup_sites():
    print("Select which sites to enable (Enter comma-separated numbers):")
    for i, site in enumerate(sites, 1):
        print(f"{i}. {site.capitalize()}")
    print(f"Q. Quit")

    choices = input("Enter numbers of sites to enable (e.g., 1,2,3,4) or 'Q' to quit: ")

    if choices.strip().upper() == 'Q':
        close_script()

    choices = choices.split(',')
    selected_sites = []
    for choice in choices:
        if not choice.isdigit():
            print(colored(f"Invalid choice '{choice}'. Please enter valid numbers.", error_color))
            return []

        choice = int(choice)
        if not 0 < choice <= len(sites):
            print(colored(f"Invalid choice '{choice}'. Please enter valid numbers.", error_color))
            return []

        selected_sites.append(sites[choice - 1])

    return selected_sites

def clear_clipboard():
    pyperclip.copy('')

def check_clipboard():
    global opened_codes, clipboard_error_shown

    # Retry until clipboard is accessible
    while True:
        try:
            # Get the current clipboard content
            current_clipboard = pyperclip.paste()
            break  # If we successfully got clipboard content, exit retry loop
        except pyperclip.PyperclipException as e:
            print(colored(f"Error accessing clipboard: {e}. Retrying in 5 seconds...", error_color))
            time.sleep(5)  # Wait for 5 seconds before retrying

    # Continue with rest of the logic as before
    # Validate clipboard content using a regular expression
    if not re.match(r"^[a-zA-Z0-9]+$", current_clipboard):
        if not clipboard_error_shown:
            print(colored("Waiting for a valid address...", error_color))
        clipboard_error_shown = True
        return

    # Validate clipboard content length (40-50 characters)
    if not (40 <= len(current_clipboard) <= 50):
        if not clipboard_error_shown:
            print(colored(f"Error: clipboard content length is invalid. Expected 40-50 characters, got {len(current_clipboard)} characters.", error_color))
        clipboard_error_shown = True
        return

    # Check if the code has been copied in the last minute
    current_time = time.time()
    if current_clipboard in last_copied_time and current_time - last_copied_time[current_clipboard] < 60:
        if current_clipboard not in last_warning_time or current_time - last_warning_time[current_clipboard] > 60:
            print(colored("Warning: This token has been opened within the last minute.", 'yellow'))
            print(colored(f"Token: {current_clipboard}", 'yellow'))  # Print the token in yellow
            last_warning_time[current_clipboard] = current_time  # Update the timestamp of the last warning
        return

    # Reset clipboard error flag
    clipboard_error_shown = False

    # Update last copied time for the code
    last_copied_time[current_clipboard] = current_time

    opened_codes.add(current_clipboard)
    print(colored(f"Opening URLs for {current_clipboard}", ok_color))

    try:
        # Send the code to the server (replace with your logic)
        send_to_server(current_clipboard)

        # Open URLs for enabled sites
        for site in selected_sites:
            open_url(site, current_clipboard)

        # Wait for 30 seconds before clearing the clipboard
        time.sleep(30)

        # Clear the clipboard after opening URLs
        clear_clipboard()
    except Exception as e:
        print(colored(f"Error: An error occurred while processing the code. Exception: {e}", error_color))

def send_to_server(code):
    # Place your code logic here to send the code to your server
    # For example:
    # print(f"Sending code to server: {code}")
    pass

def open_url(site, code):
    # Opens the URL in a new browser tab
    if site == "rugcheck":
        webbrowser.open_new_tab("https://rugcheck.xyz/tokens/" + code)
    elif site == "solsniffer":
        webbrowser.open_new_tab("https://solsniffer.com/scanner/" + code)
    elif site == "dexscreener":
        webbrowser.open_new_tab("https://dexscreener.com/solana/" + code)
    elif site == "birdeye":
        webbrowser.open_new_tab("https://birdeye.so/token/" + code)

def close_script():
    print(colored("Closing the script...", 'yellow'))
    sys.exit()

if __name__ == '__main__':
    try:
        # Ensure 'color' command works on your system (optional)
        os.system('color')
    except OSError:
        print(colored("Warning: 'color' command might not be supported on your system. Color highlighting might not work.", 'yellow'))

    while True:
        try:
            selected_sites = setup_sites()  # Run setup to select sites to enable

            if not selected_sites:
                print(colored("No sites selected. Exiting.", error_color))
                break

            print(colored("Press Ctrl+C to return to the menu.", 'yellow'))

            while True:
                # Check the clipboard
                check_clipboard()
                time.sleep(1)  # Add a 1-second delay between clipboard checks

        except KeyboardInterrupt:
            print(colored("Returning to the menu...", 'yellow'))
            continue
        except EOFError:
            close_script()
        except SystemExit:
            break
