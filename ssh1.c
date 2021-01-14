#include<stdio.h>
#include<stdlib.h>
#include<libssh/libssh.h>
#include<string.h>
int verify_host(ssh_session ss);
int verify_user(ssh_session ss);
int show_remote_process(ssh_session ss);

int main(){
	int rc;
	ssh_session ss = ssh_new();
	if(ss==NULL){
		printf("ssh_new error\n");
		exit(-1);
	}
	
	int verb = SSH_LOG_PROTOCOL;
	int port = 22;
	ssh_options_set(ss,SSH_OPTIONS_HOST,"localhost");
	ssh_options_set(ss,SSH_OPTIONS_LOG_VERBOSITY,&verb);
	ssh_options_set(ss,SSH_OPTIONS_PORT,&port);
	rc = ssh_connect(ss);
    if(rc!=SSH_OK){
        printf("ssh_connect error\n");
        exit(-1);
    }

    if(verify_host(ss)==-1){
            1;
            //return -1;
    }    
    verify_user(ss);    
    show_remote_process(ss);

    ssh_disconnect(ss);
	ssh_free(ss);	
	return 1;
}


int verify_host(ssh_session ss){
    unsigned char *hash = NULL;
    ssh_key srv_pubkey = NULL;
    char buff[10];
    size_t hlen;
    char *hexa;
    int rc;
    
    if(ssh_get_server_publickey(ss,&srv_pubkey)<0){
        return -1;
    }
    if(ssh_get_publickey_hash(srv_pubkey,SSH_PUBLICKEY_HASH_SHA1,&hash,&hlen)<0){
        return -1;
    }
    hexa = ssh_get_hexa(hash,hlen);
    switch(ssh_session_is_known_server(ss)){
        case SSH_KNOWN_HOSTS_OK:
            printf("known hosts\n");
            return 1;
        case SSH_KNOWN_HOSTS_CHANGED:
            printf("host key chaged\n");
            printf("the new key hash is:%s\n",hexa);
            return -1;
        case SSH_KNOWN_HOSTS_UNKNOWN:
            printf("the server is unknown, Do you trust\n");
            printf("the key hash is:%s\n",hexa);
            while(1){
                printf("yes or no :");
                fgets(buff,sizeof(buff),stdin);
                if(strncmp(buff,"yes",3)==0){
                        printf("get yes\n");
                        if(ssh_session_update_known_hosts(ss)<0){
                            printf("update known_hosts wrong\n");
                        }
                        else{
                            printf("update known_hosts ok");
                            return 1;
                        }
                }
                else if(strncmp(buff,"no",2)==0){
                        printf("get no\n");
                        return -1;
                }
            }

        case SSH_KNOWN_HOSTS_NOT_FOUND:
            printf("could not find host file\n");
            return -1;
        default:
            printf("enter case default\n");
            return -1;
    }
    ssh_clean_pubkey_hash(&hash);
    return -1;
}

int verify_user(ssh_session ss){
    //char *password = getpass("Password: ");
    char password[]="dsq"; 
    if(ssh_userauth_password(ss,NULL,password)!=SSH_AUTH_SUCCESS){
        printf("auth user failed\n");
        return -1;
    }
    return 1;
}


int show_remote_process(ssh_session ss){
    ssh_channel ch;
    int rc;
    char buffer[1024];
    int nbytes;
    ch = ssh_channel_new(ss);
    if(ch == NULL){
        printf("ssh_channel_new wrong\n");
        return -1;
    }

    if(ssh_channel_open_session(ch)!=SSH_OK){
        printf("ssh_channel_open_session wrong\n");
        return -1;
    }

    if(ssh_channel_request_exec(ch,"ps -ef")!=SSH_OK){
        printf("ssh_channel_request_exec wrong\n");
        return -1;
    }
    
    while(1){
        nbytes=ssh_channel_read(ch,buffer,sizeof(buffer),0);
        if(nbytes!=0&&nbytes!=SSH_ERROR){
            write(1,buffer,nbytes);
        }
        else break;
    }
    return 1;
}
