'''
Created on Jan 16, 2017

@author: Sonnya
'''


class SquareSolved() :
    def __init__ (self, row, col, value) :
        self.value = value
        self.row = row
        self.col = col
        self.box = int(row/3)*3 + int(col/3)
        
    def __str__ (self) :
        return "Row="+str(self.row)+" Col="+str(self.col)+" Box="+str(self.box)+"; Val="+str(self.value)
           

class SquareToSolve():
    def __init__ (self, row, col, candidates=None) :
        self.candidates = set(candidates) if candidates else set()
        self.row = row
        self.col = col
        self.box = int(row/3)*3 + int(col/3)
        
    def __eq__ (self, other) :
        return self.row==other.row and self.col==other.col
        
    def __ne__(self, other) :
        return not __eq__(self, other)
    
    def __str__ (self) :
        return "Row="+str(self.row)+" Col="+str(self.col)+" Box="+str(self.box)+"; Ans="+str(self.candidates)
    
    def setCandidates(self, numbers):
        self.candidates = set(numbers)
    
    def getAdjacentColNumbers(self) :
        n1 = int(self.col/3)*3
        n2 = n1+3
        return list(set(range(n1,n2)).difference([self.col]))
    
    def getAdjacentRowNumbers(self) :
        n1 = int(self.row/3)*3
        n2 = n1+3
        return list(set(range(n1,n2)).difference([self.row]))
    
    def getAdjacentVBoxNumbers(self) :
        n1 = self.box%3
        n2 = n1+3
        n3 = n2+3
        return list(set([n1,n2,n3]).difference([self.box]))
    
    def getAdjacentHBoxNumbers(self) :
        n1 = int(self.box/3)*3
        n2 = n1+3
        return list(set(range(n1,n2)).difference([self.box]))
    
    def identical (self, other) :
        '''if self.row==7 and self.col==0 and other.row==7 and other.col==3 :
            print "idenical start"
            print set(self.candidates)
            print set(other.candidates)
            print set(self.candidates)-set(other.candidates)
            print (set(self.candidates)-set(other.candidates))==set()
            print "iden end"
        '''
        return self.candidates==other.candidates
        
        
class Puzzle() :
    
    ID = 0
    
    def __init__ (self, listRows, idspec=None) :
        
        if idspec :
            self.id = idspec
        
        else :
            Puzzle.ID+=1
            self.id = Puzzle.ID
        
        self.listToSolve  = list()
        self.listSolved   = list()
        self.listRows     = [[],[],[],[],[],[],[],[],[]]
        self.listColumns  = [[],[],[],[],[],[],[],[],[]]
        self.listBoxes    = [[],[],[],[],[],[],[],[],[]]
        self.listRowAns   = [[],[],[],[],[],[],[],[],[]]
        self.listColAns   = [[],[],[],[],[],[],[],[],[]]
        self.listBoxAns   = [[],[],[],[],[],[],[],[],[]]
        
        for r, line in enumerate(listRows) :
            for c, num in enumerate(line) :
                if num==0 :
                    self.listToSolve.append(SquareToSolve(r, c))
                else :
                    self.listSolved.append(SquareSolved(r, c, num))        
                    
        for sq in self.listSolved :
            self.listRows[sq.row].append(sq)
            self.listColumns[sq.col].append(sq)
            self.listBoxes[sq.box].append(sq)
            
        for sq in self.listToSolve :
            self.listRowAns[sq.row].append(sq)
            self.listColAns[sq.col].append(sq)
            self.listBoxAns[sq.box].append(sq)
            
            
    def __str__(self) :
        s = ""
        
        if self.isSolved():
            s += "(SOLVED)"
        s += "\n"
        
        for r in range(9) :
            row = ""
            for c in range(9) :
                if self.getItem(r,c) :
                    row+=(str(self.getItem(r,c).value))
                else :
                    row+="0"
            s += row + '\n'
        return s
    
    def to_string(self)  :
        result = []
        for r in range(9) :
            row = ""
            for c in range(9) :
                if self.getItem(r,c) :
                    row+=(str(self.getItem(r,c).value))
                else :
                    row+="0"
            result.append(row)
        return result
        
        
    def getItem (self, row, col):
        for sq in self.listSolved :
            if sq.row==row and sq.col==col :
                return sq
            
            
    def getCandidates (self, row, col):
        for sq in self.listToSolve :
            if sq.row==row and sq.col==col :
                return sq
    
    def switchToUnsolved (self, row, col, cand) :
        sq2del = self.getItem(row, col)
        if sq2del :
            self.listSolved.remove(sq2del)
            self.listRows[row].remove(sq2del)
            self.listColumns[col].remove(sq2del)
            self.listBoxes[sq2del.box].remove(sq2del)
            del sq2del
        
            sq = SquareToSolve(row, col)
            sq.setCandidates(cand)
            self.listToSolve.append(sq)
            self.listRowAns[row].append(sq)
            self.listColAns[col].append(sq)
            self.listBoxAns[sq.box].append(sq)
            
        else :
            sq = self.getCandidates(row, col)
            sq.setCandidates(cand)
    
    
    def getRowSet(self, row):
        return set(sq.value for sq in self.listRows[row])
    
    
    def getColSet(self, col):
        return set(sq.value for sq in self.listColumns[col])
    
    
    def getBoxSet(self, box):
        return set(sq.value for sq in self.listBoxes[box])
    
    
    def positionsInBox(self, num, boxList):
        listPos=[]
        for sq in boxList :
            if num in sq.candidates :
                listPos.append(sq)
        return listPos
    
    
    def getVerticalNeighbors(self, item) :
        vn = []
        r  = item.getAdjacentRowNumbers()
        for sq in self.listSolved :
            if sq.row in r and sq.col==item.col :
                vn.append(sq)
        return vn
    
    
    def solveSquare(self, sq2s, num) :
        sq = SquareSolved(sq2s.row, sq2s.col, num)
        self.listSolved.append(sq)
        self.listRows[sq.row].append(sq)
        self.listColumns[sq.col].append(sq)
        self.listBoxes[sq.box].append(sq)
        
        for s in self.listToSolve :
            if s.row==sq.row or s.col==sq.col or s.box==sq.box :
                if num in s.candidates :
                    s.candidates.remove(num)
        
        self.listToSolve.remove(sq2s)
        self.listRowAns[sq.row].remove(sq2s)
        self.listColAns[sq.col].remove(sq2s)
        self.listBoxAns[sq.box].remove(sq2s)
        del sq2s
    
    def solveSquareByRowCol(self, row, col, num) :
        sq2s = self.getCandidates(row, col)
        sq = SquareSolved(sq2s.row, sq2s.col, num)
        self.listSolved.append(sq)
        self.listRows[sq.row].append(sq)
        self.listColumns[sq.col].append(sq)
        self.listBoxes[sq.box].append(sq)
        
        for s in self.listToSolve :
            if s.row==sq.row or s.col==sq.col or s.box==sq.box :
                if num in s.candidates :
                    s.candidates.remove(num)
        
        self.listToSolve.remove(sq2s)
        self.listRowAns[sq.row].remove(sq2s)
        self.listColAns[sq.col].remove(sq2s)
        self.listBoxAns[sq.box].remove(sq2s)
        del sq2s    
    
    def isSolved(self) :
        if len(self.listToSolve)>0 :
            return False
        return True
    
    
    def is_valid_answer(self):
        if not self.isSolved():
            return False
        
        for row in self.listRows :
            num = set(list(sq.value for sq in row))
            if num-set(range(1,10)) :
                return False
            
        for col in self.listColumns :
            num = set(list(sq.value for sq in col))
            if num-set(range(1,10)) :
                return False
            
        for box in self.listRows :
            num = set(list(sq.value for sq in box))
            if num-set(range(1,10)) :
                return False
            
        return True
    
    def is_valid(self):        
        for row in self.listRows :
            num = list(sq.value for sq in row)
            if len(num) != len (set(num)) :
                return False
            
        for col in self.listColumns :
            num = set(list(sq.value for sq in col))
            if len(num) != len (set(num)) :
                return False
            
        for box in self.listRows :
            num = set(list(sq.value for sq in box))
            if len(num) != len (set(num)) :
                return False
            
        return True
    
    @classmethod
    def createFromText(cls, txt) :
        listNb = []
        for i in range(0, 9):
            row = [int(number) for number in txt[9*i:9*(i+1)]]
            listNb.append(row)
        if len(listNb) != 9 :
            return
        for i in range(0,9) :
            if len(listNb[i]) != 9 :
                return
        return cls(listNb)
                
        
import copy, time

class Solver() :
    
    def __init__(self, puzzle) :
        self.puzzle = puzzle
    
    def solve(self) :
        self.setUpAns()
        old_count = 81
        while not self.puzzle.isSolved() and old_count > len(self.puzzle.listToSolve) :
            old_count  = len(self.puzzle.listToSolve)
            while self.methodBasic() < len(self.puzzle.listToSolve) :
                pass
            while self.methodBasic2() < len(self.puzzle.listToSolve) :
                pass
            self.methodElimByRowOrCol()
            self.methodSimilarSet()
            self.methodXWing()
        if not self.puzzle.is_valid_answer() :
            self.brute_force()
        return self.puzzle
    
    # The very basic method in solving a Sudoku puzzle that will give one unique answer per square whenever possible
    def setUpAns(self) :
        for sq in self.puzzle.listToSolve :
            rowSet = self.puzzle.getRowSet(sq.row)
            colSet = self.puzzle.getColSet(sq.col)
            boxSet = self.puzzle.getBoxSet(sq.box)
            
            # Gives a list of numbers that are neither in the row, column, and box
            ans = set(list(x for x in list(range(1,10)) if x not in rowSet and x not in colSet and x not in boxSet))
            sq.setCandidates(ans)
    
    # Returns the number of squares with no unique answer
    def methodBasic(self) :
        counter = 0
        for sq in self.puzzle.listToSolve:
            rowSet = self.puzzle.getRowSet(sq.row)
            colSet = self.puzzle.getColSet(sq.col)
            boxSet = self.puzzle.getBoxSet(sq.box)
            
            # If there's only one unique answer, this value is assigned directly
            ans = list(sq.candidates)
            if len(ans)==1 :
                self.puzzle.solveSquare(sq, ans[0])
                continue
            
            # Otherwise, use the adjacent columns method
            col2 = min(sq.getAdjacentColNumbers()) 
            col3 = max(sq.getAdjacentColNumbers())
            row2 = min(sq.getAdjacentRowNumbers()) 
            row3 = max(sq.getAdjacentRowNumbers())
            
            sqU = self.puzzle.getItem(row2,sq.col)
            sqD = self.puzzle.getItem(row3,sq.col)
            sqL = self.puzzle.getItem(sq.row,col2)
            sqR = self.puzzle.getItem(sq.row,col3)
            
            colSet2 = self.puzzle.getColSet(col2)
            colSet3 = self.puzzle.getColSet(col3)
            ansByCols = list(colSet2 & colSet3 - boxSet - rowSet - colSet)
            
            if len(ansByCols)==1 and sqU and sqD :
                self.puzzle.solveSquare(sq, ansByCols[0])
                continue
            
            rowSet2 = self.puzzle.getRowSet(row2)
            rowSet3 = self.puzzle.getRowSet(row3)
            ansByRows = list(rowSet2 & rowSet3 - boxSet - rowSet - colSet)
                
            if len(ansByRows)==1 and sqL and sqR :
                self.puzzle.solveSquare(sq, ansByRows[0])
                continue
            
            counter+=1
        return counter
    # retrieve unique element (hidden unique)
    
    def methodBasic2(self) :
        counter = 0
        for sq in self.puzzle.listToSolve :
            rowSet = self.puzzle.getRowSet(sq.row)
            colSet = self.puzzle.getColSet(sq.col)
            boxSet = self.puzzle.getBoxSet(sq.box)
            rowAnsList = self.puzzle.listRowAns[sq.row]
            colAnsList = self.puzzle.listColAns[sq.col]
            boxAnsList = self.puzzle.listBoxAns[sq.box]
            
            for rcb in [rowAnsList, colAnsList, boxAnsList] :
                ans = sq.candidates
                for sm in rcb :
                    if not(ans) :
                        break
                    if sm is not sq :
                        ans = ans - sm.candidates
                if len(ans)==1 and list(ans)[0] not in rowSet and list(ans)[0] not in colSet and list(ans)[0] not in boxSet :
                    self.puzzle.solveSquare(sq, list(ans)[0])
                    break
            
            counter+=1
        return counter                        
      
    def methodSimilarSet(self) :
        for sq in self.puzzle.listToSolve :
            rowAnsList = self.puzzle.listRowAns[sq.row]
            colAnsList = self.puzzle.listColAns[sq.col]
            boxAnsList = self.puzzle.listBoxAns[sq.box]
            for rcb in [rowAnsList, colAnsList, boxAnsList] :
                ans  = sq.candidates
                iden = []
                iden.append(sq)
                
                for sm in rcb :
                    if sm is not sq :
                        if sq.identical(sm) :
                            iden.append(sm)
                if len(ans)==len(iden) :
                    for sm in rcb :
                        if sm is not sq and sm not in iden :
                            if ans & sm.candidates :
                                sm.setCandidates(sm.candidates-ans)
                                                                      
    def methodElimByRowOrCol(self) :
        for i in range(1,10) :
            for box in self.puzzle.listBoxAns :
                pos1=self.puzzle.positionsInBox(i, box)
                if len(pos1)<=3 :
                    
                    row = set([sq.row for sq in pos1])
                    if len(row)==1 :
                        row = list(row)[0]
                        for sq in self.puzzle.listRowAns[row] :
                            if sq not in pos1 :
                                if i in sq.candidates :
                                    sq.candidates.remove(i)
                        continue
                             
                    col = set([sq.col for sq in pos1])
                    if len(col)==1 :
                        col = list(col)[0]
                        for sq in self.puzzle.listColAns[col] :
                            if sq not in pos1 :
                                if i in sq.candidates :
                                    sq.candidates.remove(i)
                        continue  
    
    def methodXWing(self) :
        for i in range(1,10) :
            #time.sleep(1)
            for box1 in self.puzzle.listBoxAns :
                pos1 = self.puzzle.positionsInBox(i, box1)
                if len(pos1)==2 :
                    row1 = set([sq.row for sq in pos1])
                    if len(row1)==1 :
                        row1 = list(row1)[0]
                        col1 = [sq.col for sq in pos1]
                        boxs = pos1[0].getAdjacentVBoxNumbers()
                        for box2 in boxs :
                            pos2 = self.puzzle.positionsInBox(i, self.puzzle.listBoxAns[box2])
                            row2 = set([sq.row for sq in pos2])
                            if len(row2)==1 :
                                row2 = list(row2)[0]
                                col2 = [sq.col for sq in pos2]
                                if set(col1)==set(col2) :
                                    for sq in self.puzzle.listToSolve :
                                        if sq.row==row1 or sq.row==row2 or sq.col in col1 :
                                            if sq not in pos1 and sq not in pos2 :
                                                if i in sq.candidates :
                                                    sq.candidates.remove(i)
                                                    #print sq
                                    continue
                    col1 = set([sq.col for sq in pos1])
                    if len(col1)==1 :
                        col1 = list(col1)[0]
                        row1 = [sq.row for sq in pos1]
                        boxs = pos1[0].getAdjacentHBoxNumbers()
                        for box2 in boxs :
                            pos2 = self.puzzle.positionsInBox(i, self.puzzle.listBoxAns[box2])
                            col2 = set([sq.col for sq in pos2])
                            if len(col2)==1 :
                                col2 = list(col2)[0]
                                row2 = [sq.col for sq in pos2]
                                if set(row1)==set(row2) :
                                    for sq in self.puzzle.listToSolve :
                                        if sq.col==col1 or sq.col==col2 or sq.row in row1 :
                                            if sq not in pos1 and sq not in pos2 :
                                                if i in sq.candidates :
                                                    sq.candidates.remove(i)
                                continue

    def brute_force(self) :
        self.setUpAns()
        dict_to_solve   = {}
        for i, sq in enumerate(self.puzzle.listToSolve) :
            dict_to_solve[i] = sq
        dict_const = copy.deepcopy(dict_to_solve)
        dict_const_abs = copy.deepcopy(dict_to_solve)
        n = 0
        while not self.puzzle.isSolved() :
            sq  = dict_to_solve[n]
            sr  = self.puzzle.getCandidates(sq.row, sq.col)
            for i, sd in dict_to_solve.iteritems() :
                if i >= n :
                    rowSet = self.puzzle.getRowSet(sd.row)
                    colSet = self.puzzle.getColSet(sd.col)
                    boxSet = self.puzzle.getBoxSet(sd.box)
                    sd.setCandidates(sd.candidates - rowSet - colSet - boxSet)
            num = list(sq.candidates)
            if num :
                self.puzzle.solveSquare(sr, num[0])
                try :
                    sq.candidates.remove(num[0])
                except KeyError :
                    pass
                n += 1   
            else :
                m = n
                while True :
                    n  -= 1
                    sq  = dict_to_solve[n]
                    sr  = self.puzzle.getCandidates(sq.row, sq.col)
                    if sq.candidates :
                        for key, x in dict_const_abs.iteritems() :
                            if key > n :
                                dict_to_solve[key].candidates = x.candidates
                                dict_const[key].candidates    = x.candidates
                            if key >= n and key <= m :
                                self.puzzle.switchToUnsolved(x.row, x.col, x.candidates)
                        sr = self.puzzle.getCandidates(sq.row, sq.col)
                        sr.setCandidates(dict_to_solve[n].candidates)
                        break