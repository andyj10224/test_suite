import os
import sys
import databases.s22 as s22

def _gen_inputs_s22(testname, subset, template_path):
    if not os.path.isdir(testname):
        os.system(f'mkdir {testname}')
    
    test_dir_path = os.path.join(testname, subset)
    if not os.path.isdir(test_dir_path):
        os.system(f'mkdir {test_dir_path}')
    
    s22_path = os.path.join(test_dir_path, 's22')
    if not os.path.isdir(s22_path):
        os.system(f'mkdir {s22_path}')

    input_dir_path = os.path.join(s22_path, 'inputs')
    if not os.path.isdir(input_dir_path):
        os.system(f'mkdir {input_dir_path}')

    template_file = open(template_path, 'r')
    template_lines = template_file.readlines()

    for k, v in s22.dimer.items():
        input_file_path = os.path.join(input_dir_path, f's22_dimer_{k}.in')
        input = open(input_file_path, 'w')
        for line in template_lines:
            if '### MOLECULE ###' in line:
                input.write(f'{v}\n')
            else:
                input.write(line)

    for k, v in s22.monoA.items():
        input_file_path = os.path.join(input_dir_path, f's22_monoA_{k}.in')
        input = open(input_file_path, 'w')
        for line in template_lines:
            if '### MOLECULE ###' in line:
                input.write(f'{v}\n')
            else:
                input.write(line)
    
    for k, v in s22.monoB.items():
        input_file_path = os.path.join(input_dir_path, f's22_monoB_{k}.in')
        input = open(input_file_path, 'w')
        for line in template_lines:
            if '### MOLECULE ###' in line:
                input.write(f'{v}\n')
            else:
                input.write(line)

def _run_s22(testname, subset, psipath, ncore):

    input_dir_path = os.path.join(testname, subset, 's22', 'inputs')
    if not os.path.isdir(input_dir_path):
        raise Exception("You idiot! You have not made the inputs yet!!!")
    
    output_dir_path = os.path.join(testname, subset, 's22', 'outputs')
    if not os.path.isdir(output_dir_path):
        os.system(f'mkdir {output_dir_path}')

    timer_dir_path = os.path.join(testname, subset, 's22', 'timings')
    if not os.path.isdir(timer_dir_path):
        os.system(f'mkdir {timer_dir_path}')

    for k, v in s22.dimer.items():
        input_file_path = os.path.join(input_dir_path, f's22_dimer_{k}.in')
        cmd1 = f'{psipath} -n {ncore} {input_file_path}'
        cmd2 = f'mv {input_dir_path}/s22_dimer_{k}.out {output_dir_path}/s22_dimer_{k}.out'
        cmd3 = f'mv timer.dat {timer_dir_path}/s22_dimer_{k}.time'
        os.system(f'{cmd1} && {cmd2} && {cmd3}')

    for k, v in s22.monoA.items():
        input_file_path = os.path.join(input_dir_path, f's22_monoA_{k}.in')
        cmd1 = f'{psipath} -n {ncore} {input_file_path}'
        cmd2 = f'mv {input_dir_path}/s22_monoA_{k}.out {output_dir_path}/s22_monoA_{k}.out'
        cmd3 = f'mv timer.dat {timer_dir_path}/s22_monoA_{k}.time'
        os.system(f'{cmd1} && {cmd2} && {cmd3}')
    
    for k, v in s22.monoB.items():
        input_file_path = os.path.join(input_dir_path, f's22_monoB_{k}.in')
        cmd1 = f'{psipath} -n {ncore} {input_file_path}'
        cmd2 = f'mv {input_dir_path}/s22_monoB_{k}.out {output_dir_path}/s22_monoB_{k}.out'
        cmd3 = f'mv timer.dat {timer_dir_path}/s22_monoB_{k}.time'
        os.system(f'{cmd1} && {cmd2} && {cmd3}')

def gen_input_files(database, testname, subset, template_path):
    if database.lower() == 's22':
        _gen_inputs_s22(testname, subset, template_path)
    else:
        raise Exception(f"Database {database} is currently not available!")

def run_jobs(database, testname, subset, psipath, ncore):
    if os.path.isfile('timer.dat'):
        os.system('rm timer.dat')
    if database.lower() == 's22':
        _run_s22(testname, subset, psipath, ncore)
    else:
        raise Exception(f"Database {database} is currently not available!")

if __name__ == '__main__':
    args = sys.argv
    mode = args[1]
    database = args[2]
    method = args[3]
    subset = args[4]
    template = args[5]
    psipath = args[6]
    ncore = int(args[7])

    # Example call to the script:
    # python testjet.py generate s22 linK reference template/ref_template.in (full path of jeff4) 8

    if mode.lower() == 'generate':
        gen_input_files(database, method, subset, template)
    elif mode.lower() == 'run':
        run_jobs(database, method, subset, psipath, ncore)