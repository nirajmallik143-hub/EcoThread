# Bad code - O(n2)
def find_duplicates(arr):
    dups = []
    for i in range(len(arr)):
        for j in range(len(arr)):
            if i != j and arr[i] == arr[j]:
                dups.append(arr[i])
    return dups
    
