%Use toolkit 'letswave7' to convert bdf file to mat file
function letswave7
    foldername = 'C:\Users\User\Desktop\data_original';  %folder change to bdf file's folder
    cd(foldername);
    LW_manager;                                          %built-in functions
    LW_init();
    for i = 1:32                                         %32 people's bdf file 
        fname='s'+string(i)+'.bdf';
        ffname=convertStringsToChars(fname);
        FLW_import_data.get_lwdata('filename',ffname,'pathname',foldername,'is_save',1);
    end
end

