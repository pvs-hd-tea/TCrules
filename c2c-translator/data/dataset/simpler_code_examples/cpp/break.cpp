#include <iostream>
  
int main(){
	int count = 0;
    while (true) {
    	std::cout<<count<<std::endl;
        count += 1;
        if (count >= 5){
        	break;
        }
    }
	return 0;
}
