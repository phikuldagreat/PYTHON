#empty dict
student_list = {}

while True:
    
    #menu for available options
    print('==== STUDENT GRADEBOOK MENU ====')
    print('1. Add student')
    print('2. Display list')
    print('3. Search/Update student grade')
    print('4. Display highest student grade')
    print('5. Exit')

    choice = input('\nChoose an option (1-6): ')

    if choice == '1':
        try:
                sName = input('\nEnter student name: ')
                if sName not in student_list: #checks if input already exists in dict
                    sGrade = int(input('Enter student\'s grade: '))
                    student_list[sName] = sGrade #add student and grade to dict
                    print('\nStudent added successfully.\n')
                else:
                    print(f'\n{sName} already exists.\n') 
        except:
            print('Error input, please try again')

    elif choice == '2':
            if student_list: #check if gradebook has content
                print(f'\n{student_list}\n') #simply prints dict
            else:
                print('\nGradebook is empty.\n')

    elif choice == '3':
        if student_list:
            student = input('\nSearch for student: ')
            if student in student_list: #checks if user input is available in dict
                print(f'{student}\'s grade is: {student_list[student]} \n')
                opt = input('Would you like to update their grade? (Y/N): ')
                if opt in ['Y', 'y']:
                    try:
                        new_grade = int(input('Enter new grade: '))
                        student_list[student] = new_grade #replaces former grade to new grade
                        print(f'\n{student}\'s new grade: {new_grade}.\n')
                    except:
                        print('\nInvalid input, please enter a numeric grade.\n')
                else:
                    print('Okay. returning to menu...\n')
            else:
                print(f'{student} does not exist in the list.\n')
        else:
            print('\nGradebook is empty.\n')

    elif choice == '4':
        if student_list:
            Hgrade = None
            Hstudent = None
            for key in student_list:
                if Hgrade is None or student_list[key] > Hgrade: #compares Hgrade to highest value in dict
                    Hgrade = student_list[key] #store highest grade in dict to Hgrade
                    Hstudent = key #store student's name w/ the highest grade in Hstudent
            print(f'Top student is: {Hstudent} with grade: {Hgrade}.\n')
        else:
            print('\nGradebook is empty.\n')

    elif choice == '5':
        print('Exiting... Goodbye...')
        break

    else:
        print('\nInvalid input, please select a valid choice.\n')
        