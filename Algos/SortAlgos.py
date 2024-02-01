
#SELECTION SORT
def selectionsort(seq):
    for i in range(len(seq) - 1):
        k = i
        for j in range(i + 1, len(seq)):
            if seq[j] < seq[k]:
                k = j
        seq[i], seq[k] = seq[k], seq[i]

#BUBBLE SORT
def bubbleSort(first, second):
    n = len(first)
    for i in range(n):
        for j in range(0, n-i-1):
            if first[j] > first[j+1]:
                first[j], first[j+1] = first[j+1], first[j]
                second[j], second[j+1] = second[j+1], second[j]
    return first, second

#QUICK SORT
def partition(array, begin, end):
    pivot = begin
    for i in range(begin+1, end+1):
        if array[i] <= array[begin]:
            pivot += 1
            array[i], array[pivot] = array[pivot], array[i]
    array[pivot], array[begin] = array[begin], array[pivot]
    return pivot

def quicksort(array, begin=0, end=None):
    if end is None:
        end = len(array) - 1
    def _quicksort(array, begin, end):
        if begin >= end:
            return
        pivot = partition(array, begin, end)
        _quicksort(array, begin, pivot-1)
        _quicksort(array, pivot+1, end)
    return _quicksort(array, begin, end)

#INSERTION SORT
def insertionSort(arr): 
  
    for i in range(1, len(arr)): 
  
        key = arr[i] 
  
        j = i-1
        while j >=0 and key < arr[j] : 
                arr[j+1] = arr[j] 
                j -= 1
        arr[j+1] = key

#MERGE SORT
def merge(arr, l, m, r): 
    n1 = m - l + 1
    n2 = r- m 

    L = [0] * (n1) 
    R = [0] * (n2) 

    for i in range(0 , n1): 
        L[i] = arr[l + i] 
  
    for j in range(0 , n2): 
        R[j] = arr[m + 1 + j] 
  
    i = 0     
    j = 0     
    k = l     
  
    while i < n1 and j < n2 : 
        if L[i] <= R[j]: 
            arr[k] = L[i] 
            i += 1
        else: 
            arr[k] = R[j] 
            j += 1
        k += 1
  
    while i < n1: 
        arr[k] = L[i] 
        i += 1
        k += 1
 
    while j < n2: 
        arr[k] = R[j] 
        j += 1
        k += 1

def mergeSort(arr, l, r): 
    if l < r: 

        m = (l+(r-1))/2
  
        mergeSort(arr, l, m) 
        mergeSort(arr, m+1, r) 
        merge(arr, l, m, r) 

#GNOME SORT
def gnomeSort(array):
    n = len(array)
    index = 0
    while index < n:
        if index == 0:
            index = index + 1
        if array[index] >= array[index-1]:
            index = index + 1
        else:
            array[index], array[index-1] = array[index-1], array[index]
            index = index - 1
 
    return array
