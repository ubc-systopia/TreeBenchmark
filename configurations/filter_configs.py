import pandas as pd


def remove_configs(input_config_path, output_config_path):
    input_configs = pd.read_csv(input_config_path)
    # set the right tyes for the data frame
    input_configs = input_configs.astype({'fold': pd.Int64Dtype(), 'optimaldepth': pd.Int64Dtype(), 'max_depth': pd.Int64Dtype(), 'n_est': pd.Int64Dtype(), 'lb_max_depth': pd.Int64Dtype(), 'lb_n_est': pd.Int64Dtype()})
    
    #begin pruning:
    #currently, we want to run only lb_guess and thresholding tests, and if we are using both thresh and lbguess we want to have the sam black box hyperparameters for each
    to_remove = input_configs.index[((((input_configs['lb_guess'] == True) & (input_configs['thresh'] == True)) & ((input_configs['n_est'] != input_configs['lb_n_est'])|(input_configs['max_depth'] != input_configs['lb_max_depth']))) | ((input_configs['lb_guess'] == False) & (input_configs['thresh'] == False)))]
    output_configs = input_configs.drop(to_remove)
   
    #sort results
    output_configs.sort_values(by=['fold']) 
    #save results
    output_configs.to_csv(output_config_path, index=False)
import argparse

if __name__=="__main__":

    parser  = argparse.ArgumentParser()
    parser.add_argument("input_config_path", help="path to config file to start with")
    parser.add_argument("output_config_path", help="path to save resulting reduced config file")
    args = parser.parse_args()

    input_config_path = (args.input_config_path)
    output_config_path = (args.output_config_path)

    remove_configs(input_config_path, output_config_path)

