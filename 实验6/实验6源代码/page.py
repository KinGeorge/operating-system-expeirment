import random
import matplotlib.pyplot as plt
random.seed(10)

def setup():    
    print("页容量: ",end="")
    capacity = int(input())
    print("页序列: ",end="")
    stream = list(map(int,input().strip().split()))
    print("\nStream|Frame →\t",end='')
    for i in range(capacity):
        print(i,end=' ')
    print("Fault\n")
    return capacity, stream

def report(steam_len, fault):
    print("\n页序列数: %d\n未命中数量: %d\n缺页率: %0.2f%%"%(steam_len,fault,(fault/steam_len)*100))

# LRU
def LRU(capacity, stream, screen = True):
    find,st,fault,is_fault = [],[],0,'No'
    for i in stream:
        if i not in find:
            if len(find)<capacity:
                find.append(i)
                st.append(len(find)-1)
            else:
                ind = st.pop(0)
                find[ind] = i
                st.append(ind)
            is_fault = 'Yes'
            fault += 1
        else:
            st.append(st.pop(st.index(find.index(i))))
            is_fault = 'No'
        if screen:
            print("   %d\t\t"%i,end='')
            for x in find:
                print(x,end=' ')
            for x in range(capacity-len(find)):
                print(' ',end=' ')
            print(" %s"%is_fault)
    if screen:
        report(len(stream),fault)
    return fault/len(stream)


def FIFO(capacity, stream, screen = True):
    find,fault,top,is_fault = [],0,0,'No'
    for i in stream:
        if i not in find:
            if len(find)<capacity:
                find.append(i)
            else:
                find[top] = i
                top = (top+1)%capacity
            fault += 1
            is_fault = 'Yes'
        else:
            is_fault = 'No'
        if screen:
            print("   %d\t\t"%i,end='')
            for x in find:
                print(x,end=' ')
            for x in range(capacity-len(find)):
                print(' ',end=' ')
            print(" %s"%is_fault)

    if screen:
        report(len(stream),fault)
    return fault/len(stream)

if __name__ == "__main__":
    print("选择算法，LRU算法输入L，FIFO算法输入F: ",end='')
    algorithm  = input()
    if algorithm == 'L' or algorithm == 'l':
        capacity, stream = setup()
        LRU(capacity, stream)
    elif algorithm == 'F' or algorithm == 'f':
        capacity, stream = setup()
        FIFO(capacity, stream)
    else:
        raise ValueError

    # 不同页数的变化：
    stream, rate = [], []
    for i in range(1000):
    # 生一个成包含1000个0～100之间的随机整数的列表
        stream.append(random.randint(0, 100))

    if algorithm == 'L' or algorithm == 'l':
        for capacity in range(100):
            rate.append(LRU(capacity, stream))
        plt.plot(rate)
        plt.show()
        
    elif algorithm == 'F' or algorithm == 'f':
        for capacity in range(100):
            rate.append(FIFO(capacity, stream))    
        plt.plot(rate)
        plt.show()