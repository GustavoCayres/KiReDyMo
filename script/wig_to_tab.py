import re
import sys


def main(wig_file_path):
    output = []
    trigger = 0
    with open(wig_file_path) as wig_file:
        for line in wig_file.readlines():
            if trigger != 0:
                if line.startswith("fixedStep"):
                    break

                output.append(str(trigger) + "\t" + line.strip("\n") + "\t\n")
                trigger += 2500

            if re.search("Tb927_11_v5\.1", line):
                output.append("[Position]\t[Score]\t\n")
                trigger = 1250

    with open("origins_Tb927_11_v5.1.txt", 'w') as output_file:
        output_file.writelines(output)

if __name__ == "__main__":
    main(sys.argv[1])
