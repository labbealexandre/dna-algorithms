import os

class CustomAssertions:
    def assertEqualMatrix(self, A, B):
        nA1, nA2 = len(A), len(A[0])
        nB1, nB2 = len(B), len(B[0])
        if (nA1 != nB1 or nA2 != nB2):
            raise AssertionError(
                'dimensions', nA1, '*', nA2,
                'don\'t match with', nB1, '*', nB2
            )

        for i in range(nA1):
            for j in range(nA2):
                if (A[i][j] != B[i][j]):
                    raise AssertionError('matrices are not equal, indices (' + str(i) + ',' + str(j) + ') ' + 'A : ' + str(A[i][j]) + ' and B : ' + str(B[i][j]))