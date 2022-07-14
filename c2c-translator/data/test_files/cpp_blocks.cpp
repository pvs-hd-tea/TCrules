int j = 1;
while (j < 5) {
    std::cout<<j;
    if (j==2) {
        std::cout<<"j has the value 2";
        a = 5;
    }
    if (j==3) {
        std::cout<<"j has the value 3";
    }
    else {
        std::cout<<"j has not the value 3";
    }
    if (j==4) {
        std::cout<<"j has the value 4";
    }
    j = j + 1;
}