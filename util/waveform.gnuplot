set terminal png transparent size 500,100;

unset key;
unset tics;
unset border;
set lmargin 0;
set rmargin 0;
set tmargin 0;
set bmargin 0;

plot '<cat' binary filetype=bin format='%int16' endian=little array=1:0 with lines lt rgb "blue";