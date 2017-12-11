import os

if __name__ == "__main__":
    header = ''
    array = []
    abs_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    print(abs_path)

    for (dirpath, dirnames, filenames) in os.walk(abs_path + '/staff/full'):
        for filename in filenames:
            with open(os.path.join(dirpath, filename), "r") as ins:
                lines = ins.readlines()
                header = lines[0]
                array.extend(lines[1:])
                print(filename, len(lines))

    print('total: ', len(array))
    array.insert(0, header)
    with open('staff.csv', "w+") as ins:
        ins.writelines(array)
    print("end")


