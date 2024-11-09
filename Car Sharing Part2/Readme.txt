There are all the individual 7 questions as separate modules (Part2 Q1 ... Q7). You can integrate them into one module as in previous part by omitting the common codes like import statements at the same time being careful not to exclude the distinct ones. Also the dataframe populating is same in all the modules, so should be included once in the integrated module.
                      # Load the CarSharing.csv file
                      df = pd.read_csv('Updated_CarSharing.csv')
There will be cases where the execution seem to freeze, but that is just the process time to execute large dataset. Also where graphical plots pop up, execution will stall and continue execution only when they are closed. For Q4, after closing the acf and pacf plots, you will be prompted to enter the values of 'p' and 'q' which is decided upon studying the acf and pacf plots and that requires the knowledge to do so. You may have to call to know the process to do so. (the values to enter in this case will most likely be p = 2 and q = 1 if I recall correct).
If there are FutureWarnings prompted you are supposed to ignore them. Some could be suppressed, like for question 5 I believe, where you start your execution by executing the command `$env:TF_ENABLE_ONEDNN_OPTS=0` in your terminal before actually proceeding with your execution.
The CarSharing.csv file should be present in your working directory. The `CarSharingDB`is the database created in the previous part and should also be included in the working directory. The `Updated_CarSharing.csv` file is the product (output) of the execution of the module Part2 Q1 and will be created automatically on its successful execution (but is also included just for clarity, ideally place it in a different folder just for backup).






