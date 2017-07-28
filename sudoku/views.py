# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from .forms import PuzzleForm
import solver


def index(request):
    puzzle_form = PuzzleForm()
    if request.method == "POST":
        puzzle_form = PuzzleForm(request.POST)
        if puzzle_form.is_valid() :
            cd = puzzle_form.cleaned_data
            txt = ""
            for k in sorted(cd): 
                if cd[k]: 
                    txt += str(cd[k])
                else: txt += '0'
            puzzle = solver.Puzzle.createFromText(txt)
            if puzzle and puzzle.is_valid() :
                solved = solver.Solver(puzzle).solve()
                results = solved.to_string()
                return render(request, 'sudoku/results.html', {'valid': True, 'results': results})
            else: 
                return render(request, 'sudoku/results.html', {'valid': False})
    else:
        puzzle_form = PuzzleForm()
    return render(request, 'sudoku/index.html', {'puzzle_form': puzzle_form})