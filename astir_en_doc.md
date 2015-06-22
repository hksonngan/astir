
```
# ls

Listing all variables in work space
ls
    
# ldir

Listing the current directory
ldir
    
# rm

Remove variables in work space
rm all
rm <name>
rm <name1> <name2> ...
rm <na*>
    
# mv

Move/rename variables
mv <source_name> <target_name>
    
# cp

Copy variable
cp <source_name> <target_name>
    
# mem

Memories used in work space by the variables
mem
    
# fun

Listing funtions available in Astir
fun
    
# save_var

Save Astir variable to file
save_var <var_name> <file_name>
    
# save_world

Save the whole work space to a file
save_world <file_name>
    
# load_var

Load variable fron file to work space
load_var <file_name>
    
# load_world

Load a work space from a file
load_world <file_name>    
    
# load_im

Load images from files
Only one image
load_im <file_name.[bmp, jpg, png]>
Several images as a sequence
load_im <file_na*.png>
    
# save_im

Save image from a variable to a file
save_im <mat_name> <file_name.[bmp, jpg, png]>
    
# show_mat

Display a mat variable as an image
show_mat <mat_name>
show_mat <mat1_name> <mat2_name> ...
    
# color2gray

Convert mat color (RGB or RGBA) to gray scale (Luminance)
Convert in-place
color2gray <mat_name>
Convert to new mat
color2gray <mat_name> <mat_new_name>
Convert a mat sequence in-place
color2gray <seq_name>
Convert a mat sequence to a new one
color2gray <seq_name> <seq_new_name>
    
# seq2mat

Extract mat variables from a sequence
Only one
seq2mat <seq_name> 5 <basename_mat>
Or several mat, in this case 3 mats
seq2mat <seq_name> 2:4 <basename_mat>
Or all mat store in the sequence
seq2mat <seq_name> all <basename_mat>
new mat name = <basename_mat> + index (format 000)
% seq2mat test 2 res
res002
    
# seq_reg_ave

This function use a simple registration to match images together
and compute the averages. The sequence of matrices must be in gray scale.

seq_reg_ave <seq_name> <dx> <dy> <ws>

dx: is the translation range search on x (x-dx to x+dx)
dy: is the translation range search on y (y-dy to y+dy)
ws: window size used to track translation between images (must be odd)

seq_reg_ave im 10 10 35
    
# load_vid

Load video (avi file only) to a sequence
load_vid <video_name> <frame_per_second>
    
# wiener

Image restoration by Wiener filter
wiener <mat_source_name> <mat_res_name>
    
# mosaicing

Create mosaicing from two images
mosaicing <mat_1> <mat_2>
    
# cut_seq

Cut a part of sequence to another sequence, start and stop
specifies the part you want keep

cut_seq <seq_name> <start_num:stop_num> <new_seq_name>

cut_seq vid1 :24 vid2   # keep only first image to 24
cut_seq vid1 10:24 vid2 # keep 10 to 24
cut_seq vid1 :24 vid2   # keep 10 to last image
    
```