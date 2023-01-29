# show used, not_used
def show(used, not_used):
    print("used:", end=" ")
    for use in used:
        print(use, end=" ")
    print()
    print("not used:", end=" ")
    for use in not_used:
        print(use, end=" ")
    print()
    print("===" * 20)

def firstfit(actions, memory_size):
    used = []
    not_used = [(0, memory_size)]
    for action in actions:
        if action[0] == 'a':
            for index, ran in enumerate(not_used):
                if action[1] < ran[1]:
                    del not_used[index]
                    not_used.append((ran[0] + action[1], ran[1] - action[1]))
                    used.append((ran[0], action[1]))
                    not_used.sort(key=lambda x: x[0])
                    print(f'* 申请{action[1]}K')
                    break
        elif action[0] == 'r':
            for index, ran in enumerate(used):
                if ran[1] == action[1]:
                    del used[index]
                    not_used.append(ran)
                    print(f'# 释放{action[1]}K')

            # 合并not_used
            not_used.sort(key=lambda x: x[0])
            index = not_used.index(ran)

            # 与后面合并
            if index + 1 < len(not_used) and (not_used[index][0]+not_used[index][1]) == not_used[index + 1][0]:
                new_tpl = (not_used[index][0], not_used[index][1]+not_used[index + 1][1])
                del not_used[index + 1]
                not_used[index] = new_tpl
                not_used.sort(key=lambda x: x[0])
            
            # 与前面合并
            if index > 0 and (not_used[index-1][0]+not_used[index-1][1]) == not_used[index][0]:
                new_tpl = (not_used[index-1][0], not_used[index-1][1]+not_used[index][1])
                del not_used[index]
                not_used[index-1] = new_tpl
                not_used.sort(key=lambda x: x[0])

        used.sort(key=lambda x: x[0])
        show(used, not_used)

def bestfit(actions, memory_size):
    used = []
    not_used = [(0, memory_size)]
    idx = memory_size
    for action in actions:
        if action[0] == 'a':
            for index, ran in enumerate(not_used):
                if action[1] < ran[1]:
                    idx = index
            ran = not_used[idx]
            index = idx
            del not_used[index]
            not_used.append((ran[0] + action[1], ran[1] - action[1]))
            used.append((ran[0], action[1]))
            not_used.sort(key=lambda x: x[0])
            print(f'* 申请{action[1]}K')

        elif action[0] == 'r':
            for index, ran in enumerate(used):
                if ran[1] == action[1]:
                    del used[index]
                    not_used.append(ran)
                    print(f'# 释放{action[1]}K')

            # 合并not_used
            not_used.sort(key=lambda x: x[0])
            index = not_used.index(ran)

            # 与后面合并
            if index + 1 < len(not_used) and (not_used[index][0]+not_used[index][1]) == not_used[index + 1][0]:
                new_tpl = (not_used[index][0], not_used[index][1]+not_used[index + 1][1])
                del not_used[index + 1]
                not_used[index] = new_tpl
                not_used.sort(key=lambda x: x[0])
            
            # 与前面合并
            if index > 0 and (not_used[index-1][0]+not_used[index-1][1]) == not_used[index][0]:
                new_tpl = (not_used[index-1][0], not_used[index-1][1]+not_used[index][1])
                del not_used[index]
                not_used[index-1] = new_tpl
                not_used.sort(key=lambda x: x[0])
                
        used.sort(key=lambda x: x[0])
        show(used, not_used)

if __name__ == '__main__':
    memory_size = 640
    actions1 = [['a', 130], ['a', 60], ['a', 100], ['r', 60],
             ['r', 100], ['r', 130]]

    print("首次适应法：1\n最佳适应法：2\n退出：其他任意键")
    choice = input("请输入：")
    while choice == '1' or choice == '2':
        if choice == '1':
            firstfit(actions1, memory_size)
        else:
            bestfit(actions1, memory_size)
        print("\n\n首次适应法：1\n最佳适应法：2\n退出：exit")
        choice = input("请输入：")
