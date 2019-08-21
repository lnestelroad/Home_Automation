#!/bin/bash

FILES=~/Documents/Home_Automation/actions/*

for f in $FILES
do 
    echo -e "#!/bin/bash\n" > $f
    echo -e 'echo "Service not avaliable yet" >> /tmp/home_automation/logs.txt' >> $f
    echo -e 'echo $1 $0' >> $f
done

