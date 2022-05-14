#!/usr/bin/python

from distutils.core import run_setup
import subprocess
from pathlib import Path
import shutil
import argparse


def compile(nb, run_tests=False):
    if run_tests:
        subprocess.check_call(
            ['otter', 'assign', str(nb), str(tmp),  '--v1'])
    else:
        subprocess.check_call(
            ['otter', 'assign', '--no-run-tests', str(nb), str(tmp),  '--v1'])

def copy_assignmet(src, dst, grading=False):
    dst.mkdir(parents=True, exist_ok=True)
    for file in src.iterdir():
        if file.is_dir():
            # copy dir
            shutil.copytree(file, dst.joinpath(
                file.name), dirs_exist_ok=True)
        elif grading or str(file.suffix) in extensions:
            # copy file
            shutil.copyfile(file, dst.joinpath(file.name))
    
def copy_content(training, grading=False):
    # students
    src = tmp.joinpath('student')
    dst = students_dir.joinpath(training.name)
    clean(dst)
    copy_assignmet(src, dst)

    # solutions with or without grading information
    src = tmp.joinpath('autograder')
    dst = solution_dir.joinpath(training.name)
    clean(dst)
    copy_assignmet(src, dst, grading)

def clean(dir):
    if dir.exists():
        shutil.rmtree(str(dir))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate student and solution notebooks.')
    parser.add_argument('-m', '--master', dest='master', type=str, default='master',
                        help='path to the master directory')
    parser.add_argument('-sol', '--solutions', dest='solutions', type=str, default='solutions',
                        help='path to the solutions directory')
    parser.add_argument('-s', '--students', dest='students', type=str, default='students',
                        help='path to the students directory')
    parser.add_argument('-t', '--trainings', dest='trainings', type=str,
                        help='list of specific training directories', nargs='*')
    parser.add_argument('-rt', '--runTests', action='store_true',
                        help='run otter tests if this flag is set')
    parser.add_argument('-g', '--grading', action='store_true',
                        help='keep the grading information')

    tmp = Path('tmp')
    extensions = ['.ipynb', '.pdf', '.txt',
                  '.gif', '.jpeg', '.jpg', '.png', '.svg']

    args = parser.parse_args()
    solution_dir = Path(args.solutions)
    master_dir = Path(args.master)
    students_dir = Path(args.students)
    run_tests = args.runTests
    grading = args.grading
    if hasattr(args, 'trainings'):
        trainings = args.trainings
    else:
        trainings = None
    print('########## start build process ##########')
    print(f'master dir: {master_dir}')
    print(f'solution dir: {solution_dir}')
    print(f'student dir: {students_dir}')
    print(f'trainings dir: {trainings}')
    print(f'run test: {run_tests}')
    print(f'grading: {grading}')
    
    if not tmp.exists():
        for training_dir in master_dir.iterdir():
            if (training_dir.is_dir() and trainings == None) or (trainings != None and training_dir.name in trainings):
                path_in_str = str(training_dir)
                found = False
                print(f'\nprocess: {training_dir}')
                for nb in training_dir.iterdir():
                    if nb.match('*.ipynb'):
                        compile(nb)
                        copy_content(training_dir, grading)
                        clean(tmp)
                        found = True
                if not found:
                    shutil.copytree(training_dir, students_dir.joinpath(
                        training_dir.name), dirs_exist_ok=True)
    else:
        print('Error: the temporary directory tmp already exists. Pleare remove it and try again.')
        exit(-1)
    
    print('########## build process finished ##########')
