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
        _root = root.replace(source_path, target_path)
        if os.path.exists(_root) :
            if mode == 1 :
                # remove dirs and files
                for item in os.listdir(_root) :
                    if os.path.isdir(os.path.join(_root, item)) and item not in dirs:
                        shutil.rmtree(os.path.join(_root, item))
                    elif os.path.isfile(os.path.join(_root, item)) and item not in files:
                        os.remove(os.path.join(_root, item))
        else :
            os.mkdir(_root)

        # copy dirs
        for _dir in dirs :
            t_dir = os.path.join(_root, _dir)
            if not os.path.exists(t_dir) :
                os.mkdir(t_dir)

        # copy files
        for _file in files :
            s_file = os.path.join(root, _file)
            t_file = os.path.join(_root, _file)
            if not os.path.exists(t_file) or os.path.getsize(s_file) != os.path.getsize(t_file) :
                shutil.copy2(s_file, t_file)

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
    
