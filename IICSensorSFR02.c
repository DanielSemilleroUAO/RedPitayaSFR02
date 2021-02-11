#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <linux/ioctl.h>
#include <sys/ioctl.h>
#include <linux/i2c-dev.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <stdint.h>
#define I2C_SLAVE_FORCE 		   0x0706
#define I2C_SLAVE    			   0x0703   
#define I2C_FUNCS    			   0x0705    
#define I2C_RDWR    			   0x0707   
#define EEPROM_ADDR            	   0x3c
#define PAGESIZE                   32
#define EEPROMSIZE                 64*1024/8
int fd； 
int main(int argc， char *argv[])
{
    int status；
	char *buffer = (char *)malloc(EEPROMSIZE * sizeof(char))；
	unsigned char a1[] = {2，0x00}；
	unsigned char recbuff[6]；
int offset = 0x100；
	ssize_t bytes_written；
    ssize_t bytes_read；
    fd = open("/dev/i2c-0"， O_RDWR)；
    if(fd < 0)
    {
        printf("Cannot open the IIC device\n")；
        return 1；
    }
    status = ioctl(fd， I2C_SLAVE， EEPROM_ADDR>>1)；
    if(status < 0)
    {
        printf("Unable to set the IIC address\n")；
        return -1；
    }
	 bytes_written = write(fd，a1，2)；
     if(bytes_written < 0){
         fprintf(stderr， " write address error.\n")；
         return -1；
     }
    a1[0] = 0x03；
	while(1)
	{
		int i=5000000；
		int j=5000000；
	write(fd，a1，1)；
		bytes_read = read(fd， recbuff， 6)；
		if(bytes_read < 0){
			fprintf(stderr， "read error.\n")；
			return -1；
		}
printf("%d %d %d %d %d %d\n"，recbuff[0]，recbuff[1]，recbuff[2]，recbuff[3]，recbuff[4]，recbuff[5])；
   		while(i--){} 
		while(j--){}
	}
    close(fd)；
    free(buffer)；
    return 0；
}