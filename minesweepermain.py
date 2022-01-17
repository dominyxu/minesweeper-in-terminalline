#main() for cmd line minesweeper game
from minesweeperfunctions import Board
from minesweeperfunctions import play
import math

print(""" _______________
< Welcome To MineSweeper! >
 ------------------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/
                ||----w |
                ||     || """)

placeholder = input("")
play_again = True

#while play_again:
while play_again:
    while True:
        try:
            level = int(input("Please select the difficulty \n\t1: easy (5x5) \n\t2: medium (10x10) \n\t3: hard (20x20) \n\t4: create custom dimensions \nSelection: "))
            if level==1 or level==2 or level==3 or level==4:
                break
            else:
                print("INVALID INPUT. Please enter either 1 (easy), 2 (medium), 3 (hard), or 4 (custom)")
        except ValueError:
            print("INVALID INPUT. Please enter either 1 (easy), 2 (medium), 3 (hard), or 4 (create custom)")
            continue   

    if level==1:
        play(5,5)
    elif level==2:
        play(10,23)
    elif level==3:
        play(20,85)                                     
    elif level==4:
        dimension = int(input("what would you like the dimensions to be? (X x X): "))
        custom_bombs = input("Would you like to have a custom number of bombs? (YES/NO) ")
        custom_bombs = custom_bombs.strip().upper()
        if custom_bombs == "YES":
            while True:
                try: 
                    num_bombs = int(input("How many bombs would you like to have? "))
                    if num_bombs < dimension**2 -1 and num_bombs>0: 
                        break
                    else: 
                        print("INVALID INPUT. Your dimensions do not support this number of bombs: ")
                except ValueError:
                    print("INVALID INPUT. Please enter a valid input.")
                    continue
            play(dimension, num_bombs)
        if custom_bombs =="NO":
            play(dimension, math.sqrt(num_bombs))

    while True:
        try: 
            play_again_input = input("Would you like to play again? (Yes/No) ")
            play_again_input = play_again_input.strip().upper()
            if play_again_input=="YES" or play_again_input=="NO":
                break
            else:
                print("Please enter a valid answer")
        except:
            print("Please enter a valid answer (YES/NO)")
    
    if play_again_input=="YES":
        continue
    else:
        break
print("GG")