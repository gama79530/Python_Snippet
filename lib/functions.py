import random 
import os, shutil

def rand_sampling(ratio, stop, start=1) :
    """
    random sampling from close interval [start, stop]

    Args :
        ratio (float): percentage of sampling
        stop (int): upper bound of sampling interval
        start (int): lower bound of sampling interval
    
    Returns :
        A random sampling list
    """
    assert 0 <= ratio and ratio <= 100, 'The ratio must be between 0 and 100.'
    assert stop >= start, 'Invalid interval'

    sample_pool = [i for i in range(start, stop + 1)]
    select_num = int(len(sample_pool) * ratio)
    return sorted(random.sample(sample_pool, select_num))

def backup_folder(source_path, target_path, mode, verbose=True) :
    """
    Backup all files and folders in source_path to target_path
    
    Args :
        source_path (str): absolute path of directory which will be backup 
        target_path (str): absolute path of directory those backup files and floders will be placed
        mode (int): 
            0 (merge) - copy files in source_path to target_path
            1 (sync) - sync source_path to target_path
        verbose(bool): print verbose message
    """

    for root, dirs, files in os.walk(source_path) :
        target_root = root.replace(source_path, target_path)
        if os.path.exists(target_root) :
            if mode == 1 :
                # remove dirs and files
                for item in os.listdir(target_root) :
                    if os.path.isdir(os.path.join(target_root, item)) and item not in dirs:
                        shutil.rmtree(os.path.join(target_root, item))
                    elif os.path.isfile(os.path.join(target_root, item)) and item not in files:
                        os.remove(os.path.join(target_root, item))
        else :
            os.mkdir(target_root)

        # copy dirs
        for target_dir in dirs :
            target_dir_path = os.path.join(target_root, target_dir)
            if not os.path.exists(target_dir_path) :
                os.mkdir(target_dir_path)

        # copy files
        for target_file in files :
            source_file_path = os.path.join(root, target_file)
            target_file_path = os.path.join(target_root, target_file)
            if not os.path.exists(target_file_path) or os.path.getsize(source_file_path) != os.path.getsize(target_file_path) :
                shutil.copy2(source_file_path, target_file_path)
    if verbose:
        print('====== Task finish!!! ======')

def rand_file_sampling(source_path, target_path, is_dir_base, ratio=0.35, merge_before=True, verbose=True):
    """
    Random sampling files from source_path to target_path

    Args :
        source_path (str): absolute path of directory which contains sample files
        target_path (str): absolute path of directory those sampled files and floders will be placed
        is_dir_base (bool): use dir as a sample unit or use file as a sample unit
        ratio (float): sampling ratio
        merge_before (bool): merge target_path files to source_path before sampling
        verbose(bool): print verbose message
    
    """
    def mkdir(path):
        if not os.path.exists(os.path.dirname(path)):
            mkdir(os.path.dirname(path))
        if not os.path.exists(path):
            os.mkdir(path)

    # sync before    
    if merge_before and os.path.exists(target_path):
        backup_folder(target_path, source_path, 0, False)
    elif os.path.exists(target_path):
        shutil.rmtree(target_path)
        
    # count number of files
    total_count = 0
    sample_pool_list = list()
    for root, dirs, files in os.walk(source_path):
        total_count += len(files)
        if is_dir_base:
            sample_pool_list.append((root, files))
        else:
            for f in files:
                sample_pool_list.append(os.path.join(root, f))

    # sampling
    random.shuffle(sample_pool_list)
    sample_count = 0 
    sample_num = min(int(ratio * total_count), total_count)
    samples_list = None 
    if is_dir_base:
        samples_list = list()
        while sample_count < sample_num:
            sample_root, sample_files = sample_pool_list.pop()
            if len(sample_files) > 0:
                samples_list.append((sample_root, sample_files))
                sample_count += len(sample_files)
    else:
        sample_count = sample_num
        samples_list = list(sample_pool_list[:sample_count])

    # rename target
    target_temp_path = target_path + str(hash(__file__))
    if os.path.exists(target_path):
        os.rename(target_path, target_temp_path)
    
    # copy files
    if is_dir_base:
        for sample_root, sample_files in samples_list:
            target_root = sample_root.replace(source_path, target_path)
            target_temp_root = target_root + str(hash(__file__))
            mkdir(target_root)
            for sample_file in sample_files:
                sample_file_path = os.path.join(sample_root, sample_file)
                target_file_path = os.path.join(target_root, sample_file)
                target_temp_file_path = os.path.join(target_temp_root, sample_file)
                if os.path.exists(target_temp_file_path) and os.path.getsize(target_temp_file_path) == os.path.getsize(sample_file_path):
                    os.rename(target_temp_file_path, target_file_path)
                else:
                    shutil.copy2(sample_file_path, target_file_path)
    else:
        for sample_file_path in samples_list:
            target_file_path = sample_file_path.replace(source_path, target_path)
            target_temp_file_path = sample_file_path.replace(source_path, target_temp_path)
            mkdir(os.path.dirname(target_file_path))
            if os.path.exists(target_temp_file_path) and os.path.getsize(target_temp_file_path) == os.path.getsize(sample_file_path):
                os.rename(target_temp_file_path, target_file_path)
            else:
                shutil.copy2(sample_file_path, target_file_path)
            
    # delete unsampled files
    if os.path.exists(target_temp_path):
        shutil.rmtree(target_temp_path)

    if verbose:
        print('total files: ' + str(total_count))
        print('sample files: ' + str(sample_count))
        print('====== Task finish!!! ======')

    