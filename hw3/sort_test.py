# File: sort_test.py
# Author(s):
# Jordna Giebas
# Daniel Rojas Coy
# Harveen Oberoi
# Lucas Duarte Bahia

import random    # to generate random int values
import time      # functionality like C++ <ctime>

# BEGINNING OF SORTING ALGORITHMS CODE

# QUICKSORT ALGORITHM -- three functions

# a is the "array" (list) of values to partition
# b is the beginning index within a
# e is one past the ending index within a
def qsort_partition(a, b, e):
    if e - b <= 0:
        return -1         # nothing to partition: no pivot index
    pivot = a[b]
    j = b                 # initial pivot index
    for k in range(b+1,e):
        if a[k] <= pivot:
            j += 1        # bump the pivot index forward
            a[j], a[k] = a[k], a[j]  # Python swap "trick"
    a[b], a[j] = a[j], a[b]
    return j              # return the pivot index

# this is the recursive function: we don't have pointers
# in Python, so use a helper
def quicksort_help(a, b, e):
    if e - b <= 0:
        return            # no array to sort
    pindex = qsort_partition(a, b, e)
    if pindex >= 0:
        quicksort_help(a, b, pindex)
        quicksort_help(a, pindex + 1, e)

# this is the top-level non-recursive function for the user to call:
# the "array" a is SORTED IN PLACE in quicksort
def quicksort(a):
    quicksort_help(a, 0, len(a))

# END OF QUICKSORT

# END OF SORTING ALGORITHMS CODE

# sorting algorithm testing function
# for "array" sizes of 1000, 2000, ..., 128000
def sort_alg_tester(alg):    # alg is the algorithm (function object) to test
    alg_name = str(alg).split(' ')[1]
    sort_times = []
    for a_size in [ 1000 * 2**i for i in range(8) ]:
        # randomly generated test "array"
        a_test = [random.randint(1,2048) for i in range(a_size)]

        a_test_copy = a_test.copy()    # a_test_copy refers to a COPY of a_test
        a_test_copy.sort()             # use built-in list sort on a_test_copy

        # test and time the sorting algorithm
        start_time = time.time()
        alg(a_test)
        end_time = time.time()
        run_time = end_time - start_time
        
        if a_test == a_test_copy:
            sort_times.append(run_time)
            print('{}, a_size: {:8d}, {:10.4f} sec'.format(
                alg_name, a_size, run_time))
        else:
            print(alg_name, 'NOT successful')
    return sort_times
   
# Insertion Sort Implementation
def insertionsort(vec):

    for idx in range(1,len(vec)):
        currentval = vec[idx]
        pos = idx

        while ( pos > 0 and vec[pos-1] > currentval ):
            vec[pos] = vec[pos-1]
            pos -= 1

        vec[pos] = currentval

# Selecetion Sort Implementation
def selectionsort(vec):

    for fill in range(len(vec)-1,0,-1):
        posMaximum = 0
        for loc in range(1,fill+1):
            if vec[loc] > vec[posMaximum]:
                posMaximum = loc

        # Swap them
        tmp = vec[fill]
        vec[fill] = vec[posMaximum]
        vec[posMaximum] = tmp

# Merge Sort Implementation
def mergesort(alist):
    
    if len(alist)>1:
        mid = len(alist)//2
        lefthalf = alist[:mid]
        righthalf = alist[mid:]

        mergesort(lefthalf)
        mergesort(righthalf)

        i=0
        j=0
        k=0
        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i] < righthalf[j]:
                alist[k]=lefthalf[i]
                i=i+1
            else:
                alist[k]=righthalf[j]
                j=j+1
            k=k+1

        while i < len(lefthalf):
            alist[k]=lefthalf[i]
            i=i+1
            k=k+1

        while j < len(righthalf):
            alist[k]=righthalf[j]
            j=j+1
            k=k+1

# Counting Sort Implementation
def countingsort(arr):
    """in-place counting sort"""
    
    n = len(arr)
    m = max(arr) + 1
    count = [0] * m               # init with zeros
    for a in arr:
        count[a] += 1             # count occurences
    i = 0
    for a in range(m):            # emit
        for c in range(count[a]): # - emit 'count[a]' copies of 'a'
            arr[i] = a
            i += 1
    return arr

def main():
#    qs_times = sort_alg_tester(quicksort)
#    is_times = sort_alg_tester(insertionsort)
#    ss_times = sort_alg_tester(selectionsort)
#    ms_times = sort_alg_tester(mergesort)
    count_times = sort_alg_tester(countingsort)

if __name__ == '__main__':
    main()

    
