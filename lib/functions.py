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

def backup_folder(source_path, target_path, mode=0) :
    """
    Backup all files and folders in source_path to target_path
    
    Args :
        source_path (str): absolute path which will be backup 
        target_path (str): absolute path which will place those backup files and floders
        mode (int): 
            0 (merge) - copy files in source_path to target_path
            1 (sync) - sync source_path to target_path

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

    print('====== Task finish!!! ======')

def rand_file_sampling(source_path, target_path, ratio=0.5, sync_before=True):
    """
    Random sampling files from source_path to target_path

    Args :
        source_path (str): absolute path which will be sampled 
        target_path (str): absolute path which will place those sampled files and floders
        ratio: sampling ratio
        sync_before: sync target_path files to source_path before sampling
    
    """
    if sync_before:
        backup_folder(target_path, source_path, 0)
    
    # count number of files
    count = 0
    
