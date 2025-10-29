#!/usr/bin/env python3
import cmd
import time
import random
import os
import shutil
import subprocess

# ----------------------------------------------------------------------
# Helper: Get terminal size (fallback to 80x24 if unavailable)
def get_term_size():
    try:
        cols, rows = shutil.get_terminal_size(fallback=(80, 24))
    except Exception:
        cols, rows = 80, 24
    return cols, rows

# ----------------------------------------------------------------------
# Simple glitch animation effect for a single line
def glitch_text(text, duration=0.03, iterations=2):
    """Animate text with a glitch effect."""
    chars = list(text)
    original = chars[:]
    for _ in range(iterations):
        # Randomly corrupt some chars
        for i in range(len(chars)):
            if random.random() < 0.5:  # 20% chance to glitch a char
                chars[i] = random.choice('!@#$%^&*()_+-=[]{}|;:,.<>?/`~')
        print(''.join(chars), end='\r', flush=True)  # Overwrite line
        time.sleep(duration)
    # Restore original
    print(''.join(original), flush=True)
    time.sleep(0.1)

# ----------------------------------------------------------------------
# Typing animation for a single line
def type_text(text, delay=0.001):  # Reduced delay for quicker typing
    """Type out text character by character."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print(flush=True)

# ----------------------------------------------------------------------
# Animate the intro with glitch and typing effects
def animate_intro():
    cols, rows = get_term_size()

    # fsociety ASCII mask (red) – RAW STRING
    mask = r"""
\033[31m  ///////////     ///////////     ///////////     ///////////
   ///////////     ///////////     ///////////     ///////////
  ///             ///             ///             ///
 ///             ///             ///             ///
///////////     ///////////     ///////////     ///////////
///////////     ///////////     ///////////     ///////////
 ///             ///             ///             ///
  ///             ///             ///             ///
   ///////////     ///////////     ///////////     ///////////
    ///////////     ///////////     ///////////     ///////////\033[0m
"""

    # Big ASCII art for "Welcome MR ROBOT"
    big_welcome = r"""
W   W EEEEE L      CCC   OOO  M   M EEEEE       M   M RRRR        RRRR   OOO  BBBB   OOO  TTTTT
W   W E     L     C   C O   O MM MM E           MM MM R   R       R   R O   O B   B O   O   T
W W W EEE   L     C     O   O M M M EEE         M M M RRRR        RRRR  O   O BBBB  O   O   T
WW WW E     L     C   C O   O M   M E           M   M R R         R R   O   O B   B O   O   T
W   W EEEEE LLLLL  CCC   OOO  M   M EEEEE       M   M R  RR       R  RR  OOO  BBBB   OOO    T
"""

    # Process mask lines
    mask_lines = [line.rstrip() for line in mask.strip().split('\n')]
    padded_mask = [line.center(cols) for line in mask_lines]
    mask_height = len(mask_lines)

    # Process big welcome lines
    welcome_lines = [line.rstrip() for line in big_welcome.strip().split('\n')]
    padded_welcome = [line.center(cols) for line in welcome_lines]
    welcome_height = len(welcome_lines)

    # Vertical layout calculations
    top_padding = 2
    spacing = max(0, (rows - mask_height - welcome_height - top_padding) // 2)

    # Animate mask line by line with glitch
    os.system('cls' if os.name == 'nt' else 'clear')
    for i in range(top_padding):
        print()
    for line in padded_mask:
        glitch_text(line)
        time.sleep(0.05)  # Pause after each mask line (adjust this to change mask animation speed)

    # Add spacing lines
    for _ in range(spacing):
        print()

    # Animate welcome line by line with typing
    for line in padded_welcome:
        type_text(line)
        time.sleep(0.02)  # Reduced pause after each welcome line for quicker animation (adjust this to change welcome speed)

    # Add remaining space if needed
    remaining = rows - top_padding - mask_height - spacing - welcome_height
    for _ in range(max(0, remaining)):
        print()

# ----------------------------------------------------------------------
class MrRobotCLI(cmd.Cmd):
    prompt = 'fsociety> '

    # ------------------- COMMANDS -------------------
    def do_hack(self, arg):
        """hack [target]: Simulate hacking a system. Example: hack evilcorp"""
        target = arg if arg else 'unknown target'
        print(f"\nInitiating hack on {target}...")
        time.sleep(1)
        for i in range(5):
            print(f"  Breaching layer {i+1}... ", end='')
            glitch_text(random.choice(['SUCCESS', 'FIREWALL BYPASSED', 'ENCRYPTION CRACKED']))
            time.sleep(0.3)
        print("\nHack complete. Data dump:\n" + random_data_dump())

    def do_scan(self, arg):
        """scan: Scan for vulnerabilities."""
        print("\nScanning network...")
        time.sleep(2)
        ips = [f"192.168.1.{random.randint(1,255)}" for _ in range(3)]
        for ip in ips:
            print(f"  Found: {ip} → ", end='')
            type_text(random.choice(['Vulnerable to SQLi', 'Open SSH', 'Weak password']))
        print("Scan complete.\n")

    def do_encrypt(self, arg):
        """encrypt [file]: Pretend to encrypt a file."""
        if not arg:
            print("Usage: encrypt <filename>")
            return
        print(f"\nEncrypting {arg} with AES-256...")
        time.sleep(1.5)
        print("Encryption complete. File secured (simulated).\n")

    def do_decrypt(self, arg):
        """decrypt [file]: Pretend to decrypt a file."""
        if not arg:
            print("Usage: decrypt <filename>")
            return
        print(f"\nDecrypting {arg}...")
        time.sleep(1.5)
        print("Decryption complete. Contents revealed (simulated).\n")

    def do_whoami(self, arg):
        """whoami: Reveal your hacker identity."""
        identities = ["Elliot Alderson", "Mr. Robot", "fsociety operative", "ghost in the machine"]
        print(f"\nYou are: \033[1;33m", end='')
        glitch_text(random.choice(identities), iterations=3)
        print("\033[0m\n")

    def do_clear(self, arg):
        """clear: Clear the screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def do_exit(self, arg):
        """exit: Leave the terminal."""
        print("\nLogging out. We do not forgive. We do not forget.\n")
        return True

    def do_quit(self, arg):
        """quit: Same as exit."""
        return self.do_exit(arg)

    def default(self, line):
        """Handle unknown commands as shell commands."""
        try:
            result = subprocess.run(line, shell=True, capture_output=True, text=True)
            print(result.stdout)
            if result.stderr:
                print(result.stderr)
        except Exception as e:
            print(f"Error executing shell command: {e}")
        print()  # Newline for prompt

# ----------------------------------------------------------------------
def random_data_dump():
    dumps = [
        "User: admin | Pass: admin123\nBank records: $9,999,999,999.00\nPlan: Delete everything.",
        "Email leak:\n> 'The board knows. Burn it all.' - CEO",
        "Secret file: project_icarus.txt\n> 'Phase 2 begins at midnight.'"
    ]
    return random.choice(dumps)

# ----------------------------------------------------------------------
if __name__ == '__main__':
    animate_intro()
    MrRobotCLI().cmdloop(intro="Type 'help' for commands. Society is a lie.\n")
