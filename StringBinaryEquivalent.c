#include <stdio.h>
#include <string.h>

//The input function
void input(char str[]){
    printf("Input a string: ");
    fgets(str, 255, stdin);
}

//Converting the decimal number to a binary number
long int decToBin(int dec){  
    long int bin = 0;
    int p = 1;
    while(dec != 0){
        bin += (dec%2)*p;
        p *= 10;
        dec /= 2;
    }
    return bin;
}


//The output function
void output(long int a[], int s){
    printf("\nThe binary string equivalent is:\n");
    for(int k = 0; k < s-1; k++){
        printf("%ld ", a[k]);
    }    
}    

int main(){
    //Taking Input
    char str[255];
    input(str);
    
    //Converting the string's characters to binary numbers
    long int bin[strlen(str)];
    
    for(int j = 0; j < strlen(str); j++){
        bin[j] = decToBin((int)(str[j]));
    }    
    
    //Printing the output
    output(bin, strlen(str));
    
    return 0;
}    