
tasks = []

while True:

    print('==== TO-DO LIST MENU ====')
    print('1. View To-Do List')
    print('2. Add Task')
    print('3. Edit Task')
    print('4. Remove Task')
    print('5. Exit')

    choice = int(input('Choose an option (1-5): '))
    
    if choice == 1:
            if tasks:
                print('\nTasks:')
                for i, task in enumerate(tasks, start = 1):
                    print(f'{i}.{task}')
                print(' ')
            else:
                print('\nNo tasks to show.\n')

    elif choice == 2:
        task = input('\nAdd a task: ')
        tasks.append(task)
        print(tasks)
        print(f'\n{task} added successfully.\n')

    elif choice == 3:
        try:
            print(f'\n{tasks}')
            index = int(input('Enter task index to edit: '))
            new_task = input('Enter new task: ')
            tasks[index] = new_task
            print(f'\nUpdated list: {tasks}\n')
        except:
            print('\nInvalid input, please choose an existing index value.\n')

    elif choice == 4:
        try:
            print(f'\n{tasks}')
            index = int(input('Enter the task index to delete: '))
            removed = tasks.pop(index)
            print(f'\n{tasks}')
            print(f'Successfully removed {removed}\n.')
        except:
            print('\nInvalid input, please choose an existing index value.')

    elif choice == 5:
        print('Exiting... Goodbye.')
        break

    else: 
        print('\nInvalid choice, please select a valid choice.\n')




