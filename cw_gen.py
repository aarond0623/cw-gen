import re
import sys
import argparse


def generate_clues(across_nums, down_nums, filename=None, out=None):
    """Generates a clue file for use with LaTeX's cwpuzzle package."""
    if filename:
        clue_file = open(filename, 'r')
        clues = clue_file.read()
        clue_file.close()
        clues = clues.split('\n')
    else:
        # If no file provided, get one from the user.
        clues = []
        print("Enter each Across clue and press enter.")
        print("Do not include the clue number.")
        while True:
            clue = input()
            clues.append(clue)
            if clue == "":
                break
        print("Enter each Down clue and press enter.")
        print("Do not include the clue number.")
        while True:
            clue = input()
            if clue == "":
                break
            clues.append(clue)
    
    # Clean the clues for LaTeX
    clues = [re.sub('{', r'\\{', x) for x in clues]
    clues = [re.sub('}', r'\\}', x) for x in clues]
    clues = [re.sub(r'[_]+', r'{\\blank}', x) for x in clues]
    clues = [re.sub('&', r'\\&', x) for x in clues]
    clues = [re.sub('#', r'\\#', x) for x in clues]
    clues = [re.sub(r'\u00AD', r'', x) for x in clues]
    clues = [re.sub(r'[“”]', r'"', x) for x in clues]
    clues = [re.sub(r'[‘’]', r"'", x) for x in clues]
    clues = [re.sub('—', r'---', x) for x in clues]
    clues = [re.sub(r'\$', r'\\$', x) for x in clues]
    clues = [re.sub(r'\.\.\.([A-Za-z])', r'\\elip \1', x) for x in clues]
    clues = [re.sub(r'\.\.\.', r'\\elip', x) for x in clues]
    clues = [re.sub(r'\[([^\]]*)\]', r'{[\1]}', x) for x in clues]
    clues = [re.sub(r'^[0-9]+\. ', r'', x) for x in clues]
    
    # Find a line break in the clues that separates Across from Down
    i = clues.index('')
    across_clues = clues[0:i]
    down_clues = clues[i+1:]
    
    if not out:
        out = input("Enter filename to save clues: ")
    clue_file = open(out, 'w')
    clue_file.write("\\begin{clues}{Across}\n")
    i = 0
    for clue in across_clues:
        clue_file.write("    \\clue{{{}}} {}\n".format(across_nums[i], clue))
        i += 1
    clue_file.write("\\end{clues}\n")
    clue_file.write("\\vspace{\\cluesep}\n")
    clue_file.write("\\begin{clues}{Down}\n")
    i = 0
    for clue in down_clues:
        clue_file.write("    \\clue{{{}}} {}\n".format(down_nums[i], clue))
        i += 1
    clue_file.write("\\end{clues}")
    clue_file.close()


def generate_puzzle(filename=None, out=None):
    if filename:
        puz_file = open(filename, 'r')
        puzzle = puz_file.read()
        puz_file.close()
        puzzle = puzzle.split('\n')
    else:
        # If no file, get one from the user
        puzzle = []
        print("Enter each row of the crossword using the following key:")
        print("Blank squares: .")
        print("Black squares: x")
        print("Circles: o")
        while True:
            puz_line = input()
            if puz_line == "":
                break
            puzzle.append(puz_line)
    
    # Delete any trailing blank lines
    puzzle = [x for x in puzzle if x != '']
    
    # Not all rows are the same length
    if len({len(i) for i in puzzle}) != 1:
        print("ERROR: Puzzle dimensions are irregular!")
        return None
    
    puzzle_width = len(puzzle[0])
    puzzle_height = len(puzzle)
    
    if not out:
        out = input("Enter filename to save puzzle: ")
    puz_file = open(out, 'w')
    puz_file.write("\\begin{{Puzzle}}{{{}}}{{{}}}\n".format(puzzle_width, puzzle_height))
    puz_key = {".": "I", "o": "[o]I", "x": "*"}
    counter = 0
    across_nums = []
    down_nums = []
    for y in range(len(puzzle)):
        for x in range(len(puzzle[y])):
            across = False
            puz_file.write("|[")
            # If a square is blocked on the left, then this is an across square
            if x == 0 or (x > 0 and puzzle[y][x-1] == 'x'):
                if puzzle[y][x] != 'x':
                    across = True
                    counter += 1
                    puz_file.write("{}".format(counter))
                    across_nums.append(counter)
            # If a square is blocked above, then this is a down square
            if y == 0 or (y > 0 and puzzle[y-1][x] == 'x'):
                if puzzle[y][x] != 'x':
                    # Only print the number if it wasn't already printed for
                    # across
                    if not across:
                        counter += 1
                        puz_file.write("{}".format(counter))
                    down_nums.append(counter)    
            puz_file.write("]")
            puz_file.write(puz_key[puzzle[y][x]])
        puz_file.write("|.\n")
    puz_file.write("\\end{Puzzle}")
    puz_file.close()
    return (across_nums, down_nums)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate crossword files for use with LaTeX's cwpuzzle package.")
    parser.add_argument("-p", "--puzzle", metavar="filename", type=str, help="A puzzle file with the puzzle layout, where . = blank, o = circle, and x = black squares.")
    parser.add_argument("-c", "--clues", metavar="filename", type=str, help="A clues file with across and down clues separated by a blank line. Clues should not be numbered. That will be done automatically.")
    parser.add_argument("out_puzzle", metavar="puzzle-output", help="Output file for the puzzle file.")
    parser.add_argument("out_clues", metavar="clues-output", help="Output file for the clues file.")
    
    args = parser.parse_args()
    generate_clues(*generate_puzzle(args.puzzle, args.out_puzzle), args.clues, args.out_clues)
    