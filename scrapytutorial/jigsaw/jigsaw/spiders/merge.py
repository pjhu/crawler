import os

if __name__ == "__main__":
    header = ''
    array = []
    abs_path = os.path.dirname(os.path.realpath(__file__))

    for (dirpath, dirnames, filenames) in os.walk(abs_path + '/staff/full'):
        for filename in filenames:
            print(filename)
            with open(os.path.join(dirpath, filename), "r") as ins:
                lines = ins.readlines()
                header = lines[0]
                array.extend(lines[1:])

    array.insert(0, header)
    with open('item.csv', "w") as ins:
        ins.writelines(array)
    print("end")


