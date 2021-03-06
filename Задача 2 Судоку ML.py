"""
name: Sudoku
author: vladvekov
"""
import os
import time
import random
import pickle
import pickletools
from os import path


class ClassSudokuField(object):
    def __init__(self):
        self.Field = [[0] * 9 for i in range(9)]

    def GetElem(self, i, j):
        return self.Field[i][j]

    def SetElem(self, i, j, value):
        self.Field[i][j] = value

    def GenerateField(self):
        TempValue = 1  # генерация 1 триады
        for i in range(9):
            self.Field[0][i] = TempValue
            TempValue += 1

        TempValue = 1  # генерация 2 триады
        for i in range(8, 17):
            self.Field[3][i % 9] = TempValue
            TempValue += 1

        TempValue = 1  # генерация 3 триады
        for i in range(7, 16):
            self.Field[6][i % 9] = TempValue
            TempValue += 1

        for i in range(1, 9):  # заполнение матрицы числами
            for j in range(0, 9):
                if i % 3 != 0:
                    self.Field[i][j] = self.Field[i - 1][(j + 3) % 9]

    def TransportField(self):  # транспортирование матрицы
        TempField = [[0] * 9 for i in range(9)]
        for i in range(9):
            for j in range(9):
                TempField[i][j] = self.Field[j][i]
        self.Field = TempField

    def SwapString(self, IndexSwapFirst, IndexSwapSecond):  # меняем местами двес строки с заданными индексами
        self.Field[IndexSwapFirst], self.Field[IndexSwapSecond] = \
            self.Field[IndexSwapSecond], self.Field[IndexSwapFirst]

    def SwapColumns(self, IndexSwapFirst, IndexSwapSecond):  # меняесм две колонки с заданными индексами
        for i in range(9):
            self.Field[i][IndexSwapFirst], self.Field[i][IndexSwapSecond] = self.Field[i][IndexSwapSecond], \
                                                                            self.Field[i][IndexSwapFirst]

    def SwapString3X(self, ObjectNumberFist,
                     ObjectNumberSecond):  # меняем местами два поля с заданными номерами горизонтально
        for IterCounter in range(3):
            self.Field[ObjectNumberFist * 3 + IterCounter], self.Field[ObjectNumberSecond * 3 + IterCounter] = \
                self.Field[ObjectNumberSecond * 3 + IterCounter], self.Field[ObjectNumberFist * 3 + IterCounter]

    def SwapColumns3X(self, ObjectNumberFist,
                      ObjectNumberSecond):  # меняем местами два поля с заданными номерами вертикально
        for IterConter in range(3):
            for i in range(9):
                self.Field[i][ObjectNumberFist * 3 + IterConter], self.Field[i][ObjectNumberSecond * 3 + IterConter] = \
                    self.Field[i][ObjectNumberSecond * 3 + IterConter], self.Field[i][ObjectNumberFist * 3 + IterConter]

    def GenerateRandomFeeld(self):
        for GlobalIterator in range(50):
            RandomNum = random.randint(1, 5)
            if RandomNum == 1:
                self.TransportField()
            elif RandomNum == 2:
                RandomArea = 3 * random.randint(0, 2)
                RandomStringIndexFirst = random.randint(0, 2)
                RandomStringIndexSecond = 0
                if RandomStringIndexFirst == 1:
                    RandomStringIndexSecond = 2
                else:
                    RandomStringIndexSecond = 2 - RandomStringIndexFirst
                self.SwapString(RandomArea + RandomStringIndexFirst,
                                RandomArea + RandomStringIndexSecond)
            elif RandomNum == 3:
                RandomArea = 3 * random.randint(0, 2)
                RandomColumnIndexFirst = random.randint(0, 2)
                RandomAreaSecond = 0
                if RandomColumnIndexFirst == 1:
                    RandomColumnIndexSecond = 0
                else:
                    RandomColumnIndexSecond = 2 - RandomColumnIndexFirst
                self.SwapColumns(RandomArea + RandomColumnIndexFirst, RandomArea + RandomColumnIndexSecond)
            elif RandomNum == 4:
                RandomAreaFirst = random.randint(0, 2)
                RandomAreaSecond = 0
                if RandomAreaFirst == 1:
                    RandomAreaSecond = 2
                else:
                    RandomAreaSecond = 2 - random.randint(0, 2)
                self.SwapString3X(RandomAreaFirst, RandomAreaSecond)
            elif RandomNum == 5:
                RandomAreaFirst = random.randint(0, 2)
                RandomAreaSecond = 0
                if RandomAreaFirst == 1:
                    RandomAreaSecond = 0
                else:
                    RandomAreaSecond = 2 - random.randint(0, 2)
                self.SwapColumns3X(RandomAreaFirst, RandomAreaSecond)

    def CreatingPuzzle(self, NumberZeroFields):
        GlobalIterationsCounter = 0
        ZeroElementCounter = 0
        while ZeroElementCounter < NumberZeroFields and GlobalIterationsCounter < 200:
            ElemRandomIndex_I = random.randint(0, 8)
            ElemRandomIndex_J = random.randint(0, 8)
            while self.Field[ElemRandomIndex_I][ElemRandomIndex_J] == 0:
                ElemRandomIndex_I = random.randint(0, 8)
                ElemRandomIndex_J = random.randint(0, 8)
            DeletedItemValue = self.Field[ElemRandomIndex_I][ElemRandomIndex_J]
            self.Field[ElemRandomIndex_I][ElemRandomIndex_J] = 0

            if Decision(self):
                ZeroElementCounter += 1
            else:
                self.Field[ElemRandomIndex_I][ElemRandomIndex_J] = DeletedItemValue
            GlobalIterationsCounter += 1

        if ZeroElementCounter < NumberZeroFields:
            ElemRandomIndex_I = random.randint(0, 8)
            ElemRandomIndex_J = random.randint(0, 8)
            while self.Field[ElemRandomIndex_I][ElemRandomIndex_J] == 0:
                ElemRandomIndex_I = random.randint(0, 8)
                ElemRandomIndex_J = random.randint(0, 8)
                self.Field[ElemRandomIndex_I][ElemRandomIndex_J] = 0

    def Validation(self):
        for i in range(9):  # проверка на сумму по сторокам
            ElementSum = 0
            for j in range(9):
                ElementSum += self.Field[i][j]
            if ElementSum != 45:
                return False
        for j in range(9):  # проверка на сумму по столбцам
            ElementSum = 0
            for i in range(9):
                ElementSum += self.Field[i][j]
            if ElementSum != 45:
                return False
        for i_iter in range(0, 9, 3):  # проверка на сумму по квадратам 3x3
            for j_iter in range(0, 9, 3):
                ElementSum = 0
                for i in range(i_iter, i_iter + 3):
                    for j in range(j_iter, j_iter + 3):
                        ElementSum += self.Field[i][j]
                if ElementSum != 45:
                    return False
        return True

    def PrintField(self):  # выводим поле не экан
        for i in range(9):
            for j in range(9):
                if self.Field[i][j] == 0:
                    print(' ', end=' ')
                else:
                    print(self.Field[i][j], end=' ')
            print()


class pair(object):
    def __init__(self, first, second):
        self.first = first
        self.second = second


def Decision(SudokuField, DisplayMoves=False,
             CheckPossibilitySolution=True):  # CheckPossibilitySolution костыль, проверка на невозможность модфикации
    MatrixBackup = [[0] * 9 for i in range(9)]
    for i in range(9):
        for j in range(9):
            MatrixBackup[i][j] = SudokuField.Field[i][j]

    FieldSolutions = {}
    for i in range(0, 9):  # заполняем множество возможных решений для каждой клетки
        for j in range(0, 9):
            if SudokuField.GetElem(i, j) == 0:
                IndexStr = str(i) + str(j)
                SetNumbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                FieldSolutions[IndexStr] = set(SetNumbers)

    СhangesPointer = True
    while СhangesPointer:
        СhangesPointer = False
        for i in range(9):
            for j in range(9):
                CurValue = SudokuField.GetElem(i, j)
                if CurValue != 0:
                    for RightJ in range(j + 1, 9):
                        StrTempIndex = str(i) + str(RightJ)
                        if SudokuField.GetElem(i, RightJ) == 0 and (CurValue in FieldSolutions[StrTempIndex]):
                            СhangesPointer = True
                            FieldSolutions[StrTempIndex].discard(CurValue)
                            if len(FieldSolutions[StrTempIndex]) == 1:
                                SetValueTemp = 0
                                for IterTempTemp in FieldSolutions[StrTempIndex]:
                                    SetValueTemp = IterTempTemp
                                SudokuField.SetElem(i, RightJ, SetValueTemp)
                                if DisplayMoves:  # вывод сделанного хода
                                    print(i, RightJ, SetValueTemp)
                                FieldSolutions[StrTempIndex].discard(SetValueTemp)

                    for LeftJ in range(j - 1, -1, -1):
                        StrTempIndex = str(i) + str(LeftJ)
                        if SudokuField.GetElem(i, LeftJ) == 0 and (CurValue in FieldSolutions[StrTempIndex]):
                            СhangesPointer = True
                            FieldSolutions[StrTempIndex].discard(CurValue)
                            if len(FieldSolutions[StrTempIndex]) == 1:
                                SetValueTemp = 0
                                for IterTempTemp in FieldSolutions[StrTempIndex]:
                                    SetValueTemp = IterTempTemp
                                SudokuField.SetElem(i, LeftJ, SetValueTemp)
                                if DisplayMoves:  # вывод сделанного хода
                                    print(i, LeftJ, SetValueTemp)
                                FieldSolutions[StrTempIndex].discard(SetValueTemp)

                    for UpI in range(i - 1, -1, -1):
                        StrTempIndex = str(UpI) + str(j)
                        if SudokuField.GetElem(UpI, j) == 0 and (CurValue in FieldSolutions[StrTempIndex]):
                            СhangesPointer = True
                            FieldSolutions[StrTempIndex].discard(CurValue)
                            if len(FieldSolutions[StrTempIndex]) == 1:
                                SetValueTemp = 0
                                for IterTempTemp in FieldSolutions[StrTempIndex]:
                                    SetValueTemp = IterTempTemp
                                SudokuField.SetElem(UpI, j, SetValueTemp)
                                if DisplayMoves:  # вывод сделанного хода
                                    print(UpI, j, SetValueTemp)
                                FieldSolutions[StrTempIndex].discard(SetValueTemp)

                    for DownI in range(i + 1, 9):
                        StrTempIndex = str(DownI) + str(j)
                        if SudokuField.GetElem(DownI, j) == 0 and (CurValue in FieldSolutions[StrTempIndex]):
                            СhangesPointer = True
                            FieldSolutions[StrTempIndex].discard(CurValue)
                            if len(FieldSolutions[StrTempIndex]) == 1:
                                SetValueTemp = 0
                                for IterTempTemp in FieldSolutions[StrTempIndex]:
                                    SetValueTemp = IterTempTemp
                                SudokuField.SetElem(DownI, j, SetValueTemp)
                                if DisplayMoves:  # вывод сделанного хода
                                    print(DownI, j, SetValueTemp)
                                FieldSolutions[StrTempIndex].discard(SetValueTemp)

        for IBegin in range(0, 9, 3):  # проверка на еинственность выора значения
            for JBegin in range(0, 9, 3):
                for CurValue in range(1, 10):
                    SetCoords = list()
                    for i in range(IBegin, IBegin + 3):
                        for j in range(JBegin, JBegin + 3):
                            StrTempIndex = str(i) + str(j)
                            if SudokuField.GetElem(i, j) == 0 and CurValue in FieldSolutions[StrTempIndex]:
                                SetCoords.append(StrTempIndex)
                    if len(SetCoords) == 1:
                        СhangesPointer = True
                        ElementIndex = SetCoords[0]
                        XCoordinate = int(ElementIndex[0])
                        YCoordinate = int(ElementIndex[1])
                        SudokuField.SetElem(XCoordinate, YCoordinate, CurValue)
                        if DisplayMoves:  # вывод сделанного хода
                            print(XCoordinate, YCoordinate, CurValue)
                        FieldSolutions[ElementIndex].clear()

    if CheckPossibilitySolution:
        result = SudokuField.Validation()
        SudokuField.Field = MatrixBackup
        return result
    return SudokuField.Validation()


def GenerateSudokuPuzzle():
    print('Enter the number of filled cells :')
    NumberNeroCells = 81 - int(input())
    CurrentGame = ClassSudokuField()
    CurrentGame.GenerateField()
    CurrentGame.GenerateRandomFeeld()
    CurrentGame.CreatingPuzzle(NumberNeroCells)
    CurrentGame.PrintField()
    return CurrentGame


def UserSudokuSolution(CurrentGame):
    print("If you want to exit the game enter -1")
    print("If you want to check the solved sudoku enter -2")
    print("cell coordinates and value enter in one line separated by spaces")
    TempList = list(map(int, input().split()))
    Row, Column, Number = 0, 0, 0
    if len(TempList) == 1:
        Row = TempList[0]
    else:
        Row, Column, Number = TempList[0], TempList[1], TempList[2]
    while True:
        if Row == -2:
            print(CurrentGame.Validation())
            print("Do you want to start a new game yes/no")
            ContinueDecision = input()
            if ContinueDecision == 'yes' or ContinueDecision == 'y' or ContinueDecision == '1':
                NewSession = GameSession()
            break
        elif Row == -1:
            with open('SavedGame.pickle', 'wb') as PickleFile:
                pickle.dump(CurrentGame, PickleFile)
            break

        CurrentGame.SetElem(Row, Column, Number)
        CurrentGame.PrintField()

        TempList = list(map(int, input().split()))
        Row, Column, Number = 0, 0, 0
        if len(TempList) == 1:
            Row = TempList[0]
        else:
            Row, Column, Number = TempList[0], TempList[1], TempList[2]


class GameSession(object):
    def __init__(self):
        CurrentGame = ClassSudokuField()
        if path.exists("SavedGame.pickle"):
            if os.path.getsize('SavedGame.pickle') > 0:
                with open('SavedGame.pickle', 'rb') as PickleFile:
                    CurrentGame = pickle.load(PickleFile)
            print("You have a saved game, you want to continue it yes/no")
            GameLoadingFlag = input()
            if GameLoadingFlag == 'yes' or GameLoadingFlag == 'y' or GameLoadingFlag == '1':
                CurrentGame.PrintField()
                UserSudokuSolution(CurrentGame)
            elif GameLoadingFlag == 'no' or GameLoadingFlag == 'n' or GameLoadingFlag == '0':
                print("how do you want to solve sudoku, programmatically or on your own prog/yourSelf")
                TempDecision = input()
                if TempDecision == "yourSelf" or TempDecision == "your" \
                        or TempDecision == "your" or TempDecision == "y":
                    CurrentGame = GenerateSudokuPuzzle()
                    UserSudokuSolution(CurrentGame)
                else:
                    CurrentGame = GenerateSudokuPuzzle()
                    BoolFlagTemp = Decision(CurrentGame, DisplayMoves=True)
                    if BoolFlagTemp:
                        print("Sudoku solved")
                    else:
                        print("sorry we cannot work it out")
        else:
            print("how do you want to solve sudoku, programmatically or on your own prog/yourSelf")
            TempDecision = input()
            if TempDecision == "yourSelf" or TempDecision == "your" \
                    or TempDecision == "your" or TempDecision == "y":
                CurrentGame = GenerateSudokuPuzzle()
                UserSudokuSolution(CurrentGame)
            else:
                CurrentGame = GenerateSudokuPuzzle()
                PossibilitySolve  = Decision(CurrentGame, DisplayMoves=True)
                if PossibilitySolve:
                    print("Sudoku solved successfully")
                    print()
                else:
                    print("Sorry but we cannot solve this sudoku")
                    print()
                print("Do you want to start a new game yes/no")
                ContinueDecision = input()
                if ContinueDecision == 'yes' or ContinueDecision == 'y' or ContinueDecision == '1':
                    NewSession = GameSession()


def main():
    NewSession = GameSession()


if __name__ == '__main__':
    main()
