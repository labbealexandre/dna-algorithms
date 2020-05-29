# def mergeSort(K):

#     """merge sort for dictionnary [(key, value)]"""

#     n = len(K)
#     if n <= 1:
#         return K
    
#     m = n//2
#     L = mergeSort(K[:m])
#     R = mergeSort(K[m:])

#     i, j = 0, 0
#     res = []
#     while (i < len(L) and j < len(R)):
#         if L[i][1] < R[j][1]:
#             res.append(L[i])
#             i+=1
#         else:
#             res.append(R[j])
#             j+=1

#     while i < len(L):
#         res.append(L[i])
#         i+=1

#     while j < len(R):
#         res.append(R[j])
#         j+=1

#     return res