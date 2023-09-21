import h5py
from scarlink.src.model import RegressionModel

def read_model(out_dir, out_file_name = 'coefficients.hd5', input_file_name='', read_only=False):
    """Read SCARlink outputs.
    
    Parameters
    ----------
    out_dir : str
        Directory in which SCARlink regression outputs are going to be saved. The function creates 
        directory <output dir>/scarlink_out in which results are saved.
    out_file_name : str
        Name of the regression output file. The output file is saved in <output dir>/scarlink_out/. 
        The output file name has the format coefficients_<process_number>.hd5. The <process_id> is None
        if SCARlink is run sequentially on all genes in coassay_matrix.h5. If SCARlink is submitted as
        a parallel job on the cluster then process_number would be the index for a given split.
    input_file : str
        coassay_matrix.h5 file generated by scarlink_preprocessing. This file name is pulled 
        from the output directory provided by the --outdir parameter. The output directory 
        contains file coassay_matrix.h5 generated by scarlink_preprocessing.
    read_only : bool
        Whether to open out_file_name in read-only mode.

    Returns
    -------
    m
        RegressionModel object.
    """
    # read_only=True: mode = 'r', else mode = 'a'
    out_dir = out_dir + '/' if out_dir[-1] != '/' else out_dir
    
    f = h5py.File(out_dir + out_file_name, mode = 'r')
    # if input_file_name == '': input_file_name = f['genes'].attrs['input_file_name']
    dirname = '/'.join(out_dir[:-1].split('/')[:-1]) + '/'
    input_file_name = dirname + 'coassay_matrix.h5'
    gtf_file = f['genes'].attrs['gtf_file']
    scatac_fragment_file = f['genes'].attrs['scatac_fragment_file']
    f.close()

    if read_only: mode = 'r'
    else: mode = 'a'
    m = RegressionModel(input_file = input_file_name, output_dir = out_dir, gtf_file = gtf_file, scatac_fragment_file = scatac_fragment_file, out_file_name = out_file_name, mode=mode)
    return m
